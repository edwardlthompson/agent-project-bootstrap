# Baseline Profile / Macrobenchmark stub (FOSS)

No Google Play Baseline Profile Gradle plugin required. Child products may add
`androidx.benchmark:benchmark-macro-junit4` later for local Macrobenchmark on a
physical device / AOSP emulator.

Until then: keep cold-start smoke in instrumented tests and document startup in
`docs/SPRINT_SMOKE.md`. Do **not** add Play App Profile Installer proprietary APIs
on the FOSS path.
