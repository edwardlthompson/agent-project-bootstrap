# Feature: feature-catalog-navigation

> Register `navigation` in `schemas/golden-path/feature-catalog.json`.

## Acceptance criteria

- ✅ Catalog id `navigation` points at `docs/features/navigation.md`
- ✅ Stacks are `web` and `android` with detect paths for `src/nav` and `ui/nav`

## Smoke scenario

1. _Given_ a child web repo without `src/nav`
2. _When_ `check-template-gaps` runs
3. _Then_ `navigation` is reported as a feature gap

## Container map

| Layer | Path |
|-------|------|
| Logic | `schemas/golden-path/feature-catalog.json` |
| View | N/A |
| Tests | `tests/test_feature_catalog_navigation.py` |
| Wiring | `scripts/lib/template_gap.py` |

## Tests

- Automated: yes — catalog JSON shape
- Coverage: missing id / wrong stacks

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
