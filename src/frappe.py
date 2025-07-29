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


def get_user_profile(email: str):
    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.profile.get_user_profile"

    payload = json.dumps({"username": email})

    headers = {
        "Authorization": f"token {settings.frappe_backend_client_id}:{settings.frappe_backend_client_secret}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    return response.json()["message"]


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


async def event_exists(action_uuid: str):
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            'SELECT name FROM "tabEvents" WHERE name = $1',
            action_uuid,
        )
        return row is not None
