# ADR-0008: Local vs Cloud agent venues on BUILD_PLAN

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Template maintainer

## Context

Cursor Cloud Agents and This Computer agents can both claim open `[AGENT]` rows. Parallel `/scope` locks are gitignored and invisible to Cloud. Without a git-visible venue and path scope, the two sides overwrite each other.

## Decision

1. **Who stays** `AGENT` · `HUMAN` · `ADB` · `AUTO`. Do not add Grok/Cline/Codex/Bugbot/Review Whos.
2. **Venue** on code rows only: `🔲 [AGENT][LOCAL] …` or `🔲 [AGENT][CLOUD] …` with required `— scope: <path-prefix>`.
3. **Board lanes** `### Local agent (This Computer)` and `### Cloud agent (Cursor Cloud)` hold the standing queue (`<!-- local-agent-lane -->` / `<!-- cloud-agent-lane -->`). Sprint rows remain the execution source during a sprint and must carry the same venue tags.
4. **Isolation:** LOCAL branches `feature/local-<slug>`; CLOUD uses Cursor `cursor/*`. `check-agent-venue` forbids open LOCAL vs CLOUD scope prefix overlap. `/resume` warns when Cloud PR files overlap the next LOCAL scope. Local `/build`/`/feature`/`/scope` pick LOCAL only; Cloud picks CLOUD only.
5. **Forbidden paths** (composition roots, board orchestrator files) stay Local Sequential only.

## Alternatives considered

- Replace Who with LOCAL/CLOUD — rejected: venue is where, Who is actor kind.
- Rely on `parallel-scope-lock.json` across machines — rejected: gitignored.
- Third venue EITHER — rejected: planner picks one venue when writing the row.

### Critique

| Issue | Resolution |
|-------|------------|
| Null/empty lane | Stub `_No local agent items._` / `_No cloud agent items._` |
| Cloud PR race | `/resume` overlap check before next LOCAL |
| Untagged AGENT | `check-agent-venue` rejects open `[AGENT]` without venue |
| Composition roots | Forbidden for Cloud; Sequential LOCAL only |

## Consequences

- Child `BUILD_PLAN_TEMPLATE.md` ships both lane stubs; playbook AGENT rows are `[LOCAL]`.
- `check-agent-venue` is part of `validate-bootstrap --quick`.
- Tally shows `AGENT · LOCAL · CLOUD · AUTO · HUMAN · ADB` (AGENT = LOCAL+CLOUD; total open does not double-count venue).
