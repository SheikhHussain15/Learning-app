# Implementation Plan: AI Agent Orchestration

**Branch**: `004-ai-agent-orchestration` | **Date**: 2026-07-13 | **Spec**: specs/004-ai-agent-orchestration/spec.md
**Input**: Phase 4 AI Agent Specification Description

## Summary

Implement the complete AI Agent ecosystem for the AI Learning Platform: 10 specialized agents (Document Processing, Knowledge Structuring, Summary, Explanation, Translation, Diagram, Quiz, Revision, Progress, Recommendation) orchestrated through a dependency-aware Orchestrator with incremental execution, standardized Request/Response contracts, grounding via retrieval context, comprehensive error handling, and Langfuse observability — all building on the Phase 3 infrastructure (OpenRouter, ChromaDB, LlamaIndex, Langfuse, tenacity retry).

## Technical Context

**Language/Version**: Python 3.11+ (backend)
**Primary Dependencies**: openai-agents, chromadb, llama-index, langfuse, fastapi, sqlalchemy, pydantic, tenacity
**Storage**: SQLite dev / PostgreSQL prod (AgentRun, AgentOutput, ProcessingNode), ChromaDB (vector embeddings)
**Testing**: pytest + pytest-asyncio (unit, integration, contract)
**Target Platform**: Linux server (Docker), local development (Windows/PowerShell)
**Project Type**: Web application (FastAPI backend)
**Performance Goals**: Full pipeline <60s per document, incremental <30s, orchestrator overhead <100ms
**Constraints**: <200ms p95 orchestrator overhead, <1s p95 retrieval, source_refs required on all outputs
**Scale/Scope**: 100 concurrent documents, 1000 docs/hour peak, 10 agent types

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project Constitution is in template form (placeholders unset). Evaluated against the established Phase 3 principles:

1. **Stable Agent Contracts** — Respected. All 10 agents use the existing RequestEnvelope/ResponseEnvelope contract. New agent_params keys are additive and backward-compatible.
2. **Orchestrator as Single Source of Truth** — Respected. All agent invocations flow through `Orchestrator.dispatch()`. No direct agent calls.
3. **Grounded AI Architecture** — Respected. Every content-generating agent receives retrieval chunks via `context.chunks`. Outputs include `source_refs` linking back to source document chunks.
4. **Type Safety** — Respected. AgentType enum extended with new values. All agent output schemas are Pydantic models. Dependency graph is typed.
5. **Production-First Architecture** — Respected. Retry/backoff, timeout, fallback, error classification carried forward. New agents inherit BaseAgent validation.
6. **Security by Default** — Respected. Document ownership validation before processing. User isolation via document_id scoping. No cross-user data leakage.
7. **Documentation as Code** — Respected. This plan, research, data model, contracts, and quickstart are generated artifacts.
8. **AI-Friendly Codebase** — Respected. Centralized model registry, shared contracts, single orchestrator entry point.
9. **Observability by Default** — Respected. All 10 agents use `@observe` decorators. Langfuse traces mandatory.

**GATE RESULT: PASS** — No violations. All constitution constraints are met.

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-agent-orchestration/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── document-processing.json
│   ├── knowledge-structuring.json
│   ├── summary.json
│   ├── explanation.json
│   ├── translation.json
│   ├── diagram.json
│   ├── quiz.json
│   ├── revision.json
│   ├── progress.json
│   └── recommendation.json
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
app/backend/src/
├── agents/                  # NEW: Production agents
│   ├── __init__.py
│   ├── base.py              # Existing (extend with output validation)
│   ├── registry.py          # Existing (extend AgentType enum)
│   ├── contracts.py         # Existing (extend with agent-specific schemas)
│   ├── echo_agent.py        # Existing (unchanged)
│   ├── failing_agent.py     # Existing (unchanged)
│   ├── document_processing.py   # NEW: Document parsing, OCR, text cleaning
│   ├── knowledge_structuring.py # NEW: Chapter/topic/subtopic hierarchy
│   ├── summary.py               # NEW: Content summarization
│   ├── explanation.py           # NEW: Concept explanation
│   ├── translation.py           # NEW: Multilingual translation
│   ├── diagram.py               # NEW: Diagram data generation
│   ├── quiz.py                  # NEW: Quiz/assessment generation
│   ├── revision.py              # NEW: Revision notes & flashcards
│   ├── progress.py              # NEW: Learning event recording
│   └── recommendation.py        # NEW: Personalized study recommendations
├── orchestrator/            # EXTEND: Dependency resolution, incremental execution
│   ├── __init__.py
│   ├── orchestrator.py      # Existing (extend with pipeline orchestration)
│   ├── state_machine.py     # Existing (unchanged)
│   ├── retry.py             # Existing (unchanged)
│   ├── router.py            # Existing (extend with dependency graph)
│   └── pipeline.py          # NEW: Multi-agent pipeline with dependency resolution
├── retrieval/               # Existing (unchanged)
├── tracing/                 # Existing (unchanged)
├── models/
│   ├── agent_run.py         # Existing (extend AgentType enum)
│   └── processing_node.py   # NEW: Hierarchical document structure
├── schemas/
│   ├── agent.py             # Existing (extend with agent-specific schemas)
│   └── pipeline.py          # NEW: Pipeline request/response schemas
├── services/
│   ├── agent_service.py     # Existing (extend with pipeline invocation)
│   └── pipeline_service.py  # NEW: Pipeline orchestration service
├── api/
│   └── v1/
│       └── agent/
│           └── routes.py    # Existing (extend with pipeline endpoints)
└── core/
    └── config.py            # Existing (extend with pipeline config)

