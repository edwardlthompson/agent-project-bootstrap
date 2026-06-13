# Build Plan

> Prioritized task board with owner labels, Sequential and Parallel lanes per sprint.

> Move completed items to `COMPLETED_TASKS.md`.

## Owner Label Legend

| Label | Owner | When to use |

|-------|-------|-------------|

| `AGENT` | Cursor Agent | Code, docs, scaffolding, tests, CI config |

| `HUMAN` | Human developer | Approvals, credentials, GitHub settings, product decisions |

| `ADB` | Human (Android) | Android SDK, emulator/device testing, F-Droid submission |

| `AUTO` | CI/scripts/bots | GitHub Actions, Dependabot, pre-commit, update checker |

**Task format:** `- [ ] [OWNER] Description`

**Filter by label:**

```bash

grep '\[AGENT\]' BUILD_PLAN.md

grep '\[HUMAN\]' BUILD_PLAN.md

grep '\[ADB\]' BUILD_PLAN.md

grep '\[AUTO\]' BUILD_PLAN.md

```

**Agent rule:** Execute all `[AGENT]` Sequential items first, then dispatch Parallel agents with isolated file scopes. Shared schema/types are Sequential-only.

> **Sprint M0–M3** are template-maintainer sprints (this repo). Child repos created from the template use Sprint 0–2 only.

---

## Sprint 0 — Template Customization

### Sequential (must complete in order)

1. [ ] [HUMAN] Click **Use this template** on GitHub to create your project repo

2. [ ] [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)

3. [ ] [HUMAN] Run `scripts/init-project.sh` or `scripts/init-project.ps1`

4. [ ] [HUMAN] Run `scripts/setup-github-repo.sh` (or `.ps1`) for Dependabot alerts, private vulnerability reporting, and branch protection

5. [ ] [HUMAN] Select stack during init (web / python / android / multi) to prune unused examples and modules

6. [ ] [HUMAN] Enable Dependabot alerts + security updates (see `docs/SECURITY_TRIAGE.md` § Setup)

7. [ ] [HUMAN] Enable private vulnerability reporting + branch protection on `main`

8. [ ] [AGENT] Create `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md`

9. [ ] [AGENT] Add `.github/CODEOWNERS` and `THIRD_PARTY_LICENSES.md`

10. [ ] [AGENT] Initialize workspace memory files from template seeds (`AGENT_MEMORY.md`, etc.)

11. [ ] [AGENT] Wire update checker config into devcontainer and README

12. [ ] [HUMAN] Set GitHub repo About description from `docs/GITHUB_ABOUT.md`

13. [ ] [AGENT] Commit lockfiles (`package-lock.json`, `uv.lock`) and `.env.example`

14. [ ] [AGENT] Ensure `TEMPLATE_INDEX.json` includes all scripts, workflows, and playbooks

15. [ ] [AUTO] `scripts/check-file-encoding.sh` passes

16. [ ] [AUTO] Full Build Verification Gate (INITIALIZATION_PROMPT Section 7) green

17. [ ] [AUTO] `scripts/validate-bootstrap.sh` (expanded) passes in CI

18. [ ] [HUMAN] Approve Sprint 0 only after CI green on `main` and Build Verification Gate passes

### Parallel (safe after Sequential step 10)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Prune unused `examples/` folders | AGENT | `examples/**` |

| Prune unused `modules/` folders | AGENT | `modules/**` |

| Run `scripts/sync-design-tokens.py` after brand customization | AGENT | `design-tokens/**` |

| Configure `.template-update.json` interval | HUMAN | `.template-update.json` |

| Confirm GitHub Pages uses Actions (not `/docs` folder) | AGENT | `.github/workflows/pages.yml`, `docs/WEB_PROJECT_LAYOUT.md` |

| Verify pre-commit hooks install | AUTO | `.pre-commit-config.yaml` |

---

## Sprint 1 — Golden Path Foundation

### Sequential (must complete in order)

1. [ ] [AGENT] Propose directory structure for target stack

2. [ ] [AGENT] Draft ADR-0001 core architecture (`docs/adr/0001-core-architecture.md`)

3. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1

