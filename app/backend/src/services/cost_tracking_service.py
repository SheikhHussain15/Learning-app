from datetime import datetime

from src.core.logging import get_logger

logger = get_logger("cost_tracking")


class CostTrackingService:
    def __init__(self):
        self._records = []

    def record_generation(
        self,
        agent_type: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: int,
        trace_id: str | None = None,
        user_id: str | None = None,
    ):
        total_tokens = prompt_tokens + completion_tokens
        cost_per_1k = self._get_cost_per_1k(model)
        estimated_cost = (total_tokens / 1000) * cost_per_1k

        record = {
            "agent_type": agent_type,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "latency_ms": latency_ms,
            "estimated_cost": estimated_cost,
            "trace_id": trace_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._records.append(record)

        logger.info(
            "generation_recorded",
            agent_type=agent_type,
            model=model,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            estimated_cost=estimated_cost,
            trace_id=trace_id,
        )

        return record

    def _get_cost_per_1k(self, model: str) -> float:
        costs = {
            "openai/gpt-4o": 0.005,
            "openai/gpt-4o-mini": 0.00015,
            "anthropic/claude-3.5-sonnet": 0.003,
            "anthropic/claude-3-haiku": 0.00025,
        }
        return costs.get(model, 0.003)

    def get_daily_summary(self, date: str | None = None) -> dict:
        if not date:
            date = datetime.utcnow().strftime("%Y-%m-%d")

        daily_records = [
            r for r in self._records
            if r["timestamp"].startswith(date)
        ]

        total_cost = sum(r["estimated_cost"] for r in daily_records)
        total_tokens = sum(r["total_tokens"] for r in daily_records)
        avg_latency = (
            sum(r["latency_ms"] for r in daily_records) / len(daily_records)
            if daily_records
            else 0
        )

        return {
            "date": date,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "request_count": len(daily_records),
            "average_latency_ms": round(avg_latency),
        }


cost_tracker = CostTrackingService()
