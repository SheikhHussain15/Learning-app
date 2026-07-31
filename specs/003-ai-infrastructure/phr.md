# Project History Record: AI Infrastructure (003-ai-infrastructure)

**Branch**: `003-ai-infrastructure`  
**Date Range**: 2026-07-09 — 2026-07-10  
**Status**: ✅ Complete  

## Summary

Built the foundational AI infrastructure for the AI Learning Platform: OpenRouter provider via OpenAI Agents SDK, centralized Orchestrator with typed agent contracts, Echo Agent for lifecycle validation, ChromaDB + LlamaIndex retrieval pipeline, Langfuse observability, MCP integrations (Drive, Notion, Tavily, Excalidraw), retry/fallback with exponential backoff, and security hardening — all validated by 87 passing tests.

## Deliverables

### Phase 1: Setup (T001–T011)
- Added deps: `openai-agents`, `chromadb`, `llama-index`, `langfuse`, `tenacity` to `requirements.txt`
- Created 10 new directories with `__init__.py` under `src/agents/`, `src/orchestrator/`, `src/retrieval/`, `src/tracing/`, `src/mcp/` and `tests/` mirrors

### Phase 2: Foundational (T012–T022)
- `.env` vars for OpenRouter, Langfuse, ChromaDB, LlamaIndex
- `config.py` — all AI env vars loaded via `os.getenv` with defaults
- `models/agent_run.py` — `AgentRun` ORM model, `AgentType`/`AgentStatus` enums
- `schemas/agent.py` — `RequestEnvelope`, `ResponseEnvelope`, `TokenUsage`, `ErrorInfo`, `RequestContext`, `RetrievedChunk`, `SourceRef`, `AgentRunCreate`, `AgentRunResponse`
- `agents/registry.py` — `ModelConfig` schema, `create_openai_provider()`, `MODEL_REGISTRY` mapping each `AgentType` to primary+fallback model IDs

### Phase 3: US1 — Echo Agent Lifecycle (T023–T039)
- `agents/contracts.py` — re-exports envelope schemas
- `agents/base.py` — abstract `BaseAgent` with `validate()` and `make_error_response()`
- `orchestrator/state_machine.py` — `validate_transition()`, `can_transition()`, `is_terminal()`
- `orchestrator/retry.py` — `RetryableError`, `NonRetryableError`, `classify_error()`
- `orchestrator/router.py` — agent registry, `_init_default_agents()` factory
- `agents/echo_agent.py` — `EchoAgent` echoes IDs, returns dummy token usage (50/20/70)
- `orchestrator/orchestrator.py` — `Orchestrator.dispatch()`: full lifecycle with DB persistence, retry, fallback, state transitions, logging
- `services/agent_service.py` — `invoke_agent()`, `get_run()`, `list_runs()`
- `api/v1/agent/routes.py` — `POST /agents/{agent_type}/invoke`, `GET /agents/runs`, `GET /agents/runs/{run_id}`
- Tests: `test_contracts.py` (8), `test_echo_agent.py` (4), `test_state_machine.py` (4), `test_orchestrator.py` (2)

### Phase 4: US2 — Langfuse Observability (T040–T046)
- `tracing/langfuse_client.py` — `get_langfuse()` singleton (returns `None` on invalid config)
- `tracing/trace_decorator.py` — `@trace_agent`, `@trace_orchestrator` decorators (fail-open: errors logged, never raised)
- Orchestrator integration: root trace → agent span → observations
- Tests: `test_tracing.py` (4) — trace creation, failure resilience

### Phase 5: US3 — Retrieval Pipeline (T047–T054)
- `retrieval/chroma_client.py` — `ChromaClientWrapper` singleton, `PersistentClient`, `get_or_create_collection()`
- `retrieval/indexer.py` — `Indexer` with lazy embedding model init, `index_document()`
- `retrieval/retriever.py` — `Retriever` with `retrieve()` (top-10, min 0.5 score, empty query guard)
- Orchestrator integration: retrieval context assembled into `RequestEnvelope.context.chunks`
- Tests: `test_indexer.py` (3), `test_retriever.py` (4)

### Phase 6: US4 — Retry & Fallback (T055–T063)
- `agents/failing_agent.py` — `FailingAgent` returns `RetryableError` on demand
- Orchestrator retry loop: 3 primary attempts → fallback model → 3 fallback attempts
- Timeout enforcement: provider 60s, invocation 180s, workflow 300s
- Error classification: 429/502/503/timeout = retryable; 401/403/404/invalid = non-retryable
- Tests: `test_retry.py` (10) — classification, backoff, max retries, fallback, non-retryable

