from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from .db import get_connection
from .schemas import EventType, IdeaCreate, IdeaUpdate, TransitionRequest

SORT_COLUMNS: dict[str, str] = {
    "created_at": "ideas.created_at",
    "last_activity": "last_activity",
    "estimated_value": "ideas.estimated_value",
}

Order = Literal["asc", "desc"]

ALLOWED_TRANSITIONS: dict[str, list[str]] = {
    "GERME": ["EXPLORATION", "ABANDONNE"],
    "EXPLORATION": ["POC", "EN_VEILLE", "ABANDONNE"],
    "POC": ["TRANSMIS", "EN_VEILLE", "ABANDONNE"],
    "TRANSMIS": ["REALISE", "EN_VEILLE"],
    "EN_VEILLE": ["EXPLORATION", "ABANDONNE"],
    "ABANDONNE": ["EXPLORATION"],
    "REALISE": [],
}

REQUIRED_COMMENT_STATUSES = {"TRANSMIS", "EN_VEILLE", "ABANDONNE", "REALISE"}
REQUIRED_REASON_STATUS: dict[str, set[str]] = {
    "EN_VEILLE": {"TOO_EARLY", "NO_PRIORITY", "WAITING_DEPENDENCY"},
    "ABANDONNE": {"NO_VALUE", "TOO_COMPLEX", "DUPLICATE", "CONTEXT_CHANGED"},
}


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _create_event(
    conn,
    idea_id: str,
    event_type: EventType,
    from_status: str | None,
    to_status: str | None,
    comment: str,
    reason_code: str | None,
) -> None:
    conn.execute(
        """
        INSERT INTO idea_events (id, idea_id, event_type, from_status, to_status, comment, reason_code, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (str(uuid4()), idea_id, event_type.value, from_status, to_status, comment, reason_code, now_iso()),
    )


def create_idea(payload: IdeaCreate) -> dict:
    idea_id = str(uuid4())
    title = payload.title.strip()
    if not title:
        raise ValueError("title must not be empty")

    timestamp = now_iso()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ideas (
                id, title, description, domain, tags, source_type, source_context,
                created_at, updated_at, current_status, archived,
                confidence_level, estimated_value, estimated_effort,
                next_action, revisit_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'GERME', 0, ?, ?, ?, ?, ?)
            """,
            (
                idea_id,
                title,
                payload.description,
                payload.domain.value,
                json.dumps(payload.tags),
                payload.source_type.value,
                payload.source_context,
                timestamp,
                timestamp,
                payload.confidence_level,
                payload.estimated_value,
                payload.estimated_effort,
                payload.next_action,
                payload.revisit_at.isoformat() if payload.revisit_at else None,
            ),
        )
        _create_event(conn, idea_id, EventType.CREATION, None, "GERME", "", None)

    return get_idea_by_id(idea_id)


def get_idea_by_id(idea_id: str) -> dict:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()

    if row is None:
        raise ValueError("Idea not found")

    return _row_to_dict(row)


def update_idea(idea_id: str, payload: IdeaUpdate) -> dict:
    existing = get_idea_by_id(idea_id)

    update_data = payload.model_dump(exclude_unset=True)
    if "title" in update_data and update_data["title"] is not None:
        update_data["title"] = update_data["title"].strip()
        if not update_data["title"]:
            raise ValueError("title must not be empty")

    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = json.dumps(update_data["tags"])

    if "domain" in update_data and update_data["domain"] is not None:
        update_data["domain"] = update_data["domain"].value

    if "source_type" in update_data and update_data["source_type"] is not None:
        update_data["source_type"] = update_data["source_type"].value

    if "revisit_at" in update_data and update_data["revisit_at"] is not None:
        update_data["revisit_at"] = update_data["revisit_at"].isoformat()

    if not update_data:
        return existing

    update_data["updated_at"] = now_iso()

    fields = ", ".join(f"{field} = ?" for field in update_data)
    values = list(update_data.values()) + [idea_id]

    with get_connection() as conn:
        conn.execute(f"UPDATE ideas SET {fields} WHERE id = ?", values)
        _create_event(conn, idea_id, EventType.EDIT, None, None, "Idea edited", None)

    return get_idea_by_id(idea_id)


