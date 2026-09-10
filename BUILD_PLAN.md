# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 17 · AUTO 7 · HUMAN 4 · ADB 2 · **30 open**
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

**Now:** M56. Last ship **v1.1.0**. Child model: [`BUILD_PLAN_TEMPLATE.md`](BUILD_PLAN_TEMPLATE.md).

> **M55** archived in COMPLETED_TASKS.md @ `c9ab417`.

### M56 — Desktop packaging

<!-- parallel_exception: Winget docs then binary loop -->

1. ✅ [AGENT] Winget manifest example
2. 🔲 [AGENT] Winget multi-arch docs
3. 🔲 [AGENT] Desktop binary + Winget publish loop

### M57 — Cursor + docs

<!-- parallel_exception: registry/docs are one overlapping slice -->

1. 🔲 [AGENT] Land `docs/GROK_BOTS.md` on main
2. 🔲 [AGENT] Plugin marketplace runbook
3. 🔲 [AGENT] Skills for `/emulator` and `/adr`
4. 🔲 [AGENT] Refresh `CURSOR_FEATURE_REGISTRY.json`
5. 🔲 [AGENT] Commercial Automations YAML
6. 🔲 [AGENT] Commercial Cloud hook merge test
7. 🔲 [AGENT] Canvas / design-mode walkthrough
8. 🔲 [AGENT] Cursor CLI local-loop recipe
9. 🔲 [AGENT] `/tour` + COACH: Settings-only chrome
10. 🔲 [AGENT] `batch-commands-print.html` audit
11. 🔲 [AGENT] `check-template-gaps` optional-stack rows
12. 🔲 [AGENT] ADR-0001 architecture-pick gate
13. 🔲 [AGENT] Living `ci-gap` registry

### Waiting on a person

1. 🔲 [HUMAN] CII Best Practices checklist (login + public badge)
2. 🔲 [HUMAN] Optional: Ollama at `http://127.0.0.1:11434/v1` (`docs/LOCAL_MODELS.md`)
3. 🔲 [ADB] Optional: Android SDK licenses + first AVD (`/emulator`)
4. 🔲 [ADB] Golden Path nav smoke on device (Settings Back → home; second Back stays)

Done on this board: **M55** CI / security · **M54** catalog / Lightroom · **M53** Android distribution · **M52** UI / a11y / nav · **M51** CLI / API · **M50** chrome follow-through · **M49** Settings-only chrome · **M47** Cline + nav. Archive: `COMPLETED_TASKS.md`.

---

## Ongoing Maintenance (recurring)

Template weekly: `bash scripts/run-maintainer-gates.sh` (omit `--quick` to wait on CI).

### Weekly

- 🔲 [AUTO] `cursor-feature-radar.sh` (non-blocking)
- 🔲 [AUTO] `check-security-triage.sh --wait-ci 300`
- 🔲 [AGENT] `/update-deps`; leftover Dependabot + Scorecard
- 🔲 [AUTO] CI + Repo Hygiene + Feature Gate green on `main`

### Monthly

- 🔲 [AUTO] `simulate-template-upgrade.sh`
- 🔲 [AUTO] `check-license-compliance.sh` + SBOM on latest release
- 🔲 [AGENT] Review Dependabot auto-merge PRs (KB-007)

### Pre-release (every version)

- 🔲 [AUTO] `pre-release-gate.sh --local` before push; full gate + `run-maintainer-gates.sh` after
- 🔲 [AUTO] Release Please merged; CHANGELOG + manifest bumped

### Human (after automation)

- 🔲 [HUMAN] Approve release tag when product-ready
- 🔲 [HUMAN] Quarterly Cursor feature radar (next 2026-11-15; last 2026-08-15)

---

## Archive

Older sprints and releases: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
