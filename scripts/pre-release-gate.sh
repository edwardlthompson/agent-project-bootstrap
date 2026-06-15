#!/usr/bin/env bash
# Pre-release gate: CI green, zero Critical/High Dependabot alerts, template version present.
# Usage: scripts/pre-release-gate.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERRORS=0
VERSION=""

echo "=== Pre-release gate ==="

if ! bash scripts/feature-gate.sh --stack multi --json; then
  echo "FAIL: feature-gate.sh"
  ERRORS=$((ERRORS + 1))
else
  echo "OK   feature-gate.sh passed"
fi

if ! bash scripts/check-github-ci.sh HEAD --wait 300; then
  echo "FAIL: required GitHub workflows not green"
  ERRORS=$((ERRORS + 1))
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI required for Dependabot alert count"
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
if [ -z "$REPO" ]; then
  echo "ERROR: run from a git repo with gh auth, or export GITHUB_REPO=owner/name"
  exit 1
fi

ALERT_COUNT="$(gh api "repos/${REPO}/dependabot/alerts?state=open&per_page=100" \
  --jq '[.[] | select(.security_vulnerability.severity == "critical" or .security_vulnerability.severity == "high")] | length' 2>/dev/null || echo "error")"

if [ "$ALERT_COUNT" = "error" ]; then
  echo "WARN: could not fetch Dependabot alerts (check gh auth and Dependabot alerts enabled)"
  ERRORS=$((ERRORS + 1))
elif [ "${ALERT_COUNT:-0}" -gt 0 ]; then
  echo "FAIL: ${ALERT_COUNT} open Critical/High Dependabot alert(s)"
  ERRORS=$((ERRORS + 1))
else
  echo "OK   Zero open Critical/High Dependabot alerts"
fi

if [ ! -f .template-version ]; then
  echo "MISSING: .template-version"
  ERRORS=$((ERRORS + 1))
else
  VERSION="$(tr -d '[:space:]' < .template-version)"
  echo "OK   .template-version = ${VERSION}"
fi

echo ""
echo "REMINDER: Before tagging, trigger the Release workflow via workflow_dispatch:"
echo "  GitHub -> Actions -> Release -> Run workflow"
echo "  (.github/workflows/release.yml)"
if [ -n "$VERSION" ]; then
  echo "  Confirm CHANGELOG.md [${VERSION}] section and tag match .template-version"
fi

if [ "$ERRORS" -gt 0 ]; then
  echo "${ERRORS} pre-release gate check(s) failed"
  exit 1
fi

echo "Pre-release gate passed"
