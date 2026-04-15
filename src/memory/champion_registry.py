from __future__ import annotations

import json
from pathlib import Path

from src.common.models import ExperimentRecord
from src.common.scoring import compute_global_score
from src.decision.pareto_front import pareto_front


class ChampionRegistry:
    def __init__(self, campaign_dir: Path) -> None:
        self.path = campaign_dir / "champions.json"

    def update(self, history: list[ExperimentRecord]) -> None:
        if not history:
            return

        best_abs = max(history, key=lambda x: compute_global_score(x.metrics))
        best_cost = min(history, key=lambda x: x.metrics.get("normalized_cost", 1.0))
        best_latency = min(history, key=lambda x: x.metrics.get("normalized_latency", 1.0))
        front = pareto_front(history)

        data = {
            "best_score_absolute": self._serialize(best_abs),
            "best_cost_efficiency": self._serialize(best_cost),
            "best_latency": self._serialize(best_latency),
            "pareto_front": [self._serialize(x) for x in front],
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _serialize(exp: ExperimentRecord) -> dict:
        return {
            "experiment_id": exp.experiment_id,
            "score": compute_global_score(exp.metrics),
            "status": exp.status,
            "metrics": exp.metrics,
            "config": exp.config,
        }
