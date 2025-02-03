from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api import crud, schemas
from api.core.auth import get_current_user
from api.exceptions import ProjectNameTakenError

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


class ProjectCreate(BaseModel):
    name: str
    domain_whitelist: list[str]


@router.post("/")
async def create_project(
    data: ProjectCreate,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
) -> schemas.Project:
    try:
        project_id = await crud.create_project(
            user_id=current_user.id,
            name=data.name,
            domain_whitelist=data.domain_whitelist,
        )
    except ProjectNameTakenError:
        raise HTTPException(status_code=400, detail="You already have a project with that name.")
    project = await crud.get_project(project_id)
    return project


@router.get("/")
async def list_projects(current_user: Annotated[schemas.User, Depends(get_current_user)]) -> list[schemas.Project]:
    return await crud.list_projects_by_user(current_user.id)


@router.get("/{project_id}")
async def get_project(current_user: Annotated[schemas.User, Depends(get_current_user)], project_id: int, ) -> schemas.Project:
    project = await crud.get_project(project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not found.")
    return project
