from src.rag.pipeline import RagPipeline


def test_pipeline_uses_fallback_or_model() -> None:
    pipe = RagPipeline()
    result = pipe.run(
        config={
            "retriever_type": "similarity",
            "chunk_size": 400,
            "top_k": 4,
            "temperature": 0.0,
            "generator_model": "qwen2.5:7b-instruct",
            "embedding_model": "nomic-embed-text",
        },
        question="What is RAG?",
    )

    assert "answer" in result
    assert "metrics_seed" in result
    assert "embedding_model" in result["llm"]
    assert result["llm"]["used"] in (True, False)
