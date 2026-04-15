from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.benchmarks.dataset_loader import load_questions
from src.common.models import ExperimentRecord
from src.decision.decision_engine import DecisionEngine
from src.evaluation.evaluator import Evaluator
from src.memory.champion_registry import ChampionRegistry
from src.memory.experiment_store import ExperimentStore
from src.memory.research_log import ResearchLog
from src.rag.pipeline import RagPipeline
from src.research.researcher_agent import ResearcherAgent


class ExperimentLoop:
    def __init__(self, campaign_dir: Path, benchmark_path: Path | None = None) -> None:
        self.researcher = ResearcherAgent()
        self.pipeline = RagPipeline()
        self.evaluator = Evaluator()
        self.decider = DecisionEngine()
        self.store = ExperimentStore(campaign_dir)
        self.log = ResearchLog(campaign_dir)
        self.champions = ChampionRegistry(campaign_dir)
        self.benchmark_path = benchmark_path or Path("data/benchmarks/default.jsonl")

    def run_iteration(self, campaign_id: str, history: list[ExperimentRecord]) -> ExperimentRecord:
        config, hypothesis = self.researcher.next_experiment(history)
        questions = load_questions(self.benchmark_path)
        outputs = [self.pipeline.run(config=config, question=item["question"]) for item in questions]
        metrics = self.evaluator.evaluate(outputs)

        tokens_in = sum(x.get("llm", {}).get("usage", {}).get("prompt_tokens", 0) for x in outputs)
        tokens_out = sum(x.get("llm", {}).get("usage", {}).get("completion_tokens", 0) for x in outputs)
        models_used = sorted({x.get("llm", {}).get("model", "mock") for x in outputs})

        record = ExperimentRecord(
            experiment_id=f"exp_{uuid4().hex[:8]}",
            campaign_id=campaign_id,
            parent_experiment_id=history[-1].experiment_id if history else None,
            timestamp=datetime.now(timezone.utc).isoformat(),
            hypothesis=hypothesis,
            config=config,
            metrics=metrics,
            cost_usd=round((metrics["normalized_cost"] * 0.05), 5),
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=round(450 + metrics["normalized_latency"] * 1100, 2),
            status="baseline",
            notes=f"Benchmark run on {self.benchmark_path}; models={models_used}",
        )
        record.status = self.decider.decide(record, history)

        self.store.persist(record)
        self.log.append(record)
        self.champions.update(history + [record])
        return record
