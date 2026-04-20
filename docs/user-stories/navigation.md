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

### SCENARIO 2: Move backward from North

**Scenario ID**: NAV-STORY-001-S2

**GIVEN**
* the rover is at position (0, 0) facing North on a 5×5 grid

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `NORTH`
* the rover moves to `(0, 4)` (boundary wrapping per WORLD-STORY-002)

### SCENARIO 3: Move forward towards South

**Scenario ID**: NAV-STORY-001-S3

**GIVEN**
* the rover is at position (0, 0) facing South on a 5×5 grid

**WHEN**
* the mission controller submits the command `F`

**THEN**
* the rover's heading is `SOUTH`
* the rover moves to `(0, 4)` (boundary wrapping per WORLD-STORY-002)

### SCENARIO 4: Move backward from South

**Scenario ID**: NAV-STORY-001-S4

**GIVEN**
* the rover is at position (0, 0) facing South on a 5×5 grid

**WHEN**
* the mission controller submits the command `B`

**THEN**
* the rover's heading is `SOUTH`
* the rover moves to `(0, 1)` (boundary wrapping per WORLD-STORY-002)

**Dependencies**: WORLD-STORY-002 (boundary wrapping)

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

#### SCENARIO 2: Mover delegates boundary handling for B from (0, 0) facing NORTH

**Scenario ID**: NAV-BE-001.1-S2

**GIVEN**
* the current `RoverState` is `(x=0, y=0, heading=NORTH)`

**WHEN**
* the Mover processes command `B`

**THEN**
* it delegates the resulting coordinate to the Grid component for boundary resolution (see WORLD-STORY-002)

---

## INFRA Sub-stories

### NAV-INFRA-001.1: Docker build — movement component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the Mover component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with Mover component

**Scenario ID**: NAV-INFRA-001.1-S1

**GIVEN**
* the Mover component source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0
* the image `kata-tests` is available locally

---

### NAV-INFRA-001.2: Test execution — movement tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the Mover test suite
SO THAT movement logic is verified inside the container

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Movement tests pass inside Docker

**Scenario ID**: NAV-INFRA-001.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all NAV-BE-001 tests
* the container exits with code 0

---

### NAV-INFRA-001.3: Dependencies — movement dependencies installed

AS A platform engineer
I WANT all packages required by the Mover component listed in `requirements.txt`
SO THAT `pip install -r requirements.txt` inside Docker installs everything needed

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all movement dependencies

**Scenario ID**: NAV-INFRA-001.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Mover component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error
* the Mover module imports successfully inside the container

---

### NAV-INFRA-001.4: CI verification — movement pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the movement component
SO THAT every push verifies the Mover tests pass in Docker

**Parent**: NAV-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for movement component

**Scenario ID**: NAV-INFRA-001.4-S1

**GIVEN**
* a push is made to the feature branch containing Mover changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### NAV-INFRA-002.1: Docker build — navigation component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the Turner component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with Turner component

**Scenario ID**: NAV-INFRA-002.1-S1

**GIVEN**
* the Turner component source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### NAV-INFRA-002.2: Test execution — navigation tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the Turner test suite
SO THAT heading logic is verified inside the container

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Navigation tests pass inside Docker

**Scenario ID**: NAV-INFRA-002.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all NAV-BE-002 tests
* the container exits with code 0

---

### NAV-INFRA-002.3: Dependencies — navigation dependencies installed

AS A platform engineer
I WANT all packages required by the Turner component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all navigation dependencies

**Scenario ID**: NAV-INFRA-002.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Turner component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### NAV-INFRA-002.4: CI verification — navigation pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the navigation component
SO THAT every push verifies the Turner tests pass in Docker

**Parent**: NAV-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for navigation component

**Scenario ID**: NAV-INFRA-002.4-S1

**GIVEN**
* a push is made to the feature branch containing Turner changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN
