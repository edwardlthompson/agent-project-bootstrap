# Feature: unifiedpush

> FOSS UnifiedPush sample for Golden Path Android. No FCM or Play Services.

## Acceptance criteria

- ✅ Distributor discovery via `org.unifiedpush.android.distributor.REGISTER`
- ✅ Message receiver listens for `org.unifiedpush.android.connector.MESSAGE`
- ✅ `usesProprietaryPush()` is always false
- ✅ Registration stays off until a distributor package is present

## Smoke scenario

1. _Given_ no UnifiedPush distributor installed
2. _When_ the app starts
3. _Then_ logs `no UnifiedPush distributor` and never references Firebase

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/android/app/src/main/java/dev/foss/goldenpath/push/` |
| View | N/A (no new chrome) |
| Tests | `push/UnifiedPushConfigTest.kt`, `tests/test_unifiedpush_sample.py` |
| Wiring | `GoldenPathApplication.logUnifiedPush` + manifest receiver/`queries` |

## Tests

- Automated: yes — JUnit parse/register/state tests + Python manifest/FOSS checks
- Coverage: empty distributor list, endpoint register, ignore non-connector actions

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack android`

## Definition of Done

See `docs/FEATURE_MODULES.md`. Installing ntfy/NextPush and receiving a live push stays `[ADB]`.
