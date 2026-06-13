# Changelog





All notable changes to this template will be documented in this file.





The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),


and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).





## [0.6.0] - 2026-06-12

### Added

- Cross-stack design system: `design-tokens/design-tokens.json` + `scripts/sync-design-tokens.py`
- Android Jetpack Compose Material 3 Golden Path with system/light/dark theme toggle (DataStore)
- Web CSS design tokens, theme toggle (`theme.ts`), and i18n scaffold (`locales/`, `t()`)
- `docs/DESIGN_GUIDE.md` and `.cursor/rules/design-system.mdc`
- `scripts/check-design-cohesion.sh` / `.ps1` wired into `validate-bootstrap.sh`
- Sprint M4 in BUILD_PLAN.md (template maintainer v0.6.0)

### Changed

- `examples/android/` migrated from XML Views to Compose M3
- `examples/web/` uses CSS variables, logical properties, `prefers-reduced-motion`
- `modules/android/MODULE.md` and `modules/web/MODULE.md` design system sections
- `docs/START_HERE.md`, `docs/FOR_AGENTS.md` read order includes DESIGN_GUIDE
- `.template-version` bumped to `0.6.0`

## [0.5.0] - 2026-06-13





### Added





- `examples/lightroom/` stub (`Info.lua`, README with SDK version table) per `modules/lightroom/MODULE.md`


- Optional `modules/rust/MODULE.md` + `examples/rust/` hello stub (Cargo.toml, clippy/fmt/test CI)


- Optional `modules/go/MODULE.md` + `examples/go/` hello stub (vet/fmt/test CI)


- `docs/OPTIONAL_STACKS.md` — Rust/Go/Lightroom/Node opt-in outside default init stack picker


- CI `stack-filters` job; `lightroom`, `node`, `rust`, `go` jobs gated on directory existence and path changes


- F-Droid submission dry-run checklist in `modules/android/MODULE.md` (`[ADB]`)





### Changed





- `TEMPLATE_INDEX.json` — `modules.lightroom.example` → `examples/lightroom/`; added `rust` and `go` modules


- `.template-version` → `0.5.0`


- README Supported Stacks table includes Lightroom example path and optional stacks note





## [0.2.2] - 2026-06-13





### Added





- `scripts/setup-github-repo.sh` and `scripts/setup-github-repo.ps1` - idempotent gh api setup for Dependabot alerts, private vulnerability reporting, branch protection


- `scripts/pre-release-gate.sh` and `scripts/pre-release-gate.ps1` - CI poll, Dependabot Critical/High count, template version check, release workflow reminder


- `scripts/check-file-encoding.py` - cross-platform UTF-8/UTF-16 BOM check; `check-file-encoding.sh` delegates to Python


- `.cursor/rules/windows-encoding.mdc` - Python UTF-8 write guidance for Windows


- Gitleaks CI job in `.github/workflows/security.yml` (SHA-pinned `gitleaks/gitleaks-action@v3.0.0`)


- Pre-commit hooks: `file-limits`, `validate-bootstrap --quick`


- KNOWLEDGE_BASE KB-007 npm/pip overrides policy; DECISION_LOG entry for `@lhci/cli` overrides


- PROMPT_LIBRARY entries 10 (pre-release gate) and 11 (GitHub repo setup)





### Changed





- `scripts/validate-bootstrap.sh` - `--quick` flag skips `validate-workflow-actions`


- `.github/workflows/health-check.yml` - `npm audit` for `examples/web`, `uv pip audit` for `examples/python`


- `docs/SECURITY_TRIAGE.md` - documents `setup-github-repo.sh` in Setup section


- `init-project` scripts remind to run `setup-github-repo` after init


- `AGENT_MEMORY.md` template version synced to `0.2.2`; em-dash corruption fixed to ASCII hyphen


- README CI gate section mentions `setup-github-repo` and `pre-release-gate`





## [Unreleased]





## [0.3.0] - 2026-06-13





### Added





- Stack picker `web/python/android/multi/none` in `init-project` scripts; `none` keeps all examples


- `scripts/init-stack-sync.py` - sync `AGENT_MEMORY.md` checkboxes and `.cursor/stack-selection.json`


- `.cursor-session-state.example.json` - session restore schema


- `docs/adr/0001-core-architecture.md` - MVVM / Clean / Hexagonal choice template for child repos


- `android-release` CI job with `SOURCE_DATE_EPOCH=1700000000` and APK hash flake check


