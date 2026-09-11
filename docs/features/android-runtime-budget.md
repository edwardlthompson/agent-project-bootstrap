# Feature: android-runtime-budget

> Golden Path release R8 + Android 17 memory limits (Sprint M48). Compose BOM already `2026.08.00`.

## Acceptance criteria

- ✅ Release builds minify and shrink with `proguard-android-optimize.txt`
- ✅ No broad `-keep public class *` rules; no `largeHeap`; R8 full mode left on
- ✅ `GoldenPathApplication` installs crash capture, logs limiter kills, trims on UI_HIDDEN / BACKGROUND
- ✅ Compose 1.12: no `onFirstVisible`; Credential Manager stays off FOSS path
- ✅ Optional Grok Bot ops documented; FOSS default stays local `/gates`

## Smoke scenario

1. _Given_ `examples/android/` with an Android SDK
2. _When_ `./gradlew :app:analyzeReleaseR8Config` (or `assembleRelease`)
3. _Then_ the analyzer HTML exists and structure tests still pass without SDK via `python3 -m unittest tests.test_android_runtime_budget`

## Container map

| Layer | Path |
|-------|------|
| Logic | `examples/android/app/src/main/java/dev/foss/goldenpath/memory/` |
| View | N/A (no new UI) |
| Tests | `memory/MemoryBudgetTest.kt`, `tests/test_android_runtime_budget.py` |
| Wiring | `GoldenPathApplication` + manifest `android:name` (≤10 lines of feature wiring) |
## Tests

- Automated: yes — JUnit `MemoryBudgetTest` + Python structure tests
- Coverage: limiter null/empty, trim levels, Gradle/manifest invariants

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack android` (Gradle when SDK present)

## Definition of Done

See `docs/FEATURE_MODULES.md`. Device memory-limiter adb simulation stays `[ADB]`.

## Notes

- Retrace release crashes with `app/build/outputs/mapping/release/mapping.txt`
- Analyzer: [R8 Configuration Analyzer](https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer)

### Upload `mapping.txt` to GitHub Releases (FOSS)

Do **not** commit mapping files. Attach them as a Release asset next to the APK/AAB (same tag as SBOM):

```bash
# after assembleRelease
MAP=examples/android/app/build/outputs/mapping/release/mapping.txt
TAG=v1.2.3   # match the GitHub Release
gh release upload "$TAG" "$MAP" --clobber

```

Wire optionally in `.github/workflows/release.yml` after the Android release job produces the mapping artifact. Keep the file out of git (`**/mapping.txt` already ignored via build outputs).
- Grok Bot prompts: [`docs/GROK_BOTS.md`](../GROK_BOTS.md)
