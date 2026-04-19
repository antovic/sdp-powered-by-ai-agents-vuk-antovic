# INPUT-BE-002.1: Raise ValueError for unknown command characters
import pytest
from src.rover import CommandParser


def test_input_be_002_1_s1_unknown_character_raises_value_error():
    # GIVEN
    parser = CommandParser()

    # WHEN / THEN
    with pytest.raises(ValueError, match="Invalid command 'X'. Allowed commands: F, B, L, R"):
        parser.parse("FXB")
