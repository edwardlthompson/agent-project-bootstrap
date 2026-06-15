# Build Plan

> Prioritized task board with owner labels. **Completed sprints:** `COMPLETED_TASKS.md`.

## Owner Label Legend

| Label | Owner | When to use |
|-------|-------|-------------|
| `AGENT` | Cursor Agent | Code, docs, scaffolding, tests, CI config |
| `HUMAN` | Human developer | Approvals, credentials, GitHub settings, product decisions |
| `ADB` | Human (Android) | Android SDK, emulator/device testing, F-Droid submission |
| `AUTO` | CI/scripts/bots | GitHub Actions, Dependabot, pre-commit, update checker |

**Task format:** `- [ ] [OWNER] Description`

```bash
grep '\[AGENT\]' BUILD_PLAN.md
grep '\[HUMAN\]' BUILD_PLAN.md
grep '\[ADB\]' BUILD_PLAN.md
grep '\[AUTO\]' BUILD_PLAN.md
```

**Agent rule:** Execute all `[AGENT]` **Sequential** items first, then dispatch **Parallel** agents with isolated file scopes (`docs/PARALLEL_AGENT_SCOPES.md`). Shared schema/types are Sequential-only.

> **Template maintainer:** work **Sprint M9** below. **Child repos:** copy the playbook after **Use this template**.

---

## Child Repo Playbook (copy after Use this template)

> Init scripts, feature docs (`docs/features/_template.md`), and About exemplar ship with the template. Mirror the Sequential + Parallel lane structure from Sprint M9 when customizing.

### Sprint 0 — Template Customization

#### Sequential

