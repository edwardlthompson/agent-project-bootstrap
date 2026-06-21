# Full repo review and BUILD_PLAN execution

Framework: use AGENT/HUMAN/ADB/AUTO labels; Sequential before Parallel; gates after AGENT steps; update memory files at milestones.

## Step 1 — Review

Explore via targeted reads (active stack only — @docs/FOR_AGENTS.md token economy). Run when available:

```bash
bash scripts/validate-bootstrap.sh --quick
bash scripts/feature-gate.sh --stack multi
bash scripts/check-repo-hygiene.sh
bash scripts/check-readme-health.sh
```

Check Dependabot/CodeQL via `gh` if authenticated. Write @CODE_REVIEW.md from @CODE_REVIEW.md.example (severity: Critical / High / Medium / Low / Deferred).

## Step 2 — BUILD_PLAN

Add a review sprint at the top of @BUILD_PLAN.md active board. Link findings to CODE_REVIEW sections. Use 🔲 [AGENT] / 🔲 [HUMAN] format (✅ done · ❌ blocked per BUILD_PLAN legend).

## Step 3 — Execute

Work Sequential [AGENT] items top-to-bottom. After each step:

```bash
bash scripts/watch-agent-gates.sh --once --autofix --step none
```

## Step 4 — Cleanup

Archive completed sprint to @COMPLETED_TASKS.md; slim active board; update Archived Sprints row.

Begin now.
