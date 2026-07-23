from fastapi import APIRouter

from app.services.metrics_service import (
    get_metrics
)

router = APIRouter(
    prefix="/api",
    tags=["Metrics"]
)


@router.get("/metrics")
async def metrics():

    return get_metrics()
