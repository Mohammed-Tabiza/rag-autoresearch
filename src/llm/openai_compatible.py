from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib import error, request


@dataclass
class ChatResult:
    content: str
    model: str
    usage: dict[str, int]


@dataclass
class EmbeddingResult:
    vector: list[float]
    model: str
    usage: dict[str, int]


class OpenAICompatibleClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.base_url = (
            os.getenv("OPENAI_BASE_URL")
            or os.getenv("OLLAMA_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.generation_model = os.getenv("GENERATION_MODEL") or os.getenv("GENERATOR_MODEL") or "gpt-4.1-mini"
        self.embedding_model = os.getenv("EMBEDDING_MODEL") or "text-embedding-3-large"

    @property
    def enabled(self) -> bool:
        # Ollama OpenAI-compatible endpoint may not require API key.
        if self.api_key:
            return True
        return self.base_url.startswith("http://") or self.base_url.startswith("https://")

    def chat(
        self,
        *,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 350,
    ) -> ChatResult:
        payload = {
            "model": model or self.generation_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        raw = self._post("/chat/completions", payload)
        choice = raw["choices"][0]["message"]["content"]
        usage = raw.get("usage", {})
        return ChatResult(
            content=choice,
            model=raw.get("model", payload["model"]),
            usage={
                "prompt_tokens": int(usage.get("prompt_tokens", 0)),
                "completion_tokens": int(usage.get("completion_tokens", 0)),
                "total_tokens": int(usage.get("total_tokens", 0)),
            },
        )

    def embed(self, *, text: str, model: str | None = None) -> EmbeddingResult:
        payload = {
            "model": model or self.embedding_model,
            "input": text,
        }
        raw = self._post("/embeddings", payload)
        data = raw.get("data", [])
        if not data:
            raise RuntimeError("Embedding response is missing data")
        usage = raw.get("usage", {})
        return EmbeddingResult(
            vector=data[0]["embedding"],
            model=raw.get("model", payload["model"]),
            usage={
                "prompt_tokens": int(usage.get("prompt_tokens", 0)),
                "total_tokens": int(usage.get("total_tokens", usage.get("prompt_tokens", 0))),
            },
        )

    def _post(self, endpoint: str, payload: dict) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(
            f"{self.base_url}{endpoint}",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"LLM HTTP error {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"LLM network error: {exc.reason}") from exc
