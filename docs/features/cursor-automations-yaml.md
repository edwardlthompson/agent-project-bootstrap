# Feature: cursor-automations-yaml

> Commercial Automations YAML example. Disabled on the FOSS path.

## Acceptance criteria

- ✅ `.cursor/automations.commercial.example.yaml` ships `enabled: false`
- ✅ Recipes deny `git push` and treat webhooks as untrusted
- ✅ Live `.cursor/automations.yaml` is not committed
- ✅ Example includes disabled `weekly-maintain` and `monthly-dependabot-review` crons

## Smoke scenario

1. _Given_ the FOSS checkout
2. _When_ `scripts/check-cursor-automations.sh` runs
3. _Then_ the example exists and no live automations file is tracked

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_automations.py` |
| View | `.cursor/automations.commercial.example.yaml` |
| Tests | `tests/test_cursor_automations.py` |
| Wiring | `scripts/check-cursor-automations.sh` |

## Tests

- Automated: yes — needles + no live file
- Coverage: missing example

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
