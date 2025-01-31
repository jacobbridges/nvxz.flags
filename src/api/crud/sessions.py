from api.core.db import get_conn
from api.schemas import User


async def create_session(username: str, session_id: str):
    async with get_conn() as conn:
        await conn.execute("INSERT INTO session (username, session_id) VALUES (?, ?)", (username, session_id))
        await conn.commit()


async def delete_session(session_id: str):
    async with get_conn() as conn:
        await conn.execute("DELETE FROM session WHERE session_id = ?", (session_id,))
        await conn.commit()


async def delete_all_user_sessions(username: str):
    async with get_conn() as conn:
        await conn.execute("DELETE FROM session WHERE username = ?", (username,))
        await conn.commit()
