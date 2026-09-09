# Feature: android-signing

> Upload-key runbook and optional Gradle env signing. No keystore in git.

## Acceptance criteria

- ✅ `docs/ANDROID_SIGNING.md` covers keystore, env vars, CI, F-Droid/Play, and rollback
- ✅ `docs/RUNBOOK.md` and `examples/android/README.md` link to the runbook
- ✅ Gradle reads `GOLDENPATH_UPLOAD_*` only when a store path is set
- ✅ `*.jks` / `*.keystore` / `*.p12` are gitignored; none are tracked

## Smoke scenario

1. _Given_ no `GOLDENPATH_UPLOAD_STORE_FILE`
2. _When_ `bash scripts/check-android-signing-runbook.sh`
3. _Then_ the gate passes and `assembleRelease` stays debug-signed

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/android/app/build.gradle.kts` (env signing) |
| View | N/A |
| Tests | `tests/test_android_signing_runbook.py` |
| Wiring | `scripts/check-android-signing-runbook.sh` in feature-gate |

## Tests

- Automated: yes — Python runbook/Gradle/gitignore structure tests
- Coverage: missing headings, tracked keystore names, feature-gate hook

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack android`

## Definition of Done

See `docs/FEATURE_MODULES.md`. Creating a real upload keystore stays `[HUMAN]`.
