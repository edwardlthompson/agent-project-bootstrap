# Spec: Frequent commit/push cadence

## Goal
Pressure small commits and human-approved /push so dirty trees stay small.

## Trigger / users
After each AGENT row or large dirty tree; /coach /build /feature.

## Requirements
- coach/build/feature nudge: commit now, then ask human for /push.
- Mention /split-to-prs when diffs are huge.
- Never silent git push; destructive-ops unchanged.
- PREFERENCES.md documents the preference.
- Tests assert nudge text and forbid silent push instruction.

## Out of scope
Auto-push without approval.

## Acceptance checks
- Command twins contain commit+/push nudge; tests pass.

## Assumptions (flagged)
- Agents may commit when user asks.

## Open questions
None.

## Files likely touched
.cursor/commands/coach.md, build.md, feature.md, docs/help/COACH.md, docs/PREFERENCES.md, tests/
