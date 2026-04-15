# Auto-RAG Research Platform (MVP+ Skeleton)

Ce dépôt contient un squelette exécutable d'une plateforme de recherche autonome RAG.

## Capacités MVP+
- Boucle fermée: observe → propose → run → evaluate → decide → archive
- Benchmark JSONL chargé depuis `data/benchmarks/default.jsonl`
- Génération **et embeddings** via endpoint OpenAI-compatible (Ollama, OpenAI, OpenRouter)
- Registre des expériences (`research_log.md` + `experiment_store/*.json`)
- Champion registry multi-catégories + front de Pareto
- CLI pour lancer une campagne et afficher les champions

## Configuration `.env` (Ollama)
Exemple recommandé:

```bash
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=

GENERATION_MODEL=qwen2.5:7b-instruct
EMBEDDING_MODEL=nomic-embed-text
```

- `GENERATION_MODEL` est utilisé pour `/chat/completions`
- `EMBEDDING_MODEL` est utilisé pour `/embeddings`

Sans endpoint disponible, le pipeline passe en mode fallback mock pour le développement local.

## Lancer une campagne
```bash
python app.py run-campaign --campaign-id default --max-iterations 5 --benchmark data/benchmarks/default.jsonl
```

## Voir les champions
```bash
python app.py show-champions --campaign-id default
```

Les artefacts sont écrits dans `campaigns/<campaign_id>/`.

## Note
Les artefacts de runtime (`experiment_store`, `research_log.md`, `champions.json`) sont générés à l'exécution et ne doivent pas être versionnés avec des résultats de run locaux.
