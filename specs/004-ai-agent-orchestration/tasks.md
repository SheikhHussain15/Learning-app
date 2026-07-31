# Tasks: AI Agent Orchestration

**Input**: Design documents from `/specs/004-ai-agent-orchestration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `app/backend/src/`, `app/backend/tests/`
- **Models**: `app/backend/src/models/`
- **Agents**: `app/backend/src/agents/`
- **Schemas**: `app/backend/src/schemas/`
- **Orchestrator**: `app/backend/src/orchestrator/`
- **API**: `app/backend/src/api/v1/agent/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Extend existing infrastructure to support new agent types and entities

- [X] T001 Extend AgentType enum with new values (document_processing, knowledge_structuring, explanation, progress) in `app/backend/src/models/agent_run.py`
- [X] T002 [P] Create ProcessingNode model in `app/backend/src/models/processing_node.py`
- [X] T003 [P] Create AgentOutput model in `app/backend/src/models/agent_output.py`
- [X] T004 [P] Create ProgressEvent model in `app/backend/src/models/progress_event.py`
- [X] T005 [P] Create Pydantic schemas for agent-specific outputs (DocumentProcessingOutput, KnowledgeStructuringOutput, SummaryOutput, ExplanationOutput, TranslationOutput, DiagramOutput, QuizOutput, RevisionOutput, ProgressOutput, RecommendationOutput) in `app/backend/src/schemas/agent_outputs.py`
- [X] T006 [P] Create PipelineRequest/PipelineResponse schemas in `app/backend/src/schemas/pipeline.py`
- [X] T007 [P] Add Alembic migration for ProcessingNode, AgentOutput, ProgressEvent tables and extended AgentType enum
- [X] T008 Extend MODEL_REGISTRY with entries for document_processing, knowledge_structuring, explanation, progress in `app/backend/src/agents/registry.py`
- [X] T009 [P] Create base classes for production agents (DocumentProcessingAgent, KnowledgeStructuringAgent, SummaryAgent, ExplanationAgent, TranslationAgent, DiagramAgent, QuizAgent, RevisionAgent, ProgressAgent, RecommendationAgent) in `app/backend/src/agents/`

