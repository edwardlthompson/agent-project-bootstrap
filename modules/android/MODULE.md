# Module A: Android / F-Droid Pure Compliance

> Activate when your stack includes Android or F-Droid distribution.

## Requirements (Verbatim)

- **Absolute FOSS Isolation:** No commercial or proprietary closed-source SDKs are permitted (e.g., no Google Play Services, Firebase, or closed telemetry trackers). Rely exclusively on open alternatives (e.g., UnifiedPush or native OS providers).
- **Reproducible Build Environment:** Lock all compiler toolchains and build dependencies using cryptographic hashes or strict versioning. Enforce determinism by eliminating compilation timestamps (using SOURCE_DATE_EPOCH or platform-equivalent) to ensure byte-for-byte reproducible binaries matching F-Droid verification targets.

## Activation Checklist

- [ ] Confirm no proprietary SDKs in `build.gradle.kts` / `build.gradle` dependencies
- [ ] Set SOURCE_DATE_EPOCH in build scripts and CI
- [ ] Pin Gradle wrapper (`gradlew`, `gradle-wrapper.jar`, `gradle-wrapper.properties`) and dependency versions
- [ ] Review `examples/android/` Golden Path stub
- [ ] Add [ADB] tasks to BUILD_PLAN for device/emulator verification
- [ ] Document F-Droid metadata path (Fastlane or manual)

## Operations Checklist

- [ ] Crash reporting via FOSS channel only (no proprietary trackers)
- [ ] UnifiedPush or native OS notification provider configured
- [ ] Reproducible build verified locally (`./gradlew assembleRelease` with fixed SOURCE_DATE_EPOCH)
- [ ] Signing keys stored outside repo; CI uses protected secrets
- [ ] Rollback procedure documented in docs/RUNBOOK.md
- [ ] F-Droid submission checklist reviewed before release

## Golden Path Reference

See `examples/android/` for FOSS Gradle/Kotlin skeleton. CI runs `./gradlew assembleDebug` on every push to `main`.

## Owner Labels for This Module

| Task type | Label |
|-----------|-------|
| Scaffold Gradle, Kotlin code, tests | AGENT |
| Emulator/device testing, F-Droid submit | ADB |
| FOSS dependency audit approval | HUMAN |
| CI Gradle compile / structure validation | AUTO |