4. [ ] [AGENT] Implement Golden Path reference feature (shared schema/types first; UI must use `design-tokens/` + `docs/DESIGN_GUIDE.md`; web strings in `src/locales/` + `t()`, Android in `strings.xml` + `stringResource`)

5. [ ] [AUTO] `scripts/check-design-cohesion.sh` passes (no UI string literals, no copy in CSS)

6. [ ] [AUTO] CI matrix green on main

### Parallel (safe after Sequential step 4)

> Guardrail: no two parallel tasks may modify overlapping files.

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Web PWA offline cache + bundle budget + visual snapshots | AGENT | `examples/web/**` |

| Python CLI + 90% coverage gate + optional pyright | AGENT | `examples/python/**` |

| Android FOSS skeleton + Fastlane metadata stub | AGENT | `examples/android/**` |

| Node API stub (if stack includes node) | AGENT | `examples/node/**` |

| CodeQL + Trivy workflow wiring | AGENT | `.github/workflows/**` |

| Devcontainer + pre-commit hooks | AGENT | `.devcontainer/**`, `.pre-commit-config.yaml` |

---

## Sprint 2 — First Real Feature

### Sequential (must complete in order)

1. [ ] [HUMAN] Define first feature milestone and acceptance criteria

2. [ ] [AGENT] Propose implementation plan with `### Critique` subsection

3. [ ] [HUMAN] Approve plan

4. [ ] [AGENT] Implement feature following Golden Path patterns

5. [ ] [AUTO] All quality gates pass (lint, test, coverage, file limits)

6. [ ] [HUMAN] Sign off for release

### Parallel (safe after Sequential step 4)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| _Define per feature_ | AGENT | _Isolated per agent scope_ |

---

## Ongoing Maintenance

### Weekly (recurring)

- [ ] [HUMAN] Run weekly CVE triage pass per `docs/SECURITY_TRIAGE.md` (recommended: Monday)

- [ ] [AGENT] Apply Dependabot dependency bumps and open PRs as needed

- [ ] [AUTO] Trivy + CodeQL + CI matrix green after merges

- [ ] [AUTO] OpenSSF Scorecard workflow result reviewed (after Sprint M1)

- [ ] [AUTO] `scripts/pre-release-gate.sh` run before any version bump

- [ ] [AGENT] Triage Scorecard findings into BUILD_PLAN `[AUTO]` items

### Monthly (recurring)

- [ ] [AUTO] Run `scripts/simulate-template-upgrade.sh` on schedule (first Monday)

- [ ] [HUMAN] Review `THIRD_PARTY_LICENSES.md` and SBOM for distribution

- [ ] [AGENT] Dependabot auto-merge PRs reviewed for override/transitive policy (KB-007)

---

## Sprint M0 — Template Hardening v0.2.2

> Template maintainer only. Target release: v0.2.2.

### Sequential (must complete in order)

1. [x] [AGENT] Add `scripts/setup-github-repo.sh` and `scripts/setup-github-repo.ps1` — idempotent Dependabot alerts, private vulnerability reporting, branch protection/rulesets (CI + Security Scan + CodeQL); print UI fallback checklist on API 422

2. [ ] [HUMAN] Run setup script on template repo; replace `@[PROJECT_OWNER]` in `.github/CODEOWNERS` with real GitHub username

3. [x] [AGENT] Add gitleaks CI job to `.github/workflows/security.yml` (or `ci.yml`) on PR + `main` push

4. [x] [AGENT] Add `check-file-limits` and `validate-bootstrap --quick` to `.pre-commit-config.yaml`

5. [x] [AGENT] Add `scripts/pre-release-gate.sh` and `scripts/pre-release-gate.ps1` — CI poll, Dependabot Critical/High count, template version/tag match, release dry-run reminder

6. [x] [AGENT] Add KNOWLEDGE_BASE KB-007 (npm/pip overrides policy for transitive CVEs); document `@lhci/cli` override in DECISION_LOG

7. [x] [AGENT] Add `npm audit` step to `examples/web` and `uv pip audit` (or equivalent) to weekly `.github/workflows/health-check.yml`

