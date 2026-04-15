from src.common.models import ExperimentRecord
from src.decision.pareto_front import pareto_front


def record(exp_id: str, quality: float, cost: float, latency: float) -> ExperimentRecord:
    return ExperimentRecord(
        experiment_id=exp_id,
        campaign_id="c1",
        parent_experiment_id=None,
        timestamp="2026-01-01T00:00:00+00:00",
        hypothesis="h",
        config={},
        metrics={
            "faithfulness": quality / 2,
            "answer_relevance": quality / 2,
            "normalized_cost": cost,
            "normalized_latency": latency,
        },
        cost_usd=0.1,
        tokens_in=10,
        tokens_out=10,
        latency_ms=10,
        status="keep",
        notes="",
    )


def test_pareto_front_excludes_dominated() -> None:
    a = record("a", quality=1.2, cost=0.2, latency=0.2)
    b = record("b", quality=1.0, cost=0.3, latency=0.3)
    c = record("c", quality=1.1, cost=0.1, latency=0.4)

    front = pareto_front([a, b, c])
    ids = sorted(item.experiment_id for item in front)

    assert "b" not in ids
    assert "a" in ids
    assert "c" in ids
