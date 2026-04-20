# Chapter 4: Solution Strategy

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.12 | Course standard, fast iteration |
| Architecture style | Layered (CLI → Parser → Engine → Grid) | Clear separation of concerns |
| State management | Immutable dataclass per step | Predictable, easy to test |
| Command pattern | Each command is a callable object | Open/closed principle — new commands without modifying engine |

## Bounded Contexts

1. **Input** — CLI and command parsing
2. **Navigation** — Rover movement and heading logic
3. **World** — Grid boundaries and obstacle detection
