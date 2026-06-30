# Local validation gates

> Skill: `.cursor/skills/validate-bootstrap/`

Run Sprint 0 / pre-push validation (Git Bash on Windows):

```bash
bash scripts/validate-bootstrap.sh --quick
bash scripts/feature-gate.sh --stack multi
bash scripts/check-repo-hygiene.sh
```

Report pass/fail per script. Fix failures in scope before marking BUILD_PLAN items complete.

Begin now.
