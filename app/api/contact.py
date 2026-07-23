from fastapi import APIRouter, Request

from app.schemas.contact import ContactRequest
from app.services.contact_service import process_contact
from app.services.rate_limit_service import limiter


router = APIRouter(
    prefix="/api",
    tags=["Contact"]
)


@router.post("/contact")
@limiter.limit("5/minute")
async def contact(
    request: Request,
    data: ContactRequest
):

    ai = await process_contact(data)

    return {
        "success": True,
        "data": data,
        "ai": ai
    }
    