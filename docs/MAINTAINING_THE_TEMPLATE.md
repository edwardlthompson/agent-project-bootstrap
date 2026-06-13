# Maintaining the Template

Playbook for template maintainers optimizing agent-project-bootstrap over time.

## Semver Policy

- **MAJOR:** Breaking changes to init prompt structure or file layout
- **MINOR:** New modules, examples, CI gates, non-breaking features
- **PATCH:** Doc fixes, dependency bumps, typo corrections

## Release Checklist

1. All CI checks green on main
2. Run `scripts/pre-release-gate.sh` (or `.ps1`) — CI poll, Dependabot Critical/High count, version/tag match
3. Bump `.template-version`
4. Update `CHANGELOG.md` (Keep a Changelog)
5. Update `TEMPLATE_INDEX.json` version and file entries
6. Run `scripts/validate-template-index.sh`
7. Tag `vX.Y.Z` and create GitHub Release with migration notes
8. **Dry-run:** use **Actions → Release → Run workflow** (`workflow_dispatch`) to validate SBOM/provenance steps before tagging
9. Update repo About if description changed
10. Weekly CVE triage completed within last 7 days (`docs/SECURITY_TRIAGE.md`)
11. Zero open Critical/High Dependabot alerts (or documented exception with linked issue)
12. `THIRD_PARTY_LICENSES.md` reviewed; SBOM attached to release
13. Move completed Sprint M* items to `COMPLETED_TASKS.md`

## Safe Edit Zones

| Zone | Risk | Notes |
|------|------|-------|
| `docs/`, `modules/` | Low | Additive changes preferred |
| `.github/workflows/` | Medium | Document in CHANGELOG |
| `TEMPLATE_INDEX.json` schema | High | Requires migration notes |
| `INITIALIZATION_PROMPT.md` structure | High | MAJOR version bump |

## Feedback Loop

Encourage `template_improvement` issues. Triage labels:

- `agent-confusion` — agent could not self-route
- `token-waste` — unnecessary files read
- `ci-gap` — missing quality gate
- `module-request` — new ecosystem module

## Regression

Template CI must pass before every release. The template eats its own dogfood.

## Roadmap Index

`TEMPLATE_INDEX.json` includes a `roadmap` object listing planned paths per maintainer sprint (M0–M3). These paths are **not** validated until implemented; move each path into the `files` array (and `modules` when applicable) when the corresponding BUILD_PLAN sprint item ships.
