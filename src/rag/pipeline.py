from __future__ import annotations

import random


class RagPipeline:
    def run(self, config: dict, question: str) -> dict:
        base = 0.65 if config.get("retriever_type") == "similarity" else 0.7
        top_k_bonus = min(config.get("top_k", 4), 10) * 0.01
        chunk_penalty = 0.03 if config.get("chunk_size", 600) > 700 else 0.0

        faithfulness = max(0.0, min(1.0, base + top_k_bonus - chunk_penalty + random.uniform(-0.02, 0.02)))
        relevance = max(0.0, min(1.0, base + 0.08 + random.uniform(-0.03, 0.03)))

        return {
            "answer": f"Réponse simulée pour: {question}",
            "metrics_seed": {
                "faithfulness": faithfulness,
                "answer_relevance": relevance,
            },
        }
