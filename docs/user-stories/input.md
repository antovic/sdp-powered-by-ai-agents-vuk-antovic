# INPUT Domain — User Stories

---

# INPUT-STORY-001: Submit a command sequence via CLI [CORE]

## Original Story

AS A mission controller
I WANT to submit a sequence of commands (`F`, `B`, `L`, `R`) via the CLI
SO THAT the rover executes them and reports its final position and heading

**Architecture Reference**: Chapter 3 — System Scope and Context; Chapter 5 — Building Block View (CLI component)

### SCENARIO 1: Valid command sequence produces final position

**Scenario ID**: INPUT-STORY-001-S1

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits the command string `FFRFF`

**THEN**
* the CLI outputs the final position `(2, 2, EAST)`

### SCENARIO 2: Empty command string returns initial position

**Scenario ID**: INPUT-STORY-001-S2

**GIVEN**
* the rover is at position (0, 0) facing North

**WHEN**
* the mission controller submits an empty command string

**THEN**
* the CLI outputs `(0, 0, NORTH)` unchanged

---

## BE Sub-stories

### INPUT-BE-001.1: Parse a valid command string into a command list

AS A rover engine
I WANT to receive a parsed list of command objects from the Command Parser
SO THAT I can execute each command without knowing the raw input format

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 5 — Building Block View (Command Parser component)

#### SCENARIO 1: Valid string is tokenised correctly

**Scenario ID**: INPUT-BE-001.1-S1

**GIVEN**
* the Command Parser receives the string `FBLR`

**WHEN**
* the parser tokenises the string

**THEN**
* it returns a list of four command objects: `[Forward, Backward, Left, Right]`

---

## INFRA Sub-stories

### INPUT-INFRA-001.1: Lambda deployment — CLI handler

AS A platform engineer
I WANT the CLI entry point deployed as an AWS Lambda function
SO THAT command sequences can be submitted via an API without a running server

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda executes on invocation

**Scenario ID**: INPUT-INFRA-001.1-S1

**GIVEN**
* the Lambda function is deployed with the rover package

**WHEN**
* it is invoked with a JSON payload `{"commands": "FFRFF"}` and rover at (0, 0) facing North

**THEN**
* it returns HTTP 200 with body `{"x": 2, "y": 2, "heading": "EAST"}`

---

### INPUT-INFRA-001.2: Data store — command audit log (DynamoDB)

AS A platform engineer
I WANT each command sequence and its result stored in a DynamoDB table
SO THAT mission history is auditable

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View; Chapter 8 — Cross-cutting Concepts

#### SCENARIO 1: Successful execution is persisted

**Scenario ID**: INPUT-INFRA-001.2-S1

**GIVEN**
* the Lambda has processed a command sequence successfully

**WHEN**
* the handler writes the result to DynamoDB

**THEN**
* a record exists with `commandString`, `finalPosition`, and `timestamp` attributes

---

### INPUT-INFRA-001.3: Event handling — command received event

AS A platform engineer
I WANT a `CommandReceived` event published to EventBridge after each invocation
SO THAT downstream consumers (e.g., monitoring) can react without coupling to the Lambda

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 6 — Runtime View (Scenario 1)

#### SCENARIO 1: Event is published on successful parse

**Scenario ID**: INPUT-INFRA-001.3-S1

**GIVEN**
* the Lambda has successfully parsed a command string

**WHEN**
* the handler publishes to the EventBridge bus

**THEN**
* a `CommandReceived` event appears on the bus with the command string and rover ID

---

### INPUT-INFRA-001.4: Monitoring and alarms — CLI Lambda

AS A platform engineer
I WANT CloudWatch alarms on the CLI Lambda's error rate and duration
SO THAT I am alerted when command processing degrades

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 10 — Quality Requirements; Chapter 11 — Risks and Technical Debts

#### SCENARIO 1: Error rate alarm triggers

**Scenario ID**: INPUT-INFRA-001.4-S1

