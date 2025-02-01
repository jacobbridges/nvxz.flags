import sqlite3
from datetime import datetime

from api.core.auth import ph
from api.core.db import get_conn
from api.core.settings import SESSION_AGE_LIMIT
from api.schemas import User
from api.exceptions import UsernameTakenError

now = datetime.utcnow


async def create_user(username, password):
    async with get_conn() as conn:
        hashed_password = ph.hash(password)
        try:
            await conn.execute(
                "INSERT INTO user (username, hashed_password) VALUES (?, ?);",
                (username, hashed_password),
            )
            await conn.commit()
        except sqlite3.IntegrityError as e:
            await conn.rollback()
            raise UsernameTakenError()


async def get_user(username) -> User | None:
    async with get_conn() as conn:
        cursor = await conn.execute("SELECT id, username, hashed_password FROM user WHERE username = ?", (username,))
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return User(
            id=row[0],
            username=row[1],
            hashed_password=row[2],
        )


async def get_user_by_session_id(session_id: str) -> User | None:
    async with get_conn() as conn:
        cursor = await conn.execute(
            "SELECT username, created_at FROM session WHERE session_id = ?",
            (session_id,),
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        username, created_at = row
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        if (now() - created_at) > SESSION_AGE_LIMIT:
            return None
        cursor = await conn.execute(
            "SELECT id, username, hashed_password FROM user WHERE username = ?",
            (username,),
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return User(
            id=row[0],
            username=row[1],
            hashed_password=row[2],
        )
