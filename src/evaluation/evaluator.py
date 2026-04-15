from __future__ import annotations


class Evaluator:
    def evaluate(self, outputs: list[dict]) -> dict[str, float]:
        if not outputs:
            return {
                "faithfulness": 0.0,
                "answer_relevance": 0.0,
                "context_precision": 0.0,
                "citation_accuracy": 0.0,
                "normalized_cost": 1.0,
                "normalized_latency": 1.0,
            }

        faithfulness = sum(x["metrics_seed"]["faithfulness"] for x in outputs) / len(outputs)
        relevance = sum(x["metrics_seed"]["answer_relevance"] for x in outputs) / len(outputs)
        citation = sum(x["metrics_seed"]["citation_accuracy"] for x in outputs) / len(outputs)

        total_tokens = sum(x.get("llm", {}).get("usage", {}).get("total_tokens", 0) for x in outputs)
        used_model_count = sum(1 for x in outputs if x.get("llm", {}).get("used"))

        if used_model_count:
            normalized_cost = min(1.0, 0.1 + total_tokens / 20_000)
            normalized_latency = min(1.0, 0.15 + 0.03 * len(outputs))
        else:
            normalized_cost = min(1.0, 0.05 + 0.01 * len(outputs))
            normalized_latency = min(1.0, 0.05 + 0.01 * len(outputs))

        return {
            "faithfulness": faithfulness,
            "answer_relevance": relevance,
            "context_precision": max(0.0, min(1.0, relevance - 0.05)),
            "citation_accuracy": citation,
            "normalized_cost": normalized_cost,
            "normalized_latency": normalized_latency,
        }
