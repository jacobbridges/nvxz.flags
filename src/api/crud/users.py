from pwdlib import PasswordHash

from api.core.db import get_conn
from api.schemas import User


def hash_password(password: str) -> str:
    hasher = PasswordHash.recommended()
    return hasher.hash(password)


async def create_user(username, password):
    async with get_conn() as conn:
        hashed_password = hash_password(password)
        await conn.execute("INSERT INTO user (username, hashed_password) VALUES (?, ?);", (username, hashed_password))
        await conn.commit()


async def get_user(username) -> User | None:
    async with get_conn() as conn:
        cursor = await conn.execute("SELECT id, username, hashed_password FROM user WHERE username = ?", (username,))
        row = await cursor.fetchone()
        if row is None:
            return None
        return User(
            id=row[0],
            username=row[1],
            hashed_password=row[2],
        )
