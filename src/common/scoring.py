from __future__ import annotations


def compute_global_score(metrics: dict[str, float]) -> float:
    return (
        0.45 * metrics.get("faithfulness", 0.0)
        + 0.25 * metrics.get("answer_relevance", 0.0)
        + 0.15 * metrics.get("context_precision", 0.0)
        + 0.15 * metrics.get("citation_accuracy", 0.0)
        - 0.10 * metrics.get("normalized_cost", 0.0)
        - 0.05 * metrics.get("normalized_latency", 0.0)
    )
