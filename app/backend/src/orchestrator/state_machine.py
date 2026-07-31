from src.models.agent_run import AgentStatus

VALID_TRANSITIONS: dict[AgentStatus, set[AgentStatus]] = {
    AgentStatus.queued: {AgentStatus.running},
    AgentStatus.running: {AgentStatus.succeeded, AgentStatus.failed, AgentStatus.cancelled},
    AgentStatus.succeeded: set(),
    AgentStatus.failed: set(),
    AgentStatus.cancelled: set(),
}


class InvalidTransitionError(Exception):
    def __init__(self, from_status: AgentStatus, to_status: AgentStatus):
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(f"Invalid transition: {from_status.value} -> {to_status.value}")


def validate_transition(from_status: AgentStatus, to_status: AgentStatus) -> bool:
    allowed = VALID_TRANSITIONS.get(from_status, set())
    if to_status not in allowed:
        raise InvalidTransitionError(from_status, to_status)
    return True


def can_transition(from_status: AgentStatus, to_status: AgentStatus) -> bool:
    try:
        validate_transition(from_status, to_status)
        return True
    except InvalidTransitionError:
        return False


def is_terminal(status: AgentStatus) -> bool:
    return status in {AgentStatus.succeeded, AgentStatus.failed, AgentStatus.cancelled}
