# Commercial Golden Path

For `--distribution-tier commercial` only. FOSS remains the template default.

## Activate

1. `[HUMAN]` approve commercial tier at init or `python3 scripts/sync-cursor-features.py --tier commercial --copy-commercial`
2. Follow [`CURSOR_COMMERCIAL_ACTIVATION.md`](CURSOR_COMMERCIAL_ACTIVATION.md)
3. Compliance rule: [`.cursor/rules/commercial-compliance.mdc`](../.cursor/rules/commercial-compliance.mdc)

## Playbook milestones

| Area | Do | Must not |
|------|-----|----------|
| License | Document product license / ToS; keep `THIRD_PARTY_LICENSES.md` | Pretend MIT covers proprietary SDKs |
| Monetization | IAP / subscriptions / Stripe / ads — ADR before wiring | Ship paid APIs without store policy review |
| Analytics / trackers | Firebase, Amplitude, etc. **with consent UX + privacy policy** | Silent install-time tracking |
| Crash | Crashlytics / Sentry OK when disclosed | Secrets in crash payloads |
| Auth | Sign in with Apple/Google, Credential Manager | Commit OAuth client secrets |
| Push | FCM allowed — see [`modules/android/COMMERCIAL.md`](../modules/android/COMMERCIAL.md) | Force FCM on FOSS path |
| Web | Cookie consent + gated snippets — [`modules/web/COMMERCIAL.md`](../modules/web/COMMERCIAL.md) | Load trackers before consent |
| Stores | Privacy nutrition labels / data-safety forms | Skip DPIA when processing personal data |

## Privacy

Update [`PRIVACY.md`](PRIVACY.md) / threat model when adding trackers. Opt-in or first-run disclosure is required even on commercial.

## FOSS CI

Default examples and FOSS gates stay free of proprietary SDKs. Commercial patterns live in docs and `*.commercial.example` files.
