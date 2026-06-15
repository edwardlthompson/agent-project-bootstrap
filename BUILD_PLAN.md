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

> **Template maintainer:** Sprint **M17** active (post-M16 code review on `7e4a50e`). **Child repos:** copy the playbook.

---

## Template Maintainer — Sprint M17: Post-M16 code review remediation

> **Source:** full code review on `7e4a50e` (2026-06-15). Verified: Android manifest lacks `INTERNET`; web `lastChecked` written before fetch; prune leaves stale `TEMPLATE_INDEX.json`; `sbom-assets` has no CI gate on `release` published; `check-github-ci.ps1` false-fails in-progress jobs.

### Critique

- **Null/empty:** Pruned child repos still reference deleted paths in `TEMPLATE_INDEX.json`; `init-stack-sync.py` no-op on `AGENT_MEMORY.md` emoji format.
- **Network timeouts:** `sbom-assets` can upload on `release` published while post-merge CI is still running; tag-gate polls only Repo Hygiene + Feature Gate.
- **Race conditions:** Release Please merge + release publish can race fresh CI on `main`; `check-github-ci.sh` may score cancelled runs as FAIL during concurrency retries.
- **Unhandled exceptions:** `init-project.ps1` donation write lacks `Test-Path` guard; web update check persists `lastChecked` before GitHub fetch succeeds.

### Sequential (must complete in order)

1. ✅ [AGENT] **P0 — Android INTERNET:** add `android.permission.INTERNET` to manifest; add unit test or instrumented assertion that `ReleaseTagFetcher` is reachable when network enabled
2. ✅ [AGENT] **P0 — Web update timing:** move `LAST_CHECKED_KEY` write in `aboutSession.ts` to after successful GitHub fetch (or clear on failure); add unit test for failed-fetch retry
3. ✅ [AGENT] **P0 — Prune + template index:** after prune, update `TEMPLATE_INDEX.json` (or prune-aware `validate-template-index.sh` using `.cursor/stack-selection.json`); extend `simulate-template-upgrade.sh` with post-prune `validate-bootstrap.sh --quick` + primary-stack removal asserts
4. ✅ [AGENT] **P0 — Release SBOM gate:** add pre-SBOM poll on `release` published (`check-github-ci.sh --wait` full rollup or `needs:` workflow_run) so assets attach only after post-merge CI green
5. ✅ [AGENT] **P1 — check-github-ci.ps1:** treat empty/in-progress job `conclusion` as WAIT (parity with `.sh`); add `--wait` to `health-check.yml` or schedule offset
6. ✅ [AGENT] **P1 — init-stack-sync:** sync `AGENT_MEMORY.md` ✅/❌ emoji lines (not `[ ]` checkboxes); add rust/go to `MODULE_LINES`; fix `multi`+`--prune` `pruned: true` when nothing deleted
7. ✅ [AGENT] **P1 — Docs P0 drift:** fix `INITIALIZATION_PROMPT.md` Sprint 0 “step 6” → step 5; reconcile Node as init stack vs optional across `OPTIONAL_STACKS.md`, `README.md`, `TEMPLATE_INDEX.json`
8. ✅ [AGENT] **P1 — FOSS grep scope:** extend Android proprietary-SDK scan to Kotlin/manifest/XML in `ci.yml` (not only `*.gradle*`)
9. ✅ [AGENT] **P1 — Pre-release completeness:** add `check-license-compliance.sh` to `pre-release-gate.sh`; fail on missing `.release-please-manifest.json` (not WARN-only)
10. ✅ [AGENT] **P1 — path-changes:** include `modules/android/**`, `.github/workflows/ci.yml`, and shared scripts in android-instrumented trigger paths
11. ⬜ [AUTO] CI + Feature Gate green on `main` after rows 1–4

### Parallel (safe after Sequential step 4)

| # | Task | Owner | Isolated scope |
|---|------|-------|----------------|
| A | Release + CI gates | AGENT | `release.yml`, `check-github-ci.sh`, `check-github-ci.ps1`, `health-check.yml`, `ci.yml` |
| B | Init + index + smoke | AGENT | `init-project.sh`, `init-project.ps1`, `init-stack-sync.py`, `validate-template-index.sh`, `simulate-template-upgrade.sh` |
| C | Web + Android exemplars | AGENT | `aboutSession.ts`, `AndroidManifest.xml`, `AboutPanel.ts`, `SettingsPanel.ts`, e2e/unit tests |
| D | Docs hygiene | AGENT | `INITIALIZATION_PROMPT.md`, `OPTIONAL_STACKS.md`, `MAINTAINING_THE_TEMPLATE.md`, `README.md`, `TEMPLATE_INDEX.json` |

### P2 backlog (after M17 sequential)

- ⬜ [AGENT] Web modal a11y: `role="dialog"`, `aria-modal`, focus trap, Escape on About/Settings panels
- ⬜ [AGENT] Wire `applyPwaUpdate()` / Android `UpdateApplier` or remove dead apply paths; SW cache strategy → network-first when online
- ⬜ [AGENT] Config hygiene: `.example` pattern for `app-update.json` / `donations.json` in web public + Android assets; stub `release_repo` in template
- ⬜ [AGENT] `init-project.ps1` smoke in CI (`simulate-template-upgrade` or dedicated job); donation `Test-Path` guard
- ⬜ [AGENT] Renumber duplicate module letters (Node/Rust both E; Go/Lightroom both F); add `node` to `PARALLEL_AGENT_SCOPES.md` child table
- ⬜ [AGENT] Index `MAINTAINING_THE_TEMPLATE.md` in `TEMPLATE_INDEX.json`; fix badge step reference (step 3 vs 6)
- ⬜ [AGENT] Android instrumented: settings/about/theme/update UI assertions beyond launch smoke
- ⬜ [AGENT] `checkForUpdates()` unit tests (fetch mock); axe e2e on settings/about open states
- ⬜ [AGENT] `android-release` CI: align reproducibility WARN vs `verify-reproducible-apk.sh --strict`
- ⬜ [AGENT] Optional rust/go SBOM slices in `release.yml` when examples exist

### Open (template maintainer — human judgment only)

| Item | Owner | Command / gate |
|------|-------|----------------|
| F-Droid dry-run on device/emulator | ADB | `modules/android/MODULE.md` checklist |
| F-Droid listing / anti-feature sign-off | HUMAN | After `verify-fdroid-metadata.sh` |
| `gh auth refresh -s security_events` (one-time OAuth) | HUMAN | Then `run-maintainer-gates.sh` full |

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

## Archived Sprints

| Sprint | Status | Archive |
|--------|--------|---------|
| M5–M16 maintainer sprints | Complete | `COMPLETED_TASKS.md` |
| M17 Post-M16 review | Active | `BUILD_PLAN.md` |
| v0.9.0 release (`fd699bc`) | Complete | `COMPLETED_TASKS.md` |
| M16 Post-M15 review (`1634917`) | Complete | `COMPLETED_TASKS.md` |
| M14 Post-M13 review (`fc71433`) | Complete | `COMPLETED_TASKS.md` |
| Child Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
