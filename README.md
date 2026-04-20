# Mars Rover Kata

A Mars Rover kata implemented with full TDD/BDD discipline, CI/CD pipelines, and AI-assisted development as part of the *Software Development Processes Powered by AI Agents* course.

## What it solves

The rover accepts a sequence of commands (`F`, `B`, `L`, `R`) and navigates a toroidal grid, detecting obstacles and reporting its final position and heading.

## Tech stack

- **Language**: Python 3.12
- **Testing**: pytest with TDD/BDD discipline
- **Container**: Docker (single-image build + test)
- **CI/CD**: GitHub Actions
- **Docs**: Sphinx + GitHub Pages

## Architecture overview

The rover engine is composed of four pure components:

| Component | Responsibility |
|-----------|---------------|
| `CommandParser` | Tokenises and validates raw command strings |
| `Turner` | Computes heading changes for `L`/`R` commands |
| `Mover` | Computes position changes for `F`/`B` commands |
| `Grid` | Enforces boundary wrapping and obstacle detection |
| `CommandHistory` | Audit log of executed command sequences |

All state is immutable (`RoverState` is a frozen dataclass). See `docs/architecture/` for full arc42 documentation.

## Build and run locally

```bash
docker build -t kata-tests .
docker run --rm kata-tests
```

## Run tests locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## Documentation

Live Sphinx site: **https://antovic.github.io/sdp-powered-by-ai-agents-vuk-antovic/**

## Project structure

```
├── src/
│   └── rover.py              # All domain logic
├── tests/                    # pytest test suite (one file per BE scenario)
├── docs/
│   ├── architecture/         # arc42 chapters + diagrams
│   └── user-stories/         # Story inventory + domain bundles
├── .github/workflows/
│   ├── ci.yml                # Build + test on every push
│   └── docs-deploy.yml       # Sphinx → GitHub Pages
├── Dockerfile
└── requirements.txt
```

## Author

Vuk Antovic
