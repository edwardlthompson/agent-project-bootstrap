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
else
  run_step "security-triage" bash scripts/check-security-triage.sh --wait-ci "$WAIT_CI"
  run_step "pre-release" bash scripts/pre-release-gate.sh
fi

if command -v gh >/dev/null 2>&1; then
  REF="$(git rev-parse HEAD)"
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
  if [ -n "$REPO" ]; then
    echo ""
    echo "=== ci-jobs (Repo Hygiene + Feature Gate) ==="
    RUN_ID="$(gh run list --repo "$REPO" --commit "$REF" --workflow CI --json databaseId -q '.[0].databaseId' 2>/dev/null || true)"
    if [ -z "$RUN_ID" ]; then
      echo "WARN no CI run for HEAD"
      ERRORS=$((ERRORS + 1))
    else
      for job in "Repo Hygiene" "Feature Gate"; do
        conclusion="$(gh run view "$RUN_ID" --repo "$REPO" --json jobs \
          -q ".jobs[] | select(.name == \"${job}\") | .conclusion" 2>/dev/null | head -1 || true)"
        case "$conclusion" in
          success) echo "OK   CI job: ${job}" ;;
          "") echo "WARN CI job not found: ${job}"; ERRORS=$((ERRORS + 1)) ;;
          *) echo "FAIL CI job ${job} (${conclusion})"; ERRORS=$((ERRORS + 1)) ;;
        esac
      done
    fi
  fi
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
  echo "${ERRORS} maintainer gate(s) failed"
  exit 1
fi

echo "All maintainer gates passed"
