---
name: ai-agent-orchestration
= ai-agent-orchestration
---

# AI Agent Orchestration Skill

This skill guides the implementation of the AI Agent Orchestration system that coordinates and manages multiple specialized AI agents through a centralized, production-ready architecture. The Orchestrator acts as the single entry point for all AI agent interactions, providing dependency resolution, context management, incremental processing, and comprehensive observability.

## Procedure

### 1. Design Orchestrator Architecture
- Create `app/backend/src/core/orchestrator.py`
- Define Orchestrator class with configuration options:
  - Agent registry for all available agents
  - Dependency graph for processing order resolution
  - Context management system for state passing
  - Retry and timeout configuration
  - Cache management for incremental processing
- Implement agent selector based on dependencies and requirements

### 2. Implement Agent Registry
- Create `app/backend/src/registry/agents.py`
- Define agent metadata including:
  - Agent type and capabilities
  - Input/output contract definitions
  - Default configuration parameters
  - Dependency requirements (other agents needed)
  - Execution priority and constraints
- Register all ten agents: Document Processing, Knowledge Structuring, Summary, Explanation, Translation, Diagram, Quiz, Revision, Progress, and Recommendation

### 3. Build Dependency Resolution Engine
- Create `app/backend/src/core/dependency_engine.py`
- Implement topological sorting for agent execution order
- Handle cycle detection and resolution
- Support optional vs. mandatory dependencies
- Cache resolved dependency graphs for repeated requests
- Validate dependency constraints dynamically

### 4. Implement Context Management System
- Create `app/backend/src/core/context_manager.py`
- Design context objects for passing between agents:
  - Document context: document_id, chunks, metadata
  - Processing context: previous agent outputs, trace IDs
  - Session context: user_id, preferences, permissions
- Implement context serialization and caching
- Support context validation and sanitization

### 5. Develop Incremental Processing Engine
- Create `app/backend/src/core/incremental_processor.py`
- Implement output caching with key based on agent + inputs
- Provide dependency validation before skip decisions
- Support partial re-processing for modified requirements
- Implement cache invalidation strategies
- Monitor cache effectiveness and performance

### 6. Create Agent Execution Engine
- Build `app/backend/src/core/agent_executor.py`
- Implement agent request preparation and envelope creation
- Add retry logic with exponential backoff
- Implement timeout handling with configurable limits
- Provide comprehensive error classification (retryable vs. non-retryable)
- Support parallel execution for independent agents

### 7. Establish Output Validation System
- Create `app/backend/src/core/output_validator.py`
- Implement contract validation for all agent outputs:
  - Schema validation using Pydantic
  - Source reference extraction and validation
  - Metadata completeness checks
  - Traceability verification
- Provide detailed error reporting for validation failures

### 8. Implement Orchestrator API Interface
- Create `app/backend/src/api/v1/orchestrator.py`
- Define FastAPI endpoints for orchestration control:
  - POST `/api/v1/orchestrator/process` - Start agent processing
  - GET `/api/v1/orchestrator/status/{orchestration_id}` - Get status
  - POST `/api/v1/orchestrator/cancel/{orchestration_id}` - Cancel processing
  - GET `/api/v1/orchestrator/agents` - List available agents
  - POST `/api/v1/orchestrator/agent-run` - Create standalone agent run
- Implement rate limiting and authentication
- Provide WebSocket support for real-time progress updates

### 9. Add Monitoring and Observability
- Create `app/backend/src/core/monitoring.py`
- Implement Langfuse integration for trace collection:
  - Orchestration trace spans
  - Agent execution spans
  - Performance metrics collection
  - Error tracking and alerting
- Add Prometheus metrics for monitoring
- Implement structured logging with correlation IDs

### 10. Configure Agent Contracts and Templates
- Create `app/backend/src/contracts/agent_envelope.py`
- Define Request Envelope schema:
  - document_id, node_ids, agent_params
  - context (chunks, previous outputs)
  - trace_id for observability
- Define Response Envelope schema:
  - status, output, source_refs
  - usage metrics, error information
- Implement contract validation and schema evolution

