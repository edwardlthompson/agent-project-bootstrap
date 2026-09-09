# Build Plan

Live board. Finished work: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).

**Who:** `AGENT` code · `HUMAN` person · `ADB` device · `AUTO` CI/scripts  
**State:** 🔲 open · ✅ done · ❌ blocked — reason

Format: `🔲 [AGENT] Short task`. Sequential `[AGENT]` first. Parallel scopes: [`docs/PARALLEL_AGENT_SCOPES.md`](docs/PARALLEL_AGENT_SCOPES.md). `/build` tries HUMAN/ADB after automation; failures go to `HUMAN_BACKLOG.md`.

## Sprint smoke (hard stop)

After every `[AGENT]` row: `python3 scripts/agent-run.py watch-agent-gates --once --autofix --scope auto`

After the **last** `[AGENT]`/`[AUTO]` row in a sprint is ✅, do **not** start the next sprint until this exits 0:

```bash
python3 scripts/agent-run.py smoke-sprint --require
```

That command re-smokes **every** ✅ row: no errors or crashes, plus startup time and load order. Details: [`docs/SPRINT_SMOKE.md`](docs/SPRINT_SMOKE.md). Fail → leave the last row open or ❌; fix; re-run. `/gates` wrap-up includes the same check.

---

## Template Maintainer

**Now:** M50. Last ship **v1.1.0**. Child repos copy the playbook below.

### M50 — Chrome follow-through

<!-- parallel_exception: overlapping scripts, docs, web, and Android — Sequential order -->

1. 🔲 [AGENT] Chrome + chip regression gate in `check-design-cohesion`
2. 🔲 [AGENT] Compile Android instrumented tests in feature-gate (no emulator)
3. 🔲 [AGENT] Android Settings Data export/import (web Data parity)
4. 🔲 [AGENT] Child Sprint 1: lock Settings-only chrome (Settings → App info)
5. 🔲 [AGENT] Second locale catalog (web + Android)
6. 🔲 [AGENT] Home first-canvas empty state (no new chrome)
7. 🔲 [AGENT] Tokenize launch-prompt buttons (dark-mode contrast)

### M51 — CLI / API

<!-- parallel_exception: shared contract then per-stack ports -->

1. 🔲 [AGENT] Shared JSON About/donate/update (Node, Python, Rust, Go)
2. 🔲 [AGENT] Node GitHub feedback HTTP route
3. 🔲 [AGENT] Python `--feedback` CLI
4. 🔲 [AGENT] Rust/Go version from Cargo.toml / module
5. 🔲 [AGENT] Rust/Go JSON logs + readiness
6. 🔲 [AGENT] Node OpenAPI spec + contract tests
7. 🔲 [AGENT] Python OpenAPI + JSON logging
8. 🔲 [AGENT] Python mypy in pre-commit

### M52 — UI, a11y, nav proof

<!-- parallel_exception: shared Settings/a11y contract across web and Android -->

1. 🔲 [AGENT] Settings/About/Feedback visual snapshots
2. 🔲 [AGENT] Settings in-panel search
3. 🔲 [AGENT] Settings export schema migrations
4. 🔲 [AGENT] Android RTL/locale instrumented stress
5. 🔲 [AGENT] Android TalkBack + keyboard smoke
6. 🔲 [AGENT] Compose a11y lint gate
7. 🔲 [AGENT] Lighthouse a11y + best-practices floors
8. 🔲 [AGENT] Android nav-stack property tests

### M53 — Android distribution

<!-- parallel_exception: release path is one slice (R8 → recipe → metadata) -->

