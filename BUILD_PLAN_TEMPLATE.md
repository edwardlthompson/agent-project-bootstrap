# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 11 · AUTO 4 · HUMAN 9 · ADB 1 · **25 open**
<!-- /remaining-tally -->

Live board for a product repo. Finished work: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).

**Who:** `AGENT` code · `HUMAN` person · `ADB` device · `AUTO` CI/scripts  
**State:** 🔲 open · ✅ done · ❌ blocked — reason

Format: `🔲 [AGENT] Short task`. Sequential `[AGENT]` first. Parallel scopes: [`docs/PARALLEL_AGENT_SCOPES.md`](docs/PARALLEL_AGENT_SCOPES.md). `/build` tries HUMAN/ADB after automation; failures go to `HUMAN_BACKLOG.md`.

This file is the **child model**. After `init-project`, it becomes your `BUILD_PLAN.md`. On the bootstrap template, the live maintainer board is [`BUILD_PLAN.md`](BUILD_PLAN.md).

## Smoke gate (hard stop)

After every `[AGENT]` row: `python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto`

After the **last** `[AGENT]`/`[AUTO]` row in a sprint is ✅, do **not** start the next sprint until this exits 0:

```bash
python3 scripts/agent-run.py smoke-sprint --require
```

That command re-smokes **every** ✅ row: no errors or crashes, plus startup time and load order. Details: [`docs/SPRINT_SMOKE.md`](docs/SPRINT_SMOKE.md). Fail → leave the last row open or ❌; fix; re-run. `/gates` wrap-up includes the same check.

---

## Product

Copy this shape when you add sprints: `### Sprint N — title`, then numbered rows. Keep it this short.

### Sprint 0 — Customize

<!-- parallel_exception: stack not selected until init -->

1. 🔲 [AGENT] Run `scripts/init-project.sh` or `.ps1` (`--stack`; scripted: `--non-interactive --project-name --purpose`)
2. 🔲 [AGENT] Fill `branding/product.json` (`mode: product`); sync tokens + README
3. 🔲 [AGENT] Run `scripts/setup-github-repo.sh` (`gh` admin)
4. 🔲 [AUTO] Sprint 0 sign-off on `main`: `validate-bootstrap --quick` · `feature-gate --stack <active>` · `check-github-ci --wait 300` (CI, Security Scan, CodeQL) · `check-license-compliance`
5. 🔲 [HUMAN] Use this template on GitHub
6. 🔲 [HUMAN] Pick FOSS vs Commercial (`init-project.sh --distribution-tier`)
7. 🔲 [HUMAN] Fill `docs/INITIALIZATION_PROMPT.md`
8. 🔲 [HUMAN] Pick Cursor mode (`docs/CURSOR_MODES.md`)
9. 🔲 [HUMAN] Bookmark `docs/help/BATCH_COMMANDS.md` (`/bootstrap`)

### Sprint 1 — Golden Path

<!-- parallel_exception: Settings-only chrome + About + nav are one lock -->

1. 🔲 [AGENT] Lock types/API: Settings-only chrome, About, navigation (no header Theme/About/donate)
2. 🔲 [AGENT] Verify About, public assets, and module docs for the active stack
3. 🔲 [HUMAN] Fill `app-update.json` + `donations.json` (init runs `scripts/sync-stack-config.py`)
4. 🔲 [HUMAN] Approve ADR-0001 and Sprint 1

### Sprint 2+ — Next feature

<!-- parallel_exception: one vertical slice; add a Parallel table after the public API is locked -->

1. 🔲 [AGENT] Copy `docs/features/_template.md` → `docs/features/{name}.md`
2. 🔲 [AGENT] Scaffold feature container (public API only)
3. 🔲 [AGENT] Logic + unit tests
4. 🔲 [AGENT] View + i18n
5. 🔲 [AGENT] Wire view; composition root ≤10 lines
6. 🔲 [HUMAN] Optional product smoke after `smoke-sprint --require`

### Waiting on a person

1. 🔲 [ADB] Optional: Android SDK licenses + first AVD (`/emulator`)

---

## Ongoing Maintenance (recurring)

### Weekly

- 🔲 [AUTO] CI + Repo Hygiene + Feature Gate green on `main`
- 🔲 [AGENT] `/update-deps`; leftover Dependabot

### Monthly

- 🔲 [AUTO] `check-license-compliance.sh` + SBOM on latest release

### Pre-release (every version)

- 🔲 [AUTO] `pre-release-gate.sh --local` before push
- 🔲 [HUMAN] Approve release tag when product-ready

---

## Archive

Older sprints: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
