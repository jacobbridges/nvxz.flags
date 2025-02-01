from fastapi import APIRouter, HTTPException

from api import crud, schemas
from api.exceptions import UsernameTakenError
from api.core.settings import DISABLE_USER_CREATE_ENDPOINT

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{username}")
async def retrieve_user(username: str) -> schemas.User:
    user = await crud.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return user


@router.post("/")
async def create_user(user: schemas.UserCreate) -> schemas.User:
    if DISABLE_USER_CREATE_ENDPOINT:
        raise HTTPException(status_code=403, detail="Disabled")
    try:
        await crud.create_user(user.username, user.password)
    except UsernameTakenError:
        raise HTTPException(status_code=400, detail="That username is taken.")
    user = await crud.get_user(user.username)
    return user
