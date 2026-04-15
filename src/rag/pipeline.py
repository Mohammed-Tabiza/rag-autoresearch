from __future__ import annotations

import math
import random

from src.llm.openai_compatible import OpenAICompatibleClient


class RagPipeline:
    def __init__(self) -> None:
        self.client = OpenAICompatibleClient()

    def run(self, config: dict, question: str) -> dict:
        chunks = self._build_chunks(config)

        # Try real embedding-based retrieval first.
        if self.client.enabled:
            try:
                q_emb = self.client.embed(text=question, model=config.get("embedding_model"))
                scored: list[tuple[float, str]] = []
                emb_tokens = q_emb.usage.get("total_tokens", 0)
                emb_model = q_emb.model
                for chunk in chunks:
                    c_emb = self.client.embed(text=chunk, model=config.get("embedding_model"))
                    score = self._cosine(q_emb.vector, c_emb.vector)
                    scored.append((score, chunk))
                    emb_tokens += c_emb.usage.get("total_tokens", 0)
                    emb_model = c_emb.model
                scored.sort(reverse=True, key=lambda x: x[0])
                context = "\n".join([c for _, c in scored[: max(1, int(config.get("top_k", 4)) // 2)]])

                result = self.client.chat(
                    model=config.get("generator_model") or config.get("generation_model"),
                    temperature=float(config.get("temperature", 0.0)),
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a RAG assistant. Answer only from provided context. If uncertain, say you don't know.",
                        },
                        {
                            "role": "user",
                            "content": f"Context:\n{context}\n\nQuestion: {question}\nReturn a concise grounded answer.",
                        },
                    ],
                )
                answer = result.content
                seed = self._heuristic_metrics(config, question, answer)
                seed["citation_accuracy"] = min(1.0, seed["faithfulness"] + 0.03)
                return {
                    "answer": answer,
                    "metrics_seed": seed,
                    "llm": {
                        "used": True,
                        "model": result.model,
                        "embedding_model": emb_model,
                        "usage": {
                            "prompt_tokens": result.usage.get("prompt_tokens", 0),
                            "completion_tokens": result.usage.get("completion_tokens", 0),
                            "total_tokens": result.usage.get("total_tokens", 0) + emb_tokens,
                        },
                    },
                }
            except Exception:
                # Fall through to deterministic local mock if remote model/embeddings fail.
                pass

        answer = f"[MOCK] Réponse simulée pour: {question}"
        seed = self._heuristic_metrics(config, question, answer)
        seed["citation_accuracy"] = max(0.0, seed["faithfulness"] - 0.04)
        return {
            "answer": answer,
            "metrics_seed": seed,
            "llm": {
                "used": False,
                "model": "mock",
                "embedding_model": "mock",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            },
        }

    @staticmethod
    def _build_chunks(config: dict) -> list[str]:
        return [
            f"retriever={config.get('retriever_type')}",
            f"top_k={config.get('top_k')}",
            f"chunk_size={config.get('chunk_size')}",
            "grounded answers require faithful context usage",
            "citation accuracy improves traceability",
        ]

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        n = min(len(a), len(b))
        if n == 0:
            return 0.0
        a = a[:n]
        b = b[:n]
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    @staticmethod
    def _heuristic_metrics(config: dict, question: str, answer: str) -> dict[str, float]:
        seed = hash((question, answer, tuple(sorted(config.items())))) & 0xFFFFFFFF
        rnd = random.Random(seed)

        base = 0.67 if config.get("retriever_type") == "similarity" else 0.72
        top_k_bonus = min(int(config.get("top_k", 4)), 12) * 0.008
        chunk_penalty = 0.03 if int(config.get("chunk_size", 600)) > 700 else 0.0

        faithfulness = max(0.0, min(1.0, base + top_k_bonus - chunk_penalty + rnd.uniform(-0.02, 0.02)))
        relevance = max(0.0, min(1.0, base + 0.08 + rnd.uniform(-0.02, 0.02)))
        return {
            "faithfulness": faithfulness,
            "answer_relevance": relevance,
        }
