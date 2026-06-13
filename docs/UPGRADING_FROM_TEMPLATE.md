# Upgrading From Template

Child repos do not auto-sync with the upstream template. Use this guide when the update checker notifies you of a new release.

## Step 1: Read the Notification

Run `scripts/check-template-updates.sh` or check the devcontainer postStart output.

## Step 2: Review CHANGELOG

Read the upstream release notes at `github.com/edwardlthompson/agent-project-bootstrap/releases`.

## Step 3: Cherry-Pick by Area

| Changed area | Strategy | Owner |
|-------------|----------|-------|
| `.github/workflows/` | Cherry-pick or manual merge | AGENT + HUMAN review |
| `.cursor/rules/` | Copy new/changed `.mdc` files | AGENT |
| `docs/INITIALIZATION_PROMPT.md` | Manual review; do not blind overwrite | HUMAN |
| `scripts/` | Copy updated scripts | AGENT |
| `examples/` | Reference only unless adopting new stack | HUMAN decision |
| `TEMPLATE_INDEX.json` | Run validate script after merge | AGENT |

## Version Compatibility

| Upgrade | Notes |
|---------|-------|
| 0.1.x → 0.1.y | Safe PATCH; cherry-pick freely |
| 0.1.x → 0.2.0 | Check CHANGELOG for new files/schema changes |
| 0.x → 1.0.0 | Full review; init prompt structure may have changed |

## Decision Points

- `[HUMAN]` Approve which upstream changes to adopt
- `[AGENT]` Apply diffs to matching files
- `[AUTO]` CI validates after merge
