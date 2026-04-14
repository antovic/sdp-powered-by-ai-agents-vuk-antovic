# User Story Inventory

## Domains (Bounded Contexts)

Extracted from `architecture/04-solution-strategy.md` — Chapter 4: Solution Strategy.

| Domain | Description |
|--------|-------------|
| INPUT | CLI entry point and command parsing |
| NAV | Rover movement and heading logic |
| WORLD | Grid boundaries and obstacle detection |

---

## Story Inventory

| Story ID | Title | Domain | Priority | Type | Status |
|----------|-------|--------|----------|------|--------|
| INPUT-STORY-001 | Submit a command sequence via CLI | INPUT | 1 | [CORE] | ⬜ pending |
| INPUT-STORY-002 | Reject invalid commands at parse time | INPUT | 4 | [SUPPORTING] | ⬜ pending |
| NAV-STORY-001 | Move the rover forward and backward | NAV | 2 | [CORE] | ⬜ pending |
| NAV-STORY-002 | Turn the rover left and right | NAV | 3 | [CORE] | ⬜ pending |
| WORLD-STORY-001 | Detect and report an obstacle | WORLD | 5 | [SUPPORTING] | ⬜ pending |
| WORLD-STORY-002 | Enforce grid boundaries | WORLD | 6 | [SUPPORTING] | ⬜ pending |
| WORLD-STORY-003 | Report current rover position | WORLD | 7 | [SUPPORTING] | ⬜ pending |

**Total stories**: 7
**Core stories (20% → 80% value)**: INPUT-STORY-001, NAV-STORY-001, NAV-STORY-002 — 3 stories (43% of inventory marked core; justified for small story set per agent rules)

> Note: This kata has a small story set. Core stories are those that directly implement primary user-facing behaviour per Chapter 1 quality goals.

---

## Pareto Progress

| Metric | Value |
|--------|-------|
| Core stories total | 3 |
| Core stories complete | 0 |
| Pareto progress | 0 of 3 core stories complete (0% of 80% value delivered) |

---

## File Map

| File | Stories |
|------|---------|
| `docs/user-stories/input.md` | INPUT-STORY-001, INPUT-STORY-002 |
| `docs/user-stories/navigation.md` | NAV-STORY-001, NAV-STORY-002 |
| `docs/user-stories/world.md` | WORLD-STORY-001, WORLD-STORY-002, WORLD-STORY-003 |
