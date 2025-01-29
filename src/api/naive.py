from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "project": "nvxz.flags",
        "description": "Simple feature flag server"
    }


@app.get("/flags/")
async def read_flags():
    return {"data": [
        {"name": "menu", "type": "string", "value": "v2"},
        {"name": "is_summer", "type": "bool", "value": False},
    ]}
