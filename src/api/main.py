from fastapi import FastAPI
from pydantic import BaseModel

from .routers import flags, users, auth, projects

app = FastAPI()

app.include_router(auth.router)
app.include_router(flags.router)
app.include_router(users.router)
app.include_router(projects.router)


class ServerInfo(BaseModel):
    project: str
    description: str


@app.get("/")
async def read_root() -> ServerInfo:
    return ServerInfo(
        project="nvxz.flags",
        description="A tiny feature flag service."
    )
