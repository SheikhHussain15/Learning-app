# Tasks: AI Infrastructure

**Input**: Design documents from `specs/003-ai-infrastructure/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Test tasks are included for acceptance criteria validation (AC-001 through AC-009).

**Organization**: Tasks are grouped by user story for independent implementation.

## Format: `[ID] [P] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: User story this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `app/backend/src/`
- **Tests**: `app/backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency installation, and directory structure

- [x] T001 Add new AI dependencies to `app/backend/requirements.txt` (openai-agents, chromadb, llama-index, langfuse, tenacity)
- [x] T002 [P] Create `app/backend/src/agents/` directory with `__init__.py`
- [x] T003 [P] Create `app/backend/src/orchestrator/` directory with `__init__.py`
- [x] T004 [P] Create `app/backend/src/retrieval/` directory with `__init__.py`
- [x] T005 [P] Create `app/backend/src/tracing/` directory with `__init__.py`
- [x] T006 [P] Create `app/backend/src/mcp/` directory with `__init__.py`
- [x] T007 [P] Create `app/backend/tests/agents/` directory with `__init__.py`
- [x] T008 [P] Create `app/backend/tests/orchestrator/` directory with `__init__.py`
- [x] T009 [P] Create `app/backend/tests/retrieval/` directory with `__init__.py`
- [x] T010 [P] Create `app/backend/tests/tracing/` directory with `__init__.py`
- [x] T011 [P] Create `app/backend/tests/mcp/` directory with `__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

- [x] T012 Add environment variables to `app/backend/.env` for OpenRouter, Langfuse, ChromaDB, LlamaIndex, agent config, logging
- [x] T013 Add environment variable loading for new config keys in `app/backend/src/core/config.py`
- [x] T014 Create AgentRun SQLAlchemy model in `app/backend/src/models/agent_run.py`
- [x] T015 Create AgentType and AgentStatus Python enums in `app/backend/src/models/agent_run.py`
- [x] T016 [P] Create Pydantic schemas for RequestEnvelope, ResponseEnvelope, TokenUsage, ErrorInfo, RequestContext, RetrievedChunk, SourceRef in `app/backend/src/schemas/agent.py`
- [x] T017 [P] Create AgentRunCreate, AgentRunResponse Pydantic schemas in `app/backend/src/schemas/agent.py`
- [x] T018 [P] Create ModelConfig Pydantic schema in `app/backend/src/agents/registry.py`
- [x] T019 Create OpenRouter provider configuration using OpenAI Agents SDK in `app/backend/src/agents/registry.py`
- [x] T020 Create model registry with pinned model IDs for all agent types in `app/backend/src/agents/registry.py`
- [x] T021 Register new models in `app/backend/src/main.py` agent_run import
- [x] T022 Update SQLite/PostgreSQL database tables with `Base.metadata.create_all` for agent_runs table

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — Developer Validates Infrastructure with Echo Agent (Priority: P1) 🎯 MVP

**Goal**: Dispatch a request through the Orchestrator to the Echo Agent and receive a valid response, proving the entire AI pipeline works.

**Independent Test**: POST to `/api/v1/agents/echo/invoke` with a valid RequestEnvelope and verify response contains echoed identifiers and status "success".

### Implementation for User Story 1

- [x] T023 [P] [US1] Create contract schemas module in `app/backend/src/agents/contracts.py` with RequestEnvelope, ResponseEnvelope, TokenUsage, ErrorInfo, RequestContext, RetrievedChunk, SourceRef
- [x] T024 [P] [US1] Create base agent class in `app/backend/src/agents/base.py` with envelope validation and response construction
- [x] T025 [P] [US1] Create state machine logic in `app/backend/src/orchestrator/state_machine.py` with transition validation for queued/running/succeeded/failed/cancelled
- [x] T026 [P] [US1] Create retry/backoff strategy in `app/backend/src/orchestrator/retry.py` with RetryableError, NonRetryableError, tenacity retry policy, exponential backoff with jitter
- [x] T027 [P] [US1] Create agent routing and dependency resolution in `app/backend/src/orchestrator/router.py`
- [x] T028 [P] [US1] Create Echo Agent in `app/backend/src/agents/echo_agent.py` — validates envelope, echoes document_id/node_ids/trace_id, returns dummy usage
- [x] T029 [US1] Create core Orchestrator in `app/backend/src/orchestrator/orchestrator.py` — handles dispatch, retry, fallback, state management, response aggregation
- [x] T030 [US1] Create Agent service layer in `app/backend/src/services/agent_service.py` — bridges API to Orchestrator
- [x] T031 [US1] Create agent API routes in `app/backend/src/api/v1/agent/__init__.py` with POST /agents/{agent_type}/invoke
- [x] T032 [US1] Create agent API routes in `app/backend/src/api/v1/agent/routes.py` — invoke, get_run, list_runs endpoints
- [x] T033 [US1] Register agent router in `app/backend/src/api/v1/__init__.py`
- [x] T034 [US1] Add Echo Agent import and table creation for agent_runs in `app/backend/src/main.py`
- [x] T035 [US1] Add logging for orchestrator lifecycle events in `app/backend/src/orchestrator/orchestrator.py`

