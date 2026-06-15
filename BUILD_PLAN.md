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

> **Template maintainer:** open items below. **Child repos:** copy the playbook after **Use this template**.

---

## Child Repo Playbook (copy after Use this template)

> Init scripts, feature docs (`docs/features/_template.md`), and About + Settings exemplars ship with the template. Mirror the Sequential + Parallel lane structure from Sprint M9 when customizing.

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

> One vertical slice at a time. See `docs/FEATURE_MODULES.md`. Reference exemplars: `docs/features/settings.md` (Sprint 2), About (Sprint 1).

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

- [ ] [AUTO] `check-security-triage.sh --wait-ci 300` (Dependabot + CI + Scorecard)
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

## Template Maintainer — Open Items

### Release (HUMAN)

1. [ ] [HUMAN] Verify branch protection check names in GitHub UI; fix `setup-github-repo.sh` contexts if mismatched
2. [ ] [HUMAN] Merge Release Please PR #11 (`v0.8.0`) after CI green on `main`
3. [ ] [HUMAN] Approve release tag after pre-release gates pass

### Distribution (ADB + HUMAN)

- [ ] [ADB] F-Droid dry-run on device/emulator (`modules/android/MODULE.md` checklist)
- [ ] [ADB] Verify reproducible APK hashes locally (`assembleRelease` ×2, `SOURCE_DATE_EPOCH` set)
- [ ] [HUMAN] Sign off anti-feature flags and store listing copy before F-Droid draft MR

### Maintainer gate (HUMAN)

- [ ] [HUMAN] `gh auth` with security-alerts scope for local Dependabot triage; re-run `run-maintainer-gates.sh` full (not `--quick`) before v0.8.0 tag

### CI sign-off (AUTO)

- [ ] [AUTO] CI green on `main` after Sprint M11 (Feature Gate + CodeQL + Android build)

---

## Archived Sprints

| Sprint | Status | Archive |
|--------|--------|---------|
| M5 README refresh | Complete | `COMPLETED_TASKS.md` |
| M6 Repo hygiene | Complete | `COMPLETED_TASKS.md` |
| M7 Feature assembly + agent gates | Complete | `COMPLETED_TASKS.md` |
| M8 Feature gate CI | Complete | `COMPLETED_TASKS.md` |
| M9 Agent gate fidelity + exemplars | Complete | `COMPLETED_TASKS.md` |
| M10 Code review remediation | Complete | `COMPLETED_TASKS.md` |
| M11 Post-M10 hardening (AGENT) | Complete | `COMPLETED_TASKS.md` |
| Sprint 2 starter scaffold | Complete | `COMPLETED_TASKS.md` |
| Maintainer gate cycle 2026-06-15 | Complete | `COMPLETED_TASKS.md` |
| BUILD_PLAN cleanup 2026-06-15 | Complete | `COMPLETED_TASKS.md` |
