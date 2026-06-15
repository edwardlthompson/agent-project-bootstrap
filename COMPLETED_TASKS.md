# Completed Tasks

> Archive of finished BUILD_PLAN items.

## Sprint M5 — README Visual Refresh (2026-06-12)

- ✅ [AGENT] Harden `scripts/normalize-markdown-whitespace.py` — table-aware blank-line collapse
- ✅ [AGENT] Add `scripts/check-markdown-tables.sh`; hook into `validate-bootstrap.sh`
- ✅ [AGENT] Redesign README sections — shields.io badges + HTML `<dl>`/tables for What's Included, BUILD_PLAN Labels, Template Update Checker, Supported Stacks
- ✅ [AGENT] Add README badge conventions to `docs/MAINTAINING_THE_TEMPLATE.md`
- ✅ [AGENT] Run verification — encoding, design cohesion, markdown table lint, TEMPLATE_INDEX validation
- ✅ [HUMAN] Visual review on GitHub after push — badges load, links resolve *(closed M14: superseded by maintainer README cycles)*

## Template Maintainer — v0.2.1 Full Bootstrap Hardening (2026-06-13)

- ✅ [AGENT] Normalize `.gitignore` UTF-16 to UTF-8; extend encoding scan and pre-commit hook
- ✅ [AGENT] Sync `PROMPT_LIBRARY.md` entries 4, 6, 8, 9; populate `KNOWLEDGE_BASE.md` (6 entries)
- ✅ [AGENT] Document Lighthouse 3-run median in `modules/web/MODULE.md`
- ✅ [AGENT] SHA-pin `release.yml` actions; add pin policy to `docs/SECURITY_TRIAGE.md`
- ✅ [AGENT] Add `check-workflow-action-ref-format.sh` pre-commit hook
- ✅ [AGENT] Init scripts: `validate-workflow-actions` + `check-github-ci` reminder
- ✅ [AGENT] Devcontainer: encoding check, gh CLI feature, CI gate tip
- ✅ [AGENT] Add `health-check.yml` weekly workflow
- ✅ [AGENT] Bootstrap Gradle wrapper; CI `android-build` assembleDebug job
- ✅ [AGENT] Bump to v0.2.1; sync `TEMPLATE_INDEX.json`, `CHANGELOG.md`, `README.md`
- ✅ [HUMAN] Set GitHub About from `docs/GITHUB_ABOUT.md` (via `gh repo edit`)
- ✅ [HUMAN] Create GitHub Release tag `v0.2.1` (https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.1)
- ✅ [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection (CI + Security Scan + CodeQL)
- ✅ [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson` (template maintainer)

## Template Maintainer — v0.2.0 Backlog Fix (2026-06-12)

- ✅ [AGENT] Normalize UTF-16 files to UTF-8; add `scripts/check-file-encoding.sh` + CI + pre-commit
- ✅ [AGENT] Add `package-lock.json`, `uv.lock`, `.env.example`; expand `validate-bootstrap.sh`
- ✅ [AGENT] Sync `TEMPLATE_INDEX.json` with LICENSE, scripts, workflows, rules
- ✅ [AGENT] Sync README, SECURITY_TRIAGE, RUNBOOK, UPGRADING_FROM_TEMPLATE, PROMPT_LIBRARY, CHANGELOG
- ✅ [AGENT] Harden license-compliance CI; web coverage budget; android ops checklist
- ✅ [AGENT] Harden INITIALIZATION_PROMPT Sections 2/7/8 with Build Verification Gate
- ✅ [AGENT] Update BUILD_PLAN Sprint 0 + Milestone Gates
- ✅ [AGENT] Bump `.template-version` to 0.2.0; finalize CHANGELOG
- ✅ [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection, About
- ✅ [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson`

## Template Maintainer — v0.6.0+ Web Layout & CI Fixes (2026-06-13)

- ✅ [AGENT] Add `docs/WEB_PROJECT_LAYOUT.md` and agent routing for docs/ vs examples/web/
- ✅ [AGENT] Localization scaffold docs (web `locales/` + Android `strings.xml`) separated from styles
- ✅ [AGENT] Android `NetworkStatusMonitor` for online/offline status parity with web
- ✅ [AGENT] Harden `check-design-cohesion` (CSS content guard, main.ts i18n, PS1 parity)
- ✅ [AUTO] CI, Security Scan, CodeQL, and GitHub Pages green on `main` (commit `38ce003`)
- ✅ [HUMAN] Enable GitHub Pages (Actions source) and workflow PR permissions via repo settings

## Sprint M0 — Template Hardening v0.2.2

- ✅ [AGENT] Add `scripts/setup-github-repo.sh` and `scripts/setup-github-repo.ps1` — idempotent Dependabot alerts, private vulnerability reporting, branch protection/rulesets (CI + Security Scan + CodeQL); print UI fallback checklist on API 422
- ✅ [AGENT] Add gitleaks CI job to `.github/workflows/security.yml` (or `ci.yml`) on PR + `main` push
- ✅ [AGENT] Add `check-file-limits` and `validate-bootstrap --quick` to `.pre-commit-config.yaml`
- ✅ [AGENT] Add `scripts/pre-release-gate.sh` and `scripts/pre-release-gate.ps1` — CI poll, Dependabot Critical/High count, template version/tag match, release dry-run reminder
- ✅ [AGENT] Add KNOWLEDGE_BASE KB-007 (npm/pip overrides policy for transitive CVEs); document `@lhci/cli` override in DECISION_LOG
- ✅ [AGENT] Add `npm audit` step to `examples/web` and `uv pip audit` (or equivalent) to weekly `.github/workflows/health-check.yml`
- ✅ [AGENT] Sync `AGENT_MEMORY.md` seed template version with `.template-version`; fix stale `0.1.0` reference
- ✅ [AGENT] Bump `.template-version` to `0.2.2`; update CHANGELOG, TEMPLATE_INDEX, README

## Sprint M1 — Template Hardening v0.3.0

- ✅ [AGENT] Extend `init-project.sh` / `.ps1` with interactive stack picker (web / python / android / multi / none) — prune unused `examples/` and `modules/`, never delete LICENSE/CI/scripts
- ✅ [AGENT] On init: sync `AGENT_MEMORY.md` active modules; emit minimal BUILD_PLAN Parallel section for chosen stack
- ✅ [AGENT] Add `.cursor-session-state.example.json` schema; document restore flow in `docs/FOR_AGENTS.md`
- ✅ [AGENT] Expand `docs/FOR_AGENTS.md` failure playbook (CI poll, GH_TOKEN, Dependabot conflicts, 3-strike escalation, parallel scope collision grep)
- ✅ [AGENT] Add `android-release` CI job — `SOURCE_DATE_EPOCH=1700000000 ./gradlew assembleRelease`, FOSS grep, optional two-run APK hash compare with flake tolerance
- ✅ [AGENT] Enforce `pytest --cov-fail-under=90` in CI for `examples/python`
- ✅ [AGENT] Add Conventional Commits PR title check (`amannn/action-semantic-pull-request`) to `.github/workflows/ci.yml`
- ✅ [AGENT] Draft `docs/adr/0001-core-architecture.md` pattern for child repos (MVVM / Clean / Hexagonal choice template)
- ✅ [AGENT] Bump `.template-version` to `0.3.0`; update CHANGELOG, TEMPLATE_INDEX, README

## Sprint M2 — Template Features v0.4.0

- ✅ [AGENT] Add `modules/node/MODULE.md` and `examples/node/` Golden Path stub (Fastify or Hono, MIT, typed, vitest)
- ✅ [AGENT] Add Node CI job to `.github/workflows/ci.yml` (lint, test, locked install)
- ✅ [AGENT] Add GitHub Pages deploy workflow for `examples/web` demo (FOSS, no tracking)
- ✅ [AGENT] Add Dependabot auto-merge workflow — patch/minor only, requires CI + dependency-review pass, excludes major without `[HUMAN]` label
- ✅ [AGENT] Add changelog automation (`release-please` or `git-cliff`) wired to Conventional Commits
- ✅ [AGENT] Add `scripts/simulate-template-upgrade.sh` — clone, init, cherry-pick per `docs/UPGRADING_FROM_TEMPLATE.md`, assert validate-bootstrap passes
- ✅ [AGENT] Add composite GitHub Action `action.yml` exporting `validate-bootstrap` for downstream repos
- ✅ [AGENT] Bump `.template-version` to `0.4.0`; update CHANGELOG, TEMPLATE_INDEX, README
- ✅ [AUTO] Upgrade simulation test passes in CI (optional scheduled job)
- ✅ [AGENT] GitHub Actions stale bot (`actions/stale`); exempt `template-improvement` (`.github/workflows/stale.yml`)
- ✅ [AGENT] PR coverage comment job (vitest + pytest artifacts; Codecov optional) (`.github/workflows/ci.yml`)
- ✅ [AGENT] `scripts/generate-winget-manifest.sh` stub generator (`packaging/winget/**`, `scripts/`)
- ✅ [AGENT] F-Droid `metadata/` template in `examples/android/` (`examples/android/metadata/**`)
- ✅ [AGENT] Per-stack SBOM slices on GitHub Release (`examples/web`, `examples/python`) (`.github/workflows/release.yml`)
- ✅ [AGENT] PROMPT_LIBRARY Entry 15 — Post-release regression (`PROMPT_LIBRARY.md`)
- ✅ [AGENT] PROMPT_LIBRARY Entry 16 — Template upgrade simulation (`PROMPT_LIBRARY.md`)
- ✅ [AGENT] Issue template: auto-suggest `.template-version` in placeholder text (`.github/ISSUE_TEMPLATE/*.yml`)

## Sprint M3 — Ecosystem Expansion v0.5.0+

- ✅ [AGENT] Add `examples/lightroom/` minimal stub (`Info.lua`, SDK version doc) per `modules/lightroom/MODULE.md`
- ✅ [AGENT] Update `TEMPLATE_INDEX.json` — set `examples/lightroom` module `example` path
- ✅ [AGENT] (Optional) Add `modules/rust/MODULE.md` + `examples/rust/` stub behind stack picker
- ✅ [AGENT] (Optional) Add `modules/go/MODULE.md` + `examples/go/` stub behind stack picker
- ✅ [AGENT] Gate new module CI behind workflow matrix `inputs.stack` or path filters to control CI minutes

## Sprint M4 — Design System v0.6.0

- ✅ [AGENT] Add `design-tokens/` + schema + `scripts/sync-design-tokens.py`
- ✅ [AGENT] Migrate Android example to Compose M3 + theme toggle (DataStore) + `strings.xml` i18n
- ✅ [AGENT] Refactor web example: CSS variables + theme toggle + `locales/` i18n scaffold
- ✅ [AGENT] Add `docs/DESIGN_GUIDE.md` + `.cursor/rules/design-system.mdc`
- ✅ [AGENT] Add `scripts/check-design-cohesion.sh` + validate-bootstrap wiring
- ✅ [AUTO] `android-build` + web tests green (theme toggle smoke tests)
- ✅ [AGENT] Web theme + i18n unit tests (`examples/web/src/theme.test.ts`, `examples/web/src/i18n/**`)
- ✅ [AGENT] Android Compose theme components (`examples/android/.../ui/**`)

## Milestone Gates

- ✅ [AUTO] Workflow action refs validated (`scripts/validate-workflow-actions.sh`)
- ✅ [AUTO] Pre-commit bare-semver guard (`scripts/check-workflow-action-ref-format.sh`)
- ✅ [AUTO] Android assembleDebug CI smoke on `examples/android/`
- ✅ [AUTO] Weekly health-check workflow polls CI + Security Scan + CodeQL
- ✅ [AUTO] UTF-8 encoding check clean (`scripts/check-file-encoding.sh`)
- ✅ [AUTO] Lockfiles present and CI uses locked installs (`npm ci`, `uv sync --locked`)
- ✅ [AUTO] `TEMPLATE_INDEX.json` complete (`scripts/validate-template-index.sh`)
- ✅ [AUTO] Gitleaks CI job passes on `main` (M0)
- ✅ [AUTO] Pre-commit includes file-limits and quick bootstrap validation (M0)
- ✅ [AUTO] Android `assembleRelease` with `SOURCE_DATE_EPOCH` passes (M1)
- ✅ [AUTO] Python coverage ≥ 90% in CI (M1)
- ✅ [AUTO] Web bundle size budget within threshold (M1)
- ✅ [AUTO] OpenSSF Scorecard run completed within last 30 days (M1)
- ✅ [AUTO] Upgrade simulation test passes (M2)
- ✅ [AUTO] GitHub Pages demo deploys successfully (M2)
- ✅ [AUTO] Node example CI green when `examples/node/` present (M2)
## BUILD_PLAN Automation Pass (2026-06-13)

### Sprint 0 — Template (maintainer repo complete)

- ✅ [AGENT] Create `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md`
- ✅ [AGENT] Add `.github/CODEOWNERS` and `THIRD_PARTY_LICENSES.md`
- ✅ [AGENT] Initialize workspace memory files from template seeds (`AGENT_MEMORY.md`, etc.)
- ✅ [AGENT] Wire update checker config into devcontainer and README
- ✅ [HUMAN] Set GitHub repo About description from `docs/GITHUB_ABOUT.md` (via `gh repo edit`)
- ✅ [AGENT] Commit lockfiles (`package-lock.json`, `uv.lock`) and `.env.example`
- ✅ [AGENT] Ensure `TEMPLATE_INDEX.json` includes all scripts, workflows, and playbooks
- ✅ [AUTO] `scripts/check-file-encoding.sh` passes
- ✅ [AUTO] Full Build Verification Gate (INITIALIZATION_PROMPT Section 7) green
- ✅ [AUTO] `scripts/validate-bootstrap.sh` (expanded) passes in CI
- ✅ [HUMAN] Enable Dependabot alerts + security updates
- ✅ [HUMAN] Enable private vulnerability reporting + branch protection on `main` (via `setup-github-repo.sh`)
- ✅ [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson`

### Sprint 0 Parallel (maintainer)

- ✅ [AGENT] Confirm GitHub Pages uses Actions (not `/docs` folder)
- ✅ [AUTO] Verify pre-commit hooks install

### Sprint 1 — Golden Path (maintainer)

- ✅ [AGENT] Propose directory structure for target stack
- ✅ [AGENT] Draft ADR-0001 core architecture (`docs/adr/0001-core-architecture.md`)
- ✅ [AGENT] Implement Golden Path reference feature (design tokens, i18n, theme toggle)
- ✅ [AUTO] `scripts/check-design-cohesion.sh` passes
- ✅ [AUTO] CI matrix green on main
- ✅ [AGENT] Web PWA offline cache + bundle budget + visual snapshots
- ✅ [AGENT] Python CLI + 90% coverage gate + pyright
- ✅ [AGENT] Android FOSS skeleton + Fastlane metadata stub
- ✅ [AGENT] Node API stub
- ✅ [AGENT] CodeQL + Trivy workflow wiring
- ✅ [AGENT] Devcontainer + pre-commit hooks

### Sprint M0 Parallel

- ✅ [AGENT] Cross-platform `scripts/check-file-encoding.py` (UTF-8/UTF-16 BOM)
- ✅ [AGENT] Add `.cursor/rules/windows-encoding.mdc`
- ✅ [AGENT] Add PROMPT_LIBRARY Entry 10 — Pre-release gate
- ✅ [AGENT] Add PROMPT_LIBRARY Entry 11 — GitHub repo setup
- ✅ [AGENT] Document setup script in `docs/SECURITY_TRIAGE.md` § Setup
- ✅ [AGENT] Wire `setup-github-repo` reminder into `init-project.sh` / `.ps1`
- ✅ [AUTO] Full Build Verification Gate + `scripts/pre-release-gate.sh` green on `main`

### Sprint M1 Parallel

- ✅ [AGENT] Web bundle size budget in CI (`scripts/check-bundle-size.sh`)
- ✅ [AGENT] Playwright visual snapshot regression test
- ✅ [AGENT] Service-worker offline smoke test
- ✅ [AGENT] Android Fastlane metadata stub
- ✅ [AGENT] Android emulator checklist in `examples/android/README.md`
- ✅ [AGENT] Optional pyright CI job for Python
- ✅ [AGENT] Add `.cursor/rules/testing.mdc` (coverage budgets)
- ✅ [AGENT] Add `.cursor/rules/ci-gates.mdc` (post-push poll protocol)
- ✅ [AGENT] PROMPT_LIBRARY Entry 12 — Stack prune complete
- ✅ [AGENT] PROMPT_LIBRARY Entry 13 — Session state restore
- ✅ [AGENT] PROMPT_LIBRARY Entry 14 — Parallel agent scope map
- ✅ [AGENT] OpenSSF Scorecard weekly workflow
- ✅ [AGENT] `scripts/check-parallel-scope.sh`
- ✅ [AUTO] CI matrix green including `android-release` and coverage gate
- ✅ [AGENT] Conventional Commits PR title check (`amannn/action-semantic-pull-request`)

### Sprint M3 Parallel

- ✅ [HUMAN] Decide which optional modules to ship — all three (Lightroom, Rust, Go); see `DECISION_LOG.md`
- ✅ [AGENT] Lightroom lint/checklist in CI (Lua SDK namespace grep)
- ✅ [AGENT] Rust CI job (`cargo fmt`, `clippy`, `test`)
- ✅ [AGENT] Go CI job (`go vet`, `gofmt`, `test`)
- ✅ [AGENT] F-Droid submission dry-run checklist doc (`modules/android/MODULE.md`)

### Milestone Gates

- ✅ [AUTO] Regression tests: zero failures
- ✅ [AUTO] Static analysis and vulnerability scans clean
- ✅ [AUTO] `scripts/pre-release-gate.sh` passes before release tag (M0)

## Sprint M7 — Incremental Feature Assembly + Agent Gates (2026-06-15)

- ✅ [AGENT] Add `docs/FEATURE_MODULES.md` and `.cursor/rules/feature-modules.mdc`
- ✅ [AGENT] Add `feature-gate.sh`, `feature-autofix.sh`, `agent-progress.sh`, `watch-agent-gates.sh`, `smoke-stack.sh` (+ `.ps1`)
- ✅ [AGENT] Extend session-state example, `ci-gates.mdc`, `testing.mdc`, `destructive-ops.mdc`; gitignore `agent-progress.json`
- ✅ [AGENT] Update BUILD_PLAN Sprint 2+ template, INITIALIZATION_PROMPT, FOR_AGENTS, PROMPT_LIBRARY Entry 17
- ✅ [AGENT] Harden agent handoff: `gates_passed`, `failed_stage`, `log_tail` in `agent-progress.sh`; `--step` forwarding
- ✅ [AGENT] Fix `watch-agent-gates.sh` JSON capture; scoped `--paths` autofix; `GATES_PASSED` subshell fix
- ✅ [AGENT] Add `FEATURE_MODULES.md` to `validate-bootstrap.sh`; cross-link `START_HERE.md`; node MODULE Feature gate section
- ✅ [AGENT] Integrate M7 closeout + Sprint M8 block into BUILD_PLAN.md

## Sprint M8 — Feature Gate CI Enforcement (2026-06-15)

- ✅ [AGENT] CI **Feature Gate** job with `--strict` multi-stack
- ✅ [AGENT] `pre-release-gate.sh` runs `feature-gate.sh`
- ✅ [AUTO] Branch protection includes Repo Hygiene + Feature Gate via `setup-github-repo.sh`
- ✅ [AUTO] `verify-about-feature-gate.sh`, `check-security-triage.sh`, `check-readme-health.sh`
- ✅ [AUTO] CI green on `810e259`; BUILD_PLAN HUMAN rows re-labeled to AGENT/AUTO where automatable

## Sprint M6 — Repo Hygiene Automation (2026-06-15)

- ✅ [AGENT] Add `.gitattributes`, `.editorconfig`, `.cursorignore`; expand `.gitignore`
- ✅ [AGENT] Add `check-tracked-artifacts`, `check-large-tracked-files`, `check-repo-hygiene`, `purge-ephemeral` scripts (+ `.ps1`)
- ✅ [AGENT] Wire repo-hygiene into pre-commit, `validate-bootstrap.sh`, and CI `repo-hygiene` job
- ✅ [AGENT] Add `docs/REPO_HYGIENE.md` and `.cursor/rules/repo-hygiene.mdc`
- ✅ [AUTO] CI **Repo Hygiene** job green after merge
- ✅ [AGENT] Archive Sprint M6 completions to `COMPLETED_TASKS.md`
- ✅ [AGENT] Index hygiene `.ps1` twins in `TEMPLATE_INDEX.json`

## Maintainer gate cycle (2026-06-15)

- ✅ [AUTO] `check-security-triage.sh --wait-ci 120` — zero Critical/High Dependabot; CI + Security Scan + CodeQL green on `f3013a0`
- ✅ [AUTO] `pre-release-gate.sh` — feature-gate, CI, Dependabot, `.template-version` 0.7.1
- ✅ [AUTO] `simulate-template-upgrade.sh` passed
- ✅ [AUTO] `run-maintainer-gates.sh --quick` — readme, fdroid metadata, feature-gate, CI jobs Repo Hygiene + Feature Gate
- ✅ [AUTO] `check-license-compliance.sh web` passed
- ✅ [AGENT] Fix Scorecard workflow job-level permissions (was failing publish_results)
- ✅ [AGENT] Add `docs/features/_template.md`, `docs/features/settings.md`, `verify-fdroid-metadata.sh`, `run-maintainer-gates.sh`
- ✅ [AGENT] F-Droid metadata scaffold: changelogs/1.txt, images/README.md
- ✅ [AUTO] Release Please PR #11 open (`chore(main): release 0.8.0`); pre-release gate green on `main`

## Sprint 2 starter scaffold (template maintainer, 2026-06-15)

- ✅ [AGENT] Feature acceptance template + Settings feature draft in `docs/features/`
- ✅ [AGENT] About screen remains Sprint 1 reference exemplar (not duplicated as Sprint 2 feature)
- ✅ [AGENT] BUILD_PLAN Sprint 2+ feature template rows indexed for child repos

## BUILD_PLAN cleanup (2026-06-15)

- ✅ [AGENT] Archive completed M5–M8 sprints; remove stale `✅` rows from active board
- ✅ [AGENT] Consolidate milestone gates into recurring pre-release + `run-maintainer-gates.sh`
- ✅ [AGENT] Split child-repo playbook from template-maintainer open items

## Code review → Sprint M9 integration (2026-06-15)

- ✅ [AGENT] Integrate 46 code-review findings into BUILD_PLAN Sprint M9 (Sequential + Parallel + Critique)
- ✅ [AGENT] Update PARALLEL_AGENT_SCOPES.md with M9 active scopes
- ✅ [AGENT] Reconcile child-repo Sprint 0 sign-off; simplify per-feature checklist; restore lane structure

## Sprint M9 — Sequential 1–7 (2026-06-15)

- ✅ [HUMAN/AGENT] Commit maintainer artifacts; scorecard fix; feature docs; metadata scaffold
- ✅ [AGENT] Fix 3-strike logic; `verify-agent-strikes.sh`
- ✅ [AGENT] `agent-progress.sh next --lane maintainer`; default `--step gate`
- ✅ [AGENT] `feature-gate.sh`: file-limits, python mypy/pyright; CI-only web gates documented
- ✅ [AGENT] Paginated Dependabot; `pre-release-gate` in `release.yml` workflow_dispatch
- ✅ [AGENT] TEMPLATE_INDEX bulk index + reverse validate-template-index scan
- ✅ [AGENT] About exemplar: AppShell refactor, Android UpdateStatusEvaluator, expanded about unit tests

## Sprint M9 — Sequential 8–12 + Parallel A–D (2026-06-15)

- ✅ [AGENT] Settings vertical slice per `docs/features/settings.md` (web + android containers, tests, i18n)
- ✅ [AGENT] Extend `check-file-limits.sh` for `.kt` Compose + `components/*.ts`; node in `init-project` stack picker
- ✅ [AGENT] Reconcile Sprint 0 sign-off across BUILD_PLAN, `INITIALIZATION_PROMPT.md`, `read-before-write.mdc`
- ✅ [AGENT] Scorecard in `check-security-triage.sh`; update `SECURITY.md`, `MAINTAINING_THE_TEMPLATE.md`, `START_HERE.md`, `FEATURE_MODULES.md`
- ✅ [AGENT] Module E/F renumbering; ADR-0000 template baseline; `security-triage.mdc`
- ✅ [AGENT] Parallel A: web settings slice + e2e smoke
- ✅ [AGENT] Parallel B: android settings slice + tests
- ✅ [AGENT] Parallel C: gate/CI hardening (file-limits, Scorecard triage)
- ✅ [AGENT] Parallel D: docs + rules + index (Node column, ADR-0000, security-triage.mdc)
- ✅ [AGENT] F-Droid image paths under `metadata/en-US/images/`; fdroiddata handoff in `modules/android/MODULE.md`

## BUILD_PLAN cleanup (2026-06-15, M9 closeout)

- ✅ [AGENT] Archive completed M9 AGENT rows; slim active board to release + distribution open items

## Sprint M11 — Post-M10 hardening (AGENT, 2026-06-15)

- ✅ [AGENT] Fix Android compile errors (`MainActivity` launch import; `GoldenPathApp` scope.launch)
- ✅ [AGENT] CodeQL java-kotlin: setup-java, Android SDK, Gradle assembleDebug before analyze
- ✅ [AGENT] ReleaseTagFetcher on Dispatchers.IO; offline + CheckSchedule gating; ReleaseAssetSelector wired
- ✅ [AGENT] release.yml: full pre-release on workflow_dispatch; lightweight tag gate (version + CI snapshot)
- ✅ [AGENT] Robolectric DataStore tests: ThemePreferencesTest, AppUpdatePreferencesTest
- ✅ [AGENT] About parity: clickable donations, no_compatible string, header nav toggle, BuildConfig.VERSION_NAME
- ✅ [AGENT] Web appBootstrap.ts composition root; settings.md wiring map updated
- ✅ [AGENT] Gate dedupe: run-maintainer-gates full mode uses pre-release only; check-github-ci --jobs
- ✅ [AGENT] Prune stale about.update.interval.* i18n; web e2e for update-check + About panel

## Sprint M12 — Post-M11 polish (AGENT, 2026-06-15)

- ✅ [AGENT] CodeQL Android: init before Gradle traced build
- ✅ [AGENT] Tag release gate `--wait 300 --jobs "Repo Hygiene,Feature Gate"`; `check-github-ci.ps1` `-Jobs`
- ✅ [AGENT] Robolectric DataStore isolation + `pendingRestart` test
- ✅ [AGENT] `ReleaseTagFetcherTest`, `DonationsLoaderTest`, `MainActivitySmokeTest`
- ✅ [AGENT] Web `appBootstrap.ts` vitest coverage + smoke tests
- ✅ [AGENT] Android `pendingRestart` UI stub in `GoldenPathApp`; DESIGN_GUIDE parity note
- ✅ [AGENT] Composition-root docs (`FEATURE_MODULES.md`, `feature-modules.mdc`, BUILD_PLAN Sprint 2)
- ✅ [AGENT] CHANGELOG M10/M11/M12; exemplar vs `.template-version` in MAINTAINING_THE_TEMPLATE; bug_report placeholder
- ✅ [AUTO] CodeQL workflow green on `main` after push (`7055255`)
- ✅ [HUMAN] Merge Release Please PR #11 after CodeQL + branch-protection checks green

## v0.9.0 release (2026-06-15)

- ✅ [HUMAN] Approve release tag; merge Release Please PR #12 (`chore(main): release 0.9.0`, `fd699bc`)
- ✅ [AUTO] Release Please published [v0.9.0](https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.9.0)
- ✅ [AUTO] CI + Feature Gate + CodeQL green on `main` after merge (`fd699bc`)

## v0.8.0 release (2026-06-15)

- ✅ [HUMAN] Merge Release Please PR #11 (`chore(main): release 0.8.0`, `10b46d6`)
- ✅ [AUTO] CI + Feature Gate + CodeQL green on `main` after M12 (`7055255`)

## BUILD_PLAN cleanup (2026-06-15, M12 + v0.8.0 closeout)

- ✅ [AGENT] Archive M12 sprint body; slim active board to distribution + maintainer open items
- ✅ [AGENT] Unicode task markers (`✅` / `⬜`) across BUILD_PLAN and checklist docs

## Sprint M13 — Human-gate automation (AGENT, 2026-06-15)

- ✅ [AGENT] `verify-branch-protection.sh` / `.ps1` — gh API compare vs `setup-github-repo.sh` defaults
- ✅ [AGENT] `init-project.sh` / `.ps1` `--stack`, `--prune`, and related CLI flags
- ✅ [AGENT] `verify-reproducible-apk.sh` / `.ps1` — local double-build hash check (CI parity)
- ✅ [AGENT] Wire branch-protection into `run-maintainer-gates.sh`; `TEMPLATE_INDEX.json` entries
- ✅ [AUTO] `verify-branch-protection.sh` green on template repo `main`

## Sprint M14 — Post-M13 review remediation (AGENT, 2026-06-15)

- ✅ [AGENT] P0 version coherence: `.template-version`, `TEMPLATE_INDEX.json`, `AGENT_MEMORY.md` → 0.8.0; manifest assert in `pre-release-gate.sh`
- ✅ [AGENT] P0 `init-project.ps1` `2>$null` fix; `-NonInteractive` + Python placeholder replacement in both init scripts
- ✅ [AGENT] P1 `run-maintainer-gates.sh`: `verify-reproducible-apk.sh` wiring, `--skip-apk`, unknown-flag fail, `--quick` docs
- ✅ [AGENT] P1 `verify-branch-protection.sh`: `strict` + `allow_force_pushes` asserts; rulesets note in `SECURITY_TRIAGE.md`
- ✅ [AGENT] P1 docs: `settings.md` in `TEMPLATE_INDEX.json`; reconcile `CHANGELOG.md` `[Unreleased]`; init CLI in `INITIALIZATION_PROMPT.md` §8
- ✅ [AGENT] P1 web: `AboutPanel.ts` DOM-safe donations; `APP_VERSION` via Vite `define`
- ✅ [AGENT] P1 Android: `check-file-limits.sh` GoldenPath UI roots; home-screen update status banner
- ✅ [AGENT] P1 CI: Android SBOM in `release.yml`; tag vs `workflow_dispatch` gate docs
- ✅ [AUTO] CI + Feature Gate green on `main` (`fc71433`)
- ✅ [HUMAN] Close stale M5 visual-review row (superseded by maintainer README cycles)
- ✅ [AGENT] Init next-steps numbering fixed in `.sh` / `.ps1`

## Sprint M15 — P2 backlog (AGENT, 2026-06-15)

- ✅ [AGENT] Init `--keep-optional` / `--prune-optional` for rust/go/lightroom when pruning
- ✅ [AGENT] CodeQL rust/go exclusion documented in `codeql.yml` + `modules/rust|go/MODULE.md`
- ✅ [AGENT] Playwright e2e: update check enabled → About status assertion
- ✅ [AGENT] `simulate-template-upgrade.sh` non-interactive init smoke
- ✅ [AGENT] `MainActivitySmokeTest` migrated to `ActivityScenarioRule`
- ✅ [AUTO] CI + Feature Gate green on `main` (`a5f3199`)
- ✅ [AGENT] `connectedDebugAndroidTest` CI job (`android-instrumented`); documented in `modules/android/MODULE.md`
- ✅ [AGENT] `release.yml` SBOM upload on `release` published + Release Please dispatch; tag push gate-only split
- ✅ [AUTO] CI + Feature Gate green on `main` (`5195c46`)

## BUILD_PLAN cleanup (2026-06-15, M15 complete)

- ✅ [AGENT] Archive M15 sprint body; slim board to maintenance + human open items

## BUILD_PLAN cleanup (2026-06-15, M14 + v0.9.0 archive)

- ✅ [AGENT] Archive M14 sprint body; promote P2 to Sprint M15 active board
- ✅ [AGENT] Reset pre-release checklist for next version cycle

## Sprint M10 — Code review remediation (AGENT, 2026-06-15)

- ✅ [AGENT] M9-8 settings slice + parallel A–D committed; BUILD_PLAN cleanup
- ✅ [AGENT] Branch protection: export `GITHUB_REQUIRED_CHECKS` in `setup-github-repo.sh`; docs sync (5 checks)
- ✅ [AGENT] Node stack init: prune paths, `init-stack-sync.py` MODULE_LINES + PARALLEL_NOTES, INITIALIZATION_PROMPT Node row
- ✅ [AGENT] `check-security-triage.sh --strict`; Scorecard in `pre-release-gate.sh`; `SECURITY_TRIAGE.md` Scorecard section
- ✅ [AGENT] Gate parity: `--strict` in pre-release/maintainer gates; `pre-release-gate.sh` on tag push in `release.yml`
- ✅ [AGENT] Web settings fidelity: i18n, CSS, vitest coverage, cold-restart e2e, theme toggle sync
- ✅ [AGENT] Android settings fidelity: theme FilterChips, innerPadding, CheckSchedule tests
- ✅ [AGENT] Android About parity: DonationsLoader, ReleaseTagFetcher, GoldenPathApp composition root
- ✅ [AGENT] Opt-in update checks default `off`; About interval UI removed (Settings toggle only)
- ✅ [AGENT] CI/release: CodeQL java-kotlin, node SBOM + health-check audit

