from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api import crud, schemas
from api.core.auth import ph, generate_token, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await crud.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not ph.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": await generate_token(user),
        "token_type": "bearer",
    }


@router.get("/me")
async def retrieve_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user
