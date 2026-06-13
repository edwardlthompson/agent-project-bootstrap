# Maintaining the Template

Playbook for template maintainers optimizing agent-project-bootstrap over time.

## Semver Policy

- **MAJOR:** Breaking changes to init prompt structure or file layout
- **MINOR:** New modules, examples, CI gates, non-breaking features
- **PATCH:** Doc fixes, dependency bumps, typo corrections

## Release Checklist

1. All CI checks green on main
2. Bump `.template-version`
3. Update `CHANGELOG.md` (Keep a Changelog)
4. Update `TEMPLATE_INDEX.json` version and file entries
5. Run `scripts/validate-template-index.sh`
6. Tag `vX.Y.Z` and create GitHub Release with migration notes
7. Update repo About if description changed

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
