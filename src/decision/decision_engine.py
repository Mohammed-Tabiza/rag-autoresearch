from __future__ import annotations

from src.common.models import ExperimentRecord
from src.common.scoring import compute_global_score


class DecisionEngine:
    def decide(self, current: ExperimentRecord, history: list[ExperimentRecord]) -> str:
        current_score = compute_global_score(current.metrics)
        if not history:
            return "baseline"

        best_score = max(compute_global_score(exp.metrics) for exp in history)
        if current_score > best_score + 0.02:
            return "promote"
        if current_score >= best_score - 0.01:
            return "keep"
        return "discard"
