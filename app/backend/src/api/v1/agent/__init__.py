from fastapi import APIRouter

from src.api.v1.agent.routes import router as agent_router

agent_router_v1 = APIRouter()
agent_router_v1.include_router(agent_router, tags=["agents"])
