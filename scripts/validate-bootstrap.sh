#!/usr/bin/env bash
# Verify required bootstrap artifacts exist and pass delegated checks
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

QUICK=false
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=true ;;
  esac
done

REQUIRED=(
  README.md
  LICENSE
  CONTRIBUTING.md
  SECURITY.md
  CODE_OF_CONDUCT.md
  BUILD_PLAN.md
  AGENTS.md
  AGENT_MEMORY.md
  docs/START_HERE.md
  docs/CURSOR_MODES.md
  docs/INITIALIZATION_PROMPT.md
  .cursor/rules/cursor-modes.mdc
  docs/DESIGN_GUIDE.md
  docs/WEB_PROJECT_LAYOUT.md
  docs/SECURITY_TRIAGE.md
  docs/THREAT_MODEL.md
  docs/PRIVACY.md
  docs/RUNBOOK.md
  docs/FEATURE_MODULES.md
  .github/dependabot.yml
  .github/CODEOWNERS
  THIRD_PARTY_LICENSES.md
  .env.example
  design-tokens/design-tokens.json
  docs/help/BATCH_COMMANDS.md
  docs/BATCH_COMMANDS.md
  .cursor/rules/batch-commands.mdc
  CODE_REVIEW.md.example
  RELEASE_NOTES.md.example
)

BATCH_COMMANDS=(
  audit debug gates triage dependabot push prerelease regress
  feature fix init prune ci docs upgrade setup plan restore compact scope
  bootstrap verify build ship maintain
)

for cmd in "${BATCH_COMMANDS[@]}"; do
  REQUIRED+=(".cursor/commands/${cmd}.md")
done

ERRORS=0

run_check() {
  if ! "$@"; then
    ERRORS=$((ERRORS + 1))
  fi
}

for f in "${REQUIRED[@]}"; do
  if [ ! -e "$f" ]; then
    echo "MISSING: $f"
    ERRORS=$((ERRORS + 1))
  fi
done

if [ -f LICENSE ] && [ ! -s LICENSE ]; then
  echo "EMPTY: LICENSE"
  ERRORS=$((ERRORS + 1))
fi

if [ -f examples/web/package.json ] && [ ! -f examples/web/package-lock.json ]; then
  echo "MISSING: examples/web/package-lock.json (required when web example present)"
  ERRORS=$((ERRORS + 1))
fi

if [ -f examples/node/package.json ] && [ ! -f examples/node/package-lock.json ]; then
  echo "MISSING: examples/node/package-lock.json (required when node example present)"
  ERRORS=$((ERRORS + 1))
fi

if [ -f examples/python/pyproject.toml ] && [ ! -f examples/python/uv.lock ]; then
  echo "MISSING: examples/python/uv.lock (required when python example present)"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q '\[AGENT\]' BUILD_PLAN.md && ! grep -q '\[HUMAN\]' BUILD_PLAN.md; then
  echo "MISSING: BUILD_PLAN.md owner labels"
  ERRORS=$((ERRORS + 1))
fi

run_check bash scripts/sync-exemplar-config.sh
run_check bash scripts/check-file-encoding.sh
run_check bash scripts/check-design-cohesion.sh
run_check bash scripts/check-markdown-tables.sh
run_check bash scripts/check-changelog-unreleased.sh
run_check bash scripts/check-repo-hygiene.sh
run_check bash scripts/check-batch-commands.sh
run_check bash scripts/check-template-version-sync.sh

if [ "$QUICK" = false ]; then
  run_check bash scripts/validate-workflow-actions.sh
fi

run_check bash scripts/validate-template-index.sh

if [ "$ERRORS" -gt 0 ]; then
  echo "$ERRORS bootstrap check(s) failed"
  exit 1
fi

if [ "$QUICK" = true ]; then
  echo "Bootstrap validation passed (--quick: skipped validate-workflow-actions)"
else
  echo "Bootstrap validation passed"
fi
