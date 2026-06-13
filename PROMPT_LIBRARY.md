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
check-license-compliance, pre-commit run --all-files.
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
Review Dependabot alerts (Critical/High first), triage open PRs, confirm CI green.
```

## Entry 7 — Pre-Release SBOM Audit

**Prompt:**

```
Before tagging a release, verify release workflow attaches SBOM and provenance.
Review THIRD_PARTY_LICENSES.md and run check-license-compliance.sh after locked installs.
```
