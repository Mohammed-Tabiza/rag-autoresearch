from __future__ import annotations

import json
from pathlib import Path

from src.common.models import ExperimentRecord


class ExperimentStore:
    def __init__(self, campaign_dir: Path) -> None:
        self.campaign_dir = campaign_dir
        self.store_dir = campaign_dir / "experiment_store"
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, record: ExperimentRecord) -> None:
        path = self.store_dir / f"{record.experiment_id}.json"
        path.write_text(json.dumps(record.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
