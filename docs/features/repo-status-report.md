# Feature: repo-status-report

> `/status` — pure-read settings + golden-path report. Checklist: 🔲 open · ✅ done · ❌ blocked.

## Acceptance criteria

- ✅ `/status` prints the full scannable report (agent mode, distribution tier, stacks, venue policy, local compute, key config files, cost-diet note, last mode change, open BUILD_PLAN LOCAL/CLOUD counts, next row, ADR pointers)
- ✅ Pure read — no writes, no mode changes
- ✅ Unknown values print `unknown` (or a clear placeholder) without failing the whole report

## Smoke scenario

1. _Given_ `.cursor/agent-mode.json` and `BUILD_PLAN.md` exist
2. _When_ the human runs `/status`
3. _Then_ a single report includes Agent mode, Venue policy, and Open BUILD_PLAN summary

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/repo_status.py` |
| View | `.cursor/commands/status.md` |
| Tests | `tests/test_repo_status.py` |
| Wiring | `scripts/repo-status.sh` |

## Tests

- Automated: yes — `tests/test_repo_status.py`
- Coverage: report contains required section headers; missing mode file ⇒ balanced

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py repo-status`

## Notes

- Companion: [`agent-mode-switch.md`](agent-mode-switch.md) · ADR-0010
