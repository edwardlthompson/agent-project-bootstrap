# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 0 · AUTO 0 · HUMAN 0 · ADB 2 · **2 open**
<!-- /remaining-tally -->

Live board for **this template repo**. Finished work: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md). Child products use [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md) (copied onto their `BUILD_PLAN.md` at init).

**Who:** `AGENT` code · `HUMAN` person · `ADB` device · `AUTO` CI/scripts
**State:** 🔲 open · ✅ done · ❌ blocked — reason

Format: `🔲 [AGENT] Short task`. Sequential `[AGENT]` first. Parallel scopes: [`docs/PARALLEL_AGENT_SCOPES.md`](docs/PARALLEL_AGENT_SCOPES.md). `/build` tries HUMAN/ADB after automation; failures go to `HUMAN_BACKLOG.md`.

## Smoke gate (hard stop)

After every `[AGENT]` row: `python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto`

After the **last** `[AGENT]`/`[AUTO]` row in a sprint is ✅, do **not** start the next sprint until this exits 0:

```bash
python3 scripts/agent-run.py smoke-sprint --require

```

That command re-smokes **every** ✅ row: no errors or crashes, plus startup time and load order. Details: [`docs/SPRINT_SMOKE.md`](docs/SPRINT_SMOKE.md). Fail → leave the last row open or ❌; fix; re-run. `/gates` wrap-up includes the same check.

---

## Template Maintainer

**Now:** v1.1.0 shipped. #95 R8 + Android 17 memory is on `main`. Recurring work is Monday cron, not this board. Child model: [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md).

> **M57** archived in COMPLETED_TASKS.md @ `e65513d`.

### Waiting on a person

1. 🔲 [ADB] Optional: Android SDK licenses + first AVD (`/emulator`)
2. 🔲 [ADB] Golden Path nav smoke on device (Settings Back → home; second Back stays)

Done on this board: **M57** Cursor + docs · **M56** desktop packaging · **M55** CI / security · **M54** catalog / Lightroom · **M53** Android distribution · **M52** UI / a11y / nav · **M51** CLI / API · **M50** chrome follow-through · **M49** Settings-only chrome · **M48** R8 + memory (#95 on `main`) · **M47** Cline + nav. Archive: `COMPLETED_TASKS.md`.

---

## Ongoing Maintenance

Not a checklist. GitHub Monday 07:00 UTC (`.github/workflows/weekly-health-check.yml`) already runs CI wait, security triage, upgrade-sim, radar, `update-deps` dry-run, Dependabot leftover list, and latest-release SBOM. `/ship` owns pre-release and the release tag.

If Monday cron is red: Cursor Automation `weekly-maintain`, then Grok Bot 4–5. Do not put those chores back on this board. [`docs/GROK_BOTS.md`](docs/GROK_BOTS.md) · [`docs/CURSOR_AUTOMATIONS.commercial.md`](docs/CURSOR_AUTOMATIONS.commercial.md)

---

## Archive

Older sprints and releases: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
