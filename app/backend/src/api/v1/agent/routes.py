from fastapi import APIRouter, Depends, HTTPException

from src.middleware.auth import get_current_user
from src.models.agent_run import AgentType
from src.models.user import User
from src.schemas.agent import AgentRunCreate, AgentRunResponse
from src.schemas.pipeline import PipelineRequest, PipelineResponse
from src.services import agent_service
from src.services.pipeline_service import execute_pipeline

router = APIRouter(prefix="/agents")

ERROR_MESSAGES = {
    "PROCESSING_ERROR": {
        "message": "Document processing failed",
        "action": "Please ensure the document is valid and try again. Supported formats: PDF, DOCX, TXT.",
        "retryable": True,
    },
    "STRUCTURING_ERROR": {
        "message": "Content structuring failed",
        "action": "The document content may be too short or corrupted. Try uploading a different document.",
        "retryable": True,
    },
    "NO_INPUT": {
        "message": "No content available for processing",
        "action": "Please ensure the document has been processed first before generating content.",
        "retryable": False,
    },
    "TIMEOUT": {
        "message": "Request timed out",
        "action": "The processing is taking longer than expected. Please try again in a moment.",
        "retryable": True,
    },
    "RATE_LIMIT": {
        "message": "Rate limit exceeded",
        "action": "Too many requests. Please wait a moment and try again.",
        "retryable": True,
    },
}


def _get_user_friendly_error(error_code: str, detail: str) -> dict:
    error_info = ERROR_MESSAGES.get(error_code, {
        "message": "An unexpected error occurred",
        "action": "Please try again. If the problem persists, contact support.",
        "retryable": False,
    })
    return {
        "error": error_info["message"],
        "detail": detail,
        "action": error_info["action"],
        "retryable": error_info["retryable"],
        "code": error_code,
    }


@router.post("/{agent_type}/invoke")
async def invoke_agent(agent_type: AgentType, payload: AgentRunCreate, current_user: User = Depends(get_current_user)) -> AgentRunResponse:
    try:
        result = await agent_service.invoke_agent(agent_type, payload)
        return result
    except ValueError as e:
        error_response = _get_user_friendly_error("INVALID_REQUEST", str(e))
        raise HTTPException(status_code=400, detail=error_response)
    except Exception as e:
        error_response = _get_user_friendly_error("UNKNOWN", str(e))
        raise HTTPException(status_code=500, detail=error_response)


@router.get("/runs/{run_id}")
def get_run(run_id: str, current_user: User = Depends(get_current_user)) -> AgentRunResponse:
    run = agent_service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail={
            "error": "Run not found",
            "action": "Please check the run ID and try again.",
            "retryable": False,
        })
    return AgentRunResponse(
        id=run.id,
        status=run.status,
        agent_type=run.agent_type,
        response_envelope=run.response_envelope,
        error=None,
        duration_ms=run.duration_ms,
        created_at=run.created_at,
        completed_at=run.completed_at,
    )


@router.get("/runs")
def list_runs(agent_type: AgentType | None = None, limit: int = 20, offset: int = 0, current_user: User = Depends(get_current_user)) -> list[AgentRunResponse]:
    runs = agent_service.list_runs(agent_type, limit, offset)
    return [
        AgentRunResponse(
            id=r.id,
            status=r.status,
            agent_type=r.agent_type,
            response_envelope=r.response_envelope,
            error=None,
            duration_ms=r.duration_ms,
            created_at=r.created_at,
            completed_at=r.completed_at,
        )
        for r in runs
    ]


@router.post("/pipeline/invoke")
async def invoke_pipeline(payload: PipelineRequest, current_user: User = Depends(get_current_user)) -> PipelineResponse:
    try:
        result = await execute_pipeline(payload)
        return result
    except ValueError as e:
        error_response = _get_user_friendly_error("INVALID_REQUEST", str(e))
        raise HTTPException(status_code=400, detail=error_response)
    except Exception as e:
        error_response = _get_user_friendly_error("PIPELINE_ERROR", str(e))
        raise HTTPException(status_code=500, detail=error_response)
