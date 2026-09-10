# Feature: adr-0001-architecture-pick

> Template ADR-0001 lists MVVM / Clean / Hexagonal and does not pre-select one.

## Acceptance criteria

- ✅ `docs/adr/0001-core-architecture.md` names all three patterns with open 🔲 boxes
- ✅ The template must not mark a pattern ✅
- ✅ `docs/INITIALIZATION_PROMPT.md` still names the ADR-0001 Sprint 1 row

## Smoke scenario

1. _Given_ this template checkout
2. _When_ `scripts/check-adr-architecture.sh` runs
3. _Then_ it exits 0 and treats ADR-0001 as an open child pick

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/adr_architecture.py` |
| View | `docs/adr/0001-core-architecture.md` |
| Tests | `tests/test_adr_architecture.py` |
| Wiring | `scripts/check-adr-architecture.sh` in `validate-bootstrap.sh` |

## Tests

- Automated: yes — open boxes, no pre-select, prompt names ADR-0001
- Coverage: selected pattern marked ✅

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
