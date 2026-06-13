# Agent Memory

> Centralized index of tech stack, threat models, persistent context, and retrospectives.
> Update only at session startups, milestone boundaries, or major architectural pivots.

## Tech Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Platform | [INSERT PLATFORM / TECH STACK HERE] | - | Fill during Sprint 0 |
| License | MIT | - | Pure FOSS |
| Distribution | GitHub Releases | - | Platform channels TBD |

## Active Modules

- [ ] Android / F-Droid (`modules/android/MODULE.md`)
- [ ] Web / PWA (`modules/web/MODULE.md`)
- [ ] Python (`modules/python/MODULE.md`)
- [ ] Lightroom Classic (`modules/lightroom/MODULE.md`)

## Threat Model Checklist

- [ ] `docs/THREAT_MODEL.md` drafted (STRIDE, trust boundaries, top abuse cases)
- [ ] No proprietary closed-source SDKs in production path
- [ ] Opt-in only telemetry (GDPR/CCPA compliant); see `docs/PRIVACY.md`
- [ ] Secrets excluded from VCS (Gitleaks pre-commit)
- [ ] Dependency vulnerability scanning enabled (CodeQL + Trivy + Dependabot)
- [ ] Input validation at all data boundaries
- [ ] `SECURITY.md` and private vulnerability reporting enabled

## Persistent Context

### Project Purpose

[INSERT DETAILED APP DESCRIPTION AND GOALS HERE]

### Key Constraints

- Max 250 lines per view file, 150 lines per logic file
- Trunk-based development with Conventional Commits
- Strict type safety and test coverage budgets

## Session Retrospectives

| Date | Milestone | What worked | What to improve |
|------|-----------|-------------|-----------------|
| - | - | - | - |

## Template Provenance

- **Source template:** `edwardlthompson/agent-project-bootstrap`
- **Template version:** `0.3.0` (see `.template-version`)
- **Last update check:** See `.template-update.json`
