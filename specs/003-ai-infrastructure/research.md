# Research: AI Infrastructure — Phase 3

## Research Tasks

### 1. OpenRouter API Compatibility with OpenAI Agents SDK

- **Decision**: Use OpenAI Agents SDK `OpenAIProvider` with custom base URL pointing to OpenRouter.
- **Rationale**: OpenRouter explicitly maintains OpenAI API compatibility. The SDK's `OpenAIProvider` accepts a `base_url` parameter that overrides the default OpenAI endpoint. All OpenAI SDK features (function calling, streaming, tool execution) work through OpenRouter as long as the chosen model supports them.
- **Alternatives Considered**: Direct provider SDKs (OpenAI, Anthropic, Google) — rejected because they would require per-provider integration and eliminate OpenRouter's fallback/abstraction benefits. Custom HTTP client — rejected because it would duplicate the SDK's agent lifecycle and tool execution features.
- **Key Finding**: Set `base_url="https://openrouter.ai/api/v1"` and pass OpenRouter API key as the OpenAI API key. Set `HTTP-Referer` and `X-Title` headers via default_headers in the provider constructor for OpenRouter ranking/analytics.

### 2. ChromaDB Persistent Mode Configuration

- **Decision**: Use ChromaDB persistent client with local disk storage.
- **Rationale**: ChromaDB's `PersistentClient` stores data on disk and survives process restarts. The persistence directory is configurable. In-memory mode is suitable for testing but not production.
- **Alternatives Considered**: ChromaDB HTTP client (client/server mode) — deferred to Phase 4 when horizontal scaling is needed. Qdrant, Pinecone — rejected for Phase 3 due to additional setup complexity; ChromaDB is the simplest self-hosted vector DB.
- **Key Finding**: `chromadb.PersistentClient(path="./data/chromadb")` creates/starts a persistent instance. ChromaDB handles its own internal serialization. Database metadata (hnsw:space, etc.) configures similarity search behavior.

### 3. Langfuse Python SDK Trace Hierarchy

- **Decision**: Use Langfuse `@observe()` decorator for automatic tracing, with manual `get_trace_client()` for creating hierarchical spans.
- **Rationale**: Langfuse Python SDK supports decorator-based auto-tracing and manual span creation. The hierarchical trace structure (Orchestrator root → Agent child → Model call observations) maps directly to Langfuse's `trace()` → `span()` → `generation()` hierarchy.
- **Alternatives Considered**: Langfuse callback for LangChain — not applicable since we're using OpenAI Agents SDK, not LangChain. Custom logging → rejected because it lacks trace visualization and cost tracking.
- **Key Finding**: Create root trace in Orchestrator with `langfuse.trace(name="orchestration", id=trace_id)`. Create child spans for each agent invocation with `trace.span(name="agent.invoke")`. Use `span.generation()` to log model calls with token counts. Set `LANGFUSE_RELEASE` environment variable for deployment tracking.

### 4. LlamaIndex ChromaDB Vector Store Integration

- **Decision**: Use `llama_index.vector_stores.chroma.ChromaVectorStore` wrapper around ChromaDB.
- **Rationale**: LlamaIndex provides first-class ChromaDB integration via `ChromaVectorStore`. This wraps the ChromaDB collection and exposes it through LlamaIndex's standard `VectorStoreIndex` interface. Embedding model is configured on the LlamaIndex `Settings` object.
- **Alternatives Considered**: Direct ChromaDB queries without LlamaIndex — rejected because LlamaIndex provides query transformation, result post-processing, and reranking capabilities out of the box.
- **Key Finding**: Configure: `vector_store = ChromaVectorStore(chroma_collection=collection)`, then `index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)`. For retrieval: `index.as_query_engine(similarity_top_k=10)`. The `similarity_cutoff` parameter enforces the minimum similarity threshold.

### 5. OpenAI Agents SDK MCP Tool Registration

- **Decision**: Register MCP servers as `FunctionTool` instances on the OpenAI Agent.
- **Rationale**: OpenAI Agents SDK treats tools as `FunctionTool` objects. Each MCP server's toolkit is converted into one or more `FunctionTool` instances with name, description, and parameter schema. The agent receives these tools in its constructor.
- **Alternatives Considered**: Custom MCP protocol handler — rejected because the SDK's tool system already supports arbitrary function-based tools. Direct function integration — rejected for MCP-specific functionality because MCP provides standard protocol semantics.
- **Key Finding**: Each MCP tool follows this pattern: `FunctionTool(name="tool_name", description="...", params_json_schema={...}, fn=async_handler)`. The Echo Agent needs no MCP tools. Future agents will selectively register MCP tools based on their domain.

### 6. Exponential Backoff Implementation Patterns

- **Decision**: Use `tenacity` library with custom retry strategy.
- **Rationale**: `tenacity` provides battle-tested retry/backoff primitives: `@retry(stop=stop_after_attempt(6), wait=wait_exponential(multiplier=1, min=1, max=30), retry=retry_if_exception_type(RetryableError))`. Custom jitter added via `wait=wait_exponential(...) + wait_random(0, 0.25*calculated_delay)`.
- **Alternatives Considered**: Manual retry loop — rejected because it duplicates tenacity's robust implementations. `backoff` library — less actively maintained than tenacity.
- **Key Finding**: Retryable errors are raised as `RetryableError` exceptions. Non-retryable errors raise `NonRetryableError`. The Orchestrator wraps each agent invocation in a tenacity-retried function. The `before_sleep` callback logs each retry attempt with backoff delay. Fallback model switch occurs after 3 consecutive `RetryableError` on primary model.

## Technology Stack Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| AI Provider Gateway | OpenRouter | Unified API, fallback, cost tracking |
| AI Agent Runtime | OpenAI Agents SDK | Function calling, tool execution, streaming |
| Orchestrator | Custom FastAPI service | Full control, stateless, typed |
| Agent Contract | Pydantic v2 schemas | Type safety, validation, serialization |
| Vector DB | ChromaDB (persistent) | Self-hosted, simple setup, LlamaIndex-compatible |
| Retrieval Orchestration | LlamaIndex | Query transformation, reranking, structured retrieval |
| Observability | Langfuse | Trace hierarchy, cost tracking, LLM-specific |
| Retry Library | tenacity | Mature, composable retry/backoff/wait strategies |
| MCP Protocol | OpenAI Agents SDK FunctionTool | Standard tool registration, no custom protocol |
| Database | PostgreSQL (existing) | AgentRun persistence, separation from ChromaDB |

## Integration Patterns

- **OpenRouter + SDK**: Provider config with `base_url`, `api_key`, `default_headers`. Per-agent model binding from registry.
- **ChromaDB + LlamaIndex**: `ChromaVectorStore` wrapper around persistent ChromaDB collection. LlamaIndex `VectorStoreIndex` for querying.
- **Langfuse Tracing**: Decorator-based for automatic traces, manual spans for orchestration-specific events. `trace_id` shared between Request Envelope and Langfuse trace for observability linkage.
- **MCP + Agents**: MCP server → FunctionTool conversion → Agent tool registration. One tool per MCP operation. Credentials from environment variables.
- **Orchestrator + AgentRun**: Each invocation creates AgentRun in PostgreSQL via SQLAlchemy. State transitions update the record. Errors accumulate in `errors` JSON array.
