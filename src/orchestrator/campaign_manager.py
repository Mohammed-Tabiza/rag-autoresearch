from __future__ import annotations

from pathlib import Path

from src.orchestrator.budget_guard import BudgetGuard
from src.orchestrator.experiment_loop import ExperimentLoop
from src.orchestrator.scheduler import Scheduler
from src.orchestrator.state_store import StateStore


class CampaignManager:
    def __init__(self, root: Path = Path("campaigns")) -> None:
        self.root = root
        self.store = StateStore()
        self.scheduler = Scheduler()
        self.budget = BudgetGuard()

    def run(self, campaign_id: str = "default", max_iterations: int = 5) -> int:
        campaign_dir = self.root / campaign_id
        campaign_dir.mkdir(parents=True, exist_ok=True)

        loop = ExperimentLoop(campaign_dir)
        state = self.store.get_or_create(campaign_id)

        while True:
            if self.scheduler.should_stop(state.experiments, max_iterations):
                break
            if not self.budget.can_continue(state.experiments):
                break
            state.experiments.append(loop.run_iteration(campaign_id, state.experiments))
        return len(state.experiments)
