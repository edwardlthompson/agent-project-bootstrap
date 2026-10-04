# Local agent (Cline + Ollama)

Optional fully local path for coding agents. This template does **not** require Ollama. Free-tier Cline first-run: [`CLINE.md`](CLINE.md). Hardware tiers and Modelfiles: [`docs/LOCAL_MODELS.md`](../LOCAL_MODELS.md). Failures: [`LOCAL_TROUBLESHOOTING.md`](LOCAL_TROUBLESHOOTING.md).

## Quick setup

```bash
python3 scripts/agent-run.py recommend-model
python3 scripts/agent-run.py setup-local
# When the base model is already pulled:
python3 scripts/agent-run.py setup-local -- --apply
```

## Cline settings (paste targets)

| Setting | Value |
|---------|--------|
| API Provider | Ollama |
| Base URL | `http://127.0.0.1:11434` (default) |
| Model | Custom name from setup (e.g. `qwen3-coder-agent-64k`) |
| Context Window | Match Modelfile `num_ctx` (65536 for 64k templates) |
| Compact Prompts | On when the setting exists |
| Plan / Act | Plan first for multi-file work |

## Hard rules under Cline + Qwen

1. **Anthropic-style XML tool calls only.** Never emit raw JSON tool calls like `{"name":"...","arguments":{...}}` — that causes infinite retry loops.
2. Prefer the smallest correct change. Read before write. Run the smallest relevant verification after every change.
3. Keep replies short (1–3 sentences) unless the human asks for more.
4. Before multi-file work, restate the single next BUILD_PLAN row and the verification command.
5. Same tool call or same error three times → stop and ask the human.
6. When context grows long, update `.agent/session-state.md` (and milestone `AGENT_MEMORY.md`) instead of relying on chat history.

Template rules: `.clinerules/AGENTS.md` (pointer + short hard block). Source of truth: root [`AGENTS.md`](../../AGENTS.md).

## Recommended workflow

1. Session start: [`SESSION_START.md`](SESSION_START.md).
2. One focused objective per chat; start fresh on topic change.
3. Prefer `grep` / targeted slices over dumping whole files.
4. Compact / summarize before the window is ~75% full (`/compact` workflow or Cline `/smol`).
5. Declare venue `[AGENT][LOCAL]` when using Ollama/LM Studio.

## Recover from a loop

1. Stop the task in Cline.
2. If Ollama is hung: `ollama stop <model>` and restart the Ollama service.
3. Clear or compress context (`/smol` or `/compact`).
4. Re-state a **single** next BUILD_PLAN row and the verify command.
5. If XML/JSON tool loops persist, confirm the custom Modelfile SYSTEM prompt and `.clinerules/AGENTS.md` hard block are loaded.

## Slash commands in VS Code

Type `/` in Cline chat (enable workflows under Rules & Workflows / scale icon if missing). Cheat sheet: [`VSCODE_COMMANDS.md`](VSCODE_COMMANDS.md).
