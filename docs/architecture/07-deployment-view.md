# Chapter 7: Deployment View

## Environment

The Mars Rover kata is a local CLI application. There is no server, cloud, or database deployment.

| Environment | Description |
|-------------|-------------|
| Developer machine | Python 3.12+, run via `python -m rover` or test runner |
| CI | Not currently configured in this repository; pre-commit hooks and unit tests are run locally |

## Runtime Dependencies

- Python 3.12+ interpreter
- No third-party runtime packages
- `pre-commit` for development tooling only