**GIVEN**
* the CLI Lambda error rate exceeds 5% over a 5-minute window

**WHEN**
* CloudWatch evaluates the alarm

**THEN**
* the alarm state changes to `ALARM` and an SNS notification is sent

---

# INPUT-STORY-002: Reject invalid commands at parse time [SUPPORTING]

## Original Story

AS A mission controller
I WANT the system to immediately reject any command string containing invalid characters
SO THAT I receive a clear error before the rover attempts to move

**Architecture Reference**: Chapter 8 — Cross-cutting Concepts (Input Validation)

### SCENARIO 1: Invalid character raises an error

**Scenario ID**: INPUT-STORY-002-S1

**GIVEN**
* the rover is ready to accept commands

**WHEN**
* the mission controller submits the string `FXB`

**THEN**
* the CLI outputs an error: `Invalid command 'X'. Allowed commands: F, B, L, R`
* the rover does not move

---

## BE Sub-stories

### INPUT-BE-002.1: Raise ValueError for unknown command characters

AS A command parser
I WANT to raise a `ValueError` with a descriptive message for any character outside `{F, B, L, R}`
SO THAT invalid input never reaches the rover engine

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 8 — Cross-cutting Concepts (Error Handling)

#### SCENARIO 1: Unknown character raises ValueError

**Scenario ID**: INPUT-BE-002.1-S1

**GIVEN**
* the Command Parser receives the string `FXB`

**WHEN**
* it encounters the character `X`

**THEN**
* it raises `ValueError("Invalid command 'X'. Allowed commands: F, B, L, R")`
* no command objects are returned

---

## INFRA Sub-stories

### INPUT-INFRA-002.1: Lambda deployment — validation error response

AS A platform engineer
I WANT the Lambda to return a structured 400 error response for invalid commands
SO THAT API consumers receive actionable feedback

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Invalid input returns 400

**Scenario ID**: INPUT-INFRA-002.1-S1

**GIVEN**
* the Lambda receives a payload with command string `FXB`

**WHEN**
* the parser raises a `ValueError`

**THEN**
* the Lambda returns HTTP 400 with body `{"error": "Invalid command 'X'. Allowed commands: F, B, L, R"}`

---

### INPUT-INFRA-002.2: Data store — validation errors are not persisted

AS A platform engineer
I WANT validation errors to be discarded without writing to DynamoDB
SO THAT the audit log contains only valid executions

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 8 — Cross-cutting Concepts (Error Handling)

#### SCENARIO 1: Validation error skips DynamoDB write

**Scenario ID**: INPUT-INFRA-002.2-S1

**GIVEN**
* the Lambda receives an invalid command string

**WHEN**
* the parser raises a `ValueError`

**THEN**
* no record is written to the DynamoDB audit table

---

### INPUT-INFRA-002.3: Event handling — validation failure event

AS A platform engineer
I WANT a `CommandRejected` event published to EventBridge on validation failure
SO THAT monitoring can track invalid input rates

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 6 — Runtime View

#### SCENARIO 1: Rejected command publishes event

**Scenario ID**: INPUT-INFRA-002.3-S1

**GIVEN**
* the Lambda has rejected a command string due to an invalid character

**WHEN**
* the error handler publishes to EventBridge

**THEN**
* a `CommandRejected` event appears with the offending string and error message

---

### INPUT-INFRA-002.4: Monitoring and alarms — validation error rate

AS A platform engineer
I WANT a CloudWatch alarm on the rate of `CommandRejected` events
SO THAT a spike in bad input is visible in the operations dashboard

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 10 — Quality Requirements

#### SCENARIO 1: High rejection rate triggers alarm

**Scenario ID**: INPUT-INFRA-002.4-S1

**GIVEN**
* more than 10 `CommandRejected` events occur within 1 minute

**WHEN**
* CloudWatch evaluates the metric filter

**THEN**
* the alarm transitions to `ALARM` and notifies the on-call SNS topic


---

# INPUT-STORY-003: Log command execution history [SUPPORTING]

## Original Story

