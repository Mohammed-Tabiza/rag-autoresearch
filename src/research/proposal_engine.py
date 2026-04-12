from __future__ import annotations

import random
from src.common.models import ExperimentRecord
from src.research.search_space import SearchSpace


class ProposalEngine:
    def __init__(self, search_space: SearchSpace | None = None) -> None:
        self.search_space = search_space or SearchSpace()

    def propose(self, history: list[ExperimentRecord]) -> tuple[dict, str]:
        seen = {self._signature(x.config) for x in history}
        for _ in range(100):
            candidate = {
                "retriever_type": random.choice(self.search_space.retriever_type),
                "chunk_size": random.choice(self.search_space.chunk_size),
                "chunk_overlap": random.choice(self.search_space.chunk_overlap),
                "top_k": random.choice(self.search_space.top_k),
                "temperature": random.choice(self.search_space.temperature),
            }
            if self._signature(candidate) not in seen:
                hypothesis = (
                    f"Tester {candidate['retriever_type']} avec chunk_size={candidate['chunk_size']} "
                    f"et top_k={candidate['top_k']} pour améliorer le compromis qualité/coût."
                )
                return candidate, hypothesis
        return {
            "retriever_type": "similarity",
            "chunk_size": 600,
            "chunk_overlap": 80,
            "top_k": 8,
            "temperature": 0.0,
        }, "Fallback config faute de nouveauté dans l'espace de recherche."

    @staticmethod
    def _signature(config: dict) -> tuple[tuple[str, str], ...]:
        return tuple(sorted((k, str(v)) for k, v in config.items()))
