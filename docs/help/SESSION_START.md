# Session start (any agent)

Portable checklist when Cursor slash commands are unavailable. Source of truth: [`AGENTS.md`](../../AGENTS.md).

1. Read `AGENTS.md`, then the next open 🔲 `[AGENT]` (or `[AGENT][LOCAL]`) row in `BUILD_PLAN.md`.
2. If using Ollama / LM Studio: run `python3 scripts/agent-run.py recommend-model` (or note the last recommendation) and declare venue `[AGENT][LOCAL]`.
3. Read the last ~20 lines of `AGENT_MEMORY.md` and current session state:
   - Portable / Cline: `.agent/session-state.md` (copy from `.agent/session-state.md.example` if missing)
   - Cursor: `.cursor-session-state.json` (from `/compact`)
4. Pick Cursor mode via [`docs/CURSOR_MODES.md`](../CURSOR_MODES.md) (Plan for non-trivial multi-file — especially when local).
5. State the **single** next action. In VS Code + Cline you can type `/coach`, `/build`, or `/tour` (see [`VSCODE_COMMANDS.md`](VSCODE_COMMANDS.md)).

Optional paste block: `python3 scripts/agent-run.py compress-memory`.
