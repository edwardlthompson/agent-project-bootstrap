#!/usr/bin/env bash
# Poll GitHub Actions for required workflows on a commit.
# Usage: scripts/check-github-ci.sh [REF] [--wait SECONDS]
# Requires: gh CLI authenticated to the repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REF="$(git rev-parse "${1:-HEAD}")"
WAIT=0
if [[ "${2:-}" == "--wait" ]]; then
  WAIT="${3:-300}"
fi

REQUIRED=("CI" "Security Scan" "CodeQL")

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI required (https://cli.github.com/)"
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
if [ -z "$REPO" ]; then
  echo "ERROR: run from a git repo with gh auth, or export GITHUB_REPO=owner/name"
  exit 1
fi

echo "GitHub Actions status for ${REPO} @ ${REF:0:7}"

deadline=$((SECONDS + WAIT))
while true; do
  mapfile -t RUNS < <(gh run list --repo "$REPO" --commit "$REF" \
    --json workflowName,conclusion,status,url -q '.[] | [.workflowName,.status,.conclusion,.url] | @tsv')

  declare -A SEEN=()
  PENDING=0
  FAILED=0

  for wf in "${REQUIRED[@]}"; do
    line="$(printf '%s\n' "${RUNS[@]}" | grep "^${wf}"$'\t' | head -1 || true)"
    if [ -z "$line" ]; then
      echo "WAIT ${wf}: no run yet"
      PENDING=$((PENDING + 1))
      continue
    fi
    IFS=$'\t' read -r _ status conclusion url <<<"$line"
    SEEN["$wf"]=1
    case "$conclusion" in
      success) echo "OK   ${wf}: ${url}" ;;
      failure|cancelled|timed_out|action_required)
        echo "FAIL ${wf} (${conclusion}): ${url}"
        FAILED=$((FAILED + 1))
        ;;
      *)
        if [ "$status" = "completed" ]; then
          echo "FAIL ${wf} (${conclusion:-unknown}): ${url}"
          FAILED=$((FAILED + 1))
        else
          echo "WAIT ${wf} (${status}): ${url}"
          PENDING=$((PENDING + 1))
        fi
        ;;
    esac
  done

  if [ "$FAILED" -gt 0 ]; then
    echo "${FAILED} required workflow(s) failed on GitHub"
    exit 1
  fi
  if [ "$PENDING" -eq 0 ]; then
    echo "All ${#REQUIRED[@]} required workflows passed on GitHub"
    exit 0
  fi
  if [ "$WAIT" -eq 0 ] || [ "$SECONDS" -ge "$deadline" ]; then
    echo "INCOMPLETE: ${PENDING} workflow(s) still pending (re-run with --wait 300)"
    exit 1
  fi
  sleep 15
done
