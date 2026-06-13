# Module B: Web / Static Sites / Progressive Web Apps (PWAs)

> Activate when your stack includes web, static sites, or PWAs.

## Requirements (Verbatim)

- **PWA & Cache Integrity:** Enforce fully compliant PWA manifests, offline-first service workers, and responsive, high-performance offline caching strategies.
- **Asset Optimization & Audits:** Enforce automated asset minification, image compression, responsive media rendering, and build-time HTML/CSS validation. Builds must fail if Lighthouse performance, accessibility, or best-practice scores fall below target budgets.

## Repository layout

Read [`docs/WEB_PROJECT_LAYOUT.md`](../../docs/WEB_PROJECT_LAYOUT.md) before moving or creating site files.

| Path | Role |
|------|------|
| `docs/` | Agent documentation — **not** the public website |
| `examples/web/` | PWA source (Vite, TypeScript, tests) |
| `examples/web/dist/` | Build output published via GitHub Actions |
| `site/` or `website/` | Optional non-PWA static site only |

## GitHub Pages hosting

- Source: `examples/web/` — edit and test here
- Deploy: [`.github/workflows/pages.yml`](../../.github/workflows/pages.yml) builds `dist/` on push to `main`
- Settings: Pages source must be **GitHub Actions**, not "Deploy from `/docs`"
- Base path: workflow sets `VITE_BASE_PATH=/${{ github.event.repository.name }}/` for project-site URLs
- FOSS: no analytics or tracking scripts in the template workflow

If you prune the web stack during init, disable `pages.yml` and turn off GitHub Pages in repo settings.

## Localization

Strings are separate from styles. See [`docs/DESIGN_GUIDE.md`](../../docs/DESIGN_GUIDE.md).

| Layer | Path | API |
|-------|------|-----|
| Strings | `src/locales/en.json` | `t(key)` from `src/i18n/index.ts` |
| Styles | `style.css`, `design-tokens.css` | `var(--gp-*)` only — no user copy |
| Theme | `theme.ts` | Preference only; labels from `t()` |

Default locale: English only. Add `src/locales/{lang}.json` when shipping translations.

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
- [x] i18n scaffold (`src/locales/`, `src/i18n/`) — see `docs/DESIGN_GUIDE.md`
- [ ] Confirm GitHub Pages uses Actions workflow (not `/docs` folder source)

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
| GitHub Pages source setting (Actions vs /docs) | `HUMAN` |
