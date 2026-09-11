## What's changed

$CHANGES

## Verify before promoting

- [ ] Required checks green on the release commit (`docs/CI_REQUIRED_CHECKS.md`)
- [ ] SBOM + OpenVEX assets attached (`gh release view`)
- [ ] **Instrumented tests:** Android `connectedDebugAndroidTest` ran on CI (path filter) or was intentionally skipped — do not treat unit-only green as device coverage
- [ ] Espresso ≥ 3.7.0 if instrumented suite touches Compose on API 36+
