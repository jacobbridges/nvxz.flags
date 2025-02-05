from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api import crud, schemas, exceptions as exc
from api.core.auth import get_current_user

router = APIRouter(
    prefix="/flags",
    tags=["flags"],
)


class FlagCreate(BaseModel):
    name: str
    value: bool
    project_id: int


class FlagUpdate(BaseModel):
    name: str | None = None
    value: bool | None = None


@router.post("/")
async def create_flag(
    data: FlagCreate,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
) -> schemas.Flag:
    # Validate that the current user owns the project
    project = await crud.get_project(data.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not Found")
    try:
        flag_id = await crud.create_flag(
            name=data.name,
            value=data.value,
            project_id=data.project_id,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Flag creation failed")
    flag = await crud.get_flag(flag_id)
    return flag


@router.get("/")
async def list_flags(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    project_id: int | None = None,
) -> list[schemas.Flag]:
    """
    Provides a list of flags belonging to the current user.

    Supported query filters:
    -   project_id: Filter flags by project.
    """
    return await crud.list_flags_by_user(current_user.id, project_id=project_id)


@router.patch("/{flag_id}")
async def update_flag(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    flag_id: int,
    data: FlagUpdate,
) -> schemas.Flag:
    flag = await crud.get_flag(flag_id)
    project = await crud.get_project(flag.project_id)
    if project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not Found")
    update_data = data.model_dump(exclude_unset=True)
    updated_flag = flag.model_copy(update=update_data)
    try:
        await crud.update_flag(updated_flag)
    except exc.FlagNameTakenError:
        raise HTTPException(status_code=400, detail="Flag already exists")
    return updated_flag
