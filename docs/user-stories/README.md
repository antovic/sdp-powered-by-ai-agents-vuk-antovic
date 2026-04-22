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
| INPUT-STORY-001 | Submit a command sequence via CLI | INPUT | 1 | [CORE] | ✅ done |
| INPUT-STORY-002 | Reject invalid commands at parse time | INPUT | 4 | [SUPPORTING] | ✅ done |
| INPUT-STORY-003 | Log command execution history | INPUT | 8 | [SUPPORTING] | ✅ done |
| INPUT-STORY-004 | Validate grid configuration at startup | INPUT | 9 | [SUPPORTING] | ✅ done |
| NAV-STORY-001 | Move the rover forward and backward | NAV | 2 | [CORE] | ✅ done |
| NAV-STORY-002 | Turn the rover left and right | NAV | 3 | [CORE] | ✅ done |
| WORLD-STORY-001 | Detect and report an obstacle | WORLD | 5 | [SUPPORTING] | ✅ done |
| WORLD-STORY-002 | Enforce grid boundaries | WORLD | 6 | [SUPPORTING] | ✅ done |
| WORLD-STORY-003 | Report current rover position | WORLD | 7 | [SUPPORTING] | ✅ done |
| WORLD-STORY-004 | Add obstacle to grid at runtime | WORLD | 10 | [SUPPORTING] | ✅ done |
| WORLD-STORY-005 | Remove obstacle from grid | WORLD | 11 | [SUPPORTING] | ✅ done |

**Total stories**: 11
**Core stories (20% → 80% value)**: INPUT-STORY-001, NAV-STORY-001, NAV-STORY-002 — 3 stories (27% of inventory marked core)

> Note: This kata has a small story set. Core stories are those that directly implement primary user-facing behaviour per Chapter 1 quality goals.

---

## Pareto Progress

| Metric | Value |
|--------|-------|
| Core stories total | 3 |
| Core stories complete | 3 |
| Pareto progress | 3 of 3 core stories complete (100% of 80% value delivered) |

---

## File Map

| File | Stories |
|------|---------|
| `docs/user-stories/input.md` | INPUT-STORY-001, INPUT-STORY-002, INPUT-STORY-003, INPUT-STORY-004 |
| `docs/user-stories/navigation.md` | NAV-STORY-001, NAV-STORY-002 |
| `docs/user-stories/world.md` | WORLD-STORY-001, WORLD-STORY-002, WORLD-STORY-003, WORLD-STORY-004, WORLD-STORY-005 |