**Checkpoint**: Foundation ready - all new entities and schemas in place

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create Alembic migration for extended AgentType enum values (document_processing, knowledge_structuring, explanation, progress)
- [X] T011 [P] Implement document parsing utilities (PDF via pdfplumber, DOCX via python-docx, TXT via open()) in `app/backend/src/agents/document_processing.py`
- [X] T012 [P] Implement text cleaning pipeline (normalize whitespace, remove headers/footers, detect language, split into ~500-char chunks with overlap) in `app/backend/src/agents/document_processing.py`
- [X] T013 [P] Implement output validation utility that checks agent output against JSON Schema contracts in `app/backend/src/agents/base.py`
- [X] T014 Implement AgentOutput cache lookup/update logic (params_hash = sha256(json.dumps(agent_params, sort_keys=True))) in `app/backend/src/services/agent_service.py`
- [X] T015 [P] Create dependency graph configuration (Document Processing → Knowledge Structuring → [Summary, Explanation, Translation, Diagram, Quiz, Revision]) in `app/backend/src/orchestrator/pipeline.py`
- [X] T016 [P] Implement pipeline orchestration service with asyncio.gather() for parallel content agents in `app/backend/src/services/pipeline_service.py`
- [X] T017 Implement incremental processing logic (check cache, skip completed agents, validate dependencies) in `app/backend/src/services/pipeline_service.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Document Processing Pipeline (Priority: P1) 🎯 MVP

**Goal**: Transform raw educational documents into structured learning resources through Document Processing and Knowledge Structuring agents

**Independent Test**: Upload a simple document (PDF/TXT), verify it gets processed through Document Processing agent producing text chunks, then through Knowledge Structuring agent producing hierarchical chapter/topic/subtopic organization

### Implementation for User Story 1

- [X] T018 [US1] Implement DocumentProcessingAgent in `app/backend/src/agents/document_processing.py` - Parse documents (PDF/DOCX/TXT), extract text, clean content, generate chunks with metadata (page_number, section_header, position), return DocumentProcessingOutput
- [X] T019 [US1] Implement KnowledgeStructuringAgent in `app/backend/src/agents/knowledge_structuring.py` - Use LLM with response_format=json_schema to analyze chunks and generate hierarchical ProcessingNodeData (chapter→topic→subtopic), return KnowledgeStructuringOutput
- [X] T020 [US1] Create ProcessingNode CRUD operations in `app/backend/src/services/processing_node_service.py` - Create, read, update, delete ProcessingNode entities with tree traversal
- [X] T021 [US1] Extend Orchestrator.dispatch() to handle document_processing and knowledge_structuring agent types in `app/backend/src/orchestrator/orchestrator.py`
- [X] T022 [US1] Add pipeline endpoint for document processing in `app/backend/src/api/v1/agent/routes.py` - POST /api/v1/pipeline/invoke accepting PipelineRequest, returning PipelineResponse
- [X] T023 [US1] Validate Document Processing output against contracts/document-processing.json schema
- [X] T024 [US1] Validate Knowledge Structuring output against contracts/knowledge-structuring.json schema

**Checkpoint**: Document Processing → Knowledge Structuring pipeline works end-to-end

---

## Phase 4: User Story 1 Continued - Content Agents

**Goal**: Generate educational content (summaries, explanations, translations, diagrams, quizzes, revision materials) from structured documents

**Independent Test**: Given structured ProcessingNode hierarchy from US1, verify each content agent produces valid output with source_refs

### Implementation for Content Agents

- [X] T025 [P] [US1] Implement SummaryAgent in `app/backend/src/agents/summary.py` - Generate summaries with key_points and source_chunk_ids for each ProcessingNode, return SummaryOutput
- [X] T026 [P] [US1] Implement ExplanationAgent in `app/backend/src/agents/explanation.py` - Generate concept explanations with examples and complexity_level, return ExplanationOutput
- [X] T027 [P] [US1] Implement TranslationAgent in `app/backend/src/agents/translation.py` - Translate content with source_chunk_ids, return TranslationOutput
- [X] T028 [P] [US1] Implement DiagramAgent in `app/backend/src/agents/diagram.py` - Generate Mermaid/Excalidraw diagram data from content, return DiagramOutput
- [X] T029 [P] [US1] Implement QuizAgent in `app/backend/src/agents/quiz.py` - Generate questions with difficulty calibration (easy/medium/hard), 4 options each, source_chunk_ids, return QuizOutput
- [X] T030 [P] [US1] Implement RevisionAgent in `app/backend/src/agents/revision.py` - Generate revision notes and flashcards with source_chunk_ids, return RevisionOutput
- [X] T031 [US1] Register all content agents in `app/backend/src/agents/registry.py` MODEL_REGISTRY
- [X] T032 [US1] Update Orchestrator to support parallel content agent execution via asyncio.gather() in `app/backend/src/orchestrator/pipeline.py`
- [X] T033 [US1] Validate all content agent outputs against their respective JSON Schema contracts in `app/backend/src/agents/`

**Checkpoint**: Full document processing pipeline works: Document Processing → Knowledge Structuring → [all content agents in parallel]

---

## Phase 5: User Story 2 - Incremental Agent Execution (Priority: P2)

**Goal**: Avoid redundant agent execution through output caching and dependency validation

**Independent Test**: Run pipeline for one document, then request different output type without re-running completed agents

### Implementation for User Story 2

- [X] T034 [US2] Implement AgentOutput cache storage - Store agent outputs with (document_id, agent_type, params_hash) key in `app/backend/src/services/agent_service.py`
- [X] T035 [US2] Implement cache lookup before agent invocation - Check if matching output exists in `app/backend/src/services/pipeline_service.py`
- [X] T036 [US2] Implement cache invalidation on document re-processing - Delete related AgentOutput entries in `app/backend/src/services/agent_service.py`
- [X] T037 [US2] Add force_reprocess flag support in PipelineRequest to bypass cache in `app/backend/src/services/pipeline_service.py`
- [X] T038 [US2] Implement dependency validation - Ensure all required agents completed before running dependent agents in `app/backend/src/orchestrator/pipeline.py`
- [X] T039 [US2] Add pipeline status tracking (queued, running, succeeded, partial, failed) in `app/backend/src/schemas/pipeline.py`
- [X] T040 [US2] Implement partial pipeline execution - Return results for completed agents even if some fail in `app/backend/src/services/pipeline_service.py`

**Checkpoint**: Incremental processing reduces total processing time by 50%+ for subsequent requests

---

## Phase 6: User Story 3 - Error Handling and Recovery (Priority: P3)

**Goal**: Ensure system reliability and user trust when agent failures occur

**Independent Test**: Simulate various failure scenarios (network issues, processing errors) and verify graceful recovery

### Implementation for User Story 3

- [X] T041 [US3] Implement ProgressAgent in `app/backend/src/agents/progress.py` - Record learning events (quiz_completed, document_viewed, revision_studied, explanation_requested, recommendation_dismissed) in ProgressEvent table
- [X] T042 [US3] Implement RecommendationAgent in `app/backend/src/agents/recommendation.py` - Analyze ProgressEvent data, identify weak_areas, generate personalized recommendations, return RecommendationOutput
- [X] T043 [US3] Add ProgressEvent CRUD operations in `app/backend/src/services/progress_service.py`
- [X] T044 [US3] Implement fallback content generation when primary agents fail - Simplified explanations/quizzes as fallback in `app/backend/src/orchestrator/pipeline.py`
- [X] T045 [US3] Add error classification (retryable vs non-retryable) for all new agent types in `app/backend/src/orchestrator/retry.py`
- [X] T046 [US3] Implement graceful degradation - Return partial results when some agents fail in `app/backend/src/services/pipeline_service.py`
- [X] T047 [US3] Add user-friendly error messages with actionable options in `app/backend/src/api/v1/agent/routes.py`

**Checkpoint**: All user stories independently functional with proper error handling

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T048 [P] Add @observe decorators to all new agents for Langfuse tracing in `app/backend/src/agents/`
- [X] T049 [P] Add comprehensive logging for all agent operations in `app/backend/src/agents/`
- [X] T050 [P] Implement performance monitoring - Track agent execution times, token usage, success rates in `app/backend/src/tracing/`
- [X] T051 Add timeout handling for long-running agents (>5s target per agent) in `app/backend/src/orchestrator/orchestrator.py`
- [X] T052 Implement document ownership validation before processing in `app/backend/src/services/agent_service.py`
- [X] T053 Add user session isolation - Ensure no cross-user data leakage in `app/backend/src/services/pipeline_service.py`
- [X] T054 [P] Create integration test for full pipeline in `app/backend/tests/integration/test_full_pipeline.py`
- [X] T055 [P] Create pipeline orchestration tests in `app/backend/tests/orchestrator/test_pipeline.py`
- [X] T056 [P] Create dependency resolution tests in `app/backend/tests/orchestrator/test_dependency.py`
- [X] T057 Run quickstart.md validation - Verify all agent endpoints work correctly
- [X] T058 Code cleanup and refactoring - Ensure consistent code style across all agents
- [X] T059 Performance optimization - Parallel execution, efficient context sharing
- [X] T060 Security hardening - Document ownership, user isolation, no sensitive data exposure

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion - BLOCKS all user stories
- **User Story 1 (Phase 3+4)**: Depends on Phase 2 completion - MVP scope
- **User Story 2 (Phase 5)**: Depends on Phase 2 completion - Can start in parallel with US1
- **User Story 3 (Phase 6)**: Depends on Phase 2 completion - Can start in parallel with US1/US2
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Phase 2 - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Phase 2 - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- All content agents (T025-T030) can run in parallel within US1
- All test tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all content agents together (different files, no dependencies):
Task: "Implement SummaryAgent in app/backend/src/agents/summary.py"
Task: "Implement ExplanationAgent in app/backend/src/agents/explanation.py"
Task: "Implement TranslationAgent in app/backend/src/agents/translation.py"
Task: "Implement DiagramAgent in app/backend/src/agents/diagram.py"
Task: "Implement QuizAgent in app/backend/src/agents/quiz.py"
Task: "Implement RevisionAgent in app/backend/src/agents/revision.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T017) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 - Document Processing Pipeline (T018-T024)
4. Complete Phase 4: User Story 1 - Content Agents (T025-T033)
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Document Processing + Content Agents)
   - Developer B: User Story 2 (Incremental Execution)
   - Developer C: User Story 3 (Error Handling + Progress/Recommendation)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
