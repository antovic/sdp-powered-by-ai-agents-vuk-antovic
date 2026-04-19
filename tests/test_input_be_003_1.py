# INPUT-BE-003.1: Retrieve command history ordered by timestamp
from src.rover import CommandHistory


def test_input_be_003_1_s1_query_returns_history_in_desc_timestamp_order():
    # GIVEN
    history = CommandHistory()
    history.record("FF", "T1", (0, 2, "NORTH"))
    history.record("LF", "T2", (1, 2, "WEST"))
    history.record("RR", "T3", (1, 2, "EAST"))

    # WHEN
    records = history.query()

    # THEN
    assert [r["timestamp"] for r in records] == ["T3", "T2", "T1"]
