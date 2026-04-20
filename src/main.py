"""Mars Rover interactive CLI."""
import sys
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
            return s
    return state


if __name__ == "__main__":
    grid = Grid(width=5, height=5, obstacles={(2, 2)})
    state = RoverState(x=0, y=0, heading=Heading.NORTH)

    print("=== Mars Rover ===")
    print("Grid: 5x5  |  Obstacle at (2,2)")
    print("Commands: F=forward  B=backward  L=left  R=right  Q=quit")
    print(f"Start: ({state.x}, {state.y}, {state.heading.value})\n")

    for line in sys.stdin:
        commands = line.strip().upper()
        if commands == "Q":
            break
        if not commands:
            continue
        try:
            state = run(commands, state, grid)
            print(f"  → ({state.x}, {state.y}, {state.heading.value})")
        except ValueError as e:
            print(f"  Error: {e}")
