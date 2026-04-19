# WORLD-BE-002.1: Grid enforces boundary wrapping
from src.rover import Grid


def test_world_be_002_1_s1_y_coordinate_wraps_at_grid_height():
    # GIVEN
    grid = Grid(width=5, height=5)

    # WHEN
    _, y = grid.wrap(0, 5)

    # THEN
    assert y == 0
