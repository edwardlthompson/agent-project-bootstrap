# Feature: android-module-fdroid

> Keep `modules/android/MODULE.md` F-Droid rows in sync with the Golden Path recipe.

## Acceptance criteria

- ✅ Checklist names the F-Droid recipe, Fastlane listing, AntiFeatures template, signing runbook, and UnifiedPush spec

## Smoke scenario

1. _Given_ `modules/android/MODULE.md`
2. _When_ `python3 -m unittest tests.test_android_module_fdroid`
3. _Then_ the shipped metadata paths are present

## Container map

| Layer | Path |
|-------|------|
| Logic | N/A |
| View | N/A |
| Tests | `tests/test_android_module_fdroid.py` |
| Wiring | `modules/android/MODULE.md` |

## Tests

- Automated: yes — phrase lock on MODULE.md
- Coverage: missing recipe / Fastlane / signing rows

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
