# Agent Contribution Guide

## Overview

This guide explains how to add a new AI agent to the platform without understanding Orchestrator internals.

## Steps

### 1. Define Contract

Create your agent's request/response schemas in `src/schemas/agent.py` (or a new file):

```python
from pydantic import BaseModel, Field

class MyAgentRequest(BaseModel):
    document_id: str
    content: str
    options: dict = Field(default_factory=dict)

class MyAgentResponse(BaseModel):
    result: str
    metadata: dict = Field(default_factory=dict)
```

### 2. Implement Agent

Create `src/agents/my_agent.py`:

```python
from src.agents.base import BaseAgent
from src.schemas.agent import RequestEnvelope, ResponseEnvelope, TokenUsage

class MyAgent(BaseAgent):
    agent_type: str = "my_agent"

    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        # Validate input
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        # Implement your agent logic here
        result = await self.process(envelope)

        return ResponseEnvelope(
            status="success",
            output={"result": result},
            source_refs=[],
            usage=TokenUsage(
                prompt_tokens=100,
                completion_tokens=50,
                total_tokens=150,
            ),
        )

    async def process(self, envelope: RequestEnvelope) -> str:
        # Your processing logic
        return "processed"
```

### 3. Register Agent

Add to `src/agents/registry.py`:

```python
from src.models.agent_run import AgentType
from src.schemas.agent import ModelConfig

# Add to MODEL_REGISTRY
AgentType.my_agent: ModelConfig(
    agent_type=AgentType.my_agent,
    primary_model_id="openai/gpt-4o",
    fallback_model_id="anthropic/claude-3.5-sonnet",
    capabilities=["text"],
    cost_tier="high",
),
```

### 4. Write Tests

Create `tests/agents/test_my_agent.py`:

```python
import pytest
from src.agents.my_agent import MyAgent
from src.schemas.agent import RequestEnvelope

@pytest.mark.asyncio
async def test_my_agent_invoke(mock_langfuse):
    agent = MyAgent()
    envelope = RequestEnvelope(
        document_id="doc-1",
        node_ids=["node-1"],
        trace_id="trace-1",
    )
    result = await agent.invoke(envelope)
    assert result.status == "success"
```

### 5. Update Documentation

Create `docs/agents/my_agent.md` with:
- Agent purpose and capabilities
- Input/output schema reference
- Example usage
- Error handling behavior
- Performance characteristics

## Contract Requirements

Every agent MUST:
- Extend `BaseAgent`
- Set `agent_type` class attribute
- Implement `invoke(RequestEnvelope) -> ResponseEnvelope`
- Validate input using `validate_envelope()`
- Return proper `TokenUsage` in response
- Handle errors gracefully

## Testing Requirements

- Unit tests for agent logic (>90% coverage)
- Contract tests for schema validation
- Integration test with Orchestrator (if applicable)

## Submission

1. Create feature branch
2. Implement agent following steps above
3. Add tests
4. Update documentation
5. Submit PR with agent-specific checklist
