import pytest
from src.agents.echo_agent import EchoAgent
from src.schemas.agent import RequestEnvelope


@pytest.fixture
def echo_agent():
    return EchoAgent()


@pytest.mark.asyncio
async def test_echo_agent_valid_request(echo_agent):
    envelope = RequestEnvelope(
        document_id="550e8400-e29b-41d4-a716-446655440000",
        node_ids=["550e8400-e29b-41d4-a716-446655440001"],
        agent_params={"test": True},
        trace_id="trace-1",
    )
    response = await echo_agent.invoke(envelope)
    assert response.status == "success"
    assert response.output["echoed_document_id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert response.output["echoed_node_ids"] == ["550e8400-e29b-41d4-a716-446655440001"]
    assert response.output["echoed_trace_id"] == "trace-1"
    assert response.output["received_agent_params"] == {"test": True}
    assert response.usage.total_tokens == 70
    assert response.error is None


@pytest.mark.asyncio
async def test_echo_agent_empty_node_ids(echo_agent):
    envelope = RequestEnvelope(
        document_id="550e8400-e29b-41d4-a716-446655440000",
        node_ids=[],
        trace_id="trace-2",
    )
    response = await echo_agent.invoke(envelope)
    assert response.status == "success"


@pytest.mark.asyncio
async def test_echo_agent_invalid_envelope(echo_agent):
    envelope = RequestEnvelope(
        document_id="",
        node_ids=[],
        trace_id="trace-3",
    )
    response = await echo_agent.invoke(envelope)
    assert response.status == "error"
    assert response.error is not None
    assert response.error.code == "INVALID_REQUEST"


@pytest.mark.asyncio
async def test_echo_agent_with_context(echo_agent):
    from src.schemas.agent import RequestContext, RetrievedChunk
    envelope = RequestEnvelope(
        document_id="550e8400-e29b-41d4-a716-446655440000",
        node_ids=[],
        trace_id="trace-4",
        context=RequestContext(
            chunks=[
                RetrievedChunk(chunk_id="c1", text="Test", score=0.95, metadata={})
            ],
            source_doc_id="550e8400-e29b-41d4-a716-446655440000",
        ),
    )
    response = await echo_agent.invoke(envelope)
    assert response.status == "success"
