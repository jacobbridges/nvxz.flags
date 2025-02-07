import base64
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel

from api import schemas


password_hasher = ph = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def decode_token(token: str) -> str:
    session_id = base64.b64decode(token).decode("utf-8")
    return session_id


async def generate_token(user: schemas.User) -> str:
    from api import crud  # prevent circular dependency
    session_id = str(uuid4())
    await crud.create_session(user.username, session_id)
    return base64.b64encode(session_id.encode("utf-8")).decode("utf-8")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    from api import crud  # prevent circular dependency
    user = await crud.get_user_by_session_id(decode_token(token))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def generate_api_key(user: schemas.User) -> schemas.NewUserApiKey:
    from api import crud  # prevent circular dependency
    api_key = str(uuid4()) + "-" + user.username[:5]
    hashed_api_key = ph.hash(api_key)
    api_key_id = await crud.create_user_api_key(user_id=user.id, hashed_api_key=hashed_api_key)
    return schemas.NewUserApiKey(
        id=api_key_id,
        user_id=user.id,
        api_key=api_key,
    )
