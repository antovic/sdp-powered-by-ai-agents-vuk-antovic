# Chapter 10: Quality Requirements

## Quality Tree

| Quality | Scenario | Measure |
|---------|----------|---------|
| Correctness | Given any valid command string, rover ends at the correct position | 100% of unit tests pass |
| Extensibility | Adding a new command requires no changes to existing classes | New command added in < 30 min |
| Testability | All components testable without mocks or I/O | Unit test coverage ≥ 90% |
| Robustness | Invalid input produces a clear error, not a crash | No unhandled exceptions on bad input |
