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

---

## Sprint 0 — Template Customization

### Sequential (must complete in order)

1. [ ] [HUMAN] Click **Use this template** on GitHub to create your project repo
2. [ ] [HUMAN] Fill placeholders in `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
3. [ ] [HUMAN] Run `scripts/init-project.sh` or `scripts/init-project.ps1`
4. [ ] [HUMAN] Enable Dependabot alerts + security updates (see `docs/SECURITY_TRIAGE.md` § Setup)
5. [ ] [HUMAN] Enable private vulnerability reporting + branch protection on `main`
6. [ ] [AGENT] Create `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md`
7. [ ] [AGENT] Add `.github/CODEOWNERS` and `THIRD_PARTY_LICENSES.md`
8. [ ] [AGENT] Initialize workspace memory files from template seeds (`AGENT_MEMORY.md`, etc.)
9. [ ] [AGENT] Wire update checker config into devcontainer and README
10. [ ] [HUMAN] Set GitHub repo About description from `docs/GITHUB_ABOUT.md`
11. [ ] [AGENT] Commit lockfiles (`package-lock.json`, `uv.lock`) and `.env.example`
12. [ ] [AGENT] Ensure `TEMPLATE_INDEX.json` includes all scripts, workflows, and playbooks
13. [ ] [AUTO] `scripts/check-file-encoding.sh` passes
14. [ ] [AUTO] Full Build Verification Gate (INITIALIZATION_PROMPT Section 7) green
15. [ ] [AUTO] `scripts/validate-bootstrap.sh` (expanded) passes in CI
16. [ ] [HUMAN] Approve Sprint 0 only after CI green on `main` and Build Verification Gate passes

### Parallel (safe after Sequential step 8)

| Task | Owner | Isolated scope |
|------|-------|----------------|
| Prune unused `examples/` folders | AGENT | `examples/**` |
| Prune unused `modules/` folders | AGENT | `modules/**` |
| Configure `.template-update.json` interval | HUMAN | `.template-update.json` |
| Verify pre-commit hooks install | AUTO | `.pre-commit-config.yaml` |

---

## Sprint 1 — Golden Path Foundation

### Sequential (must complete in order)

1. [ ] [AGENT] Propose directory structure for target stack
2. [ ] [AGENT] Draft ADR-0001 core architecture (`docs/adr/0001-core-architecture.md`)
3. [ ] [HUMAN] Approve ADR-0001 and BUILD_PLAN Sprint 1
4. [ ] [AGENT] Implement Golden Path reference feature (shared schema/types first)
5. [ ] [AUTO] CI matrix green on main

### Parallel (safe after Sequential step 4)

> Guardrail: no two parallel tasks may modify overlapping files.

| Task | Owner | Isolated scope |
|------|-------|----------------|
| Web PWA offline cache + tests | AGENT | `examples/web/**` |
| Python CLI + type/lint suite | AGENT | `examples/python/**` |
| Android FOSS Gradle skeleton | AGENT | `examples/android/**` |
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

| Task | Owner | Isolated scope |
|------|-------|----------------|
| _Define per feature_ | AGENT | _Isolated per agent scope_ |

---

## Ongoing Maintenance

### Weekly (recurring)

- [ ] [HUMAN] Run weekly CVE triage pass per `docs/SECURITY_TRIAGE.md` (recommended: Monday)
- [ ] [AGENT] Apply Dependabot dependency bumps and open PRs as needed
- [ ] [AUTO] Trivy + CodeQL + CI matrix green after merges

---

## Milestone Gates

- [ ] [AUTO] Regression tests: zero failures
- [ ] [AUTO] Static analysis and vulnerability scans clean
- [x] [AUTO] Workflow action refs validated (scripts/validate-workflow-actions.sh)
- [x] [AUTO] Pre-commit bare-semver guard (scripts/check-workflow-action-ref-format.sh)
- [x] [AUTO] Android assembleDebug CI smoke on xamples/android/
- [x] [AUTO] Weekly health-check workflow polls CI + Security Scan + CodeQL
- [ ] [AUTO] UTF-8 encoding check clean (`scripts/check-file-encoding.sh`)
- [ ] [AUTO] Lockfiles present and CI uses locked installs (`npm ci`, `uv sync --locked`)
- [ ] [AUTO] `TEMPLATE_INDEX.json` complete (`scripts/validate-template-index.sh`)
- [ ] [HUMAN] Weekly CVE triage completed within last 7 days
- [ ] [HUMAN] Zero open Critical/High Dependabot alerts (or documented exception)
- [ ] [HUMAN] State persistence survives simulated upgrade
- [ ] [HUMAN] CHANGELOG.md updated (Keep a Changelog format)
- [ ] [HUMAN] Version bumped and GitHub Release drafted
- [ ] [AUTO] SBOM attached to GitHub Release
- [ ] [HUMAN] `THIRD_PARTY_LICENSES.md` reviewed for distribution
