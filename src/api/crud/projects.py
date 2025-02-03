import sqlite3

from loguru import logger

from api.core.db import get_conn
from api.schemas import Project
from api.exceptions import ProjectNameTakenError


async def create_project(user_id: int, name: str, domain_whitelist: list[str]) -> int:
    whitelist = (
        "" if not domain_whitelist
        else ",".join(domain_whitelist)
    )
    async with get_conn() as conn:
        await conn.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor = await conn.cursor()
            await cursor.execute(
                "INSERT INTO project (name, user_id, domain_whitelist) VALUES (?, ?, ?) RETURNING id;",
                (name, user_id, whitelist),
            )
            row = await cursor.fetchone()
            await conn.commit()
            (inserted_id,) = row if row else [None]
            return inserted_id
        except sqlite3.IntegrityError as e:
            await conn.rollback()
            if "failed: project.user_id, project.name" in e.args[0]:
                raise ProjectNameTakenError()
            logger.exception("Error while creating new project")
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