### Phase 7: MCP Integration (T064–T070)
- `mcp/base_mcp.py` — abstract `BaseMCPServer` with `FunctionTool` registration
- `mcp/google_drive_mcp.py` — `read_drive_file`, `list_drive_files`
- `mcp/notion_mcp.py` — `read_notion_page`, `query_notion_database`
- `mcp/tavily_mcp.py` — `web_search`
- `mcp/excalidraw_mcp.py` — `create_excalidraw_diagram`
- All registered with Echo Agent for validation
- Tests: `test_mcp.py` (12) — server name, get_tools, tool invocation

### Phase 8: Polish & Cross-Cutting (T071–T076)
- `middleware/logging.py` — `SensitiveDataFilter` redacts API keys, secrets, tokens, passwords, auth headers
- `middleware/error_handler.py` — `ai_error_handler`: `RetryableError` → 502, `NonRetryableError` → 400
- `tests/conftest.py` — shared fixtures: `mock_langfuse`, `test_chroma_client`, `db`
- `tests/benchmarks/test_performance.py` — orchestration <100ms, retrieval <500ms, tracing <50ms

## Test Results

```
87 passed, 1 failed (pre-existing) in 34.81s
```

**All new tests pass** (agents, orchestrator, retrieval, tracing, MCP, benchmarks).

**1 pre-existing failure** — `test_get_profile_unauthenticated` expects 401 but FastAPI returns 403 (auth middleware issue, not related to this phase).

## Key Architecture Decisions

| Decision | Rationale |
|---|---|
| **OpenRouter via OpenAI Agents SDK** | Single provider gateway; custom `OpenAIProvider` with base URL = `https://openrouter.ai/api/v1` |
| **Orchestrator as sole invocation point** | Strict single-entry pattern; no agent calls another agent |
| **No tenacity for retry** | Manual exponential backoff loop in orchestrator (more control, no extra dep at runtime) |
| **Langfuse fail-open** | `get_langfuse()` returns `None` on invalid config; decorators catch/log all errors |
| **Per-document ChromaDB collections** | `doc_{document_id}` naming; simple isolation without multi-tenant complexity |
| **FunctionTool for MCP** | OpenAI Agents SDK native tool system; no MCP protocol server needed |
| **Pydantic V1 compat for langfuse** | Langfuse SDK uses V1 internally; warning is cosmetic on Python 3.14 |

## Known Issues

1. `test_get_profile_unauthenticated` — FastAPI returns 403 instead of 401 (pre-existing auth middleware)
2. Langfuse Pydantic V1 warning on Python 3.14 — cosmetic, `langfuse` SDK internally uses V1
3. Deprecation warnings for `datetime.utcnow()` — used throughout orchestrator, needs `datetime.now(datetime.UTC)` migration

## Files Changed

### New files (41)
```
src/agents/__init__.py
src/agents/contracts.py
src/agents/base.py
src/agents/echo_agent.py
src/agents/failing_agent.py
src/agents/registry.py
src/orchestrator/__init__.py
src/orchestrator/orchestrator.py
src/orchestrator/state_machine.py
src/orchestrator/retry.py
src/orchestrator/router.py
src/retrieval/__init__.py
src/retrieval/chroma_client.py
src/retrieval/indexer.py
src/retrieval/retriever.py
src/tracing/__init__.py
src/tracing/langfuse_client.py
src/tracing/trace_decorator.py
src/mcp/__init__.py
src/mcp/base_mcp.py
src/mcp/google_drive_mcp.py
src/mcp/notion_mcp.py
src/mcp/tavily_mcp.py
src/mcp/excalidraw_mcp.py
src/models/agent_run.py
src/schemas/agent.py
src/services/agent_service.py
src/api/v1/agent/__init__.py
src/api/v1/agent/routes.py
src/middleware/logging.py
src/middleware/error_handler.py
tests/agents/__init__.py
tests/agents/test_contracts.py
tests/agents/test_echo_agent.py
tests/orchestrator/__init__.py
tests/orchestrator/test_orchestrator.py
tests/orchestrator/test_state_machine.py
tests/orchestrator/test_retry.py
tests/retrieval/__init__.py
tests/retrieval/test_indexer.py
tests/retrieval/test_retriever.py
tests/tracing/__init__.py
tests/tracing/test_tracing.py
tests/mcp/__init__.py
tests/mcp/test_mcp.py
tests/benchmarks/test_performance.py
```

### Modified files (6)
```
requirements.txt           — added AI deps
.env                       — added AI env vars
src/core/config.py         — added AI config loading
src/main.py                — added agent router, agent_runs table creation
tests/conftest.py          — added shared fixtures
specs/003-ai-infrastructure/tasks.md — all 76 tasks marked complete
```

## Next Steps

Phase 4 can begin: implement real AI agents (Summary, Quiz, Translation, Diagram, Revision, Recommendation) using the Echo Agent as a template. The Orchestrator, contracts, retrieval, tracing, and MCP layers are all ready.
