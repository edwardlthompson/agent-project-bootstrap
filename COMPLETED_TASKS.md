# Completed Tasks

> Archive of finished BUILD_PLAN items.

## Sprint M5 — README Visual Refresh (2026-06-12)

- [x] [AGENT] Harden `scripts/normalize-markdown-whitespace.py` — table-aware blank-line collapse
- [x] [AGENT] Add `scripts/check-markdown-tables.sh`; hook into `validate-bootstrap.sh`
- [x] [AGENT] Redesign README sections — shields.io badges + HTML `<dl>`/tables for What's Included, BUILD_PLAN Labels, Template Update Checker, Supported Stacks
- [x] [AGENT] Add README badge conventions to `docs/MAINTAINING_THE_TEMPLATE.md`
- [x] [AGENT] Run verification — encoding, design cohesion, markdown table lint, TEMPLATE_INDEX validation
- [ ] [HUMAN] Visual review on GitHub after push — badges load, links resolve

## Template Maintainer — v0.2.1 Full Bootstrap Hardening (2026-06-13)

- [x] [AGENT] Normalize `.gitignore` UTF-16 to UTF-8; extend encoding scan and pre-commit hook
- [x] [AGENT] Sync `PROMPT_LIBRARY.md` entries 4, 6, 8, 9; populate `KNOWLEDGE_BASE.md` (6 entries)
- [x] [AGENT] Document Lighthouse 3-run median in `modules/web/MODULE.md`
- [x] [AGENT] SHA-pin `release.yml` actions; add pin policy to `docs/SECURITY_TRIAGE.md`
- [x] [AGENT] Add `check-workflow-action-ref-format.sh` pre-commit hook
- [x] [AGENT] Init scripts: `validate-workflow-actions` + `check-github-ci` reminder
- [x] [AGENT] Devcontainer: encoding check, gh CLI feature, CI gate tip
- [x] [AGENT] Add `health-check.yml` weekly workflow
- [x] [AGENT] Bootstrap Gradle wrapper; CI `android-build` assembleDebug job
- [x] [AGENT] Bump to v0.2.1; sync `TEMPLATE_INDEX.json`, `CHANGELOG.md`, `README.md`
- [x] [HUMAN] Set GitHub About from `docs/GITHUB_ABOUT.md` (via `gh repo edit`)
- [x] [HUMAN] Create GitHub Release tag `v0.2.1` (https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.1)
- [x] [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection (CI + Security Scan + CodeQL)
- [x] [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson` (template maintainer)

## Template Maintainer — v0.2.0 Backlog Fix (2026-06-12)

- [x] [AGENT] Normalize UTF-16 files to UTF-8; add `scripts/check-file-encoding.sh` + CI + pre-commit
- [x] [AGENT] Add `package-lock.json`, `uv.lock`, `.env.example`; expand `validate-bootstrap.sh`
- [x] [AGENT] Sync `TEMPLATE_INDEX.json` with LICENSE, scripts, workflows, rules
- [x] [AGENT] Sync README, SECURITY_TRIAGE, RUNBOOK, UPGRADING_FROM_TEMPLATE, PROMPT_LIBRARY, CHANGELOG
- [x] [AGENT] Harden license-compliance CI; web coverage budget; android ops checklist
- [x] [AGENT] Harden INITIALIZATION_PROMPT Sections 2/7/8 with Build Verification Gate
- [x] [AGENT] Update BUILD_PLAN Sprint 0 + Milestone Gates
- [x] [AGENT] Bump `.template-version` to 0.2.0; finalize CHANGELOG
- [x] [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection, About
- [x] [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson`

## Template Maintainer — v0.6.0+ Web Layout & CI Fixes (2026-06-13)

- [x] [AGENT] Add `docs/WEB_PROJECT_LAYOUT.md` and agent routing for docs/ vs examples/web/
- [x] [AGENT] Localization scaffold docs (web `locales/` + Android `strings.xml`) separated from styles
- [x] [AGENT] Android `NetworkStatusMonitor` for online/offline status parity with web
- [x] [AGENT] Harden `check-design-cohesion` (CSS content guard, main.ts i18n, PS1 parity)
- [x] [AUTO] CI, Security Scan, CodeQL, and GitHub Pages green on `main` (commit `38ce003`)
- [x] [HUMAN] Enable GitHub Pages (Actions source) and workflow PR permissions via repo settings

## Sprint M0 — Template Hardening v0.2.2

- [x] [AGENT] Add `scripts/setup-github-repo.sh` and `scripts/setup-github-repo.ps1` — idempotent Dependabot alerts, private vulnerability reporting, branch protection/rulesets (CI + Security Scan + CodeQL); print UI fallback checklist on API 422
- [x] [AGENT] Add gitleaks CI job to `.github/workflows/security.yml` (or `ci.yml`) on PR + `main` push
- [x] [AGENT] Add `check-file-limits` and `validate-bootstrap --quick` to `.pre-commit-config.yaml`
- [x] [AGENT] Add `scripts/pre-release-gate.sh` and `scripts/pre-release-gate.ps1` — CI poll, Dependabot Critical/High count, template version/tag match, release dry-run reminder
- [x] [AGENT] Add KNOWLEDGE_BASE KB-007 (npm/pip overrides policy for transitive CVEs); document `@lhci/cli` override in DECISION_LOG
- [x] [AGENT] Add `npm audit` step to `examples/web` and `uv pip audit` (or equivalent) to weekly `.github/workflows/health-check.yml`
- [x] [AGENT] Sync `AGENT_MEMORY.md` seed template version with `.template-version`; fix stale `0.1.0` reference
- [x] [AGENT] Bump `.template-version` to `0.2.2`; update CHANGELOG, TEMPLATE_INDEX, README

## Sprint M1 — Template Hardening v0.3.0

- [x] [AGENT] Extend `init-project.sh` / `.ps1` with interactive stack picker (web / python / android / multi / none) — prune unused `examples/` and `modules/`, never delete LICENSE/CI/scripts
- [x] [AGENT] On init: sync `AGENT_MEMORY.md` active modules; emit minimal BUILD_PLAN Parallel section for chosen stack
- [x] [AGENT] Add `.cursor-session-state.example.json` schema; document restore flow in `docs/FOR_AGENTS.md`
- [x] [AGENT] Expand `docs/FOR_AGENTS.md` failure playbook (CI poll, GH_TOKEN, Dependabot conflicts, 3-strike escalation, parallel scope collision grep)
- [x] [AGENT] Add `android-release` CI job — `SOURCE_DATE_EPOCH=1700000000 ./gradlew assembleRelease`, FOSS grep, optional two-run APK hash compare with flake tolerance
- [x] [AGENT] Enforce `pytest --cov-fail-under=90` in CI for `examples/python`
- [x] [AGENT] Add Conventional Commits PR title check (`amannn/action-semantic-pull-request`) to `.github/workflows/ci.yml`
- [x] [AGENT] Draft `docs/adr/0001-core-architecture.md` pattern for child repos (MVVM / Clean / Hexagonal choice template)
- [x] [AGENT] Bump `.template-version` to `0.3.0`; update CHANGELOG, TEMPLATE_INDEX, README

## Sprint M2 — Template Features v0.4.0

- [x] [AGENT] Add `modules/node/MODULE.md` and `examples/node/` Golden Path stub (Fastify or Hono, MIT, typed, vitest)
- [x] [AGENT] Add Node CI job to `.github/workflows/ci.yml` (lint, test, locked install)
- [x] [AGENT] Add GitHub Pages deploy workflow for `examples/web` demo (FOSS, no tracking)
- [x] [AGENT] Add Dependabot auto-merge workflow — patch/minor only, requires CI + dependency-review pass, excludes major without `[HUMAN]` label
- [x] [AGENT] Add changelog automation (`release-please` or `git-cliff`) wired to Conventional Commits
- [x] [AGENT] Add `scripts/simulate-template-upgrade.sh` — clone, init, cherry-pick per `docs/UPGRADING_FROM_TEMPLATE.md`, assert validate-bootstrap passes
- [x] [AGENT] Add composite GitHub Action `action.yml` exporting `validate-bootstrap` for downstream repos
- [x] [AGENT] Bump `.template-version` to `0.4.0`; update CHANGELOG, TEMPLATE_INDEX, README
- [x] [AUTO] Upgrade simulation test passes in CI (optional scheduled job)
- [x] [AGENT] GitHub Actions stale bot (`actions/stale`); exempt `template-improvement` (`.github/workflows/stale.yml`)
- [x] [AGENT] PR coverage comment job (vitest + pytest artifacts; Codecov optional) (`.github/workflows/ci.yml`)
- [x] [AGENT] `scripts/generate-winget-manifest.sh` stub generator (`packaging/winget/**`, `scripts/`)
- [x] [AGENT] F-Droid `metadata/` template in `examples/android/` (`examples/android/metadata/**`)
- [x] [AGENT] Per-stack SBOM slices on GitHub Release (`examples/web`, `examples/python`) (`.github/workflows/release.yml`)
- [x] [AGENT] PROMPT_LIBRARY Entry 15 — Post-release regression (`PROMPT_LIBRARY.md`)
- [x] [AGENT] PROMPT_LIBRARY Entry 16 — Template upgrade simulation (`PROMPT_LIBRARY.md`)
- [x] [AGENT] Issue template: auto-suggest `.template-version` in placeholder text (`.github/ISSUE_TEMPLATE/*.yml`)

## Sprint M3 — Ecosystem Expansion v0.5.0+

- [x] [AGENT] Add `examples/lightroom/` minimal stub (`Info.lua`, SDK version doc) per `modules/lightroom/MODULE.md`
- [x] [AGENT] Update `TEMPLATE_INDEX.json` — set `examples/lightroom` module `example` path
- [x] [AGENT] (Optional) Add `modules/rust/MODULE.md` + `examples/rust/` stub behind stack picker
- [x] [AGENT] (Optional) Add `modules/go/MODULE.md` + `examples/go/` stub behind stack picker
- [x] [AGENT] Gate new module CI behind workflow matrix `inputs.stack` or path filters to control CI minutes

## Sprint M4 — Design System v0.6.0

- [x] [AGENT] Add `design-tokens/` + schema + `scripts/sync-design-tokens.py`
- [x] [AGENT] Migrate Android example to Compose M3 + theme toggle (DataStore) + `strings.xml` i18n
- [x] [AGENT] Refactor web example: CSS variables + theme toggle + `locales/` i18n scaffold
- [x] [AGENT] Add `docs/DESIGN_GUIDE.md` + `.cursor/rules/design-system.mdc`
- [x] [AGENT] Add `scripts/check-design-cohesion.sh` + validate-bootstrap wiring
- [x] [AUTO] `android-build` + web tests green (theme toggle smoke tests)
- [x] [AGENT] Web theme + i18n unit tests (`examples/web/src/theme.test.ts`, `examples/web/src/i18n/**`)
- [x] [AGENT] Android Compose theme components (`examples/android/.../ui/**`)

## Milestone Gates

- [x] [AUTO] Workflow action refs validated (`scripts/validate-workflow-actions.sh`)
- [x] [AUTO] Pre-commit bare-semver guard (`scripts/check-workflow-action-ref-format.sh`)
- [x] [AUTO] Android assembleDebug CI smoke on `examples/android/`
- [x] [AUTO] Weekly health-check workflow polls CI + Security Scan + CodeQL
- [x] [AUTO] UTF-8 encoding check clean (`scripts/check-file-encoding.sh`)
- [x] [AUTO] Lockfiles present and CI uses locked installs (`npm ci`, `uv sync --locked`)
- [x] [AUTO] `TEMPLATE_INDEX.json` complete (`scripts/validate-template-index.sh`)
- [x] [AUTO] Gitleaks CI job passes on `main` (M0)
- [x] [AUTO] Pre-commit includes file-limits and quick bootstrap validation (M0)
- [x] [AUTO] Android `assembleRelease` with `SOURCE_DATE_EPOCH` passes (M1)
- [x] [AUTO] Python coverage ≥ 90% in CI (M1)
- [x] [AUTO] Web bundle size budget within threshold (M1)
- [x] [AUTO] OpenSSF Scorecard run completed within last 30 days (M1)
- [x] [AUTO] Upgrade simulation test passes (M2)
- [x] [AUTO] GitHub Pages demo deploys successfully (M2)
- [x] [AUTO] Node example CI green when `examples/node/` present (M2)
## BUILD_PLAN Automation Pass (2026-06-13)

### Sprint 0 — Template (maintainer repo complete)

- [x] [AGENT] Create `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md`
- [x] [AGENT] Add `.github/CODEOWNERS` and `THIRD_PARTY_LICENSES.md`
- [x] [AGENT] Initialize workspace memory files from template seeds (`AGENT_MEMORY.md`, etc.)
- [x] [AGENT] Wire update checker config into devcontainer and README
- [x] [HUMAN] Set GitHub repo About description from `docs/GITHUB_ABOUT.md` (via `gh repo edit`)
- [x] [AGENT] Commit lockfiles (`package-lock.json`, `uv.lock`) and `.env.example`
- [x] [AGENT] Ensure `TEMPLATE_INDEX.json` includes all scripts, workflows, and playbooks
- [x] [AUTO] `scripts/check-file-encoding.sh` passes
- [x] [AUTO] Full Build Verification Gate (INITIALIZATION_PROMPT Section 7) green
- [x] [AUTO] `scripts/validate-bootstrap.sh` (expanded) passes in CI
- [x] [HUMAN] Enable Dependabot alerts + security updates
- [x] [HUMAN] Enable private vulnerability reporting + branch protection on `main` (via `setup-github-repo.sh`)
- [x] [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with `@edwardlthompson`

### Sprint 0 Parallel (maintainer)

- [x] [AGENT] Confirm GitHub Pages uses Actions (not `/docs` folder)
- [x] [AUTO] Verify pre-commit hooks install

### Sprint 1 — Golden Path (maintainer)

- [x] [AGENT] Propose directory structure for target stack
- [x] [AGENT] Draft ADR-0001 core architecture (`docs/adr/0001-core-architecture.md`)
- [x] [AGENT] Implement Golden Path reference feature (design tokens, i18n, theme toggle)
- [x] [AUTO] `scripts/check-design-cohesion.sh` passes
- [x] [AUTO] CI matrix green on main
- [x] [AGENT] Web PWA offline cache + bundle budget + visual snapshots
- [x] [AGENT] Python CLI + 90% coverage gate + pyright
- [x] [AGENT] Android FOSS skeleton + Fastlane metadata stub
- [x] [AGENT] Node API stub
- [x] [AGENT] CodeQL + Trivy workflow wiring
- [x] [AGENT] Devcontainer + pre-commit hooks

### Sprint M0 Parallel

- [x] [AGENT] Cross-platform `scripts/check-file-encoding.py` (UTF-8/UTF-16 BOM)
- [x] [AGENT] Add `.cursor/rules/windows-encoding.mdc`
- [x] [AGENT] Add PROMPT_LIBRARY Entry 10 — Pre-release gate
- [x] [AGENT] Add PROMPT_LIBRARY Entry 11 — GitHub repo setup
- [x] [AGENT] Document setup script in `docs/SECURITY_TRIAGE.md` § Setup
- [x] [AGENT] Wire `setup-github-repo` reminder into `init-project.sh` / `.ps1`
- [x] [AUTO] Full Build Verification Gate + `scripts/pre-release-gate.sh` green on `main`

### Sprint M1 Parallel

- [x] [AGENT] Web bundle size budget in CI (`scripts/check-bundle-size.sh`)
- [x] [AGENT] Playwright visual snapshot regression test
- [x] [AGENT] Service-worker offline smoke test
- [x] [AGENT] Android Fastlane metadata stub
- [x] [AGENT] Android emulator checklist in `examples/android/README.md`
- [x] [AGENT] Optional pyright CI job for Python
- [x] [AGENT] Add `.cursor/rules/testing.mdc` (coverage budgets)
- [x] [AGENT] Add `.cursor/rules/ci-gates.mdc` (post-push poll protocol)
- [x] [AGENT] PROMPT_LIBRARY Entry 12 — Stack prune complete
- [x] [AGENT] PROMPT_LIBRARY Entry 13 — Session state restore
- [x] [AGENT] PROMPT_LIBRARY Entry 14 — Parallel agent scope map
- [x] [AGENT] OpenSSF Scorecard weekly workflow
- [x] [AGENT] `scripts/check-parallel-scope.sh`
- [x] [AUTO] CI matrix green including `android-release` and coverage gate
- [x] [AGENT] Conventional Commits PR title check (`amannn/action-semantic-pull-request`)

### Sprint M3 Parallel

- [x] [HUMAN] Decide which optional modules to ship — all three (Lightroom, Rust, Go); see `DECISION_LOG.md`
- [x] [AGENT] Lightroom lint/checklist in CI (Lua SDK namespace grep)
- [x] [AGENT] Rust CI job (`cargo fmt`, `clippy`, `test`)
- [x] [AGENT] Go CI job (`go vet`, `gofmt`, `test`)
- [x] [AGENT] F-Droid submission dry-run checklist doc (`modules/android/MODULE.md`)

### Milestone Gates

- [x] [AUTO] Regression tests: zero failures
- [x] [AUTO] Static analysis and vulnerability scans clean
- [x] [AUTO] `scripts/pre-release-gate.sh` passes before release tag (M0)

## Sprint M7 — Incremental Feature Assembly + Agent Gates (2026-06-15)

- [x] [AGENT] Add `docs/FEATURE_MODULES.md` and `.cursor/rules/feature-modules.mdc`
- [x] [AGENT] Add `feature-gate.sh`, `feature-autofix.sh`, `agent-progress.sh`, `watch-agent-gates.sh`, `smoke-stack.sh` (+ `.ps1`)
- [x] [AGENT] Extend session-state example, `ci-gates.mdc`, `testing.mdc`, `destructive-ops.mdc`; gitignore `agent-progress.json`
- [x] [AGENT] Update BUILD_PLAN Sprint 2+ template, INITIALIZATION_PROMPT, FOR_AGENTS, PROMPT_LIBRARY Entry 17
- [x] [AGENT] Harden agent handoff: `gates_passed`, `failed_stage`, `log_tail` in `agent-progress.sh`; `--step` forwarding
- [x] [AGENT] Fix `watch-agent-gates.sh` JSON capture; scoped `--paths` autofix; `GATES_PASSED` subshell fix
- [x] [AGENT] Add `FEATURE_MODULES.md` to `validate-bootstrap.sh`; cross-link `START_HERE.md`; node MODULE Feature gate section
- [x] [AGENT] Integrate M7 closeout + Sprint M8 block into BUILD_PLAN.md

## Sprint M8 — Feature Gate CI Enforcement (2026-06-15)

- [x] [AGENT] CI **Feature Gate** job with `--strict` multi-stack
- [x] [AGENT] `pre-release-gate.sh` runs `feature-gate.sh`
- [x] [AUTO] Branch protection includes Repo Hygiene + Feature Gate via `setup-github-repo.sh`
- [x] [AUTO] `verify-about-feature-gate.sh`, `check-security-triage.sh`, `check-readme-health.sh`
- [x] [AUTO] CI green on `810e259`; BUILD_PLAN HUMAN rows re-labeled to AGENT/AUTO where automatable

## Sprint M6 — Repo Hygiene Automation (2026-06-15)

- [x] [AGENT] Add `.gitattributes`, `.editorconfig`, `.cursorignore`; expand `.gitignore`
- [x] [AGENT] Add `check-tracked-artifacts`, `check-large-tracked-files`, `check-repo-hygiene`, `purge-ephemeral` scripts (+ `.ps1`)
- [x] [AGENT] Wire repo-hygiene into pre-commit, `validate-bootstrap.sh`, and CI `repo-hygiene` job
- [x] [AGENT] Add `docs/REPO_HYGIENE.md` and `.cursor/rules/repo-hygiene.mdc`
- [x] [AUTO] CI **Repo Hygiene** job green after merge
- [x] [AGENT] Archive Sprint M6 completions to `COMPLETED_TASKS.md`
- [x] [AGENT] Index hygiene `.ps1` twins in `TEMPLATE_INDEX.json`

## Maintainer gate cycle (2026-06-15)

- [x] [AUTO] `check-security-triage.sh --wait-ci 120` — zero Critical/High Dependabot; CI + Security Scan + CodeQL green on `f3013a0`
- [x] [AUTO] `pre-release-gate.sh` — feature-gate, CI, Dependabot, `.template-version` 0.7.1
- [x] [AUTO] `simulate-template-upgrade.sh` passed
- [x] [AUTO] `run-maintainer-gates.sh --quick` — readme, fdroid metadata, feature-gate, CI jobs Repo Hygiene + Feature Gate
- [x] [AUTO] `check-license-compliance.sh web` passed
- [x] [AGENT] Fix Scorecard workflow job-level permissions (was failing publish_results)
- [x] [AGENT] Add `docs/features/_template.md`, `docs/features/settings.md`, `verify-fdroid-metadata.sh`, `run-maintainer-gates.sh`
- [x] [AGENT] F-Droid metadata scaffold: changelogs/1.txt, images/README.md
- [x] [AUTO] Release Please PR #11 open (`chore(main): release 0.8.0`); pre-release gate green on `main`

## Sprint 2 starter scaffold (template maintainer, 2026-06-15)

- [x] [AGENT] Feature acceptance template + Settings feature draft in `docs/features/`
- [x] [AGENT] About screen remains Sprint 1 reference exemplar (not duplicated as Sprint 2 feature)
- [x] [AGENT] BUILD_PLAN Sprint 2+ feature template rows indexed for child repos

## BUILD_PLAN cleanup (2026-06-15)

- [x] [AGENT] Archive completed M5–M8 sprints; remove stale `[x]` rows from active board
- [x] [AGENT] Consolidate milestone gates into recurring pre-release + `run-maintainer-gates.sh`
- [x] [AGENT] Split child-repo playbook from template-maintainer open items

## Code review → Sprint M9 integration (2026-06-15)

- [x] [AGENT] Integrate 46 code-review findings into BUILD_PLAN Sprint M9 (Sequential + Parallel + Critique)
- [x] [AGENT] Update PARALLEL_AGENT_SCOPES.md with M9 active scopes
- [x] [AGENT] Reconcile child-repo Sprint 0 sign-off; simplify per-feature checklist; restore lane structure

## Sprint M9 — Sequential 1–7 (2026-06-15)

- [x] [HUMAN/AGENT] Commit maintainer artifacts; scorecard fix; feature docs; metadata scaffold
- [x] [AGENT] Fix 3-strike logic; `verify-agent-strikes.sh`
- [x] [AGENT] `agent-progress.sh next --lane maintainer`; default `--step gate`
- [x] [AGENT] `feature-gate.sh`: file-limits, python mypy/pyright; CI-only web gates documented
- [x] [AGENT] Paginated Dependabot; `pre-release-gate` in `release.yml` workflow_dispatch
- [x] [AGENT] TEMPLATE_INDEX bulk index + reverse validate-template-index scan
- [x] [AGENT] About exemplar: AppShell refactor, Android UpdateStatusEvaluator, expanded about unit tests

## Sprint M9 — Sequential 8–12 + Parallel A–D (2026-06-15)

- [x] [AGENT] Settings vertical slice per `docs/features/settings.md` (web + android containers, tests, i18n)
- [x] [AGENT] Extend `check-file-limits.sh` for `.kt` Compose + `components/*.ts`; node in `init-project` stack picker
- [x] [AGENT] Reconcile Sprint 0 sign-off across BUILD_PLAN, `INITIALIZATION_PROMPT.md`, `read-before-write.mdc`
- [x] [AGENT] Scorecard in `check-security-triage.sh`; update `SECURITY.md`, `MAINTAINING_THE_TEMPLATE.md`, `START_HERE.md`, `FEATURE_MODULES.md`
- [x] [AGENT] Module E/F renumbering; ADR-0000 template baseline; `security-triage.mdc`
- [x] [AGENT] Parallel A: web settings slice + e2e smoke
- [x] [AGENT] Parallel B: android settings slice + tests
- [x] [AGENT] Parallel C: gate/CI hardening (file-limits, Scorecard triage)
- [x] [AGENT] Parallel D: docs + rules + index (Node column, ADR-0000, security-triage.mdc)
- [x] [AGENT] F-Droid image paths under `metadata/en-US/images/`; fdroiddata handoff in `modules/android/MODULE.md`

## BUILD_PLAN cleanup (2026-06-15, M9 closeout)

- [x] [AGENT] Archive completed M9 AGENT rows; slim active board to release + distribution open items

## Sprint M11 — Post-M10 hardening (AGENT, 2026-06-15)

- [x] [AGENT] Fix Android compile errors (`MainActivity` launch import; `GoldenPathApp` scope.launch)
- [x] [AGENT] CodeQL java-kotlin: setup-java, Android SDK, Gradle assembleDebug before analyze
- [x] [AGENT] ReleaseTagFetcher on Dispatchers.IO; offline + CheckSchedule gating; ReleaseAssetSelector wired
- [x] [AGENT] release.yml: full pre-release on workflow_dispatch; lightweight tag gate (version + CI snapshot)
- [x] [AGENT] Robolectric DataStore tests: ThemePreferencesTest, AppUpdatePreferencesTest
- [x] [AGENT] About parity: clickable donations, no_compatible string, header nav toggle, BuildConfig.VERSION_NAME
- [x] [AGENT] Web appBootstrap.ts composition root; settings.md wiring map updated
- [x] [AGENT] Gate dedupe: run-maintainer-gates full mode uses pre-release only; check-github-ci --jobs
- [x] [AGENT] Prune stale about.update.interval.* i18n; web e2e for update-check + About panel

## Sprint M10 — Code review remediation (AGENT, 2026-06-15)

- [x] [AGENT] M9-8 settings slice + parallel A–D committed; BUILD_PLAN cleanup
- [x] [AGENT] Branch protection: export `GITHUB_REQUIRED_CHECKS` in `setup-github-repo.sh`; docs sync (5 checks)
- [x] [AGENT] Node stack init: prune paths, `init-stack-sync.py` MODULE_LINES + PARALLEL_NOTES, INITIALIZATION_PROMPT Node row
- [x] [AGENT] `check-security-triage.sh --strict`; Scorecard in `pre-release-gate.sh`; `SECURITY_TRIAGE.md` Scorecard section
- [x] [AGENT] Gate parity: `--strict` in pre-release/maintainer gates; `pre-release-gate.sh` on tag push in `release.yml`
- [x] [AGENT] Web settings fidelity: i18n, CSS, vitest coverage, cold-restart e2e, theme toggle sync
- [x] [AGENT] Android settings fidelity: theme FilterChips, innerPadding, CheckSchedule tests
- [x] [AGENT] Android About parity: DonationsLoader, ReleaseTagFetcher, GoldenPathApp composition root
- [x] [AGENT] Opt-in update checks default `off`; About interval UI removed (Settings toggle only)
- [x] [AGENT] CI/release: CodeQL java-kotlin, node SBOM + health-check audit

