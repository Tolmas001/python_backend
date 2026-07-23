from fastapi import APIRouter

from app.schemas.contact import (
    ContactRequest
)

router = APIRouter(
    prefix="/api",
    tags=["Contact"]
)


@router.post("/contact")
async def contact(
        data: ContactRequest
):

    return {
        "success": True,
        "data": data
    }