# Changelog

All notable changes to this template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- CI: Web TS null narrowing in main.ts, MIT license on web package, scoped Android FOSS grep to Gradle files
- Python: ruff format on greet.py
- Index/pre-commit: CONTRIBUTING.md in TEMPLATE_INDEX; encoding hook covers .ts/.tsx/.toml
- License script: --excludePrivatePackages for private stub packages
- Encoding: normalize UTF-16 index.html and style.css; extend encoding scan to .html/.css

## [0.2.0] - 2026-06-12

### Added

- `scripts/check-file-encoding.sh` — UTF-8 enforcement in CI and pre-commit
- `.env.example` — documented environment variable stub
- `examples/web/package-lock.json` and `examples/python/uv.lock` — reproducible locked installs
- Build Verification Gate in `INITIALIZATION_PROMPT.md` Section 7 (Sprint 0 + release)
- `PROMPT_LIBRARY.md` entries: bootstrap verification, security triage, SBOM audit, build verification
- Secret rotation procedure in `docs/RUNBOOK.md`
- Android operations checklist in `modules/android/MODULE.md`
- Release workflow `workflow_dispatch` for maintainer dry-run
- Web Vitest coverage budget (90%) matching Python example

### Changed

- Normalized ~46 UTF-16 corrupted files to UTF-8
- `scripts/validate-bootstrap.sh` — encoding, index, lockfile, and LICENSE checks
- `scripts/check-license-compliance.sh` — strict fail on disallowed licenses; stack-scoped CI steps
- `TEMPLATE_INDEX.json` — added LICENSE, scripts, dependency-review, destructive-ops, `.env.example`; version 0.2.0
- `.github/CODEOWNERS` — `@[PROJECT_OWNER]` placeholder; init scripts replace during Sprint 0
- `docs/SECURITY_TRIAGE.md` — private vulnerability reporting in setup
- `docs/UPGRADING_FROM_TEMPLATE.md` — cherry-pick rows for new scripts/workflows
- `BUILD_PLAN.md` — encoding, lockfiles, Build Verification Gate in Sprint 0 and Milestone Gates
- `README.md` — link `THIRD_PARTY_LICENSES.md` and `LICENSE`
- CI: license check after locked installs; `uv sync --locked`; encoding-check job first
- `docs/MAINTAINING_THE_TEMPLATE.md` — release dry-run step
- Init scripts — CODEOWNERS replacement, SECURITY/playbooks/`.env.example` reminders

### Human-only (not automated)

- Enable Dependabot alerts + private vulnerability reporting on GitHub
- Branch protection on `main` with required CI checks (`encoding-check`, `validate-bootstrap`)
- Replace `@[PROJECT_OWNER]` in CODEOWNERS with real GitHub username
- Paste GitHub About description

## [0.1.0] - 2026-06-12

### Added

- Verbatim Project Initialization Prompt (`docs/INITIALIZATION_PROMPT.md`)
- Agent routing: `docs/START_HERE.md`, `docs/FOR_AGENTS.md`, `TEMPLATE_INDEX.json`
- Workspace memory files: `AGENTS.md`, `AGENT_MEMORY.md`, `BUILD_PLAN.md`, and related docs
- Owner-labeled sprint structure (AGENT / HUMAN / ADB / AUTO) with Sequential and Parallel lanes
- Multi-stack Golden Path stubs: Web (Vite PWA), Python (uv CLI), Android (FOSS Gradle skeleton)
- Ecosystem module guides: Android, Web, Python, Lightroom
- CI/CD guardrails: matrix CI, CodeQL, Trivy, Dependabot, release workflow
- Template update checker with configurable intervals (`off`, `daily`, `weekly`, `monthly`, `on_session`)
- Maintainer and consumer docs: `MAINTAINING_THE_TEMPLATE.md`, `UPGRADING_FROM_TEMPLATE.md`
- Devcontainer, pre-commit hooks, init scripts (bash + PowerShell)
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS` — community health and responsible disclosure
- `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md` — threat model, privacy-by-design, operations
- `THIRD_PARTY_LICENSES.md` + `scripts/check-license-compliance.sh` — license compliance
- `scripts/validate-bootstrap.sh` — Sprint 0 artifact verification in CI
- `.github/workflows/dependency-review.yml` — PR dependency review (fail on High/Critical)
- Release workflow: SBOM (CycloneDX) + SLSA build provenance attestation
- `.cursor/rules/destructive-ops.mdc` — human-in-the-loop gates for destructive agent operations

[0.2.0]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.0
[0.1.0]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.1.0
