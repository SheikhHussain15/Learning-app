import logging

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

logger = logging.getLogger(__name__)


class RetryableError(Exception):
    def __init__(self, message: str, code: str = "RETRYABLE_ERROR"):
        self.code = code
        super().__init__(message)


class NonRetryableError(Exception):
    def __init__(self, message: str, code: str = "NON_RETRYABLE_ERROR"):
        self.code = code
        super().__init__(message)


RETRYABLE_HTTP_CODES = {429, 502, 503, 504}
NON_RETRYABLE_HTTP_CODES = {400, 401, 403, 404}

AGENT_RETRYABLE_ERRORS = {
    "PROCESSING_ERROR",
    "STRUCTURING_ERROR",
    "SUMMARY_ERROR",
    "EXPLANATION_ERROR",
    "TRANSLATION_ERROR",
    "DIAGRAM_ERROR",
    "QUIZ_ERROR",
    "REVISION_ERROR",
}

AGENT_NON_RETRYABLE_ERRORS = {
    "NO_INPUT",
    "MISSING_PARAM",
    "INVALID_REQUEST",
}


def classify_error(status_code: int | None, error_message: str = "", error_code: str = "") -> Exception:
    if error_code in AGENT_RETRYABLE_ERRORS:
        return RetryableError(error_message, code=error_code)
    if error_code in AGENT_NON_RETRYABLE_ERRORS:
        return NonRetryableError(error_message, code=error_code)
    if status_code in RETRYABLE_HTTP_CODES:
        return RetryableError(f"HTTP {status_code}: {error_message}", code=f"HTTP_{status_code}")
    if status_code in NON_RETRYABLE_HTTP_CODES:
        return NonRetryableError(f"HTTP {status_code}: {error_message}", code=f"HTTP_{status_code}")
    if status_code and status_code >= 500:
        return RetryableError(f"HTTP {status_code}: {error_message}", code=f"HTTP_{status_code}")
    if "timeout" in error_message.lower():
        return RetryableError(error_message, code="TIMEOUT")
    if "rate limit" in error_message.lower():
        return RetryableError(error_message, code="RATE_LIMIT")
    if "invalid" in error_message.lower() or "contract" in error_message.lower():
        return NonRetryableError(error_message, code="INVALID_REQUEST")
    return RetryableError(error_message, code="UNKNOWN")


def build_retry_policy(max_attempts: int = 6):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=30) + wait_random(0, 0.25),
        retry=retry_if_exception_type(RetryableError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
