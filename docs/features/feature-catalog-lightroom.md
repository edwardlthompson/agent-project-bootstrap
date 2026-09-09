# Feature: feature-catalog-lightroom

> Optional Lightroom stack in `schemas/golden-path/feature-catalog.json`.

## Acceptance criteria

- ✅ Catalog id `lightroom-plugin` is stack-filtered to `lightroom` only
- ✅ Detect path includes `examples/lightroom/Info.lua`
- ✅ Web/Android gap reports omit the Lightroom feature

## Smoke scenario

1. _Given_ a child repo with `stack: web`
2. _When_ feature gaps are computed
3. _Then_ `lightroom-plugin` is not listed

## Container map

| Layer | Path |
|-------|------|
| Logic | `schemas/golden-path/feature-catalog.json` |
| View | N/A |
| Tests | `tests/test_feature_catalog_lightroom.py`, `tests/test_template_gap.py` |
| Wiring | `scripts/lib/template_gap.py` |

## Tests

- Automated: yes — catalog JSON + stack filter
- Coverage: web omits lightroom; lightroom stack reports the gap

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
