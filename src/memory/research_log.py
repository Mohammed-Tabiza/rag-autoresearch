from __future__ import annotations

from pathlib import Path

from src.common.models import ExperimentRecord


class ResearchLog:
    def __init__(self, campaign_dir: Path) -> None:
        self.path = campaign_dir / "research_log.md"
        if not self.path.exists():
            self.path.write_text("# Research Log\n\n", encoding="utf-8")

    def append(self, record: ExperimentRecord) -> None:
        block = (
            f"## {record.experiment_id}\n"
            f"- timestamp: {record.timestamp}\n"
            f"- hypothesis: {record.hypothesis}\n"
            f"- config: `{record.config}`\n"
            f"- metrics: `{record.metrics}`\n"
            f"- cost_usd: {record.cost_usd:.4f}\n"
            f"- latency_ms: {record.latency_ms:.2f}\n"
            f"- status: {record.status}\n"
            f"- notes: {record.notes}\n\n"
        )
        with self.path.open("a", encoding="utf-8") as f:
            f.write(block)
