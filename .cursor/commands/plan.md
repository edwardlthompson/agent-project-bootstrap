# Feature or ADR plan (Plan Mode)

Read @docs/CURSOR_MODES.md and the active BUILD_PLAN row.
If the trivial rubric says Agent, skip planning and execute directly.
Otherwise propose 1–3 approaches with mandatory ### Critique before coding.

When drafting or extending **BUILD_PLAN.md** sprints, include mandatory **### Parallelization** (alongside ### Critique):

1. **Sequential lock list** — shared schema/types/API that must finish before Parallel (1–3 items max)
2. **Decomposition table** — Task | Isolated scope | Why safe in parallel
3. **`agent_count_target`** — integer; justify any target `< 2` in one sentence
4. **Dry-run** — expected output of `bash scripts/plan-parallel-dispatch.sh --draft BUILD_PLAN.md --suggest`

Apply the decomposition checklist in @BUILD_PLAN.md (multi-stack, logic/view split, tests/docs/CI). **Maximize agent_count** across non-overlapping scopes.

Before asking human approval of BUILD_PLAN changes, run:

```bash
bash scripts/check-build-plan-parallel.sh
```

Do not edit code until the user approves the plan.

Begin now.
