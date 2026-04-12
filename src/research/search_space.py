from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchSpace:
    retriever_type: list[str] = None
    chunk_size: list[int] = None
    chunk_overlap: list[int] = None
    top_k: list[int] = None
    temperature: list[float] = None

    def __post_init__(self) -> None:
        self.retriever_type = self.retriever_type or ["similarity", "mmr"]
        self.chunk_size = self.chunk_size or [400, 600, 800]
        self.chunk_overlap = self.chunk_overlap or [40, 80]
        self.top_k = self.top_k or [4, 8, 12]
        self.temperature = self.temperature or [0.0, 0.2]
