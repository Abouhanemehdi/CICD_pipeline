import re

import pytest

from app.ingestion import transform_record


def test_transform_record_normalizes_values():
    input_record = {
        "id": " 42 ",
        "event_type": "PURCHASE",
        "event_ts": "2026-04-10T10:00:00Z",
    }

    out = transform_record(input_record)

    assert out["id"] == "42"
    assert out["event_type"] == "purchase"
    assert out["event_ts"] == "2026-04-10T10:00:00Z"


@pytest.mark.parametrize(
    "bad_record, expected_msg",
    [
        (
            {"event_type": "click", "event_ts": "2026-04-10T10:00:00Z"},
            "Missing required column(s): id",
        ),
        (
            {"id": "1", "event_type": "", "event_ts": "2026-04-10T10:00:00Z"},
            "event_type cannot be empty",
        ),
        (
            {"id": "1", "event_type": "click", "event_ts": "bad-date"},
            "event_ts must be a valid ISO-8601 datetime",
        ),
    ],
)
def test_transform_record_rejects_invalid_data(bad_record, expected_msg):
    with pytest.raises(ValueError, match=re.escape(expected_msg)):
        transform_record(bad_record)
