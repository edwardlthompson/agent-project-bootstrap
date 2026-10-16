# Spec: Commercial Golden Path

## Goal
Full playbook for paid/closed apps with monetization and trackers on commercial tier only.

## Trigger / users
Init with --distribution-tier commercial; tour/coach on commercial children.

## Requirements
- docs/COMMERCIAL_GOLDEN_PATH.md covers license, IAP/ads/Stripe, analytics with consent, crash SDKs, auth, FCM, store privacy.
- modules/web/COMMERCIAL.md for web monetization/consent.
- Expand commercial-compliance.mdc for documented trackers/monetization.
- Tour/coach point at commercial playbook when tier is commercial.
- FOSS CI unchanged; no proprietary SDKs in default examples.

## Out of scope
Making trackers FOSS default; silent tracking.

## Acceptance checks
- COMMERCIAL_GOLDEN_PATH.md exists; FOSS integrations check still passes.

## Assumptions (flagged)
- Consent + privacy policy required on commercial.

## Open questions
None.

## Files likely touched
docs/COMMERCIAL_GOLDEN_PATH.md, modules/web/COMMERCIAL.md, .cursor/rules/commercial-compliance.mdc, docs/help/TOUR.md, tests/
