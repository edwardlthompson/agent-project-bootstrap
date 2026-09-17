# Coach (why)

Output: **one next action** + optional one Why link. No health novels. Twin: `docs/help/COACH.md`.

```bash
python3 scripts/agent-run.py project-health
python3 scripts/agent-run.py feedback-inbox

```

Rules:

- Fixes in inbox → `/audit`
- Open AGENT/AUTO → `/build` (name `next_row`)
- No AGENT + dirty Unreleased → `/ship` or `/prerelease`
- Both empty → `/allideas` (or `/ideas` for a short backlog, or `/maintain`)
- Child with newer template → offer `/upgrade` (gap plan only)

Begin now.
