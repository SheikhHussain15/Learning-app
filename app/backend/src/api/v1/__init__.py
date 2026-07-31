from fastapi import APIRouter

from src.api.v1.agent.routes import router as agent_router
from src.api.v1.auth import login, logout, profile, register
from src.api.v1.dashboard.routes import router as dashboard_router
from src.api.v1.deploy.routes import router as deploy_router
from src.api.v1.diagram.routes import router as diagram_router
from src.api.v1.document import router as document_router
from src.api.v1.flashcard.routes import router as flashcard_router
from src.api.v1.health.routes import router as health_router
from src.api.v1.progress.routes import router as progress_router
from src.api.v1.quiz.routes import router as quiz_router
from src.api.v1.security.routes import router as security_router
from src.api.v1.testing.routes import router as testing_router
from src.api.v1.tutor.routes import router as tutor_router
from src.api.v1.workspace.routes import router as workspace_router

api_router = APIRouter()
api_router.include_router(register.router, prefix="/auth", tags=["auth"])
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/auth", tags=["auth"])
api_router.include_router(logout.router, prefix="/auth", tags=["auth"])
api_router.include_router(document_router, prefix="/document", tags=["document"])
api_router.include_router(agent_router, prefix="", tags=["agents"])
api_router.include_router(workspace_router, tags=["workspace"])
api_router.include_router(dashboard_router, tags=["dashboard"])
api_router.include_router(quiz_router, tags=["quiz"])
api_router.include_router(flashcard_router, tags=["flashcard"])
api_router.include_router(tutor_router, tags=["tutor"])
api_router.include_router(progress_router, tags=["progress"])
api_router.include_router(diagram_router, tags=["diagram"])
api_router.include_router(testing_router, prefix="/testing", tags=["testing"])
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(deploy_router, prefix="/deploy", tags=["deploy"])
api_router.include_router(security_router, prefix="/security", tags=["security"])
