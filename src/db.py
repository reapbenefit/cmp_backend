from collections import defaultdict
from contextlib import asynccontextmanager
from typing import List
import os
from os.path import exists
import sqlite3
import uuid
import aiosqlite
from config import (
    sqlite_db_path,
    chat_history_table_name,
    users_table_name,
    communities_table_name,
    actions_table_name,
    action_categories_table_name,
    action_types_table_name,
    skills_table_name,
    action_skills_table_name,
)
from models import (
    SignupUserRequest,
    CreateCommunityRequest,
    UpdateUserProfileRequest,
    CreateActionRequest,
    AddChatMessageRequest,
    Skill,
    UpdateActionRequest,
)
from utils import skill_to_name


@asynccontextmanager
async def get_new_db_connection():
    conn = None
    try:
        conn = await aiosqlite.connect(sqlite_db_path)
        await conn.execute("PRAGMA synchronous=NORMAL;")
        yield conn
    except Exception as e:
        if conn:
            await conn.rollback()  # Rollback on any exception
        raise  # Re-raise the exception to propagate the error
    finally:
        if conn:
            await conn.close()


def set_db_defaults():
    conn = sqlite3.connect(sqlite_db_path)

    current_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]

    if current_mode.lower() != "wal":
        settings = "PRAGMA journal_mode = WAL;"

        conn.executescript(settings)
        print("Defaults set.")
    else:
        print("Defaults already set.")


