# Chapter 11: Risks and Technical Debts

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Grid wrapping logic edge cases | Medium | High | Cover all boundary conditions with parameterised tests |
| Heading calculation off-by-one (e.g. L from N → W not E) | Medium | High | Table-driven unit tests for all heading transitions |

## Technical Debts

| Debt | Description | Plan |
|------|-------------|------|
| No CLI argument parsing | Input currently hardcoded or via stdin | Add `argparse` when integrating with other modules |
| No obstacle file loading | Obstacles defined in code | Add JSON/CSV loader if kata is extended |
