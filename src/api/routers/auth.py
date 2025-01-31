import base64
from uuid import uuid4
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api import crud
from api import schemas
from api.core.auth import ph


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def decode_token(token: str) -> schemas.User | None:
    session_id = base64.b64decode(token).decode("utf-8")
    user = await crud.get_user_by_session_id(session_id)
    return user


async def generate_token(user: schemas.User) -> str:
    session_id = str(uuid4())
    await crud.create_session(user.username, session_id)
    return base64.b64encode(session_id.encode("utf-8")).decode("utf-8")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user


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
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user
