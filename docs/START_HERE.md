# Start Here

> First file for humans and agents. Word list: [`help/GLOSSARY.md`](help/GLOSSARY.md) — [**Sacred**](help/GLOSSARY.md), [**Canon**](help/GLOSSARY.md), [**AGENT**](help/GLOSSARY.md) / [**HUMAN**](help/GLOSSARY.md) / [**ADB**](help/GLOSSARY.md) / [**AUTO**](help/GLOSSARY.md).

## Mode

- [**Bootstrap**](help/GLOSSARY.md) — new project from this template → write `AGENT.md`, then `docs/INITIALIZATION_PROMPT.md`
- [**Reference**](help/GLOSSARY.md) — rules only → `docs/FOR_AGENTS.md`

Cursor modes: Ask / Plan / Agent / Debug — [`CURSOR_MODES.md`](CURSOR_MODES.md).

## Three commands

| Need | Cursor | Elsewhere |
|------|--------|-----------|
| First run | `/tour` | Read [`help/TOUR.md`](help/TOUR.md) |
| New project | `/bootstrap` | Init + tour |
| What next | `/coach` | [`help/COACH.md`](help/COACH.md) |
Cheat sheet: [`help/BATCH_COMMANDS.md`](help/BATCH_COMMANDS.md). UI law: [`ux-ui-guidelines.md`](ux-ui-guidelines.md). Cline (free): [`help/CLINE.md`](help/CLINE.md). Optional Grok bots: [`GROK_BOTS.md`](GROK_BOTS.md).

On session start: name next 🔲 `[AGENT]` row; say if CHANGELOG `[Unreleased]` has notes (first ~20 lines only).

## Read order (when needed)

1. `README.md` → this file → `CURSOR_MODES.md`
2. `AGENTS.md` → `BUILD_PLAN.md` Sequential
3. Active `modules/{stack}/` + `examples/{stack}/` only
4. UI → `DESIGN_GUIDE.md` + `ux-ui-guidelines.md`

Session protocol (short): [`AGENTS.md`](../AGENTS.md) · cost diet [ADR-0009](adr/0009-cost-diet-brevity.md) · session checklist [`help/SESSION_START.md`](help/SESSION_START.md).

**First-time path: Cline (free).** Open this project in Cursor or VS Code. Install recommended extensions if prompted, or search Extensions for Cline (`saoudrizwan.claude-dev`). Click the Cline icon, Sign In with GitHub (Google/email ok). Do not paste API keys, install Codex, or set `OPENAI_API_KEY`. Set API Provider = Cline and pick a FREE model. Type `/tour` (enable workflows under Rules & Workflows if needed) or paste: `Read docs/help/TOUR.md and walk me through it. Follow AGENTS.md.` Review every diff; run `python3 scripts/agent-run.py verify` before trusting changes. Full steps: [`help/CLINE.md`](help/CLINE.md) · VS Code `/` map: [`help/VSCODE_COMMANDS.md`](help/VSCODE_COMMANDS.md).

Optional local Ollama path: [`LOCAL_MODELS.md`](LOCAL_MODELS.md) · [`help/LOCAL_AGENT.md`](help/LOCAL_AGENT.md) · `python3 scripts/agent-run.py recommend-model` / `setup-local`.

In Windsurf, Antigravity, or any other agent: ask it to read [`docs/help/TOUR.md`](help/TOUR.md) (first run) or [`docs/help/COACH.md`](help/COACH.md) (what next).

Optional commercial Grok Bots (not required to build or ship): [`GROK_BOTS.md`](GROK_BOTS.md). OpenSSF Best Practices (project 14564): [`OPENSSF_BEST_PRACTICES.md`](OPENSSF_BEST_PRACTICES.md).
