from __future__ import annotations

from dataclasses import dataclass, field

from src.common.models import ExperimentRecord


@dataclass
class CampaignState:
    campaign_id: str
    experiments: list[ExperimentRecord] = field(default_factory=list)
    best_experiment_id: str | None = None


class StateStore:
    def __init__(self) -> None:
        self._states: dict[str, CampaignState] = {}

    def get_or_create(self, campaign_id: str) -> CampaignState:
        if campaign_id not in self._states:
            self._states[campaign_id] = CampaignState(campaign_id=campaign_id)
        return self._states[campaign_id]
