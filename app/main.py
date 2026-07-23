from fastapi import FastAPI

from app.api.contact import router as contact_router
from app.api.health import router as health_router
from app.api.metrics import router as metrics_router


app = FastAPI(
    title="Developer Landing API",
    version="1.0.0"
)

app.include_router(contact_router)
app.include_router(health_router)
app.include_router(metrics_router)


@app.get("/")
async def root():
    return {
        "message": "API Working"
    }
    