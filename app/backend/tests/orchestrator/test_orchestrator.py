import pytest
from unittest.mock import patch, MagicMock
from src.orchestrator.orchestrator import Orchestrator
from src.models.agent_run import AgentType, AgentStatus
from src.schemas.agent import RequestEnvelope
from src.orchestrator.router import register_agent
from src.agents.echo_agent import EchoAgent


@pytest.mark.asyncio
async def test_orchestrator_full_lifecycle(mock_langfuse, db):
    register_agent(AgentType.echo, EchoAgent())
    orchestrator = Orchestrator()

    envelope = RequestEnvelope(
        document_id="550e8400-e29b-41d4-a716-446655440000",
        node_ids=["550e8400-e29b-41d4-a716-446655440001"],
        trace_id="trace-orc-1",
    )

    agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
    assert agent_run is not None
    assert agent_run.status == AgentStatus.succeeded
    assert agent_run.duration_ms is not None
    assert agent_run.model_used is not None


@pytest.mark.asyncio
async def test_orchestrator_invalid_agent_type(mock_langfuse, db):
    orchestrator = Orchestrator()
    envelope = RequestEnvelope(
        document_id="doc-1",
        node_ids=[],
        trace_id="trace-orc-2",
    )

    agent_run = await orchestrator.dispatch(
        AgentType.summary, envelope, db_session=db
    )
    assert agent_run.status == AgentStatus.failed
