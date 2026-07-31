import pytest
from src.tracing.langfuse_client import get_langfuse, flush_langfuse


def test_get_langfuse_returns_none_on_invalid_config():
    import src.core.config as config
    original_key = config.LANGFUSE_PUBLIC_KEY
    config.LANGFUSE_PUBLIC_KEY = ""
    result = get_langfuse()
    assert result is not None
    config.LANGFUSE_PUBLIC_KEY = original_key


def test_flush_langfuse_does_not_raise():
    try:
        flush_langfuse()
    except Exception:
        pytest.fail("flush_langfuse raised unexpectedly")


def test_trace_decorator_importable():
    from src.tracing.trace_decorator import trace_agent, trace_orchestrator
    assert trace_agent is not None
    assert trace_orchestrator is not None


@pytest.mark.asyncio
async def test_langfuse_failure_never_blocks(mock_langfuse, monkeypatch):
    from src.orchestrator.orchestrator import Orchestrator
    from src.models.agent_run import AgentType
    from src.schemas.agent import RequestEnvelope
    from src.orchestrator.router import register_agent
    from src.agents.echo_agent import EchoAgent

    def raise_on_trace(*args, **kwargs):
        raise Exception("Langfuse is down")

    monkeypatch.setattr("src.tracing.langfuse_client.Langfuse", raise_on_trace)

    register_agent(AgentType.echo, EchoAgent())

    orchestrator = Orchestrator()
    envelope = RequestEnvelope(
        document_id="doc-tracing-1",
        node_ids=[],
        trace_id="trace-resilience-1",
    )

    from src.core.database import SessionLocal
    db = SessionLocal()
    try:
        agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
        assert agent_run.status.value == "succeeded"
    finally:
        db.close()
