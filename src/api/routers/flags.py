from fastapi import APIRouter

router = APIRouter(
    prefix="/flags",
    tags=["flags"],
)


@router.get("/")
async def list_flags():
    return [
        {"name": "summer_sale", "value": True},
        {"name": "halloween_landing_page", "value": False},
    ]


@router.get("/{flag_name}")
async def retrieve_flag(flag_name: str):
    return {"name": flag_name, "value": True}
