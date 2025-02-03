from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api import crud, schemas
from api.exceptions import UsernameTakenError
from api.core.settings import DISABLE_USER_CREATE_ENDPOINT

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


class UserCreate(BaseModel):
    username: str
    password: str


class UserDetail(BaseModel):
    id: int
    username: str


@router.get("/{username}")
async def retrieve_user(username: str) -> UserDetail:
    user = await crud.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return UserDetail(
        id=user.id,
        username=user.username,
    )


@router.post("/")
async def create_user(user: UserCreate) -> UserDetail:
    if DISABLE_USER_CREATE_ENDPOINT:
        raise HTTPException(status_code=403, detail="Disabled")
    try:
        await crud.create_user(user.username, user.password)
    except UsernameTakenError:
        raise HTTPException(status_code=400, detail="That username is taken.")
    user = await crud.get_user(user.username)
    return UserDetail(
        id=user.id,
        username=user.username,
    )
