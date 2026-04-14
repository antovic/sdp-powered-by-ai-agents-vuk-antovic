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
