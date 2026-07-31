# Feature Specification: AI Infrastructure

**Feature Branch**: `003-ai-infrastructure`  
**Created**: 2026-07-09  
**Status**: Draft  
**Input**: Phase 3 AI Infrastructure specification for AI Learning Platform

## Executive Summary

This specification defines the foundational AI infrastructure for the AI Learning Platform. It establishes a production-ready orchestration, observability, retrieval, and communication layer that every future AI agent will depend upon. The infrastructure is validated using a placeholder Echo Agent that proves the Orchestrator-to-Agent lifecycle works correctly before real AI agents are implemented in Phase 4. The architecture centers on an Orchestrator that acts as the sole entry point for all agent invocations, a shared Agent Contract that ensures type-safe communication, a vector retrieval pipeline (LlamaIndex on ChromaDB) for grounded AI responses, and Langfuse-based observability for every invocation.

## Goals

1. Establish a centralized Orchestrator as the single point of control for all AI agent interactions.
2. Define a stable, versioned inter-agent contract (request/response envelopes) shared by every agent.
3. Provide a working end-to-end lifecycle (Orchestrator to Agent to Orchestrator) validated by a placeholder Echo Agent.
4. Integrate retrieval infrastructure (LlamaIndex + ChromaDB) for grounded content lookups.
5. Ensure every AI request produces observable traces via Langfuse.
6. Enforce retry, timeout, and error handling policies without hardcoding them in individual agents.

## Scope

### In Scope

- AI provider integration via OpenRouter through the OpenAI Agents SDK.
- Centralized model registry with pinned models and fallback strategies.
- Orchestrator architecture for request routing, dependency resolution, context passing, retry handling, state management, and response aggregation.
- Inter-Agent Contract (Request Envelope and Response Envelope) with validation rules and schema evolution.
- Echo Agent placeholder for lifecycle validation.
- AgentRun entity for execution history, separated from generated outputs.
- State machine (queued, running, succeeded, failed, cancelled) with transition rules.
- Retry strategy with exponential backoff, retryable/non-retryable failure classification.
- LlamaIndex architecture for indexing and retrieval workflows.
- ChromaDB architecture for vector storage and similarity search.
- Langfuse integration for tracing, latency, model info, token usage, execution status, and errors.
- MCP integration architecture for Google Drive, Notion, Tavily, and Excalidraw.
- Configuration management for all infrastructure components.
- Error handling strategy for provider, model, timeout, contract, orchestration, vector database, and tracing failures.
- Security requirements for API keys, authentication, MCP permissions, and trace privacy.
- Logging requirements for debugging without exposing sensitive information.
- Performance budgets for orchestration, retrieval, tracing, and provider timeouts.

### Out of Scope

- Summary Agent, Quiz Agent, Translation Agent, Diagram Agent, Revision Agent, Recommendation Agent implementation.
- Document Processing, Knowledge Structuring, AI Tutor, Dashboard, Learning Workspace, Frontend UI.
- Chunking algorithm details (deferred to Phase 4).
- Real AI agent logic or educational content generation.

## AI Infrastructure Overview

**OpenAI Agents SDK**: Runtime for defining, configuring, and executing AI agents. Handles function calling, tool execution, streaming, and agent lifecycle. Every agent is an instance of an OpenAI Agent with system prompt, tools, and model binding.

**OpenRouter**: Unified AI provider gateway. All model requests pass through OpenRouter, which routes to the appropriate underlying provider. Provides single API surface, model availability abstraction, and cost tracking. The platform never calls individual providers directly.

**Orchestrator**: The only component permitted to invoke AI agents. Receives client requests, resolves dependencies, constructs request envelopes, dispatches to the correct agent, handles retries and timeouts, aggregates responses, and persists execution history.

**Specialized Agents**: Task-specific AI agents (Summary, Quiz, Translation, Diagram, Revision, Recommendation) that receive a standardized Request Envelope and return a standardized Response Envelope. Each agent is stateless. Not invoked in Phase 3 — contracts defined and validated by the Echo Agent.

**ChromaDB**: Vector database storing document chunks as embeddings with metadata. Provides similarity search for retrieving semantically relevant content.

**LlamaIndex**: Retrieval framework orchestrating the indexing and retrieval pipeline. Manages chunk-to-embedding conversion, constructs the vector index within ChromaDB, and provides query engines for grounded AI responses.

