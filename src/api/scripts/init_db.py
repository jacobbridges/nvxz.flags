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


async def build_session_table(conn):
    """
    Build/Maintain the session table.
    """
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS session (
        session_id TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    )
    """)
    await conn.commit()


async def build_project_table(conn):
    """
    Build/Maintain the project table.
    """
    # Build initial table for project
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS project (
        id INTEGER PRIMARY KEY ASC,
        name TEXT NOT NULL,
        user_id INTEGER,
        domain_whitelist TEXT,
        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """)
    await conn.commit()

    # Add unique index for name + user_id
    await conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS uniq_projectname ON project (user_id, name COLLATE NOCASE);
    """)
    await conn.commit()


async def load_db():
    """
    Build/Maintain the database structure.
    """
    async with get_conn() as conn:
        await build_user_table(conn)
        await build_session_table(conn)
        await build_project_table(conn)


def main():
    asyncio.run(load_db())
