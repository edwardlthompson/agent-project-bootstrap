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

> **Sprint M0–M4** are template-maintainer sprints (this repo). Child repos created from the template use Sprint 0–2 only.

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

1. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1 for your stack

### Sprint 2 — First Real Feature

1. [ ] [HUMAN] Define first feature milestone and acceptance criteria
2. [ ] [HUMAN] Approve implementation plan
3. [ ] [HUMAN] Sign off for release

---

## Ongoing Maintenance (template + child repos)

### Weekly (recurring)

- [ ] [HUMAN] Run weekly CVE triage pass per `docs/SECURITY_TRIAGE.md` (recommended: Monday)
- [ ] [AGENT] Apply Dependabot dependency bumps and open PRs as needed
- [ ] [AUTO] Trivy + CodeQL + CI matrix green after merges
- [ ] [AUTO] OpenSSF Scorecard workflow result reviewed
- [ ] [AUTO] `scripts/pre-release-gate.sh` run before any version bump
- [ ] [AGENT] Triage Scorecard findings into BUILD_PLAN `[AUTO]` items

### Monthly (recurring)

- [ ] [AUTO] Run `scripts/simulate-template-upgrade.sh` on schedule (first Monday)
- [ ] [HUMAN] Review `THIRD_PARTY_LICENSES.md` and SBOM for distribution
- [ ] [AGENT] Dependabot auto-merge PRs reviewed for override/transitive policy (KB-007)

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
