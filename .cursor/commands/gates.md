# Local validation gates

> Skill: `.cursor/skills/validate-bootstrap/`

Run Sprint 0 / pre-push validation (Git Bash on Windows):

```bash
python3 scripts/agent-run.py validate-bootstrap --quick
python3 scripts/agent-run.py feature-gate --stack multi
python3 scripts/agent-run.py check-repo-hygiene
```

Report pass/fail per script. Fix failures in scope before marking BUILD_PLAN items complete.

Begin now.
