# Feature vertical slice step

Execute the active BUILD_PLAN feature row only (one feature per task). See @docs/FEATURE_MODULES.md.

After each AGENT step:

```bash
bash scripts/watch-agent-gates.sh --once --autofix --step scaffold
```

Use `--step tests` or `--step wire` when appropriate. On exit 2, use `/debug` or escalate.

When the active feature block is fully ✅ and gates pass, read @.cursor/commands/cleanup.md — execute fully.

Begin now.
