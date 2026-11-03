# Feature: agent-mode-switch

> Repo-wide Agent Mode (`speed` / `balanced` / `lean`) to cut Cursor token spend. Checklist: 🔲 open · ✅ done · ❌ blocked.

## Acceptance criteria

- ✅ `/lean`, `/balanced`, `/speed`, `/mode` work via `.cursor/commands/`
- ✅ Mode is read from `.cursor/agent-mode.json` (missing ⇒ balanced)
- ✅ Lean converts open `🔲 [AGENT][CLOUD]` → `🔲 [AGENT][LOCAL]`
- ✅ Lean refuses Cloud Agent / Grok Bot execution
- ✅ Default on new child repos is `balanced` (init writes the file)
- ✅ ADR-0010 documents the decision

## Smoke scenario

1. _Given_ a BUILD_PLAN with an open `[AGENT][CLOUD]` row
2. _When_ the human runs `/lean` (or `python3 scripts/agent-run.py set-agent-mode --mode lean`)
3. _Then_ mode is lean, the row is LOCAL, and `/status` reports Cloud blocked

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/agent_mode.py` |
| View | `.cursor/commands/{lean,balanced,speed,mode}.md` |
| Tests | `tests/test_agent_mode.py` |
| Wiring | `.cursor/agent-mode.json`, `.cursor/rules/agent-mode.mdc` |

## Tests

- Automated: yes — `tests/test_agent_mode.py`
- Coverage: load/default, set mode, CLOUD→LOCAL conversion idempotence

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py set-agent-mode --mode balanced && python3 scripts/agent-run.py repo-status`

## Notes

- ADR: [`docs/adr/0010-agent-mode-speed-balanced-lean.md`](../adr/0010-agent-mode-speed-balanced-lean.md)