async def create_tables(cursor):
    """Create the necessary tables for the application"""

    # Create users table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {users_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            location_state TEXT,
            location_city TEXT,
            location_country TEXT,
            profile_picture TEXT,
            bio TEXT,
            highlight TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    # Create actions table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {actions_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            title TEXT,
            description TEXT,
            user_id INTEGER NOT NULL,
            status TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
            is_pinned BOOLEAN DEFAULT FALSE,
            category TEXT,
            type TEXT,
            time_invested_value INTEGER,
            time_invested_unit TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Create chat_history table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {chat_history_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            response_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (action_id) REFERENCES actions (id)
        )
    """
    )

    # Create index on action_id column for chat_history table
    await cursor.execute(
        f"""
        CREATE INDEX IF NOT EXISTS idx_chat_history_action_id ON {chat_history_table_name} (action_id)
    """
    )

    # Create communities table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {communities_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Create skills table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {skills_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            label TEXT
        )
    """
    )

    # Create action_skills table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {action_skills_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            summary TEXT,
            FOREIGN KEY (action_id) REFERENCES actions (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id)
        )
    """
    )

    # Create index on skill_id column for action_skills table
    await cursor.execute(
        f"""
        CREATE INDEX IF NOT EXISTS idx_action_skills_skill_id ON {action_skills_table_name} (skill_id)
    """
    )

    # Create index on action_id column for action_skills table
    await cursor.execute(
        f"""
        CREATE INDEX IF NOT EXISTS idx_action_skills_action_id ON {action_skills_table_name} (action_id)
    """
    )


async def init_db():
    # Ensure the database folder exists
    db_folder = os.path.dirname(sqlite_db_path)
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    if not exists(sqlite_db_path):
        # only set the defaults the first time
        set_db_defaults()

    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        try:
            # Check if any table is missing and create tables if needed
            await create_tables(cursor)
            await conn.commit()

        except Exception as exception:
            # delete db
            os.remove(sqlite_db_path)
            raise exception


async def verify_user_credentials(email: str, password: str) -> bool:
    """Verify user credentials against the database."""
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, username, first_name, last_name, email FROM {users_table_name} WHERE email = ? AND password = ?",
            (email, password),
        )
        user_record = await result.fetchone()

        if user_record:
            return {
                "id": user_record[0],
                "username": user_record[1],
                "first_name": user_record[2],
                "last_name": user_record[3],
                "email": user_record[4],
            }

        return None


async def create_user(user: SignupUserRequest):
    """Create a new user in the database."""
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        # Check if username already exists
        result = await cursor.execute(
            f"SELECT id FROM {users_table_name} WHERE username = ?",
            (user.username,),
        )
        existing_username = await result.fetchone()
        if existing_username:
            raise Exception("Username already exists")

        # Check if email already exists
        result = await cursor.execute(
            f"SELECT id FROM {users_table_name} WHERE email = ?",
            (user.email,),
        )
        existing_email = await result.fetchone()
        if existing_email:
            raise Exception("Email already exists")

        await cursor.execute(
            f"INSERT INTO {users_table_name} (email, password, first_name, last_name, username) VALUES (?, ?, ?, ?, ?)",
            (user.email, user.password, user.first_name, user.last_name, user.username),
        )

        await conn.commit()

        await cursor.execute(
            f"SELECT id, first_name, last_name, username, email FROM {users_table_name} WHERE id = ?",
            (cursor.lastrowid,),
        )
        new_user = await cursor.fetchone()

        return {
            "id": new_user[0],
            "first_name": new_user[1],
            "last_name": new_user[2],
            "username": new_user[3],
            "email": new_user[4],
        }


async def get_user_portfolio(username: str):
    """Get the portfolio of a user."""
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, first_name, last_name, username, email, is_verified, bio, location_state, location_city, location_country, highlight FROM {users_table_name} WHERE username = ?",
            (username,),
        )

        user = await result.fetchone()
        if not user:
            raise Exception("User not found")

        communities_result = await cursor.execute(
            f"SELECT id, name, description, link FROM communities WHERE user_id = ?",
            (user[0],),
        )
        communities = await communities_result.fetchall()
        communities = [
            {
                "id": community[0],
                "name": community[1],
                "description": community[2],
                "link": community[3],
            }
            for community in communities
        ]

        actions_result = await cursor.execute(
            f"""
            SELECT a.id, a.uuid, a.title, a.description, a.is_verified, a.is_pinned, a.category, a.type, a.created_at
            FROM {actions_table_name} a
            WHERE a.user_id = ? AND a.status = 'published'
            ORDER BY a.created_at DESC
            """,
            (user[0],),
        )
        actions_data = await actions_result.fetchall()

        actions = []
        skill_id_to_data = {}

        for action_data in actions_data:
            action_id = action_data[0]

            skills_result = await cursor.execute(
                f"""
                SELECT s.id, s.name, s.label, acs.summary
                FROM {action_skills_table_name} acs
                INNER JOIN {skills_table_name} s ON acs.skill_id = s.id
                WHERE acs.action_id = ?
                ORDER BY s.name ASC
                """,
                (action_id,),
            )

            skills_data = await skills_result.fetchall()

            skills = [
                {
                    "id": skill[0],
                    "name": skill[1],
                    "label": skill[2],
                    "summary": skill[3],
                }
                for skill in skills_data
            ]

            for skill in skills:
                if skill["id"] not in skill_id_to_data:
                    skill_id_to_data[skill["id"]] = {
                        "id": skill["id"],
                        "name": skill["name"],
                        "label": skill["label"],
                        "history": [],
                    }

                skill_id_to_data[skill["id"]]["history"].append(
                    {"action_title": action_data[2], "summary": skill["summary"]}
                )

            chat_history_result = await cursor.execute(
                f"SELECT id, role, content, response_type, created_at FROM {chat_history_table_name} WHERE action_id = ?",
                (action_id,),
            )
            chat_history_data = await chat_history_result.fetchall()

            chat_history = [
                {
                    "id": chat[0],
                    "role": chat[1],
                    "content": chat[2],
                    "response_type": chat[3],
                    "created_at": chat[4],
                }
                for chat in chat_history_data
                if chat[1] in ["user", "assistant"]
            ]

            action = {
                "id": action_data[0],
                "uuid": action_data[1],
                "title": action_data[2],
                "description": action_data[3],
                "is_verified": action_data[4],
                "is_pinned": action_data[5],
                "category": action_data[6],
                "type": action_data[7],
                "created_at": action_data[8],
                "skills": skills,
                "chat_history": chat_history,
            }
            actions.append(action)

        skills = []

        for _, data in skill_id_to_data.items():
            skills.append(data)

        return {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "username": user[3],
            "email": user[4],
            "is_verified": user[5],
            "bio": user[6],
            "location_state": user[7],
            "location_city": user[8],
            "location_country": user[9],
            "highlight": user[10],
            "communities": communities,
            "actions": actions,
            "skills": skills,
        }


async def create_community_for_user(community: CreateCommunityRequest):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        await cursor.execute(
            f"INSERT INTO {communities_table_name} (name, description, link, user_id) VALUES (?, ?, ?, ?)",
            (community.name, community.description, community.link, community.user_id),
        )

        await conn.commit()

        new_community = await cursor.execute(
            f"SELECT id, name, description, link FROM {communities_table_name} WHERE id = ?",
            (cursor.lastrowid,),
        )
        new_community = await new_community.fetchone()

        return {
            "id": new_community[0],
            "name": new_community[1],
            "description": new_community[2],
            "link": new_community[3],
        }


async def update_user_profile_for_user(
    username: str, request: UpdateUserProfileRequest
):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        await cursor.execute(
            f"UPDATE {users_table_name} SET bio = ?, location_state = ?, location_city = ? WHERE username = ?",
            (
                request.bio,
                request.location_state,
                request.location_city,
                username,
            ),
        )

        await conn.commit()

        return await get_user_portfolio(username)


async def get_action_for_user(action_id: int):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, uuid, title, description, status, is_verified, created_at, category, type FROM {actions_table_name} WHERE id = ?",
            (action_id,),
        )

        action = await result.fetchone()
        if not action:
            raise Exception("Action not found")

        return {
            "id": action[0],
            "uuid": action[1],
            "title": action[2],
            "description": action[3],
            "status": action[4],
            "is_verified": action[5],
            "created_at": action[6],
            "category": action[7],
            "type": action[8],
        }


async def create_action_for_user(action: CreateActionRequest):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        action_uuid = str(uuid.uuid4())

        await cursor.execute(
            f"INSERT INTO {actions_table_name} (user_id, title, status, uuid) VALUES (?, ?, ?, ?)",
            (action.user_id, action.title, "draft", action_uuid),
        )

        action_id = cursor.lastrowid

        await cursor.execute(
            f"INSERT INTO {chat_history_table_name} (action_id, role, content, response_type) VALUES (?, ?, ?, ?)",
            (action_id, "user", action.user_message, "text"),
        )

        await conn.commit()

        return await get_action_for_user(action_id)


async def get_action_chat_history(action_uuid: str):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, role, content, response_type, created_at FROM {chat_history_table_name} WHERE action_id = (SELECT id FROM {actions_table_name} WHERE uuid = ?) ORDER BY created_at ASC",
            (action_uuid,),
        )

        chat_history = await result.fetchall()

        return [
            {
                "id": chat[0],
                "role": chat[1],
                "content": chat[2],
                "response_type": chat[3],
                "created_at": chat[4],
            }
            for chat in chat_history
        ]


async def get_all_chat_sessions_for_user(user_id: int):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"""
            SELECT a.uuid, a.title, MAX(c.created_at) as last_message_time
            FROM {actions_table_name} a
            INNER JOIN {chat_history_table_name} c ON a.id = c.action_id
            WHERE a.user_id = ?
            GROUP BY a.id, a.uuid, a.title
            ORDER BY last_message_time DESC
            """,
            (user_id,),
        )

        chat_sessions = await result.fetchall()

        return [
            {
                "uuid": session[0],
                "title": session[1],
                "last_message_time": session[2],
            }
            for session in chat_sessions
        ]


async def add_messages_to_action_history(
    action_uuid: str, messages: List[AddChatMessageRequest]
):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        for message in messages:
            await cursor.execute(
                f"INSERT INTO {chat_history_table_name} (action_id, role, content, response_type) VALUES ((SELECT id FROM {actions_table_name} WHERE uuid = ?), ?, ?, ?)",
                (action_uuid, message.role, message.content, message.response_type),
            )

        await conn.commit()

        return await get_action_chat_history(action_uuid)


async def get_skills_data_from_names(skill_names: List[str]) -> List[Skill]:
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, name, label FROM {skills_table_name} WHERE name IN ({', '.join([f'?' for _ in skill_names])})",
            skill_names,
        )

        skills = await result.fetchall()

        return [
            {
                "id": skill[0],
                "name": skill[1],
                "label": skill[2],
            }
            for skill in skills
        ]


async def update_action_for_user(action_uuid: str, request: UpdateActionRequest):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        action_id = await cursor.execute(
            f"SELECT id FROM {actions_table_name} WHERE uuid = ?",
            (action_uuid,),
        )
        action_id = (await action_id.fetchone())[0]

        await cursor.execute(
            f"UPDATE {actions_table_name} SET title = ?, description = ?, status = ?, category = ?, type = ? WHERE id = ?",
            (
                request.title,
                request.description,
                request.status,
                request.category,
                request.type,
                action_id,
            ),
        )

        if request.skills:
            await cursor.execute(
                f"DELETE FROM {action_skills_table_name} WHERE action_id = ?",
                (action_id,),
            )

            values = []
            for skill in request.skills:
                values.append((action_id, skill.id, skill.summary))

            await cursor.executemany(
                f"INSERT INTO {action_skills_table_name} (action_id, skill_id, summary) VALUES (?, ?, ?)",
                values,
            )

        await conn.commit()

        return await get_action_for_user(action_id)


async def has_skills():
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT COUNT(*) FROM {skills_table_name}",
        )
        return (await result.fetchone())[0] > 0


async def seed_skills():
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        values = []
        for skill_name, skill_label in skill_to_name.items():
            values.append((skill_name, skill_label))

        await cursor.executemany(
            f"INSERT INTO {skills_table_name} (name, label) VALUES (?, ?)",
            values,
        )

        await conn.commit()
