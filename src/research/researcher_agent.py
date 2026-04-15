from __future__ import annotations

from src.common.models import ExperimentRecord
from src.research.proposal_engine import ProposalEngine


class ResearcherAgent:
    def __init__(self, proposal_engine: ProposalEngine | None = None) -> None:
        self.proposal_engine = proposal_engine or ProposalEngine()

    def next_experiment(self, history: list[ExperimentRecord]) -> tuple[dict, str]:
        return self.proposal_engine.propose(history)
