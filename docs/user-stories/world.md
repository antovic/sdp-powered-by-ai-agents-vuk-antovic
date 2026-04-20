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

### WORLD-INFRA-001.1: Docker build — obstacle detection component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the Grid obstacle detection component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with obstacle detection component

**Scenario ID**: WORLD-INFRA-001.1-S1

**GIVEN**
* the Grid component source with obstacle detection is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0
* the image `kata-tests` is available locally

---

### WORLD-INFRA-001.2: Test execution — obstacle detection tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the obstacle detection test suite
SO THAT collision logic is verified inside the container

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Obstacle detection tests pass inside Docker

**Scenario ID**: WORLD-INFRA-001.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all WORLD-BE-001 tests
* the container exits with code 0

---

### WORLD-INFRA-001.3: Dependencies — obstacle detection dependencies installed

AS A platform engineer
I WANT all packages required by the Grid component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all obstacle detection dependencies

**Scenario ID**: WORLD-INFRA-001.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Grid component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error
* the Grid module imports successfully inside the container

---

### WORLD-INFRA-001.4: CI verification — obstacle detection pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the obstacle detection component
SO THAT every push verifies the obstacle tests pass in Docker

**Parent**: WORLD-STORY-001
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for obstacle detection component

**Scenario ID**: WORLD-INFRA-001.4-S1

**GIVEN**
* a push is made to the feature branch containing Grid obstacle changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### WORLD-INFRA-002.1: Docker build — boundary component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the Grid boundary component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with boundary component

**Scenario ID**: WORLD-INFRA-002.1-S1

**GIVEN**
* the Grid boundary source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### WORLD-INFRA-002.2: Test execution — boundary tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the boundary wrapping test suite
SO THAT wrap-around logic is verified inside the container

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Boundary tests pass inside Docker

**Scenario ID**: WORLD-INFRA-002.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all WORLD-BE-002 tests
* the container exits with code 0

---

### WORLD-INFRA-002.3: Dependencies — boundary dependencies installed

AS A platform engineer
I WANT all packages required by the Grid boundary component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all boundary dependencies

**Scenario ID**: WORLD-INFRA-002.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Grid component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### WORLD-INFRA-002.4: CI verification — boundary pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the boundary component
SO THAT every push verifies the boundary tests pass in Docker

**Parent**: WORLD-STORY-002
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for boundary component

**Scenario ID**: WORLD-INFRA-002.4-S1

**GIVEN**
* a push is made to the feature branch containing Grid boundary changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

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

### WORLD-INFRA-003.1: Docker build — state query component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the RoverState query component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with state query component

**Scenario ID**: WORLD-INFRA-003.1-S1

**GIVEN**
* the RoverState query source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### WORLD-INFRA-003.2: Test execution — state query tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the state query test suite
SO THAT read-only state access is verified inside the container

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: State query tests pass inside Docker

**Scenario ID**: WORLD-INFRA-003.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all WORLD-BE-003 tests
* the container exits with code 0

---

### WORLD-INFRA-003.3: Dependencies — state query dependencies installed

AS A platform engineer
I WANT all packages required by the RoverState component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all state query dependencies

**Scenario ID**: WORLD-INFRA-003.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the RoverState component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### WORLD-INFRA-003.4: CI verification — state query pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the state query component
SO THAT every push verifies the state query tests pass in Docker

**Parent**: WORLD-STORY-003
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for state query component

**Scenario ID**: WORLD-INFRA-003.4-S1

**GIVEN**
* a push is made to the feature branch containing RoverState changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

---

# WORLD-STORY-004: Add obstacle to grid at runtime [SUPPORTING]

## Original Story

AS A mission controller
I WANT to add a new obstacle to the grid at a specified coordinate
SO THAT I can update the terrain map without redeploying the system

**Architecture Reference**: Chapter 5 — Building Block View (Grid component); Chapter 8 — Cross-cutting Concepts (Configuration Management)

### SCENARIO 1: Add obstacle at valid coordinate

**Scenario ID**: WORLD-STORY-004-S1

**GIVEN**
* the grid is 5×5
* no obstacle exists at (2, 3)

**WHEN**
* the mission controller adds an obstacle at (2, 3)

**THEN**
* the grid contains an obstacle at (2, 3)
* subsequent move commands to (2, 3) are blocked

---

## BE Sub-stories

### WORLD-BE-004.1: Insert obstacle into grid state

AS A rover engine
I WANT the Grid component to accept a new obstacle coordinate and update its internal state
SO THAT the obstacle is immediately active for collision detection

**Parent**: WORLD-STORY-004
**Architecture Reference**: Chapter 5 — Building Block View (Grid component)

#### SCENARIO 1: Grid state includes new obstacle

**Scenario ID**: WORLD-BE-004.1-S1

**GIVEN**
* the Grid has obstacles at `[(0,1)]`

**WHEN**
* the Grid processes an add-obstacle command for `(2,3)`

**THEN**
* the Grid's obstacle set is `[(0,1), (2,3)]`

---

## INFRA Sub-stories

### WORLD-INFRA-004.1: Docker build — add obstacle component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the add-obstacle component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: WORLD-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with add-obstacle component