AS A mission controller
I WANT to query the history of all executed command sequences with their results
SO THAT I can review past rover operations and outcomes

**Architecture Reference**: Chapter 8 — Cross-cutting Concepts (Audit Logging); Chapter 5 — Building Block View (CLI component)

### SCENARIO 1: Query returns command history

**Scenario ID**: INPUT-STORY-003-S1

**GIVEN**
* the audit log contains 3 command executions

**WHEN**
* the mission controller queries the command history

**THEN**
* the system returns a list of 3 records with command strings, timestamps, and final positions

---

## BE Sub-stories

### INPUT-BE-003.1: Retrieve command history from audit log

AS A rover engine
I WANT a query operation that retrieves command execution records ordered by timestamp
SO THAT command history can be presented chronologically

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 8 — Cross-cutting Concepts (Audit Logging)

#### SCENARIO 1: Query returns ordered history

**Scenario ID**: INPUT-BE-003.1-S1

**GIVEN**
* the audit log contains records with timestamps `[T1, T2, T3]`

**WHEN**
* the engine processes a history query

**THEN**
* it returns records ordered by timestamp descending `[T3, T2, T1]`

---

## INFRA Sub-stories

### INPUT-INFRA-003.1: Lambda deployment — history query handler

AS A platform engineer
I WANT a GET endpoint deployed as a Lambda function to query command history
SO THAT audit logs can be retrieved via HTTP

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: GET request returns history

**Scenario ID**: INPUT-INFRA-003.1-S1

**GIVEN**
* the rover Lambda is deployed with a history query handler
* the audit log contains 2 command executions

**WHEN**
* a GET request is sent to `/commands/history`

**THEN**
* it returns HTTP 200 with body `[{"commandString": "FF", "finalPosition": {"x": 0, "y": 2, "heading": "NORTH"}, "timestamp": "2026-04-14T20:00:00Z"}, ...]`

---

### INPUT-INFRA-003.2: Data store — query DynamoDB audit table

AS A platform engineer
I WANT the history handler to query the DynamoDB audit table with a timestamp index
SO THAT command history is retrieved efficiently

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Query uses timestamp index

**Scenario ID**: INPUT-INFRA-003.2-S1

**GIVEN**
* the DynamoDB audit table has a GSI on `timestamp`

**WHEN**
* the Lambda queries the table

**THEN**
* it uses the GSI to retrieve records ordered by timestamp

---

### INPUT-INFRA-003.3: Event handling — history queried event

AS A platform engineer
I WANT a `HistoryQueried` event published to EventBridge after each history query
SO THAT audit access patterns are tracked

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 6 — Runtime View

#### SCENARIO 1: HistoryQueried event is published

**Scenario ID**: INPUT-INFRA-003.3-S1

**GIVEN**
* the Lambda has processed a history query

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `HistoryQueried` event appears with `queryTimestamp` and `recordCount`

---

### INPUT-INFRA-003.4: Monitoring and alarms — history query rate

AS A platform engineer
I WANT a CloudWatch metric tracking history query frequency
SO THAT audit access patterns are visible

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 10 — Quality Requirements

#### SCENARIO 1: Query metric is emitted

**Scenario ID**: INPUT-INFRA-003.4-S1

**GIVEN**
* the Lambda has processed a history query

**WHEN**
* the Lambda publishes a custom CloudWatch metric `HistoryQueryCount`

**THEN**
* the metric appears in the `MarsRover` CloudWatch namespace with value `1`

---

# INPUT-STORY-004: Validate grid configuration at startup [SUPPORTING]

## Original Story

AS A platform engineer
I WANT the system to validate grid dimensions and obstacle coordinates at startup
SO THAT invalid configurations are rejected before accepting commands

**Architecture Reference**: Chapter 2 — Constraints; Chapter 8 — Cross-cutting Concepts (Input Validation)

### SCENARIO 1: Valid configuration passes validation

**Scenario ID**: INPUT-STORY-004-S1

