# Chapter 8: Cross-cutting Concepts

## Error Handling

- Invalid commands raise `ValueError` with a descriptive message at parse time
- Obstacle collisions raise `ObstacleError` containing the last safe position
- All errors propagate to the CLI layer which formats them for output

## Logging

- No runtime logging required for the kata
- Debug output can be enabled via `--verbose` flag printing each command step

## Testability

- All components are pure functions or stateless classes — no mocks needed for unit tests
- `RoverState` is an immutable dataclass, making assertions straightforward

## Input Validation

- Command parser rejects any character outside `{F, B, L, R}` immediately
- Grid size and obstacle positions are validated at construction time
