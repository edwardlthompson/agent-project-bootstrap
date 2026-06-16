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

> **Template maintainer:** Sprint **M18** complete (incl. P2). **Child repos:** copy the playbook.

---

## Template Maintainer — Sprint M18: Post-P2 code review remediation

> **Source:** full code review on `f59023c` (2026-06-15). Verified: GitHub Pages `VITE_BASE_PATH` breaks root-absolute fetches/SW; `appBootstrap` defers first render until donations load; Android `UpdateApplier` not wired to UI; `release.yml` SBOM steps lack stack guards; init config copies root-only.

### Critique

- **Null/empty:** `loadDonations()` failure still blocks first paint; empty `release_repo` in web public stub after init leaves update check inert.
- **Network timeouts:** Pages-deployed PWA fetches `/app-update.json` at site root, not repo subpath — silent failure on GitHub Pages demo.
- **Race conditions:** Background `checkForUpdates()` re-renders only when About is open (web); Android home shows status banner — parity gap.
- **Unhandled exceptions:** `release.yml` SBOM for missing `examples/node/` after prune can fail release upload; `android-release` strict hash compare may flake on unrelated `main` pushes.

### Sequential (must complete in order)

1. ✅ [AGENT] **P0 — Pages base path:** centralize `import.meta.env.BASE_URL` for fetch (`app-update.json`, `donations.json`), SW register, and SW precache paths
2. ✅ [AGENT] **P0 — Web first paint:** call `render()` immediately in `appBootstrap.ts`; merge donations when fetch resolves
3. ✅ [AGENT] **P0 — Android apply slice:** wire download → `UpdateApplier.launchApkInstall()` → `pendingRestart`/`Activity.recreate()` per `INITIALIZATION_PROMPT` Module A; unit/instrumented tests
4. ✅ [AGENT] **P0 — Init config propagation:** copy `release_repo` / donation URLs to `examples/web/public/` and `examples/android/app/src/main/assets/` during init; update Sprint 1 HUMAN step paths
5. ✅ [AGENT] **P1 — Release SBOM guards:** add `hashFiles` conditionals for web/python/node/android SBOM steps (parity with rust/go); skip missing files in upload
6. ✅ [AGENT] **P1 — init-stack-sync active modules:** derive `active_modules` from filesystem after prune (not all seven for `multi`/`none`)
7. ✅ [AGENT] **P1 — Release tag gate:** poll full required checks (`CI`, `Security Scan`, `CodeQL`, `Repo Hygiene`, `Feature Gate`) not jobs-only subset
8. ✅ [AGENT] **P1 — Repo hygiene:** track only `public/*.example` + `assets/*.example`; extend `check-tracked-artifacts.sh` for live JSON stubs
9. ✅ [AGENT] **P1 — Go example:** `go mod tidy` in CI; SBOM conditional on `go.sum` (zero-dep stub has no sum file)
10. ✅ [AUTO] CI + Feature Gate green on `main` after rows 1–4

### Parallel (safe after Sequential step 4)

| # | Task | Owner | Isolated scope |
|---|------|-------|----------------|
| A | Web Pages + bootstrap | AGENT | `aboutSession.ts`, `donations.ts`, `appBootstrap.ts`, `public/sw.js`, `vite.config.ts` |
| B | Android apply + tests | AGENT | `GoldenPathApp.kt`, `AboutScreen.kt`, `UpdateApplier.kt`, `androidTest/**` |
| C | Init + index + release | AGENT | `init-project.sh`, `init-project.ps1`, `init-stack-sync.py`, `release.yml`, `simulate-template-upgrade.sh` |
| D | Docs + gates | AGENT | `PARALLEL_AGENT_SCOPES.md`, `BUILD_PLAN.md` child playbook, `feature-gate.sh`, `health-check.yml` |

### P2 backlog (after M18 sequential)

- ✅ [AGENT] `panelDialog.ts` unit tests (focus trap, Escape, focus restore)
- ✅ [AGENT] Playwright e2e for PWA apply button (`[data-testid="about-apply"]`) and restart guard
- ✅ [AGENT] Web/Android update UX parity (home status banner vs About-only re-render)
- ✅ [AGENT] `feature-gate.sh`: optional `check-design-cohesion.sh` + `verify-about-feature-gate.sh` in strict multi-stack
- ✅ [AGENT] Android instrumented cadence: schedule or `health-check` emulator run when `path-changes` skips
- ✅ [AGENT] `android-release` flake policy: document tolerance vs strict in `KNOWLEDGE_BASE.md` or restore WARN path
- ✅ [AGENT] `health-check.yml`: monthly `simulate-template-upgrade.sh` step
- ✅ [AGENT] `run-maintainer-gates.sh`: dedupe `feature-gate` when `pre-release-gate` already runs it
- ✅ [AGENT] `TEMPLATE_INDEX.json`: refresh empty `roadmap` or index key exemplar paths (`panelDialog.ts`, `sw.js`)
- ✅ [AGENT] SW `CACHE_NAME` bump tied to app version or build hash
- ✅ [AGENT] `feature-gate.sh` rust/go smoke for maintainer `--stack multi --strict`
- ✅ [AGENT] `check-license-compliance.sh` rust/go slices when examples exist

### Open (template maintainer — human judgment only)

| Item | Owner | Command / gate |
|------|-------|----------------|
| F-Droid dry-run on device/emulator | ADB | `modules/android/MODULE.md` checklist |
| F-Droid listing / anti-feature sign-off | HUMAN | After `verify-fdroid-metadata.sh` |
| `gh auth refresh -s security_events` (one-time OAuth) | HUMAN | Then `run-maintainer-gates.sh` full |
| Merge Release Please PR #13 (`0.10.0`) | HUMAN | After `pre-release-gate.sh` green; verify SBOM on `release` published |

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
2. ⬜ [HUMAN] Fill stack-local config: web `examples/web/public/app-update.json` + `donations.json`; Android `assets/` mirrors; or root `.app-update.json` / `donations.json` when using init scripts (see M18 row 4)
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
| M5–M17 maintainer sprints + P2 backlog | Complete | `COMPLETED_TASKS.md` |
| M18 Post-P2 review | Complete | `COMPLETED_TASKS.md` |
| M17 Post-M16 review (`5d9be3e`) | Complete | `COMPLETED_TASKS.md` |
| v0.9.0 release (`fd699bc`) | Complete | `COMPLETED_TASKS.md` |
| M16 Post-M15 review (`1634917`) | Complete | `COMPLETED_TASKS.md` |
| M14 Post-M13 review (`fc71433`) | Complete | `COMPLETED_TASKS.md` |
| Child Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