### 11. Set Up Database Integration
- Create `app/backend/src/models/orchestration.py`
- Define AgentRun model for execution tracking:
  - orchestration_id, agent_type
  - document_id, node_ids, trace_id
  - status, retry_count, execution details
  - start/complete timestamps
- Create AgentOutput model for generated artifacts
- Implement connection pooling and transaction management

### 12. Configure Environment and Dependencies
- Update `app/backend/requirements.txt` with new packages:
  - `graphlib-backport` (for topological sorting, Python 3.9)
  - `prometheus-client` for metrics
  - Additional agent-specific dependencies
- Create `.env.example` with orchestration configuration:
  - ORCHESTRATOR_MAX_CONCURRENT
  - ORCHESTRATOR_TIMEOUT_MS
  - ORCHESTRATOR_CACHE_TTL
  - AGENT_RETRY_CONFIG

## File Structure

```
app/backend/src/
├── core/
│   ├── orchestrator.py          # Orchestrator class (main)
│   ├── dependency_engine.py      # Dependency resolution
│   ├── context_manager.py       # Context passing
│   ├── incremental_processor.py # Cache and incremental processing
│   ├── agent_executor.py        # Agent execution and retry logic
│   └── output_validator.py      # Output validation
├── registry/
│   └── agents.py               # Agent registry definitions
├── contracts/
│   └── agent_envelope.py       # Request/Response envelope schemas
├── core/
│   ├── monitoring.py            # Observability integration
│   ├── logging.py               # Structured logging
│   └── exceptions.py           # Custom exception hierarchy
├── models/
│   └── orchestration.py        # Database models
├── api/v1/
│   └── orchestrator.py        # REST API interface
└── services/
    └── agent_service.py        # Agent service abstractions

app/backend/
├── __init__.py
├── requirements.txt           # MODIFIED (new dependencies)
├── .env.example               # MODIFIED (orchestration config)
└── main.py                   # MODIFIED (import orchestrator)
```

## Agent Implementation Patterns

### 1. Agent Registration Pattern
```python
# In agents.py
AGENT_REGISTRY = {
    "document_processing": {
        "type": "document_processing",
        "dependencies": [],
        "capabilities": ["ocr", "text_extraction"],
        "config_class": DocumentProcessingConfig,
        "service_class": DocumentProcessingService,
    },
    "knowledge_structuring": {
        "type": "knowledge_structuring",
        "dependencies": ["document_processing"],
        "capabilities": ["hierarchy_generation"],
        "config_class": KnowledgeStructuringConfig,
        "service_class": KnowledgeStructuringService,
    },
    # ... other agents
}
```

### 2. Orchestrator Processing Pattern
```python
# In orchestrator.py
async def process_document_with_agents(self, document_id, agent_types=None):
    """
    Process document through selected agents using dependency resolution.
    """
    # 1. Resolve dependencies and execution order
    execution_plan = await self.dependency_engine.resolve_dependencies(
        agent_types or self.default_agent_sequence,
        document_id
    )
    
    # 2. Initialize orchestration record
    orchestration_id = await self._create_orchestration_record(document_id, execution_plan)
    
    # 3. Execute agents in order
    for agent_info in execution_plan:
        # 3.1. Build context from previous agent outputs
        context = await self.context_manager.build_context(
            orchestration_id, agent_info
        )
        
        # 3.2. Prepare agent request envelope
        request_envelope = await self._prepare_request_envelope(
            agent_info, context, orchestration_id
        )
        
        # 3.3. Execute agent with retries
        try:
            response_envelope = await self.agent_executor.execute_agent(
                agent_info["type"], request_envelope
            )
            
            # 3.4. Validate output
            await self.output_validator.validate(response_envelope)
            
            # 3.5. Cache successful output
            await self.incremental_processor.cache_output(
                agent_info["type"], request_envelope, response_envelope
            )
            
            # 3.6. Store agent run record
            await self._record_agent_run(orchestration_id, agent_info, response_envelope)
            
        except Exception as e:
            await self._handle_agent_failure(orchestration_id, agent_info, e)
            if agent_info.get("retryable", True):
                continue
            raise
    
    # 4. Return aggregated results
    return await self._aggregate_orchestration_results(orchestration_id)
```

