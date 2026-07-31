import time
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging import get_logger

logger = get_logger("rate_limiter")


class RateLimitConfig:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds


RATE_LIMITS = {
    "default": RateLimitConfig(max_requests=100, window_seconds=60),
    "auth": RateLimitConfig(max_requests=20, window_seconds=300),
    "ai": RateLimitConfig(max_requests=10, window_seconds=60),
    "upload": RateLimitConfig(max_requests=5, window_seconds=60),
}


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _get_client_id(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _get_rate_limit(self, path: str) -> RateLimitConfig:
        if "/auth/" in path:
            return RATE_LIMITS["auth"]
        if "/agent" in path or "/pipeline" in path:
            return RATE_LIMITS["ai"]
        if "/upload" in path:
            return RATE_LIMITS["upload"]
        return RATE_LIMITS["default"]

    def _is_rate_limited(self, client_id: str, config: RateLimitConfig) -> bool:
        now = time.time()
        cutoff = now - config.window_seconds
        self._requests[client_id] = [
            t for t in self._requests[client_id] if t > cutoff
        ]
        return len(self._requests[client_id]) >= config.max_requests

    async def dispatch(self, request: Request, call_next):
        client_id = self._get_client_id(request)
        config = self._get_rate_limit(request.url.path)

        if self._is_rate_limited(client_id, config):
            logger.warning("rate_limit_exceeded", client_id=client_id, path=request.url.path)
            return Response(
                content='{"error": {"code": "RATE_LIMITED", "message": "Too many requests. Please wait."}}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(config.window_seconds)},
            )

        self._requests[client_id].append(time.time())
        response = await call_next(request)
        return response
