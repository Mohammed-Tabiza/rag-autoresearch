# Auto-RAG Research Platform (MVP Skeleton)

Ce dépôt contient un squelette exécutable d'une plateforme de recherche autonome RAG.

## Capacités MVP
- Boucle fermée: observe → propose → run → evaluate → decide → archive
- Registre des expériences (`research_log.md` + `experiment_store/*.json`)
- Champion registry (`champions.json`)
- Variantes retrieval minimales (`similarity`, `mmr`)
- CLI pour lancer une campagne

## Lancer une campagne
```bash
python app.py run-campaign --campaign-id default --max-iterations 5
```

Les artefacts sont écrits dans `campaigns/<campaign_id>/`.


## Note
Les artefacts de runtime (`experiment_store`, `research_log.md`, `champions.json`) sont générés à l'exécution et ne doivent pas être versionnés avec des résultats de run locaux.
