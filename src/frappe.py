import requests
import json
from fastapi import HTTPException
import asyncpg
from settings import settings
from typing import Literal
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_connection():
    conn = await asyncpg.connect(settings.database_url)
    try:
        yield conn
    finally:
        await conn.close()


async def add_message_to_chat_history(
    action_uuid: str, user_email: str, role: str, content: str, response_type: str
):
    url = f"{settings.frappe_backend_base_url}/resource/Chat%20History"

    payload = json.dumps(
        {
            "event_id": action_uuid,
            "user": user_email,
            "role": role,
            "content": content,
            "response_type": response_type,
        }
    )
    headers = {
        "Authorization": f"token {settings.frappe_backend_client_id}:{settings.frappe_backend_client_secret}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(
            f"Failed to add message to chat history: {response.text} for action {action_uuid}"
        )

    return response.json()


def login_user(email: str, password: str):
    url = f"{settings.frappe_backend_base_url}/method/login"

    payload = json.dumps({"usr": email, "pwd": password})
    headers = {
        "Content-Type": "application/json",
    }

    return requests.request("POST", url, headers=headers, data=payload)


def login_user_with_sso(code: str):
    url = f"{settings.frappe_backend_base_url}/method/frappe.integrations.oauth2.get_token"

    payload = f"grant_type=authorization_code&code={code}&redirect_uri={settings.frappe_sso_redirect_uri}&client_id={settings.frappe_sso_client_id}&client_secret={settings.frappe_sso_client_secret}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    return requests.request("POST", url, headers=headers, data=payload)


def get_user_profile_from_token(token: str):
    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.profile.get_user_profile"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    return response.json()["message"]


def get_user_profile_from_username(username: str):
    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.profile.get_user_profile"

    headers = {
        "Authorization": f"token {settings.frappe_backend_client_id}:{settings.frappe_backend_client_secret}",
        "Content-Type": "application/json",
    }

    payload = json.dumps({"username": username})

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    return response.json()["message"]


