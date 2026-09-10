# Feature: lightroom-lua-lint

> Static Lr* lint for `examples/lightroom`. No Lightroom app required.

## Acceptance criteria

- ✅ Generic `require()` / `os.execute` / `io.popen` fail the lint
- ✅ `import` is limited to `Lr*` SDK modules
- ✅ `examples/lightroom/.luacheckrc` allows the `import` global
- ✅ Feature-gate `lightroom` runs `scripts/check-lightroom-lua.sh`

## Smoke scenario

1. _Given_ the Golden Path Lightroom stub
2. _When_ `bash scripts/check-lightroom-lua.sh`
3. _Then_ the gate passes without Adobe Lightroom installed

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/lightroom/*.lua` |
| View | N/A |
| Tests | `tests/test_lightroom_lua_lint.py` |
| Wiring | `scripts/check-lightroom-lua.sh` in feature-gate + CI |

## Tests

- Automated: yes — Python lint + fixture that rejects `require()`
- Coverage: missing Info.lua tokens, forbidden OS calls

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack lightroom`

## Definition of Done

See `docs/FEATURE_MODULES.md`. Loading the plugin in Lightroom Classic stays `[HUMAN]`.
