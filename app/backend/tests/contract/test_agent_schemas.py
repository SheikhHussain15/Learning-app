import pytest
from pydantic import ValidationError
from src.schemas.agent import (
    RequestEnvelope,
    ResponseEnvelope,
    TokenUsage,
    ErrorInfo,
    RequestContext,
    RetrievedChunk,
    SourceRef,
    ModelConfig,
    AgentRunCreate,
    AgentRunResponse,
)
from src.models.agent_run import AgentType


class TestRequestEnvelopeContract:
    def test_valid_minimal(self):
        env = RequestEnvelope(document_id="doc-1", node_ids=[], trace_id="t-1")
        assert env.document_id == "doc-1"
        assert env.agent_params == {}

    def test_valid_full(self):
        env = RequestEnvelope(
            document_id="doc-1",
            node_ids=["n1", "n2"],
            agent_params={"key": "val"},
            context=RequestContext(chunks=[], source_doc_id="doc-1"),
            trace_id="t-1",
        )
        assert env.context is not None

    def test_missing_document_id_fails(self):
        with pytest.raises(ValidationError):
            RequestEnvelope(node_ids=[], trace_id="t-1")

    def test_missing_trace_id_fails(self):
        with pytest.raises(ValidationError):
            RequestEnvelope(document_id="doc-1", node_ids=[])


class TestResponseEnvelopeContract:
    def test_valid_success(self):
        resp = ResponseEnvelope(
            status="success",
            output={"key": "val"},
            source_refs=[],
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )
        assert resp.status == "success"
        assert resp.error is None

    def test_valid_error(self):
        resp = ResponseEnvelope(
            status="error",
            output={},
            source_refs=[],
            usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            error=ErrorInfo(code="ERR", message="failed", retryable=False),
        )
        assert resp.error is not None

    def test_invalid_status_fails(self):
        with pytest.raises(ValidationError):
            ResponseEnvelope(
                status="invalid",
                output={},
                source_refs=[],
                usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )

    def test_partial_status_valid(self):
        resp = ResponseEnvelope(
            status="partial",
            output={"partial": True},
            source_refs=[],
            usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
        )
        assert resp.status == "partial"


class TestTokenUsageContract:
    def test_valid(self):
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        assert usage.total_tokens == 150

    def test_negative_fails(self):
        with pytest.raises(ValidationError):
            TokenUsage(prompt_tokens=-1, completion_tokens=0, total_tokens=0)

    def test_defaults(self):
        usage = TokenUsage()
        assert usage.prompt_tokens == 0
        assert usage.completion_tokens == 0
        assert usage.total_tokens == 0


class TestRetrievedChunkContract:
    def test_valid_score_boundary(self):
        chunk = RetrievedChunk(chunk_id="c1", text="text", score=0.0)
        assert chunk.score == 0.0
        chunk2 = RetrievedChunk(chunk_id="c2", text="text", score=1.0)
        assert chunk2.score == 1.0

    def test_invalid_score_fails(self):
        with pytest.raises(ValidationError):
            RetrievedChunk(chunk_id="c1", text="text", score=-0.1)
        with pytest.raises(ValidationError):
            RetrievedChunk(chunk_id="c1", text="text", score=1.1)


class TestModelConfigContract:
    def test_valid(self):
        config = ModelConfig(
            agent_type=AgentType.echo,
            primary_model_id="openai/gpt-4o",
            fallback_model_id="anthropic/claude-3-haiku",
            capabilities=["text"],
            cost_tier="low",
        )
        assert config.cost_tier == "low"

    def test_invalid_cost_tier_fails(self):
        with pytest.raises(ValidationError):
            ModelConfig(
                agent_type=AgentType.echo,
                primary_model_id="m1",
                fallback_model_id="m2",
                cost_tier="invalid",
            )
