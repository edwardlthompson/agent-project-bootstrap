# Changelog





All notable changes to this template will be documented in this file.





The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),


and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).





## [0.8.0](https://github.com/edwardlthompson/agent-project-bootstrap/compare/v0.7.1...v0.8.0) (2026-06-15)


### Added

* add in-app About screen with format-locked update checker ([29278cc](https://github.com/edwardlthompson/agent-project-bootstrap/commit/29278ccad8f1e7ee623e3c761026bbc4711a83a3))
* add industry-standard repo hygiene automation ([136bfe3](https://github.com/edwardlthompson/agent-project-bootstrap/commit/136bfe336e3f868c9f32c12e531ea26517765cc2))
* **agents:** automate BUILD_PLAN human gates and Sprint M8 CI ([810e259](https://github.com/edwardlthompson/agent-project-bootstrap/commit/810e259ceb69994800372d2f66df09c918465738))
* **agents:** execute Sprint M9 sequential rows 1-7 ([e8e6831](https://github.com/edwardlthompson/agent-project-bootstrap/commit/e8e6831f3367f41fce5cb22f25c7d07347034e98))
* **agents:** execute Sprint M9-8 and M10 code review remediation ([9163dab](https://github.com/edwardlthompson/agent-project-bootstrap/commit/9163dab255d4a7552ea1d0d4f169f2b78f569593))
* **agents:** incremental feature assembly and autonomous agent gates ([3d47485](https://github.com/edwardlthompson/agent-project-bootstrap/commit/3d4748595589a642db0373947ae2152e5e3cd1de))


### Fixed

* **agents:** execute Sprint M11 post-M10 hardening ([daa9d85](https://github.com/edwardlthompson/agent-project-bootstrap/commit/daa9d858afe0eed78e95913107af704e652fb964))
* **agents:** execute Sprint M12 post-M11 polish ([0f859fd](https://github.com/edwardlthompson/agent-project-bootstrap/commit/0f859fd5211e06d06647760cccde452402254614))
* **android:** pin Kotlin compose plugin 2.3.20 for CodeQL ([7055255](https://github.com/edwardlthompson/agent-project-bootstrap/commit/70552559df7dd57d8f9ad7d2ee334ee4f6759c04))
* **ci:** repair M12 gate failures (TS tests, Kotlin pin) ([cb1c5d5](https://github.com/edwardlthompson/agent-project-bootstrap/commit/cb1c5d5a51793daa0377c9f82ea84affc7b9d222))
* **web:** assign narrowed HTMLDivElement for AppShell root ([f1dad83](https://github.com/edwardlthompson/agent-project-bootstrap/commit/f1dad832e03f2adda807a99fadc63e314d0d833c))
* **web:** narrow app root type for AppShell render ([53406b1](https://github.com/edwardlthompson/agent-project-bootstrap/commit/53406b1b84736d145ebf620a5852a6d6eb23c087))
* **web:** resolve CI lint and file-size budget failures ([1759a8f](https://github.com/edwardlthompson/agent-project-bootstrap/commit/1759a8f54b80f54564318e4174f56388d20047ef))


### Changed

* sync template version to 0.7.1 and fix CHANGELOG encoding ([e7ebf2d](https://github.com/edwardlthompson/agent-project-bootstrap/commit/e7ebf2dadc367ceec14f701bd927a20b7c4dcde0))


### Documentation

* **build-plan:** mark M12 CI sign-off complete on 7055255 ([3189747](https://github.com/edwardlthompson/agent-project-bootstrap/commit/31897474dec6b30b1ee7f95701f3cebecc9c249b))
* mark automated BUILD_PLAN gates complete after CI green ([f3013a0](https://github.com/edwardlthompson/agent-project-bootstrap/commit/f3013a06f9ff1c9e7f5d5a85e96f495065a0610a))
* mark Sprint M6 repo-hygiene CI gate complete ([7ed666b](https://github.com/edwardlthompson/agent-project-bootstrap/commit/7ed666ba8c4b482f948b22a8e29e87dad2cef2e1))
* refresh README with badges, TOC, and collapsible sections ([008140e](https://github.com/edwardlthompson/agent-project-bootstrap/commit/008140ed6eed951a788cfdb1832f5b035bb7a582))

## [Unreleased]

### Added

- Sprint M12: CodeQL Android init-before-build order; tag release gate `--wait`/`--jobs`; Robolectric DataStore isolation; `ReleaseTagFetcherTest`, `DonationsLoaderTest`, `MainActivitySmokeTest`; web `appBootstrap` vitest coverage; Android `pendingRestart` UI stub
- Sprint M11: Android compile fixes; CodeQL Java setup; `ReleaseTagFetcher` IO dispatcher; release workflow lightweight vs full gate split; Robolectric theme/update prefs tests; web `appBootstrap.ts` extraction; gate dedupe in `run-maintainer-gates.sh`
- Sprint M10: Settings vertical slice (web + Android); gate parity (`--strict`, Scorecard, security triage); node stack init fixes; About/update exemplar fidelity; opt-in update checks default off
- Sprint M9 execution: 3-strike fix, maintainer lane routing, gate/CI parity, About exemplar tests
- `scripts/count-critical-high-dependabot.sh`, `scripts/verify-agent-strikes.sh`
- Web `AppShell.ts` composition refactor; Android `UpdateStatusEvaluator` + unit tests
- `TEMPLATE_INDEX.json` reverse scan in `validate-template-index.sh`

### Fixed

- CodeQL `java-kotlin` matrix: initialize before Gradle traced build; pin Kotlin compose plugin 2.3.20 for CodeQL extractor compatibility
- Tag release lightweight gate polls CI with `--wait 300 --jobs "Repo Hygiene,Feature Gate"`; PowerShell `check-github-ci.ps1` `-Jobs` parity
- Sprint M11: `kotlinx.coroutines.launch` imports in `MainActivity` / `GoldenPathApp`; offline update-check gating; clickable donations; header nav toggle
- F-Droid metadata validator: `verify-fdroid-metadata.sh` (+ `.ps1`); changelog and images README under `examples/android/metadata/`
- Sprint 2 feature docs: `docs/features/_template.md`, proposed first slice `docs/features/settings.md`
- `TEMPLATE_INDEX.json` entries for verify-about, security-triage, readme-health, fdroid-metadata, maintainer-gates scripts

### Fixed

- OpenSSF Scorecard workflow: move `security-events` and `id-token` write permissions to job level (publish_results API requirement)

- Incremental feature assembly: `docs/FEATURE_MODULES.md`, vertical-slice Sprint 2+ BUILD_PLAN template
- Autonomous agent gates: `feature-gate.sh`, `feature-autofix.sh`, `agent-progress.sh`, `watch-agent-gates.sh`, `smoke-stack.sh` (+ PowerShell twins)
- Cursor rules: `feature-modules.mdc`; extended `testing.mdc`, `ci-gates.mdc`, `destructive-ops.mdc` for auto-fix protocol
- Session state + gitignored `.cursor/agent-progress.json` for extended agent sessions
- PROMPT_LIBRARY Entry 17 — autonomous feature step

- In-app About screen: init prompt guidance, Golden Path web/Android stubs, format-locked update checker, donation placeholders
- Repo hygiene automation: `.gitattributes`, `.editorconfig`, `.cursorignore`, hygiene scripts, CI `repo-hygiene` job, `docs/REPO_HYGIENE.md`

## [0.7.1](https://github.com/edwardlthompson/agent-project-bootstrap/compare/v0.7.0...v0.7.1) (2026-06-13)


### Fixed

* **android:** bump compileSdk to 37 for androidx 1.19 dependencies ([3a74f0c](https://github.com/edwardlthompson/agent-project-bootstrap/commit/3a74f0c08d32aff7a14d6fb7eff829578cbe73da))
* **android:** migrate Golden Path example to AGP 9 built-in Kotlin ([a84a16c](https://github.com/edwardlthompson/agent-project-bootstrap/commit/a84a16c8fa7e67d3179b820962aead03add7be34))
* **android:** rewrite Gradle Kotlin DSL files as UTF-8 ([11bc782](https://github.com/edwardlthompson/agent-project-bootstrap/commit/11bc78233b804ccaaca318f630f9eb1501cf10b8))
* **ci:** gofmt Go example and harden PR coverage comment parsing ([0423990](https://github.com/edwardlthompson/agent-project-bootstrap/commit/0423990b4ece9559a42db6c6bc66cec0eab518c8))
* **ci:** remove job-level hashFiles guards from ci.yml ([36fdbc1](https://github.com/edwardlthompson/agent-project-bootstrap/commit/36fdbc118f25e5865fb18aee653728ee87613f09))
* **ci:** repair corrupted template literals in coverage comment job ([a64ad04](https://github.com/edwardlthompson/agent-project-bootstrap/commit/a64ad04b1fd5ec301110925d8783ed8a1653a6ab))


### Changed

* **deps:** Bump the github-actions group across 1 directory with 12 updates ([c70ce00](https://github.com/edwardlthompson/agent-project-bootstrap/commit/c70ce00d5d2bd89525aa928ef279ffe66d82e720))
* **deps:** Bump the github-actions group across 1 directory with 12 updates ([c242785](https://github.com/edwardlthompson/agent-project-bootstrap/commit/c2427853e0aec0c0680b68beb0497cbed4da7e8c))
* **deps:** Bump the node-dependencies group in /examples/node with 2 updates ([42b87eb](https://github.com/edwardlthompson/agent-project-bootstrap/commit/42b87eb548942b4197fe67194698d1eaf49028e4))
* sync v0.7.0 and complete BUILD_PLAN automation pass ([369e17e](https://github.com/edwardlthompson/agent-project-bootstrap/commit/369e17ea198e671a4e0cec5943282e6f5e1f2786))

## [0.7.0](https://github.com/edwardlthompson/agent-project-bootstrap/compare/v0.6.0...v0.7.0) (2026-06-13)


### Added

* design system, web layout docs, and Golden Path UI refresh ([912ebbe](https://github.com/edwardlthompson/agent-project-bootstrap/commit/912ebbe2c57fb2d47223c49b3332f3037cc9c80f))
* initial agent-project-bootstrap template v0.1.0 ([d71c23c](https://github.com/edwardlthompson/agent-project-bootstrap/commit/d71c23c22dd97b96f3ef91435319d5df04bb28b6))
* template v0.2.0 with UTF-8 gates, lockfiles, and build verification ([2317440](https://github.com/edwardlthompson/agent-project-bootstrap/commit/2317440eeecec0ef961bb9cf54ea3830c183d8cf))


### Fixed

* add gradle.properties with android.useAndroidX for assembleDebug ([ea87f7d](https://github.com/edwardlthompson/agent-project-bootstrap/commit/ea87f7dfd40500a7550759fb4466418de5ed2aae))
* Android CI ΓÇö google maven for AGP and FOSS grep comment false positive ([b907c46](https://github.com/edwardlthompson/agent-project-bootstrap/commit/b907c46628f05275ecefb149bc230ea08ac47845))
* bind vite preview to 127.0.0.1 for Playwright CI and extend pre-commit encoding ([9a3f935](https://github.com/edwardlthompson/agent-project-bootstrap/commit/9a3f9357ab4ca2d2afcdf8250ce955a6f46e9c60))
* **ci:** repair workflow action SHAs, e2e selectors, and shell line endings ([38ce003](https://github.com/edwardlthompson/agent-project-bootstrap/commit/38ce003771c04cdc043ffc79bf8ee2296fac19aa))
* **ci:** use full git history for Gitleaks on Release Please PRs ([01d585b](https://github.com/edwardlthompson/agent-project-bootstrap/commit/01d585bcc1183633139cf46d4ca4932c3dbd8ee3))
* correct gh api calls in validate-workflow-actions.sh ([100df56](https://github.com/edwardlthompson/agent-project-bootstrap/commit/100df5649aee5724b22a70c84742453a106f1f1a))
* **deps:** override transitive tmp and uuid for @lhci/cli alerts ([222fb59](https://github.com/edwardlthompson/agent-project-bootstrap/commit/222fb59f5aa2d11b66c79496c23ad0980108b620))
* extend encoding scan to Android kts/kt/xml/properties ([8f52c55](https://github.com/edwardlthompson/agent-project-bootstrap/commit/8f52c550f52231520c76dd0a12326c0838db07e4))
* improve CI configs for python packaging and vitest ([36fbb39](https://github.com/edwardlthompson/agent-project-bootstrap/commit/36fbb394c5c1aa414c812334aa8628abfc47f178))
* normalize Android example UTF-16 files for Gradle CI ([39a78d3](https://github.com/edwardlthompson/agent-project-bootstrap/commit/39a78d36844739a9b5b77cb1f9876feb229accca))
* normalize UTF-16 index.html and extend encoding scan to html/css ([e16272e](https://github.com/edwardlthompson/agent-project-bootstrap/commit/e16272eded9901380c086dad4da6189e548209f4))
* playwright preview server host and timeout for CI e2e ([99188fa](https://github.com/edwardlthompson/agent-project-bootstrap/commit/99188faff52638196366aa8f967cfa832900e37e))
* repair Security Scan workflow and add GH CI automation ([80f9fc0](https://github.com/edwardlthompson/agent-project-bootstrap/commit/80f9fc03a5ada9ef795b39111d2de6b508a982c6))
* resolve CI failures in web lint, python format, and android grep ([444ad7b](https://github.com/edwardlthompson/agent-project-bootstrap/commit/444ad7b4c713257bb749371c7c9882b0e883bd19))
* stabilize Lighthouse CI with 3-run median ([f41c48d](https://github.com/edwardlthompson/agent-project-bootstrap/commit/f41c48daff6d8a148d86ba5cfabf800d015c806d))


### Changed

* **deps:** Bump the github-actions group across 1 directory with 10 updates ([#3](https://github.com/edwardlthompson/agent-project-bootstrap/issues/3)) ([648f5d2](https://github.com/edwardlthompson/agent-project-bootstrap/commit/648f5d202b1b2820e10b59c680b6980109290f77))
* release v0.2.1 full bootstrap hardening ([a2749a3](https://github.com/edwardlthompson/agent-project-bootstrap/commit/a2749a30cfac1b3bf3f2d450666592453ca3aca2))


### Documentation

* harden initialization prompt against CI failure patterns ([ec5ee91](https://github.com/edwardlthompson/agent-project-bootstrap/commit/ec5ee914332e7697e6168676c88eaca341cff643))
* mark v0.2.1 About and release human tasks complete ([33dc47f](https://github.com/edwardlthompson/agent-project-bootstrap/commit/33dc47fa934728a4b1b0247e14af95e95d031db0))

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


- `docs/OPTIONAL_STACKS.md` ΓÇö Rust/Go/Lightroom/Node opt-in outside default init stack picker


- CI `stack-filters` job; `lightroom`, `node`, `rust`, `go` jobs gated on directory existence and path changes


- F-Droid submission dry-run checklist in `modules/android/MODULE.md` (`[ADB]`)





### Changed





- `TEMPLATE_INDEX.json` ΓÇö `modules.lightroom.example` ΓåÆ `examples/lightroom/`; added `rust` and `go` modules


- `.template-version` ΓåÆ `0.5.0`


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

### Changed

- README (M5.1): hero badges, table of contents, GitHub alert callouts, collapsible detail sections, audience dividers
- README (M5): shields.io badges + HTML definition lists/tables for What's Included, BUILD_PLAN Labels, Template Update Checker, and Supported Stacks
- `scripts/normalize-markdown-whitespace.py`: table-aware blank-line collapse
- `scripts/check-markdown-tables.sh`: fail on broken GFM table rows; wired into `validate-bootstrap.sh`
- `docs/MAINTAINING_THE_TEMPLATE.md`: README badge conventions and hero/TOC sync notes

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





- `scripts/check-workflow-action-ref-format.sh` ΓÇö local pre-commit guard against bare-semver action refs


- `.github/workflows/health-check.yml` ΓÇö weekly Monday 07:00 UTC poll of CI + Security Scan + CodeQL on main


- CI `android-build` job ΓÇö `./gradlew assembleDebug` smoke for `examples/android/`


- Gradle wrapper binaries (`gradlew`, `gradlew.bat`, `gradle-wrapper.jar`) in `examples/android/`


- `KNOWLEDGE_BASE.md` ΓÇö six structured entries from v0.2.0 CI/security fix round


- `PROMPT_LIBRARY.md` entries 8ΓÇô9 ΓÇö workflow action validation and post-push GitHub gate


- Devcontainer `github-cli` feature; postStart runs encoding check + CI gate reminder


- README GitHub CI Gate section; init scripts run `validate-workflow-actions` and remind `check-github-ci`





### Changed





- Normalized root `.gitignore` from UTF-16 to UTF-8; added to encoding scan and pre-commit hook


- SHA-pinned `release.yml` actions: `anchore/sbom-action`, `softprops/action-gh-release`, `actions/attest-build-provenance`


- `docs/SECURITY_TRIAGE.md` ΓÇö GitHub Actions pin policy, health-check in weekly triage table


- `modules/web/MODULE.md` ΓÇö Lighthouse 3-run median policy documented


- `modules/android/MODULE.md` ΓÇö CI assembleDebug documented; fixed corrupted path characters


- `docs/INITIALIZATION_PROMPT.md` ΓÇö root `.gitignore` in encoding extension list


- `PROMPT_LIBRARY.md` entries 4 and 6 ΓÇö validate-workflow-actions, three-workflow sign-off





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





- `scripts/check-file-encoding.sh` ΓÇö UTF-8 enforcement in CI and pre-commit


- `.env.example` ΓÇö documented environment variable stub


- `examples/web/package-lock.json` and `examples/python/uv.lock` ΓÇö reproducible locked installs


- Build Verification Gate in `INITIALIZATION_PROMPT.md` Section 7 (Sprint 0 + release)


- `PROMPT_LIBRARY.md` entries: bootstrap verification, security triage, SBOM audit, build verification


- Secret rotation procedure in `docs/RUNBOOK.md`


- Android operations checklist in `modules/android/MODULE.md`


- Release workflow `workflow_dispatch` for maintainer dry-run


- Web Vitest coverage budget (90%) matching Python example





### Changed





- Normalized ~46 UTF-16 corrupted files to UTF-8


- `scripts/validate-bootstrap.sh` ΓÇö encoding, index, lockfile, and LICENSE checks


- `scripts/check-license-compliance.sh` ΓÇö strict fail on disallowed licenses; stack-scoped CI steps


- `TEMPLATE_INDEX.json` ΓÇö added LICENSE, scripts, dependency-review, destructive-ops, `.env.example`; version 0.2.0


- `.github/CODEOWNERS` ΓÇö `@[PROJECT_OWNER]` placeholder; init scripts replace during Sprint 0


- `docs/SECURITY_TRIAGE.md` ΓÇö private vulnerability reporting in setup


- `docs/UPGRADING_FROM_TEMPLATE.md` ΓÇö cherry-pick rows for new scripts/workflows


- `BUILD_PLAN.md` ΓÇö encoding, lockfiles, Build Verification Gate in Sprint 0 and Milestone Gates


- `README.md` ΓÇö links THREAT_MODEL, PRIVACY, RUNBOOK, THIRD_PARTY_LICENSES, LICENSE


- CI: license check after locked installs; `uv sync --locked`; encoding-check job first


- `docs/MAINTAINING_THE_TEMPLATE.md` ΓÇö release dry-run steps


- Init scripts ΓÇö CODEOWNERS replacement, GITHUB_ABOUT.md draft, update checker config





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


- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS` ΓÇö community health and responsible disclosure


- `docs/THREAT_MODEL.md`, `docs/PRIVACY.md`, `docs/RUNBOOK.md` ΓÇö threat model, privacy-by-design, operations


- `THIRD_PARTY_LICENSES.md` + `scripts/check-license-compliance.sh` ΓÇö license compliance


- `scripts/validate-bootstrap.sh` ΓÇö Sprint 0 artifact verification in CI


- `.github/workflows/dependency-review.yml` ΓÇö PR dependency review (fail on High/Critical)


- Release workflow: SBOM (CycloneDX) + SLSA build provenance attestation


- `.cursor/rules/destructive-ops.mdc` ΓÇö human-in-the-loop gates for destructive agent operations





[0.2.0]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.0


[0.2.1]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.2.1


[0.1.0]: https://github.com/edwardlthompson/agent-project-bootstrap/releases/tag/v0.1.0
