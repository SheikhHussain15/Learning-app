import time
from datetime import datetime

from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.models.health_check import HealthCheck, HealthStatus

logger = get_logger("health_service")

COMPONENTS = ["database", "chromadb", "langfuse", "storage", "backend"]


class HealthService:
    def __init__(self, db: Session):
        self.db = db

    def check_database(self) -> dict:
        start = time.time()
        try:
            self.db.execute("SELECT 1")
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "database", "status": HealthStatus.healthy.value, "latency_ms": latency_ms}
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "database", "status": HealthStatus.unhealthy.value, "latency_ms": latency_ms, "error": str(e)}

    def check_chromadb(self) -> dict:
        start = time.time()
        try:
            from src.retrieval.chroma_client import get_chroma_client
            client = get_chroma_client()
            client.heartbeat()
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "chromadb", "status": HealthStatus.healthy.value, "latency_ms": latency_ms}
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "chromadb", "status": HealthStatus.unhealthy.value, "latency_ms": latency_ms, "error": str(e)}

    def check_langfuse(self) -> dict:
        start = time.time()
        try:
            from src.tracing.langfuse_client import get_langfuse
            client = get_langfuse()
            if client:
                latency_ms = int((time.time() - start) * 1000)
                return {"name": "langfuse", "status": HealthStatus.healthy.value, "latency_ms": latency_ms}
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "langfuse", "status": HealthStatus.degraded.value, "latency_ms": latency_ms, "error": "Client not initialized"}
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return {"name": "langfuse", "status": HealthStatus.unhealthy.value, "latency_ms": latency_ms, "error": str(e)}

    def check_all(self) -> dict:
        components = [
            self.check_database(),
            self.check_chromadb(),
            self.check_langfuse(),
        ]

        statuses = [c["status"] for c in components]
        if all(s == HealthStatus.healthy.value for s in statuses):
            overall = HealthStatus.healthy.value
        elif any(s == HealthStatus.unhealthy.value for s in statuses):
            overall = HealthStatus.unhealthy.value
        else:
            overall = HealthStatus.degraded.value

        result = {
            "status": overall,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "components": components,
        }

        for comp in components:
            health_record = HealthCheck(
                component=comp["name"],
                status=comp["status"],
                latency_ms=comp["latency_ms"],
                error_message=comp.get("error"),
            )
            self.db.add(health_record)
        self.db.commit()

        return result

    def check_component(self, component_name: str) -> dict:
        checkers = {
            "database": self.check_database,
            "chromadb": self.check_chromadb,
            "langfuse": self.check_langfuse,
        }
        checker = checkers.get(component_name)
        if not checker:
            return {"name": component_name, "status": HealthStatus.unhealthy.value, "latency_ms": 0, "error": f"Unknown component: {component_name}"}
        return checker()
