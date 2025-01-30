import asyncio

from api.core.db import get_conn


async def build_user_table(conn):
    """
    Build/Maintain the user table.
    """
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY ASC,
        username TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )
    """)
    await conn.commit()


async def load_db():
    """
    Build/Maintain the database structure.
    """
    async with get_conn() as conn:
        await build_user_table(conn)


def main():
    asyncio.run(load_db())