- Semantic PR title job (`amannn/action-semantic-pull-request`, SHA-pinned)


- `scripts/check-bundle-size.sh` - Vite dist JS gzip budget (200 KB)


- Playwright visual snapshot and service-worker offline e2e tests


- Optional `pyright` CI job for Python example


- `.cursor/rules/testing.mdc` and `.cursor/rules/ci-gates.mdc`


- `docs/PARALLEL_AGENT_SCOPES.md` and `scripts/check-parallel-scope.sh`


- PROMPT_LIBRARY entries 12-14


- `.github/workflows/scorecard.yml` - weekly OpenSSF Scorecard (SHA-pinned)


- Android Fastlane `short_description.txt` stub and emulator checklist in README





### Changed





- `docs/FOR_AGENTS.md` - failure playbook (CI poll, GH_TOKEN, Dependabot, 3-strike, parallel scope)


- Python CI enforces `pytest --cov-fail-under=90` explicitly


- `.template-version` bumped to `0.3.0`; TEMPLATE_INDEX and README updated





## [0.2.1] - 2026-06-13





### Added





- `scripts/check-workflow-action-ref-format.sh` — local pre-commit guard against bare-semver action refs


- `.github/workflows/health-check.yml` — weekly Monday 07:00 UTC poll of CI + Security Scan + CodeQL on main


- CI `android-build` job — `./gradlew assembleDebug` smoke for `examples/android/`


- Gradle wrapper binaries (`gradlew`, `gradlew.bat`, `gradle-wrapper.jar`) in `examples/android/`


- `KNOWLEDGE_BASE.md` — six structured entries from v0.2.0 CI/security fix round


- `PROMPT_LIBRARY.md` entries 8–9 — workflow action validation and post-push GitHub gate


- Devcontainer `github-cli` feature; postStart runs encoding check + CI gate reminder


- README GitHub CI Gate section; init scripts run `validate-workflow-actions` and remind `check-github-ci`





### Changed





- Normalized root `.gitignore` from UTF-16 to UTF-8; added to encoding scan and pre-commit hook


- SHA-pinned `release.yml` actions: `anchore/sbom-action`, `softprops/action-gh-release`, `actions/attest-build-provenance`


- `docs/SECURITY_TRIAGE.md` — GitHub Actions pin policy, health-check in weekly triage table


- `modules/web/MODULE.md` — Lighthouse 3-run median policy documented


- `modules/android/MODULE.md` — CI assembleDebug documented; fixed corrupted path characters


- `docs/INITIALIZATION_PROMPT.md` — root `.gitignore` in encoding extension list


- `PROMPT_LIBRARY.md` entries 4 and 6 — validate-workflow-actions, three-workflow sign-off





### Fixed





- CI: Lighthouse CI uses 3 runs with median assertion to reduce shared-runner flake while keeping 0.9 performance budget


- Security Scan: pin `aquasecurity/trivy-action` to SHA `a9c7b0f` (v0.36.0); invalid `@0.28.0` ref caused workflow setup failure


- Automation: `scripts/validate-workflow-actions.sh` and `scripts/check-github-ci.sh` (+ `.ps1`) to catch bad action refs and poll required GH workflows before sign-off


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


- `README.md` — links THREAT_MODEL, PRIVACY, RUNBOOK, THIRD_PARTY_LICENSES, LICENSE


- CI: license check after locked installs; `uv sync --locked`; encoding-check job first


- `docs/MAINTAINING_THE_TEMPLATE.md` — release dry-run steps


- Init scripts — CODEOWNERS replacement, GITHUB_ABOUT.md draft, update checker config





### Human-only (not automated)





- Enable Dependabot alerts + private vulnerability reporting on GitHub


- Branch protection on `main` with required CI checks (`encoding-check`, `validate-bootstrap`)


- Replace `@[PROJECT_OWNER]` in CODEOWNERS with real GitHub username


- Paste GitHub About description from `docs/GITHUB_ABOUT.md`





## [0.1.0] - 2026-06-12





### Added





- Verbatim Project Initialization Prompt (`docs/INITIALIZATION_PROMPT.md`)


- Agent routing: `docs/START_HERE.md`, `docs/FOR_AGENTS.md`, `TEMPLATE_INDEX.json`


- Workspace memory files: `AGENT_MEMORY.md`, `DECISION_LOG.md`, `KNOWLEDGE_BASE.md`, `BUILD_PLAN.md`


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


[0.2.1]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.1


[0.1.0]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.1.0


