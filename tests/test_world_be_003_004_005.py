# WORLD-BE-003.1 / 004.1 / 005.1: RoverState query, add/remove obstacle
from src.rover import RoverState, Heading, Grid


def test_world_be_003_1_s1_state_query_returns_rover_state_without_mutation():
    # GIVEN
    state = RoverState(x=2, y=3, heading=Heading.EAST)

    # WHEN
    result = state

    # THEN
    assert result == RoverState(x=2, y=3, heading=Heading.EAST)


def test_world_be_004_1_s1_grid_state_includes_new_obstacle():
    # GIVEN
    grid = Grid(width=5, height=5, obstacles={(0, 1)})

    # WHEN
    grid.add_obstacle(2, 3)

    # THEN
    assert (2, 3) in grid.obstacles


def test_world_be_005_1_s1_grid_state_excludes_removed_obstacle():
    # GIVEN
    grid = Grid(width=5, height=5, obstacles={(0, 1), (2, 3)})

    # WHEN
    grid.remove_obstacle(2, 3)

    # THEN
    assert (2, 3) not in grid.obstacles
    assert (0, 1) in grid.obstacles
