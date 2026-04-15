# Copilot Review Instructions

## Review Focus

- Only flag critical bugs, security vulnerabilities, or broken functionality
- Do not comment on style, grammar, punctuation, or documentation formatting
- Do not suggest refactoring, architectural changes, or alternative implementations
- Assume all cross-references (e.g., `architecture/` directory) will be resolved by dependent PRs

## What to Ignore

- Missing directories or files referenced in docs (assume they exist in other branches)
- Markdown formatting preferences
- Wording choices in user stories or requirements documents
- Pareto ratio justifications (trust the author's domain knowledge)
- Scenario coverage completeness (assume minimal viable scenarios are intentional)

## What to Flag

- Syntax errors or malformed JSON/YAML
- Security issues (hardcoded secrets, injection vulnerabilities)
- Logic errors that would cause runtime failures
- Broken links within the same PR's changed files
