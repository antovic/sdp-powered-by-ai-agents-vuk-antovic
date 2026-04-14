# WORLD Domain — User Stories

---

# WORLD-STORY-001: Detect and report an obstacle [SUPPORTING]

## Original Story

AS A mission controller
I WANT the rover to stop and report its last safe position when it detects an obstacle
SO THAT I know the rover is safe and can issue new commands from that position

**Architecture Reference**: Chapter 5 — Building Block View (Grid component); Chapter 6 — Runtime View (Scenario 2: Obstacle Detected); Chapter 8 — Cross-cutting Concepts (Error Handling)

### SCENARIO 1: Rover stops before an obstacle

**Scenario ID**: WORLD-STORY-001-S1

**GIVEN**
* the rover is at position (0, 0) facing North
* an obstacle exists at (0, 1)

**WHEN**
* the mission controller submits the command `F`

**THEN**
* the rover does not move to (0, 1)
* the system reports `ObstacleError` with last safe position `(0, 0, NORTH)`

### SCENARIO 2: Rover completes safe commands before hitting obstacle

**Scenario ID**: WORLD-STORY-001-S2

**GIVEN**
* the rover is at position (0, 0) facing North
* an obstacle exists at (0, 2)

**WHEN**
* the mission controller submits `FF`

**THEN**
* the rover moves to (0, 1) on the first `F`
* the rover stops at (0, 1) on the second `F` and reports `ObstacleError` with last safe position `(0, 1, NORTH)`

---

## BE Sub-stories

### WORLD-BE-001.1: Raise ObstacleError with last safe position

AS A rover engine
I WANT the Grid component to raise an `ObstacleError` containing the last safe `RoverState` when a move would collide with an obstacle
SO THAT the engine can halt execution and return a meaningful response

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 5 — Building Block View (Grid component); Chapter 8 — Cross-cutting Concepts (Error Handling)

#### SCENARIO 1: ObstacleError contains last safe state

**Scenario ID**: WORLD-BE-001.1-S1

**GIVEN**
* the rover is at `RoverState(x=0, y=1, heading=NORTH)`
* an obstacle exists at `(0, 2)`

**WHEN**
* the Mover asks the Grid to validate the move to `(0, 2)`

**THEN**
* the Grid raises `ObstacleError` with `last_safe_state = RoverState(x=0, y=1, heading=NORTH)`

---

## INFRA Sub-stories

### WORLD-INFRA-001.1: Lambda deployment — obstacle detection in rover Lambda

AS A platform engineer
I WANT obstacle detection logic deployed as part of the rover Lambda
SO THAT obstacle checks happen in-process without a network call

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda returns obstacle report

**Scenario ID**: WORLD-INFRA-001.1-S1

**GIVEN**
* the rover Lambda is deployed with the Grid component
* the grid is initialised with an obstacle at (0, 1)

**WHEN**
* the Lambda is invoked with `{"commands": "F"}` and rover at (0, 0) facing North

**THEN**
* the Lambda returns HTTP 200 with body `{"status": "obstacle", "lastSafePosition": {"x": 0, "y": 0, "heading": "NORTH"}}`

---

### WORLD-INFRA-001.2: Data store — obstacle map in DynamoDB

AS A platform engineer
I WANT the grid's obstacle positions stored in a DynamoDB table
SO THAT the Lambda can load the current obstacle map on each invocation without hardcoding it

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View; Chapter 5 — Building Block View (Grid)

#### SCENARIO 1: Obstacle map is loaded from DynamoDB

**Scenario ID**: WORLD-INFRA-001.2-S1

**GIVEN**
* a DynamoDB table `rover-grid` contains an item `{gridId: "mars-1", obstacles: [[0,1],[3,4]]}`

**WHEN**
* the Lambda initialises the Grid component

**THEN**
* the Grid is constructed with obstacles at `(0,1)` and `(3,4)`

---

### WORLD-INFRA-001.3: Event handling — obstacle detected event

AS A platform engineer
I WANT an `ObstacleDetected` event published to EventBridge whenever the rover is blocked
SO THAT mission control systems can react to obstacle events asynchronously

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 6 — Runtime View (Scenario 2: Obstacle Detected)

#### SCENARIO 1: ObstacleDetected event is published

