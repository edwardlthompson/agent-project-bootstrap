# Spec: Brief re-anchor during Golden Path

## Goal
Stop child-project agents from treating Golden Path About/Settings/copy as the product; keep scaffolding aimed at `AGENT.md`.

## Trigger / users
Child repo with a live `AGENT.md`. Agent runs Sprint 0 / Golden Path About, Settings, purpose, or donate work.

## Requirements
- Extend `check-agent-brief` (or sibling gate): when `AGENT.md` exists, Golden Path About/purpose user-facing strings in the active stack must include the brief’s keywords (case-insensitive).
- Template repo without live `AGENT.md` still passes (example-only path unchanged).
- `/tour`, `/feature`, and `product-brief.mdc` remind: re-read `AGENT.md` before adapting Golden Path UI copy — not only before About.
- Never overwrite, delete, or “refresh” `AGENT.md` from Golden Path or `AGENTS.md`.
- Document the rule next to existing anti-amnesia (`docs/features/product-brief-anti-amnesia.md` or a short help note).

## Out of scope
Auto-rewriting Golden Path demos on init; a second brief file; replacing `AGENT.md` with a guidelines hub; `/shape quick`; rewriting `/plan`.

## Acceptance checks
- Fixture: brief keywords `neon, camera, messages` → About/purpose missing them fails the gate; including them passes.
- Template without `AGENT.md`: `check-agent-brief` still green.
- Tour or feature command text mentions re-reading the brief before Golden Path copy work.

## Assumptions (flagged)
- Failure mode is demo About/copy replacing the product (defaults 1a).
- Hard gate preferred over docs-only (defaults 2a).
- UI construction stays in `docs/ux-ui-guidelines.md`; this spec is product-identity only.
- Keyword match is enough for v1 (not full one-liner paraphrase).

## Open questions
None for slice 1 (`defaults`).

## Files likely touched
`scripts/lib/check_agent_brief.py`, `scripts/lib/agent_brief.py`, `tests/test_agent_brief.py`, `.cursor/rules/product-brief.mdc`, `.cursor/commands/tour.md`, `.cursor/commands/feature.md`, `docs/help/TOUR.md`, `docs/features/product-brief-anti-amnesia.md` (optional: active-stack About i18n paths under `examples/`).
