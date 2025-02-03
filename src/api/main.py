from fastapi import FastAPI

from .routers import flags, users, auth, projects

app = FastAPI()

app.include_router(auth.router)
app.include_router(flags.router)
app.include_router(users.router)
app.include_router(projects.router)


@app.get("/")
async def read_root():
    return {
        "project": "nvxz.flags",
        "description": " A tiny feature flag service."
    }
