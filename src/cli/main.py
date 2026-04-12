from __future__ import annotations

import argparse

from src.orchestrator.campaign_manager import CampaignManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto-RAG research CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_campaign_parser = sub.add_parser("run-campaign", help="Run a research campaign")
    run_campaign_parser.add_argument("--campaign-id", default="default")
    run_campaign_parser.add_argument("--max-iterations", type=int, default=5)
    return parser


def run_campaign(campaign_id: str = "default", max_iterations: int = 5) -> int:
    manager = CampaignManager()
    count = manager.run(campaign_id=campaign_id, max_iterations=max_iterations)
    print(f"Campaign {campaign_id} completed with {count} experiments.")
    return count


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "run-campaign":
        run_campaign(campaign_id=args.campaign_id, max_iterations=args.max_iterations)


if __name__ == "__main__":
    main()
