# Feature: cursor-cloud-hooks

> Merge commercial Cloud conversation hooks without dropping FOSS guards.

## Acceptance criteria

- ✅ Merge keeps `beforeShellExecution` and `afterFileEdit`
- ✅ Merge adds `afterAgentResponse` and `stop`
- ✅ Live FOSS `hooks.json` does not ship those commercial events

## Smoke scenario

1. _Given_ `.cursor/hooks.json` and the commercial Cloud example
2. _When_ `merge_hooks` runs
3. _Then_ FOSS shell/encoding hooks remain and Cloud events are appended

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_cloud_hooks.py` |
| View | `.cursor/hooks.cloud.commercial.example.json` |
| Tests | `tests/test_cursor_cloud_hooks.py` |
| Wiring | `scripts/check-cursor-cloud-hooks.sh` |

## Tests

- Automated: yes — merge unit test + repo check
- Coverage: dropped FOSS hook

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