### 3. Context Building Pattern
```python
# In context_manager.py
async def build_context(self, orchestration_id, agent_info, previous_output=None):
    """
    Build context for agent execution from orchestration state.
    """
    context = {
        "document_id": self.get_orchestration_document_id(orchestration_id),
        "node_ids": agent_info.get("node_ids", []),
        "previous_agent_output": previous_output,
        "trace_id": orchestration_id,
        "user_context": await self._get_user_context(orchestration_id),
    }
    
    # Add relevant data based on agent dependencies
    if agent_info["type"] == "knowledge_structuring":
        # Add previous document processing output
        doc_output = await self._get_last_output_for_type(orchestration_id, "document_processing")
        context["document_chunks"] = self._extract_chunks_from_output(doc_output)
    
    # Cache context for future use
    await self._cache_context(orchestration_id, agent_info["type"], context)
    
    return context
```

## Error Handling Patterns

### 1. Agent Execution Errors
```python
# In agent_executor.py
async def execute_agent(self, agent_type, request_envelope):
    """
    Execute agent with comprehensive error handling and retry logic.
    """
    max_retries = self.config.get(agent_type, {}).get("max_retries", 3)
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            # Execute with timeout
            response = await asyncio.wait_for(
                self.agent_service.call_agent(agent_type, request_envelope),
                timeout=self.config.get(agent_type, {}).get("timeout_seconds", 300)
            )
            return response
            
        except asyncio.TimeoutError:
            retry_count += 1
            if retry_count > max_retries:
                raise OrchestrationException(
                    f"Agent {agent_type} timeout after {max_retries} retries",
                    error_code="AGENT_TIMEOUT"
                )
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
            
        except AgentValidationError as e:
            # Non-retryable error - fail fast
            raise OrchestrationException(
                f"Agent {agent_type} validation failed: {str(e)}",
                error_code="AGENT_VALIDATION"
            )
            
        except AgentExecutionError as e:
            retry_count += 1
            if not e.retryable or retry_count > max_retries:
                raise OrchestrationException(
                    f"Agent {agent_type} execution failed: {str(e)}",
                    error_code="AGENT_EXECUTION"
                )
            await asyncio.sleep(2 ** retry_count)
```

### 2. Orchestration Recovery Pattern
```python
# In orchestrator.py
async def handle_agent_failure(self, orchestration_id, agent_info, error):
    """
    Handle agent failure with recovery and appropriate escalation.
    """
    # Log failure with detailed information
    await self._log_failure(orchestration_id, agent_info, error)
    
    # Determine if failure is recoverable
    if isinstance(error, AgentExecutionError) and error.retryable:
        # Update AgentRun status for retry
        await self._update_agent_run_status(
            orchestration_id,
            agent_info["type"],
            "retry_needed",
            error_details=str(error)
        )
    elif isinstance(error, AgentValidationError):
        # Non-retryable validation error
        await self._update_agent_run_status(
            orchestration_id,
            agent_info["type"],
            "validation_failed",
            error_details=str(error)
        )
        # Skip dependent agents if validation failed
        await self._skip_dependent_agents(orchestration_id, agent_info)
    else:
        # Other failures
        await self._update_agent_run_status(
            orchestration_id,
            agent_info["type"],
            "failed",
            error_details=str(error)
        )
        raise
```

## Configuration Patterns

### 1. Agent Configuration Management
```python
# In orchestrator.py

class OrchestratorConfig:
    def __init__(self):
        self.max_concurrent_agents = int(os.getenv("ORCHESTRATOR_MAX_CONCURRENT", "10"))
        self.default_timeout_ms = int(os.getenv("ORCHESTRATOR_TIMEOUT_MS", "300000"))
        self.retry_config = self._load_retry_config()
        self.cache_ttl_seconds = int(os.getenv("ORCHESTRATOR_CACHE_TTL", "3600"))
        self.enable_parallel_execution = os.getenv("ORCHESTRATOR_PARALLEL", "true").lower() == "true"
    
    def _load_retry_config(self):
        """
        Load retry configuration from environment variables.
        Format: agent_type:max_retries,agent_type:max_retries
        """
        config = {}
        env_config = os.getenv("AGENT_RETRY_CONFIG", "")
        for item in env_config.split(","):
            if ":" in item:
                agent_type, max_retries = item.split(":")
                config[agent_type] = int(max_retries)
        return config
```

