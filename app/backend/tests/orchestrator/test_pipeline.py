import pytest
from src.orchestrator.pipeline import (
    get_execution_order,
    get_dependencies,
    get_content_agents,
    get_mandatory_agents,
    validate_dependencies,
    DEPENDENCY_GRAPH,
    MANDATORY_AGENTS,
    CONTENT_AGENTS,
)
from src.models.agent_run import AgentType


class TestDependencyGraph:
    def test_dependency_graph_has_all_agents(self):
        expected_agents = [
            AgentType.document_processing,
            AgentType.knowledge_structuring,
            AgentType.summary,
            AgentType.explanation,
            AgentType.translation,
            AgentType.diagram,
            AgentType.quiz,
            AgentType.revision,
            AgentType.progress,
            AgentType.recommendation,
        ]
        for agent in expected_agents:
            assert agent in DEPENDENCY_GRAPH

    def test_document_processing_has_no_dependencies(self):
        deps = get_dependencies(AgentType.document_processing)
        assert deps == []

    def test_knowledge_structuring_depends_on_document_processing(self):
        deps = get_dependencies(AgentType.knowledge_structuring)
        assert AgentType.document_processing in deps

    def test_summary_depends_on_knowledge_structuring(self):
        deps = get_dependencies(AgentType.summary)
        assert AgentType.knowledge_structuring in deps

    def test_all_content_agents_depend_on_knowledge_structuring(self):
        for agent in CONTENT_AGENTS:
            deps = get_dependencies(agent)
            assert AgentType.knowledge_structuring in deps

    def test_progress_has_no_dependencies(self):
        deps = get_dependencies(AgentType.progress)
        assert deps == []

    def test_recommendation_has_no_dependencies(self):
        deps = get_dependencies(AgentType.recommendation)
        assert deps == []


class TestExecutionOrder:
    def test_mandatory_agents_first(self):
        order = get_execution_order([AgentType.document_processing, AgentType.knowledge_structuring])
        assert order[0] == [AgentType.document_processing]
        assert order[1] == [AgentType.knowledge_structuring]

    def test_content_agents_parallel(self):
        order = get_execution_order([
            AgentType.document_processing,
            AgentType.knowledge_structuring,
            AgentType.summary,
            AgentType.quiz,
        ])
        parallel_group = [g for g in order if len(g) > 1]
        assert len(parallel_group) > 0

    def test_standalone_agents_last(self):
        order = get_execution_order([
            AgentType.document_processing,
            AgentType.knowledge_structuring,
            AgentType.progress,
        ])
        assert order[-1] == [AgentType.progress]


class TestValidation:
    def test_validate_dependencies_satisfied(self):
        completed = [AgentType.document_processing, AgentType.knowledge_structuring]
        assert validate_dependencies(AgentType.summary, completed) is True

    def test_validate_dependencies_not_satisfied(self):
        completed = [AgentType.document_processing]
        assert validate_dependencies(AgentType.summary, completed) is False

    def test_validate_dependencies_no_deps(self):
        assert validate_dependencies(AgentType.document_processing, []) is True
        assert validate_dependencies(AgentType.progress, []) is True
        assert validate_dependencies(AgentType.recommendation, []) is True


class TestHelperFunctions:
    def test_get_content_agents(self):
        agents = get_content_agents()
        assert AgentType.summary in agents
        assert AgentType.quiz in agents
        assert AgentType.document_processing not in agents

    def test_get_mandatory_agents(self):
        agents = get_mandatory_agents()
        assert AgentType.document_processing in agents
        assert AgentType.knowledge_structuring in agents
        assert AgentType.summary not in agents
