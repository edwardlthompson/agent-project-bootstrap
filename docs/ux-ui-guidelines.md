# UX & UI guidelines (construction law)

> **How to ship UI**, not a post-hoc audit. Golden Path tokens and Settings-only chrome: [`DESIGN_GUIDE.md`](DESIGN_GUIDE.md). `/ux-review` scores the same law and writes every change to the BUILD_PLAN **UX inventory**. `/ux-apply UX-NNN` implements one inventory item.

When you add or change a view, copy, nav, or form: **follow this file**. If you notice a gap you cannot fix in this slice, append a `UX-NNN` inventory item **in the same turn**. Do not wait for `/ux-review`. Do not hide work as backlog, later, or optional.

## Principles

1. **Clarity over decoration.** Users always know where they are, what they can do, and what happens next.
2. **Speed of understanding.** Scan in seconds. Hierarchy before color. Labels before icons-only.
3. **Feedback in &lt;200ms.** Clicks, taps, saves, errors, and success acknowledge immediately.
4. **Progressive disclosure.** Show what is needed now; hide power until needed.
5. **Calm confidence.** Fewer competing accents, less visual noise, stronger defaults.
6. **Inclusive by default.** Keyboard, screen reader, contrast, motion, language, and small screens are first-class.
7. **Trust platform habits** (web, iOS, Android) unless breaking them is clearly better.
8. **Protect what is working.** Polish only when it reduces friction or raises perceived quality.
9. **Capture everything.** Incomplete plans are a process failure. Comprehensiveness beats sequencing.

## Visual language

- **Type:** One scale, few weights. Body readable at 16px equivalent. Line-height ~1.4–1.6. At most two font families; prefer system fonts or one well-loaded family (no FOIT).
- **Spacing:** 4px base (4, 8, 12, 16, 24, 32, 48, 64). No magic numbers. Use Golden Path tokens (`DESIGN_GUIDE.md`).
- **Color:** Semantic tokens only (`bg`, `surface`, `text`, `muted`, `border`, `primary`, `danger`, `success`, `warning`). No raw hex in components.
- **Contrast:** Text ≥ 4.5:1 (large text ≥ 3:1). UI components ≥ 3:1 against adjacent colors. Run `check-token-contrast`.
- **Radius & elevation:** One radius scale, one shadow scale. Do not invent a new card style per page.
- **Icons:** One family, same stroke, 20/24px grid. Icon-only controls need accessible names.
- **Density:** Comfortable default; compact only with an explicit density control.
- **Imagery:** Optional, consistent, never a substitute for a clear next action. No AI-slop illustrations or random gradients.

## Interaction and motion

- One **primary** action per view. Secondary/tertiary quieter. Destructive separate, confirmed, reversible when possible.
- Hover, focus, active, and disabled for every control. Focus rings visible — never `outline: none` without a replacement.
- Touch targets ≥ 44×44px (hit area can exceed the visual).
- Motion 150–300ms. Ease-out enter, ease-in exit, ease-in-out large layout. Honor `prefers-reduced-motion`.
- Skeletons for content-shaped loading; spinners only for unknown short waits.
- Optimistic UI for cheap reversible actions; rollback with a clear in-place error (toasts confirm, they do not hold errors the user must fix).
- Do not block the whole app for a local save. Do not stack modals. Long tasks get pages, not dialogs.
- Sticky headers must not steal half the mobile viewport.

## Content and voice

- Plain language (~8th grade). Short labels. Verbs on buttons (`Save`, `Create project`, `Try again`).
- Visible label always. Placeholder is format/example, not the label.
- Errors: what happened + how to fix + keep the user’s data.
- Empty states: why empty + one primary CTA (+ optional secondary). Honest empty over fake sample data in production.
- Externalize strings (`t()` / `stringResource`). Rewrite weak microcopy when you touch a screen.

## Information architecture

- One obvious primary nav. Current location always indicated. Deep places get breadcrumbs or equivalent.
- Settings grouped by task, not by engineering module (see DESIGN_GUIDE chrome).
- Search/command palette if many destinations — discoverable (`?`), do not steal OS/browser shortcuts.
- Do not hide rare/destructive actions at the same weight as primary work.
- Tables: responsive cards or horizontal scroll with a sticky first column.

## Forms

- Labels above fields. Helper text under the field. Errors tied with `aria-describedby`.
- Validate on submit; optionally on blur for format. Do not yell on first keystroke.
- Preserve input on error. Autocomplete, `inputmode`, correct `type`/`name`.
- Multi-step: step position, back, no lost data. Disabled submit must say what is missing.

## Empty, error, permission, edge (must ship with the slice)

Cover at least: first-run empty, zero search results, offline/timeout, 403/404/500, permission denied + how to grant (ask in context), partial failure, session expired, rate limited. Hunt dead ends, unlabeled icons, trapped focus, unrecoverable errors, layout jump, content flash, fake clickables.

## Accessibility (WCAG 2.2 AA floor)

Keyboard Tab/Enter/Space/Escape; arrows in menus. Name, role, value. Do not rely on color alone. Zoom 200% usable. One `h1` per view + landmarks. Screen-reader path for the main job. AAA opportunities are inventory items, not excuses to skip AA.

## Responsive, themes, i18n

Mobile-first. No accidental horizontal scroll. Breakpoints as a scale. Dark mode via tokens, not invert; follow system with override. Text may grow ~30% in translation; RTL uses start/end. Locale date/time/number. Safe-area / notch padding on mobile web.

## Design system hygiene

Reuse existing components. Add tokens rather than special-casing a page. Flag one-offs. No new component library if Golden Path already has one — record the gap if it truly cannot meet this law.

## Performance as UX

Skeletons, last-good cache, no layout shift. Lazy-load below-the-fold images. Delayed taps are UX bugs.

**First-paint continuity:** splash / cold start uses the same mark and surface colors as the first frame (no white↔dark flash). Prefer system SplashScreen / `theme-color` over custom interstitial UIs. See [`branding/BRANDING.md`](../branding/BRANDING.md).

## Delight (still record; implement after clarity/a11y)

Honest hover/press/success. Empty-state personality that still helps. First-run aha without a 7-step carousel (Skip always available). Command palette / shortcuts for power users.

## Heuristics

Nielsen’s 10 plus: first-use vs power-user, tiny phone vs desktop, dark/light, slow CPU/network, interrupted flow, RTL/long copy. Embarrassing moments become inventory items (and you still record every other finding).

## Extra guardrails

Feature-flag empty labs must not look broken. Analytics events are not UX — if a tooltip is required to explain a button, the button is wrong. Print/reduced-data optional; contrast and keyboard are not.

## Conflict

If code and this law disagree, ship the **smaller** change that meets the law. Record any remaining larger change as `UX-NNN`. Never drop findings to keep the plan short.
