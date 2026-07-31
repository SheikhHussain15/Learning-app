from agents import OpenAIProvider
from src.core import config
from src.models.agent_run import AgentType
from src.schemas.agent import ModelConfig

MODEL_REGISTRY: dict[AgentType, ModelConfig] = {
    AgentType.echo: ModelConfig(
        agent_type=AgentType.echo,
        primary_model_id="openai/gpt-4o-mini",
        fallback_model_id="anthropic/claude-3-haiku",
        capabilities=["text"],
        cost_tier="low",
    ),
    AgentType.document_processing: ModelConfig(
        agent_type=AgentType.document_processing,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "document-parsing"],
        cost_tier="high",
    ),
    AgentType.knowledge_structuring: ModelConfig(
        agent_type=AgentType.knowledge_structuring,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "structured-output"],
        cost_tier="high",
    ),
    AgentType.summary: ModelConfig(
        agent_type=AgentType.summary,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "long-context"],
        cost_tier="high",
    ),
    AgentType.explanation: ModelConfig(
        agent_type=AgentType.explanation,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "educational"],
        cost_tier="high",
    ),
    AgentType.translation: ModelConfig(
        agent_type=AgentType.translation,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "multilingual"],
        cost_tier="high",
    ),
    AgentType.diagram: ModelConfig(
        agent_type=AgentType.diagram,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "diagram"],
        cost_tier="high",
    ),
    AgentType.quiz: ModelConfig(
        agent_type=AgentType.quiz,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "structured-output"],
        cost_tier="high",
    ),
    AgentType.revision: ModelConfig(
        agent_type=AgentType.revision,
        primary_model_id="openai/gpt-4o",
        fallback_model_id="anthropic/claude-3.5-sonnet",
        capabilities=["text", "long-context"],
        cost_tier="high",
    ),
    AgentType.progress: ModelConfig(
        agent_type=AgentType.progress,
        primary_model_id="openai/gpt-4o-mini",
        fallback_model_id="anthropic/claude-3-haiku",
        capabilities=["text"],
        cost_tier="low",
    ),
    AgentType.recommendation: ModelConfig(
        agent_type=AgentType.recommendation,
        primary_model_id="openai/gpt-4o-mini",
        fallback_model_id="anthropic/claude-3-haiku",
        capabilities=["text"],
        cost_tier="low",
    ),
}


def get_model_config(agent_type: AgentType) -> ModelConfig:
    return MODEL_REGISTRY[agent_type]


def get_all_model_configs() -> list[ModelConfig]:
    return list(MODEL_REGISTRY.values())


def create_openai_provider() -> OpenAIProvider:
    return OpenAIProvider(
        api_key=config.OPENROUTER_API_KEY,
        base_url=config.OPENROUTER_BASE_URL,
    )
