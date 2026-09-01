# 10-minute tour

A first-time walk for **any** coding agent or IDE. In Cursor you can type `/tour` instead.

Do not dump whole files. After each stop, pause for a question.

## 1. Start here (2 min)

Read [`docs/START_HERE.md`](../START_HERE.md).

- Pick [**Bootstrap**](GLOSSARY.md) (new project from this template) or [**Reference**](GLOSSARY.md) (rules only).
- This repo works in Cursor, Windsurf, Antigravity, Claude Code, Copilot, Gemini CLI, Aider, and Cline. The shared contract is [`AGENTS.md`](../../AGENTS.md). See [`docs/AGENT_PORTABILITY.md`](../AGENT_PORTABILITY.md).
- Word list: [`GLOSSARY.md`](GLOSSARY.md) ([**Sacred**](GLOSSARY.md), [**Canon**](GLOSSARY.md), [**AGENT**](GLOSSARY.md) / [**HUMAN**](GLOSSARY.md) / [**ADB**](GLOSSARY.md) / [**AUTO**](GLOSSARY.md), 🔲 status).

**First-time path: Cline (free).** Open this project in Cursor. Install recommended extensions if prompted, or search Extensions for Cline (`saoudrizwan.claude-dev`). Click the Cline icon, Sign In with GitHub (Google/email ok). Do not paste API keys, install Codex, or set `OPENAI_API_KEY`. Set API Provider = Cline and pick a FREE model. Paste: `Read docs/help/TOUR.md and walk me through it. Follow AGENTS.md.` Review every diff; run `python3 scripts/agent-run.py verify` before trusting changes. Full steps: [`CLINE.md`](CLINE.md).

**Paste prompt:** `Read docs/START_HERE.md and tell me which repo mode I am in.`

## 2. Why the files exist (3 min)

Read [`docs/BEST_PRACTICES.md`](../BEST_PRACTICES.md) — only these three:

- **LICENSE** — others cannot safely use an unlicensed repo
- **SECURITY.md** — vulnerabilities go to a private advisory, not a public issue
- **BUILD_PLAN labels** — `AGENT` / `HUMAN` / `ADB` / `AUTO` so agents do not block on credentials or devices

**Paste prompt:** `Explain LICENSE, SECURITY.md, and BUILD_PLAN labels from docs/BEST_PRACTICES.md.`

## 3. Golden Path (3 min)

Open the README for your stack under `examples/{stack}/`. If you have not chosen a stack yet, start with [`examples/web/README.md`](../../examples/web/README.md).

That folder is the runnable slice you copy for the next feature.

**Paste prompt:** `Read the active examples/{stack}/README.md (or examples/web) and summarize how I run tests.`

## 4. Week 1 (2 min)

Read [`docs/FIRST_30_DAYS.md`](../FIRST_30_DAYS.md) **Week 1 only**. Check off what you have already done.

Later sessions: in Cursor type `/coach`. In any other tool, ask it to follow [`COACH.md`](COACH.md).

## 5. First verify (2 min)

Run the local harness (`verify.sh --quick`) and interpret only the first failure:

```bash
python3 scripts/agent-run.py tour-verify
```

- Pass: Week 1 gates are green. Next: [`COACH.md`](COACH.md).
- Fail: quote the `Tour verify: first failure` block. Next: `/fix`, or `/debug` if strikes ≥ 3.

**Paste prompt:** `Run python3 scripts/agent-run.py tour-verify and explain the first failure only.`
