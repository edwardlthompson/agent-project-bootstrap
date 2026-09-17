# ADR-0009: Agent cost diet and ADHD brevity

- **Status:** Accepted
- **Date:** 2026-09-16
- **Deciders:** Template maintainer

## Context

Fourteen `alwaysApply` Cursor rules plus a “read START_HERE + AGENTS + CURSOR_MODES every session” protocol burned ~5–14k tokens per turn. Dirty `scripts/` / `tests/` paths forced full 8-stack `feature-gate` via `WIDE_PREFIX`. Pre-commit ran ~70 `validate-bootstrap --quick` checks on every commit. Human-facing docs and agent replies were walls of text.

## Decision

1. **Demote alwaysApply** (keep content): `batch-commands`, `ux-ui` (globs), `windows-encoding`, `local-compute`, `local-deps`, `foss-compliance` (FOSS one-liner stays in `core-directives`; tier sync no longer forces foss always-on).
2. **Keep thin always-on:** `main`, `core-directives`, `brief-replies`, `destructive-ops`, `feature-modules`, `product-brief`, `repo-hygiene`, `cursor-modes`, `read-before-write`. Commercial tier still flips `commercial-compliance` always-on. **`brief-replies`:** 1–3 sentences / ≤5 bullets; gates = `OK` / `FAIL X — fix Y`.
3. **Session protocol:** hook + next BUILD_PLAN row + mode name; Unreleased = first ~20 CHANGELOG lines; no mandatory full START_HERE/AGENTS reload every turn.
4. **`gate_scope` LIGHT_PREFIX:** `scripts/`, `tests/`, `schemas/`, `.cursor/rules/` → docs mode. Wide remains `modules/`, `.github/`, hooks/agents/plugin, adapter roots.
5. **`validate-bootstrap --agent`:** ~12 core checks for pre-commit. `--quick` / full stay for CI and `/gates --full`.
6. **Commands:** `/gates` defaults to agent-fast + dirty stacks; `--full` restores multi. `/build` wrap-up uses scoped gate + hygiene, not full multi unless `--full`.

## Alternatives considered

- Tokens-only or gates-only diet — rejected: both drive Cursor $ and idle time.
- Removing gitleaks / venue / smoke — rejected: release safety stays.

### Critique

| Issue | Resolution |
|-------|------------|
| Demoting foss-compliance weakens FOSS | Gitleaks + destructive-ops always-on; CI license/CodeQL remain |
| scripts-only misses Android break | Wide still for modules/workflows; CI/`/gates --full` |
| Short replies hide failures | Failures name command + one fix line |
| Pre-commit `--agent` misses catalog drift | CI + `/gates --full` keep full parallel set |

## Consequences

- Cursor turns pay fewer always-on tokens; mid-slice gates stay light on tooling edits.
- Maintainer `/gates --full` and CI remain release-grade.
