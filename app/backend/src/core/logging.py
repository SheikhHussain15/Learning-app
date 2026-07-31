import logging
import sys

import structlog

from src.core import config


def redact_pii_processor(logger, method_name, event_dict):
    """Redact PII from log events."""
    sensitive_keys = {"password", "token", "secret", "api_key", "authorization"}
    for key in list(event_dict.keys()):
        if key.lower() in sensitive_keys:
            event_dict[key] = "***REDACTED***"
    if "user_id" in event_dict and isinstance(event_dict["user_id"], str):
        uid = event_dict["user_id"]
        if len(uid) > 8:
            event_dict["user_id"] = uid[:4] + "***" + uid[-4:]
    return event_dict


def setup_logging():
    """Configure structured logging with structlog."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            redact_pii_processor,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(config.LOG_LEVEL)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """Get a structured logger instance."""
    return structlog.get_logger(name)
