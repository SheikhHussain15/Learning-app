from src.agents.base import BaseAgent
from src.agents.diagram import DiagramAgent
from src.agents.document_processing import DocumentProcessingAgent
from src.agents.echo_agent import EchoAgent
from src.agents.explanation import ExplanationAgent
from src.agents.knowledge_structuring import KnowledgeStructuringAgent
from src.agents.progress import ProgressAgent
from src.agents.quiz import QuizAgent
from src.agents.recommendation import RecommendationAgent
from src.agents.registry import get_model_config
from src.agents.revision import RevisionAgent
from src.agents.summary import SummaryAgent
from src.agents.translation import TranslationAgent
from src.models.agent_run import AgentType

_agent_registry: dict[AgentType, BaseAgent] = {}


def register_agent(agent_type: AgentType, agent: BaseAgent) -> None:
    _agent_registry[agent_type] = agent


def get_agent(agent_type: AgentType) -> BaseAgent | None:
    return _agent_registry.get(agent_type)


def resolve_dependencies(agent_type: AgentType) -> dict:
    model_config = get_model_config(agent_type)
    return {
        "primary_model_id": model_config.primary_model_id,
        "fallback_model_id": model_config.fallback_model_id,
        "capabilities": model_config.capabilities,
    }


def _init_default_agents() -> None:
    if AgentType.echo not in _agent_registry:
        register_agent(AgentType.echo, EchoAgent())
    if AgentType.document_processing not in _agent_registry:
        register_agent(AgentType.document_processing, DocumentProcessingAgent())
    if AgentType.knowledge_structuring not in _agent_registry:
        register_agent(AgentType.knowledge_structuring, KnowledgeStructuringAgent())
    if AgentType.summary not in _agent_registry:
        register_agent(AgentType.summary, SummaryAgent())
    if AgentType.explanation not in _agent_registry:
        register_agent(AgentType.explanation, ExplanationAgent())
    if AgentType.translation not in _agent_registry:
        register_agent(AgentType.translation, TranslationAgent())
    if AgentType.diagram not in _agent_registry:
        register_agent(AgentType.diagram, DiagramAgent())
    if AgentType.quiz not in _agent_registry:
        register_agent(AgentType.quiz, QuizAgent())
    if AgentType.revision not in _agent_registry:
        register_agent(AgentType.revision, RevisionAgent())
    if AgentType.progress not in _agent_registry:
        register_agent(AgentType.progress, ProgressAgent())
    if AgentType.recommendation not in _agent_registry:
        register_agent(AgentType.recommendation, RecommendationAgent())
