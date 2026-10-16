# Web — Commercial distribution patterns

> Not used on FOSS bootstrap. For `--distribution-tier commercial` only.

## Allowed (when documented + consent)

- Stripe / Paddle / similar for payments
- Analytics (Plausible self-host is FOSS; GA/Amplitude when consented)
- Error tracking (Sentry) with scrubbed PII
- Cookie / consent banners before non-essential scripts

## Must

- Privacy policy link in About/Settings
- No tracker scripts on first paint before consent
- ADR for each proprietary SaaS SDK
- Never commit API keys; use env / CI secrets

## FOSS path

Default Vite PWA Golden Path ships without trackers or payment SDKs.
