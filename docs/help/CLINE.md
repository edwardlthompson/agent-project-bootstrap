# Cline first-run (Cursor)

Cline is the first-time agent for this project. It is **free**. Display name **Cline**. Marketplace id `saoudrizwan.claude-dev`.

Do **not** paste API keys. Do **not** install Codex. Do **not** set `OPENAI_API_KEY`.

## Steps

1. Open this project in Cursor.
2. Install recommended extensions if prompted, or search Extensions for Cline.
3. Click the Cline icon in the sidebar.
4. Sign In with GitHub (Google/email also ok). Do NOT paste API keys. Do NOT install Codex. Do NOT set OPENAI_API_KEY.
5. In Cline settings, API Provider = Cline. Pick a model tagged FREE.
6. Paste: `Read docs/help/TOUR.md and walk me through it. Follow AGENTS.md.`
7. Review every diff. Run `python3 scripts/agent-run.py verify` before trusting changes.

## Rules file

`.clinerules` already points at [`AGENTS.md`](../../AGENTS.md). Never put project rules in `.clinerules`. Edit `AGENTS.md`, then:

```bash
bash scripts/bootstrap-lifecycle.sh --sync-adapters
```

## How Cline works

Plan mode then Act mode. Use checkpoints. Approve file and command steps before they run.

Cline works beside Cursor Agent/Composer. Cline is the autonomous hands that replace Codex for a new user. Codex is optional later, not this first-run path.

Next: [`TOUR.md`](TOUR.md).
