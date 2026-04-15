# Chapter 1: Introduction and Goals

## Purpose

The Mars Rover kata simulates a rover on a grid-based planet surface. The system accepts a sequence of commands (`F`, `B`, `L`, `R`) and moves the rover accordingly, respecting grid boundaries and obstacles.

## Quality Goals

| Priority | Quality Goal | Motivation |
|----------|-------------|------------|
| 1 | Correctness | Commands must produce accurate position and heading changes |
| 2 | Extensibility | New commands or grid types should be easy to add |
| 3 | Testability | All logic must be unit-testable in isolation |

## Stakeholders

| Role | Expectation |
|------|-------------|
| Mission Controller | Reliable command execution and accurate position reporting |
| Developer | Clean, maintainable codebase with clear separation of concerns |
