# Release: commit, push, and update docs

Framework: AGENT/HUMAN/ADB/AUTO; semver via Release Please / `.template-version`.
**User invoked `/push` — explicit approval for `git push origin main`.**

## Step 1 — Pre-release validation

- **Child repo:** `validate-bootstrap.sh --quick`, `feature-gate.sh --stack <active>`, `check-license-compliance.sh` after locked installs
- **Template maintainer:** also `run-maintainer-gates.sh` and `pre-release-gate.sh` per @docs/MAINTAINING_THE_TEMPLATE.md
- Verify @README.md via `check-readme-health.sh`
- Update @CHANGELOG.md `[Unreleased]`

## Step 2 — Release notes

Create/update RELEASE_NOTES.md from CHANGELOG, BUILD_PLAN rows, recent commits (use @RELEASE_NOTES.md.example).

## Step 3 — Commit and push

- Stage **explicit paths only** (never `git add .`)
- Commit: `chore(release): prepare vX.Y.Z release` with key changes in body
- `git push origin main`
- `bash scripts/check-github-ci.sh --wait 600`
- Zero open Critical/High Dependabot alerts

## Step 4 — Release

- Prefer Release Please PR merge ([HUMAN] if branch protection blocks agent)
- Update @AGENT_MEMORY.md and @DECISION_LOG.md at milestone boundary

## Step 5 — Cleanup

Replace 🔲 with ✅ on completed BUILD_PLAN rows; archive sprint to @COMPLETED_TASKS.md if applicable.

Do not force-push, amend published tags, or disable hooks. Halt and escalate [HUMAN] on failure.

Start executing now.
