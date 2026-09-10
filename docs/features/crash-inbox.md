# Feature: crash-inbox

> Disabled GlitchTip/Bugsink stub. Not a live crash-proxy. DPIA before enable.

## Acceptance criteria

- ✅ Example stub ships `enabled: false` with empty DSN/endpoint
- ✅ Gate fails if the stub is enabled or a live DSN is present
- ✅ FOSS example manifests do not depend on Sentry/Crashlytics/GlitchTip/Bugsink SDKs

## Smoke scenario

1. _Given_ the template checkout
2. _When_ `scripts/check-crash-inbox.sh` runs
3. _Then_ it exits 0 and prints that the stub stays disabled

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/crash_inbox.py` |
| View | `docs/CRASH_INBOX.md` |
| Tests | `tests/test_crash_inbox.py` |
| Wiring | `scripts/check-crash-inbox.sh` in `validate-bootstrap.sh` |

## Tests

- Automated: yes — stub off, DSN rejected, validate-bootstrap wiring
- Coverage: missing example file; enabled=true

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
