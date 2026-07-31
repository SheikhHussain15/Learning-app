import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.v1 import api_router
from src.core.database import Base, engine
from src.models import (  # noqa: F401
    AgentOutput,
    AgentRun,
    DeploymentRecord,
    Document,
    FlashcardReview,
    HealthCheck,
    ProcessingNode,
    ProgressEvent,
    QuizAttempt,
    Recommendation,
    SecretRotationLog,
    SecurityAuditLog,
    TestSuiteResult,
    TutorConversation,
    User,
    UserNote,
    WorkspaceSection,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    from src.tracing.langfuse_client import shutdown_langfuse
    shutdown_langfuse()


app = FastAPI(title="AI Learning Platform API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
                "retryable": exc.status_code in (429, 502, 503, 504),
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Please check your input.",
                "details": exc.errors(),
                "retryable": False,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
                "retryable": False,
                "request_id": request_id,
            }
        },
    )


try:
    from src.middleware.rate_limiter import RateLimiterMiddleware
    app.add_middleware(RateLimiterMiddleware)
except ImportError:
    pass

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_endpoint():
    return {"status": "ok"}
