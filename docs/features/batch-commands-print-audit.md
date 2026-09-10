# Feature: batch-commands-print-audit

> Print cheat sheet stays synced, accessible, and Settings-only in the header.

## Acceptance criteria

- ✅ Committed HTML matches `batch_commands_print.py --write`
- ✅ Column headers use `<th scope="col">`; header/lead never mention Theme, donate, or About
- ✅ `/tour` and `/coach` captions mention Settings-only chrome

## Smoke scenario

1. _Given_ the print JSON and HTML
2. _When_ `python3 scripts/lib/batch_commands_print.py --check` runs for all registry names
3. _Then_ sync and a11y/Settings-only audits pass

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/batch_commands_print.py`, `scripts/lib/batch_commands_print_audit.py` |
| View | `docs/help/batch-commands-print.html` |
| Tests | `tests/test_batch_commands_print.py` |
| Wiring | `scripts/check-batch-commands.sh` |

## Tests

- Automated: yes — render sync, `scope="col"`, Settings-only captions
- Coverage: missing Settings-only tour caption

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
