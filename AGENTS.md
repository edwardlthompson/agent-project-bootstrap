# Agent Router

1. **First read:** `docs/START_HERE.md`
2. **Bootstrap mode:** `docs/INITIALIZATION_PROMPT.md`
3. **Reference mode:** `docs/FOR_AGENTS.md` + `TEMPLATE_INDEX.json`
4. **Task board:** `BUILD_PLAN.md` (Sequential before Parallel)
5. **Living memory:** update `AGENT_MEMORY.md` only at milestone boundaries

> Legacy `.cursorrules` is deprecated. Use `.cursor/rules/*.mdc` and this file instead.

## Architecture Constraints

- Pure FOSS under MIT license; no proprietary closed-source SDKs in production path
- Max 250 lines per view file, 150 lines per logic file
- Strict type safety and runtime validation at all data boundaries
- Core business logic decoupled from layout framework (MVVM / Clean / Hexagonal)
- Opt-in only telemetry; GDPR/CCPA compliant

## Coding Style

- Conventional Commits for all changes
- Small, modular functions; keep files within token-optimal size
- Read-before-write: inspect types/interfaces via `@filename` before editing
- Plan Mode for all non-trivial tasks; include `### Critique` in plans

## Session Protocol

- On session start: read `START_HERE.md`, then `BUILD_PLAN.md` Sequential lane
- On milestone end: update `AGENT_MEMORY.md`, append to `DECISION_LOG.md` or `docs/adr/`
- On 3-strike failure: halt and escalate to human
- On context bloat: write `.cursor-session-state`, ask human to clear chat
- Sprint 2+ features: after each AGENT step run `scripts/watch-agent-gates.sh --once --autofix` (see `docs/FEATURE_MODULES.md`)
- Destructive operations require `[HUMAN]` approval (see `.cursor/rules/destructive-ops.mdc`)
- Repo hygiene: track source only; run `scripts/check-repo-hygiene.sh` before push (see `docs/REPO_HYGIENE.md`)
- Log significant agent actions in `DECISION_LOG.md` at milestone boundaries

## Module Activation

Activate only the modules matching your stack. See `modules/*/MODULE.md`.

## Ecosystem-Specific Rules

- **Android:** FOSS only; reproducible builds with `SOURCE_DATE_EPOCH`
- **Web/PWA:** Offline-first service workers; Lighthouse budget gates
- **Python:** Strict typing (mypy), ruff lint/format, locked dependencies
- **Lightroom:** Adobe SDK Lua API only (`Lr*` namespaces)
