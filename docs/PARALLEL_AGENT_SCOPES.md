# Parallel Agent Scopes

> Isolated file scopes for BUILD_PLAN Parallel lane. No two agents may touch the same path prefix.

## Rules

1. One branch per agent: `feature/agent-<task-slug>`
2. Run `scripts/check-parallel-scope.sh` before dispatch
3. Shared types/schemas: **Sequential agent only**
4. Never edit `BUILD_PLAN.md` from parallel agents (sequential owner)

## Sprint 1 (child repo) defaults

| Stack | Isolated scope |
|-------|----------------|
| web | `examples/web/**` |
| python | `examples/python/**` |
| android | `examples/android/**` |
| multi | One scope per stack row; no overlap |
| none | Match `AGENT_MEMORY.md` checked modules |

## Sprint M13 (template maintainer) — archived

> Completed 2026-06-15. Branch protection verify, init `--stack`, local APK hash wrapper.

| Agent | Scope |
|-------|-------|
| A — Branch protection | `scripts/verify-branch-protection.sh`, `.ps1`, `run-maintainer-gates.sh` |
| B — Init CLI | `scripts/init-project.sh`, `scripts/init-project.ps1` |
| C — APK reproducibility | `scripts/verify-reproducible-apk.sh`, `.ps1`, `modules/android/MODULE.md` |

## Sprint M14 (template maintainer) — archived

> Completed 2026-06-15. Version sync, init.ps1 fix, gate wiring, web/Android hardening. See `COMPLETED_TASKS.md`.

## Sprint M15 (template maintainer) — active

> P2 backlog post-0.9.0. Init optional-stack prune, CodeQL docs, Playwright About e2e, upgrade sim.

| Agent | Scope |
|-------|-------|
| A — Init + upgrade sim | `scripts/init-project.*`, `simulate-template-upgrade.sh` |
| B — Web e2e | `examples/web/e2e/app.spec.ts` |
| C — Android smoke | `MainActivitySmokeTest.kt`, `modules/android/MODULE.md` |
| D — CI/docs | `codeql.yml`, `modules/rust|go/MODULE.md`, `release.yml` |

## Sprint M12 (template maintainer) — archived

> Completed 2026-06-15. CodeQL init order + Kotlin 2.3.20 pin; tag gate `--jobs`; bootstrap coverage.

| Agent | Scope |
|-------|-------|
| A — CodeQL + release gate | `.github/workflows/codeql.yml`, `release.yml`, `scripts/check-github-ci.ps1` |
| B — Android tests + restart UI | `examples/android/app/src/test/**`, `src/androidTest/**`, `ui/GoldenPathApp.kt` |
| C — Web bootstrap | `examples/web/src/appBootstrap.ts`, `vitest.config.ts` |
| D — Docs + CHANGELOG | `docs/FEATURE_MODULES.md`, `CHANGELOG.md`, `.cursor/rules/feature-modules.mdc` |

## Sprint M11 (template maintainer) — archived

> Completed 2026-06-15. CI blocker fixes on `9163dab` follow-up.

## Sprint M10 (template maintainer) — archived

> Completed 2026-06-15. Reference scopes for future maintainer parallel work.

| Agent | Scope |
|-------|-------|
| A — Web settings | `examples/web/src/components/SettingsPanel.ts`, `examples/web/src/locales/**`, `examples/web/src/style.css`, `examples/web/e2e/**` |
| B — Android settings/About | `examples/android/app/src/main/java/dev/foss/goldenpath/ui/**`, `examples/android/app/src/main/res/**`, `examples/android/app/src/main/assets/**` |
| C — Init + gates | `scripts/init-project.sh`, `scripts/init-project.ps1`, `scripts/init-stack-sync.py`, `scripts/setup-github-repo.sh`, `scripts/check-security-triage.sh`, `scripts/pre-release-gate.sh`, `scripts/run-maintainer-gates.sh` |
| D — Docs | `docs/**`, `modules/**`, `SECURITY.md` |

**Sequential-only (no Parallel):** `BUILD_PLAN.md`, `examples/web/src/AppShell.ts`, `examples/web/src/main.ts`, `MainActivity.kt`, `.github/workflows/release.yml`

## Sprint M9 (template maintainer) — archived

> Completed 2026-06-15. Reference scopes for future maintainer parallel work.

| Agent | Scope |
|-------|-------|
| A — Web | `examples/web/src/**`, `examples/web/e2e/**` |
| B — Android | `examples/android/app/**` |
| C — Gates/CI | `scripts/feature-gate.sh`, `scripts/feature-autofix.sh`, `scripts/run-maintainer-gates.sh`, `scripts/pre-release-gate.sh`, `scripts/check-security-triage.sh`, `.github/workflows/release.yml`, `.github/workflows/ci.yml` |
| D — Docs | `docs/**`, `.cursor/rules/**`, `TEMPLATE_INDEX.json`, `modules/**` |

**Sequential-only (no Parallel):** `BUILD_PLAN.md`, `scripts/agent-progress.sh`, `scripts/watch-agent-gates.sh`, shared `design-tokens/`

## Sprint M1 (template maintainer) — archived

| Task | Scope |
|------|-------|
| Web bundle + snapshots | `examples/web/**`, `scripts/check-bundle-size.sh` |
| Python pyright | `examples/python/**` |
| Android metadata | `examples/android/fastlane/**`, `examples/android/README.md` |
| Cursor rules | `.cursor/rules/testing.mdc`, `.cursor/rules/ci-gates.mdc` |
| Scorecard | `.github/workflows/scorecard.yml` |
| Parallel checker | `scripts/check-parallel-scope.sh`, `docs/PARALLEL_AGENT_SCOPES.md` |

## Collision Response

If `check-parallel-scope.sh` fails, split the task or move one item back to Sequential lane.
