# Implementation Plan: AI Infrastructure

**Branch**: `003-ai-infrastructure` | **Date**: 2026-07-09 | **Spec**: specs/003-ai-infrastructure/spec.md
**Input**: Phase 3 AI Infrastructure specification for AI Learning Platform

## Summary

Establish the foundational AI infrastructure for the AI Learning Platform by integrating OpenRouter through the OpenAI Agents SDK, building a centralized Orchestrator with strict single-invocation-point semantics, defining a shared typed agent contract (Request/Response Envelopes), implementing Echo Agent for lifecycle validation, setting up ChromaDB + LlamaIndex for grounded retrieval, deploying Langfuse for observability, configuring MCP integrations, and implementing retry, timeout, error handling, and security policies — all validated by a full Orchestrator-to-Agent-to-Orchestrator lifecycle test.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript (frontend)  
**Primary Dependencies**: openai-agents, chromadb, llama-index, langfuse, fastapi, sqlalchemy, pydantic  
**Storage**: PostgreSQL (AgentRun, config), ChromaDB (vector embeddings)  
**Testing**: pytest + pytest-asyncio (unit, integration), Langfuse SDK test mode (trace verification)  
**Target Platform**: Linux server (Docker), local development (Windows/PowerShell)  
**Project Type**: Web application (FastAPI backend + Next.js frontend)  
**Performance Goals**: Orchestration overhead <100ms, retrieval <500ms, tracing <50ms, provider timeout 60s, total invocation timeout 180s  
**Constraints**: <200ms p95 orchestration overhead, <1s p95 retrieval, zero API key exposure in logs  
**Scale/Scope**: Single-tenant MVP supporting 10+ concurrent agent invocations, 50+ concurrent retrieval queries  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project Constitution is in template form (placeholders unset). None of the core principles, constraints, or governance rules are defined beyond structural placeholders. Therefore:

1. **Stable Agent Contracts** — Respected. The inter-agent contract (Request/Response Envelopes) is explicitly versioned with a defined evolution strategy.
2. **Orchestrator as Single Source of Truth** — Respected. The Orchestrator is the sole invocation point; no other component may call agents.
3. **Grounded AI Architecture** — Respected. Retrieval pipeline (LlamaIndex + ChromaDB) provides context for every agent invocation.
4. **Type Safety** — Respected. Envelopes are typed schemas (Pydantic), model registry is typed, state transitions are enforced.
5. **Production-First Architecture** — Respected. Retry/backoff, timeout, fallback, error classification, and observability designed from the start.
6. **Security by Default** — Respected. API keys in env only, trace privacy enforced, MCP permissions scoped, HTTPS/TLS.
7. **Documentation as Code** — Respected. This plan, spec, research, data model, and contracts are generated as documentation artifacts.
8. **AI-Friendly Codebase** — Respected. Centralized model registry, shared contracts, single orchestrator entry point.
9. **Observability by Default** — Respected. Langfuse traces mandatory for every invocation; observability failures never block operations.

