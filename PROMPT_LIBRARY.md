# Prompt Library

> Living catalog of highly effective prompt strategies for this repository.

## Entry 1 — Project Initialization (Primary)

**File:** `docs/INITIALIZATION_PROMPT.md`

**Prompt:**

```
Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md.
Follow Section 8 Startup Sequence.
Use BUILD_PLAN.md Sequential lane first; respect AGENT/HUMAN/ADB/AUTO labels.
```

## Entry 2 — Reference Mode (Existing Project)

**Prompt:**

```
Read @docs/FOR_AGENTS.md and @TEMPLATE_INDEX.json from github.com/edwardlthompson/agent-project-bootstrap.
Apply matching modules and rules to this repo. Do not scaffold examples/ unless missing.
```

## Entry 3 — Pre-Release Audit

**Prompt:**

```
Activate Debugging/Audit persona per INITIALIZATION_PROMPT.md Section 7.
Verify all quality gates pass. Only then update CHANGELOG.md and create a GitHub Release.
```

## Entry 4 — Build Verification Gate

**Prompt:**

```
Run the Build Verification Gate from INITIALIZATION_PROMPT.md Section 7.
Execute: check-file-encoding, validate-template-index, validate-bootstrap,
validate-workflow-actions, check-license-compliance, pre-commit run --all-files.
After pushing to main, run scripts/check-github-ci.sh --wait 300
(or scripts/check-github-ci.ps1 -WaitSeconds 300 on Windows).
Report pass/fail per script. Do not mark BUILD_PLAN items complete until all pass.
```

## Entry 5 — Bootstrap Verification

**Prompt:**

```
Run scripts/validate-bootstrap.sh and scripts/validate-template-index.sh.
Confirm .env.example, LICENSE, lockfiles, and TEMPLATE_INDEX.json completeness.
Fix any failures before Sprint 0 sign-off.
```

## Entry 6 — Security Triage

**Prompt:**

```
Follow docs/SECURITY_TRIAGE.md weekly triage pass.
Review Dependabot alerts (Critical/High first), triage open PRs.
Confirm all three required workflows are green on main: CI, Security Scan, CodeQL.
Run scripts/check-github-ci.sh after any workflow or dependency change.
```

## Entry 7 — Pre-Release SBOM Audit

**Prompt:**

```
Before tagging a release, verify release workflow attaches SBOM and provenance.
Review THIRD_PARTY_LICENSES.md and run check-license-compliance.sh after locked installs.
```

## Entry 8 — Workflow Action Validation

**Prompt:**

```
Before committing changes to .github/workflows/, run scripts/validate-workflow-actions.sh.
If gh is unavailable locally, rely on scripts/check-workflow-action-ref-format.sh
(pre-commit) and the CI workflow-actions job. Fix any invalid or bare-semver refs
before push. SHA-pin third-party actions per docs/SECURITY_TRIAGE.md.
```

## Entry 9 — Post-Push GitHub Gate

**Prompt:**

```
After pushing to main, poll required GitHub workflows until green:
  bash scripts/check-github-ci.sh --wait 300
  # Windows: scripts/check-github-ci.ps1 -WaitSeconds 300
Required workflows: CI, Security Scan, CodeQL.
Do not mark release or Sprint 0 complete while any are failing.
```
