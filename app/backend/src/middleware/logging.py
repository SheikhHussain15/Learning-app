import logging
import re

SENSITIVE_PATTERNS = re.compile(
    r"(api[_-]?key|secret|token|password|authorization|bearer)\s*[:=]?\s*['\"]?[\w\-]+",
    re.IGNORECASE,
)


def redact_sensitive(data: str) -> str:
    return SENSITIVE_PATTERNS.sub(lambda m: f"{m.group(1)}: ***REDACTED***", data)


class SensitiveDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = redact_sensitive(record.msg)
        if record.args:
            record.args = tuple(
                redact_sensitive(str(a)) if isinstance(a, str) else a
                for a in record.args
            )
        return True


def setup_logging_redaction() -> None:
    for handler in logging.root.handlers:
        handler.addFilter(SensitiveDataFilter())
