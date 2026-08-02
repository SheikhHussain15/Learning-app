import asyncio
import logging
import time
import uuid

from src.core.database import SessionLocal
from src.models.agent_run import AgentStatus, AgentType
from src.orchestrator.orchestrator import get_orchestrator
from src.orchestrator.pipeline import get_execution_order
from src.schemas.agent import RequestContext, RequestEnvelope, RetrievedChunk
from src.schemas.pipeline import AgentRunResponse, PipelineRequest, PipelineResponse
from src.services.agent_output_cache import get_cached_output, store_output

logger = logging.getLogger(__name__)


def _generate_fallback_output(agent_type: AgentType, context_data: dict) -> dict:
    """Generate simplified fallback output when primary agent fails."""
    chunks_raw = context_data.get("document_processing", {}).get("chunks", [])
    [c.get("text", "")[:200] for c in chunks_raw[:5]]

    if agent_type == AgentType.summary:
        return {
            "summaries": [{
                "node_id": "fallback",
                "summary_text": "Summary generation temporarily unavailable. Please try again later.",
                "key_points": ["Content processing is in progress"],
                "source_chunk_ids": [c.get("chunk_id", "") for c in chunks_raw[:3]],
            }],
            "overall_summary": "Summary will be available shortly.",
        }
    elif agent_type == AgentType.quiz:
        return {
            "questions": [{
                "question": "Quiz generation is temporarily unavailable.",
                "options": ["Try again later", "Contact support", "Skip quiz", "View content"],
                "correct_index": 0,
                "explanation": "Quiz generation is currently processing your content.",
                "difficulty": "easy",
                "source_chunk_ids": [],
            }],
            "metadata": {
                "total_questions": 1,
                "difficulty_distribution": {"easy": 1, "medium": 0, "hard": 0},
                "coverage_nodes": [],
            },
        }
    elif agent_type == AgentType.explanation:
        return {
            "explanations": [{
                "concept": "Content Processing",
                "explanation": "Detailed explanations are being generated for your content.",
                "examples": ["Please try again in a moment"],
                "complexity_level": "beginner",
                "source_chunk_ids": [],
            }],
        }
    else:
        return {"message": f"{agent_type.value} is temporarily unavailable"}


async def execute_pipeline(request: PipelineRequest) -> PipelineResponse:
    """Execute the agent pipeline with dependency resolution and caching."""
    pipeline_id = str(uuid.uuid4())
    execution_order = get_execution_order(request.requested_agents)

    agent_results: dict[str, AgentRunResponse] = {}
    completed_agents: list[AgentType] = []
    all_output_data: dict[str, dict] = {}
    failed_agents: list[str] = []

    start_time = time.time()

    for group in execution_order:
        tasks = []
        for agent_type in group:
            if not request.force_reprocess:
                cached = get_cached_output(
                    request.document_id,
                    agent_type.value,
                    request.agent_params.get(agent_type.value, {}),
                )
                if cached:
                    logger.info("Using cached output for %s", agent_type.value)
                    all_output_data[agent_type.value] = cached
                    completed_agents.append(agent_type)
                    continue

            tasks.append(_execute_agent(
                agent_type=agent_type,
                document_id=request.document_id,
                user_id=request.user_id,
                agent_params=request.agent_params.get(agent_type.value, {}),
                context_data=all_output_data,
            ))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for agent_type, result in zip(group, results, strict=False):
                if isinstance(result, Exception):
                    logger.error("Agent %s failed: %s", agent_type.value, result)
                    fallback_output = _generate_fallback_output(agent_type, all_output_data)
                    agent_results[agent_type.value] = AgentRunResponse(
                        id=str(uuid.uuid4()),
                        status="failed",
                        agent_type=agent_type,
                        error={"code": "AGENT_ERROR", "message": str(result)},
                        response_envelope=fallback_output,
                    )
                    failed_agents.append(agent_type.value)
                else:
                    agent_run, response = result
                    response_data = response or {}
                    run_failed = agent_run.status != AgentStatus.succeeded or response_data.get("status") == "error"
                    agent_results[agent_type.value] = AgentRunResponse(
                        id=agent_run.id,
                        status=agent_run.status.value,
                        agent_type=agent_type,
                        response_envelope=response_data.get("output"),
                        duration_ms=agent_run.duration_ms,
                    )

                    if run_failed:
                        failed_agents.append(agent_type.value)
                    else:
                        output_data = response_data.get("output", {})
                        all_output_data[agent_type.value] = output_data
                        completed_agents.append(agent_type)

                        if not request.force_reprocess:
                            store_output(
                                document_id=request.document_id,
                                agent_type=agent_type.value,
                                agent_params=request.agent_params.get(agent_type.value, {}),
                                output_data=output_data,
                                source_refs=response_data.get("source_refs", []),
                                token_usage=response_data.get("usage", {}),
                            )

    duration_ms = int((time.time() - start_time) * 1000)

    failed_count = len(failed_agents)
    if failed_count == 0:
        status = "succeeded"
    elif failed_count < len(agent_results):
        status = "partial"
    else:
        status = "failed"

    return PipelineResponse(
        pipeline_id=pipeline_id,
        status=status,
        agent_results=agent_results,
        duration_ms=duration_ms,
    )


async def _execute_agent(
    agent_type: AgentType,
    document_id: str,
    user_id: str,
    agent_params: dict,
    context_data: dict[str, dict],
) -> tuple:
    """Execute a single agent and return (AgentRun, ResponseEnvelope)."""
    from src.orchestrator.router import _init_default_agents

    _init_default_agents()

    trace_id = str(uuid.uuid4())

    context = None
    ks_nodes = context_data.get("knowledge_structuring", {}).get("nodes", [])
    if ks_nodes:
        chunks = [
            RetrievedChunk(
                chunk_id=n.get("node_id", ""),
                text=n.get("content", ""),
                score=0.95,
                metadata={"node_type": n.get("node_type"), "title": n.get("title")},
            )
            for n in ks_nodes[:20]
        ]
    else:
        chunks_raw = context_data.get("document_processing", {}).get("chunks", [])
        chunks = [
            RetrievedChunk(
                chunk_id=c.get("chunk_id", ""),
                text=c.get("text", ""),
                score=0.95,
                metadata=c.get("metadata", {}),
            )
            for c in chunks_raw[:20]
        ]

    if chunks:
        context = RequestContext(chunks=chunks)

    envelope = RequestEnvelope(
        document_id=document_id,
        node_ids=[],
        agent_params=agent_params,
        context=context,
        trace_id=trace_id,
    )

    orchestrator = get_orchestrator()
    db = SessionLocal()
    try:
        agent_run = await orchestrator.dispatch(agent_type, envelope, db_session=db)
        response_data = agent_run.response_envelope
        return agent_run, response_data
    finally:
        db.close()
