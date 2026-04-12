from __future__ import annotations

import json
from pathlib import Path

from src.common.models import ExperimentRecord
from src.common.scoring import compute_global_score


class ChampionRegistry:
    def __init__(self, campaign_dir: Path) -> None:
        self.path = campaign_dir / "champions.json"

    def update(self, history: list[ExperimentRecord]) -> None:
        if not history:
            return
        champion = max(history, key=lambda x: compute_global_score(x.metrics))
        data = {
            "best_score_absolute": {
                "experiment_id": champion.experiment_id,
                "score": compute_global_score(champion.metrics),
                "status": champion.status,
                "config": champion.config,
            }
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
