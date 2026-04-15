from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.orchestrator.campaign_manager import CampaignManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto-RAG research CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_campaign_parser = sub.add_parser("run-campaign", help="Run a research campaign")
    run_campaign_parser.add_argument("--campaign-id", default="default")
    run_campaign_parser.add_argument("--max-iterations", type=int, default=5)
    run_campaign_parser.add_argument("--benchmark", default="data/benchmarks/default.jsonl")

    show_parser = sub.add_parser("show-champions", help="Display champion registry for a campaign")
    show_parser.add_argument("--campaign-id", default="default")
    return parser


def run_campaign(campaign_id: str = "default", max_iterations: int = 5, benchmark: str = "data/benchmarks/default.jsonl") -> int:
    manager = CampaignManager()
    count = manager.run(campaign_id=campaign_id, max_iterations=max_iterations, benchmark_path=Path(benchmark))
    print(f"Campaign {campaign_id} completed with {count} experiments.")
    return count


def show_champions(campaign_id: str = "default") -> None:
    path = Path("campaigns") / campaign_id / "champions.json"
    if not path.exists():
        print(f"No champions file found for campaign '{campaign_id}'.")
        return
    print(json.dumps(json.loads(path.read_text(encoding='utf-8')), ensure_ascii=False, indent=2))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "run-campaign":
        run_campaign(campaign_id=args.campaign_id, max_iterations=args.max_iterations, benchmark=args.benchmark)
    if args.command == "show-champions":
        show_champions(campaign_id=args.campaign_id)


if __name__ == "__main__":
    main()
