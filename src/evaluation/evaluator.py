from __future__ import annotations

import random


class Evaluator:
    def evaluate(self, pipeline_output: dict) -> dict[str, float]:
        seed = pipeline_output["metrics_seed"]
        return {
            "faithfulness": seed["faithfulness"],
            "answer_relevance": seed["answer_relevance"],
            "context_precision": max(0.0, min(1.0, seed["answer_relevance"] - 0.05)),
            "citation_accuracy": max(0.0, min(1.0, seed["faithfulness"] - 0.04)),
            "normalized_cost": random.uniform(0.15, 0.40),
            "normalized_latency": random.uniform(0.10, 0.30),
        }
