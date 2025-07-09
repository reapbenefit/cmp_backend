import requests
import json
from settings import settings
from db import get_action_for_user


async def create_action_on_frappe(action_id: int):
    url = f"{settings.frappe_backend_base_url}/method/solve_ninja.api.events.create_events"

    action_details = await get_action_for_user(action_id)

    payload = json.dumps(
        {
            "title": action_details["title"],
            "type": action_details["type"],
            "category": action_details["category"],
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

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
