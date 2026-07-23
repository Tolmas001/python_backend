from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.contact import router as contact_router
from app.api.health import router as health_router
from app.api.metrics import router as metrics_router
from app.middleware.request_logger import log_requests
from app.services.rate_limit_service import limiter
from app.core.config import settings

app = FastAPI(
    title="Developer Landing API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_router)
app.include_router(health_router)
app.include_router(metrics_router)


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    return await log_requests(request, call_next)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )


app.state.limiter = limiter


@app.get("/")
async def root():
    return {
        "message": "API Working"
    }


@app.on_event("startup")
async def startup_event():
    import os
    from app.services.metrics_service import ensure_file

    os.makedirs("storage", exist_ok=True)
    ensure_file()
