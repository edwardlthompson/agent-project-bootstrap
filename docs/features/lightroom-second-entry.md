# Feature: lightroom-second-entry

> Second Lr* factory on the Golden Path Lightroom stub (metadata tagset).

## Acceptance criteria

- ✅ `Info.lua` registers `LrExportServiceProvider` and `LrMetadataTagsetFactory`
- ✅ `MetadataTagset.lua` returns a tagset id and Adobe field items
- ✅ `verify-lightroom.sh` and Lua lint require the second entry

## Smoke scenario

1. _Given_ `examples/lightroom/Info.lua`
2. _When_ `bash scripts/verify-lightroom.sh`
3. _Then_ both Lr* factories are present

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/lightroom/MetadataTagset.lua` |
| View | N/A |
| Tests | `tests/test_lightroom_second_entry.py` |
| Wiring | `Info.lua` `LrMetadataTagsetFactory` |

## Tests

- Automated: yes — Info.lua + verify-lightroom greps
- Coverage: missing tagset factory fails lint

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack lightroom`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
