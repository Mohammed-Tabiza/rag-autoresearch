# Idea Lifecycle Tracker (v1.3 - backend core)

Ce dossier contient un backend FastAPI/SQLite pour l'application décrite dans `SPEC.md`.

## Stack

- FastAPI
- sqlite3 natif
- SQLite local (`data/ideas.db`)

## Lancer

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./start.sh
```

### Windows

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
start.bat
```

API: <http://127.0.0.1:8000/docs>

## Endpoints implémentés

### Ideas

- `POST /ideas`
- `GET /ideas`
- `GET /ideas/{id}`
- `PUT /ideas/{id}`
- `DELETE /ideas/{id}` (soft delete)

### Lifecycle

- `POST /ideas/{id}/transition`
- `GET /ideas/{id}/events`

## Notes de conformité SPEC

- `title` est le seul champ obligatoire à la création.
- `domain`, `source_type`, `current_status`, `archived` ont des defaults automatiques.
- `updated_at` est mis à jour sur `PUT`, `DELETE (archive)` et `transition`.
- `last_activity` pour le tri/filtre stale est calculé depuis `MAX(ideas.updated_at, MAX(idea_events.created_at))`.

## Exemples

Création rapide :

```bash
curl -X POST http://127.0.0.1:8000/ideas \
  -H 'content-type: application/json' \
  -d '{"title":"Agentic architecture notebook"}'
```

Transition vers `EN_VEILLE` (avec obligations) :

```bash
curl -X POST http://127.0.0.1:8000/ideas/<id>/transition \
  -H 'content-type: application/json' \
  -d '{
        "to_status":"EN_VEILLE",
        "comment":"Attente dépendance externe",
        "reason_code":"WAITING_DEPENDENCY",
        "revisit_at":"2026-06-01T09:00:00Z"
      }'
```
