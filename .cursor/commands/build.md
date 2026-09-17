# Autonomous sprint build

Execute BUILD_PLAN without asking. Venue: This Computer = `[AGENT][LOCAL]` only. Stop only on 3-strike, exit 2, or board complete.

## Loop

```bash
python3 scripts/agent-run.py build-sprint-status --json --lane auto

```

| `next_row.action` | Do |
|-------------------|-----|
| `automate_human` / `automate_adb` | `attempt-build-plan-row` → ✅ or backlog |
| `execute` | Implement → gate → ✅ |
| `parallel_dispatch` | `@scope.md` then `set-parallel-sprint-done` |
| AUTO | Run scripts → ✅ |
Every AGENT step:

```bash
python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto

```

**Gate lock:** never skip watch-agent-gates; do not start the next row until gates exit 0. Never skip 1c to chain a second feature.

Do not re-run full validate mid-slice if watch passed.

## Wrap-up (sprint complete)

1. `smoke-sprint --require --sprint "<title>"`
2. Scoped gate + hygiene (not full multi unless user said `--full`):

```bash
python3 scripts/agent-run.py watch-agent-gates --once --scope auto
python3 scripts/agent-run.py check-repo-hygiene

```

3. `@cleanup.md`
4. Chain next sprint if `next_row` exists.

Open PRs: `sync-open-prs-build-plan -- --check` once; `--apply` only if stale.

Begin now.
