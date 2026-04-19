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

### INPUT-INFRA-001.1: Docker build — CLI component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the CLI and Command Parser components present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with CLI component

**Scenario ID**: INPUT-INFRA-001.1-S1

**GIVEN**
* the CLI and Command Parser source files are present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0
* the image `kata-tests` is available locally

---

### INPUT-INFRA-001.2: Test execution — CLI tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the CLI and Command Parser test suite
SO THAT input handling is verified inside the container

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CLI tests pass inside Docker

**Scenario ID**: INPUT-INFRA-001.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all INPUT-BE-001 tests
* the container exits with code 0

---

### INPUT-INFRA-001.3: Dependencies — CLI dependencies installed

AS A platform engineer
I WANT all packages required by the CLI component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all CLI dependencies

**Scenario ID**: INPUT-INFRA-001.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the CLI component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error
* the CLI module imports successfully inside the container

---

### INPUT-INFRA-001.4: CI verification — CLI pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the CLI component
SO THAT every push verifies the CLI tests pass in Docker

**Parent**: INPUT-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for CLI component

**Scenario ID**: INPUT-INFRA-001.4-S1

**GIVEN**
* a push is made to the feature branch containing CLI changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### INPUT-INFRA-002.1: Docker build — validation component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the validation logic present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with validation component

**Scenario ID**: INPUT-INFRA-002.1-S1

**GIVEN**
* the Command Parser validation source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### INPUT-INFRA-002.2: Test execution — validation tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the validation test suite
SO THAT input rejection logic is verified inside the container

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Validation tests pass inside Docker

**Scenario ID**: INPUT-INFRA-002.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all INPUT-BE-002 tests
* the container exits with code 0

---

### INPUT-INFRA-002.3: Dependencies — validation dependencies installed

AS A platform engineer
I WANT all packages required by the validation component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all validation dependencies

**Scenario ID**: INPUT-INFRA-002.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the validation component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### INPUT-INFRA-002.4: CI verification — validation pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the validation component
SO THAT every push verifies the validation tests pass in Docker

**Parent**: INPUT-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for validation component

**Scenario ID**: INPUT-INFRA-002.4-S1

**GIVEN**
* a push is made to the feature branch containing validation changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### INPUT-INFRA-003.1: Docker build — history component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the history query component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with history component

**Scenario ID**: INPUT-INFRA-003.1-S1

**GIVEN**
* the history query source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### INPUT-INFRA-003.2: Test execution — history tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the history query test suite
SO THAT audit log logic is verified inside the container

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: History tests pass inside Docker

**Scenario ID**: INPUT-INFRA-003.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all INPUT-BE-003 tests
* the container exits with code 0

---

### INPUT-INFRA-003.3: Dependencies — history dependencies installed

AS A platform engineer
I WANT all packages required by the history component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all history dependencies

**Scenario ID**: INPUT-INFRA-003.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the history component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### INPUT-INFRA-003.4: CI verification — history pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the history component
SO THAT every push verifies the history tests pass in Docker

**Parent**: INPUT-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for history component

**Scenario ID**: INPUT-INFRA-003.4-S1

**GIVEN**
* a push is made to the feature branch containing history changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### INPUT-INFRA-004.1: Docker build — grid validation component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the grid validation component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with grid validation component

**Scenario ID**: INPUT-INFRA-004.1-S1

**GIVEN**
* the Grid validation source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### INPUT-INFRA-004.2: Test execution — grid validation tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the grid validation test suite
SO THAT configuration validation logic is verified inside the container

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Grid validation tests pass inside Docker

**Scenario ID**: INPUT-INFRA-004.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all INPUT-BE-004 tests
* the container exits with code 0

---

### INPUT-INFRA-004.3: Dependencies — grid validation dependencies installed

AS A platform engineer
I WANT all packages required by the grid validation component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all grid validation dependencies

**Scenario ID**: INPUT-INFRA-004.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Grid component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### INPUT-INFRA-004.4: CI verification — grid validation pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the grid validation component
SO THAT every push verifies the validation tests pass in Docker

**Parent**: INPUT-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for grid validation component

**Scenario ID**: INPUT-INFRA-004.4-S1

**GIVEN**
* a push is made to the feature branch containing Grid validation changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN
