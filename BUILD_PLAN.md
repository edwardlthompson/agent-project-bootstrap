# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 0 · LOCAL 0 · CLOUD 0 · AUTO 0 · HUMAN 0 · ADB 0 · **0 open**
<!-- /remaining-tally -->

### Product (do not drift)

> Auto-managed from `AGENT.md` after init. Do not hand-edit inside markers. Read `AGENT.md` before any sprint row.

<!-- product-brief-sync:begin -->
_Template maintainer: no product AGENT.md. Children write AGENT.md before init._
<!-- product-brief-sync:end -->

Live board for **this template repo**. Finished work: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md). Child products use [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md) (copied onto their `BUILD_PLAN.md` at init).

**Who:** `AGENT` code · `HUMAN` person · `ADB` device · `AUTO` CI/scripts
**Venue (AGENT only):** `[LOCAL]` This Computer · `[CLOUD]` Cursor Cloud — see [`docs/adr/0008-agent-venue.md`](docs/adr/0008-agent-venue.md)
**State:** 🔲 open · ✅ done · ❌ blocked — reason

Format: `🔲 [AGENT][LOCAL] Short task — scope: path/prefix` (or `[CLOUD]`). Sequential `[AGENT]` first. Parallel scopes: [`docs/PARALLEL_AGENT_SCOPES.md`](docs/PARALLEL_AGENT_SCOPES.md). `/build` on This Computer picks LOCAL only; Cloud picks CLOUD only. HUMAN/ADB after automation → `HUMAN_BACKLOG.md`.

## Smoke gate (hard stop)

After every `[AGENT]` row: `python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto`

After the **last** `[AGENT]`/`[AUTO]` row in a sprint is ✅, do **not** start the next sprint until this exits 0:

```bash
python3 scripts/agent-run.py smoke-sprint --require

```

That command re-smokes **every** ✅ row: no errors or crashes, plus startup time and load order. Details: [`docs/SPRINT_SMOKE.md`](docs/SPRINT_SMOKE.md). Fail → leave the last row open or ❌; fix; re-run. `/gates` wrap-up includes the same check.

---

## Template Maintainer

**Now:** AGENT board empty. After Cloud work, `/resume`. Child model: [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md).

> **M64** archived in COMPLETED_TASKS.md @ `86bc12c`.
> **M63** archived in COMPLETED_TASKS.md @ `9b7870b`.
> **v1.6.0** release archived in COMPLETED_TASKS.md @ `d4cb35b`.
> **M62** archived in COMPLETED_TASKS.md @ `81d165b`.
> **v1.5.0** release archived in COMPLETED_TASKS.md @ `9808229`.
> **v1.4.0** release archived in COMPLETED_TASKS.md @ `f105c3b`.
> **v1.3.0** release archived in COMPLETED_TASKS.md @ `7ca6dbf`.
> **M61** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M60** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M59** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M58** archived in COMPLETED_TASKS.md @ `ca0edfb`.
> **M57** archived in COMPLETED_TASKS.md @ `e65513d`. Nav smoke ADB archived 2026-09-10.
> **Waiting HUMAN/ADB auto** archived in COMPLETED_TASKS.md @ `ca0edfb`.

### UX & UI inventory

Complete list from construction gaps and `/ux-review`. Status is only planned / in_progress / done. `/build` does not execute these until `/ux-apply UX-NNN` (or a Sequential row).

<!-- ux-inventory:begin -->
_No UX inventory items._
<!-- ux-inventory:end -->

### Local agent (This Computer)

Standing queue for This Computer. Rows: `🔲 [AGENT][LOCAL] … — scope: path`. `/build` and `/feature` claim these only. Isolation: [`docs/adr/0008-agent-venue.md`](docs/adr/0008-agent-venue.md).

<!-- local-agent-lane:begin -->
_No local agent items._
<!-- local-agent-lane:end -->

### Cloud agent (Cursor Cloud)

Standing queue for Cursor Cloud Agents. Rows: `🔲 [AGENT][CLOUD] … — scope: path`. Cloud claims these only (`cursor/*` branches). Never edit Local lane or `[LOCAL]` rows.

<!-- cloud-agent-lane:begin -->
_No cloud agent items._
<!-- cloud-agent-lane:end -->

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

_None._ Lightroom stub smoke is `feature-gate --stack lightroom` (Lua/SDK), not Plug-in Manager. Raster icons are `blender-icons` QA, not a HUMAN export.

Done on this board: **M63** Local/Cloud venues · **v1.6.0** · **M62** UX/UI construction law · **v1.5.0** · **v1.4.0** · **v1.3.0** · **M61** back/nav/gates · **M60** CI clarity · **M59** CI harden · **M58** ship CI + Espresso · **M57** Cursor + docs · **M56** desktop packaging · **M55** CI / security · **M54** catalog / Lightroom · **M53** Android distribution · **M52** UI / a11y / nav · **M51** CLI / API · **M50** chrome follow-through · **M49** Settings-only chrome · **M48** R8 + memory (#95 on `main`) · **M47** Cline + nav. Archive: `COMPLETED_TASKS.md`.

---

## Ongoing Maintenance

Not a checklist. GitHub Monday 07:00 UTC (`.github/workflows/weekly-health-check.yml`) already runs CI wait, security triage, upgrade-sim (template) or parent template-gap BUILD_PLAN sync (child), radar, `update-deps` dry-run, Dependabot leftover list, open-PR BUILD_PLAN sync, and latest-release SBOM. `/ship` owns pre-release and the release tag.

Open Dependabot / Release Please PRs are mirrored into **Open PRs (synced)** above; child catch-up rows land in **Template gaps (synced)** — allowed board automation, not standing chore rows. After Cloud Agents, use `/resume` on This Computer.

If Monday cron is red: Cursor Automation `weekly-maintain`, then Grok Bot 4–5. Do not put those chores back on this board. [`docs/GROK_BOTS.md`](docs/GROK_BOTS.md) · [`docs/CURSOR_AUTOMATIONS.commercial.md`](docs/CURSOR_AUTOMATIONS.commercial.md)

---

## Archive

Older sprints and releases: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
