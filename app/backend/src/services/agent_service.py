import logging
import uuid

from src.core.database import SessionLocal
from src.models.agent_run import AgentRun, AgentType
from src.orchestrator.orchestrator import get_orchestrator
from src.orchestrator.router import _init_default_agents
from src.schemas.agent import (
    AgentRunCreate,
    AgentRunResponse,
    ErrorInfo,
    RequestContext,
    RequestEnvelope,
    RetrievedChunk,
)

logger = logging.getLogger(__name__)


async def invoke_agent(
    agent_type: AgentType,
    payload: AgentRunCreate,
) -> AgentRunResponse:
    _init_default_agents()

    trace_id = str(uuid.uuid4())
    context = None
    if payload.context:
        context = RequestContext(
            chunks=[RetrievedChunk(**c.model_dump()) for c in payload.context.chunks] if payload.context.chunks else [],
            source_doc_id=payload.context.source_doc_id,
            previous_agent_output=payload.context.previous_agent_output,
        )

    envelope = RequestEnvelope(
        document_id=payload.document_id or "",
        node_ids=payload.node_ids,
        agent_params=payload.agent_params,
        context=context,
        trace_id=trace_id,
    )

    orchestrator = get_orchestrator()
    db = SessionLocal()
    try:
        agent_run = await orchestrator.dispatch(agent_type, envelope, db_session=db)

        response_envelope_data = agent_run.response_envelope
        error_info = None
        if response_envelope_data and isinstance(response_envelope_data, dict):
            error_data = response_envelope_data.get("error")
            if error_data:
                error_info = ErrorInfo(**error_data)

        return AgentRunResponse(
            id=agent_run.id,
            status=agent_run.status,
            agent_type=agent_run.agent_type,
            response_envelope=response_envelope_data,
            error=error_info,
            duration_ms=agent_run.duration_ms,
            created_at=agent_run.created_at,
            completed_at=agent_run.completed_at,
        )
    finally:
        db.close()


def get_run(run_id: str) -> AgentRun | None:
    db = SessionLocal()
    try:
        return db.query(AgentRun).filter(AgentRun.id == run_id).first()
    finally:
        db.close()


def list_runs(agent_type: AgentType | None = None, limit: int = 20, offset: int = 0) -> list[AgentRun]:
    db = SessionLocal()
    try:
        query = db.query(AgentRun)
        if agent_type:
            query = query.filter(AgentRun.agent_type == agent_type)
        return query.order_by(AgentRun.created_at.desc()).offset(offset).limit(limit).all()
    finally:
        db.close()
