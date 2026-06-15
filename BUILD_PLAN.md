# Build Plan

> Prioritized task board with owner labels. **Completed sprints:** `COMPLETED_TASKS.md`.

## Owner Label Legend

| Label | Owner | When to use |
|-------|-------|-------------|
| `AGENT` | Cursor Agent | Code, docs, scaffolding, tests, CI config |
| `HUMAN` | Human developer | Approvals, credentials, GitHub settings, product decisions |
| `ADB` | Human (Android) | Android SDK, emulator/device testing, F-Droid submission |
| `AUTO` | CI/scripts/bots | GitHub Actions, Dependabot, pre-commit, update checker |

**Task format:** `⬜ [OWNER] Description` · done: `✅`

```bash
grep '\[AGENT\]' BUILD_PLAN.md
grep '\[HUMAN\]' BUILD_PLAN.md
grep '\[ADB\]' BUILD_PLAN.md
grep '\[AUTO\]' BUILD_PLAN.md
```

**Agent rule:** Execute all `[AGENT]` **Sequential** items first, then dispatch **Parallel** agents with isolated file scopes (`docs/PARALLEL_AGENT_SCOPES.md`). Shared schema/types are Sequential-only.

> **Template maintainer:** work **Sprint M14** below. **Child repos:** copy the playbook after **Use this template**.

---

## Child Repo Playbook (copy after Use this template)

> Init scripts, feature docs (`docs/features/_template.md`), and About + Settings exemplars ship with the template. Mirror the Sequential + Parallel lane structure from Sprint M9 when customizing.

### Sprint 0 — Template Customization

#### Sequential

