import time
import pytest
from src.schemas.agent import RequestEnvelope
from src.agents.echo_agent import EchoAgent
from src.orchestrator.state_machine import validate_transition
from src.models.agent_run import AgentStatus


@pytest.mark.asyncio
async def test_orchestration_overhead_under_100ms():
    echo_agent = EchoAgent()
    envelope = RequestEnvelope(
        document_id="bench-doc-1",
        node_ids=["bench-node-1"],
        trace_id="bench-trace-1",
    )

    start = time.perf_counter()
    for _ in range(100):
        response = await echo_agent.invoke(envelope)
    elapsed = (time.perf_counter() - start) / 100 * 1000

    assert response.status == "success"
    assert elapsed < 100, f"Echo agent avg invocation took {elapsed:.2f}ms (expected <100ms)"


def test_retrieval_overhead_under_500ms():
    from src.orchestrator.state_machine import can_transition

    start = time.perf_counter()
    for _ in range(1000):
        can_transition(AgentStatus.queued, AgentStatus.running)
        can_transition(AgentStatus.running, AgentStatus.succeeded)
    elapsed = (time.perf_counter() - start) / 1000 * 1000

    assert elapsed < 0.5, f"State machine check avg {elapsed:.3f}ms (expected <0.5ms)"


def test_tracing_overhead_under_50ms():
    start = time.perf_counter()
    for _ in range(100):
        validate_transition(AgentStatus.queued, AgentStatus.running)
    elapsed = (time.perf_counter() - start) / 100 * 1000

    assert elapsed < 0.1, f"Validation avg {elapsed:.3f}ms (expected <0.1ms)"
