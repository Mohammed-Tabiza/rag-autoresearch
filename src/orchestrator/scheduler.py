from __future__ import annotations

from src.common.models import ExperimentRecord


class Scheduler:
    def should_stop(self, history: list[ExperimentRecord], max_iterations: int) -> bool:
        return len(history) >= max_iterations
