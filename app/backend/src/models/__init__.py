# Import all models to ensure they're registered in SQLAlchemy metadata
from src.models.agent_output import AgentOutput  # noqa: F401
from src.models.agent_run import AgentRun  # noqa: F401
from src.models.deployment_record import DeploymentRecord  # noqa: F401
from src.models.document import Document  # noqa: F401
from src.models.flashcard_review import FlashcardReview  # noqa: F401
from src.models.health_check import HealthCheck  # noqa: F401
from src.models.processing_node import ProcessingNode  # noqa: F401
from src.models.progress_event import ProgressEvent  # noqa: F401
from src.models.quiz_attempt import QuizAttempt  # noqa: F401
from src.models.recommendation import Recommendation  # noqa: F401
from src.models.secret_rotation_log import SecretRotationLog  # noqa: F401
from src.models.security_audit_log import SecurityAuditLog  # noqa: F401
from src.models.test_suite_result import TestSuiteResult  # noqa: F401
from src.models.tutor_conversation import TutorConversation  # noqa: F401
from src.models.user import User  # noqa: F401
from src.models.user_note import UserNote  # noqa: F401
from src.models.workspace_section import WorkspaceSection  # noqa: F401
