from __future__ import annotations

from src.common.models import ExperimentRecord


class BudgetGuard:
    def __init__(self, max_total_cost_usd: float = 10.0, max_total_tokens: int = 300_000) -> None:
        self.max_total_cost_usd = max_total_cost_usd
        self.max_total_tokens = max_total_tokens

    def can_continue(self, history: list[ExperimentRecord]) -> bool:
        total_cost = sum(item.cost_usd for item in history)
        total_tokens = sum(item.tokens_in + item.tokens_out for item in history)
        return total_cost < self.max_total_cost_usd and total_tokens < self.max_total_tokens
