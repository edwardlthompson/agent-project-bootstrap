# Feature: grok-bots

> Land optional Grok Bot ops docs. Not required on the FOSS path.

## Acceptance criteria

- ✅ `docs/GROK_BOTS.md` exists with FOSS alternative and destructive-ops deny
- ✅ `validate-bootstrap.sh` requires the file
- ✅ `docs/START_HERE.md` links it as optional commercial

## Smoke scenario

1. _Given_ a FOSS checkout
2. _When_ `validate-bootstrap --quick` runs
3. _Then_ `docs/GROK_BOTS.md` is present and no Bot is required to ship

## Container map

| Layer | Path |
|-------|------|
| Logic | N/A |
| View | `docs/GROK_BOTS.md` |
| Tests | `tests/test_grok_bots.py` |
| Wiring | `scripts/validate-bootstrap.sh`, `docs/START_HERE.md` |

## Tests

- Automated: yes — needles + wiring
- Coverage: missing FOSS alternative heading

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
