# Spec: Child deep upgrade

## Goal
After parent sync, analyze and reformat the child to new Canon — beyond gap file copy.

## Trigger / users
Child runs /upgrade --deep (or UPGRADE deep section).

## Requirements
- Upgrade command documents --deep: inventory, analyze, plan buckets (Canon sync, Reformat, Adopt, Sacred).
- Apply only named numbers; no silent do all; never overwrite Sacred or replace app with examples/.
- Help twin docs/help/UPGRADE.md updated.
- Tests assert deep language and Sacred protections.

## Out of scope
Blind AGENTS.md overwrite; auto do-all.

## Acceptance checks
- Command + help mention --deep and reformat bucket; tests pass.

## Assumptions (flagged)
- Plan + Critique before apply.

## Open questions
None.

## Files likely touched
.cursor/commands/upgrade.md, docs/help/UPGRADE.md, tests/
