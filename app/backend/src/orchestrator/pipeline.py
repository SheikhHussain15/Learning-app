import logging
from dataclasses import dataclass, field

from src.models.agent_run import AgentType

logger = logging.getLogger(__name__)


@dataclass
class AgentDependency:
    agent_type: AgentType
    depends_on: list[AgentType] = field(default_factory=list)


DEPENDENCY_GRAPH: dict[AgentType, AgentDependency] = {
    AgentType.document_processing: AgentDependency(
        agent_type=AgentType.document_processing,
        depends_on=[],
    ),
    AgentType.knowledge_structuring: AgentDependency(
        agent_type=AgentType.knowledge_structuring,
        depends_on=[AgentType.document_processing],
    ),
    AgentType.summary: AgentDependency(
        agent_type=AgentType.summary,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.explanation: AgentDependency(
        agent_type=AgentType.explanation,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.translation: AgentDependency(
        agent_type=AgentType.translation,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.diagram: AgentDependency(
        agent_type=AgentType.diagram,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.quiz: AgentDependency(
        agent_type=AgentType.quiz,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.revision: AgentDependency(
        agent_type=AgentType.revision,
        depends_on=[AgentType.knowledge_structuring],
    ),
    AgentType.progress: AgentDependency(
        agent_type=AgentType.progress,
        depends_on=[],
    ),
    AgentType.recommendation: AgentDependency(
        agent_type=AgentType.recommendation,
        depends_on=[],
    ),
}

MANDATORY_AGENTS = [AgentType.document_processing, AgentType.knowledge_structuring]
CONTENT_AGENTS = [
    AgentType.summary,
    AgentType.explanation,
    AgentType.translation,
    AgentType.diagram,
    AgentType.quiz,
    AgentType.revision,
]


def get_dependencies(agent_type: AgentType) -> list[AgentType]:
    """Get the list of agents that must complete before this agent can run."""
    dep = DEPENDENCY_GRAPH.get(agent_type)
    return dep.depends_on if dep else []


def get_content_agents() -> list[AgentType]:
    """Get all content agents that can run in parallel."""
    return CONTENT_AGENTS.copy()


def get_mandatory_agents() -> list[AgentType]:
    """Get the mandatory processing agents in order."""
    return MANDATORY_AGENTS.copy()


def validate_dependencies(
    agent_type: AgentType,
    completed_agents: list[AgentType],
) -> bool:
    """Check if all dependencies for an agent are satisfied."""
    deps = get_dependencies(agent_type)
    return all(dep in completed_agents for dep in deps)


def get_execution_order(
    requested_agents: list[AgentType],
) -> list[list[AgentType]]:
    """Determine execution order with parallelizable groups.

    Returns a list of groups, where each group contains agents that can run in parallel.
    """
    ordered = []
    completed = set()

    for agent in MANDATORY_AGENTS:
        if agent in requested_agents or agent in MANDATORY_AGENTS:
            ordered.append([agent])
            completed.add(agent)

    parallel_group = []
    for agent in CONTENT_AGENTS:
        if agent in requested_agents:
            if validate_dependencies(agent, completed):
                parallel_group.append(agent)
            else:
                if parallel_group:
                    ordered.append(parallel_group)
                    completed.update(parallel_group)
                    parallel_group = []
                ordered.append([agent])
                completed.add(agent)

    if parallel_group:
        ordered.append(parallel_group)

    standalone = []
    for agent in [AgentType.progress, AgentType.recommendation]:
        if agent in requested_agents:
            standalone.append(agent)

    if standalone:
        ordered.append(standalone)

    return ordered
