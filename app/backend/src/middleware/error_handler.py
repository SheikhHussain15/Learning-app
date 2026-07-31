import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logging import get_logger
from src.orchestrator.retry import NonRetryableError, RetryableError

logger = get_logger("error_handler")


async def ai_error_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    if isinstance(exc, RetryableError):
        logger.warning("retryable_error", error_code=exc.code, request_id=request_id)
        return JSONResponse(
            status_code=502,
            content={
                "error": {
                    "code": exc.code,
                    "message": "The service is temporarily unavailable. Please try again.",
                    "retryable": True,
                    "request_id": request_id,
                }
            },
        )

    if isinstance(exc, NonRetryableError):
        logger.warning("non_retryable_error", error_code=exc.code, request_id=request_id)
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": exc.code,
                    "message": "Your request could not be processed. Please check your input.",
                    "retryable": False,
                    "request_id": request_id,
                }
            },
        )

    logger.error("unexpected_error", error=str(exc), request_id=request_id, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "retryable": False,
                "request_id": request_id,
            }
        },
    )


async def validation_error_handler(request: Request, exc) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.warning("validation_error", errors=str(exc.errors()), request_id=request_id)
    return JSONResponse(
        status_code=400,
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


async def http_exception_handler(request: Request, exc) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    status_code = exc.status_code
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)

    if status_code == 404:
        message = "The requested resource was not found."
    elif status_code == 401:
        message = "Authentication required. Please sign in."
    elif status_code == 403:
        message = "You do not have permission to access this resource."
    elif status_code == 429:
        message = "Too many requests. Please wait a moment and try again."
    else:
        message = detail

    logger.warning("http_error", status_code=status_code, request_id=request_id)
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": f"HTTP_{status_code}",
                "message": message,
                "retryable": status_code in (429, 502, 503, 504),
                "request_id": request_id,
            }
        },
    )
