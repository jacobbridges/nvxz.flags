import base64
import json
from typing import Annotated
from uuid import uuid4

from fastapi import HTTPException, status, Security, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from loguru import logger
from pwdlib import PasswordHash

from api import schemas


password_hasher = ph = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def decode_token(token: str) -> str:
    session_id = base64.b64decode(token).decode("utf-8")
    return session_id


async def generate_token(user: schemas.User) -> str:
    from api import crud  # prevent circular dependency
    session_id = str(uuid4())
    await crud.create_session(user.username, session_id)
    return base64.b64encode(session_id.encode("utf-8")).decode("utf-8")


async def bearer_auth(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.User | None:
    from api import crud  # prevent circular dependency
    if not token: return None
    user = await crud.get_user_by_session_id(decode_token(token))
    if not user: return None
    return user


async def api_key_auth(x_api_key: Annotated[str, Security(api_key_header)]) -> schemas.User | None:
    from api import crud  # prevent circular dependency
    if not x_api_key: return None

    # Decode the api key
    api_key = base64.b64decode(x_api_key).decode("utf-8")
    api_key = json.loads(api_key)
    api_key_id, api_key = api_key["i"], api_key["u"]

    # Get the record associated to the decoded id
    record = await crud.get_user_api_key(api_key_id)
    if not record: return None
    verified = ph.verify(x_api_key, record.hashed_api_key)
    if not verified: return None
    user = await crud.get_user_by_id(record.user_id)
    if not user: return None
    return user


async def get_current_user(
    bearer_result: Annotated[schemas.User, Depends(bearer_auth)],
    api_key_result: Annotated[schemas.User, Depends(api_key_auth)],
) -> schemas.User:
    if not bearer_result and not api_key_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return bearer_result or api_key_result


async def generate_api_key(user: schemas.User) -> schemas.NewUserApiKey:
    from api import crud  # prevent circular dependency

    # Create an "empty" api key record (need the database id)
    new_api_key_id = await crud.create_user_api_key(user_id=user.id, hashed_api_key="")
    empty_api_key_record = await crud.get_user_api_key(new_api_key_id)

    # Generate the real api key and hash it.
    # Hashed version will be saved to the db.
    # Real key will be given to the user.
    api_key = json.dumps({
        "u": str(uuid4()),
        "i": new_api_key_id,
    })
    api_key = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
    hashed_api_key = ph.hash(api_key)

    # Update the empty record with the real hashed api key
    empty_api_key_record.hashed_api_key = hashed_api_key
    real_api_key_record = await crud.update_user_api_key(empty_api_key_record)

    # Return the NewUserApiKey with the real api key
    return schemas.NewUserApiKey(
        id=real_api_key_record.id,
        user_id=real_api_key_record.user_id,
        api_key=api_key,
    )
