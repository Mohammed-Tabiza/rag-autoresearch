from src.common.scoring import compute_global_score


def test_global_score_numeric() -> None:
    value = compute_global_score(
        {
            "faithfulness": 0.8,
            "answer_relevance": 0.7,
            "context_precision": 0.6,
            "citation_accuracy": 0.75,
            "normalized_cost": 0.2,
            "normalized_latency": 0.1,
        }
    )
    assert value > 0
