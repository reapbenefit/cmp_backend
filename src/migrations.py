from db import get_new_db_connection
from config import users_table_name


async def migrate_users_table():
    async with get_new_db_connection() as conn:
        cursor = await conn.cursor()

        # Check if the 'password' column exists before attempting to drop it
        result = await cursor.execute(f"PRAGMA table_info({users_table_name})")
        columns = await result.fetchall()
        column_names = [col[1] for col in columns]
        if "password" in column_names:
            await cursor.execute(f"ALTER TABLE {users_table_name} DROP COLUMN password")

        await conn.commit()


async def run_migrations():
    await migrate_users_table()


if __name__ == "__main__":
    import asyncio

    asyncio.run(migrate_users_table())