8. [x] [AGENT] Sync `AGENT_MEMORY.md` seed template version with `.template-version`; fix stale `0.1.0` reference

9. [x] [AGENT] Bump `.template-version` to `0.2.2`; update CHANGELOG, TEMPLATE_INDEX, README

10. [ ] [AUTO] Full Build Verification Gate + `scripts/pre-release-gate.sh` green on `main`

11. [ ] [HUMAN] Approve v0.2.2 release tag and GitHub Release

### Parallel (safe after Sequential step 5)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Cross-platform `scripts/check-file-encoding.py` (UTF-8/UTF-16 BOM) | AGENT | `scripts/check-file-encoding.py`, `scripts/check-file-encoding.sh` |

| Add `.cursor/rules/windows-encoding.mdc` | AGENT | `.cursor/rules/windows-encoding.mdc` |

| Add PROMPT_LIBRARY Entry 10 — Pre-release gate | AGENT | `PROMPT_LIBRARY.md` |

| Add PROMPT_LIBRARY Entry 11 — GitHub repo setup | AGENT | `PROMPT_LIBRARY.md` |

| Document setup script in `docs/SECURITY_TRIAGE.md` § Setup | AGENT | `docs/SECURITY_TRIAGE.md` |

| Wire `setup-github-repo` reminder into `init-project.sh` / `.ps1` | AGENT | `scripts/init-project.*` |

---

## Sprint M1 — Template Hardening v0.3.0

> Template maintainer only. Target release: v0.3.0.

### Sequential (must complete in order)

1. [x] [AGENT] Extend `init-project.sh` / `.ps1` with interactive stack picker (web / python / android / multi / none) — prune unused `examples/` and `modules/`, never delete LICENSE/CI/scripts

2. [x] [AGENT] On init: sync `AGENT_MEMORY.md` active modules; emit minimal BUILD_PLAN Parallel section for chosen stack

3. [x] [AGENT] Add `.cursor-session-state.example.json` schema; document restore flow in `docs/FOR_AGENTS.md`

4. [x] [AGENT] Expand `docs/FOR_AGENTS.md` failure playbook (CI poll, GH_TOKEN, Dependabot conflicts, 3-strike escalation, parallel scope collision grep)

5. [x] [AGENT] Add `android-release` CI job — `SOURCE_DATE_EPOCH=1700000000 ./gradlew assembleRelease`, FOSS grep, optional two-run APK hash compare with flake tolerance

6. [x] [AGENT] Enforce `pytest --cov-fail-under=90` in CI for `examples/python`

7. [x] [AGENT] Add Conventional Commits PR title check (`amannn/action-semantic-pull-request`) to `.github/workflows/ci.yml`

8. [x] [AGENT] Draft `docs/adr/0001-core-architecture.md` pattern for child repos (MVVM / Clean / Hexagonal choice template)

9. [x] [AGENT] Bump `.template-version` to `0.3.0`; update CHANGELOG, TEMPLATE_INDEX, README

10. [ ] [AUTO] CI matrix green including `android-release` and coverage gate

11. [ ] [HUMAN] Approve v0.3.0 release

### Parallel (safe after Sequential step 4)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Web bundle size budget in CI (`vite build` report threshold) | AGENT | `examples/web/**`, `ci.yml` |

| Playwright visual snapshot regression test | AGENT | `examples/web/e2e/**` |

| Service-worker offline smoke test | AGENT | `examples/web/**` |

| Android Fastlane metadata stub `examples/android/fastlane/metadata/android/en-US/` | AGENT | `examples/android/fastlane/**` |

| Android emulator checklist in `examples/android/README.md` | AGENT | `examples/android/README.md` |

| Optional pyright or `ty` CI job for Python | AGENT | `examples/python/**`, `ci.yml` |

| Add `.cursor/rules/testing.mdc` (coverage budgets) | AGENT | `.cursor/rules/testing.mdc` |

| Add `.cursor/rules/ci-gates.mdc` (post-push poll protocol) | AGENT | `.cursor/rules/ci-gates.mdc` |

| PROMPT_LIBRARY Entry 12 — Stack prune complete | AGENT | `PROMPT_LIBRARY.md` |

