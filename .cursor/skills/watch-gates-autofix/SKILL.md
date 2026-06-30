---
name: watch-gates-autofix
description: Run watch-agent-gates with autofix in feature scope. Use when /fix or after AGENT BUILD_PLAN steps.
disable-model-invocation: false
---

# Watch gates autofix (3-strike)

See also: `.cursor/commands/fix.md`

```bash
bash scripts/watch-agent-gates.sh --once --autofix
```

Exit 1: read `.cursor/agent-progress.json` and gate JSON; fix lint/tests in active feature scope; re-run (max 3 strikes).

Exit 2: halt and escalate per `docs/FOR_AGENTS.md`.

Optional: `bash scripts/feature-autofix.sh` for mechanical fixers within feature container.
