# Feature radar score ≥9 review cadence

`scripts/cursor-feature-radar.sh` (Monday weekly health) ranks Cursor / agent-DX ideas. Scores **≥9** are draft-review candidates — **not** automatic BUILD_PLAN chore rows.

## Cadence

1. Weekly cron surfaces high scores in health notes.
2. Maintainer (or `/ideas`) picks at most a few ≥9 items into a numbered allideas → board pass.
3. Do **not** add standing “review radar” rows to Ongoing Maintenance.
4. Ship via `/build` on the active milestone (M60/M61…); archive when done.

Low scores stay in the radar dump until a human promotes them.
