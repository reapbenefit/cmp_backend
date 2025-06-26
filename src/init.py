#!/usr/bin/env python3
import asyncio
from db import init_db


async def main():
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
