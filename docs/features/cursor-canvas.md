# Feature: cursor-canvas

> Walkthrough for gate Canvas vs web Design Mode. Settings-only chrome.

## Acceptance criteria

- ✅ `docs/CURSOR_CANVAS.md` names `render-gates-status` and markdown fallback
- ✅ Design Mode is web/PWA only and keeps Settings-only chrome
- ✅ `CURSOR_MODES.md` links the walkthrough

## Smoke scenario

1. _Given_ `/gates`
2. _When_ the walkthrough is followed
3. _Then_ agents render Canvas or a markdown table and do not open Design Mode for Android-only work

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_canvas.py` |
| View | `docs/CURSOR_CANVAS.md` |
| Tests | `tests/test_cursor_canvas.py` |
| Wiring | `scripts/check-cursor-canvas.sh` |

## Tests

- Automated: yes — needles + CURSOR_MODES link
- Coverage: missing Design Mode

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
