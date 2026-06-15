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

> Run these after **Use this template** to create a child project. See `docs/INITIALIZATION_PROMPT.md`.

### Sprint 0 — Template Customization

1. [ ] [HUMAN] Click **Use this template** on GitHub to create your project repo
2. [ ] [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
3. [ ] [HUMAN] Run `scripts/init-project.sh` or `scripts/init-project.ps1`
4. [ ] [HUMAN] Run `scripts/setup-github-repo.sh` (or `.ps1`) for Dependabot alerts, private vulnerability reporting, and branch protection
5. [ ] [HUMAN] Select stack during init (web / python / android / multi) to prune unused examples and modules
6. [ ] [HUMAN] Approve Sprint 0 only after CI green on `main` and Build Verification Gate passes

### Sprint 1 — Golden Path Foundation

1. [x] [AGENT] Scaffold in-app About screen with update checker (format-locked) and donation placeholders per active UI stack
2. [ ] [HUMAN] Fill `.app-update.json` `release_repo` and `donations.json` links
3. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack

### Sprint 2+ — Incremental Features (vertical slices, one at a time)

> Slow lego assembly. Sequential only. See `docs/FEATURE_MODULES.md`. Agents run automated gates without human polling.

**Agent rule:** After every `[AGENT]` step, run `bash scripts/watch-agent-gates.sh --once --autofix`. On failure, agent auto-fixes from JSON diagnostics and re-runs until pass or 3-strike. Do not start feature N+1 until `[HUMAN]` approves feature.

#### Feature template (duplicate per feature)

1. [ ] [HUMAN] Document acceptance criteria + one smoke scenario for **Feature: _[name]_**
2. [ ] [AGENT] Scaffold feature container; public API boundary only
3. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix` (post-scaffold; agent fixes until green)
4. [ ] [AGENT] Unit tests for feature pure logic
5. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix` (post-unit-tests)
6. [ ] [AGENT] Wire view/adapter; composition root ≤10 lines
7. [ ] [AUTO] `bash scripts/watch-agent-gates.sh --once --autofix --wait-ci 300` (after push to branch)
8. [ ] [HUMAN] Manual smoke happy path; approve before next feature row

#### Sprint 2 starter

1. [ ] [HUMAN] Name first feature and acceptance criteria
2. [ ] [AGENT] Implement first feature per `docs/FEATURE_MODULES.md` (About = reference shape)
3. [ ] [HUMAN] Sign off Sprint 2; duplicate feature template for Sprint 3

> **Note:** About screen (Sprint 1) is the reference exemplar. M7 row 5 uses add/remove of About as a gate verification exercise — not the first Sprint 2 feature. Duplicate the feature template for the first *new* feature.

---

## Ongoing Maintenance (template + child repos)

### Weekly (recurring)

- [ ] [HUMAN] Run weekly CVE triage pass per `docs/SECURITY_TRIAGE.md` (recommended: Monday)
- [ ] [AGENT] Apply Dependabot dependency bumps and open PRs as needed
- [ ] [AUTO] Trivy + CodeQL + CI matrix green after merges
- [ ] [AUTO] Repo Hygiene CI job green on `main`
- [ ] [AUTO] OpenSSF Scorecard workflow result reviewed
- [ ] [AUTO] `scripts/pre-release-gate.sh` run before any version bump
- [ ] [AUTO] `bash scripts/feature-gate.sh` on active stack before maintainer release tags
- [ ] [AGENT] Triage Scorecard findings into BUILD_PLAN `[AUTO]` items

### Monthly (recurring)

- [ ] [AUTO] Run `scripts/simulate-template-upgrade.sh` on schedule (first Monday)
- [ ] [HUMAN] Review `THIRD_PARTY_LICENSES.md` and SBOM for distribution
- [ ] [AGENT] Dependabot auto-merge PRs reviewed for override/transitive policy (KB-007)

---

## Template Maintainer — Sprint M5: README Visual Refresh

> AGENT work complete. Pending human visual review after push.

1. [ ] [HUMAN] Visual review on GitHub — badges load, `<dl>`/tables render as single blocks, all relative links resolve

---

## Template Maintainer — Sprint M6: Repo Hygiene Automation

> Industry-standard track-vs-ephemeral gates. Sequential before child-repo adoption.

1. [x] [AGENT] Add `.gitattributes`, `.editorconfig`, `.cursorignore`; expand `.gitignore`
2. [x] [AGENT] Add `check-tracked-artifacts`, `check-large-tracked-files`, `check-repo-hygiene`, `purge-ephemeral` scripts
3. [x] [AGENT] Wire repo-hygiene into pre-commit, `validate-bootstrap.sh`, and CI `repo-hygiene` job
4. [x] [AGENT] Add `docs/REPO_HYGIENE.md` and `.cursor/rules/repo-hygiene.mdc`
5. [ ] [HUMAN] Add **Repo Hygiene** to branch protection required checks on `main`
6. [x] [AUTO] CI **Repo Hygiene** job green after merge

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
5. [ ] [HUMAN] Verify About feature add/remove still passes `feature-gate.sh`
6. [ ] [AUTO] `feature-gate.sh` + CI green after merge

---

## Template Maintainer — Sprint M8: Feature Gate CI Enforcement

> CI becomes source of truth for feature-gate; local `--strict` for maintainer releases.

1. [ ] [AGENT] Add CI job or matrix step calling `bash scripts/feature-gate.sh --stack <active>` per present `examples/`
2. [ ] [AGENT] Add `--strict` to `feature-gate.sh` (exit 2 if any stack stage skipped in multi mode); use `--strict` in CI only
3. [ ] [AGENT] Wire `scripts/pre-release-gate.sh` to run `feature-gate.sh` before version bump
4. [ ] [HUMAN] Add feature-gate CI job to branch protection required checks on `main`
5. [ ] [AUTO] CI green including feature-gate job after merge

---

## Template Maintainer — Release Approvals

> Sequential gates before tagging. Automation handles CI and pre-release checks.

| Release | Status | Remaining |
|---------|--------|-----------|
| v0.2.2 | Ready | [ ] [HUMAN] Approve v0.2.2 release tag and GitHub Release |
| v0.3.0 | Ready | [ ] [HUMAN] Approve v0.3.0 release |
| v0.4.0 | Ready | [ ] [HUMAN] Approve v0.4.0 release |
| v0.5.0 | Ready | [ ] [HUMAN] Approve v0.5.0 release scope |
| v0.6.0 | Ready | [ ] [HUMAN] Approve v0.6.0 release |
| v0.7.0 | Open PR | [ ] [HUMAN] Review and merge Release Please PR #7 |
---

## Milestone Gates — Release Sign-off (every version)

- [ ] [HUMAN] Weekly CVE triage completed within last 7 days
- [ ] [HUMAN] Zero open Critical/High Dependabot alerts (or documented exception)
- [ ] [HUMAN] State persistence survives simulated upgrade
- [ ] [HUMAN] CHANGELOG.md updated (Keep a Changelog format)
- [ ] [HUMAN] Version bumped and GitHub Release drafted
- [ ] [AUTO] SBOM attached to GitHub Release
- [ ] [HUMAN] `THIRD_PARTY_LICENSES.md` reviewed for distribution
- [ ] [HUMAN] Conventional Commits enforced on merged PRs

---

## Template Maintainer — Device / Distribution (ADB)

- [ ] [ADB] Run F-Droid submission dry-run checklist (`modules/android/MODULE.md`) on physical device or emulator before first F-Droid release
- [ ] [ADB] Complete F-Droid `metadata/` blocks and verify reproducible APK hashes locally