**Langfuse**: Observability platform. Every AI request produces a trace with latency, model info, token usage, execution status, and errors. Traces span multiple agent calls, linking parent Orchestrator traces to child agent traces.

**PostgreSQL**: Stores non-vector data: AgentRun execution history, document metadata, user data, and configuration state. Agent-generated outputs stored here separate from execution history.

**MCP Servers**: External tool integrations (Google Drive, Notion, Tavily, Excalidraw) via Model Context Protocol. Registered with the OpenAI Agents SDK tool system.

## AI Provider Architecture

**Provider Architecture**: All AI model requests use OpenRouter as the unified provider. The OpenAI Agents SDK is configured with a custom OpenAIProvider whose base URL points to https://openrouter.ai/api/v1.

**API Configuration**: Base URL: https://openrouter.ai/api/v1. Authentication: Bearer token via environment variable. Headers: HTTP-Referer and X-Title for OpenRouter analytics.

**Model Routing**: Models are not selected dynamically. Each agent has a pinned primary and fallback model from the centralized registry. SDK configured per-agent with model ID string.

**Model Pinning**: Echo/Orchestrator: gpt-4o-mini → claude-3-haiku. Summary/Quiz/Translation/Diagram/Revision: gpt-4o → claude-3.5-sonnet. Recommendation: gpt-4o-mini → claude-3-haiku.

**Fallback**: Triggered when primary returns retryable failure (rate limit, timeout, unavailable). Invoked after primary retry budget exhausted. Single fallback per agent.

**Timeout**: Provider timeout 60s per request. Total agent invocation timeout 180s including retries. Orchestrator-level timeout 300s.

## Model Management Strategy

**Model Registry**: Centralized configuration mapping agent types to model configs (primary ID, fallback ID, capabilities, cost tier).

**Model Versioning**: Model IDs include version/date suffix from OpenRouter (e.g., openai/gpt-4o-2024-11-20). Updated explicitly through configuration changes.

**Fallback Models**: Each agent has exactly one fallback in a different provider family to reduce correlated failures.

**Cost Considerations**: High-cost models reserved for deep reasoning agents. Low-cost for routing/classification. Cost tracking via Langfuse. Monthly budget alert at OpenRouter dashboard.

**Upgrades**: Performed by updating model registry configuration. Fallback tested as primary in staging first. Registry supports model aliases for reassignment without code changes.

## Orchestrator Specification

**Responsibilities**: Request routing, dependency resolution, context passing (document/node IDs, retrieved chunks, previous agent outputs, trace ID), retry handling, state management (AgentRun records), response aggregation, error handling, logging.

**Constraints**: Only component that may invoke AI agents. Agents never call other agents directly. Orchestrator is stateless between invocations (state in PostgreSQL AgentRun records).

## Agent Contract Specification

**Request Envelope**: document_id (UUID), node_ids (UUID[]), agent_params ({key: any}), context (chunks with chunk_id/text/score/metadata, source_doc_id, previous_agent_output), trace_id (string).

**Response Envelope**: status (success|error|partial), output ({key: any}), source_refs (chunk_id/document_id/node_id[]), usage (prompt_tokens/completion_tokens/total_tokens), error (code/message/retryable or null).

**Validation**: UUID formats, non-empty node_ids, valid status enum, usage always present, error null on success.

**Schema Evolution**: Backward-compatible changes allowed anytime. Breaking changes require ADR, backward compat for one release cycle, envelope_version field.

## Echo Agent Specification

**Responsibilities**: Receive Request Envelope, validate contract, echo document_id/node_ids/trace_id in response output, return valid Response Envelope with simulated token usage.

**Limitations**: No educational content, no external services, no ChromaDB/LlamaIndex interaction. Not suitable for production beyond infrastructure validation.

**Expected Behavior**: Invalid envelope → status "error" with INVALID_REQUEST. Valid envelope → status "success" with echoed identifiers and dummy usage (50/20/70 tokens). Processing under 100ms (pure validation) or under 5s (real model call). Idempotent.

## AgentRun Specification

**Fields**: id, orchestration_id, agent_type, document_id, node_ids, trace_id, request_envelope, response_envelope, status (enum), retry_count, max_retries, errors[], started_at, completed_at, duration_ms, model_used, fallback_used, created_at, updated_at.

