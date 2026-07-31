import pytest
from src.orchestrator.retry import (
    RetryableError,
    NonRetryableError,
    classify_error,
)


class TestRetryableError:
    def test_creation(self):
        err = RetryableError("test message", code="TEST_CODE")
        assert str(err) == "test message"
        assert err.code == "TEST_CODE"

    def test_default_code(self):
        err = RetryableError("msg")
        assert err.code == "RETRYABLE_ERROR"


class TestNonRetryableError:
    def test_creation(self):
        err = NonRetryableError("test message", code="TEST_CODE")
        assert str(err) == "test message"
        assert err.code == "TEST_CODE"

    def test_default_code(self):
        err = NonRetryableError("msg")
        assert err.code == "NON_RETRYABLE_ERROR"


class TestClassifyError:
    def test_rate_limit_is_retryable(self):
        err = classify_error(429, "rate limited")
        assert isinstance(err, RetryableError)

    def test_502_is_retryable(self):
        err = classify_error(502, "bad gateway")
        assert isinstance(err, RetryableError)

    def test_503_is_retryable(self):
        err = classify_error(503, "service unavailable")
        assert isinstance(err, RetryableError)

    def test_400_is_not_retryable(self):
        err = classify_error(400, "bad request")
        assert isinstance(err, NonRetryableError)

    def test_401_is_not_retryable(self):
        err = classify_error(401, "unauthorized")
        assert isinstance(err, NonRetryableError)

    def test_404_is_not_retryable(self):
        err = classify_error(404, "not found")
        assert isinstance(err, NonRetryableError)

    def test_timeout_is_retryable(self):
        err = classify_error(500, "connection timeout occurred")
        assert isinstance(err, RetryableError)

    def test_rate_limit_text_is_retryable(self):
        err = classify_error(500, "rate limit exceeded")
        assert isinstance(err, RetryableError)

    def test_invalid_text_is_not_retryable(self):
        err = classify_error(None, "invalid request format")
        assert isinstance(err, NonRetryableError)

    def test_agent_retryable_code(self):
        err = classify_error(None, "processing error", error_code="PROCESSING_ERROR")
        assert isinstance(err, RetryableError)

    def test_agent_non_retryable_code(self):
        err = classify_error(None, "no input", error_code="NO_INPUT")
        assert isinstance(err, NonRetryableError)

    def test_5xx_server_error_is_retryable(self):
        err = classify_error(500, "internal error")
        assert isinstance(err, RetryableError)
