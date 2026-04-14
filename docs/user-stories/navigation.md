# NAV Domain — User Stories

---

# NAV-STORY-001: Move the rover forward and backward [CORE]

## Original Story

AS A mission controller
I WANT to move the rover forward and backward with the `F` and `B` commands
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
* the rover moves to `(0, 1)`

### SCENARIO 2: Move backward from North wraps to southern edge

**Scenario ID**: NAV-STORY-001-S2

**GIVEN**
* the rover is at position (0, 0) facing North on a 5×5 grid

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `NORTH`
* the rover moves to `(0, 4)` (wraps to southern edge)

### SCENARIO 3: Move forward towards South wraps to southern edge

**Scenario ID**: NAV-STORY-001-S3

**GIVEN**
* the rover is at position (0, 0) facing South on a 5×5 grid

**WHEN**
* the mission controller submits the command `F`

**THEN**
* the rover's heading is `SOUTH`
* the rover moves to `(0, 4)` (wraps to southern edge)

### SCENARIO 4: Move backward from South moves north

**Scenario ID**: NAV-STORY-001-S4

**GIVEN**
* the rover is at position (0, 0) facing South on a 5×5 grid

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `SOUTH`
* the rover moves to `(0, 1)`

---

## BE Sub-stories

### NAV-BE-001.1: Compute new position for F/B commands

AS A rover engine
I WANT the Mover component to return a new position for each `F` or `B` command
SO THAT movement is computed without mutating rover state

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 5 — Building Block View (Mover component); ADR-003 (immutable state)

#### SCENARIO 1: Mover returns (0, 1) for F from (0, 0) facing NORTH

**Scenario ID**: NAV-BE-001.1-S1

**GIVEN**
* the current `RoverState` is `(x=0, y=0, heading=NORTH)` on a 5×5 grid

**WHEN**
* the Mover processes command `F`

**THEN**
* it returns a new `RoverState` with `(x=0, y=1, heading=NORTH)`

#### SCENARIO 2: Mover wraps to (0, 4) for B from (0, 0) facing NORTH

**Scenario ID**: NAV-BE-001.1-S2

**GIVEN**
* the current `RoverState` is `(x=0, y=0, heading=NORTH)` on a 5×5 grid

**WHEN**
* the Mover processes command `B`

**THEN**
* it returns a new `RoverState` with `(x=0, y=4, heading=NORTH)`

---

## INFRA Sub-stories

### NAV-INFRA-001.1: Lambda deployment — movement handler

AS A platform engineer
I WANT the movement logic (Mover component) packaged and deployed as part of the rover Lambda
SO THAT move commands are executed in a single serverless invocation

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda handles move commands

**Scenario ID**: NAV-INFRA-001.1-S1

**GIVEN**
* the rover Lambda is deployed with the Mover component

**WHEN**
* it is invoked with payload `{"commands": "FF"}`

**THEN**
* it returns the correct final position with HTTP 200

---

### NAV-INFRA-001.2: Data store — rover position in DynamoDB

AS A platform engineer
I WANT the rover's position stored in a DynamoDB state record after each move
SO THAT the full `RoverState` is recoverable between invocations

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View; Chapter 5 — Building Block View (RoverState)

#### SCENARIO 1: Position is persisted after move

**Scenario ID**: NAV-INFRA-001.2-S1

**GIVEN**
* the Lambda has processed an `F` command from `(0, 0, NORTH)`

**WHEN**
* the result is written to DynamoDB

**THEN**
* the record contains `x: 0, y: 1, heading: "NORTH"`

---

### NAV-INFRA-001.3: Event handling — position changed event

AS A platform engineer
I WANT a `PositionChanged` event published to EventBridge after each move command
SO THAT downstream consumers can track rover position changes independently

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 6 — Runtime View (Scenario 1)

#### SCENARIO 1: PositionChanged event is published

**Scenario ID**: NAV-INFRA-001.3-S1

**GIVEN**
* the Lambda has processed a move command

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `PositionChanged` event appears with `previousPosition`, `newPosition`, and `roverId`

---

### NAV-INFRA-001.4: Monitoring and alarms — movement Lambda

AS A platform engineer
I WANT CloudWatch alarms on the movement Lambda's error rate and p99 duration
SO THAT I am alerted when move commands degrade in reliability

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 10 — Quality Requirements (Correctness)

#### SCENARIO 1: Error rate alarm triggers on failures

**Scenario ID**: NAV-INFRA-001.4-S1

**GIVEN**
* the movement Lambda error rate exceeds 1% over a 5-minute window

