from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Metrics"]
)


@router.get("/metrics")
async def metrics():

    return {
        "total_requests": 0
    }