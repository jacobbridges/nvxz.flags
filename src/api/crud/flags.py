import sqlite3

from loguru import logger

from api.core.db import get_conn
from api import schemas
from api.exceptions import FlagNameTakenError


async def create_flag(project_id: int, name: str, value: bool) -> int:
    async with get_conn() as conn:
        try:
            cursor = await conn.cursor()
            await cursor.execute(
                "INSERT INTO flag (name, project_id, value) VALUES (?, ?, ?) RETURNING id;",
                (name, project_id, value),
            )
            row = await cursor.fetchone()
            await conn.commit()
            (inserted_id,) = row if row else [None]
            return inserted_id
        except sqlite3.IntegrityError as e:
            await conn.rollback()
            logger.exception("Error while creating new flag")
            raise


async def get_flag(idx: int) -> schemas.Flag | None:
    async with get_conn() as conn:
        cursor = await conn.execute("SELECT id, name, value, project_id from flag WHERE id = ?;", (idx,))
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return schemas.Flag(
            id=row[0],
            name=row[1],
            value=row[2],
            project_id=row[3],
        )


async def list_flags_by_user(user_id: int, **kwargs) -> list[schemas.Flag]:
    project_id = None
    if "project_id" in kwargs:
        project_id = kwargs["project_id"]
    async with get_conn() as conn:
        sql = (
            "SELECT f.id, f.name, f.value, f.project_id FROM flag f "
            "  JOIN project p ON f.project_id = p.id "
            "  JOIN user u on p.user_id = u.id "
            "WHERE u.id = ? {};"
        ).format("AND f.project_id = ?" if project_id else "")
        args = (user_id,) if not project_id else (user_id, project_id)
        cursor = await conn.execute(sql, args,)
        rows = await cursor.fetchall()
        await cursor.close()
        return [
            schemas.Flag(
                id=row[0],
                name=row[1],
                value=row[2],
                project_id=row[3],
            )
            for row in rows
        ]


async def list_flags_by_project(project_id: int) -> list[schemas.Flag]:
    async with get_conn() as conn:
        cursor = await conn.execute(
            "SELECT id, name, value, project_id FROM flag WHERE project_id = ?;",
            (project_id,),
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return [
            schemas.Flag(
                id=row[0],
                name=row[1],
                value=row[2],
                project_id=row[3],
            )
            for row in rows
        ]
