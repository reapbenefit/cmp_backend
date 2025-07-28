import json
from typing import Dict
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from llm import (
    stream_llm_with_instructor,
    run_llm_with_instructor,
    stream_llm_responses_with_instructor,
    run_llm_responses_with_instructor,
)
from models import (
    ChatHistoryMessage,
    ChatHistoryMessageWithMode,
    ActionType,
    ActionCategory,
    AIActionMetadataResponse,
    AIChatResponse,
    ActionSubCategory,
)
from openai import AsyncOpenAI
from settings import settings
from utils import extract_skill_from_action_type
from db import get_skills_data_from_names
from openinference.instrumentation import using_attributes

router = APIRouter()


@router.post("/ai/basic_action_chat", response_model=AIChatResponse)
async def basic_action_chat(chat_history: list[ChatHistoryMessage]):
    class Output(BaseModel):
        chain_of_thought: str = Field(
            description="Reflect on the chat so far to clearly identify what aspects have been covered already and what should be covered in the next question"
        )
        response: str = Field(description="The response to be given to the student")
        is_done: bool = Field(description="Whether the conversation is done")

    # client = AsyncOspenAI(api_key=settings.openai_api_key)

    async def stream_response():
        with using_attributes(
            metadata={"stage": "basic_action_chat"},
        ):
            stream = await stream_llm_responses_with_instructor(
                api_key=settings.openai_api_key,
                model="gpt-4.1-mini-2025-04-14",
                response_model=Output,
                max_output_tokens=8096,
                temperature=0.1,
                input=[
                    {
                        "role": "system",
                        "content": """You are a very sharp and thoughtful coach. 

A student has submitted an action that they have taken to solve a local problem.

Your goal is to ask 2-3 reflective questions to understand what action did they take, why did they take it, and how did they do it.

Only ask **one question at a time**, based on what the student has already shared. You should customise the phrasing of your question to make it sound specific to what the student has already said instead of keeping the questions vague or generic. 

### Important Instructions
- Keep the tone warm, conversational, and efficient. Avoid being verbose.
- You can ask a maximum of 3 questions but if the what, why and how is already covered in the first response or before 3 questions, avoid asking any more questions and mark the conversation as complete.
- Avoid repetition: Never ask a question whose answer has already been given in the chat history before (even if the student wasn't explicitly asked the question before).
- Always acknowledge the student's response (e.g. *Thanks for sharing. That helps me understand better*) without repeating their words back so that they feel heard. Remember to never ever repeat their words back.
- Handle irrelevant or unclear inputs with gentle redirection.
- If the user reply is not an answer to the current question → gently guide them back.

Example: “That’s helpful, but could you go back and tell me a bit more about what exactly you did in the action?”

- If the user asks a clarifying question about your prompt:

If you can answer it clearly → answer concisely, then return to your question.

If it’s outside your scope (e.g. platform bugs, submission issues) → say:
"That’s something the Reap Benefit team can help with. I’m here to help you reflect. So let’s go back to the question I asked..."

- If the student struggles to respond meaningfully, do not end the conversation prematurely. Instead, move on to the next best reflective question. 
- The conversation should be marked as done if either: a) the what, why and how of the action they took has been mentioned; or b) 3 reflective questions have been asked.

### Closing Behaviour
Once you have marked the conversation as done, the accompanying feedback should end the conversation on an uplifting note recognizing their contribution, summarize one key insight or strength that emerged from their answers and encourage them to keep taking action.

### Style Tip
- Do not use em-dashes (--) in your replies. Use commas or short phrases instead, as humans naturally do in conversation.
- It is critical to ask only one question at a time and not include multiple questions in a single response even if those questions are related to each other as the user is from a background where asking more than 1 question can overwhelm them.""",
                    }
                ]
                + [chat_response.model_dump() for chat_response in chat_history],
            )
            async for chunk in stream:
                content = json.dumps(chunk.model_dump()) + "\n"
                yield content

    return StreamingResponse(
        stream_response(),
        media_type="application/x-ndjson",
    )


