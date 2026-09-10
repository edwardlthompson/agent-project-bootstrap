# Feature: winget-publish-loop

> Hash desktop installer files into a Winget stub. Never submit to winget-pkgs.

## Acceptance criteria

- ✅ Loop hashes existing `WINGET_INSTALLER_X64` / `WINGET_INSTALLER_ARM64` files
- ✅ `--dry-run` packs a local zip when no installer env is set
- ✅ Output is validated; `[HUMAN]` owns the microsoft/winget-pkgs PR

## Smoke scenario

1. _Given_ no installer env vars
2. _When_ `scripts/winget-publish-loop.sh --dry-run` runs
3. _Then_ `dist/winget-loop/manifest.stub.yaml` exists with a computed SHA-256

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/winget_publish_loop.py` |
| View | `docs/WINGET.md` Local publish loop |
| Tests | `tests/test_winget_publish_loop.py` |
| Wiring | `scripts/winget-publish-loop.sh` |

## Tests

- Automated: yes — hash existing file; missing file fails
- Coverage: script refuses submit

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
