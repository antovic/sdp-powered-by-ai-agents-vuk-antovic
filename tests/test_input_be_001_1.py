# INPUT-BE-001.1: Parse a valid command string into a command list
from src.rover import CommandParser


def test_input_be_001_1_s1_valid_string_tokenised_correctly():
    # GIVEN
    parser = CommandParser()

    # WHEN
    commands = parser.parse("FBLR")

    # THEN
    assert commands == ["F", "B", "L", "R"]
