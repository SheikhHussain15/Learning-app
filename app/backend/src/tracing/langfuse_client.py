import logging

from langfuse import Langfuse, get_client

from src.core import config

logger = logging.getLogger(__name__)

_langfuse: Langfuse | None = None


def get_langfuse() -> Langfuse | None:
    """Get or create the Langfuse singleton (fail-open)."""
    global _langfuse
    if _langfuse is None:
        try:
            _langfuse = Langfuse(
                public_key=config.LANGFUSE_PUBLIC_KEY,
                secret_key=config.LANGFUSE_SECRET_KEY,
                host=config.LANGFUSE_HOST,
            )
        except Exception as e:
            logger.warning("Failed to initialize Langfuse: %s", e)
            _langfuse = None
    return _langfuse


def flush_langfuse() -> None:
    """Flush pending Langfuse events (fail-open)."""
    try:
        client = get_client()
        client.flush()
    except Exception as e:
        logger.warning("Langfuse flush failed: %s", e)


def shutdown_langfuse() -> None:
    """Gracefully shutdown Langfuse client (fail-open)."""
    try:
        client = get_client()
        client.shutdown()
    except Exception as e:
        logger.warning("Langfuse shutdown failed: %s", e)
