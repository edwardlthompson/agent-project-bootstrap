# Feature: sanitize-fixtures

> Cross-stack sanitizer fixture parity in local gates and CI.

## Acceptance criteria

- ✅ Web and Android copies match `schemas/golden-path/sanitize-fixtures.json`
- ✅ Node, Python, Rust, and Go sanitizer tests cover the same injection needles
- ✅ Always-on CI job `sanitize-fixtures` is required by `ci-ok`

## Smoke scenario

1. _Given_ a Golden Path stack is present
2. _When_ `scripts/check-sanitize-fixtures.sh` runs
3. _Then_ copies match the canonical fixture and CLI tests still redact jailbreak phrases

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/sanitize_fixtures.py` |
| View | N/A |
| Tests | `tests/test_sanitize_fixture_parity.py` |
| Wiring | `.github/workflows/ci.yml` `sanitize-fixtures` job |

## Tests

- Automated: yes — canonical copy match + CI/validate-bootstrap wiring
- Coverage: missing canonical file

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