| PROMPT_LIBRARY Entry 13 — Session state restore | AGENT | `PROMPT_LIBRARY.md` |

| PROMPT_LIBRARY Entry 14 — Parallel agent scope map | AGENT | `PROMPT_LIBRARY.md`, `docs/PARALLEL_AGENT_SCOPES.md` |

| OpenSSF Scorecard weekly workflow | AGENT | `.github/workflows/scorecard.yml` |

| `scripts/check-parallel-scope.sh` — detect BUILD_PLAN scope overlap | AGENT | `scripts/check-parallel-scope.sh` |

---

## Sprint M2 — Template Features v0.4.0

> Template maintainer only. Target release: v0.4.0.

### Sequential (must complete in order)

1. [x] [AGENT] Add `modules/node/MODULE.md` and `examples/node/` Golden Path stub (Fastify or Hono, MIT, typed, vitest)

2. [x] [AGENT] Add Node CI job to `.github/workflows/ci.yml` (lint, test, locked install)

3. [x] [AGENT] Add GitHub Pages deploy workflow for `examples/web` demo (FOSS, no tracking)

4. [x] [AGENT] Add Dependabot auto-merge workflow — patch/minor only, requires CI + dependency-review pass, excludes major without `[HUMAN]` label

5. [x] [AGENT] Add changelog automation (`release-please` or `git-cliff`) wired to Conventional Commits

6. [x] [AGENT] Add `scripts/simulate-template-upgrade.sh` — clone, init, cherry-pick per `docs/UPGRADING_FROM_TEMPLATE.md`, assert validate-bootstrap passes

7. [x] [AGENT] Add composite GitHub Action `action.yml` exporting `validate-bootstrap` for downstream repos

8. [x] [AGENT] Bump `.template-version` to `0.4.0`; update CHANGELOG, TEMPLATE_INDEX, README

9. [x] [AUTO] Upgrade simulation test passes in CI (optional scheduled job)

10. [ ] [HUMAN] Approve v0.4.0 release

### Parallel (safe after Sequential step 4)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| GitHub Actions stale bot (`actions/stale`); exempt `template-improvement` | AGENT | `.github/workflows/stale.yml` | [x] |

| PR coverage comment job (vitest + pytest artifacts; Codecov optional) | AGENT | `.github/workflows/ci.yml` | [x] |

| `scripts/generate-winget-manifest.sh` stub generator | AGENT | `packaging/winget/**`, `scripts/` | [x] |

| F-Droid `metadata/` template in `examples/android/` | AGENT | `examples/android/metadata/**` | [x] |

| Per-stack SBOM slices on GitHub Release (`examples/web`, `examples/python`) | AGENT | `.github/workflows/release.yml` | [x] |

| PROMPT_LIBRARY Entry 15 — Post-release regression | AGENT | `PROMPT_LIBRARY.md` | [x] |

| PROMPT_LIBRARY Entry 16 — Template upgrade simulation | AGENT | `PROMPT_LIBRARY.md` | [x] |

| Issue template: auto-suggest `.template-version` in placeholder text | AGENT | `.github/ISSUE_TEMPLATE/*.yml` | [x] |

---

## Sprint M3 — Ecosystem Expansion v0.5.0+

> Template maintainer only. Target release: v0.5.0+.

### Sequential (must complete in order)

1. [ ] [HUMAN] Decide which optional modules to ship (Lightroom example, Rust, Go)

2. [x] [AGENT] Add `examples/lightroom/` minimal stub (`Info.lua`, SDK version doc) per `modules/lightroom/MODULE.md`

3. [x] [AGENT] Update `TEMPLATE_INDEX.json` — set `examples/lightroom` module `example` path

4. [x] [AGENT] (Optional) Add `modules/rust/MODULE.md` + `examples/rust/` stub behind stack picker

5. [x] [AGENT] (Optional) Add `modules/go/MODULE.md` + `examples/go/` stub behind stack picker

6. [x] [AGENT] Gate new module CI behind workflow matrix `inputs.stack` or path filters to control CI minutes

7. [ ] [HUMAN] Approve v0.5.0 release scope

