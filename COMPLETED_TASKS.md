# Completed Tasks

> Archive of finished BUILD_PLAN items.

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
- [ ] [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection (CI + Security Scan + CodeQL)
- [ ] [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with real GitHub username (template placeholder; run `init-project.sh` in child repos)

## Template Maintainer — v0.2.0 Backlog Fix (2026-06-12)

- [x] [AGENT] Normalize UTF-16 files to UTF-8; add `scripts/check-file-encoding.sh` + CI + pre-commit
- [x] [AGENT] Add `package-lock.json`, `uv.lock`, `.env.example`; expand `validate-bootstrap.sh`
- [x] [AGENT] Sync `TEMPLATE_INDEX.json` with LICENSE, scripts, workflows, rules
- [x] [AGENT] Sync README, SECURITY_TRIAGE, RUNBOOK, UPGRADING_FROM_TEMPLATE, PROMPT_LIBRARY, CHANGELOG
- [x] [AGENT] Harden license-compliance CI; web coverage budget; android ops checklist
- [x] [AGENT] Harden INITIALIZATION_PROMPT Sections 2/7/8 with Build Verification Gate
- [x] [AGENT] Update BUILD_PLAN Sprint 0 + Milestone Gates
- [x] [AGENT] Bump `.template-version` to 0.2.0; finalize CHANGELOG
- [ ] [HUMAN] GitHub settings: Dependabot alerts, private vulnerability reporting, branch protection, About
- [ ] [HUMAN] Replace `@[PROJECT_OWNER]` in CODEOWNERS with real GitHub username
