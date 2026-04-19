from dataclasses import dataclass
from enum import Enum


class Heading(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


@dataclass(frozen=True)
class RoverState:
    x: int
    y: int
    heading: Heading


class ObstacleError(Exception):
    def __init__(self, last_safe_state: "RoverState"):
        self.last_safe_state = last_safe_state


class Grid:
    def __init__(self, width: int, height: int, obstacles: set[tuple[int, int]] = None):
        self.width = width
        self.height = height
        self.obstacles = obstacles or set()

    def wrap(self, x: int, y: int) -> tuple[int, int]:
        return x % self.width, y % self.height

    def validate_move(self, x: int, y: int, last_safe: "RoverState") -> None:
        if (x, y) in self.obstacles:
            raise ObstacleError(last_safe)


class CommandHistory:
    def __init__(self):
        self._records: list[dict] = []

    def record(self, command_string: str, timestamp: str, final_position: tuple) -> None:
        self._records.append({"commandString": command_string, "timestamp": timestamp, "finalPosition": final_position})

    def query(self) -> list[dict]:
        return sorted(self._records, key=lambda r: r["timestamp"], reverse=True)


class CommandParser:
    _VALID = frozenset("FBLR")

    def parse(self, command_string: str) -> list[str]:
        for ch in command_string:
            if ch not in self._VALID:
                raise ValueError(f"Invalid command '{ch}'. Allowed commands: F, B, L, R")
        return list(command_string)


class Turner:
    _LEFT = [Heading.NORTH, Heading.WEST, Heading.SOUTH, Heading.EAST]
    _RIGHT = [Heading.NORTH, Heading.EAST, Heading.SOUTH, Heading.WEST]

    def turn(self, state: RoverState, command: str) -> RoverState:
        seq = self._LEFT if command == "L" else self._RIGHT
        new_heading = seq[(seq.index(state.heading) + 1) % 4]
        return RoverState(x=state.x, y=state.y, heading=new_heading)


class Mover:
    _DELTAS = {
        Heading.NORTH: (0, 1),
        Heading.SOUTH: (0, -1),
        Heading.EAST: (1, 0),
        Heading.WEST: (-1, 0),
    }

    def __init__(self, grid: Grid):
        self.grid = grid

    def move(self, state: RoverState, command: str) -> RoverState:
        dx, dy = self._DELTAS[state.heading]
        if command == "B":
            dx, dy = -dx, -dy
        x, y = self.grid.wrap(state.x + dx, state.y + dy)
        return RoverState(x=x, y=y, heading=state.heading)
