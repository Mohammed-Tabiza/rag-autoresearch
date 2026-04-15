from pathlib import Path

from src.benchmarks.dataset_loader import load_questions


def test_load_questions_default_benchmark() -> None:
    rows = load_questions(Path("data/benchmarks/default.jsonl"))
    assert len(rows) >= 3
    assert "question" in rows[0]