**WHEN**
* CloudWatch evaluates the alarm

**THEN**
* the alarm transitions to `ALARM` and notifies the on-call SNS topic

---

# NAV-STORY-002: Turn the rover left and right [CORE]

## Original Story

AS A mission controller
I WANT to turn the rover left or right with the `L` and `R` commands
SO THAT I can change its heading before issuing movement commands

**Architecture Reference**: Chapter 5 — Building Block View (Turner component); Chapter 4 — Solution Strategy (command pattern)

### SCENARIO 1: Turn left from North

**Scenario ID**: NAV-STORY-002-S1

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits the command `L`

**THEN**
* the rover's heading is `WEST`
* the rover's position remains `(0, 0)`

### SCENARIO 2: Turn right from North

**Scenario ID**: NAV-STORY-002-S2

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits the command `R`

**THEN**
* the rover's heading is `EAST`
* the rover's position remains `(0, 0)`

### SCENARIO 3: Full 360° left rotation returns to original heading

**Scenario ID**: NAV-STORY-002-S3

**GIVEN**
* the rover is facing North

**WHEN**
* the mission controller submits `LLLL`

**THEN**
* the rover's heading is `NORTH`

---

## BE Sub-stories

### NAV-BE-002.1: Compute new heading for L/R commands

AS A rover engine
I WANT the Turner component to return a new heading for each `L` or `R` command
SO THAT heading changes are computed without mutating rover state

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 5 — Building Block View (Turner component); ADR-003 (immutable state)

#### SCENARIO 1: Turner returns WEST for L from NORTH

**Scenario ID**: NAV-BE-002.1-S1

**GIVEN**
* the current `RoverState` has heading `NORTH`

**WHEN**
* the Turner processes command `L`

**THEN**
* it returns a new `RoverState` with heading `WEST` and unchanged `(x, y)`

#### SCENARIO 2: Turner returns EAST for R from NORTH

**Scenario ID**: NAV-BE-002.1-S2

**GIVEN**
* the current `RoverState` has heading `NORTH`

**WHEN**
* the Turner processes command `R`

**THEN**
* it returns a new `RoverState` with heading `EAST` and unchanged `(x, y)`

---

## INFRA Sub-stories

### NAV-INFRA-002.1: Lambda deployment — navigation handler

AS A platform engineer
I WANT the navigation logic (Mover + Turner) packaged and deployed as part of the rover Lambda
SO THAT turn commands are executed in the same serverless invocation as move commands

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda handles turn commands

**Scenario ID**: NAV-INFRA-002.1-S1

**GIVEN**
* the rover Lambda is deployed with the Turner component

**WHEN**
* it is invoked with payload `{"commands": "LR"}`

**THEN**
* it returns the correct final heading with HTTP 200

---

### NAV-INFRA-002.2: Data store — heading state in DynamoDB

AS A platform engineer
I WANT the rover's heading stored alongside its position in the DynamoDB state record
SO THAT the full `RoverState` is recoverable between invocations

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View; Chapter 5 — Building Block View (RoverState)

#### SCENARIO 1: Heading is persisted after turn

**Scenario ID**: NAV-INFRA-002.2-S1

**GIVEN**
* the Lambda has processed a `L` command from heading `NORTH`

**WHEN**
* the result is written to DynamoDB

**THEN**
* the record contains `heading: "WEST"` alongside `x` and `y`

---

### NAV-INFRA-002.3: Event handling — heading changed event

AS A platform engineer
I WANT a `HeadingChanged` event published to EventBridge after each turn command
SO THAT downstream consumers can track rover orientation changes independently

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 6 — Runtime View (Scenario 1)

#### SCENARIO 1: HeadingChanged event is published

**Scenario ID**: NAV-INFRA-002.3-S1

**GIVEN**
* the Lambda has processed a turn command

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `HeadingChanged` event appears with `previousHeading`, `newHeading`, and `roverId`

---

### NAV-INFRA-002.4: Monitoring and alarms — navigation Lambda

AS A platform engineer
I WANT CloudWatch alarms on the navigation Lambda's error rate and p99 duration
SO THAT I am alerted when turning or movement commands degrade in reliability

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 10 — Quality Requirements (Correctness)

#### SCENARIO 1: Duration alarm triggers on slow execution

**Scenario ID**: NAV-INFRA-002.4-S1

**GIVEN**
* the navigation Lambda p99 duration exceeds 1000ms over a 5-minute window

**WHEN**
* CloudWatch evaluates the alarm

**THEN**
* the alarm transitions to `ALARM` and notifies the on-call SNS topic
