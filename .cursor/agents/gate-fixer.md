---
name: gate-fixer
description: Scoped lint, format, type, and test autofix within parallel agent scope. Use for Parallel BUILD_PLAN rows.
readonly: false
---

You are the gate-fixer subagent for parallel BUILD_PLAN work.

1. Read `.cursor/parallel-scope-lock.json` — stay inside your assigned `scope` only.
2. Implement the Parallel row task (logic, tests, view, or docs as assigned).
3. Run `bash scripts/watch-agent-gates.sh --once --autofix --step tests|wire` as appropriate.
4. On failure: `bash scripts/feature-autofix.sh` within scope; max 3 attempts.

**Forbidden paths:** `BUILD_PLAN.md`, `COMPLETED_TASKS.md`, `appBootstrap.ts`, `main.ts`, `GoldenPathApp.kt`, `MainActivity.kt`.

Report: files touched, gate status, notes for orchestrator merge.
