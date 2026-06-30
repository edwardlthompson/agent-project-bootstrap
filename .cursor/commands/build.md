# Build feature super workflow

Read and execute sub-commands in order. After each step, summarize pass/fail.

1. Read @.cursor/commands/plan.md — execute fully (must include `### Parallelization` when drafting BUILD_PLAN rows)
2. **Stop.** Ask the user to approve the plan before continuing. If trivial rubric skipped plan, go to step 3.
3. Read @.cursor/commands/feature.md — execute **Sequential steps 1–2 only** (feature spec + scaffold / public API boundary)
4. **Auto-run** @.cursor/commands/scope.md — no user prompt. If Parallel agents complete logic/tests/view/e2e steps, **skip** `/feature` steps 3–4 when `agent-progress.json` lists them in `parallel_steps_completed`.
5. Read @.cursor/commands/feature.md — execute **remaining** steps (wire step 5 if not done; skip 3–4 when Parallel marked complete)
6. Read @.cursor/commands/gates.md — execute fully
7. Read @.cursor/commands/cleanup.md — execute fully (archive ✅ rows to @COMPLETED_TASKS.md; slim active board)

If `/scope` returns agent_count 0 with suggestions, expand BUILD_PLAN Parallel table once and re-run step 4 before escalating.

If gates fail after autofix, suggest `/fix` before retrying. Skip step 7 until gates pass and the active feature block is fully ✅.

Begin now.
