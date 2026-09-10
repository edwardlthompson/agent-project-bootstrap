# Feature: tour-coach-chrome

> `/tour` and COACH teach Settings-only home chrome.

## Acceptance criteria

- ✅ `docs/help/TOUR.md` says Theme/About/donate live in Settings/About
- ✅ `docs/help/COACH.md` rejects putting Theme or donate in the header
- ✅ Gate is wired into validate-bootstrap

## Smoke scenario

1. _Given_ `/tour` or `/coach`
2. _When_ the help file is read
3. _Then_ the agent is told home chrome is Settings-only

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/tour_coach_chrome.py` |
| View | `docs/help/TOUR.md`, `docs/help/COACH.md` |
| Tests | `tests/test_tour_coach_chrome.py` |
| Wiring | `scripts/check-tour-coach-chrome.sh` |

## Tests

- Automated: yes — needles in both help files
- Coverage: missing Settings-only

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