**GATE RESULT: PASS** — No violations. All constitution constraints are met by the current design.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-infrastructure/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (/sp.specify command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── checklists/          # Quality validation checklists
```

### Source Code (repository root)

```text
app/backend/src/
├── agents/                  # NEW: AI Agent definitions
│   ├── __init__.py
│   ├── base.py              # Base agent class with contract validation
│   ├── echo_agent.py        # Echo (placeholder) agent
│   ├── registry.py          # Model registry configuration
│   └── contracts.py         # Request/Response Envelope schemas
├── orchestrator/            # NEW: Orchestrator framework
│   ├── __init__.py
│   ├── orchestrator.py      # Core orchestrator logic
│   ├── state_machine.py     # AgentRun state machine
│   ├── retry.py             # Retry/backoff strategy
│   └── router.py            # Agent routing and dependency resolution
├── retrieval/               # NEW: Retrieval infrastructure
│   ├── __init__.py
│   ├── indexer.py           # LlamaIndex indexing workflow
│   ├── retriever.py         # LlamaIndex retrieval workflow
│   └── chroma_client.py     # ChromaDB client wrapper
├── tracing/                 # NEW: Observability
│   ├── __init__.py
│   ├── langfuse_client.py   # Langfuse integration
│   └── trace_decorator.py   # Trace instrumentation decorators
├── mcp/                     # NEW: MCP integrations
│   ├── __init__.py
│   ├── base_mcp.py          # Base MCP server class
│   ├── google_drive_mcp.py  # Google Drive MCP tools
│   ├── notion_mcp.py        # Notion MCP tools
│   ├── tavily_mcp.py        # Tavily MCP tools
│   └── excalidraw_mcp.py    # Excalidraw MCP tools
├── models/
│   ├── __init__.py
│   ├── user.py              # Existing
│   └── agent_run.py         # NEW: AgentRun SQLAlchemy model
├── schemas/
│   ├── __init__.py
│   ├── user.py              # Existing
│   └── agent.py             # NEW: Agent-related Pydantic schemas
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Existing
│   │   └── agent.py         # NEW: Agent orchestration endpoints
│   └── deps.py
├── core/
│   ├── __init__.py
│   ├── config.py            # Existing (update for new env vars)
│   ├── database.py
│   └── security.py
├── services/
│   ├── __init__.py
│   └── agent_service.py     # NEW: Orchestrator service layer
├── middleware/
│   ├── __init__.py
│   ├── auth.py
│   └── logging.py           # Existing (update for AI-specific logging)
├── utils/
│   ├── __init__.py
│   └── logging_config.py    # Existing
└── main.py                  # FastAPI app (update)

app/backend/tests/
├── agents/
│   ├── test_contracts.py    # Envelope validation tests
│   └── test_echo_agent.py   # Echo Agent integration tests
├── orchestrator/
│   ├── test_orchestrator.py # Orchestrator lifecycle tests
│   ├── test_state_machine.py# State transition tests
│   └── test_retry.py        # Retry/backoff tests
├── retrieval/
│   ├── test_indexer.py      # Indexing workflow tests
│   └── test_retriever.py    # Retrieval workflow tests
├── tracing/
│   └── test_tracing.py      # Langfuse integration tests
├── mcp/
│   └── test_mcp.py          # MCP integration tests
└── conftest.py              # Shared fixtures (update)
```

**Structure Decision**: Backend monorepo with feature-based module organization. New directories mirror the existing `models/`, `schemas/`, `api/routes/`, `services/`, `core/` pattern. Each AI subsystem (agents, orchestrator, retrieval, tracing, mcp) gets its own top-level module under `src/`. This follows the existing FastAPI conventions.

## Phase 0: Research & Unknowns

No NEEDS CLARIFICATION markers exist in the specification. All technical context items are known from the spec and existing codebase. Research is focused on integration best practices.

Research tasks:
1. OpenRouter API compatibility with OpenAI Agents SDK
2. ChromaDB persistent mode configuration on Windows/Linux
3. Langfuse Python SDK trace hierarchy patterns
4. LlamaIndex ChromaDB vector store integration patterns
5. OpenAI Agents SDK MCP tool registration patterns
6. Exponential backoff implementation patterns in Python (tenacity, backoff libs)

See `research.md` for consolidated findings.

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for full entity definitions including:
- AgentRun (execution history)
- AgentType enum
- AgentStatus enum
- RequestEnvelope schema
- ResponseEnvelope schema
- ErrorInfo schema
- ModelConfig schema

### API Contracts

See `contracts/` for:
- `request-envelope.json` — Request Envelope JSON Schema
- `response-envelope.json` — Response Envelope JSON Schema
- `agent-api.yaml` — OpenAPI spec for agent orchestration endpoints

### Quickstart

See `quickstart.md` for setup and validation instructions.

### Agent Context Update

Post-design, update the agent context file with new technology and architecture decisions.

## Complexity Tracking

> No Constitution violations detected. Complexity tracking section not required.
