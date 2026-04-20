# WORLD-BE-001.1: Raise ObstacleError with last safe position
import pytest
from src.rover import RoverState, Heading, Grid, ObstacleError


def test_world_be_001_1_s1_obstacle_error_contains_last_safe_state():
    # GIVEN
    last_safe = RoverState(x=0, y=1, heading=Heading.NORTH)
    grid = Grid(width=5, height=5, obstacles={(0, 2)})

    # WHEN / THEN
    with pytest.raises(ObstacleError) as exc_info:
        grid.validate_move(0, 2, last_safe)

    assert exc_info.value.last_safe_state == last_safe
