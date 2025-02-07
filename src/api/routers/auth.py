from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api import crud, schemas
from api.core import auth


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await crud.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not auth.ph.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": await auth.generate_token(user),
        "token_type": "bearer",
    }


@router.get("/me")
async def retrieve_me(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
) -> schemas.UserDetail:
    return schemas.UserDetail(**current_user.model_dump())
