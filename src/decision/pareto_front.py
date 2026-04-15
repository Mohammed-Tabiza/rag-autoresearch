from __future__ import annotations

from src.common.models import ExperimentRecord


def dominates(a: ExperimentRecord, b: ExperimentRecord) -> bool:
    a_quality = a.metrics.get("faithfulness", 0.0) + a.metrics.get("answer_relevance", 0.0)
    b_quality = b.metrics.get("faithfulness", 0.0) + b.metrics.get("answer_relevance", 0.0)

    a_cost = a.metrics.get("normalized_cost", 1.0)
    b_cost = b.metrics.get("normalized_cost", 1.0)
    a_latency = a.metrics.get("normalized_latency", 1.0)
    b_latency = b.metrics.get("normalized_latency", 1.0)

    better_or_equal = a_quality >= b_quality and a_cost <= b_cost and a_latency <= b_latency
    strictly_better = a_quality > b_quality or a_cost < b_cost or a_latency < b_latency
    return better_or_equal and strictly_better


def pareto_front(experiments: list[ExperimentRecord]) -> list[ExperimentRecord]:
    front: list[ExperimentRecord] = []
    for candidate in experiments:
        if any(dominates(other, candidate) for other in experiments if other.experiment_id != candidate.experiment_id):
            continue
        front.append(candidate)
    return front