def get_user_portfolio(username: str):
    """Get the portfolio of a user from Frappe backend in the same format as the database version."""
    frappe_data = get_user_profile_from_username(username)

    current_user = frappe_data.get("current_user", {})
    actions_data = frappe_data.get("actions", [])
    skills_data = frappe_data.get("skills", [])
    skill_assignment_log = frappe_data.get("skill_assignment_log", [])

    # Transform user data to match database format
    user = {
        "first_name": current_user.get("first_name") or "",
        "last_name": current_user.get("last_name") or "",
        "username": current_user.get("username") or "",
        "email": current_user.get("email", ""),
        "is_verified": current_user.get("is_verified", False) or False,
        "bio": current_user.get("bio", ""),
        "image": current_user.get("user_image", "") or "",
        "location_state": current_user.get("state", ""),
        "location_city": current_user.get("city", ""),
        "location_country": current_user.get("location", ""),
        "highlight": current_user.get("highlighted_action", {}).get("description", ""),
    }

    expert_reviews = frappe_data.get("reviews", [])

    user["expert_reviews"] = []

    # Fix the typo in "desigantion" to "designation" in expert reviews
    for review in expert_reviews:
        for key in [
            "review_title",
            "reviewer_name",
            "designation",
            "comment",
            "organisation",
        ]:
            if not review[key]:
                continue

        user["expert_reviews"].append(review)

        if "desigantion" in review:
            review["designation"] = review.pop("desigantion")

    # Create a mapping of skill names to skill data for easy lookup
    skill_name_to_data = {}
    for i, skill_data in enumerate(skills_data):
        skill_name = skill_data["name"]
        skill_name_to_data[skill_name] = {
            "id": i + 1,
            "name": skill_name.replace(" ", "_").lower(),
            "label": skill_name,
            "history": [],
        }

    # Create a mapping of action event_id to action title for skill history
    action_id_to_title = {
        action.get("event_id", ""): action.get("title", "") for action in actions_data
    }

    # First, deduplicate skill assignment log entries
    # Group by (badge, reference_name) combo and select the best entry
    deduplicated_log = {}
    for log_entry in skill_assignment_log:
        skill_name = log_entry.get("badge", "")
        action_event_id = log_entry.get("reference_name", "")
        reason = log_entry.get("reason", "")

        key = (skill_name, action_event_id)

        if key not in deduplicated_log:
            deduplicated_log[key] = log_entry
        else:
            # Prefer entry with non-empty reason
            existing_reason = deduplicated_log[key].get("reason", "")
            if not existing_reason and reason:
                deduplicated_log[key] = log_entry
            # If both have reasons or both are empty, keep the existing one

    # Process the deduplicated skill assignment log to build skill history and action-skill relationships
    action_skills_map = {}  # Maps action event_id to list of skills
    action_first_skill_creation = (
        {}
    )  # Maps action event_id to creation time of first skill

    for log_entry in deduplicated_log.values():
        skill_name = log_entry.get("badge", "")
        action_event_id = log_entry.get("reference_name", "")
        reason = log_entry.get("reason", "")
        creation_time = log_entry.get("creation", "")

        # Track the first skill creation time for each action
        if action_event_id not in action_first_skill_creation:
            action_first_skill_creation[action_event_id] = creation_time
        else:
            # Keep the earliest creation time
            if creation_time < action_first_skill_creation[action_event_id]:
                action_first_skill_creation[action_event_id] = creation_time

        # Add to skill history if skill exists
        if skill_name in skill_name_to_data:
            action_title = action_id_to_title.get(action_event_id, "")
            skill_name_to_data[skill_name]["history"].append(
                {"action_title": action_title, "summary": reason}
            )

        # Build action-skill mapping
        if action_event_id not in action_skills_map:
            action_skills_map[action_event_id] = []

        if skill_name in skill_name_to_data:
            skill_info = skill_name_to_data[skill_name]
            action_skills_map[action_event_id].append(
                {
                    "id": skill_info["id"],
                    "name": skill_info["name"],
                    "label": skill_info["label"],
                    "relevance": reason,
                }
            )

    # Transform actions data with populated skills
    actions = []
    for action_data in actions_data:
        event_id = action_data.get("event_id", "")

        # Use the first skill creation time as the action's created_at, fallback to action creation time
        created_at = action_first_skill_creation.get(
            event_id, action_data.get("creation", "")
        )

        # Transform action to match database format
        action = {
            "uuid": event_id,
            "title": action_data.get("title", ""),
            "hours_invested": action_data.get("hours_invested", None),
            "description": action_data.get("description", ""),
            "is_verified": action_data.get("verified_by") is not None,
            "is_pinned": False,
            "category": action_data.get("category", ""),
            "type": action_data.get("type", ""),
            "created_at": created_at,
            "skills": action_skills_map.get(
                event_id, []
            ),  # Populate skills from skill assignment log
        }

        actions.append(action)

    # Convert skill data to list format
    skills = list(skill_name_to_data.values())

    return {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "email": user["email"],
        "image": user["image"],
        "is_verified": user["is_verified"],
        "bio": user["bio"],
        "location_state": user["location_state"],
        "location_city": user["location_city"],
        "location_country": user["location_country"],
        "highlight": user["highlight"],
        "communities": [],  # Ignoring communities as requested
        "actions": actions,
        "skills": skills,
        "expert_reviews": user["expert_reviews"],
    }


async def create_or_update_action_on_frappe(
    action_id: int,
    action_uuid: str,
    subcategory: str,
    subtype: str,
    mode: Literal["create", "update"] = "create",
):
    from db import get_action_for_user

    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.events.create_events"

    action_details = await get_action_for_user(action_id)

    payload = json.dumps(
        {
            "event_id": action_uuid,
            "title": action_details["title"],
            "type": action_details["type"],
            "category": action_details["category"],
            "subcategory": subcategory,
            "sub_type": subtype,
            "user": action_details["user"]["email"],
            "description": action_details["description"],
            "source": "ConversationalBot",
            "skills": {
                skill["label"]: skill["summary"] for skill in action_details["skills"]
            },
        }
    )
    headers = {
        "Authorization": f"token {settings.frappe_backend_client_id}:{settings.frappe_backend_client_secret}",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST" if mode == "create" else "PUT", url, headers=headers, data=payload
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to create action on frappe: {response.text} for action {action_uuid}"
        )


def update_action_hours_invested_on_frappe(
    action_uuid: str,
    hours_invested_value: int,
):
    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.events.create_events"

    payload = json.dumps(
        {
            "event_id": action_uuid,
            "hours_invested": hours_invested_value,
        }
    )
    headers = {
        "Authorization": f"token {settings.frappe_backend_client_id}:{settings.frappe_backend_client_secret}",
        "Content-Type": "application/json",
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(
            f"Failed to update action hours invested on frappe: {response.text} for action {action_uuid}"
        )


async def event_exists(action_uuid: str):
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            'SELECT name FROM "tabEvents" WHERE name = $1',
            action_uuid,
        )
        return row is not None
