# ADR-0010: Repo-wide Agent Mode (speed / balanced / lean)

- **Status:** Accepted
- **Date:** 2026-11-03
- **Deciders:** Template maintainer

## Context

Cloud Agents, Grok Bots, and wide parallel Cloud lanes burn Cursor tokens even when This Computer can finish the same work. Venue tags ([ADR-0008](0008-agent-venue.md)) and the cost diet ([ADR-0009](0009-cost-diet-brevity.md)) help, but there was no single durable switch that every window, side agent, and subagent must obey. Maintainers needed a repo-wide mode with a clear Lean extreme for token spend.

## Decision

1. **Modes:** `speed` · `balanced` · `lean`. One setting for the whole repo.
2. **Source of truth:** `.cursor/agent-mode.json` (`mode`, ISO-8601 `updated`, short `updated_by`). Missing file ⇒ treat as `balanced`.
3. **Default:** new child repos get `"mode": "balanced"` at init.
4. **Lean (extreme):** hard-block Cloud Agents and Grok Bots. On entry, rewrite every open `🔲 [AGENT][CLOUD] …` row in `BUILD_PLAN.md` (and lane stubs) to `🔲 [AGENT][LOCAL] …`, preserving the rest of the row text and scope. Refuse any remaining Cloud/Grok execution while mode = lean.
5. **Commands:** `/lean`, `/balanced`, `/speed`, `/mode`, `/status` (thin wrappers around `set-agent-mode` / `repo-status`).
6. **Injection:** one short always-on line naming the mode and its policy — no heavy always-on stack.

## Alternatives considered

- Binary on/off Cloud switch — rejected: three tiers match day-to-day (speed), default, and extreme save.
- Per-session or per-chat mode only — rejected: side agents would ignore it; spend leaks.
- Soft Lean (prefer local, allow Cloud) — rejected: primary goal is token spend; Lean must hard-block.

### Critique

| Issue | Resolution |
|-------|------------|
| Lean leaves stale Cloud lane rows | Conversion rewrites open CLOUD→LOCAL; empty cloud lane stub remains valid |
| Missing JSON mid-session | Treat as balanced; `/status` prints the effective mode |
| Always-on injection bloat | One-line `agent-mode.mdc`; ADR-0009 diet unchanged |
| Commercial Grok docs confuse FOSS | Lean note in `docs/GROK_BOTS.md`; FOSS path still has no bots |

## Consequences

- Token spend drops when maintainers run `/lean` before Cloud-heavy sprints.
- Venue isolation (ADR-0008) and brevity (ADR-0009) stay; mode sits above them as a repo policy.
- Init stamps balanced; `/status` makes mode and open LOCAL/CLOUD counts scannable.
