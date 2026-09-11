# Feature: deep-link Settings → About → Feedback

## Intent
`goldenpath://settings/about/feedback` opens the feedback stack (Settings → About → Feedback).

## Validation
- Manifest intent-filter on `MainActivity`
- Fallback: instrumented nav smoke Settings→About→Feedback
- Fallback command: `./gradlew :app:connectedDebugAndroidTest` (or `/emulator`)

## Acceptance criteria

- ✅ Deep links into Feedback carry a sanitized subject when provided
- ✅ Invalid payloads fall back to the default Feedback route

## Smoke scenario

1. _Given_ a Feedback deep link
2. _When_ the app opens it
3. _Then_ Feedback is shown without crashing

## Container map

| Layer | Path |
|-------|------|
| Logic | stack feedback modules |
| View | Feedback screens |
| Tests | stack feedback / deep-link tests |
| Wiring | app bootstrap / manifest |

## Tests

- Automated: yes — covered by stack feedback tests when present

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack web`