**Scenario ID**: WORLD-INFRA-004.1-S1

**GIVEN**
* the Grid add-obstacle source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### WORLD-INFRA-004.2: Test execution — add obstacle tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the add-obstacle test suite
SO THAT obstacle insertion logic is verified inside the container

**Parent**: WORLD-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Add obstacle tests pass inside Docker

**Scenario ID**: WORLD-INFRA-004.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all WORLD-BE-004 tests
* the container exits with code 0

---

### WORLD-INFRA-004.3: Dependencies — add obstacle dependencies installed

AS A platform engineer
I WANT all packages required by the Grid add-obstacle component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: WORLD-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all add-obstacle dependencies

**Scenario ID**: WORLD-INFRA-004.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Grid component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### WORLD-INFRA-004.4: CI verification — add obstacle pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the add-obstacle component
SO THAT every push verifies the add-obstacle tests pass in Docker

**Parent**: WORLD-STORY-004
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for add-obstacle component

**Scenario ID**: WORLD-INFRA-004.4-S1

**GIVEN**
* a push is made to the feature branch containing Grid add-obstacle changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN

---

# WORLD-STORY-005: Remove obstacle from grid [SUPPORTING]

## Original Story

AS A mission controller
I WANT to remove an existing obstacle from the grid
SO THAT I can clear paths that are no longer blocked

**Architecture Reference**: Chapter 5 — Building Block View (Grid component); Chapter 8 — Cross-cutting Concepts (Configuration Management)

### SCENARIO 1: Remove existing obstacle

**Scenario ID**: WORLD-STORY-005-S1

**GIVEN**
* the grid contains an obstacle at (2, 3)

**WHEN**
* the mission controller removes the obstacle at (2, 3)

**THEN**
* the grid no longer contains an obstacle at (2, 3)
* subsequent move commands to (2, 3) succeed

---

## BE Sub-stories

### WORLD-BE-005.1: Delete obstacle from grid state

AS A rover engine
I WANT the Grid component to remove an obstacle coordinate from its internal state
SO THAT the coordinate is immediately passable

**Parent**: WORLD-STORY-005
**Architecture Reference**: Chapter 5 — Building Block View (Grid component)

#### SCENARIO 1: Grid state excludes removed obstacle

**Scenario ID**: WORLD-BE-005.1-S1

**GIVEN**
* the Grid has obstacles at `[(0,1), (2,3)]`

**WHEN**
* the Grid processes a remove-obstacle command for `(2,3)`

**THEN**
* the Grid's obstacle set is `[(0,1)]`

---

## INFRA Sub-stories

### WORLD-INFRA-005.1: Docker build — remove obstacle component included

AS A platform engineer
I WANT the Dockerfile to build successfully with the remove-obstacle component present
SO THAT `docker build -t kata-tests .` produces a runnable image

**Parent**: WORLD-STORY-005
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker image builds with remove-obstacle component

**Scenario ID**: WORLD-INFRA-005.1-S1

**GIVEN**
* the Grid remove-obstacle source is present in the repository

**WHEN**
* `docker build -t kata-tests .` is executed

**THEN**
* the build completes with exit code 0

---

### WORLD-INFRA-005.2: Test execution — remove obstacle tests run in Docker

AS A platform engineer
I WANT `docker run --rm kata-tests` to execute the remove-obstacle test suite
SO THAT obstacle deletion logic is verified inside the container

**Parent**: WORLD-STORY-005
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Remove obstacle tests pass inside Docker

**Scenario ID**: WORLD-INFRA-005.2-S1

**GIVEN**
* the `kata-tests` image has been built

**WHEN**
* `docker run --rm kata-tests` is executed

**THEN**
* pytest collects and runs all WORLD-BE-005 tests
* the container exits with code 0

---

### WORLD-INFRA-005.3: Dependencies — remove obstacle dependencies installed

AS A platform engineer
I WANT all packages required by the Grid remove-obstacle component listed in `requirements.txt`
SO THAT the Docker build installs everything needed

**Parent**: WORLD-STORY-005
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: Docker build installs all remove-obstacle dependencies

**Scenario ID**: WORLD-INFRA-005.3-S1

**GIVEN**
* `requirements.txt` lists all packages needed by the Grid component

**WHEN**
* `docker build -t kata-tests .` runs `pip install -r requirements.txt`

**THEN**
* all dependencies install without error

---

### WORLD-INFRA-005.4: CI verification — remove obstacle pipeline is GREEN

AS A platform engineer
I WANT the CI pipeline to run `docker build` and `docker run` for the remove-obstacle component
SO THAT every push verifies the remove-obstacle tests pass in Docker

**Parent**: WORLD-STORY-005
**Architecture Reference**: Chapter 7 — Deployment View

#### SCENARIO 1: CI pipeline passes for remove-obstacle component

**Scenario ID**: WORLD-INFRA-005.4-S1

**GIVEN**
* a push is made to the feature branch containing Grid remove-obstacle changes

**WHEN**
* the CI pipeline executes `docker build -t kata-tests .` and `docker run --rm kata-tests`

**THEN**
* both steps complete with exit code 0
* the pipeline reports GREEN
