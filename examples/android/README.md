<p align="center">
  <img src="../../branding/assets/logo-mark.svg" alt="Golden Path" width="64" />
</p>

# Golden Path Android (FOSS)

FOSS apps with a clear path from idea to release — FOSS-only Gradle/Kotlin skeleton (no Google Play Services or Firebase). Brand kit: [`branding/BRANDING.md`](../../branding/BRANDING.md).

## Repository layout

```text
examples/android/
  app/src/main/
    res/values/strings.xml       # user-visible strings (English default)
    res/values-{lang}/           # add when shipping translations
    java/.../ui/
      theme/                     # GoldenPathTheme, generated Color.kt / Type.kt / Dimens.kt
      components/                # GoldenPathScaffold — labels via stringResource()
      screens/                   # GoldenPathScreen, etc.

```

**Styles and strings are separate:** theme colors and spacing live in `ui/theme/` (from `design-tokens/`). All copy lives in `strings.xml`, consumed via `stringResource(R.string.*)` in Compose — never `Text("literal")`.

See [`docs/DESIGN_GUIDE.md`](../../docs/DESIGN_GUIDE.md) and [`docs/WEB_PROJECT_LAYOUT.md`](../../docs/WEB_PROJECT_LAYOUT.md) for cross-stack conventions.

Optional task runner (not required for CI): install [just](https://github.com/casey/just), then `just test` (needs Android SDK).

## Why these tools?

Gradle + Kotlin + Compose is the FOSS-friendly Android stack. We pin the wrapper hash and `SOURCE_DATE_EPOCH` so F-Droid-style reproducible builds are possible, and we ban Play Services so the Golden Path stays redistributable.

## Structure validation (CI)

CI validates Gradle file structure and FOSS compliance markers only. Full APK builds require local Android SDK.

## Local build (ADB / HUMAN tasks)

```bash
export SOURCE_DATE_EPOCH=1700000000
cd examples/android
./gradlew assembleDebug
./gradlew assembleRelease
./gradlew :app:analyzeReleaseR8Config

```

Release R8 is on (`isMinifyEnabled` + resource shrinking). Retrace stacks with `app/build/outputs/mapping/release/mapping.txt`. Do not add package-wide keep rules. Memory limits: `GoldenPathApplication` + [`docs/features/android-runtime-budget.md`](../../docs/features/android-runtime-budget.md).

## Emulator checklist

Before running instrumented tests or manual QA:

- 🔲 Android SDK Platform 34+ installed (`sdkmanager "platforms;android-34"`)
- 🔲 Build-tools 34.x installed
- 🔲 System image with Google APIs **not** required (use AOSP image for FOSS parity)
- 🔲 `adb devices` lists emulator or hardware as `device`
- 🔲 Set `SOURCE_DATE_EPOCH` for reproducible release builds (template default: `1700000000`)
- 🔲 Accept licenses: `sdkmanager --licenses`
- 🔲 Pin `androidx.test.espresso:espresso-core` **3.7.0+** (Android 16 / API 36 removed `InputManager.getInstance`)

### Instrumented UI tests (Compose rule v2)

UI `androidTest` classes use `androidx.compose.ui.test.junit4.v2.createAndroidComposeRule<MainActivity>()` (Compose UI Test v2 / StandardTestDispatcher). Prefer that over bare `ActivityScenarioRule` so Compose semantics, failure screenshots (`FailureEvidenceRule`), and Activity share one rule chain. `LocaleRtlUiTest` is resource-only and does not launch an Activity.

`scripts/verify.sh` never runs `connectedDebugAndroidTest` (honesty: no device → no instrumented claim). feature-gate compiles androidTest; device runs need `adb` + `ANDROID_SERIAL`.

About `versionName` is read from `schemas/golden-path/app-version.json` (same SoT as web/python package versions).

### Instrumented CI matrix

| Target | Where | Notes |
|--------|--------|--------|
| AVD API 34 (`goldenpath-api34`) | GitHub `Android - connectedDebugAndroidTest` | Default CI path; needs KVM on the runner |
| Physical API 36 (e.g. OnePlus) | Local `/emulator` or `/build` ADB rows | Requires Espresso 3.7+; authorize `adb` RSA once |
| Unit `./gradlew test` | `feature-gate` `android-test` | No device; Robolectric |
**Flaky quarantine:** CI runs `connectedDebugAndroidTest` once, then **retries once** on failure (emulator flake). Do not hide product bugs behind the retry — `@Ignore("issue-url")` or fix. PR label: `quarantine:instrumented`.

#### AVD snapshot bake (`goldenpath-api34`)

After the first full boot of AVD `goldenpath-api34`, save a cold snapshot for faster local/CI starts:

```bash
adb emu avd snapshot save goldenpath-cold

```

GitHub `android-emulator-runner` caches system images; when adding a custom snapshot restore, key the cache on `api-level-34-x86_64-goldenpath`. Pair with CI `disable-animations: true` and androidTest `DisableAnimationsRule`.

Local host-GPU path (skips if SDK missing): `python3 scripts/agent-run.py run-android-emulator-local` or `just android-instrumented`. Uses `-gpu host` then `swiftshader_indirect`. GitHub `android-instrumented` remains backup.

## FOSS compliance

- No `com.google.android.gms` dependencies
- No Firebase dependencies
- `SOURCE_DATE_EPOCH` for reproducible builds
- Pinned Gradle wrapper SHA-256 in `gradle/wrapper/gradle-wrapper.properties`

## Signing and rollback

Upload keystores stay outside git. Optional env-based release signing and rollback steps: [`docs/ANDROID_SIGNING.md`](../../docs/ANDROID_SIGNING.md).

## F-Droid notes

Document dependency hashes and reproducible build verification steps in your project's `AGENT_MEMORY.md` when activating module A.

## Child init inherits Espresso 3.7

`scripts/init-project.sh` keeps `examples/android/` (when Android is selected) including the Espresso **3.7.0+** pin and `check-espresso-android16` gate. Do not downgrade on child catch-up; upgrade-sim asserts the pin (#183/#184).