### Test for User Story 1

- [x] T036 [US1] Create contract validation tests in `app/backend/tests/agents/test_contracts.py` — valid/invalid envelopes, schema evolution
- [x] T037 [US1] Create Echo Agent integration test in `app/backend/tests/agents/test_echo_agent.py` — valid request returns success with echoed IDs, invalid returns error
- [x] T038 [US1] Create state machine transition tests in `app/backend/tests/orchestrator/test_state_machine.py` — valid transitions pass, invalid transitions rejected
- [x] T039 [US1] Create orchestrator lifecycle integration test in `app/backend/tests/orchestrator/test_orchestrator.py` — full queued→running→succeeded cycle

**Checkpoint (AC-001, AC-002)**: Echo Agent completes full Orchestrator→Agent→Orchestrator lifecycle. AgentRun state transitions correctly recorded.

---

## Phase 4: User Story 2 — Developer Verifies Observability with Langfuse (Priority: P1)

**Goal**: Every agent invocation produces a Langfuse trace with latency, model info, token usage, and status.

**Independent Test**: Dispatch Echo Agent request, then query Langfuse for trace and verify all required fields are present. No Langfuse failure blocks operations.

### Implementation for User Story 2

- [x] T040 [P] [US2] Create Langfuse client wrapper in `app/backend/src/tracing/langfuse_client.py` — initialize with public/secret keys, host URL
- [x] T041 [P] [US2] Create trace decorators in `app/backend/src/tracing/trace_decorator.py` — @trace_agent, @trace_orchestrator decorators for automatic span creation
- [x] T042 [US2] Integrate Langfuse tracing into Orchestrator in `app/backend/src/orchestrator/orchestrator.py` — create root trace, child agent span, observations
- [x] T043 [US2] Integrate trace failure handling — Langfuse errors logged but never block agent execution in `app/backend/src/orchestrator/orchestrator.py`
- [x] T044 [US2] Add trace_id propagation from API request to RequestEnvelope to Langfuse trace in `app/backend/src/services/agent_service.py`

### Test for User Story 2

- [x] T045 [US2] Create Langfuse tracing integration test in `app/backend/tests/tracing/test_tracing.py` — trace created with correct hierarchy, fields populated
- [x] T046 [US2] Create Langfuse failure resilience test in `app/backend/tests/tracing/test_tracing.py` — agent completes successfully when Langfuse is unreachable

**Checkpoint (AC-003, AC-009)**: Langfuse produces complete traces for every invocation. Langfuse failures never block operations.

---

## Phase 5: User Story 3 — Developer Validates Retrieval Pipeline (Priority: P1)

**Goal**: Index a document into ChromaDB via LlamaIndex and retrieve relevant chunks with metadata and similarity scores.

**Independent Test**: Index a test document, query it, and verify chunks are returned with similarity scores above the minimum threshold and correct metadata.

### Implementation for User Story 3

- [x] T047 [P] [US3] Create ChromaDB client wrapper in `app/backend/src/retrieval/chroma_client.py` — PersistentClient with configurable path, collection management
- [x] T048 [P] [US3] Create LlamaIndex indexer in `app/backend/src/retrieval/indexer.py` — embedding model config, chunk embedding, ChromaDB storage, indexing lifecycle
- [x] T049 [P] [US3] Create LlamaIndex retriever in `app/backend/src/retrieval/retriever.py` — query embedding, similarity search (top-10, min 0.5 threshold), result assembly
- [x] T050 [US3] Expose retrieval results as context in RequestEnvelope via Orchestrator in `app/backend/src/orchestrator/orchestrator.py`
- [x] T051 [US3] Create health endpoint for ChromaDB connectivity check in `app/backend/src/api/v1/agent/routes.py`

