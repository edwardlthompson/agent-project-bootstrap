# Security Triage

Weekly CVE triage playbook for Dependabot alerts and release security gates.

## Setup (one-time, [HUMAN])

1. Open GitHub -> **Settings** -> **Code security and analysis**
2. Enable **Dependabot alerts** and **Dependabot security updates** (CVE advisories on dependencies)
3. Enable **Private vulnerability reporting** (Settings -> Code security -> Private vulnerability reporting)
4. Verify .github/dependabot.yml exists for each active package ecosystem

**Public repos:** Dependabot alerts are free.

dependabot.yml schedules version-update PRs; **Dependabot alerts** are a separate GitHub setting for CVE advisories — both are required.

## Weekly Triage Pass

Recommended cadence: **Monday** (aligned with scheduled security scans and `health-check.yml`).

| Step | Owner | Action |
|------|-------|--------|
| 1 | HUMAN | Open **Security -> Dependabot alerts**; sort Critical/High first |
| 2 | HUMAN | Review open Dependabot version-update PRs |
| 3 | AGENT | Apply dependency bumps, run tests locally, open PR |
| 4 | AUTO | CI (Trivy, CodeQL, matrix tests) validates merge |
| 5 | HUMAN | Merge PR or escalate deferred items |
| 6 | AUTO | Review `health-check.yml` weekly run (Monday 07:00 UTC); confirm CI + Security Scan + CodeQL green on main HEAD |

## Triage Decisions

| Decision | When | Action |
|----------|------|--------|
| **Fix** | Patch available, low risk | Merge Dependabot PR or [AGENT] applies bump |
| **Defer** | No fix yet, acceptable risk window | Open issue with expiry date; log in DECISION_LOG.md |
| **Dismiss** | False positive or not applicable | Document rationale in issue or ADR |

After triage, confirm Trivy and CodeQL workflows are green on main.

## GitHub Actions Pin Policy

Third-party workflow actions must use **immutable refs** to reduce supply-chain risk (see Trivy action advisory, March 2026).

| Rule | Detail |
|------|--------|
| **Allowed** | `@vX.Y.Z` (v-prefix semver) or full commit SHA with `# vX.Y.Z` comment |
| **Forbidden** | Bare semver (`@0.28.0`), floating `@v0` / `@main`, unpinned third-party actions |
| **Pre-push** | Run `scripts/validate-workflow-actions.sh` (requires `gh` + `GH_TOKEN`) |
| **Local fast guard** | `scripts/check-workflow-action-ref-format.sh` (pre-commit; no network) |
| **Post-push** | `scripts/check-github-ci.sh --wait 300` — required workflows: **CI**, **Security Scan**, **CodeQL** |

## Release Gate (mandatory before tag)

Before any version bump or GitHub Release:

- [ ] Weekly triage completed within last **7 days**
- [ ] Zero open **Critical** or **High** Dependabot alerts (or documented exception with [HUMAN] approval + linked issue/ADR)
- [ ] Deferred vulnerabilities have a linked issue and [HUMAN] sign-off in release notes
- [ ] All [AUTO] security scans green on main (Trivy, CodeQL)

If a Critical/High alert has no upstream fix, release may proceed only when:

1. A linked issue documents the advisory, impact, and mitigation
2. [HUMAN] explicitly approves in the release notes or DECISION_LOG.md

## Related Files

| File | Purpose |
|------|---------|
| .github/dependabot.yml | Weekly grouped version-update PRs |
| .github/workflows/security.yml | Trivy filesystem scan |
| .github/workflows/codeql.yml | CodeQL static analysis |
| .github/workflows/health-check.yml | Weekly CI + Security Scan + CodeQL status on main |
| scripts/validate-workflow-actions.sh | Resolve action refs via GitHub API |
| scripts/check-workflow-action-ref-format.sh | Local bare-semver guard |
| scripts/check-github-ci.sh | Post-push workflow gate |
| docs/MAINTAINING_THE_TEMPLATE.md | Maintainer release checklist |
| docs/INITIALIZATION_PROMPT.md | Section 7 pre-release gate |
