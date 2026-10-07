# Branding kit

Replaceable product identity for projects bootstrapped from **agent-project-bootstrap**.

**Parent template mark** (2D human↔robot handshake) and photoreal README splash live under [`template/`](template/) and are **not** synced into apps. See [`template/IDENTITY.md`](template/IDENTITY.md). Child products own everything under `assets/` + `product.json`. Rebrand with `/brand` (or follow the checklist below).

## Single sources of truth

| Concern | Edit here | Then run |
|---------|-----------|----------|
| Colors, type, spacing | [`design-tokens/design-tokens.json`](../design-tokens/design-tokens.json) | `python3 scripts/sync-design-tokens.py` |
| Logos / favicon / heroes | [`branding/assets/`](assets/) | `python3 scripts/sync-design-tokens.py` |
| Name, pitch, README copy | [`branding/product.json`](product.json) | `python3 scripts/generate-project-readme.py` |
| Voice guidelines | [`branding/voice.md`](voice.md) | (docs only) |

Official color stylesheet (generated): [`official-colors.css`](official-colors.css).

## Creative brief (fill before the mark)

Answer these in one short pass (agent asks; human confirms):

1. **Audience** — who opens the app on day one?
2. **One promise** — the outcome in one sentence (becomes tagline seed).
3. **Three adjectives** — tone (e.g. calm, precise, playful). Avoid hype words.
4. **Do / don’t** — one visual do, one visual don’t (e.g. “geometric mark / no mascot”).

Do not finalize SVGs until name + tagline + promise are set in `product.json`.

## Catchy logo rules

- **One silhouette at 16px** — the mark must read as a single shape in a favicon.
- **Works monochrome** — ship `logo-mark-mono.svg`; no meaning that depends on color alone.
- **Clear space** — at least 1/8 of the mark’s width as padding around the mark.
- **No text in the mark** — wordmark is separate (`logo-wordmark.svg` / lockup).
- **Differentiate from the Golden Path triangle** — children must replace the placeholder, not tweak its color only.
- **Prefer mark-on-dark** (surface ink) or mono mark on light surfaces.
- Check contrast for primary on surface in both themes after token edits (`check-token-contrast` / design cohesion).

## Name, tagline, pitch

1. Set `"mode": "product"` in child repos (never on the upstream template).
2. Fill `name`, `short_name`, `tagline`, `pitch`, `features` in [`product.json`](product.json).
3. Match UI title (`app.title` / `app_name`) to `product.json` `name`.
4. Run `python3 scripts/generate-project-readme.py`.

Pitch formulas: [`voice.md`](voice.md).

## Splash / first paint

Brand splash is **system continuity**, not a marketing carousel.

| Rule | Detail |
|------|--------|
| Same mark everywhere | App icon = favicon = Android 12+ SplashScreen icon = `logo-mark.svg` |
| Background | Surface token (light/dark), not a one-off hex |
| Duration | Perceived flash ≤ ~300ms; never gate content behind splash |
| Motion | Honor `prefers-reduced-motion`; no looping logo animation |
| Continuity | Splash → first frame uses the same colors (no white flash → dark app) |
| Web | `theme-color` + favicon match tokens; first paint matches Settings theme |
| Android | SplashScreen API + `windowSplashScreen*` / theme using brand drawable (`ic_brand_mark`) |
| Forbidden | Onboarding carousels as splash; donate/update dialogs as “splash”; content locked until animation ends |

Golden Path Android stub: `Theme.GoldenPath.Splash` → `MainActivity` installs the splash then switches to `Theme.GoldenPath`. See [`docs/DESIGN_GUIDE.md`](../docs/DESIGN_GUIDE.md).

## Asset inventory

| File | Use |
|------|-----|
| `assets/logo-mark.svg` | App mark; synced to web `icon.svg` / `logo.svg` |
| `assets/logo-mark-mono.svg` | Monochrome / print |
| `assets/logo-wordmark.svg` | Wordmark only |
| `assets/logo-lockup.svg` | Mark + wordmark |
| `assets/favicon.svg` | Browser tab |
| `assets/app-icon-512.svg` | Vector SoT; raster `icon.png` via `blender-icons` (`[AGENT]`/`[AUTO]`), not a HUMAN export |
| `assets/readme-hero.svg` | README banner |
| `assets/social-preview.svg` | GitHub / OG 1280×640 (upload PNG export in repo Settings → Social preview) |

Parent-only assets: [`template/`](template/) — see [`template/IDENTITY.md`](template/IDENTITY.md).

## Rebrand checklist

Prefer `/brand` in Cursor. Manual path:

1. Complete the creative brief (above).
2. Update `meta.name` and colors in `design-tokens/design-tokens.json`.
3. Replace SVGs under `branding/assets/` (keep filenames). Sacred: never overwrite via icon-factory.
4. Fill `branding/product.json` (set `"mode": "product"` in child repos).
5. Run `python3 scripts/sync-design-tokens.py`.
6. Run `python3 scripts/generate-project-readme.py`.
7. Align UI strings (`locales` / `strings.xml`), `manifest.webmanifest`, and GitHub About.
8. Confirm splash / `theme-color` / Android splash theme still use the synced mark.
9. Export PNGs for F-Droid / social preview when ready — do not commit large binaries unless intentional.

## Template vs product README

- `"mode": "template"` (default here) — generator writes only `generated/README.preview.md`; root `README.md` stays the template guide (logo `template/logo-mark.png`, splash `template/readme-splash.jpg`).
- `"mode": "product"` — generator overwrites root `README.md` with the pitch README. **Never** set this on the upstream template.

## Store listing sizes

See [`examples/android/metadata/en-US/images/README.md`](../examples/android/metadata/en-US/images/README.md) for `icon.png` and `featureGraphic.png`. Source art: `app-icon-512.svg` and `social-preview.svg`.
