# Agent Memory

> Centralized index of tech stack, threat models, persistent context, and retrospectives.
> Update only at session startups, milestone boundaries, or major architectural pivots.

## Tech Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Platform | Multi-stack template (Web, Python, Android, Node, optional Lightroom/Rust/Go) | 0.14.0 | Template maintainer repo |
| License | MIT | - | Pure FOSS |
| Distribution | GitHub Releases + GitHub Pages demo | - | F-Droid/Winget stubs for child repos |

## Active Modules

- ✅ Web / PWA (`modules/web/MODULE.md`)
- ✅ Python (`modules/python/MODULE.md`)
- ✅ Android / F-Droid (`modules/android/MODULE.md`)
- ✅ Node API (`modules/node/MODULE.md`)
- ✅ Lightroom Classic (`modules/lightroom/MODULE.md`)
- ✅ Rust (`modules/rust/MODULE.md`)
- ✅ Go (`modules/go/MODULE.md`)

## Threat Model Checklist

- ✅ `docs/THREAT_MODEL.md` drafted (STRIDE, trust boundaries, top abuse cases)
- ✅ No proprietary closed-source SDKs in production path
- ✅ Opt-in only telemetry (GDPR/CCPA compliant); see `docs/PRIVACY.md`
- ✅ Secrets excluded from VCS (Gitleaks pre-commit)
- ✅ Dependency vulnerability scanning enabled (CodeQL + Trivy + Dependabot)
- ✅ Input validation at all data boundaries
- ✅ `SECURITY.md` and private vulnerability reporting enabled

## Persistent Context

### Project Purpose

FOSS Cursor agent bootstrap template: labeled BUILD_PLAN sprints, Golden Path examples, CI guardrails, workspace memory, and design-system cohesion across Web and Android.

### Key Constraints

- Max 300 lines per static data file (UI + i18n), 150 lines per pure logic file
- Trunk-based development with Conventional Commits
- Strict type safety and test coverage budgets

## Session Retrospectives

| Date | Milestone | What worked | What to improve |
|------|-----------|-------------|-----------------|
| 2026-07-12 | M32 audit | Caught GITHUB_TOKEN automerge skipping push CI; Git Bash preference for Windows agent-run | Enable required status checks + AUTOMERGE_TOKEN (HUMAN) |
| 2026-06-13 | v0.6.0 design system | Cross-stack tokens + i18n scaffold | Restore optional-stack CI jobs after large merge |
| 2026-06-30 | Autonomous /build + HUMAN automation | Grouped human section keeps board readable; automation router backlogs failures only | Release Please PR #20 for 0.12.0 needs human merge |

## Template Provenance

- **Source template:** `edwardlthompson/agent-project-bootstrap` (self-maintained)
- **Template version:** `0.14.0` (see `.template-version`)
- **Last update check:** See `.template-update.json`