**Separation**: AgentRun stores execution history in PostgreSQL. Generated outputs stored in domain tables linked via document_id and trace_id.

## State Machine Specification

**queued**: Awaiting dispatch. Valid → running. Invalid → succeeded/failed/cancelled. No retry.

**running**: Agent executing. Valid → succeeded/failed/cancelled. Invalid → queued. Retry increments retry_count, status stays running.

**succeeded**: Terminal. Completed successfully. No transitions out.

**failed**: Terminal. All retries exhausted or non-retryable error. No transitions out.

**cancelled**: Terminal. External cancellation signal. No transitions out.

## Retry Strategy

**Limits**: 3 retries primary, then 3 fallback = 6 total. **Backoff**: 1s base, 2x multiplier, ±25% jitter, 30s cap. **Retryable**: 429, 502, 503, timeout, OpenRouter upstream failure, token limit exceeded. **Non-retryable**: 401, 403, 404, invalid contract, content policy violation, cancellation. **Timeout**: Provider 60s, invocation 180s, workflow 300s. **Cancellation**: Immediate terminal transition.

## LlamaIndex Architecture

**Indexing**: Document ingestion → chunk embedding → vector index in ChromaDB. Indexing lifecycle: pending → indexing → indexed → failed → reindexing.

**Retrieval**: Query embedding → ChromaDB similarity search (cosine, top-10, min 0.5 threshold) → result post-processing → context assembly into Request Envelope.

**Metadata per chunk**: chunk_id, document_id, node_id, chunk_index, title, format.

## ChromaDB Architecture

**Collections**: doc_{document_id} per-document, kb_{subject_area} for knowledge-base, all_documents for cross-document search.

**Persistence**: Persistent mode on disk. Embedding model shared between indexing and retrieval.

**Scalability**: Single-node initially, client/server mode for horizontal scaling.

## Langfuse Architecture

**Trace Hierarchy**: Orchestration trace → preparation span (context retrieval) → agent invoke span (model call observations) → response assembly span → orchestration complete event.

**Data**: Trace ID, total latency, model info, token usage, execution status, error details, retry count.

**Failure Handling**: Langfuse unreachable → AI request proceeds normally. Observability never blocks operations.

## MCP Integration Specification

**Google Drive**: Read-only, OAuth 2.0, tools: read_drive_file, list_drive_files.
**Notion**: Read-only, Notion API token, tools: read_notion_page, query_notion_database.
**Tavily**: Search only, API key, tools: web_search.
**Excalidraw**: Write-only (create diagrams), no auth, tools: create_excalidraw_diagram.
**GitHub MCP**: Remains development tooling. NOT in user-facing product. Decision documented in architecture docs.

## Configuration Requirements

Environment variables documented for: OpenRouter, OpenAI Agents SDK, Langfuse, ChromaDB, LlamaIndex, PostgreSQL, MCP servers, agent configuration, logging.

## Security Requirements

API keys in environment variables only, never in code or logs. Langfuse traces exclude PII and educational content. MCP credentials scoped to minimum required access. All external communication over HTTPS/TLS.

## Logging Requirements

Structured JSON logs. Level: ERROR/WARN/INFO/DEBUG. Never log: API keys, secrets, tokens, passwords, authorization headers, request/response bodies, user educational content. Redaction middleware for sensitive field patterns.

## Functional Requirements

30 functional requirements across 8 categories (AI Provider, Orchestrator, Echo Agent, Agent Contracts, AgentRun, Retrieval, Tracing, MCP Integration) each with ID, description, priority, dependencies, and acceptance criteria.

## Non-Functional Requirements

27 non-functional requirements across 8 categories: Performance, Reliability, Scalability, Security, Maintainability, Extensibility, Observability, Type Safety.

## Risks

9 identified risks: OpenRouter compatibility, OpenAI Agents SDK stability, function calling support, provider availability, ChromaDB persistence, Langfuse dependency, retry loops, MCP permissions. Each with description, impact, and mitigation.

## Acceptance Criteria

9 acceptance criteria (AC-001 through AC-009) covering: Echo Agent lifecycle, AgentRun state transitions, Langfuse tracing, ChromaDB retrieval, retry strategy, timeout handling, contract validation, fallback invocation, observability failure resilience.
