# Cursor Automations (Commercial)

> Requires Cursor Cloud / paid tier. Template works without automations.

Automations run agents on schedules or repository events. FOSS bootstrap keeps this doc only; Commercial tier copies activation stubs via `sync-cursor-features.py`.

## When to use

- Nightly dependency triage (prefer `/maintain` + CI for FOSS)
- Post-merge review triggers (Commercial Bugbot overlap)

## Setup pointer

See [Cursor Automations docs](https://cursor.com/docs/automations) and [`CURSOR_COMMERCIAL_ACTIVATION.md`](CURSOR_COMMERCIAL_ACTIVATION.md).

Do not commit API keys or webhook secrets.
