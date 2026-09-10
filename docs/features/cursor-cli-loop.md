# Feature: cursor-cli-loop

> Local no-Cloud Cursor CLI loop. API key optional. No git push.

## Acceptance criteria

- ✅ Zero-key loop names validate-bootstrap, watch-agent-gates, and render-gates-status
- ✅ Optional CLI path requires `CURSOR_API_KEY` and denies `git push`
- ✅ GitHub Actions example stays `workflow_dispatch` only

## Smoke scenario

1. _Given_ no `CURSOR_API_KEY`
2. _When_ the zero-key loop in `docs/CURSOR_CLI.md` is run
3. _Then_ local gates run without Cloud billing

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/cursor_cli.py` |
| View | `docs/CURSOR_CLI.md` |
| Tests | `tests/test_cursor_cli.py` |
| Wiring | `scripts/check-cursor-cli.sh` |

## Tests

- Automated: yes — recipe needles
- Coverage: missing Local loop heading

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