**GIVEN**
* the grid configuration specifies width 5, height 5, and obstacles at `[(0,1), (2,3)]`

**WHEN**
* the system validates the configuration at startup

**THEN**
* validation passes and the system is ready to accept commands

### SCENARIO 2: Invalid obstacle coordinate fails validation

**Scenario ID**: INPUT-STORY-004-S2

**GIVEN**
* the grid configuration specifies width 5, height 5, and an obstacle at `(6,1)` (out of bounds)

**WHEN**
* the system validates the configuration at startup

**THEN**
* validation fails with error `Obstacle at (6,1) is outside grid bounds (5x5)`
* the system does not accept commands

---

## BE Sub-stories

### INPUT-BE-004.1: Validate grid dimensions are positive integers

AS A rover engine
I WANT the Grid component to reject non-positive width or height values
SO THAT the grid is always well-defined

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 2 — Constraints

#### SCENARIO 1: Negative dimension raises ValueError

**Scenario ID**: INPUT-BE-004.1-S1

**GIVEN**
* the grid configuration specifies width -5

**WHEN**
* the Grid validates the configuration

**THEN**
* it raises `ValueError("Grid width must be positive")`

---

### INPUT-BE-004.2: Validate obstacles are within grid bounds

AS A rover engine
I WANT the Grid component to reject obstacle coordinates outside grid dimensions
SO THAT all obstacles are reachable positions

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 2 — Constraints

#### SCENARIO 1: Out-of-bounds obstacle raises ValueError

**Scenario ID**: INPUT-BE-004.2-S1

**GIVEN**
* the grid is 5×5
* an obstacle is specified at `(6,1)`

**WHEN**
* the Grid validates the obstacle list

**THEN**
* it raises `ValueError("Obstacle at (6,1) is outside grid bounds (5x5)")`

---

## INFRA Sub-stories

### INPUT-INFRA-004.1: Lambda deployment — startup validation

AS A platform engineer
I WANT the Lambda to validate grid configuration on cold start
SO THAT invalid configurations prevent the function from becoming ready

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Lambda cold start validates configuration

**Scenario ID**: INPUT-INFRA-004.1-S1

**GIVEN**
* the Lambda is deployed with grid configuration in environment variables

**WHEN**
* the Lambda performs a cold start

**THEN**
* it validates the configuration before accepting requests

---

### INPUT-INFRA-004.2: Data store — load configuration from DynamoDB

AS A platform engineer
I WANT the Lambda to load grid configuration from DynamoDB at startup
SO THAT configuration is centralized and versioned

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Configuration is loaded and validated

**Scenario ID**: INPUT-INFRA-004.2-S1

**GIVEN**
* the DynamoDB config table contains a grid configuration record

**WHEN**
* the Lambda cold starts

**THEN**
* it loads the configuration and validates it before accepting requests

---

### INPUT-INFRA-004.3: Event handling — configuration validated event

AS A platform engineer
I WANT a `ConfigurationValidated` event published to EventBridge on successful startup validation
SO THAT deployment readiness is tracked

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 6 — Runtime View

#### SCENARIO 1: ConfigurationValidated event is published

**Scenario ID**: INPUT-INFRA-004.3-S1

**GIVEN**
* the Lambda has successfully validated its configuration

**WHEN**
* the event handler publishes to EventBridge

**THEN**
* a `ConfigurationValidated` event appears with `gridDimensions` and `obstacleCount`

---

### INPUT-INFRA-004.4: Monitoring and alarms — validation failure rate

AS A platform engineer
I WANT a CloudWatch alarm on configuration validation failures
SO THAT invalid deployments are immediately visible

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 10 — Quality Requirements

#### SCENARIO 1: Validation failure triggers alarm

**Scenario ID**: INPUT-INFRA-004.4-S1

**GIVEN**
* the Lambda has failed configuration validation on cold start

**WHEN**
* CloudWatch evaluates the error metric

**THEN**
* the alarm transitions to `ALARM` and notifies the on-call SNS topic
