import pytest
from src.schemas.agent import (
    RequestEnvelope,
    ResponseEnvelope,
    TokenUsage,
    ErrorInfo,
    RequestContext,
    RetrievedChunk,
)
from pydantic import ValidationError


def test_valid_request_envelope():
    payload = {
        "document_id": "550e8400-e29b-41d4-a716-446655440000",
        "node_ids": ["550e8400-e29b-41d4-a716-446655440001"],
        "agent_params": {"test": True},
        "trace_id": "trace-123",
    }
    envelope = RequestEnvelope(**payload)
    assert envelope.document_id == payload["document_id"]
    assert envelope.node_ids == payload["node_ids"]
    assert envelope.agent_params == payload["agent_params"]
    assert envelope.trace_id == payload["trace_id"]


def test_valid_request_envelope_with_context():
    payload = {
        "document_id": "550e8400-e29b-41d4-a716-446655440000",
        "node_ids": [],
        "trace_id": "trace-123",
        "context": {
            "chunks": [
                {"chunk_id": "c1", "text": "hello", "score": 0.95, "metadata": {"source": "doc1"}}
            ],
            "source_doc_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    }
    envelope = RequestEnvelope(**payload)
    assert envelope.context is not None
    assert len(envelope.context.chunks) == 1
    assert envelope.context.chunks[0].chunk_id == "c1"
    assert envelope.context.chunks[0].score == 0.95


def test_invalid_request_envelope_missing_document_id():
    with pytest.raises(ValidationError):
        RequestEnvelope(node_ids=[], trace_id="trace-123")


def test_invalid_request_envelope_missing_trace_id():
    with pytest.raises(ValidationError):
        RequestEnvelope(document_id="doc-1", node_ids=[])


def test_valid_response_envelope():
    payload = {
        "status": "success",
        "output": {"result": "ok"},
        "source_refs": [],
        "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
    }
    envelope = ResponseEnvelope(**payload)
    assert envelope.status == "success"
    assert envelope.usage.total_tokens == 70


def test_error_response_envelope():
    payload = {
        "status": "error",
        "output": {},
        "source_refs": [],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "error": {"code": "INVALID_REQUEST", "message": "Bad request", "retryable": False},
    }
    envelope = ResponseEnvelope(**payload)
    assert envelope.status == "error"
    assert envelope.error is not None
    assert envelope.error.code == "INVALID_REQUEST"


def test_invalid_response_status():
    with pytest.raises(ValidationError):
        ResponseEnvelope(
            status="invalid",
            output={},
            source_refs=[],
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )


def test_chunk_score_range():
    RetrievedChunk(chunk_id="c1", text="test", score=0.0, metadata={})
    RetrievedChunk(chunk_id="c2", text="test", score=1.0, metadata={})
    with pytest.raises(ValidationError):
        RetrievedChunk(chunk_id="c3", text="test", score=-0.1, metadata={})
    with pytest.raises(ValidationError):
        RetrievedChunk(chunk_id="c4", text="test", score=1.1, metadata={})
