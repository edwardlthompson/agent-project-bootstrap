# Feature: winget-multi-arch

> Winget example and runbook list x64 and arm64. One hash per asset.

## Acceptance criteria

- ✅ Example manifest lists `Architecture: x64` and `Architecture: arm64`
- ✅ Runbook says each arch has its own URL and SHA-256
- ✅ Generator stub emits both architectures

## Smoke scenario

1. _Given_ `docs/WINGET.md` and the committed example
2. _When_ the runbook gate runs
3. _Then_ both architectures are present and hashes stay placeholders

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/winget_runbook.py` |
| View | `docs/WINGET.md`, `packaging/winget/example/manifest.yaml` |
| Tests | `tests/test_winget_runbook.py` |
| Wiring | `scripts/generate-winget-manifest.sh` |

## Tests

- Automated: yes — example lists both arches
- Coverage: missing arm64 row

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
