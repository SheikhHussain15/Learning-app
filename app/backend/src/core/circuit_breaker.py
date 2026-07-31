import enum
import time

from src.core.logging import get_logger

logger = get_logger("circuit_breaker")


class CircuitState(enum.StrEnum):
    closed = "closed"
    open = "open"
    half_open = "half_open"


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self._state = CircuitState.closed
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._half_open_calls = 0

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.open and time.time() - self._last_failure_time >= self.recovery_timeout:
            self._state = CircuitState.half_open
            self._half_open_calls = 0
            logger.info("circuit_half_open", name=self.name)
        return self._state

    def record_success(self):
        if self._state == CircuitState.half_open:
            self._success_count += 1
            if self._success_count >= self.half_open_max_calls:
                self._state = CircuitState.closed
                self._failure_count = 0
                self._success_count = 0
                logger.info("circuit_closed", name=self.name)
        elif self._state == CircuitState.closed:
            self._failure_count = 0

    def record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.half_open:
            self._state = CircuitState.open
            logger.warning("circuit_reopened", name=self.name)
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.open
            logger.warning("circuit_opened", name=self.name, failures=self._failure_count)

    def allow_request(self) -> bool:
        state = self.state
        if state == CircuitState.closed:
            return True
        if state == CircuitState.half_open:
            return self._half_open_calls < self.half_open_max_calls
        return False
