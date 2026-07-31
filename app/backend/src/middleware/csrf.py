import hmac

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging import get_logger

logger = get_logger("csrf")

STATE_CHANGING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
CSRF_TOKEN_NAME = "csrf_token"
CSRF_HEADER_NAME = "x-csrf-token"


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str = "csrf-secret-key"):
        super().__init__(app)
        self.secret_key = secret_key

    def _generate_token(self, session_id: str) -> str:
        return hmac.new(
            self.secret_key.encode(),
            session_id.encode(),
            "sha256",
        ).hexdigest()

    def _validate_token(self, token: str, session_id: str) -> bool:
        expected = self._generate_token(session_id)
        return hmac.compare_digest(token, expected)

    async def dispatch(self, request: Request, call_next):
        if request.method not in STATE_CHANGING_METHODS:
            response = await call_next(request)
            return response

        if request.url.path.startswith("/api/v1/auth") and request.url.path.endswith("/login"):
            response = await call_next(request)
            return response

        csrf_token = request.headers.get(CSRF_HEADER_NAME)
        session_id = request.cookies.get("session_id", "default")

        if not csrf_token or not self._validate_token(csrf_token, session_id):
            logger.warning("csrf_validation_failed", path=request.url.path)
            return Response(
                content='{"error": {"code": "CSRF_ERROR", "message": "Invalid CSRF token"}}',
                status_code=403,
                media_type="application/json",
            )

        response = await call_next(request)
        return response
