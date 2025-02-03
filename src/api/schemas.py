from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str


class Project(BaseModel):
    id: int
    name: str
    user_id: int
    domain_whitelist: list[str]
