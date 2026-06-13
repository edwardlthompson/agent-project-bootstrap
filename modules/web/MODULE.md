# Module B: Web / Static Sites / Progressive Web Apps (PWAs)

> Activate when your stack includes web, static sites, or PWAs.

## Requirements (Verbatim)

- **PWA & Cache Integrity:** Enforce fully compliant PWA manifests, offline-first service workers, and responsive, high-performance offline caching strategies.
- **Asset Optimization & Audits:** Enforce automated asset minification, image compression, responsive media rendering, and build-time HTML/CSS validation. Builds must fail if Lighthouse performance, accessibility, or best-practice scores fall below target budgets.

## Activation Checklist

- [ ] Add `manifest.webmanifest` with required fields
- [ ] Implement offline-first service worker
- [ ] Configure Lighthouse CI budgets (`.lighthouserc.json`) with `numberOfRuns: 3` and median assertion; keep `minScore: 0.9` for performance (do not lower budget for CI flake)
- [ ] Set up axe-core accessibility tests in Playwright
- [ ] Review `examples/web/` Golden Path stub
- [ ] Add visual regression snapshots for key pages
- [ ] Enforce bundle size budgets in CI
- [ ] Keyboard-only navigation smoke test checklist
- [ ] Respect `prefers-reduced-motion` and `prefers-color-scheme`
- [ ] i18n extraction workflow if multi-locale (see module guide)

## Operations (when deployed as service)

- [ ] Health/readiness endpoints or documented static equivalent
- [ ] Structured logging standard per `docs/RUNBOOK.md`

## Golden Path Reference

See `examples/web/` for Vite + TypeScript PWA with Vitest, Playwright, and Lighthouse CI.

## Owner Labels for This Module

| Task type | Label |
|-----------|-------|
| Scaffold PWA, tests, CI config | `AGENT` |
| Lighthouse budget threshold approval | `HUMAN` |
| CI Lighthouse/axe gate enforcement | `AUTO` |