def transform_raw_chat_history_for_detail_action_chat(
    chat_history: Dict,
) -> Dict:
    # Find the index where the last message with mode == 'basic' ends
    last_basic_idx = -1
    for idx, msg in enumerate(chat_history):
        if msg["mode"] == "basic":
            last_basic_idx = idx

        if msg["mode"] != "reflection":
            break

    # Collect all messages with mode == 'basic'
    basic_msgs = chat_history[: last_basic_idx + 1]
    reflection_msgs = chat_history[last_basic_idx + 1 :]

    basic_user_response = []
    prev_ai_message = None
    for msg in basic_msgs:
        if msg["role"] == "user":
            if prev_ai_message is not None:
                basic_user_response.append(
                    f'{msg["content"]} (response to "{prev_ai_message}")'
                )
            else:
                basic_user_response.append(msg["content"])
        else:
            prev_ai_message = msg["content"]

    basic_user_response = "\n".join(basic_user_response)

    return [
        {"role": "user", "content": basic_user_response},
    ] + [{"role": msg["role"], "content": msg["content"]} for msg in reflection_msgs]


@router.post("/ai/detail_action_chat", response_model=AIChatResponse)
async def detail_action_chat(chat_history: list[ChatHistoryMessageWithMode]):
    class Output(BaseModel):
        chain_of_thought: str = Field(
            description="Reflect on the chat so far to clearly identify what aspects have been covered already and what should be covered in the next question"
        )
        response: str = Field(description="The response to be given to the student")
        is_done: bool = Field(description="Whether the conversation is done")

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    raw_chat_history = [chat_response.model_dump() for chat_response in chat_history]
    chat_history = transform_raw_chat_history_for_detail_action_chat(raw_chat_history)

    async def stream_response():
        with using_attributes(
            metadata={"stage": "detail_action_chat"},
        ):
            stream = await stream_llm_responses_with_instructor(
                model="gpt-4.1-2025-04-14",
                response_model=Output,
                max_output_tokens=8096,
                temperature=0.1,
                input=[
                    {
                        "role": "system",
                        "content": """You are a very sharp and thoughtful coach. 

A student has submitted an action that they have taken to solve a local problem along with some basic details around the action they have taken.

Your goal is to ask more reflective questions to help the student in the following ways:
- have a full picture of the action they have taken
- reflect on how it felt, what they learned, and how it connects to their values or growth.
- stay motivated to continue taking action.

Divide the conversation into 4 phases:
1. Start with getting more details on what they did
- Where and when did the action happen?
- Who else was involved?
- What was the outcome?

Stay on this step until you have a full picture of the action. Only then move on.

2. Explore why it mattered by asking questions like:
- Why was this important to them?
- What made them want to act on this?
- What kind of impact were they hoping to create?

If they struggle to answer the question, you can gently suggest things they might have cared about (e.g. reducing waste, helping others, making a difference in their area).

3. Understand how they did it by asking about their process:
- How did they go about it?
- What steps did they follow?
- What challenges or surprises came up?
- Who supported them or made it harder?

4. Reflect on what they learned or felt  by asking reflective questions like:
- How did it feel to do this?
- What skills do they think they used or built?
- What does this action say about who they are?
- Would they do something like this again? What might they do differently?

Only ask **one question at a time**, based on what the student has already shared. You should customise the phrasing of your questions to make it sound specific to what the student has said instead of keeping them vague or generic. 

Skip any of the phases above if the chat so far has already answered that question.

Within a phase, skip any of the questions if it has already been answered in the conversation history before.

### Important Instructions
- Keep the tone warm, conversational, and efficient. Avoid being verbose.
- Aim to ask 5-7 questions but allow up to 10 if the student is responding meaningfully and more clarity or reflection is needed.
  - If needed, let them skip: “No worries, we can come back to this later.”
- Avoid repetition: Never ask a question whose answer has already been given in the chat history before (even if the student wasn't explicitly asked the question before).
- Always acknowledge the student's response (e.g. *Thanks for sharing. That helps me understand better*) without repeating their words back so that they feel heard. Remember to never ever repeat their words back.
- Handle irrelevant or unclear inputs with gentle redirection.
- If the user reply is not an answer to the current question → gently guide them back.

Example: “That’s helpful, but could you go back and tell me a bit more about what exactly how you felt after taking the action?”

- If the user asks a clarifying question about your prompt:

If you can answer it clearly → answer concisely, then return to your question.

If it’s outside your scope (e.g. platform bugs, submission issues) → say:
"That’s something the Reap Benefit team can help with. I’m here to help you reflect. So let’s go back to the question I asked..."

- If the user struggles to answer a reflective question or seems stuck, offer 2–3 possible suggestions or options based on what the student has shared so far. Phrase it as gentle guidance, not a multiple-choice test.

Example:
"If you're not sure, here are some things you might consider: Did you learn how to plan better? Work with someone new? Handle a challenge more calmly? You can pick one or add your own thoughts!"

After offering suggestions, ask the student to pick one or describe something similar that fits their experience.

If the student still struggles to respond meaningfully, do not end the conversation prematurely. Instead, move on to the next best reflective question. 

- The conversation should be marked as done if either: a) all the reflective questions have been answered; or b) 7-10 questions have been asked.
- Remember that each of their answers is a bonus on top of the basic action details they have already given before. So, treat every response as such and keep motivating them to continue responding throughout the conversation.

### Closing Behaviour
After all questions (default 7–10), end with a motivational summary (e.g. “Thanks for sharing this story. You showed leadership and creativity — especially when you brought your community together to clean the well.”), offer soft nudges (e.g. “Would you like this story to be verified and shared with the wider Solve Ninja community?”, " “You’ve done something meaningful. If you’re open to mentoring others or need help with next steps, we’re here.”, etc.) if applicable, and end with a kind, motivational message based on what they shared along with highlight at least one clear strength (e.g. “You showed creativity and care. That’s inspiring.”).
- Do not ask “Anything else?” or leave the conversation open-ended.

### Style Tip
* Do not use em-dashes (--) in your replies. Use commas or short phrases instead, as humans naturally do in conversation.""",
                    }
                ]
                + chat_history,
            )
            async for chunk in stream:
                content = json.dumps(chunk.model_dump()) + "\n"
                yield content

    return StreamingResponse(
        stream_response(),
        media_type="application/x-ndjson",
    )


