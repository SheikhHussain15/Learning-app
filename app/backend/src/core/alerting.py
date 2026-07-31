import time
from collections import deque

from src.core.logging import get_logger

logger = get_logger("alerting")


class AlertingService:
    def __init__(self):
        self._error_counts = deque(maxlen=1000)
        self._latency_records = deque(maxlen=1000)
        self._alerts = []

    def record_request(self, success: bool, latency_ms: float):
        self._error_counts.append({"success": success, "timestamp": time.time()})
        self._latency_records.append({"latency_ms": latency_ms, "timestamp": time.time()})

    def get_error_rate(self, window_seconds: int = 60) -> float:
        cutoff = time.time() - window_seconds
        recent = [r for r in self._error_counts if r["timestamp"] >= cutoff]
        if not recent:
            return 0.0
        failures = sum(1 for r in recent if not r["success"])
        return failures / len(recent)

    def get_p95_latency(self, window_seconds: int = 60) -> float:
        cutoff = time.time() - window_seconds
        recent = [r["latency_ms"] for r in self._latency_records if r["timestamp"] >= cutoff]
        if not recent:
            return 0.0
        recent.sort()
        idx = int(len(recent) * 0.95)
        return recent[min(idx, len(recent) - 1)]

    def check_thresholds(self) -> list[dict]:
        alerts = []
        error_rate = self.get_error_rate(60)
        p95_latency = self.get_p95_latency(60)

        if error_rate > 0.10:
            alerts.append({
                "level": "critical",
                "metric": "error_rate",
                "value": error_rate,
                "threshold": 0.10,
                "message": f"Error rate {error_rate:.1%} exceeds critical threshold of 10%",
            })
        elif error_rate > 0.05:
            alerts.append({
                "level": "warning",
                "metric": "error_rate",
                "value": error_rate,
                "threshold": 0.05,
                "message": f"Error rate {error_rate:.1%} exceeds warning threshold of 5%",
            })

        if p95_latency > 10000:
            alerts.append({
                "level": "critical",
                "metric": "p95_latency",
                "value": p95_latency,
                "threshold": 10000,
                "message": f"P95 latency {p95_latency:.0f}ms exceeds critical threshold of 10s",
            })
        elif p95_latency > 5000:
            alerts.append({
                "level": "warning",
                "metric": "p95_latency",
                "value": p95_latency,
                "threshold": 5000,
                "message": f"P95 latency {p95_latency:.0f}ms exceeds warning threshold of 5s",
            })

        for alert in alerts:
            logger.warning("alert_triggered", **alert)

        return alerts

    def get_status(self) -> dict:
        return {
            "error_rate_1m": self.get_error_rate(60),
            "error_rate_5m": self.get_error_rate(300),
            "p95_latency_1m": self.get_p95_latency(60),
            "p95_latency_5m": self.get_p95_latency(300),
            "active_alerts": self.check_thresholds(),
        }


alerting_service = AlertingService()
