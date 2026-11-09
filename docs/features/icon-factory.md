# Feature: icon-factory

> Manifest-driven Cycles batch for photoreal app icons. Plan-only apply; Sacred SVG branding stays.

## Acceptance criteria

- ✅ Sample manifest validates against `schemas/golden-path/icon-render-manifest.schema.json`
- ✅ QA gate checks PNG size, RGBA, alpha coverage without a human review of 4000 frames
- ✅ CI / feature-gate uses Cycles CPU `--limit 1` or skips if Blender is missing
- ✅ OptiX is `BLENDER_CYCLES_DEVICE=OPTIX` on This Computer only
- ✅ Live `branding/assets/*.svg` is never overwritten

## Smoke scenario

1. _Given_ `examples/blender/fixtures/icon-manifest.sample.json`
2. _When_ `python3 scripts/agent-run.py blender-icons -- --limit 1` (or unit tests if Blender is absent)
3. _Then_ QA JSON lists pass for the sample job

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/blender/*.py` |
| View | gitignored `examples/blender/out/` |
| Tests | `tests/test_blender_icon_factory.py` |
| Wiring | `scripts/blender-icons.sh`, `feature-gate.sh --stack blender` |

## Tests

- Automated: yes — schema, QA stub PNG, device env, cap/resume
- Coverage: missing id/seed; OptiX env ignored when blender missing

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack blender`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
