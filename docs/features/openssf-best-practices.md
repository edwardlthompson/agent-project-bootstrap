# Feature: openssf-best-practices

> Public OpenSSF Best Practices badge (project 14564) plus sanitized CI refs.

## Acceptance criteria

- ✅ README hero links `bestpractices.dev/projects/14564`
- ✅ `.bestpractices.json` proposes Passing answers the repo already meets
- ✅ CI validates branch names and release tags before use (OSPS-BR-01.01 / 01.02)

## Smoke scenario

1. _Given_ project 14564
2. _When_ a maintainer clicks Save (and continue) 🤖 on bestpractices.dev
3. _Then_ automation picks up `.bestpractices.json` and the public badge stays in README

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/ci_refs.py` |
| View | `README.md`, `.bestpractices.json`, `docs/OPENSSF_BEST_PRACTICES.md` |
| Tests | `tests/test_ci_refs.py` |
| Wiring | `scripts/check-ci-refs.sh` in CI and Release |

## Tests

- Automated: yes — unsafe branch/tag rejected; workflows call the check
- Coverage: `v1;echo` tag

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
