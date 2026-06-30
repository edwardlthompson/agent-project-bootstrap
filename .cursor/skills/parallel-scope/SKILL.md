---
name: parallel-scope
description: Build parallel agent manifest and dispatch scopes. Use when /scope or after Sequential lock in BUILD_PLAN.
disable-model-invocation: false
---

# Parallel scope dispatch

See also: `.cursor/commands/scope.md`

```bash
bash scripts/plan-parallel-dispatch.sh --require-sequential-clear --json
bash scripts/check-parallel-scope.sh
```

Write manifest to `.cursor/parallel-scope-lock.json`. When `agent_count >= 2`, launch named subagents (`gate-fixer`) per scope.md — one message, concurrent tasks.

Forbidden paths: `BUILD_PLAN.md`, composition roots — see `docs/PARALLEL_AGENT_SCOPES.md`.