### Parallel (safe after Sequential step 2)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Lightroom lint/checklist in CI (Lua SDK namespace grep) | AGENT | `examples/lightroom/**`, `ci.yml` |

| Rust CI job (if module approved) | AGENT | `examples/rust/**`, `ci.yml` |

| Go CI job (if module approved) | AGENT | `examples/go/**`, `ci.yml` |

| F-Droid submission dry-run checklist doc | ADB | `modules/android/MODULE.md`, `docs/` |

---

## Sprint M4 — Design System v0.6.0

> Template maintainer only. Target release: v0.6.0.

### Sequential (must complete in order)

1. [x] [AGENT] Add `design-tokens/` + schema + `scripts/sync-design-tokens.py`

2. [x] [AGENT] Migrate Android example to Compose M3 + theme toggle (DataStore) + `strings.xml` i18n

3. [x] [AGENT] Refactor web example: CSS variables + theme toggle + `locales/` i18n scaffold

4. [x] [AGENT] Add `docs/DESIGN_GUIDE.md` + `.cursor/rules/design-system.mdc`

5. [x] [AGENT] Add `scripts/check-design-cohesion.sh` + validate-bootstrap wiring

6. [ ] [AUTO] `android-build` + web tests green (theme toggle smoke tests)

7. [ ] [HUMAN] Approve v0.6.0 release

### Parallel (safe after Sequential step 2)

| Task | Owner | Isolated scope | Done |

|------|-------|----------------|

| Web theme + i18n unit tests | AGENT | `examples/web/src/theme.test.ts`, `examples/web/src/i18n/**` |

| Android Compose theme components | AGENT | `examples/android/app/src/main/java/**/ui/**` |

---

## Milestone Gates

### Verified (v0.2.1)

- [ ] [AUTO] Regression tests: zero failures

- [ ] [AUTO] Static analysis and vulnerability scans clean

- [x] [AUTO] Workflow action refs validated (`scripts/validate-workflow-actions.sh`)

- [x] [AUTO] Pre-commit bare-semver guard (`scripts/check-workflow-action-ref-format.sh`)

- [x] [AUTO] Android assembleDebug CI smoke on `examples/android/`

- [x] [AUTO] Weekly health-check workflow polls CI + Security Scan + CodeQL

- [x] [AUTO] UTF-8 encoding check clean (`scripts/check-file-encoding.sh`)

- [x] [AUTO] Lockfiles present and CI uses locked installs (`npm ci`, `uv sync --locked`)

- [x] [AUTO] `TEMPLATE_INDEX.json` complete (`scripts/validate-template-index.sh`)

### Release sign-off (every version)

- [ ] [HUMAN] Weekly CVE triage completed within last 7 days

- [ ] [HUMAN] Zero open Critical/High Dependabot alerts (or documented exception)

- [ ] [HUMAN] State persistence survives simulated upgrade

- [ ] [HUMAN] CHANGELOG.md updated (Keep a Changelog format)

- [ ] [HUMAN] Version bumped and GitHub Release drafted

- [ ] [AUTO] SBOM attached to GitHub Release

- [ ] [HUMAN] `THIRD_PARTY_LICENSES.md` reviewed for distribution

### Planned gates (v0.2.2+)

- [x] [AUTO] Gitleaks CI job passes on `main` (M0)

- [ ] [AUTO] `scripts/pre-release-gate.sh` passes before release tag (M0)

- [x] [AUTO] Pre-commit includes file-limits and quick bootstrap validation (M0)

- [x] [AUTO] Android `assembleRelease` with `SOURCE_DATE_EPOCH` passes (M1)

- [x] [AUTO] Python coverage ≥ 90% in CI (M1)

- [x] [AUTO] Web bundle size budget within threshold (M1)

- [x] [AUTO] OpenSSF Scorecard run completed within last 30 days (M1)

- [x] [AUTO] Upgrade simulation test passes (M2)

- [x] [AUTO] GitHub Pages demo deploys successfully (M2)

- [x] [AUTO] Node example CI green when `examples/node/` present (M2)

- [ ] [HUMAN] Conventional Commits enforced on merged PRs (M1)

- [ ] [HUMAN] Stack picker run during init documents active modules in AGENT_MEMORY (M1)
