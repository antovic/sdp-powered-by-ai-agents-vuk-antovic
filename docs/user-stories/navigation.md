# NAV Domain — User Stories

---

# NAV-STORY-001: Move the rover forward and backward [CORE]

## Original Story

AS A mission controller
I WANT to turn the rover forward or backwards with the `F` and `B` commands
SO THAT I can travel across the planet surface

**Architecture Reference**: Chapter 5 — Building Block View (Mover component); Chapter 4 — Solution Strategy (command pattern)

### SCENARIO 1: Move forward towards North

**Scenario ID**: NAV-STORY-001-S1

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits the command `F`

**THEN**
* the rover's heading is `NORTH`
* the rover's moves to `(0, 1)`

### SCENARIO 2: Move backwards from North

**Scenario ID**: NAV-STORY-001-S2

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `NORTH`
* the rover's moves to `(0, -1)`

### SCENARIO 3: Move forward towards SOUTH

**Scenario ID**: NAV-STORY-001-S3

**GIVEN**
* the rover is at position (0, 0) facing South

**WHEN**
* the mission controller submits the command `F`

**THEN**
* the rover's heading is `SOUTH`
* the rover's moves to `(0, -1)`

### SCENARIO 4: Move backwards from South

**Scenario ID**: NAV-STORY-001-S4

**GIVEN**
* the rover is at position (0, 0) facing South

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `SOUTH`
* the rover's moves to `(0, 1)`
