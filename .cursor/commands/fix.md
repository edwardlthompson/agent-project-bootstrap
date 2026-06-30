# Gate autofix (feature scope)

> Skill: `.cursor/skills/watch-gates-autofix/`

Autonomous feature step with auto-fix:

```bash
bash scripts/watch-agent-gates.sh --once --autofix --step scaffold
```

If exit 1: read `.cursor/agent-progress.json` and gate JSON; fix lint/tests in active feature scope; re-run.
On exit 2 (3-strike), halt and switch to Debug Mode or escalate to human.
Push to remote still requires `/push`, `/ship`, or explicit user approval.

Begin now.