## Security and Compliance

### 1. User Isolation Pattern
```python
# In orchestrator.py
async def validate_user_access(self, user_id, document_id):
    """
    Ensure user has access to document before starting orchestration.
    """
    # Check ownership
    if await self._check_document_ownership(user_id, document_id):
        return True
    
    # Check shared access permissions
    if await self._check_shared_access(user_id, document_id):
        return True
    
    # Check team/organization access
    if await self._check_team_access(user_id, document_id):
        return True
    
    raise OrchestrationException(
        f"User {user_id} does not have access to document {document_id}",
        error_code="ACCESS_DENIED"
    )
```

## Performance Optimization

### 1. Connection Pooling Pattern
```python
# In orchestrator.py
import asyncpg
from sqlalchemy import create_engine

class Orchestrator:
    def __init__(self):
        # Database connection pool
        self.db_pool = asyncpg.create_pool(
            os.getenv("DATABASE_URL"),
            min_size=5,
            max_size=20
        )
        
        # Agent connection pools
        self.agent_pools = {}
        for agent_type in self.agent_registry:
            self.agent_pools[agent_type] = asyncpg.create_pool(
                self._get_agent_connection_string(agent_type),
                min_size=2,
                max_size=5
            )
    
    async def execute_agent_with_pool(self, agent_type, request_envelope):
        """
        Execute agent using dedicated connection pool.
        """
        pool = self.agent_pools[agent_type]
        async with pool.acquire() as connection:
            return await self._call_agent_on_connection(
                connection, agent_type, request_envelope
            )
```

## Dependencies

Required packages in `app/backend/requirements.txt`:
```
fastapi>=2.0.0  # Web framework
python-multipart>=0.5.0  # File upload handling
uvicorn>=0.23.0  # ASGI server
asyncpg>=0.29.0  # PostgreSQL driver
python-jose[cryptography]>=3.3.0  # JWT handling for auth
python-dotenv>=1.0.0  # Environment variables
asyncio-throttle>=1.0.0  # Rate limiting
apached-airflow>=2.7.0  # Workflow management
redis>=4.5.0  # Cache backend
opentelemetry-api>=1.20.0  # Observability
opentelemetry-sdk>=1.20.0  # Observability SDK
opentelemetry-instrumentation-fastapi>=0.41b0  # FastAPI instrumentation
opentelemetry-instrumentation-dbapi>=0.41b0  # Database instrumentation
opentelemetry-instrumentation-requests>=0.41b0  # HTTP client instrumentation
```

## Configuration

### Environment Variables
```bash
# Orchestrator Configuration
ORCHESTRATOR_MAX_CONCURRENT=10
ORCHESTRATOR_TIMEOUT_MS=300000
ORCHESTRATOR_CACHE_TTL=3600
ORCHESTRATOR_PARALLEL=true
ORCHESTRATOR_ENABLE_OBSERVABILITY=true

# Agent Retry Configuration
AGENT_RETRY_CONFIG=document_processing:3,summary:2,quiz:4

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/learning_app

# Agent Service Configuration
AGENT_DOCUMENT_PROCESSING_URL=http://localhost:8001
AGENT_SUMMARY_URL=http://localhost:8002
AGENT_QUIZ_URL=http://localhost:8003

# Authentication
AUTH_JWT_SECRET=your-jwt-secret
AUTH_JWT_ALGORITHM=HS256

# Observability
LANGFUSE_PUBLIC_KEY=your-langfuse-key
LANGFUSE_SECRET_KEY=your-langfuse-secret
LANGFUSE_HOST=https://cloud.langfuse.com

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0

# Monitoring
PROMETHEUS_METRICS_PORT=8000
```

## Integration with Other Components

