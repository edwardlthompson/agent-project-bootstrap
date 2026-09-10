# Feature: lightroom-sdk-bump

> Playbook and version-table gate for Lightroom Classic SDK bumps.

## Acceptance criteria

- ✅ `docs/LIGHTROOM_SDK_BUMP.md` lists current versions, steps, HUMAN load test, and do-nots
- ✅ README table matches `Info.lua` `LrSdkVersion` / `LrSdkMinimumVersion`
- ✅ Feature-gate runs `scripts/check-lightroom-sdk-playbook.sh`

## Smoke scenario

1. _Given_ Info.lua `LrSdkVersion = 13.0`
2. _When_ the README table says a different number
3. _Then_ the playbook gate fails

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/lightroom_sdk_playbook.py` |
| View | N/A |
| Tests | `tests/test_lightroom_sdk_playbook.py` |
| Wiring | `scripts/check-lightroom-sdk-playbook.sh` |

## Tests

- Automated: yes — version parse + missing playbook
- Coverage: Info/README mismatch

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack lightroom`

## Definition of Done

See `docs/FEATURE_MODULES.md`. Live Plug-in Manager reload stays `[HUMAN]`.
