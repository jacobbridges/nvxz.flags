from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str


# Does not represent
class UserDetail(BaseModel):
    id: int
    username: str


class Project(BaseModel):
    id: int
    name: str
    user_id: int
    domain_whitelist: list[str]


class Flag(BaseModel):
    id: int
    name: str
    value: bool
    project_id: int


class UserApiKey(BaseModel):
    id: int
    user_id: int
    hashed_api_key: str
    is_revoked: bool
    created_at: str


class NewUserApiKey(BaseModel):
    id: int
    user_id: int
    api_key: str
