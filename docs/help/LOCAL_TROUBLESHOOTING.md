# Local agent troubleshooting

Companion to [`LOCAL_AGENT.md`](LOCAL_AGENT.md) and [`docs/LOCAL_MODELS.md`](../LOCAL_MODELS.md).

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Infinite tool retries / “invalid tool” | Qwen emits OpenAI JSON; Cline expects Anthropic XML | Use a Modelfile from `templates/ollama/` (SYSTEM forces XML). Confirm `.clinerules/AGENTS.md` hard block. Restart the task. |
| Model “forgets” the plan mid-task | Silent context truncation (default `num_ctx` too small) | Custom Modelfile with `num_ctx` ≥ 32768 (prefer 65536 on 24 GB). Externalize state to `.agent/session-state.md`. Compact earlier. |
| “Model is stupid after 20 minutes” | Almost always context truncation / compression | Same as amnesia: raise context, fresh chat, paste `compress-memory` output. |
| Extreme slowdown after load | VRAM pressure → CPU offload | Enable `OLLAMA_FLASH_ATTENTION=1` + `OLLAMA_KV_CACHE_TYPE=q8_0`. Lower `num_ctx` or use a smaller model/quant. `OLLAMA_NUM_PARALLEL=1`. |
| OOM / process killed | Context + model too large for VRAM | Drop to budget/entry Modelfile; free VRAM (`ollama stop`); reduce parallel loads. |
| Stuck generating / hung | Server or sampler loop | `ollama stop <model>`, restart Ollama, mildly raise `repeat_penalty` / lower `temperature` in Modelfile. |
| Re-reads the same files forever | Read loop | 3-strike rule: halt. Prefer grep. Max two identical reads without a write or new plan (`AGENTS.md`). |
| Workflows missing under `/` | Toggle not enabled | Cline → Rules & Workflows (scale icon) → enable project workflows. Or paste the portable prompt from [`VSCODE_COMMANDS.md`](VSCODE_COMMANDS.md). |
| `setup-local --apply` fails | Base model not pulled | Run the printed `ollama pull …` first; never auto-pulls. |
| `recommend-model` says entry tier with a 4090 | Probe failed (`nvidia-smi` missing/timeout) | Install NVIDIA drivers / add `nvidia-smi` to PATH; re-run. |

## Commands

```bash
python3 scripts/agent-run.py recommend-model
python3 scripts/agent-run.py check-local-compute
python3 scripts/agent-run.py compress-memory
ollama ps
ollama list
```
