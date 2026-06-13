#!/usr/bin/env bash
# Post-template clone customization helper
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== agent-project-bootstrap init ==="
echo ""

read -rp "Project name: " PROJECT_NAME
read -rp "One-line purpose: " PROJECT_PURPOSE
read -rp "Primary stack (web/python/android/multi): " STACK
read -rp "Template update check interval (off/daily/weekly/monthly/on_session) [weekly]: " INTERVAL
INTERVAL="${INTERVAL:-weekly}"

# Replace placeholders
if [ -n "$PROJECT_NAME" ]; then
  sed -i "s/\[INSERT PLATFORM \/ TECH STACK HERE\]/$STACK/g" docs/INITIALIZATION_PROMPT.md 2>/dev/null || \
    sed -i '' "s/\[INSERT PLATFORM \/ TECH STACK HERE\]/$STACK/g" docs/INITIALIZATION_PROMPT.md
  sed -i "s/\[INSERT DETAILED APP DESCRIPTION AND GOALS HERE\]/$PROJECT_PURPOSE/g" docs/INITIALIZATION_PROMPT.md 2>/dev/null || \
    sed -i '' "s/\[INSERT DETAILED APP DESCRIPTION AND GOALS HERE\]/$PROJECT_PURPOSE/g" docs/INITIALIZATION_PROMPT.md
  sed -i "s/\[INSERT PLATFORM \/ TECH STACK HERE\]/$STACK/g" AGENT_MEMORY.md 2>/dev/null || \
    sed -i '' "s/\[INSERT PLATFORM \/ TECH STACK HERE\]/$STACK/g" AGENT_MEMORY.md
  sed -i "s/\[INSERT DETAILED APP DESCRIPTION AND GOALS HERE\]/$PROJECT_PURPOSE/g" AGENT_MEMORY.md 2>/dev/null || \
    sed -i '' "s/\[INSERT DETAILED APP DESCRIPTION AND GOALS HERE\]/$PROJECT_PURPOSE/g" AGENT_MEMORY.md
fi

# Update check config
python3 - "$INTERVAL" "$ROOT/.template-update.json" << 'PY'
import json, sys
interval, path = sys.argv[1], sys.argv[2]
with open(path) as f:
    d = json.load(f)
d["check_interval"] = interval
with open(path, "w") as f:
    json.dump(d, f, indent=2)
    f.write("\n")
PY

read -rp "GitHub username for CODEOWNERS (without @): " CODEOWNER
if [ -n "$CODEOWNER" ]; then
  sed -i "s/@\[PROJECT_OWNER\]/@$CODEOWNER/g" .github/CODEOWNERS 2>/dev/null || \
    sed -i '' "s/@\[PROJECT_OWNER\]/@$CODEOWNER/g" .github/CODEOWNERS
fi

ABOUT="$PROJECT_NAME - $PROJECT_PURPOSE. Built with agent-project-bootstrap. FOSS MIT."
cat > docs/GITHUB_ABOUT.md << EOF
# GitHub About Block

## Draft Description (edit to <=350 chars)

$ABOUT

## Topics

Add topics relevant to your project and stack.
EOF

# Prune unused examples/modules
read -rp "Prune unused examples/modules? (y/N): " PRUNE
if [ "$PRUNE" = "y" ] || [ "$PRUNE" = "Y" ]; then
  case "$STACK" in
    web) rm -rf examples/python examples/android modules/python modules/android modules/lightroom 2>/dev/null || true ;;
    python) rm -rf examples/web examples/android modules/web modules/android modules/lightroom 2>/dev/null || true ;;
    android) rm -rf examples/web examples/python modules/web modules/python modules/lightroom 2>/dev/null || true ;;
    *) echo "Keeping all examples (multi-stack)" ;;
  esac
fi

echo ""
echo "=== Workflow validation ==="
if command -v gh >/dev/null 2>&1; then
  if bash scripts/validate-workflow-actions.sh; then
    echo "Workflow action refs validated via GitHub API."
  else
    echo "WARN: validate-workflow-actions.sh failed. Fix refs before first push."
  fi
else
  echo "WARN: gh CLI not found. Install GitHub CLI and run:"
  echo "  bash scripts/validate-workflow-actions.sh"
  echo "See README.md and docs/SECURITY_TRIAGE.md for setup."
fi

echo ""
echo "=== Done ==="
echo ""
echo "Next steps:"
echo "  1. Review SECURITY.md, CODEOWNERS, playbooks, and .env.example"
echo "  2. Enable Dependabot alerts + private vulnerability reporting: docs/SECURITY_TRIAGE.md"
echo "  3. Configure branch protection on main (required checks, linear history)"
echo "  4. Open Cursor and paste:"
echo ""
echo "  Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md."
echo "  Follow Section 8 Startup Sequence."
echo "  Use BUILD_PLAN.md Sequential lane first; respect AGENT/HUMAN/ADB/AUTO labels."
echo ""
echo "  5. After first push to main, poll required workflows:"
echo "     bash scripts/check-github-ci.sh --wait 300"
echo ""
echo "GitHub About draft: docs/GITHUB_ABOUT.md"
