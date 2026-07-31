import pytest
from src.agents.base import BaseAgent
from src.agents.echo_agent import EchoAgent
from src.schemas.agent import RequestEnvelope, ResponseEnvelope, TokenUsage, ErrorInfo


class TestBaseAgent:
    def test_validate_envelope_valid(self):
        agent = EchoAgent()
        envelope = RequestEnvelope(
            document_id="doc-1",
            node_ids=["node-1"],
            trace_id="trace-1",
        )
        result = agent.validate_envelope(envelope)
        assert result is None

    def test_validate_envelope_missing_document_id(self):
        agent = EchoAgent()
        envelope = RequestEnvelope(
            document_id="",
            node_ids=[],
            trace_id="trace-1",
        )
        result = agent.validate_envelope(envelope)
        assert result is not None
        assert result.code == "INVALID_REQUEST"
        assert result.retryable is False

    def test_validate_envelope_missing_trace_id(self):
        agent = EchoAgent()
        envelope = RequestEnvelope(
            document_id="doc-1",
            node_ids=[],
            trace_id="",
        )
        result = agent.validate_envelope(envelope)
        assert result is not None
        assert result.code == "INVALID_REQUEST"

    def test_make_error_response(self):
        agent = EchoAgent()
        error = ErrorInfo(code="TEST_ERROR", message="test", retryable=False)
        response = agent.make_error_response(error)
        assert response.status == "error"
        assert response.error is not None
        assert response.error.code == "TEST_ERROR"
        assert response.usage.total_tokens == 0


class TestEchoAgent:
    @pytest.mark.asyncio
    async def test_invoke_success(self, mock_langfuse):
        agent = EchoAgent()
        envelope = RequestEnvelope(
            document_id="doc-1",
            node_ids=["node-1", "node-2"],
            trace_id="trace-1",
            agent_params={"key": "value"},
        )
        result = await agent.invoke(envelope)
        assert result.status == "success"
        assert result.output["echoed_document_id"] == "doc-1"
        assert result.output["echoed_node_ids"] == ["node-1", "node-2"]
        assert result.output["echoed_trace_id"] == "trace-1"
        assert result.usage.total_tokens == 70

    @pytest.mark.asyncio
    async def test_invoke_validation_error(self, mock_langfuse):
        agent = EchoAgent()
        envelope = RequestEnvelope(
            document_id="",
            node_ids=[],
            trace_id="trace-1",
        )
        result = await agent.invoke(envelope)
        assert result.status == "error"
        assert result.error is not None
