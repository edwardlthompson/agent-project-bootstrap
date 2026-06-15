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

> **Sprint M0–M8** are template-maintainer sprints (this repo). Child repos use Sprint 0–2+ with automated `feature-gate.sh` between steps.

---

## Child Repo — Sprint 0–2 (not applicable to template maintainer)

> **Template maintainer:** skip this section. Copy-paste for child projects after **Use this template**.

### Sprint 0 — Template Customization

1. [ ] [HUMAN] Click **Use this template** on GitHub to create your project repo
2. [ ] [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
3. [ ] [AGENT] Run `scripts/init-project.sh` or `scripts/init-project.ps1` (child repo bootstrap)
4. [ ] [AGENT] Run `scripts/setup-github-repo.sh` (Dependabot, branch protection — requires `gh` auth)
5. [ ] [HUMAN] Select stack during init (web / python / android / multi) to prune unused examples and modules
6. [ ] [AUTO] Sprint 0 sign-off when `validate-bootstrap.sh` + `check-github-ci.sh --wait 300` pass on `main`

### Sprint 1 — Golden Path Foundation

1. [x] [AGENT] Scaffold in-app About screen with update checker (format-locked) and donation placeholders per active UI stack
2. [ ] [HUMAN] Fill `.app-update.json` `release_repo` and `donations.json` links _(child repo only)_
3. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack _(child repo only)_

### Sprint 2+ — Incremental Features (vertical slices, one at a time)

> Slow lego assembly. Sequential only. See `docs/FEATURE_MODULES.md`. Agents run automated gates without human polling.

**Agent rule:** After every `[AGENT]` step, run `bash scripts/watch-agent-gates.sh --once --autofix`. On failure, agent auto-fixes from JSON diagnostics and re-runs until pass or 3-strike. Feature sign-off: `[AUTO]` gate pass + optional `[HUMAN]` product approval in child repos.

#### Feature template (duplicate per feature)

1. [ ] [AGENT] Scaffold acceptance criteria stub in `docs/features/{name}.md` _(or [HUMAN] refines criteria)_
2. [ ] [AGENT] Scaffold feature container; public API boundary only
3. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix` (post-scaffold; agent fixes until green)
4. [ ] [AGENT] Unit tests for feature pure logic
5. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix` (post-unit-tests)
6. [ ] [AGENT] Wire view/adapter; composition root ≤10 lines
7. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix --wait-ci 300` (after push to branch)
8. [ ] [AUTO] `feature-gate.sh` green; `[HUMAN]` optional product smoke in child repos

#### Sprint 2 starter

1. [ ] [AGENT] Propose first feature name + acceptance criteria draft in `docs/features/`
2. [ ] [AGENT] Implement first feature per `docs/FEATURE_MODULES.md` (About = reference shape)
3. [ ] [AUTO] Feature template duplicated for Sprint 3 when gates pass

> **Note:** About screen (Sprint 1) is the reference exemplar. M7 row 5 uses automated add/remove verification — not the first Sprint 2 feature.

---

## Ongoing Maintenance (template + child repos)

### Weekly (recurring)

- [ ] [AUTO] `bash scripts/check-security-triage.sh --wait-ci 300` (Dependabot Critical/High + CI green)
- [ ] [AGENT] Apply Dependabot dependency bumps and open PRs as needed
- [ ] [AUTO] Trivy + CodeQL + CI matrix green after merges
- [ ] [AUTO] Repo Hygiene CI job green on `main`
- [ ] [AUTO] OpenSSF Scorecard workflow result reviewed
- [ ] [AUTO] `scripts/pre-release-gate.sh` run before any version bump
- [ ] [AUTO] `bash scripts/feature-gate.sh` on active stack before maintainer release tags
- [ ] [AGENT] Triage Scorecard findings into BUILD_PLAN `[AUTO]` items

### Monthly (recurring)

- [ ] [AUTO] Run `scripts/simulate-template-upgrade.sh` on schedule (first Monday)
- [ ] [AUTO] `check-license-compliance.sh` + SBOM artifact present on latest release
- [ ] [AGENT] Dependabot auto-merge PRs reviewed for override/transitive policy (KB-007)

---

## Template Maintainer — Sprint M5: README Visual Refresh

> AGENT work complete. Automated health check replaces manual visual review.

1. [x] [AUTO] `bash scripts/check-readme-health.sh` (relative links, markdown tables, encoding)

---

## Template Maintainer — Sprint M6: Repo Hygiene Automation

> Industry-standard track-vs-ephemeral gates. Sequential before child-repo adoption.

1. [x] [AGENT] Add `.gitattributes`, `.editorconfig`, `.cursorignore`; expand `.gitignore`
2. [x] [AGENT] Add `check-tracked-artifacts`, `check-large-tracked-files`, `check-repo-hygiene`, `purge-ephemeral` scripts
3. [x] [AGENT] Wire repo-hygiene into pre-commit, `validate-bootstrap.sh`, and CI `repo-hygiene` job
4. [x] [AGENT] Add `docs/REPO_HYGIENE.md` and `.cursor/rules/repo-hygiene.mdc`
5. [ ] [AUTO] `bash scripts/setup-github-repo.sh` adds **Repo Hygiene** to branch protection _(requires `gh` admin)_
6. [x] [AUTO] CI **Repo Hygiene** job green after merge
7. [x] [AGENT] Archive Sprint M6 completions to `COMPLETED_TASKS.md`
8. [x] [AGENT] Index `check-repo-hygiene.ps1` and `purge-ephemeral.ps1` in `TEMPLATE_INDEX.json`

---

## Template Maintainer — Sprint M7: Incremental Feature Assembly + Agent Gates

> Vertical-slice / lego-container workflow with autonomous lint/smoke gates.

1. [x] [AGENT] Add `docs/FEATURE_MODULES.md` and `.cursor/rules/feature-modules.mdc`
2. [x] [AGENT] Add `feature-gate.sh`, `feature-autofix.sh`, `agent-progress.sh`, `watch-agent-gates.sh`, `smoke-stack.sh` (+ `.ps1`)
3. [x] [AGENT] Extend session-state example, `ci-gates.mdc`, `testing.mdc`, `destructive-ops.mdc`; gitignore `agent-progress.json`
4. [x] [AGENT] Update BUILD_PLAN Sprint 2+ template, INITIALIZATION_PROMPT, FOR_AGENTS, PROMPT_LIBRARY
7. [x] [AGENT] Harden agent handoff: populate `gates_passed`, `failed_stage`, `log_tail` in `agent-progress.sh`; forward `--step` from `feature-gate.sh`
8. [x] [AGENT] Fix `watch-agent-gates.sh` JSON capture (stdout-only); pass `--paths` to `feature-autofix.sh` for active feature scope
9. [x] [AGENT] Add `docs/FEATURE_MODULES.md` to `validate-bootstrap.sh` REQUIRED; cross-link in `docs/START_HERE.md`; add Feature gate section to `modules/node/MODULE.md`
10. [x] [AGENT] Commit M7+M7-closeout changes; archive completed AGENT rows to `COMPLETED_TASKS.md`
11. [ ] [AUTO] Push to `origin/main` when `feature-gate.sh` + `validate-bootstrap.sh --quick` pass locally
12. [x] [AGENT] Add Feature gate section to `modules/lightroom/MODULE.md` (plan: `modules/*`)
13. [x] [AGENT] Populate `build_plan_step` in `agent-progress.sh`; `feature-autofix.sh` exit 1 on fixer failure
14. [x] [AGENT] Index remaining gate/hygiene `.ps1` twins in `TEMPLATE_INDEX.json`
5. [x] [AUTO] `bash scripts/verify-about-feature-gate.sh` (About add/remove lego test)
6. [ ] [AUTO] `feature-gate.sh` + CI green after merge

---

## Template Maintainer — Sprint M8: Feature Gate CI Enforcement

> CI becomes source of truth for feature-gate; `--strict` in CI only.

1. [x] [AGENT] Add CI job **Feature Gate** calling `feature-gate.sh --stack multi --strict`
2. [x] [AGENT] Add `--strict` to `feature-gate.sh` (exit 2 if stack skipped in multi mode)
3. [x] [AGENT] Wire `scripts/pre-release-gate.sh` to run `feature-gate.sh`
4. [ ] [AUTO] `bash scripts/setup-github-repo.sh` adds **Feature Gate** to branch protection _(requires `gh` admin)_
5. [ ] [AUTO] CI green including feature-gate job after merge

---

## Template Maintainer — Release Approvals

> Superseded releases archived in `COMPLETED_TASKS.md`. Current target via Release Please.

| Release | Status | Remaining |
|---------|--------|-----------|
| v0.8.0+ | Release Please | [ ] [AUTO] `pre-release-gate.sh` + CI green before merge |
| Next tag | Pending | [ ] [HUMAN] Approve release tag only when product-ready _(irreducible)_ |

---

## Milestone Gates — Release Sign-off (every version)

- [ ] [AUTO] `check-security-triage.sh` — CVE triage within policy
- [ ] [AUTO] Zero open Critical/High Dependabot alerts (`pre-release-gate.sh`)
- [ ] [AUTO] `simulate-template-upgrade.sh` passes
- [ ] [AUTO] CHANGELOG.md updated via Release Please
- [ ] [AUTO] Version bumped via Release Please manifest
- [ ] [AUTO] SBOM attached to GitHub Release (release workflow)
- [ ] [AUTO] `check-license-compliance.sh` on release artifacts
- [ ] [AUTO] Conventional Commits enforced (`semantic-pull-request` CI check)

---

## Template Maintainer — Device / Distribution (ADB)

- [ ] [ADB] Run F-Droid submission dry-run checklist (`modules/android/MODULE.md`) on physical device or emulator before first F-Droid release
- [ ] [ADB] Complete F-Droid `metadata/` blocks and verify reproducible APK hashes locally
