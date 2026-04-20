# NAV-BE-002.1: Compute new heading for L/R commands
from src.rover import RoverState, Heading, Turner


def test_nav_be_002_1_s1_turner_returns_west_for_l_from_north():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.NORTH)
    turner = Turner()

    # WHEN
    new_state = turner.turn(state, "L")

    # THEN
    assert new_state == RoverState(x=0, y=0, heading=Heading.WEST)


def test_nav_be_002_1_s2_turner_returns_east_for_r_from_north():
    # GIVEN
    state = RoverState(x=0, y=0, heading=Heading.NORTH)
    turner = Turner()

    # WHEN
    new_state = turner.turn(state, "R")

    # THEN
    assert new_state == RoverState(x=0, y=0, heading=Heading.EAST)