def transform_chat_history_to_prompt(chat_history: list[ChatHistoryMessage]) -> str:
    return "\n".join(
        [
            f"{chat_response.role.capitalize()}: {chat_response.content}"
            for chat_response in chat_history
        ]
    )


@router.post("/ai/extract_action_metadata", response_model=AIActionMetadataResponse)
async def extract_action_metadata(chat_history: list[ChatHistoryMessage]):
    class Output(BaseModel):
        action_title: str = Field(
            description="A short title for the action (less than 5 words)"
        )
        action_description: str = Field(
            description="A concise description of the action that the young person took (less than 50 words)"
        )
        action_type: ActionType = Field(description="The type of the action")
        action_subtype: ActionType = Field(description="The subtype of the action")
        action_category: ActionCategory = Field(
            description="The category of the action"
        )
        action_subcategory: ActionSubCategory = Field(
            description="The subcategory of the action"
        )

    parser = PydanticOutputParser(pydantic_object=Output)
    format_instructions = parser.get_format_instructions()

    system_prompt = f"""Extract the action type, action category, action title and action description from the given conversation history of a young person describing their actions to solve a local civic problem. Use the provided lists to identify the correct action type and category.\n\n# Steps\n\n1. **Review the Conversation:** Thoroughly read the conversation history to understand the actions the young person has described.\n2. **Identify Action Type:** Determine the action type from the conversation, ensuring it aligns with one of the listed action types. Focus on specific verbs or phrases that indicate the nature of the activity.\n3. **Identify Action Category:** Determine the action category based on the topic or area addressed in the conversation. Use the given list to find the most suitable category.\n4. **Ensure Uniqueness:** Each task should conclude with one unique action type and one unique action category.\n\n### Output format\n\n{format_instructions}"""

    chat_history_prompt = transform_chat_history_to_prompt(chat_history)

    with using_attributes(
        metadata={"stage": "action_metadata"},
    ):
        response = await run_llm_responses_with_instructor(
            api_key=settings.openai_api_key,
            # model="gpt-4o-audio-preview-2025-06-03",
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": chat_history_prompt,
                },
            ],
            response_model=Output,
            max_output_tokens=8096,
        )

    skills = extract_skill_from_action_type(response.action_type)
    skills = await get_skills_data_from_names(skills)

    class SkillRelevance(BaseModel):
        skill: str = Field(
            description="The skill whose relevance to the action needs to be described"
        )
        relevance: str = Field(
            description="Concise description of how the skill is relevant to the action based on the chat history; no need to begin with 'The student' or 'The action'; directly describe the skill relevance"
        )
        response: str = Field(
            description="Description of the skill relevance addressed to the student"
        )

    class SkillRelevanceOutput(BaseModel):
        skill_relevances: list[SkillRelevance] = Field(
            description="The relevance of the skills to the action"
        )

    parser = PydanticOutputParser(pydantic_object=SkillRelevanceOutput)
    format_instructions = parser.get_format_instructions()

    skill_relevance_system_prompt = f"""Analyze a student's action and the corresponding conversation history to provide a personalized, one-line description of how each listed skill is demonstrated in that context as 2 fields for each skill: `relevance`, for a person viewing the student's action; `response`, for the student.\n\nReview the conversation thoroughly and connect specific elements of it to the skills listed. Each description should clearly link an aspect of the conversation to the demonstration of a particular skill.\n\n# Examples\n\n**Example** (shortened for illustration purposes; real examples should detail specific parts of the conversation):\n- **Problem-Solving**: The student's question about alternative solutions shows proactive engagement.\n\n- **Communication**: The clear explanation of their thought process demonstrates effective communication.\n\n- **Critical Thinking**: The student’s questioning of assumptions indicates critical evaluation of information.\n\n# Notes\n\nConsider nuances such as tone, clarity, and depth of the conversation that might subtly demonstrate skills. Each description should be crafted to reflect both the conversation content and the student’s unique expression of the skill.\n\n### Output format\n\n{format_instructions}"""

    with using_attributes(
        metadata={
            "stage": "skill_relevance",
            "action_type": response.action_type,
            "action_category": response.action_category,
            "action_subcategory": response.action_subcategory,
            "action_subtype": response.action_subtype,
            "action_title": response.action_title,
            "action_description": response.action_description,
        },
    ):
        skill_relevance_response = await run_llm_responses_with_instructor(
            api_key=settings.openai_api_key,
            # model="gpt-4o-audio-preview-2025-06-03",
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {
                    "role": "system",
                    "content": skill_relevance_system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Conversation history:\n```\n{chat_history_prompt}\n```\n\nSkills: {', '.join([skill['name'] for skill in skills])}",
                },
            ],
            response_model=SkillRelevanceOutput,
            max_output_tokens=8096,
        )

    skill_to_index = {skill["name"]: index for index, skill in enumerate(skills)}

    for skill_relevance in skill_relevance_response.skill_relevances:
        skills[skill_to_index[skill_relevance.skill]][
            "relevance"
        ] = skill_relevance.relevance
        skills[skill_to_index[skill_relevance.skill]][
            "response"
        ] = skill_relevance.response

    return {
        "action_title": response.action_title,
        "action_description": response.action_description,
        "action_type": response.action_type,
        "action_category": response.action_category,
        "action_subcategory": response.action_subcategory,
        "action_subtype": response.action_subtype,
        "skills": skills,
    }
