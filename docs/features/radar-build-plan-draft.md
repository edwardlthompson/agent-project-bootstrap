# Feature: radar-build-plan-draft

> High-score radar URLs become a gitignored BUILD_PLAN-shaped draft.

## Acceptance criteria

- ✅ Score ≥ 9 writes `CURSOR_RADAR_BUILD_PLAN_DRAFT.md` with `🔲 [AGENT]` rows
- ✅ Radar never writes `BUILD_PLAN.md`
- ✅ Draft filename is gitignored

## Smoke scenario

1. _Given_ a scored URL of 9
2. _When_ `write_build_plan_draft` runs
3. _Then_ the draft file exists and `BUILD_PLAN.md` is untouched

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_feature_radar_io.py` |
| View | N/A |
| Tests | `tests/test_cursor_feature_radar_draft.py` |
| Wiring | `cursor_feature_radar.py` after suggestions |

## Tests

- Automated: yes — draft markers + gitignore
- Coverage: score 6 omitted; BUILD_PLAN.md absent

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
