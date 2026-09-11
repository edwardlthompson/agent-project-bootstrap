# Feature: semgrep-prompt-injection

> FOSS Semgrep pack for jailbreak phrases and shell injection sinks.

## Acceptance criteria

- ✅ `.semgrep/prompt-injection.yml` is FOSS-only (no `SEMGREP_APP_TOKEN`)
- ✅ Rules cover ignore-previous jailbreaks, `shell=True`, and `os.system`
- ✅ Pack header documents Android 16 / reflective-API sink notes (manual review until Kotlin rules land)
- ✅ `security.yml` and `check-semgrep.sh` load the pack beside `.semgrep.yml`

## Smoke scenario

1. _Given_ the template Semgrep configs
2. _When_ `bash scripts/check-semgrep.sh`
3. _Then_ both configs are required; the scanner runs only if Semgrep is on PATH

## Container map

| Layer | Path |
|-------|------|
| Logic | `.semgrep/prompt-injection.yml` |
| View | N/A |
| Tests | `tests/test_semgrep_foss.py` |
| Wiring | `.github/workflows/security.yml` + `scripts/lib/semgrep_foss.py` |
## Tests

- Automated: yes — config/CI phrase lock
- Coverage: missing pack, SaaS token, metrics off

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
