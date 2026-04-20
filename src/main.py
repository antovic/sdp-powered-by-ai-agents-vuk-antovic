"""Mars Rover CLI — demo entry point."""
from src.rover import CommandParser, Grid, Mover, Turner, RoverState, Heading, ObstacleError


def run(command_string: str, state: RoverState, grid: Grid) -> RoverState:
    parser = CommandParser()
    turner = Turner()
    mover = Mover(grid)
    for cmd in parser.parse(command_string):
        try:
            if cmd in ("L", "R"):
                state = turner.turn(state, cmd)
            else:
                state = mover.move(state, cmd)
        except ObstacleError as e:
            s = e.last_safe_state
            print(f"  Obstacle! Stopped at ({s.x}, {s.y}, {s.heading.value})")
            return e.last_safe_state
    return state


if __name__ == "__main__":
    grid = Grid(width=5, height=5, obstacles={(2, 2)})
    state = RoverState(x=0, y=0, heading=Heading.NORTH)

    examples = [
        ("FFRFF", "Move forward twice, turn right, move forward twice — hits obstacle at (2,2)"),
        ("LLLL",  "Full 360° left rotation — returns to NORTH"),
        ("FF",    "Move forward twice — stops at (0, 2)"),
    ]

    print("=== Mars Rover Demo ===")
    print(f"Grid: 5x5  |  Obstacle at (2,2)\n")
    for commands, description in examples:
        result = run(commands, RoverState(x=0, y=0, heading=Heading.NORTH), grid)
        print(f"  {commands:8s} → ({result.x}, {result.y}, {result.heading.value})  # {description}")
    print()
