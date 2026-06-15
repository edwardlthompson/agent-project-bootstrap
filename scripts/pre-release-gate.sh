#!/usr/bin/env bash
# Pre-release gate: CI green, zero Critical/High Dependabot alerts, template version present.
# Usage: scripts/pre-release-gate.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERRORS=0
VERSION=""

echo "=== Pre-release gate ==="

if ! bash scripts/feature-gate.sh --stack multi --strict --json; then
  echo "FAIL: feature-gate.sh"
  ERRORS=$((ERRORS + 1))
else
  echo "OK   feature-gate.sh passed"
fi

if ! bash scripts/check-security-triage.sh --wait-ci 300 --strict; then
  echo "FAIL: security-triage.sh --strict"
  ERRORS=$((ERRORS + 1))
else
  echo "OK   security-triage.sh --strict passed"
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
