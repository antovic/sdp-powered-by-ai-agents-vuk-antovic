# Chapter 2: Architecture Constraints

## Technical Constraints

| Constraint | Reason |
|-----------|--------|
| Python 3.12+ | Course standard language |
| No external runtime dependencies | Kata must run with stdlib only |
| Pre-commit hooks enforced | Code quality and commit format validation required |

## Organisational Constraints

| Constraint | Reason |
|-----------|--------|
| All changes via PRs | No direct commits to master |
| Commit format: `#N type(scope): description` | Enforced by commit-msg hook |
| Branches follow `type/issue-description` | Team convention |
