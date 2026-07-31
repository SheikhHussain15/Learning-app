import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.schemas.pipeline import PipelineRequest, PipelineResponse
from src.schemas.agent import RequestEnvelope, ResponseEnvelope, TokenUsage
from src.models.agent_run import AgentType, AgentStatus


@pytest.fixture
def mock_orchestrator():
    orchestrator = MagicMock()
    orchestrator.dispatch = AsyncMock()
    return orchestrator


@pytest.fixture
def sample_pipeline_request():
    return PipelineRequest(
        document_id="doc-test-1",
        user_id="user-1",
        requested_agents=[AgentType.document_processing, AgentType.knowledge_structuring],
        agent_params={},
        force_reprocess=False,
    )


@pytest.fixture
def mock_agent_run():
    run = MagicMock()
    run.id = "run-test-1"
    run.status = AgentStatus.succeeded
    run.agent_type = AgentType.document_processing
    run.duration_ms = 150
    run.response_envelope = {
        "status": "success",
        "output": {"chunks": [{"chunk_id": "c1", "text": "Test"}]},
        "source_refs": [],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
    }
    return run


@pytest.mark.asyncio
@patch("src.services.pipeline_service.get_orchestrator")
@patch("src.services.pipeline_service.get_cached_output")
@patch("src.services.pipeline_service.store_output")
async def test_execute_pipeline_basic(
    mock_store,
    mock_cache,
    mock_get_orch,
    sample_pipeline_request,
    mock_orchestrator,
    mock_agent_run,
):
    mock_cache.return_value = None
    mock_get_orch.return_value = mock_orchestrator
    mock_orchestrator.dispatch.return_value = mock_agent_run

    from src.services.pipeline_service import execute_pipeline
    result = await execute_pipeline(sample_pipeline_request)

    assert isinstance(result, PipelineResponse)
    assert result.pipeline_id is not None
    assert result.status in ["succeeded", "partial", "failed"]
    assert result.agent_results is not None


@pytest.mark.asyncio
@patch("src.services.pipeline_service.get_orchestrator")
@patch("src.services.pipeline_service.get_cached_output")
@patch("src.services.pipeline_service.store_output")
async def test_execute_pipeline_with_cache(
    mock_store,
    mock_cache,
    mock_get_orch,
    sample_pipeline_request,
    mock_orchestrator,
):
    mock_cache.return_value = {"cached": True}
    mock_get_orch.return_value = mock_orchestrator

    from src.services.pipeline_service import execute_pipeline
    result = await execute_pipeline(sample_pipeline_request)

    assert isinstance(result, PipelineResponse)
    mock_cache.assert_called()


@pytest.mark.asyncio
@patch("src.services.pipeline_service.get_orchestrator")
@patch("src.services.pipeline_service.get_cached_output")
@patch("src.services.pipeline_service.store_output")
async def test_execute_pipeline_force_reprocess(
    mock_store,
    mock_cache,
    mock_get_orch,
    mock_orchestrator,
    mock_agent_run,
):
    request = PipelineRequest(
        document_id="doc-test-1",
        user_id="user-1",
        requested_agents=[AgentType.document_processing],
        force_reprocess=True,
    )

    mock_cache.return_value = {"cached": True}
    mock_get_orch.return_value = mock_orchestrator
    mock_orchestrator.dispatch.return_value = mock_agent_run

    from src.services.pipeline_service import execute_pipeline
    result = await execute_pipeline(request)

    assert isinstance(result, PipelineResponse)
    mock_cache.assert_not_called()


@pytest.mark.asyncio
@patch("src.services.pipeline_service.get_orchestrator")
@patch("src.services.pipeline_service.get_cached_output")
@patch("src.services.pipeline_service.store_output")
async def test_execute_pipeline_partial_failure(
    mock_store,
    mock_cache,
    mock_get_orch,
    mock_orchestrator,
):
    failed_run = MagicMock()
    failed_run.id = "run-fail-1"
    failed_run.status = AgentStatus.failed
    failed_run.agent_type = AgentType.document_processing
    failed_run.duration_ms = 100
    failed_run.response_envelope = {
        "status": "error",
        "output": {},
        "source_refs": [],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "error": {"code": "PROCESSING_ERROR", "message": "Failed"},
    }

    request = PipelineRequest(
        document_id="doc-test-1",
        user_id="user-1",
        requested_agents=[AgentType.document_processing, AgentType.knowledge_structuring],
    )

    mock_cache.return_value = None
    mock_get_orch.return_value = mock_orchestrator
    mock_orchestrator.dispatch.return_value = failed_run

    from src.services.pipeline_service import execute_pipeline
    result = await execute_pipeline(request)

    assert isinstance(result, PipelineResponse)
    assert result.status == "partial"
