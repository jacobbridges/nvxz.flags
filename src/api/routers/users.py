from fastapi import APIRouter, HTTPException

from api import crud, schemas


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
    await crud.create_user(user.username, user.password)
    user = await crud.get_user(user.username)
    return user
