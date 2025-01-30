from fastapi import FastAPI

from .routers import flags, users

app = FastAPI()

app.include_router(flags.router)
app.include_router(users.router)


@app.get("/")
async def read_root():
    return {
        "project": "nvxz.flags",
        "description": " A tiny feature flag service."
    }
