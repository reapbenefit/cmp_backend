from typing import List
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from models import (
    Portfolio,
    LoginRequest,
    SignupUserRequest,
    CreateCommunityRequest,
    UserCommunity,
    UpdateUserProfileRequest,
    CreateActionRequest,
    Action,
    ChatMessage,
    ChatSession,
    AddChatMessageRequest,
    CreateActionResponse,
)
import traceback
from settings import settings
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from ai import router, get_basic_action_response_from_chat_history
from db import (
    create_user,
    get_user_portfolio,
    create_community_for_user,
    update_user_profile_for_user,
    create_action_for_user,
    get_action_chat_history,
    add_messages_to_action_history,
    get_all_chat_sessions_for_user,
    get_user_id_by_email,
)
from frappe import login_user, get_user_profile
from llm import stream_llm_with_instructor

app = FastAPI()

app.include_router(router)


# Add CORS middleware to allow cross-origin requests (for frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(request: LoginRequest):
    response = login_user(request.email, request.password)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cookies = response.cookies
    response = response.json()

    user_id = await get_user_id_by_email(request.email)

    if user_id is None:
        name_parts = response["full_name"].split(" ")
        first_name = name_parts[0]
        last_name = ""

        if len(name_parts) > 1:
            last_name = name_parts[-1]

        new_user = await create_user(
            {
                "email": request.email,
                "first_name": first_name,
                "last_name": last_name,
                "username": request.email,
            }
        )
        user_id = new_user["id"]

    return {
        "name": response["full_name"],
        "id": user_id,
        "email": request.email,
        "sid": cookies["sid"],
    }


# @app.post("/signup")
# async def signup(request: SignupUserRequest):
#     try:
#         new_user = await create_user(request)
#         return new_user
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@app.get("/portfolio/{username}")
async def get_portfolio(username: str) -> Portfolio:
    try:
        return await get_user_portfolio(username=username)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/communities")
async def create_community(request: CreateCommunityRequest) -> UserCommunity:
    try:
        return await create_community_for_user(request)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/users/{username}")
async def update_user_profile(
    username: str, request: UpdateUserProfileRequest
) -> Portfolio:
    try:
        return await update_user_profile_for_user(username, request)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/actions")
async def create_action(request: CreateActionRequest) -> CreateActionResponse:
    try:
        ai_response_stream = await get_basic_action_response_from_chat_history(
            [
                {
                    "content": request.user_message,
                    "role": "user",
                }
            ]
        )
        ai_response = ""
        async for chunk in ai_response_stream:
            ai_response = chunk

        ai_response = ai_response.model_dump()

        action = await create_action_for_user(
            "New Action",
            request.user_email,
            request.user_message,
            json.dumps(ai_response),
        )

        return {
            "ai_response": ai_response,
            "action": action,
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/chat_history/{action_uuid}")
async def get_chat_history_for_action(action_uuid: str) -> List[ChatMessage]:
    try:
        return await get_action_chat_history(action_uuid)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/chat_history/")
async def get_all_chats_for_user(user_id: int) -> List[ChatSession]:
    try:
        return await get_all_chat_sessions_for_user(user_id)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/chat_messages/{action_uuid}")
async def add_chat_messages_for_action(
    action_uuid: str, messages: List[AddChatMessageRequest]
):
    try:
        return await add_messages_to_action_history(action_uuid, messages)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{email}/username")
async def get_username(email: str) -> str:
    try:
        user_profile = get_user_profile(email)
        return user_profile["current_user"]["username"]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}
