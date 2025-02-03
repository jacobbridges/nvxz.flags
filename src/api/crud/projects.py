import logging
import sqlite3

from api.core.db import get_conn
from api.schemas import Project

logger = logging.getLogger("nvxz")


async def create_project(user_id: int, name: str, domain_whitelist: list[str]):
    whitelist = (
        "" if not domain_whitelist
        else ",".join(domain_whitelist)
    )
    async with get_conn() as conn:
        await conn.execute("PRAGMA foreign_keys = ON;")
        try:
            await conn.execute(
                "INSERT INTO project (name, user_id, domain_whitelist) VALUES (?, ?, ?);",
                (name, user_id, whitelist),
            )
            await conn.commit()
        except sqlite3.IntegrityError as e:
            logger.exception("Error while creating new project!")
            await conn.rollback()
            raise


async def get_project(idx: int) -> Project | None:
    async with get_conn() as conn:
        await conn.execute("PRAGMA foreign_keys = ON;")
        cursor = await conn.execute("SELECT id, name, user_id, domain_whitelist FROM project WHERE id = ?;", (idx,))
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return Project(
            id=row[0],
            name=row[1],
            user_id=row[2],
            domain_whitelist=([] if not row[3] else row[3].split(",")),
        )


async def list_projects_by_user(user_id: int) -> list[Project]:
    async with get_conn() as conn:
        await conn.execute("PRAGMA foreign_keys = ON;")
        cursor = await conn.execute(
            "SELECT id, name, user_id, domain_whitelist FROM project WHERE id = ?;", (user_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return [
            Project(
                id=row[0],
                name=row[1],
                user_id=row[2],
                domain_whitelist=([] if not row[3] else row[3].split(",")),
            )
            for row in rows
        ]
