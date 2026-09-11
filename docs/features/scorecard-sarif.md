# Feature: scorecard-sarif

> Auto-classify OpenSSF Scorecard SARIF checks using the SECURITY_TRIAGE table.

## Acceptance criteria

- ✅ `TokenPermissions` → AGENT fix; pin/vuln checks → HUMAN dismiss; process scores → defer
- ✅ Unknown checks default to HUMAN defer
- ✅ Scorecard workflow prints the classification after upload

## Smoke scenario

1. _Given_ a SARIF with `TokenPermissions`
2. _When_ `python3 scripts/lib/scorecard_sarif.py results.sarif`
3. _Then_ JSON says `action=fix` and `owner=AGENT`

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/scorecard_sarif.py` |
| View | N/A |
| Tests | `tests/test_scorecard_sarif.py` |
| Wiring | `.github/workflows/scorecard.yml` Classify SARIF step |
## Tests

- Automated: yes — rule table + fixture SARIF
- Coverage: unknown check, empty runs, docs needles, golden fixtures under `tests/fixtures/scorecard/`

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
