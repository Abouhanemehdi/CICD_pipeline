from __future__ import annotations

from datetime import datetime


REQUIRED_COLUMNS = ("id", "event_type", "event_ts")


def validate_record(record: dict) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in record]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")

    if not str(record["id"]).strip():
        raise ValueError("id cannot be empty")

    if not str(record["event_type"]).strip():
        raise ValueError("event_type cannot be empty")

    ts = str(record["event_ts"]).strip()
    if not ts:
        raise ValueError("event_ts cannot be empty")

    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("event_ts must be a valid ISO-8601 datetime") from exc


def transform_record(record: dict) -> dict:
    validate_record(record)
    normalized = {
        "id": str(record["id"]).strip(),
        "event_type": str(record["event_type"]).strip().lower(),
        "event_ts": str(record["event_ts"]).strip(),
    }
    return normalized
