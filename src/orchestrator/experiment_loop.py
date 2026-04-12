from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.common.models import ExperimentRecord
from src.decision.decision_engine import DecisionEngine
from src.evaluation.evaluator import Evaluator
from src.memory.champion_registry import ChampionRegistry
from src.memory.experiment_store import ExperimentStore
from src.memory.research_log import ResearchLog
from src.rag.pipeline import RagPipeline
from src.research.researcher_agent import ResearcherAgent


class ExperimentLoop:
    def __init__(self, campaign_dir: Path) -> None:
        self.researcher = ResearcherAgent()
        self.pipeline = RagPipeline()
        self.evaluator = Evaluator()
        self.decider = DecisionEngine()
        self.store = ExperimentStore(campaign_dir)
        self.log = ResearchLog(campaign_dir)
        self.champions = ChampionRegistry(campaign_dir)

    def run_iteration(self, campaign_id: str, history: list[ExperimentRecord]) -> ExperimentRecord:
        config, hypothesis = self.researcher.next_experiment(history)
        output = self.pipeline.run(config=config, question="What is RAG optimization?")
        metrics = self.evaluator.evaluate(output)

        record = ExperimentRecord(
            experiment_id=f"exp_{uuid4().hex[:8]}",
            campaign_id=campaign_id,
            parent_experiment_id=history[-1].experiment_id if history else None,
            timestamp=datetime.now(timezone.utc).isoformat(),
            hypothesis=hypothesis,
            config=config,
            metrics=metrics,
            cost_usd=round((metrics["normalized_cost"] * 0.02), 5),
            tokens_in=900,
            tokens_out=220,
            latency_ms=round(400 + metrics["normalized_latency"] * 1200, 2),
            status="baseline",
            notes="MVP simulated run",
        )
        record.status = self.decider.decide(record, history)

        self.store.persist(record)
        self.log.append(record)
        self.champions.update(history + [record])
        return record
