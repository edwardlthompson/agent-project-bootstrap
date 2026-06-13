# Contributing

Thank you for contributing to **agent-project-bootstrap** — a Cursor agent-oriented FOSS project template.

## Who contributes what

| Label | Contributor | Examples |
|-------|-------------|----------|
| `AGENT` | Cursor Agent | Scaffolding, tests, CI config, docs |
| `HUMAN` | Human developer | Approvals, credentials, product decisions |
| `ADB` | Human (Android) | Device testing, F-Droid submission |
| `AUTO` | CI/scripts | GitHub Actions, Dependabot, pre-commit |

## Getting started

1. Fork the repository and create a feature branch.
2. Read `docs/START_HERE.md` and `docs/MAINTAINING_THE_TEMPLATE.md`.
3. Make changes; ensure CI passes locally where possible.
4. Open a PR using the provided template.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/).

## Template improvements

Use the **Template Improvement** issue template for feedback.

## Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Release process (maintainers)

See `docs/MAINTAINING_THE_TEMPLATE.md` for the full semver release checklist.
