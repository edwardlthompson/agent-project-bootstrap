# Build Plan

> Prioritized task board with owner labels. **Completed sprints:** `COMPLETED_TASKS.md`.

## Owner Label Legend

| Label | Owner | When to use |
|-------|-------|-------------|
| `AGENT` | Cursor Agent | Code, docs, scaffolding, tests, CI config |
| `HUMAN` | Human developer | Approvals, credentials, GitHub settings, product decisions |
| `ADB` | Human (Android) | Android SDK, emulator/device testing, F-Droid submission |
| `AUTO` | CI/scripts/bots | GitHub Actions, Dependabot, pre-commit, update checker |

## Status markers

Use **emoji markers** (not `- [ ]` GitHub checkboxes) so task state reads clearly in Markdown source and Preview. **Applies repo-wide** — `BUILD_PLAN.md`, module checklists, PR template, feature specs, and security triage.

| Marker | State | Agent action |
|--------|-------|--------------|
| 🔲 | Open | Default for new tasks; work or leave queued |
| ✅ | Done | Replace 🔲 when complete; archive sprint rows to `COMPLETED_TASKS.md` |
| ❌ | Blocked | Replace 🔲 when blocked; add brief reason after the description |

**Task format:** `🔲 [OWNER] Description` · done: `✅ [OWNER] Description` · blocked: `❌ [OWNER] Description — reason`

```bash
grep '\[AGENT\]' BUILD_PLAN.md
grep '\[HUMAN\]' BUILD_PLAN.md
grep '\[ADB\]' BUILD_PLAN.md
grep '\[AUTO\]' BUILD_PLAN.md
```

**Agent rule:** Execute all `[AGENT]` **Sequential** items first, then dispatch **Parallel** agents with isolated file scopes (`docs/PARALLEL_AGENT_SCOPES.md`). Shared schema/types are Sequential-only.

### Parallel dispatch protocol (orchestrator)

| Step | Action |
|------|--------|
| 1 | Finish all `[AGENT]` **Sequential** items for the active sprint/feature (shared schema/types locked) |
| 2 | **Discover** parallelizable work using the decomposition checklist below; add Parallel table rows with non-overlapping `` `path/**` `` scopes |
| 3 | Run `bash scripts/plan-parallel-dispatch.sh` → read **agent_count** |
| 4 | If `agent_count >= 2`, run `/scope` (auto Task dispatch); if `1`, execute inline; if `0`, run `--suggest` and expand the Parallel table (or document `parallel_exception`) |
| 5 | Sequential owner merges results, runs `watch-agent-gates.sh`, updates BUILD_PLAN (Parallel agents never edit BUILD_PLAN) |

**Decomposition checklist** (apply before finalizing Sequential items):

| Heuristic | Split into Parallel agents |
|-----------|---------------------------|
| Multi-stack repo | One agent per active module (`examples/{stack}/**`) |
| Feature container (Sprint 2+) | Agent A: pure logic + unit tests; Agent B: view/Composable + i18n |
| Tests vs production code | Separate `**/*.test.*`, `e2e/**`, `androidTest/**` when paths do not overlap implementation |
| Docs vs code | Agent A: `examples/**`; Agent B: `docs/**`, `modules/**`, `.cursor/rules/**` |
| CI/gates vs app code | Agent A: `scripts/**`, `.github/workflows/**`; Agent B: stack example tree |

**Default rule:** If a Sequential `[AGENT]` item touches two or more non-overlapping directory prefixes, **split it** — leave only schema-lock work Sequential.

**Planning (Plan Mode):** Every BUILD_PLAN proposal must include `### Parallelization` with `agent_count_target`, decomposition table, and dry-run from `plan-parallel-dispatch.sh`. Run `check-build-plan-parallel.sh` before human approval.

**Autonomous `/build`:** Runs all `[AGENT]`/`[AUTO]` and Parallel work first, then attempts the grouped **Human & device (after automation)** section via `scripts/attempt-build-plan-row.sh`. Success marks ✅; failure appends `HUMAN_BACKLOG.md` and continues — never halts on human labels. Humans review the grouped section (and backlog) after automation finishes. Status: `bash scripts/build-sprint-status.sh --json`.

> **Template maintainer:** No active AGENT sprint — **maintenance + human open items** below. **Child repos:** copy the playbook.

---

## Template Maintainer — Active Board

> **M19–M29** archived in `COMPLETED_TASKS.md`. **M18** @ `d6b92a2`.

### Open (human judgment only)

_No open maintainer blockers._ Recurring maintenance: see **Ongoing Maintenance** below.

---

## Child Repo Playbook (copy after Use this template)

> Init scripts, feature docs (`docs/features/_template.md`), and About + Settings exemplars ship with the template. Mirror the Sequential + Parallel lane structure from Sprint M9 when customizing.

### Sprint 0 — Template Customization

<!-- agent_count_target: 0 | sequential_lock_step: 5 -->
<!-- parallel_exception: bootstrap init and GitHub setup are inherently sequential -->

#### Sequential

3. 🔲 [AGENT] Run `scripts/init-project.sh` or `scripts/init-project.ps1` (`--stack <name>`; `--non-interactive` with `--project-name` + `--purpose` for scripted init)
4. 🔲 [AGENT] Run `scripts/setup-github-repo.sh` (requires `gh` auth with admin)
5. 🔲 [AUTO] Sprint 0 sign-off (all green on `main`):
   - `validate-bootstrap.sh --quick`
   - `feature-gate.sh --stack <active>`
   - `check-github-ci.sh --wait 300`
   - `check-license-compliance.sh` (after `npm ci` / `uv sync`)

