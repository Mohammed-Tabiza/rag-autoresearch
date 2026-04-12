from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ExperimentRecord:
    experiment_id: str
    campaign_id: str
    parent_experiment_id: str | None
    timestamp: str
    hypothesis: str
    config: dict[str, Any]
    metrics: dict[str, float]
    cost_usd: float
    tokens_in: int
    tokens_out: int
    latency_ms: float
    status: str  # baseline / keep / discard / neutral / promote / crash
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
