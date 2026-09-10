# ADR-0003: Android runtime budget (R8 + memory limits)

- **Status:** Accepted
- **Date:** 2026-09-09
- **Deciders:** Template maintainer

## Context

Compose August 2026 (BOM `2026.08.00`, Compose 1.12) already matches this repo (`compileSdk` 37, AGP 9.4). Android 17 enforces per-app memory limits (`MemoryLimiter:AnonSwap`). Tinder’s R8 Configuration Analyzer work showed broad keep rules can leave most of an app unoptimized even when R8 is “on”. Golden Path release was `isMinifyEnabled = false` with no keep-rule file.

## Decision

1. **Release R8 on** with `isMinifyEnabled`, `isShrinkResources`, and `proguard-android-optimize.txt`. Keep rules stay narrow (source-file attributes only). No `-keep public class *`, `-dontoptimize`, `-dontobfuscate`, or `android.enableR8.fullMode=false`.
2. **Audit with** `:app:analyzeReleaseR8Config` (AGP 9.3+). CI structure tests lock the Gradle/manifest invariants; HTML reports stay local/CI artifacts.
3. **Memory:** custom `Application` records limiter kills from `ApplicationExitInfo` and handles `onTrimMemory` for `UI_HIDDEN` / `BACKGROUND` only. No `largeHeap`. Do not poll `getMemoryInfo`. No Crashlytics / Play Console.
4. **Compose 1.12:** keep BOM `2026.08.00`. Do not use deprecated `Modifier.onFirstVisible`. Mesh gradients and Credential Manager stay off the FOSS Golden Path (tokens + no Play Services).
5. **Grok Bots** are optional commercial ops (`docs/GROK_BOTS.md`), not a required agent.

## Alternatives considered

- Keep minify off for simpler crash stacks — rejected: Android 17 memory + cold start depend on R8.
- `-dontobfuscate` for readable FOSS stacks — rejected: Google’s keep-rule guidance; mapping.txt is the retrace path.
- Coil/Glide in Golden Path — rejected: no product image pipeline yet; document in MODULE.md.
- ProfilingManager heap-upload — rejected: needs a backend; FOSS crash path stays on-device sanitize + GitHub issues.

### Critique

| Issue | Resolution |
|-------|------------|
| Null/empty at boundary | `MemoryBudget.isLimiterKill` treats null/blank description as not a limiter kill; unit tests cover it |
| Network timeout | N/A — no new network I/O |
| Race | `CrashCapture.install` stays idempotent; limiter read is `runCatching` on `Application.onCreate` |
| Unhandled exceptions | `getHistoricalProcessExitReasons` wrapped in `runCatching`; Robolectric API 26 skips the API 30+ path |

## Consequences

- `assembleRelease` is slower (R8). Reproducible APK job still uses `SOURCE_DATE_EPOCH`.
- Release crash stacks need `mapping/release/mapping.txt` to retrace.
- Child apps add keeps only for proven reflection.