### Test for User Story 3

- [x] T052 [US3] Create indexer integration test in `app/backend/tests/retrieval/test_indexer.py` — document indexed, ChromaDB contains entries with correct metadata
- [x] T053 [US3] Create retrieval integration test in `app/backend/tests/retrieval/test_retriever.py` — query returns top-K chunks above similarity threshold, unrelated query returns zero
- [x] T054 [US3] Create end-to-end retrieval test with Echo Agent in `app/backend/tests/agents/test_echo_agent.py` — context.chunks populated from retrieval

**Checkpoint (AC-004)**: LlamaIndex retrieves relevant chunks from ChromaDB with similarity scores above 0.5 threshold.

---

## Phase 6: User Story 4 — Developer Validates Retry and Fallback Behavior (Priority: P2)

**Goal**: Orchestrator correctly retries on failure with exponential backoff and falls back to alternative model when primary fails.

**Independent Test**: Configure a deliberately failing agent, dispatch through Orchestrator, and verify retry behavior in AgentRun errors array and fallback invocation.

### Implementation for User Story 4

- [x] T055 [US4] Create deliberately failing test agent in `app/backend/src/agents/failing_agent.py` — always returns retryable error for timeout testing
- [x] T056 [US4] Integrate fallback model switching into Orchestrator in `app/backend/src/orchestrator/orchestrator.py` — after 3 primary retries, switch to fallback model
- [x] T057 [US4] Add timeout enforcement at provider (60s), invocation (180s), and workflow (300s) levels in `app/backend/src/orchestrator/orchestrator.py`
- [x] T058 [US4] Add cancellation signal handling in `app/backend/src/orchestrator/orchestrator.py` — immediately transitions to cancelled terminal state
- [x] T059 [US4] Add error classification (retryable vs non-retryable) in `app/backend/src/orchestrator/retry.py` — map HTTP status codes and error types

### Test for User Story 4

- [x] T060 [US4] Create retry/backoff integration test in `app/backend/tests/orchestrator/test_retry.py` — retryable error triggers backoff, retry count increments, max retries exhausted = failed
- [x] T061 [US4] Create fallback model test in `app/backend/tests/orchestrator/test_retry.py` — primary fails all 3 attempts, fallback invoked and returns success
- [x] T062 [US4] Create timeout test in `app/backend/tests/orchestrator/test_retry.py` — deliberately slow agent exceeds timeout and is cancelled
- [x] T063 [US4] Create non-retryable failure test in `app/backend/tests/orchestrator/test_retry.py` — invalid contract returns error immediately, no retries

**Checkpoint (AC-005, AC-006, AC-007, AC-008)**: Retry and exponential backoff work with failing agent. Timeouts correctly terminate. Fallback model invoked. Contract validation rejects invalid envelopes.

---

## Phase 7: MCP Integration (Priority: P2)

**Goal**: MCP servers registered as tools with the OpenAI Agents SDK with defined permissions and authentication.

**Independent Test**: Each MCP server's tools appear in an agent's available tool list and can be invoked.

### Implementation for MCP Integration

- [x] T064 [P] Create Base MCP server class in `app/backend/src/mcp/base_mcp.py` — FunctionTool registration pattern, credential loading from env
- [x] T065 [P] Create Google Drive MCP in `app/backend/src/mcp/google_drive_mcp.py` — read_drive_file, list_drive_files tools (OAuth 2.0, read-only)
- [x] T066 [P] Create Notion MCP in `app/backend/src/mcp/notion_mcp.py` — read_notion_page, query_notion_database tools (API token, read-only)
- [x] T067 [P] Create Tavily MCP in `app/backend/src/mcp/tavily_mcp.py` — web_search tool (API key, search only)
- [x] T068 [P] Create Excalidraw MCP in `app/backend/src/mcp/excalidraw_mcp.py` — create_excalidraw_diagram tool (no auth, file-based output)
- [x] T069 Register MCP servers with Echo Agent in `app/backend/src/agents/echo_agent.py` — all MCP tools registered for validation

### Test for MCP Integration

- [x] T070 Create MCP integration tests in `app/backend/tests/mcp/test_mcp.py` — tool registration, credential loading, tool invocation

**Checkpoint**: MCP integrations configured and validated. GitHub MCP decision documented (remains dev tooling, not user-facing).

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, error handling, logging, and verification