#### Parallel (safe after Sequential step 5)

| Task | Owner | Isolated scope |
|------|-------|----------------|
| _None — see parallel_exception above_ | — | — |

#### Human & device (after automation)

> Address after `/build` completes AGENT/AUTO work above. `/build` attempts each row via automation; failures land in `HUMAN_BACKLOG.md`.

1. 🔲 [HUMAN] Click **Use this template** on GitHub to create your project repo
2. 🔲 [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
2a. 🔲 [HUMAN] Pick Cursor mode per [`docs/CURSOR_MODES.md`](docs/CURSOR_MODES.md) (Ask to explore, Plan for architecture)
2b. 🔲 [HUMAN] Bookmark [`docs/help/BATCH_COMMANDS.md`](docs/help/BATCH_COMMANDS.md) — type `/` in Agent chat (`/bootstrap` for Sprint 0)

### Sprint 1 — Golden Path Foundation

<!-- agent_count_target: 3 | sequential_lock_step: 1 -->

#### Sequential

1. 🔲 [AGENT] Lock shared Golden Path schema/types/API for active stack (About + navigation surface only)

#### Parallel (safe after Sequential step 1)

| Task | Owner | Isolated scope |
|------|-------|----------------|
| About screen verify | AGENT | `examples/{stack}/**/about/` |
| Stack public assets | AGENT | `examples/{stack}/public/` |
| Module + design docs | AGENT | `modules/{stack}/` |

#### Human & device (after automation)

> Address after `/build` completes AGENT/AUTO and Parallel work above.

2. 🔲 [HUMAN] Fill stack-local config: web `examples/web/public/app-update.json` + `donations.json`; Android `assets/` mirrors; or root `.app-update.json` / `donations.json` (init runs `scripts/sync-stack-config.py`)
3. 🔲 [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack

<!-- parallel_exception: none -->

### Sprint 2+ — Incremental Features

<!-- agent_count_target: 4 | sequential_lock_step: 2 -->

> One vertical slice at a time. See `docs/FEATURE_MODULES.md`. Reference exemplars: `docs/features/settings.md` (Sprint 2), About (Sprint 1).

**Agent rule:** After every `[AGENT]` step → `bash scripts/watch-agent-gates.sh --once --autofix --step <scaffold|tests|wire>`.

#### Per-feature Sequential (steps 1–2: lock API)

1. 🔲 [AGENT] Copy `docs/features/_template.md` → `docs/features/{name}.md`; refine acceptance criteria
2. 🔲 [AGENT] Scaffold feature container (public API boundary only)

#### Per-feature Parallel (safe after Sequential step 2)

| Task | Owner | Isolated scope |
|------|-------|----------------|
| Logic + unit tests | AGENT | `examples/{stack}/src/{feature}/` or stack equivalent |
| View + i18n | AGENT | `examples/{stack}/src/components/` or `ui/{feature}/`, `locales/` / `strings.xml` |
| Feature spec + acceptance | AGENT | `docs/features/{feature}.md` |
| E2e / instrumented smoke | AGENT | `examples/{stack}/e2e/` or `examples/{stack}/**/androidTest/` |

#### Per-feature Sequential (steps 3–4: after Parallel merge)

3. 🔲 [AGENT] Unit tests for feature pure logic (skip if Parallel agent completed)
4. 🔲 [AGENT] Wire view/adapter; composition root (`appBootstrap.ts` / `GoldenPathApp.kt`) ≤10 lines

#### Human & device (after automation)

> Optional product judgment after gates pass.

5. 🔲 [HUMAN] Optional product smoke after `[AUTO]` gate pass

<!-- parallel_exception: none -->

> Gates (`watch-agent-gates.sh`) run Sequential-side after each AGENT step — not in Parallel.

---

## Ongoing Maintenance (recurring)

> **Template maintainer:** `bash scripts/run-maintainer-gates.sh` weekly (omit `--quick` for full CI wait).

### Weekly

- 🔲 [AUTO] `check-security-triage.sh --wait-ci 300` (Dependabot + CI + Scorecard)
- 🔲 [AGENT] Apply Dependabot bumps; triage Scorecard SARIF findings
- 🔲 [AUTO] CI matrix + Repo Hygiene + Feature Gate green on `main`

### Monthly

- 🔲 [AUTO] `simulate-template-upgrade.sh` (also in `weekly-health-check.yml`)
- 🔲 [AUTO] `check-license-compliance.sh` + SBOM on latest release
- 🔲 [AGENT] Review Dependabot auto-merge PRs (KB-007)

### Pre-release (every version)

- 🔲 [AUTO] `pre-release-gate.sh` + `run-maintainer-gates.sh` (includes `verify-branch-protection.sh`)
- 🔲 [AUTO] Release Please PR merged; CHANGELOG + manifest bumped

### Human (after automation)

> Product approvals after automated pre-release gates pass.

- 🔲 [HUMAN] Approve release tag when product-ready

---

## Archived Sprints

| Sprint | Status | Archive |
|--------|--------|---------|
| M19–M29 — Cursor modes, batch commands, maintain, v0.11.0 release | Complete | `COMPLETED_TASKS.md` |
| v0.10.0 release (`36a02e4`) | Complete | `COMPLETED_TASKS.md` |
| M5–M18 maintainer sprints (seq + P2) | Complete | `COMPLETED_TASKS.md` @ `d6b92a2` |
| Child Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
| v0.9.0 release (`fd699bc`) | Complete | `COMPLETED_TASKS.md` |