### 1. Document Processing Integration
```python
# In orchestrator.py

async def process_document_pipeline(self, document_id, user_id):
    """
    Complete pipeline orchestration from document upload to final outputs.
    """
    # 1. Validate user access
    await self.validate_user_access(user_id, document_id)
    
    # 2. Initialize orchestration with all mandatory agents
    await self._initialize_orchestration(
        document_id,
        user_id,
        ["document_processing", "knowledge_structuring", "summary", "quiz"]
    )
    
    # 3. Execute pipeline through Orchestrator
    results = await self.process_document_with_agents(document_id)
    
    # 4. Create AgentRun records for observability
    await self._create_agent_run_records(document_id, results)
    
    return results
```

## Testing Strategy

### 1. Unit Tests
```python
# tests/unit/test_dependency_engine.py
import pytest
from app.backend.src.core.dependency_engine import DependencyEngine

@pytest.mark.asyncio
async def test_dependency_resolution():
    """Test topological sorting of agent dependencies."""
    engine = DependencyEngine()
    
    # Define agent dependencies
    agents = [
        {"type": "document_processing", "dependencies": []},
        {"type": "knowledge_structuring", "dependencies": ["document_processing"]},
        {"type": "summary", "dependencies": ["knowledge_structuring"]},
        {"type": "quiz", "dependencies": ["summary"]},
    ]
    
    result = await engine.resolve_dependencies(agents)
    
    # Verify execution order respects dependencies
    assert result[0]["type"] == "document_processing"
    assert result[1]["type"] == "knowledge_structuring"
    assert result[2]["type"] == "summary"
    assert result[3]["type"] == "quiz"

@pytest.mark.asyncio
async def test_incremental_processing_skip():
    """Test that previously completed agents are skipped."""
    processor = IncrementalProcessor()
    
    # Simulate previous agent execution
    await processor.cache_output("document_processing", {"doc_id": "1"}, {"status": "success"})
    
    # Request processing again
    result = await processor.get_cached_output("document_processing", {"doc_id": "1"})
    
    # Should return cached result, not re-execute
    assert result["status"] == "success"
    assert "cache_hit" in result
```

### 2. Integration Tests
```python
# tests/integration/test_orchestrator_full_flow.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_complete_document_processing_flow():
    """Test complete flow from document upload to quiz generation."""
    client = TestClient(app)
    
    # 1. Create test document
    with open("test_document.pdf", "rb") as f:
        upload_response = client.post(
            "/api/v1/document/upload",
            files={"file": ("test.pdf", f, "application/pdf")},
            headers={"X-User-ID": "test_user_123"}
        )
    
    assert upload_response.status_code == 200
    document_id = upload_response.json()["document_id"]
    
    # 2. Start orchestration through Orchestrator API
    start_response = client.post(
        "/api/v1/orchestrator/process",
        json={
            "document_id": document_id,
            "agent_types": ["document_processing", "knowledge_structuring", "summary", "quiz"],
            "user_id": "test_user_123"
        }
    )
    
    assert start_response.status_code == 202
    orchestration_id = start_response.json()["orchestration_id"]
    
    # 3. Poll for completion
    import time
    max_wait = 60  # seconds
    poll_interval = 1
    waited = 0
    
    while waited < max_wait:
        status_response = client.get(f"/api/v1/orchestrator/status/{orchestration_id}")
        assert status_response.status_code == 200
        
        if status_response.json()["status"] == "completed":
            results = status_response.json()["results"]
            
            # 4. Verify all expected outputs exist
            assert "document_processing" in results
            assert "knowledge_structuring" in results
            assert "summary" in results
            assert "quiz" in results
            
            # 5. Verify outputs validate contracts
            for agent_type, output in results.items():
                assert "source_refs" in output
                assert "trace_id" in output
            
            # 6. Verify source references are valid
            quiz_agent_output = results["quiz"]
            assert quiz_agent_output["output"]["questions"]
            
            return
        elif status_response.json()["status"] == "failed":
            error_details = status_response.json().get("error_details", "Unknown error")
            pytest.fail(f"Orchestration failed: {error_details}")
        
        await asyncio.sleep(poll_interval)
        waited += poll_interval
    
    pytest.fail(f"Orchestration timed out after {max_wait} seconds")
```

