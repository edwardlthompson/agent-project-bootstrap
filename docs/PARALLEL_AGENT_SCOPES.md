# Parallel Agent Scopes

> Isolated file scopes for BUILD_PLAN Parallel lane. No two agents may touch the same path prefix.

## Rules

1. One branch per agent: `feature/agent-<task-slug>`
2. Run `scripts/check-parallel-scope.sh` before dispatch
3. Shared types/schemas: **Sequential agent only**
4. Never edit `BUILD_PLAN.md` from parallel agents (sequential owner)

## Sprint 1 (child repo) defaults

| Stack | Isolated scope |
|-------|----------------|
| web | `examples/web/**` |
| python | `examples/python/**` |
| android | `examples/android/**` |
| multi | One scope per stack row; no overlap |
| none | Match `AGENT_MEMORY.md` checked modules |

## Sprint M1 (template maintainer) completed scopes

| Task | Scope |
|------|-------|
| Web bundle + snapshots | `examples/web/**`, `scripts/check-bundle-size.sh` |
| Python pyright | `examples/python/**` |
| Android metadata | `examples/android/fastlane/**`, `examples/android/README.md` |
| Cursor rules | `.cursor/rules/testing.mdc`, `.cursor/rules/ci-gates.mdc` |
| Scorecard | `.github/workflows/scorecard.yml` |
| Parallel checker | `scripts/check-parallel-scope.sh`, `docs/PARALLEL_AGENT_SCOPES.md` |

## Collision Response

If `check-parallel-scope.sh` fails, split the task or move one item back to Sequential lane.
