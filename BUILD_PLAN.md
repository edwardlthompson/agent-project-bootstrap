# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 0 · AUTO 0 · HUMAN 1 · ADB 0 · **1 open**
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

**Now:** **v1.4.0** shipped. **M61** archived · next allideas batch when ready. Open PRs + Template gaps sync below. After Cloud work, `/resume`. Child model: [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md).

> **v1.4.0** release archived in COMPLETED_TASKS.md @ `f105c3b`.
> **v1.3.0** release archived in COMPLETED_TASKS.md @ `7ca6dbf`.
> **M61** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M60** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M59** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M58** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M57** archived in COMPLETED_TASKS.md @ `e65513d`. Nav smoke ADB archived 2026-09-10.
> **Waiting HUMAN/ADB auto** archived in COMPLETED_TASKS.md @ `ca0edfb`.

### Open PRs (synced)

> Auto-managed. Do not hand-edit rows inside the markers. Run `python3 scripts/agent-run.py sync-open-prs-build-plan -- --apply` (or `/resume` / `/dependabot`).

<!-- open-prs-sync:begin -->
_No open Dependabot or Release Please PRs._
<!-- open-prs-sync:end -->

### Template gaps (synced)

> Auto-managed Monday cron + `sync-template-gaps-build-plan`. Do not hand-edit inside markers. Plan-only — run `/upgrade` then name item numbers.

<!-- template-gaps-sync:begin -->
_No template gaps; .template-version matches upstream (or template maintainer N/A)._
<!-- template-gaps-sync:end -->

### Waiting on a person

1. 🔲 [HUMAN] Lightroom Plug-in Manager load smoke (#29)

Done on this board: **v1.4.0** · **v1.3.0** · **M61** back/nav/gates · **M60** CI clarity · **M59** CI harden · **M58** ship CI + Espresso · **M57** Cursor + docs · **M56** desktop packaging · **M55** CI / security · **M54** catalog / Lightroom · **M53** Android distribution · **M52** UI / a11y / nav · **M51** CLI / API · **M50** chrome follow-through · **M49** Settings-only chrome · **M48** R8 + memory (#95 on `main`) · **M47** Cline + nav. Archive: `COMPLETED_TASKS.md`.

---

## Ongoing Maintenance

Not a checklist. GitHub Monday 07:00 UTC (`.github/workflows/weekly-health-check.yml`) already runs CI wait, security triage, upgrade-sim (template) or parent template-gap BUILD_PLAN sync (child), radar, `update-deps` dry-run, Dependabot leftover list, open-PR BUILD_PLAN sync, and latest-release SBOM. `/ship` owns pre-release and the release tag.

Open Dependabot / Release Please PRs are mirrored into **Open PRs (synced)** above; child catch-up rows land in **Template gaps (synced)** — allowed board automation, not standing chore rows. After Cloud Agents, use `/resume` on This Computer.

If Monday cron is red: Cursor Automation `weekly-maintain`, then Grok Bot 4–5. Do not put those chores back on this board. [`docs/GROK_BOTS.md`](docs/GROK_BOTS.md) · [`docs/CURSOR_AUTOMATIONS.commercial.md`](docs/CURSOR_AUTOMATIONS.commercial.md)

---

## Archive

Older sprints and releases: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
