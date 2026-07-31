import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

from src.core.logging import get_logger
from src.orchestrator.retry import RetryableError

logger = get_logger("retry")

T = TypeVar("T")


def build_retry_policy(max_attempts: int = 3, base_wait: float = 1.0, max_wait: float = 30.0):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=base_wait, min=base_wait, max=max_wait)
        + wait_random(0, 0.25),
        retry=retry_if_exception_type(RetryableError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


def retry_with_backoff(
    func: Callable[..., T],
    *args,
    max_attempts: int = 3,
    base_wait: float = 1.0,
    **kwargs,
) -> T:
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except RetryableError as e:
            last_exception = e
            if attempt < max_attempts - 1:
                wait_time = base_wait * (2 ** attempt) + random.uniform(0, 0.5)
                logger.warning(
                    "retry_attempt",
                    attempt=attempt + 1,
                    max_attempts=max_attempts,
                    wait_time=wait_time,
                )
                time.sleep(wait_time)
    raise last_exception