def archive_idea(idea_id: str) -> None:
    _ = get_idea_by_id(idea_id)
    with get_connection() as conn:
        conn.execute("UPDATE ideas SET archived = 1, updated_at = ? WHERE id = ?", (now_iso(), idea_id))
        _create_event(conn, idea_id, EventType.EDIT, None, None, "Idea archived", None)


def transition_idea(idea_id: str, payload: TransitionRequest) -> dict:
    idea = get_idea_by_id(idea_id)
    current_status = idea["current_status"]
    to_status = payload.to_status.value

    # 1) Same status forbidden
    if to_status == current_status:
        raise ValueError("Transition vers le même statut interdite")

    # 2) Must be allowed from current status
    if to_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValueError("Transition non autorisée")

    comment = payload.comment.strip()
    reason_code = payload.reason_code.value if payload.reason_code else None

    # 3) Required fields for target status
    if to_status in REQUIRED_COMMENT_STATUSES and not comment:
        raise ValueError("comment obligatoire pour ce statut")

    if to_status in REQUIRED_REASON_STATUS:
        allowed_reason_codes = REQUIRED_REASON_STATUS[to_status]
        if not reason_code:
            raise ValueError("reason_code obligatoire pour ce statut")
        if reason_code not in allowed_reason_codes:
            raise ValueError("reason_code invalide pour ce statut")
    elif reason_code is not None:
        raise ValueError("reason_code interdit pour ce statut")

    if to_status == "EN_VEILLE":
        if not payload.revisit_at:
            raise ValueError("revisit_at obligatoire pour EN_VEILLE")
        revisit_at = payload.revisit_at.isoformat()
    else:
        revisit_at = idea.get("revisit_at")

    timestamp = now_iso()
    with get_connection() as conn:
        conn.execute(
            "UPDATE ideas SET current_status = ?, revisit_at = ?, updated_at = ? WHERE id = ?",
            (to_status, revisit_at, timestamp, idea_id),
        )
        _create_event(
            conn,
            idea_id,
            EventType.TRANSITION,
            current_status,
            to_status,
            comment,
            reason_code,
        )

    return get_idea_by_id(idea_id)


def list_ideas(
    include_archived: bool = False,
    status: str | None = None,
    domain: str | None = None,
    tags: list[str] | None = None,
    stale: bool | None = None,
    revisit_before: str | None = None,
    sort: str = "created_at",
    order: Order = "desc",
) -> list[dict]:
    where: list[str] = []
    params: list[str | int] = []

    if not include_archived:
        where.append("ideas.archived = 0")
    if status:
        where.append("ideas.current_status = ?")
        params.append(status)
    if domain:
        where.append("ideas.domain = ?")
        params.append(domain)
    if revisit_before:
        where.append("ideas.revisit_at IS NOT NULL AND ideas.revisit_at <= ?")
        params.append(revisit_before)

    if stale is True:
        where.append("datetime(last_activity) <= datetime('now', '-30 day')")

    if tags:
        for tag in tags:
            where.append("EXISTS (SELECT 1 FROM json_each(ideas.tags) WHERE value = ?)")
            params.append(tag)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sort_column = SORT_COLUMNS.get(sort, "ideas.created_at")
    sort_order = "ASC" if order == "asc" else "DESC"

    query = f"""
    WITH events_max AS (
      SELECT idea_id, MAX(created_at) AS max_event_at
      FROM idea_events
      GROUP BY idea_id
    )
    SELECT
        ideas.*,
        MAX(ideas.updated_at, COALESCE(events_max.max_event_at, ideas.updated_at)) AS last_activity
    FROM ideas
    LEFT JOIN events_max ON events_max.idea_id = ideas.id
    {where_sql}
    ORDER BY {sort_column} {sort_order}
    """

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [_row_to_dict(row) for row in rows]


def list_events(idea_id: str) -> list[dict]:
    _ = get_idea_by_id(idea_id)
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM idea_events WHERE idea_id = ? ORDER BY created_at ASC",
            (idea_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def _row_to_dict(row) -> dict:
    data = dict(row)
    data["tags"] = json.loads(data.get("tags") or "[]")
    data["archived"] = bool(data.get("archived"))
    data.pop("last_activity", None)
    return data