- [x] T071 [P] Add structured JSON logging with redaction middleware in `app/backend/src/middleware/logging.py` — never log API keys, secrets, tokens, passwords, authorization headers
- [x] T072 [P] Add error handling middleware for provider failures, model failures, timeout, invalid contracts, orchestration failures, vector DB failures, tracing failures in `app/backend/src/middleware/error_handler.py`
- [x] T073 [P] Add security validation — API key management (env only), trace privacy (no PII in Langfuse), MCP credential scoping
- [x] T074 [P] Create shared test fixtures in `app/backend/tests/conftest.py` — mock OpenRouter provider, test ChromaDB instance, mock Langfuse client
- [x] T075 Add performance benchmarks in `app/backend/tests/benchmarks/test_performance.py` — orchestration overhead <100ms, retrieval <500ms, tracing <50ms
- [x] T076 Run final validation per `specs/003-ai-infrastructure/quickstart.md` — verify Echo Agent lifecycle, Langfuse traces, ChromaDB retrieval, retry behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US1 — Echo Agent (Phase 3)**: Depends on Foundational — MVP core
- **US2 — Langfuse (Phase 4)**: Depends on Foundational + US1 (Orchestrator must exist to trace)
- **US3 — Retrieval (Phase 5)**: Depends on Foundational — independent of US1/US2 but integrates with Orchestrator
- **US4 — Retry/Fallback (Phase 6)**: Depends on US1 (Orchestrator must exist to test retry)
- **MCP (Phase 7)**: Depends on Foundational + US1 (agent tool system needed)
- **Polish (Phase 8)**: Depends on all desired phases complete

### User Story Dependencies

- **US1 (P1) — Echo Agent Lifecycle**: Can start after Foundational — No story dependencies
- **US2 (P1) — Langfuse Observability**: Depends on US1 (needs Orchestrator) — integrates tracing into existing flow
- **US3 (P1) — Retrieval Pipeline**: No story dependencies — independent pipeline
- **US4 (P2) — Retry/Fallback**: Depends on US1 (needs Orchestrator) — adds retry to existing flow

### Within Each Phase

- Models before services
- Services before endpoints
- Core implementation before integration
- Tests after implementation (for validation)
- Phase complete before moving to next

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Foundational tasks T016,T017,T018 can run in parallel (different schemas)
- US1 tasks T023-T028 can all run in parallel (different files, no dependencies)
- US2 tasks T040,T041 can run in parallel
- US3 tasks T047,T048,T049 can run in parallel
- US4 tasks can run in parallel within the phase
- MCP tasks T064-T068 can all run in parallel (independent MCP server implementations)
- Polish tasks T071,T072,T073 can run in parallel

### Parallel Example: User Story 1

```bash
# All parallel tasks for US1 can launch together:
Task: T023 Create contract schemas in app/backend/src/agents/contracts.py
Task: T024 Create base agent class in app/backend/src/agents/base.py
Task: T025 Create state machine logic in app/backend/src/orchestrator/state_machine.py
Task: T026 Create retry/backoff in app/backend/src/orchestrator/retry.py
Task: T027 Create agent routing in app/backend/src/orchestrator/router.py
Task: T028 Create Echo Agent in app/backend/src/agents/echo_agent.py
```

---

## Implementation Strategy

### MVP First (Phase 3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 — Echo Agent Lifecycle
4. **STOP and VALIDATE**: Test AC-001 (Echo Agent lifecycle) and AC-002 (AgentRun transitions)
5. Deploy/demo the infrastructure foundation

### Incremental Delivery

1. Setup + Foundational → Foundation with models, schemas, provider
2. Phase 3 (US1 — Echo Agent) → Working end-to-end lifecycle! (MVP)
3. Phase 4 (US2 — Langfuse) → Observability added to lifecycle
4. Phase 5 (US3 — Retrieval) → Grounded retrieval available
5. Phase 6 (US4 — Retry) → Production resilience validated
6. Phase 7 (MCP) → External tool integrations ready

### Parallel Team Strategy

With multiple developers:

1. **Team**: Setup + Foundational together
2. **Dev A**: US1 (Echo Agent + Orchestrator) — core lifecycle
3. **Dev B**: US3 (Retrieval Pipeline) — independent of US1
4. **Dev C**: MCP integrations — independent
5. After US1 done → Dev A adds US2 (Langfuse) and US4 (Retry)
6. Integration testing after all phases

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story independently testable
- Stop at checkpoints to validate
- Commit after each logical task group
- Verify tests fail before implementation where applicable
