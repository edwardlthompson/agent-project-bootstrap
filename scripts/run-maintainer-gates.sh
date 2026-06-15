#!/usr/bin/env bash
# Orchestrate template-maintainer weekly/monthly/milestone AUTO gates.
# Usage: scripts/run-maintainer-gates.sh [--quick] [--wait-ci SEC]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

QUICK=false
WAIT_CI=300
while [ $# -gt 0 ]; do
  case "$1" in
    --quick) QUICK=true; shift ;;
    --wait-ci) WAIT_CI="${2:-300}"; shift 2 ;;
    *) shift ;;
  esac
done

ERRORS=0

run_step() {
  local name="$1"
  shift
  echo ""
  echo "=== ${name} ==="
  if "$@"; then
    echo "OK   ${name}"
  else
    echo "FAIL ${name}"
    ERRORS=$((ERRORS + 1))
  fi
}

run_step "readme-health" bash scripts/check-readme-health.sh
run_step "fdroid-metadata" bash scripts/verify-fdroid-metadata.sh
run_step "simulate-upgrade" bash scripts/simulate-template-upgrade.sh
run_step "feature-gate" bash scripts/feature-gate.sh --stack multi --strict

if [ "$QUICK" = true ]; then
  run_step "security-triage" bash scripts/check-security-triage.sh
  if command -v gh >/dev/null 2>&1; then
    run_step "ci-jobs" bash scripts/check-github-ci.sh HEAD --jobs "Repo Hygiene,Feature Gate"
  fi
else
  run_step "pre-release" bash scripts/pre-release-gate.sh
  if command -v gh >/dev/null 2>&1; then
    run_step "ci-jobs" bash scripts/check-github-ci.sh HEAD --wait "$WAIT_CI" --jobs "Repo Hygiene,Feature Gate"
  fi
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
  echo "${ERRORS} maintainer gate(s) failed"
  exit 1
fi

echo "All maintainer gates passed"
