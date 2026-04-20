# NAV-BE-001.1: Compute new position for F/B commands
from src.rover import RoverState, Heading, Grid, Mover


def test_nav_be_001_1_s1_mover_returns_0_1_for_f_from_0_0_facing_north():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.NORTH)
    grid = Grid(width=5, height=5)
    mover = Mover(grid)

    # WHEN
    new_state = mover.move(state, "F")

    # THEN
    assert new_state == RoverState(x=0, y=1, heading=Heading.NORTH)


def test_nav_be_001_1_s2_mover_wraps_to_0_4_for_b_from_0_0_facing_north():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.NORTH)
    grid = Grid(width=5, height=5)
    mover = Mover(grid)

    # WHEN
    new_state = mover.move(state, "B")

    # THEN
    assert new_state == RoverState(x=0, y=4, heading=Heading.NORTH)


def test_nav_be_001_1_s3_mover_wraps_to_0_4_for_f_from_0_0_facing_south():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.SOUTH)
    grid = Grid(width=5, height=5)
    mover = Mover(grid)

    # WHEN
    new_state = mover.move(state, "F")

    # THEN
    assert new_state == RoverState(x=0, y=4, heading=Heading.SOUTH)


def test_nav_be_001_1_s4_mover_returns_0_1_for_b_from_0_0_facing_south():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.SOUTH)
    grid = Grid(width=5, height=5)
    mover = Mover(grid)

    # WHEN
    new_state = mover.move(state, "B")

    # THEN
    assert new_state == RoverState(x=0, y=1, heading=Heading.SOUTH)
