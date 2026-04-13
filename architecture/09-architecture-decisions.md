# Chapter 9: Architecture Decisions

## ADR-001: Python as Implementation Language

**Status:** Accepted

**Context:**
The course requires a consistent language across modules. The kata needs to be runnable without complex setup.

**Decision:**
Use Python 3.12 with no external runtime dependencies.

**Rationale:**
Python is the course standard, has excellent stdlib support, and allows fast iteration. The kata logic does not require performance-critical code.

**Consequences:**
- Positive: Simple setup, readable code, fast test execution
- Negative: Not statically typed by default (mitigated with type hints)

---

## ADR-002: Command Pattern for Rover Commands

**Status:** Accepted

**Context:**
The rover needs to handle multiple command types (F, B, L, R) and potentially new ones in the future.

**Decision:**
Represent each command as a callable object implementing a common interface.

**Rationale:**
Follows the Open/Closed Principle — new commands can be added without modifying the engine. Makes unit testing each command trivial.

**Consequences:**
- Positive: Extensible, testable, decoupled
- Negative: Slight overhead vs a simple if/elif chain (negligible for this scale)

---

## ADR-003: Immutable State with Dataclasses

**Status:** Accepted

**Context:**
Rover state (position, heading) needs to be updated after each command. Mutable state makes debugging and testing harder.

**Decision:**
Use a frozen Python `dataclass` for `RoverState`, returning a new instance on each update.

**Rationale:**
Immutable state eliminates side-effect bugs and makes each command's output independently verifiable.

**Consequences:**
- Positive: Predictable, easy to test, no shared mutable state
- Negative: Slightly more verbose than in-place mutation
