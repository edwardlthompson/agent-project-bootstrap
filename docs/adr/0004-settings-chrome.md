# ADR-0004: Minimal chrome and glanceable Settings menus

- **Status:** Accepted
- **Date:** 2026-09-09
- **Deciders:** Template maintainer

## Context

Golden Path home chrome accumulated Settings, About, donate, and a theme toggle. Settings used `FilterChip` rows for exclusive enums. That fights Material 3 app-bar density (one or two trailing actions), Apple/Android Settings IA (grouped lists + disclosure rows), and Nielsen Norman grouping (scan by section, not by icon soup). Hick’s law also says extra header targets slow every first-run.

## Decision

1. **Home chrome is Settings-only.** Theme, About, and donate live under Settings → App info. Off-home Android uses Back; web hides the header Settings button and uses panel Close / Escape.
2. **Exclusive choices are dropdowns.** Theme and About feedback use `<select>` / `ExposedDropdownMenu`. Chips stay for collection filters/tags only — never for settings enums.
3. **Menus are sectioned and sorted.** Settings: Appearance → Privacy → Data → About. About: App → Support → Feedback. One control per row; section labels are secondary (`onSurfaceVariant`).
4. **Touch and labels.** Trailing Settings is a named control (web text; Android icon + `contentDescription`). Targets ≥ 44px / 2.75rem.

## Alternatives considered

- **Keep quiet header donate / About icon:** Rejected — duplicates Settings → App info and crowds the first screen.
- **Header theme toggle plus Settings dropdown:** Rejected — two places to set the same preference.
- **FilterChips for theme:** Rejected — chips are for filters, not mutually exclusive settings.

## Consequences

- Child apps start with a calm home screen; agents follow `docs/DESIGN_GUIDE.md` Chrome and menus.
- Web `ThemeToggle.ts` is removed; `initTheme()` plus Settings `<select>` remain.
- Donate walkthrough (`docs/help/DONATIONS.md`) no longer allows a web header donate control.

### Critique

| Issue | Resolution |
|-------|------------|
| Null/empty at boundary | Disabled/empty `donations.json` hides Support; feedback dropdown omitted if both callbacks missing |
| Network timeout | N/A — chrome and menus are local; update/donate fetch unchanged |
| Race conditions | Theme persist stays in existing DataStore / `localStorage` writers; no extra header listeners |
| Unhandled exceptions | Dropdown `onChange` ignores empty placeholder; About feedback resets the select after fire |
