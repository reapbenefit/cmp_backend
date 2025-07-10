#!/usr/bin/env python3
import asyncio
from db import init_db, has_skills, seed_skills
from migrations import run_migrations


async def main():
    await init_db()

    await run_migrations()

    if not await has_skills():
        await seed_skills()


if __name__ == "__main__":
    asyncio.run(main())