**Scenario ID**: WORLD-INFRA-001.3-S1

**GIVEN**
* the Lambda has caught an `ObstacleError`

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* an `ObstacleDetected` event appears with `lastSafePosition`, `attemptedPosition`, and `roverId`

---

### WORLD-INFRA-001.4: Monitoring and alarms — obstacle detection rate

AS A platform engineer
I WANT a CloudWatch alarm on the rate of `ObstacleDetected` events
SO THAT a sudden increase in obstacle collisions is visible and alertable

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 10 — Quality Requirements; Chapter 11 — Risks and Technical Debts

#### SCENARIO 1: High obstacle rate triggers alarm

**Scenario ID**: WORLD-INFRA-001.4-S1

**GIVEN**
* more than 5 `ObstacleDetected` events occur within 1 minute

**WHEN**
* CloudWatch evaluates the metric filter on the EventBridge log

**THEN**
* the alarm transitions to `ALARM` and notifies the on-call SNS topic

---

# WORLD-STORY-002: Enforce grid boundaries [SUPPORTING]

## Original Story

AS A mission controller
I WANT the rover to wrap around at grid boundaries
SO THAT it never moves to an undefined position outside the grid

**Architecture Reference**: Chapter 5 — Building Block View (Grid component); Chapter 2 — Constraints

### SCENARIO 1: Rover wraps at northern boundary

**Scenario ID**: WORLD-STORY-002-S1

**GIVEN**
* the grid is 5×5
* the rover is at position (0, 4) facing North

**WHEN**
* the mission controller submits `F`

**THEN**
* the rover wraps to position (0, 0)

### SCENARIO 2: Rover wraps at eastern boundary

**Scenario ID**: WORLD-STORY-002-S2

**GIVEN**
* the grid is 5×5
* the rover is at position (4, 0) facing East

**WHEN**
* the mission controller submits `F`

**THEN**
* the rover wraps to position (0, 0)

---

## BE Sub-stories

### WORLD-BE-002.1: Grid enforces boundary wrapping

AS A rover engine
I WANT the Grid component to wrap coordinates using modulo arithmetic
SO THAT the rover always stays within the defined grid dimensions

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 5 — Building Block View (Grid component)

#### SCENARIO 1: Y coordinate wraps at grid height

**Scenario ID**: WORLD-BE-002.1-S1

**GIVEN**
* the grid has height 5
* the Mover computes a new y of 5

**WHEN**
* the Grid normalises the coordinate

**THEN**
* the resulting y is `0` (5 mod 5)

---

## INFRA Sub-stories

### WORLD-INFRA-002.1: Lambda deployment — boundary logic in rover Lambda

AS A platform engineer
I WANT boundary enforcement deployed as part of the rover Lambda
SO THAT no out-of-bounds position is ever persisted or returned

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda wraps boundary correctly

**Scenario ID**: WORLD-INFRA-002.1-S1

**GIVEN**
* the Lambda is deployed with a 5×5 grid
* the rover is at (0, 4) facing North

**WHEN**
* invoked with `{"commands": "F"}`

**THEN**
* the response contains `{"x": 0, "y": 0, "heading": "NORTH"}`

---

### WORLD-INFRA-002.2: Data store — grid dimensions in DynamoDB

AS A platform engineer
I WANT the grid dimensions stored in DynamoDB alongside the obstacle map
SO THAT the Lambda can load both grid size and obstacles from a single record

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Grid dimensions are loaded from DynamoDB

**Scenario ID**: WORLD-INFRA-002.2-S1

**GIVEN**
* the `rover-grid` DynamoDB item contains `{width: 5, height: 5}`

**WHEN**
* the Lambda initialises the Grid

**THEN**
* the Grid is constructed with `width=5` and `height=5`

---

### WORLD-INFRA-002.3: Event handling — boundary wrap event

AS A platform engineer
I WANT a `BoundaryWrapped` event published to EventBridge when the rover wraps around the grid
SO THAT mission control can track wrap-around behaviour for telemetry

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 6 — Runtime View

#### SCENARIO 1: BoundaryWrapped event is published

**Scenario ID**: WORLD-INFRA-002.3-S1

