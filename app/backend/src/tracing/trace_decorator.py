from langfuse import observe


def trace_agent(name: str = None):
    """Decorator for agent invocations using Langfuse @observe."""

    def decorator(func):
        observed = observe(name=name or func.__name__, as_type="span")(func)
        return observed

    return decorator


def trace_orchestrator(name: str = None):
    """Decorator for orchestrator dispatch using Langfuse @observe."""

    def decorator(func):
        observed = observe(name=name or func.__name__, as_type="span")(func)
        return observed

    return decorator
