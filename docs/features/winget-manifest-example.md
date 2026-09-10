# Feature: winget-manifest-example

> Committed Winget singleton example. Placeholder hash only. Do not submit.

## Acceptance criteria

- ✅ `packaging/winget/example/manifest.yaml` has PackageIdentifier, version, license, and InstallerSha256
- ✅ Example uses `example.com` and a placeholder SHA-256
- ✅ `docs/WINGET.md` points at the example path

## Smoke scenario

1. _Given_ the committed example
2. _When_ `scripts/validate-winget-stub.sh packaging/winget/example/manifest.yaml` runs
3. _Then_ it exits 0 (never SKIP)

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/winget_runbook.py` |
| View | `packaging/winget/example/manifest.yaml` |
| Tests | `tests/test_winget_runbook.py` |
| Wiring | `scripts/check-winget-runbook.sh` |

## Tests

- Automated: yes — example keys + runbook path
- Coverage: missing example file

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
