from contextlib import asynccontextmanager
import os
from os.path import exists
import sqlite3
import aiosqlite
from config import (
    sqlite_db_path,
    chat_history_table_name,
    sessions_table_name,
    users_table_name,
    communities_table_name,
    actions_table_name,
    action_categories_table_name,
    action_types_table_name,
    skills_table_name,
    action_skills_table_name,
)
from models import SignupUserRequest, CreateCommunityRequest, UpdateUserProfileRequest


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

    # Create sessions table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {sessions_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Create chat_history table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {chat_history_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            response_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
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

    # Create actions table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {actions_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            status TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
            is_pinned BOOLEAN DEFAULT FALSE,
            category_id INTEGER,
            type_id INTEGER,
            time_invested_value INTEGER,
            time_invested_unit TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
            FOREIGN KEY (category_id) REFERENCES action_categories (id)
            FOREIGN KEY (type_id) REFERENCES action_types (id)
        )
    """
    )

    # Create action_skills table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {action_skills_table_name} (
            action_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            summary TEXT,
            PRIMARY KEY (action_id, skill_id),
            FOREIGN KEY (action_id) REFERENCES actions (id)
        )
    """
    )

    # Create action_categories table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {action_categories_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """
    )

    # Create action_types table
    await cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {action_types_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
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
            icon TEXT
        )
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
            tables_to_check = [
                users_table_name,
                sessions_table_name,
                chat_history_table_name,
                communities_table_name,
            ]
            missing_tables = []

            for table_name in tables_to_check:
                result = await cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,),
                )
                if not await result.fetchone():
                    missing_tables.append(table_name)

            if missing_tables:
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
            f"SELECT id FROM {users_table_name} WHERE email = ? AND password = ?",
            (email, password),
        )
        user_record = await result.fetchone()

        if user_record:
            return {"id": user_record[0], "email": email}

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


async def get_user_portfolio(user_id: int):
    """Get the portfolio of a user."""
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        result = await cursor.execute(
            f"SELECT id, first_name, last_name, username, email, is_verified, bio, location_state, location_city, location_country FROM {users_table_name} WHERE id = ?",
            (user_id,),
        )

        user = await result.fetchone()

        communities_result = await cursor.execute(
            f"SELECT id, name, description, link FROM communities WHERE user_id = ?",
            (user_id,),
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

        if not user:
            raise Exception("User not found")

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
            "communities": communities,
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


async def update_user_profile_for_user(user_id: int, request: UpdateUserProfileRequest):
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        await cursor.execute(
            f"UPDATE {users_table_name} SET bio = ?, location_state = ?, location_city = ? WHERE id = ?",
            (
                request.bio,
                request.location_state,
                request.location_city,
                user_id,
            ),
        )

        await conn.commit()

        return await get_user_portfolio(user_id)
