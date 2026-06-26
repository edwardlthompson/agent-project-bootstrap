# Build feature super workflow

Read and execute sub-commands in order. After each step, summarize pass/fail.

1. Read @.cursor/commands/plan.md — execute fully
2. **Stop.** Ask the user to approve the plan before continuing. If trivial rubric skipped plan, go to step 3.
3. Read @.cursor/commands/feature.md — execute fully
4. Read @.cursor/commands/gates.md — execute fully
5. Read @.cursor/commands/cleanup.md — execute fully (archive ✅ rows to @COMPLETED_TASKS.md; slim active board)

If gates fail after autofix, suggest `/fix` before retrying. Skip step 5 until gates pass and the active feature block is fully ✅.

Begin now.
