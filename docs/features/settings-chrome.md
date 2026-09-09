# Feature: settings-chrome

> Minimal home chrome and glanceable Settings/About menus for Golden Path (M49).

## Acceptance criteria

- ✅ Home header / TopAppBar has **one** trailing action: Settings
- ✅ Theme, About, and donate never appear in home chrome
- ✅ Theme is a dropdown under Settings → Appearance (system / light / dark); no chips for exclusive enums
- ✅ Settings groups scan in order: Appearance → Privacy → Data (export/import JSON) → About
- ✅ About groups scan in order: App → Support → Feedback; feedback is a dropdown
- ✅ Donate links live only under Settings → App info
- ✅ Offline: menus render from local state; no network required
- ✅ Accessibility: Settings control is labeled; dropdowns have visible labels; touch targets ≥ 44px / 2.75rem
- ✅ i18n: `nav.back`, `settings.section.*`, `about.section.*`, `about.feedback.*`

## Smoke scenario

1. Given the Golden Path is at home
2. When the user opens Settings, changes theme via the dropdown, then opens App info
3. Then the header never showed theme/About/donate; About lists version and donate links; Back/Escape returns one level

## Container map

| Layer | Web | Android |
|-------|-----|---------|
| Logic | `examples/web/src/theme.ts`, `src/settings/` | `examples/android/.../ui/theme/` |
| View | `AppShell.ts`, `components/SettingsPanel.ts`, `AboutPanel.ts` | `ui/GoldenPathScreen.kt`, `ui/settings/`, `ui/about/` |
| Tests | `AppShell.test.ts`, `e2e/app.spec.ts` | `GoldenPathUiTest.kt`, `NavBarInsetUiTest.kt` |
| Wiring | `appBootstrap.ts` | `GoldenPathApp.kt` |

## Tests

- Automated: yes — `examples/web/src/AppShell.test.ts`, `examples/web/e2e/app.spec.ts`, Android `GoldenPathUiTest.kt`
- Coverage: chrome absence + Settings → App info path

## Fallback validation

- Why tests are not feasible: N/A (automated tests exist). Instrumented Android tests need an emulator (`[ADB]`).
- Command: `python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto`

## Notes

- Contract: [`docs/DESIGN_GUIDE.md`](../DESIGN_GUIDE.md) Chrome and menus; ADR [`docs/adr/0004-settings-chrome.md`](../adr/0004-settings-chrome.md)
- After each AGENT step: `bash scripts/watch-agent-gates.sh --once --autofix`
