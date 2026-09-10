# Feature: cursor-marketplace

> Marketplace runbook. Local pack default. No unsigned install on FOSS.

## Acceptance criteria

- ✅ `docs/CURSOR_MARKETPLACE.md` names the local pack and forbids default marketplace install
- ✅ Optional wshobson pointer is `[HUMAN]` opt-in only
- ✅ Gate is wired into validate-bootstrap

## Smoke scenario

1. _Given_ the template checkout
2. _When_ `scripts/check-cursor-marketplace.sh` runs
3. _Then_ it exits 0 and the runbook still says do not install by default

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_marketplace.py` |
| View | `docs/CURSOR_MARKETPLACE.md` |
| Tests | `tests/test_cursor_marketplace.py` |
| Wiring | `scripts/check-cursor-marketplace.sh` |

## Tests

- Automated: yes — needles + validate-bootstrap wiring
- Coverage: missing runbook file

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