**GIVEN**
* the rover has wrapped from (0, 4) to (0, 0)

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `BoundaryWrapped` event appears with `fromPosition`, `toPosition`, and `roverId`

---

### WORLD-INFRA-002.4: Monitoring and alarms — boundary wrap rate

AS A platform engineer
I WANT a CloudWatch metric tracking the frequency of boundary wraps
SO THAT unusual wrap patterns are visible in the operations dashboard

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 10 — Quality Requirements

#### SCENARIO 1: Wrap metric is emitted

**Scenario ID**: WORLD-INFRA-002.4-S1

**GIVEN**
* the Lambda has processed a command that caused a boundary wrap

**WHEN**
* the Lambda publishes a custom CloudWatch metric `BoundaryWrapCount`

**THEN**
* the metric appears in the `MarsRover` CloudWatch namespace with value `1`

---

# WORLD-STORY-003: Report current rover position [SUPPORTING]

## Original Story

AS A mission controller
I WANT to query the rover's current position and heading without issuing movement commands
SO THAT I can verify its state before planning the next command sequence

**Architecture Reference**: Chapter 5 — Building Block View (RoverState); Chapter 8 — Cross-cutting Concepts (State Management)

### SCENARIO 1: Query returns current position

**Scenario ID**: WORLD-STORY-003-S1

**GIVEN**
* the rover is at position (2, 3) facing East

**WHEN**
* the mission controller queries the rover state

**THEN**
* the system returns `(2, 3, EAST)`

---

## BE Sub-stories

### WORLD-BE-003.1: Read rover state without mutation

AS A rover engine
I WANT a read-only query operation that returns the current `RoverState`
SO THAT position can be retrieved without side effects

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 5 — Building Block View (RoverState)

#### SCENARIO 1: State query returns current RoverState

**Scenario ID**: WORLD-BE-003.1-S1

**GIVEN**
* the current `RoverState` is `(x=2, y=3, heading=EAST)`

**WHEN**
* the engine processes a state query

**THEN**
* it returns `RoverState(x=2, y=3, heading=EAST)` without modifying state

---

## INFRA Sub-stories

### WORLD-INFRA-003.1: Lambda deployment — state query handler

AS A platform engineer
I WANT a GET endpoint deployed as a Lambda function to query rover state
SO THAT position can be retrieved via HTTP without issuing commands

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: GET request returns rover state

**Scenario ID**: WORLD-INFRA-003.1-S1

**GIVEN**
* the rover Lambda is deployed with a state query handler
* the rover is at position (2, 3) facing East

**WHEN**
* a GET request is sent to `/rover/state`

**THEN**
* it returns HTTP 200 with body `{"x": 2, "y": 3, "heading": "EAST"}`

---

### WORLD-INFRA-003.2: Data store — read rover state from DynamoDB

AS A platform engineer
I WANT the state query handler to read from the DynamoDB rover state table
SO THAT the current position is retrieved from persistent storage

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: State is read from DynamoDB

**Scenario ID**: WORLD-INFRA-003.2-S1

**GIVEN**
* the DynamoDB table contains a record with `x: 2, y: 3, heading: "EAST"`

**WHEN**
* the Lambda queries the table

**THEN**
* it retrieves the record and returns the state

---

### WORLD-INFRA-003.3: Event handling — state query event

AS A platform engineer
I WANT a `StateQueried` event published to EventBridge after each state query
SO THAT telemetry can track query frequency independently

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 6 — Runtime View

#### SCENARIO 1: StateQueried event is published

**Scenario ID**: WORLD-INFRA-003.3-S1

**GIVEN**
* the Lambda has processed a state query

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `StateQueried` event appears with `roverId` and `timestamp`

---

### WORLD-INFRA-003.4: Monitoring and alarms — state query rate

AS A platform engineer
I WANT a CloudWatch metric tracking the frequency of state queries
SO THAT query patterns are visible in the operations dashboard

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 10 — Quality Requirements

#### SCENARIO 1: Query metric is emitted

**Scenario ID**: WORLD-INFRA-003.4-S1

**GIVEN**
* the Lambda has processed a state query

**WHEN**
* the Lambda publishes a custom CloudWatch metric `StateQueryCount`

**THEN**
* the metric appears in the `MarsRover` CloudWatch namespace with value `1`
