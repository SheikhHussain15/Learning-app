# Data Model: AI Infrastructure — Phase 3

## Entity: AgentRun

Represents the execution history of a single agent invocation. Stored in PostgreSQL. Separated from generated AI outputs.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID (PK) | Yes | Auto | Unique identifier |
| orchestration_id | UUID (FK) | No | null | Groups multi-agent workflows |
| agent_type | Enum(AgentType) | Yes | — | Which agent was invoked |
| document_id | UUID | No | null | Source document identifier |
| node_ids | UUID[] | No | [] | Knowledge graph node identifiers |
| trace_id | String | Yes | — | Langfuse trace ID for linkage |
| request_envelope | JSON | Yes | — | Full request for audit |
| response_envelope | JSON | No | null | Full response (null if incomplete) |
| status | Enum(AgentStatus) | Yes | queued | Current execution state |
| retry_count | Integer | Yes | 0 | Current retry attempt |
| max_retries | Integer | Yes | 6 | Maximum allowed retries |
| errors | JSON[] | No | [] | Accumulated errors across attempts |
| started_at | DateTime | No | null | When execution began |
| completed_at | DateTime | No | null | When execution ended |
| duration_ms | Integer | No | null | completed_at - started_at in ms |
| model_used | String | No | null | Actual model ID that handled request |
| fallback_used | Boolean | Yes | false | Whether fallback model was used |
| created_at | DateTime | Yes | now() | Record creation timestamp |
| updated_at | DateTime | Yes | now() | Last update timestamp |

### Validation Rules

- `status` transitions must follow the state machine (see plan.md or spec.md).
- `duration_ms` is null until status reaches a terminal state.
- `errors` array entries must contain: `attempt` (int), `code` (string), `message` (string), `timestamp` (datetime).
- `request_envelope` must validate against the RequestEnvelope schema.

### Indexes

- Primary: `id`
- Query: `(agent_type, status)` for monitoring queries
- Query: `(orchestration_id)` for multi-agent workflow grouping
- Query: `(trace_id)` for Langfuse linkage lookups
- Query: `(created_at)` for time-based queries

## Enum: AgentType

| Value | Description |
|-------|-------------|
| echo | Echo (placeholder) agent for infrastructure validation |
| summary | Summary agent (Phase 4) |
| quiz | Quiz generation agent (Phase 4) |
| translation | Translation agent (Phase 4) |
| diagram | Diagram generation agent (Phase 4) |
| revision | Revision content agent (Phase 4) |
| recommendation | Recommendation agent (Phase 4) |

## Enum: AgentStatus

| Value | Description |
|-------|-------------|
| queued | Awaiting dispatch by Orchestrator |
| running | Agent actively executing |
| succeeded | Completed successfully (terminal) |
| failed | All retries exhausted or non-retryable error (terminal) |
| cancelled | Cancelled by external signal (terminal) |

### Valid Transitions

```
queued → running
running → succeeded
running → failed
running → cancelled
```

All other transitions are invalid and must be rejected.

## Schema: RequestEnvelope (Pydantic)

```python
class RequestEnvelope(BaseModel):
    document_id: UUID
    node_ids: list[UUID]
    agent_params: dict[str, Any] = Field(default_factory=dict)
    context: RequestContext | None = None
    trace_id: str

class RequestContext(BaseModel):
    chunks: list[RetrievedChunk] = Field(default_factory=list)
    source_doc_id: UUID | None = None
    previous_agent_output: dict[str, Any] | None = None

class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    score: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)
```

## Schema: ResponseEnvelope (Pydantic)

```python
class ResponseEnvelope(BaseModel):
    status: Literal["success", "error", "partial"]
    output: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[SourceRef] = Field(default_factory=list)
    usage: TokenUsage
    error: ErrorInfo | None = None

class SourceRef(BaseModel):
    chunk_id: str
    document_id: UUID
    node_id: UUID | None = None

class TokenUsage(BaseModel):
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)

class ErrorInfo(BaseModel):
    code: str
    message: str
    retryable: bool
```

## Schema: ModelConfig

```python
class ModelConfig(BaseModel):
    agent_type: AgentType
    primary_model_id: str
    fallback_model_id: str
    capabilities: list[str] = Field(default_factory=list)
    cost_tier: Literal["low", "medium", "high"]
```

## Schema: AgentRunCreate (API input)

```python
class AgentRunCreate(BaseModel):
    agent_type: AgentType
    document_id: UUID | None = None
    node_ids: list[UUID] = Field(default_factory=list)
    agent_params: dict[str, Any] = Field(default_factory=dict)
    context: RequestContext | None = None
```

## Schema: AgentRunResponse (API output)

```python
class AgentRunResponse(BaseModel):
    id: UUID
    status: AgentStatus
    agent_type: AgentType
    response_envelope: ResponseEnvelope | None = None
    error: ErrorInfo | None = None
    duration_ms: int | None = None
    created_at: datetime
    completed_at: datetime | None = None
```
