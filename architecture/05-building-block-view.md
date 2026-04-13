# Chapter 5: Building Block View

## Level 1 — System

The system is a single Python application with four internal containers:
- **CLI** — entry point, reads input
- **Command Parser** — tokenises command string
- **Rover Engine** — executes commands against rover state
- **Grid** — enforces boundaries and obstacles

See diagram: `diagrams/c4-container.puml`

## Level 2 — Rover Engine Components

See diagram: `diagrams/c4-component-rover-engine.puml`

| Component | Responsibility |
|-----------|---------------|
| CommandHandler | Dispatches each command to the correct handler |
| Mover | Computes new (x, y) for F/B commands |
| Turner | Computes new heading for L/R commands |
| RoverState | Immutable dataclass holding position and heading |
