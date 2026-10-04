# VS Code + Cline slash commands

Cursor native `/` commands live under `.cursor/commands/` and only work inside Cursor. In stock VS Code with Cline, use **project workflows** under `.clinerules/workflows/` — same short names — or paste a portable prompt.

Cursor users are unaffected: keep using `.cursor/commands/`.

## How to invoke

1. Open Cline chat.
2. Type `/` — pick a workflow (e.g. `/tour`, `/build`). Some builds show `/tour.md`.
3. If nothing appears: Rules & Workflows (scale icon) → enable the project workflows, then retry.
4. Or paste the portable line from the table below.

## Mapping

| Intent | Cursor | Cline (VS Code) | Any agent (paste) |
|--------|--------|-----------------|-------------------|
| First-run tour | `/tour` | `/tour` | `Read docs/help/TOUR.md and walk me through it. Follow AGENTS.md.` |
| One next action | `/coach` | `/coach` | `Read docs/help/COACH.md and give me one next action.` |
| Execute BUILD_PLAN | `/build` | `/build` | `Read BUILD_PLAN.md, take the next open [AGENT] row, and execute it following AGENTS.md.` |
| Verify | `/verify` | `/verify` | `Run python3 scripts/agent-run.py verify and explain the first failure only.` |
| Ship / release | `/ship` | `/ship` | Follow ship / pre-release docs; surface HUMAN gates. |
| New project | `/bootstrap` | `/bootstrap` | Point at `docs/INITIALIZATION_PROMPT.md` + init scripts. |
| Gates | `/gates` | `/gates` | Run validate-bootstrap / feature-gate for the active stack. |
| Ideas | `/ideas` | `/ideas` | `Read docs/help/IDEAS.md and give a ranked short list (do not implement).` |
| Compress context | `/compact` | `/compact` (+ built-in `/smol`) | Summarize durable state into session-state / AGENT_MEMORY. |
| Local Ollama setup | (docs) | `/setup-local` | `Run python3 scripts/agent-run.py setup-local and follow docs/help/LOCAL_AGENT.md.` |
| Gate autofix | `/fix` | `/fix` | Follow `.cursor/commands/fix.md` / watch-agent-gates autofix; follow AGENTS.md. |
| ADR | `/adr` | `/adr` | `Read docs/help/ADR.md and write one ADR under docs/adr/.` |

## Recovery if `/` fails

1. Paste the portable prompt from the table.
2. Open the Workflows tab (scale icon) and run the workflow from the UI.
3. Ask: “Execute the procedure described in docs/help/TOUR.md” (or the relevant help file).
4. Cursor-only features with no Cline twin: use the paste path; do not expect `.cursor/commands/` to run in stock VS Code.

More: [`CLINE.md`](CLINE.md) · [`BATCH_COMMANDS.md`](BATCH_COMMANDS.md) · [`LOCAL_AGENT.md`](LOCAL_AGENT.md).