1. [ ] [HUMAN] Click **Use this template** on GitHub to create your project repo
2. [ ] [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
3. [ ] [AGENT] Run `scripts/init-project.sh` or `scripts/init-project.ps1`
4. [ ] [AGENT] Run `scripts/setup-github-repo.sh` (requires `gh` auth with admin)
5. [ ] [HUMAN] Select stack during init (web / python / android / node / multi)
6. [ ] [AUTO] Sprint 0 sign-off (all green on `main`):
   - `validate-bootstrap.sh --quick`
   - `feature-gate.sh --stack <active>`
   - `check-github-ci.sh --wait 300`
   - `check-license-compliance.sh` (after `npm ci` / `uv sync`)

### Sprint 1 — Golden Path Foundation

#### Sequential

1. [ ] [AGENT] Verify About screen scaffold for your active stack (`examples/{stack}/`)
2. [ ] [HUMAN] Fill `.app-update.json` `release_repo` and `donations.json` links
3. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack

### Sprint 2+ — Incremental Features

> One vertical slice at a time. See `docs/FEATURE_MODULES.md`. Draft: `docs/features/settings.md`. Second exemplar ships after template Sprint M9.

**Agent rule:** After every `[AGENT]` step → `bash scripts/watch-agent-gates.sh --once --autofix --step <scaffold|tests|wire>`.

#### Per-feature Sequential (duplicate each feature)

1. [ ] [AGENT] Copy `docs/features/_template.md` → `docs/features/{name}.md`; refine acceptance criteria
2. [ ] [AGENT] Scaffold feature container (public API boundary only)
3. [ ] [AGENT] Unit tests for feature pure logic
4. [ ] [AGENT] Wire view/adapter; composition root ≤10 lines
5. [ ] [HUMAN] Optional product smoke after `[AUTO]` gate pass

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

- [ ] [AUTO] `check-security-triage.sh --wait-ci 300` (Dependabot + CI; Scorecard after M9-11)
- [ ] [AGENT] Apply Dependabot bumps; triage Scorecard SARIF findings
- [ ] [AUTO] CI matrix + Repo Hygiene + Feature Gate green on `main`

### Monthly

- [ ] [AUTO] `simulate-template-upgrade.sh`
- [ ] [AUTO] `check-license-compliance.sh` + SBOM on latest release
- [ ] [AGENT] Review Dependabot auto-merge PRs (KB-007)

### Pre-release (every version)

- [ ] [AUTO] `pre-release-gate.sh` + `run-maintainer-gates.sh`
- [ ] [AUTO] Release Please PR merged; CHANGELOG + manifest bumped
- [ ] [HUMAN] Approve release tag when product-ready

---

## Template Maintainer — Sprint M9: Agent Gate Fidelity + Exemplar Completion

> **Source:** code review 2026-06-15. Restores agent protocol integrity, gate/CI parity, and credible feature exemplars. Sequential before Parallel.

### Critique

- **Null/empty:** Dependabot pagination must handle empty alert pages; `agent-progress` strikes must work when `--step` omitted.
- **Network timeouts:** `watch-agent-gates --wait-ci 300` may expire on slow CI — re-run or extend wait.
- **Race conditions:** Parallel agents must not edit shared types (`design-tokens`, `TEMPLATE_INDEX.json`) — Sequential only.
- **Unhandled exceptions:** Release workflow must fail closed if `pre-release-gate.sh` errors; branch protection context mismatch may block merges silently.

### Sequential (must complete in order)

1. [x] [HUMAN] Commit pending maintainer artifacts (`run-maintainer-gates`, `verify-fdroid-metadata`, `scorecard.yml` fix, `docs/features/`, metadata changelogs); CI green on `main`
2. [x] [AGENT] Fix 3-strike logic in `agent-progress.sh` + `watch-agent-gates.sh` (strikes without `--step`; no reset on autofix-only pass); add `scripts/verify-agent-strikes.sh`
3. [x] [AGENT] Restore lane discipline: `agent-progress.sh next --lane maintainer`; integrate `set-feature` + `--step` defaults in gate docs
4. [x] [AGENT] Align `feature-gate.sh` with CI: add `check-file-limits.sh`; python mypy/pyright stages; document CI-only web gates (Playwright, Lighthouse, bundle)
5. [x] [AGENT] Harden release path: paginate Dependabot in `pre-release-gate.sh` + `check-security-triage.sh`; enforce `pre-release-gate.sh` in `release.yml` workflow_dispatch
6. [x] [AGENT] Index `init-project`, undocumented scripts, and `ci.yml` / `security.yml` / `codeql.yml` in `TEMPLATE_INDEX.json`; reverse scan in `validate-template-index.sh`
7. [x] [AGENT] Complete About exemplar: wire Android update flow; unit tests for `UpdateChecker` / `AppUpdatePreferences`; expand web vitest coverage to `src/about/**`; refactor `main.ts` composition root ≤10 lines About wiring
8. [ ] [AGENT] Scaffold settings vertical slice per `docs/features/settings.md` (web + android containers, tests, i18n)
9. [ ] [AGENT] Extend `check-file-limits.sh` for `.kt` Compose + `components/*.ts` views; add node to `init-project.sh` stack picker
10. [ ] [AGENT] Reconcile Sprint 0 sign-off lists across BUILD_PLAN, `INITIALIZATION_PROMPT.md`, `read-before-write.mdc`
11. [ ] [AGENT] Extend `check-security-triage.sh` for Scorecard workflow; update `SECURITY.md`, `MAINTAINING_THE_TEMPLATE.md`, `START_HERE.md`, `FEATURE_MODULES.md` (Node column)
12. [ ] [AGENT] Resolve Module D ID collision (node vs lightroom); renumber/index template ADR; add `security-triage.mdc`
13. [ ] [HUMAN] Verify branch protection check names in GitHub UI; fix `setup-github-repo.sh` contexts if mismatched
14. [ ] [HUMAN] Merge Release Please PR #11 (`v0.8.0`) after rows 1–5 green
15. [ ] [HUMAN] Approve release tag after pre-release gates pass

### Parallel (safe after Sequential step 7)

| # | Task | Owner | Isolated scope |
|---|------|-------|----------------|
| A | Web About refactor + settings slice | AGENT | `examples/web/src/**`, `examples/web/e2e/**` |
| B | Android About wiring + settings slice | AGENT | `examples/android/app/**`, `examples/android/app/src/test/**` |
| C | Gate/CI hardening | AGENT | `scripts/feature-gate.sh`, `scripts/feature-autofix.sh`, `scripts/run-maintainer-gates.sh`, `.github/workflows/release.yml`, `.github/workflows/ci.yml` |
| D | Docs + rules + index | AGENT | `docs/**`, `.cursor/rules/**`, `TEMPLATE_INDEX.json`, `modules/**` |

Run `bash scripts/check-parallel-scope.sh` before dispatch. Do not edit `BUILD_PLAN.md` from Parallel agents.

### Distribution (ADB — after Sequential step 8)

- [ ] [AGENT] F-Droid image asset paths or placeholders under `metadata/en-US/images/`; document fdroiddata handoff in `modules/android/MODULE.md`
- [ ] [ADB] F-Droid dry-run on device/emulator (`modules/android/MODULE.md` checklist)
- [ ] [ADB] Verify reproducible APK hashes locally (`assembleRelease` ×2, `SOURCE_DATE_EPOCH` set)
- [ ] [HUMAN] Sign off anti-feature flags and store listing copy before F-Droid draft MR

---

## Archived Sprints

| Sprint | Status | Archive |
|--------|--------|---------|
| M5 README refresh | Complete | `COMPLETED_TASKS.md` |
| M6 Repo hygiene | Complete | `COMPLETED_TASKS.md` |
| M7 Feature assembly + agent gates | Complete | `COMPLETED_TASKS.md` |
| M8 Feature gate CI | Complete | `COMPLETED_TASKS.md` |
| Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
| Maintainer gate cycle 2026-06-15 | Complete | `COMPLETED_TASKS.md` |
| BUILD_PLAN cleanup 2026-06-15 | Complete | `COMPLETED_TASKS.md` |
