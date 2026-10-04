# Local models (no cloud keys)

Use a local OpenAI-compatible server so Cursor Chat or Cline can stay on this machine. The template never stores keys and never writes Cursor `settings.json`. This template repo does **not** require Ollama (maintainer declined 2026-09-10). The recipe below is for child repos and maintainers who want a local model.

Deep dive: [`docs/help/LOCAL_AGENT.md`](help/LOCAL_AGENT.md) · Troubleshooting: [`docs/help/LOCAL_TROUBLESHOOTING.md`](help/LOCAL_TROUBLESHOOTING.md) · VS Code slash twins: [`docs/help/VSCODE_COMMANDS.md`](help/VSCODE_COMMANDS.md).

## What this is (and is not)

- **Chat / inline edit** can talk to `http://127.0.0.1:11434/v1` (Ollama) or `http://127.0.0.1:1234/v1` (LM Studio).
- **Tab completion and Agent/tool quality** may still use Cursor’s own models depending on the product version. A local 7B model is not a drop-in for `/ship`.
- Do **not** set `CURSOR_API_KEY`, create OpenAI dashboard keys, or use tunnels.
- Model tags below are **recommendations** — adjust if the Ollama library renames them.

## Hardware tiers (coder agents)

| Tier | VRAM / unified | Practical models (Q4_K_M unless noted) | Suggested `num_ctx` |
|------|----------------|----------------------------------------|---------------------|
| Entry | ≤ 8 GB | `qwen2.5-coder:7b` (or 3b) | 8k–16k |
| Budget | 12–16 GB | `qwen2.5-coder:14b` | 16k–32k |
| **Sweet spot** | **24 GB** | **`qwen3-coder:30b` (MoE)**, `qwen3.6:27b`, `qwen2.5-coder:32b` | **32k–64k** |
| High | 32 GB+ | Larger MoE / denser 30–35B / 70B Q4 with offload | 64k–128k |
**24 GB + ≥48 GB system RAM (reference):** primary `qwen3-coder:30b` with a 64k custom Modelfile; leave headroom for KV cache. Always use a custom Modelfile — Ollama’s default `num_ctx` is far too small for agent loops.

## Probe and recommend

```bash
python3 scripts/agent-run.py check-local-compute
python3 scripts/agent-run.py recommend-model
python3 scripts/agent-run.py setup-local          # dry-run
python3 scripts/agent-run.py setup-local -- --apply   # create custom model if base is local
# or: just recommend-model / just setup-local / just local-agent

```

`ollama=up` means the loopback API responded. `/coach` may point here when that line is up.

## Ollama (preferred)

1. Install [Ollama](https://ollama.com) (local binary; no account required for localhost).
2. Pull a coder model that fits VRAM, for example `ollama pull qwen3-coder:30b` on 24 GB.
3. Create a custom model from a template Modelfile (elevated context + Anthropic-style XML tool-call SYSTEM prompt):

```bash
ollama create qwen3-coder-agent-64k -f templates/ollama/Modelfile.qwen3-coder-30b-64k

```

Other templates live under [`templates/ollama/`](../templates/ollama/). Keep the server on loopback only: **127.0.0.1:11434**.

### Server tuning (24 GB reference)

```bash
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE=q8_0
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
# optional global default (Modelfile PARAMETER num_ctx still wins per model)
export OLLAMA_CONTEXT_LENGTH=65536

```

**Persist:**

| Host | Approach |
|------|----------|
| Linux systemd | Drop-in under `/etc/systemd/system/ollama.service.d/override.conf` with `Environment=` lines, then `systemctl daemon-reload && systemctl restart ollama` |
| macOS launchd | Set env in the Ollama app’s launch agent / shell profile used by the service |
| Windows | System Properties → Environment Variables for the user that runs Ollama, then restart the Ollama service/app |
**Verify:** restart Ollama, load the custom model, check `ollama ps` and server logs for Flash Attention / KV cache type. If layers spill to CPU, lower `num_ctx` or use a smaller quant.

### Cursor Settings (GUI)

1. Cursor Settings → Models.
2. Override the OpenAI-compatible base URL to `http://127.0.0.1:11434/v1`.
3. The form may refuse an empty key. **type this in the GUI** (not a secret; never commit; never put in `.env`):

```
ollama

```

4. Add the model name exactly as `ollama list` shows it (prefer the custom `*-agent-*` name). Select only that local model.

If Cursor reports a CORS error: keep Ollama on localhost; update Cursor; **do not** bind the LAN or open a tunnel.

### Cline (VS Code or Cursor)

See [`docs/help/LOCAL_AGENT.md`](help/LOCAL_AGENT.md): Provider = Ollama, model = custom name, Context Window matching `num_ctx`, Compact Prompts on when available. Template slash twins: type `/` in Cline after enabling workflows ([`VSCODE_COMMANDS.md`](help/VSCODE_COMMANDS.md)).

## LM Studio (optional)

Same GUI steps with base URL `http://127.0.0.1:1234/v1` and the same GUI dummy string.

## Never

- GitHub Actions secrets for this path
- Copying the GUI dummy string into `.env`, `.env.example`, or `.cursor/mcp.json`
- Starting a second Ollama per `/best-of-n` worker (one server is enough)
- Making Ollama required for CI, init, or `/ship`

Broader Linux DX (caches, inotify, direnv): [`LINUX_DEV.md`](LINUX_DEV.md).
