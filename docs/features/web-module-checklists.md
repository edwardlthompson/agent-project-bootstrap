# Feature: web-module-checklists

> Keep `modules/web/MODULE.md` in sync with shipped Golden Path chrome and gates.

## Acceptance criteria

- ✅ Checklist names Settings-only chrome, es.json, snapshots, and Lighthouse floors
- ✅ Feature-gate table lists design-cohesion and lighthouse-floors

## Smoke scenario

1. _Given_ `modules/web/MODULE.md`
2. _When_ `python3 -m unittest tests.test_web_module_checklist`
3. _Then_ the shipped checklist phrases are present

## Container map

| Layer | Path |
|-------|------|
| Logic | N/A |
| View | N/A |
| Tests | `tests/test_web_module_checklist.py` |
| Wiring | `modules/web/MODULE.md` |

## Tests

- Automated: yes — phrase lock on MODULE.md
- Coverage: missing chrome/lighthouse rows

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
