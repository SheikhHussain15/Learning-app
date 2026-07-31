import pytest
from src.orchestrator.state_machine import (
    validate_transition,
    can_transition,
    is_terminal,
    InvalidTransitionError,
)
from src.models.agent_run import AgentStatus


def test_valid_transitions():
    validate_transition(AgentStatus.queued, AgentStatus.running)
    validate_transition(AgentStatus.running, AgentStatus.succeeded)
    validate_transition(AgentStatus.running, AgentStatus.failed)
    validate_transition(AgentStatus.running, AgentStatus.cancelled)


def test_invalid_transitions():
    with pytest.raises(InvalidTransitionError):
        validate_transition(AgentStatus.queued, AgentStatus.succeeded)
    with pytest.raises(InvalidTransitionError):
        validate_transition(AgentStatus.queued, AgentStatus.failed)
    with pytest.raises(InvalidTransitionError):
        validate_transition(AgentStatus.succeeded, AgentStatus.running)
    with pytest.raises(InvalidTransitionError):
        validate_transition(AgentStatus.failed, AgentStatus.running)
    with pytest.raises(InvalidTransitionError):
        validate_transition(AgentStatus.cancelled, AgentStatus.running)


def test_can_transition():
    assert can_transition(AgentStatus.queued, AgentStatus.running) is True
    assert can_transition(AgentStatus.running, AgentStatus.succeeded) is True
    assert can_transition(AgentStatus.queued, AgentStatus.succeeded) is False
    assert can_transition(AgentStatus.succeeded, AgentStatus.failed) is False


def test_is_terminal():
    assert is_terminal(AgentStatus.succeeded) is True
    assert is_terminal(AgentStatus.failed) is True
    assert is_terminal(AgentStatus.cancelled) is True
    assert is_terminal(AgentStatus.queued) is False
    assert is_terminal(AgentStatus.running) is False