## Performance Benchmarks

### 1. Throughput Test
```python
# Integration test for performance benchmarking
@pytest.mark.asyncio
async def test_orchestrator_throughput():
    """Test orchestrator can handle high throughput."""
    client = TestClient(app)
    
    # Create 10 test documents
    document_ids = []
    for i in range(10):
        with open(f"test_doc_{i}.pdf", "wb") as f:
            f.write(f"Test document {i}".encode())
        
        with open(f"test_doc_{i}.pdf", "rb") as f:
            response = client.post(
                "/api/v1/document/upload",
                files={"file": (f"doc_{i}.pdf", f, "application/pdf")},
                headers={"X-User-ID": "test_user"}
            )
            assert response.status_code == 200
            document_ids.append(response.json()["document_id"])
    
    # Start parallel orchestration for all documents
    import time
    start_time = time.time()
    
    orchestration_tasks = []
    for doc_id in document_ids:
        task = asyncio.create_task(client.post(
            "/api/v1/orchestrator/process",
            json={
                "document_id": doc_id,
                "agent_types": ["document_processing", "knowledge_structuring", "summary"],
                "user_id": "test_user"
            }
        ))
        orchestration_tasks.append(task)
    
    # Wait for all orchestrations to complete
    responses = await asyncio.gather(*orchestration_tasks)
    
    total_time = time.time() - start_time
    documents_per_minute = (len(document_ids) / total_time) * 60
    
    # Verify throughput meets SLA
    assert documents_per_minute >= 2, \
        f"Throughput too low: {documents_per_minute:.2f} docs/min"
```

## Monitoring and Observability

### 1. Metrics Collection
```python
# In monitoring.py
from prometheus_client import Counter, Histogram, Gauge

class OrchestratorMetrics:
    def __init__(self):
        # Request counters
        self.orchestration_requests = Counter(
            'orchestrator_requests_total',
            'Total orchestration requests',
            ['agent_type', 'status']
        )
        
        # Request latency
        self.orchestration_latency = Histogram(
            'orchestrator_request_duration_seconds',
            'Orchestration request latency'
        )
        
        # Cache hit rate
        self.cache_hits = Counter(
            'orchestrator_cache_hits_total',
            'Total cache hits'
        )
        self.cache_misses = Counter(
            'orchestrator_cache_misses_total',
            'Total cache misses'
        )
        
        # Active executions
        self.active_orchestrations = Gauge(
            'orchestrator_active_executions',
            'Number of active orchestrations'
        )
        
        # Agent execution counters
        self.agent_executions = Counter(
            'agent_executions_total',
            'Total agent executions',
            ['agent_type', 'status']
        )
    
    def record_orchestration(self, agent_type, status, duration):
        """Record orchestration metrics."""
        self.orchestration_requests.labels(
            agent_type=agent_type,
            status=status
        ).inc()
        self.orchestration_latency.observe(duration)
        
        if status == "completed":
            self.agent_executions.labels(
                agent_type=agent_type,
                status="success"
            ).inc()
```

### 2. Langfuse Trace Integration
```python
# In orchestrator.py

async def create_orchestration_trace(self, document_id, user_id):
    """
    Create Langfuse trace for orchestration with proper hierarchy.
    """
    import os
    from langfuse import Langfuse
    
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    )
    
    # Create main orchestration trace
    trace = langfuse.trace(
        id=f"orchestration_{document_id}",
        name="Document Processing Orchestration",
        input={"document_id": document_id, "user_id": user_id},
        metadata={
            "document_id": document_id,
            "user_id": user_id,
            "orchestration_type": "ai_agent_orchestration"
        }
    )
    
    # Create preparation span
    preparation_span = trace.span(
        name="orchestrator_preparation",
        input={"document_id": document_id, "requested_agents": self._get_requested_agents()}
    )
    
    # Create output span for each agent
    self._create_agent_output_spans(trace, document_id)
    
    return trace
```