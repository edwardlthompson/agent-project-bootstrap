# Spec: Cursor.Directory rule curation

## Goal
Curate useful cursor.directory/generate rules into stack guidelines without a second project law.

## Trigger / users
Sprint 0 / stack activation on a child or template maintainer pass.

## Requirements
- docs/DIRECTORY_RULES.md playbook: pick rules for active Golden Path; human confirm before write.
- Optional scoped .cursor/rules/{stack}-practices.mdc with globs for examples/{stack}/**; cap <=3.
- Init/bootstrap checklist mentions Directory rules review.
- Never overwrite AGENTS.md or AGENT.md; no alwaysApply unless reviewed.

## Out of scope
Always-on dump of entire Directory catalog.

## Acceptance checks
- Playbook + checklist exist; test asserts globs required language in playbook.

## Assumptions (flagged)
- ADR-0005 still applies.

## Open questions
None.

## Files likely touched
docs/DIRECTORY_RULES.md, .cursor/commands/init.md, .cursor/commands/bootstrap.md, tests/
