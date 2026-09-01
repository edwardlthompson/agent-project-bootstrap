# Feature: navigation

> Golden Path route stack (Sprint M47). Schema lock before AppShell / BackHandler wiring.

## Acceptance criteria

- ✅ Navigation is a stack, not booleans (`showAbout` / `showSettings` / `showFeedback`)
- ✅ Opening a panel pushes; Close/Back pops one level
- ✅ Back never exits while a menu is open (`canPop` is true off home)
- ✅ At home (empty stack or `[home]`): `pop` is a no-op so first Back does not leave the app
- ✅ Serialize / deserialize persist the route stack and Settings/About/Feedback scroll
- ✅ Launch prompt is a modal overlay: Back dismisses the prompt one level and does not pop the route
- ✅ i18n: nav model has no user-visible strings; later wiring uses existing `settings.*` / `about.*` / `feedback.*` keys (`docs/DESIGN_GUIDE.md`)
- ✅ About → Report bug **pushes** feedback (stack `home → about → feedback`); Back returns to About, then home — does not flatten to home

## Smoke scenario

1. _Given_ the Golden Path is at home
2. _When_ the user opens About, then Report bug
3. _Then_ the stack is home → about → feedback; first Back shows About; second Back is home; neither Back leaves the app

## Container map

| Layer | Web | Android |
|-------|-----|---------|
| Logic | `examples/web/src/nav/` | `examples/android/.../ui/nav/` |
| View | later: `AppShell.ts` (not this row) | later: `GoldenPathApp.kt` / BackHandler |
| Tests | `examples/web/src/nav/nav.test.ts` | `src/test/.../ui/nav/NavTest.kt` |
| Wiring | later: `appBootstrap.ts` ≤10 lines | later: composition root ≤10 lines |

## Tests

- Automated: yes — `examples/web/src/nav/nav.test.ts` and `examples/android/app/src/test/java/dev/foss/goldenpath/ui/nav/NavTest.kt`
- Coverage: pure push/pop/persist/scroll; no DOM, no Activity

## Fallback validation

Required when Automated is **no**. Still name the smoke command when tests exist.

- Why tests are not feasible: N/A (automated tests exist)
- Command: `python3 scripts/agent-run.py feature-gate --stack web` (nav unit tests also: `npx vitest run src/nav/nav.test.ts` in `examples/web`, `./gradlew :app:testDebugUnitTest --tests dev.foss.goldenpath.ui.nav.NavTest` in `examples/android`)

## Definition of Done

- 🔲 Web history stack + persist wired in AppShell (M47 row 3)
- 🔲 Android BackHandler + persist wired in Golden Path UI (M47 row 4)
- ✅ Shared `NavState` + unit tests (this row)

## Notes

- Mirror types on both stacks; do not share a runtime
- Tiny nav module only — do not grow `AppShell.ts` / `GoldenPathApp.kt` in this row
- After each later AGENT step: `bash scripts/watch-agent-gates.sh --once --autofix --scope auto`