1. 🔲 [AGENT] Land android runtime-budget branch (PR #95)
2. 🔲 [AGENT] R8 analyzer in CI / feature-gate
3. 🔲 [AGENT] Reproducible APK in feature-gate
4. 🔲 [AGENT] F-Droid build recipe YAML
5. 🔲 [AGENT] Fastlane full metadata
6. 🔲 [AGENT] F-Droid AntiFeatures template
7. 🔲 [AGENT] UnifiedPush sample
8. 🔲 [AGENT] Android signing + rollback runbook

### M54 — Catalog + Lightroom

<!-- parallel_exception: catalog schema lock before optional-stack docs -->

1. 🔲 [AGENT] Lightroom Lua lint
2. 🔲 [AGENT] Second Lr* plugin entry
3. 🔲 [AGENT] Lightroom SDK bump playbook
4. 🔲 [AGENT] Sync web MODULE.md checklists
5. 🔲 [AGENT] Sync Android MODULE F-Droid rows
6. 🔲 [AGENT] Add `navigation` to `feature-catalog.json`
7. 🔲 [AGENT] Feature-catalog optional stacks (Lightroom)

### M55 — CI + security

<!-- parallel_exception: shared CI/security config -->

1. 🔲 [AGENT] Dependabot Cargo + Go
2. 🔲 [AGENT] Scorecard SARIF auto-classifier
3. 🔲 [AGENT] Semgrep prompt-injection pack
4. 🔲 [AGENT] Optional Nix flake CI
5. 🔲 [AGENT] Radar → BUILD_PLAN draft
6. 🔲 [AGENT] AUTOMERGE_TOKEN in setup-github-repo
7. 🔲 [AGENT] GlitchTip/Bugsink stub (not a live crash-proxy)
8. 🔲 [AGENT] Cross-stack sanitizer fixture CI job

### M56 — Desktop packaging

<!-- parallel_exception: Winget docs then binary loop -->

1. 🔲 [AGENT] Winget manifest example
2. 🔲 [AGENT] Winget multi-arch docs
3. 🔲 [AGENT] Desktop binary + Winget publish loop

### M57 — Cursor + docs

<!-- parallel_exception: registry/docs are one overlapping slice -->

1. 🔲 [AGENT] Land `docs/GROK_BOTS.md` on main
2. 🔲 [AGENT] Plugin marketplace runbook
3. 🔲 [AGENT] Skills for `/emulator` and `/adr`
4. 🔲 [AGENT] Refresh `CURSOR_FEATURE_REGISTRY.json`
5. 🔲 [AGENT] Commercial Automations YAML
6. 🔲 [AGENT] Commercial Cloud hook merge test
7. 🔲 [AGENT] Canvas / design-mode walkthrough
8. 🔲 [AGENT] Cursor CLI local-loop recipe
9. 🔲 [AGENT] `/tour` + COACH: Settings-only chrome
10. 🔲 [AGENT] `batch-commands-print.html` audit
11. 🔲 [AGENT] `check-template-gaps` optional-stack rows
12. 🔲 [AGENT] ADR-0001 architecture-pick gate
13. 🔲 [AGENT] Living `ci-gap` registry

### Waiting on a person

1. 🔲 [HUMAN] CII Best Practices checklist (login + public badge)
2. 🔲 [HUMAN] Optional: Ollama at `http://127.0.0.1:11434/v1` (`docs/LOCAL_MODELS.md`)
3. 🔲 [ADB] Optional: Android SDK licenses + first AVD (`/emulator`)
4. 🔲 [ADB] Golden Path nav smoke on device (Settings Back → home; second Back stays)

Done on this board: **M49** Settings-only chrome · **M47** Cline + nav. Archive: `COMPLETED_TASKS.md`.

---

## Child Repo Playbook (copy after Use this template)

Init, feature specs, and About + Settings exemplars ship with the template.

When Sprint 0 ends, stop living in `docs/INITIALIZATION_PROMPT.md`. Use `docs/features/_template.md` and this playbook. Reset `scratchpad.md` on sprint change; do not replace `AGENT_MEMORY.md`.

### Sprint 0 — Template Customization

#### Sequential

1. 🔲 [AGENT] Run `scripts/init-project.sh` or `.ps1` (`--stack`; scripted: `--non-interactive --project-name --purpose`)
1b. 🔲 [AGENT] Fill `branding/product.json` (`mode: product`); sync tokens + README
2. 🔲 [AGENT] Run `scripts/setup-github-repo.sh` (`gh` admin)
3. 🔲 [AUTO] Sprint 0 sign-off on `main`: `validate-bootstrap.sh --quick` · `feature-gate.sh --stack <active>` · `check-github-ci.sh --wait 300` (CI, Security Scan, CodeQL; CI must include Windows upgrade-sim, Repo Hygiene, Feature Gate) · `check-license-compliance.sh`

#### Parallel (safe after Sequential step 5)

<!-- parallel_exception: Sprint 0 — stack not selected; Parallel rows added after init -->

| Task | Owner | Isolated scope |
| ---- | ----- | -------------- |
| *None — see parallel_exception above* | — | — |

#### Human & device (after automation)

> `/build` tries these; failures → `HUMAN_BACKLOG.md`.

1. 🔲 [HUMAN] **Use this template** on GitHub
1a. 🔲 [HUMAN] Distribution tier (FOSS default vs Commercial) via `init-project.sh --distribution-tier`
2. 🔲 [HUMAN] Fill `docs/INITIALIZATION_PROMPT.md` (platform, purpose)
2a. 🔲 [HUMAN] Pick Cursor mode (`docs/CURSOR_MODES.md`)
2b. 🔲 [HUMAN] Bookmark `docs/help/BATCH_COMMANDS.md` (`/bootstrap` for Sprint 0)

### Sprint 1 — Golden Path Foundation

#### Sequential

1. 🔲 [AGENT] Lock Golden Path types/API: Settings-only chrome, About, navigation (no header Theme/About/donate)

#### Parallel (safe after Sequential step 1)

| Task | Owner | Isolated scope |
| ---- | ----- | -------------- |
| About screen verify | AGENT | `examples/{stack}/**/about/` |
| Stack public assets | AGENT | `examples/{stack}/public/` |
| Module + design docs | AGENT | `modules/{stack}/` |

#### Human & device (after automation)

1. 🔲 [HUMAN] Fill stack config (`app-update.json`, `donations.json`) or root copies; init runs `scripts/sync-stack-config.py`
2. 🔲 [HUMAN] Approve ADR-0001 and Sprint 1 for your stack

### Sprint 2+ — Incremental Features

One vertical slice at a time. [`docs/FEATURE_MODULES.md`](docs/FEATURE_MODULES.md). After each `[AGENT]` step: `watch-agent-gates --once --autofix --scope auto`. After the feature (or sprint) is all ✅: `smoke-sprint --require` before the next feature.

#### Per-feature Sequential (steps 1–2: lock API)

1. 🔲 [AGENT] Copy `docs/features/_template.md` → `docs/features/{name}.md`
2. 🔲 [AGENT] Scaffold feature container (public API only)

#### Per-feature Parallel (safe after Sequential step 2)

| Task | Owner | Isolated scope |
| ---- | ----- | -------------- |
| Logic + unit tests | AGENT | `examples/{stack}/src/{feature}/` or stack equivalent |
| View + i18n | AGENT | `examples/{stack}/src/components/` or `ui/{feature}/`, locales / `strings.xml` |
| Feature spec + acceptance | AGENT | `docs/features/{feature}.md` |
| E2e / instrumented smoke | AGENT | `examples/{stack}/e2e/` or `androidTest/` |

#### Per-feature Sequential (steps 3–4: after Parallel merge)

1. 🔲 [AGENT] Unit tests for pure logic (skip if Parallel already did)
2. 🔲 [AGENT] Wire view; composition root ≤10 lines

#### Human & device (after automation)

1. 🔲 [HUMAN] Optional product smoke after gates pass

---

## Ongoing Maintenance (recurring)

Template weekly: `bash scripts/run-maintainer-gates.sh` (omit `--quick` to wait on CI).

### Weekly

- 🔲 [AUTO] `cursor-feature-radar.sh` (non-blocking)
- 🔲 [AUTO] `check-security-triage.sh --wait-ci 300`
- 🔲 [AGENT] `/update-deps`; leftover Dependabot + Scorecard
- 🔲 [AUTO] CI + Repo Hygiene + Feature Gate green on `main`

### Monthly

- 🔲 [AUTO] `simulate-template-upgrade.sh`
- 🔲 [AUTO] `check-license-compliance.sh` + SBOM on latest release
- 🔲 [AGENT] Review Dependabot auto-merge PRs (KB-007)

### Pre-release (every version)

- 🔲 [AUTO] `pre-release-gate.sh --local` before push; full gate + `run-maintainer-gates.sh` after
- 🔲 [AUTO] Release Please merged; CHANGELOG + manifest bumped

### Human (after automation)

- 🔲 [HUMAN] Approve release tag when product-ready
- 🔲 [HUMAN] Quarterly Cursor feature radar (next 2026-11-15; last 2026-08-15)

---

## Archive

Older sprints and releases: [`COMPLETED_TASKS.md`](COMPLETED_TASKS.md).