1. ⬜ [HUMAN] Click **Use this template** on GitHub to create your project repo
2. ⬜ [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
3. ⬜ [AGENT] Run `scripts/init-project.sh` or `scripts/init-project.ps1` (`--stack <name>`; `--non-interactive` with `--project-name` + `--purpose` for scripted init)
4. ⬜ [AGENT] Run `scripts/setup-github-repo.sh` (requires `gh` auth with admin)
5. ⬜ [AUTO] Sprint 0 sign-off (all green on `main`):
   - `validate-bootstrap.sh --quick`
   - `feature-gate.sh --stack <active>`
   - `check-github-ci.sh --wait 300`
   - `check-license-compliance.sh` (after `npm ci` / `uv sync`)

### Sprint 1 — Golden Path Foundation

#### Sequential

1. ⬜ [AGENT] Verify About screen scaffold for your active stack (`examples/{stack}/`)
2. ⬜ [HUMAN] Fill `.app-update.json` `release_repo` and `donations.json` links
3. ⬜ [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack

### Sprint 2+ — Incremental Features

> One vertical slice at a time. See `docs/FEATURE_MODULES.md`. Reference exemplars: `docs/features/settings.md` (Sprint 2), About (Sprint 1).

**Agent rule:** After every `[AGENT]` step → `bash scripts/watch-agent-gates.sh --once --autofix --step <scaffold|tests|wire>`.

#### Per-feature Sequential (duplicate each feature)

1. ⬜ [AGENT] Copy `docs/features/_template.md` → `docs/features/{name}.md`; refine acceptance criteria
2. ⬜ [AGENT] Scaffold feature container (public API boundary only)
3. ⬜ [AGENT] Unit tests for feature pure logic
4. ⬜ [AGENT] Wire view/adapter; composition root (`appBootstrap.ts` / `GoldenPathApp.kt`) ≤10 lines
5. ⬜ [HUMAN] Optional product smoke after `[AUTO]` gate pass

#### Per-feature Parallel (safe after Sequential step 2)

| Task | Owner | Isolated scope |
|------|-------|----------------|
| Logic + tests | AGENT | `examples/{stack}/src/{feature}/` or stack equivalent |
| View + i18n | AGENT | `examples/{stack}/src/components/` or `ui/{feature}/`, `locales/` / `strings.xml` |

> Gates (`watch-agent-gates.sh`) run Sequential-side after each AGENT step — not in Parallel.

---

## Ongoing Maintenance (recurring)

> **Template maintainer:** `bash scripts/run-maintainer-gates.sh` weekly (omit `--quick` for full CI wait).

### Weekly

- ⬜ [AUTO] `check-security-triage.sh --wait-ci 300` (Dependabot + CI + Scorecard)
- ⬜ [AGENT] Apply Dependabot bumps; triage Scorecard SARIF findings
- ⬜ [AUTO] CI matrix + Repo Hygiene + Feature Gate green on `main`

### Monthly

- ⬜ [AUTO] `simulate-template-upgrade.sh`
- ⬜ [AUTO] `check-license-compliance.sh` + SBOM on latest release
- ⬜ [AGENT] Review Dependabot auto-merge PRs (KB-007)

### Pre-release (every version)

- ⬜ [AUTO] `pre-release-gate.sh` + `run-maintainer-gates.sh` (includes `verify-branch-protection.sh`)
- ⬜ [AUTO] Release Please PR merged; CHANGELOG + manifest bumped
- ⬜ [HUMAN] Approve release tag when product-ready

---

## Template Maintainer — Sprint M14: Post-M13 review remediation

> **Source:** full code review on `4fddec8` (2026-06-15). Verified: `.template-version` **0.7.1** vs Release Please **0.8.0**; `init-project.ps1` L147 broken stderr redirect; `verify-reproducible-apk.sh` not wired in maintainer gates.

### Critique

- **Null/empty:** `pre-release-gate.sh` checks `.template-version` exists but not manifest/CHANGELOG alignment.
- **Network timeouts:** N/A for this sprint (local script/CI config focus).
- **Race conditions:** N/A.
- **Unhandled exceptions:** `init-project.ps1` token sync line throws on Windows; child init aborts before stack sync completes.

> **Template maintainer:** M14 complete on `fc71433`. Next: P2 backlog below or Release Please for next version.

### Sequential (must complete in order)

1. ✅ [AGENT] **P0 — Version coherence:** sync `.template-version`, `TEMPLATE_INDEX.json` `template_version`, `AGENT_MEMORY.md` to **0.8.0**; add `pre-release-gate.sh` assert `.template-version` == `.release-please-manifest.json`
2. ✅ [AGENT] **P0 — Fix `init-project.ps1` L147:** replace `2> | Out-Null` with `2>$null`; smoke-test `init-project.ps1 -Stack web -Prune`
3. ✅ [AGENT] **P0 — Non-interactive init:** add `--non-interactive` (skip prompts when `--stack` + `--project-name` + `--purpose` set); replace `sed` placeholder edits with Python in both init scripts (escape `/` in names)
4. ✅ [AGENT] **P1 — Gate wiring:** wire `verify-reproducible-apk.sh` into `run-maintainer-gates.sh` full mode (`--skip-apk` opt-out); fail on unknown CLI flags; align `--quick` with `--wait-ci` or update weekly BUILD_PLAN row
5. ✅ [AGENT] **P1 — Branch protection hardening:** extend `verify-branch-protection.sh` to assert `strict: true` + `allow_force_pushes: false`; document rulesets API fallback in `SECURITY_TRIAGE.md`
6. ✅ [AGENT] **P1 — Docs/index:** index `docs/features/settings.md` in `TEMPLATE_INDEX.json`; reconcile duplicate `CHANGELOG.md` `[Unreleased]` blocks; document full init CLI in `INITIALIZATION_PROMPT.md` Section 8
7. ✅ [AGENT] **P1 — Web security:** replace `AboutPanel.ts` donation `innerHTML` with DOM APIs + `textContent`; inject `APP_VERSION` from `package.json` via Vite `define`
8. ✅ [AGENT] **P1 — Android exemplar:** extend `check-file-limits.sh` to `ui/GoldenPathApp.kt` / `GoldenPathScreen.kt`; wire `pendingRestart` visible state in About/home UI
9. ✅ [AGENT] **P1 — CI/release:** add Android SBOM slice to `release.yml`; document tag-push lightweight gate vs `workflow_dispatch` full gate in `SECURITY_TRIAGE.md`
10. ✅ [AUTO] CI + Feature Gate green on `main` after rows 1–3 (`fc71433`)

### Parallel (safe after Sequential step 3)

| # | Task | Owner | Isolated scope |
|---|------|-------|----------------|
| A | Init + version gates | AGENT | `scripts/init-project.*`, `pre-release-gate.sh`, `.template-version`, `TEMPLATE_INDEX.json` |
| B | Maintainer gates | AGENT | `run-maintainer-gates.sh`, `verify-branch-protection.sh`, `verify-reproducible-apk.sh` |
| C | Web exemplar | AGENT | `AboutPanel.ts`, `aboutSession.ts`, `vitest.config.ts`, `e2e/app.spec.ts` |
| D | Android + CI | AGENT | `GoldenPathApp.kt`, `check-file-limits.sh`, `release.yml`, `modules/android/MODULE.md` |
| E | Docs hygiene | AGENT | `CHANGELOG.md`, `INITIALIZATION_PROMPT.md`, `docs/PRIVACY.md`, `COMPLETED_TASKS.md` |

### P2 backlog (after M14 sequential)

- ⬜ [AGENT] Extend init `--prune` to optional stacks (rust/go/lightroom) or `--keep-optional` flag
- ⬜ [AGENT] Add CodeQL matrix for `examples/rust` / `examples/go` or document exclusion
- ⬜ [AGENT] Playwright e2e: enable update check → open About → assert status text
- ⬜ [AGENT] `simulate-template-upgrade.sh` smoke with `init-project.sh --non-interactive`
- ⬜ [AGENT] Modernize `MainActivitySmokeTest` (`ActivityScenario`); optional `connectedDebugAndroidTest` CI job
- ✅ [AGENT] Fix init next-steps numbering (step 4 missing in `.sh` / `.ps1`) — fixed in M14 rows 2–3
- ✅ [HUMAN] Close stale M5 visual-review row in `COMPLETED_TASKS.md`

### Open after M14 (human judgment only)

| Item | Owner | Command / gate |
|------|-------|----------------|
| Approve release tag (next version) | HUMAN | After `pre-release-gate.sh` |
| F-Droid dry-run on device/emulator | ADB | `modules/android/MODULE.md` checklist |
| F-Droid listing / anti-feature sign-off | HUMAN | After `verify-fdroid-metadata.sh` |
| `gh auth refresh -s security_events` (one-time OAuth) | HUMAN | Then `run-maintainer-gates.sh` full |

---

## Archived Sprints

| Sprint | Status | Archive |
|--------|--------|---------|
| M5–M14 maintainer sprints | Complete | `COMPLETED_TASKS.md` |
| v0.8.0 release (`10b46d6`) | Complete | `COMPLETED_TASKS.md` |
| M14 Post-M13 review (`fc71433`) | Complete | `COMPLETED_TASKS.md` |
| Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
| Maintainer gate cycles | Complete | `COMPLETED_TASKS.md` |