app/backend/tests/
├── agents/
│   ├── test_contracts.py        # Existing (extend)
│   ├── test_echo_agent.py       # Existing (unchanged)
│   ├── test_document_processing.py  # NEW
│   ├── test_knowledge_structuring.py # NEW
│   ├── test_summary.py          # NEW
│   ├── test_explanation.py      # NEW
│   ├── test_translation.py      # NEW
│   ├── test_diagram.py          # NEW
│   ├── test_quiz.py             # NEW
│   ├── test_revision.py         # NEW
│   ├── test_progress.py         # NEW
│   └── test_recommendation.py   # NEW
├── orchestrator/
│   ├── test_orchestrator.py     # Existing (extend)
│   ├── test_pipeline.py         # NEW: Pipeline orchestration tests
│   └── test_dependency.py       # NEW: Dependency resolution tests
└── integration/
    └── test_full_pipeline.py    # NEW: End-to-end pipeline test
```

**Structure Decision**: Backend monorepo with feature-based module organization. New agents follow the existing `BaseAgent` pattern. Pipeline orchestration adds `pipeline.py` to the orchestrator module. All new code extends existing modules rather than creating new top-level directories.

## Phase 0: Research & Unknowns

All technical context items are resolved from the existing Phase 3 infrastructure. Research focuses on agent-specific implementation patterns.

Research tasks:
1. Document parsing patterns (PDF, DOCX, TXT) for educational content
2. Hierarchical chapter/topic/subtopic extraction from raw text
3. LLM prompt patterns for grounded summarization with source references
4. Quiz generation with difficulty calibration and answer validation
5. Diagram data generation (Mermaid/Excalidraw) from text content
6. Progress tracking event schemas for learning analytics
7. Recommendation engine patterns using collaborative/content-based filtering
8. Multi-agent pipeline execution with dependency DAG resolution
9. Incremental processing with output caching and dependency validation

See `research.md` for consolidated findings.

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for full entity definitions including:
- ProcessingNode (hierarchical document structure)
- AgentOutput (generated content with source references)
- AgentType enum (extended with 10 new values)
- PipelineRequest/PipelineResponse schemas
- Agent-specific output schemas (SummaryOutput, QuizOutput, etc.)

### API Contracts

See `contracts/` for:
- `document-processing.json` — Document Processing agent output schema
- `knowledge-structuring.json` — Knowledge Structuring agent output schema
- `summary.json` — Summary agent output schema
- `explanation.json` — Explanation agent output schema
- `translation.json` — Translation agent output schema
- `diagram.json` — Diagram agent output schema
- `quiz.json` — Quiz agent output schema
- `revision.json` — Revision agent output schema
- `progress.json` — Progress agent output schema
- `recommendation.json` — Recommendation agent output schema
- `agent-api.yaml` — Updated OpenAPI spec with pipeline endpoints

### Quickstart

See `quickstart.md` for setup and validation instructions.

### Agent Context Update

Post-design, update the agent context file with new technology and architecture decisions.

## Complexity Tracking

> No Constitution violations detected. Complexity tracking section not required.
