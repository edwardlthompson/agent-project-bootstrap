#!/usr/bin/env bash
# Post-template clone customization helper
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== agent-project-bootstrap init ==="
echo ""

read -rp "Project name: " PROJECT_NAME
read -rp "One-line purpose: " PROJECT_PURPOSE
read -rp "Primary stack (web/python/android/multi/none): " STACK
STACK="${STACK:-none}"
case "$STACK" in
  web|python|android|multi|none) ;;
  *)
    echo "Invalid stack '$STACK'; defaulting to none (keep all examples)."
    STACK=none
    ;;
esac
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
with open(path, encoding="utf-8") as f:
    d = json.load(f)
d["check_interval"] = interval
with open(path, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2)
    f.write("\n")
PY


read -rp "GitHub owner/repo for app release checks (OWNER/REPO) [skip]: " RELEASE_REPO
read -rp "Donation URL [skip]: " DONATION_URL

python3 - "$ROOT" "$RELEASE_REPO" "$DONATION_URL" << 'PY'
import json, shutil, sys
from pathlib import Path
root, repo, url = sys.argv[1], sys.argv[2], sys.argv[3]
root = Path(root)
src_app = root / ".app-update.json.example"
dst_app = root / ".app-update.json"
if src_app.exists() and not dst_app.exists():
    shutil.copy(src_app, dst_app)
if repo.strip():
    data = json.loads(dst_app.read_text(encoding="utf-8"))
    data["release_repo"] = repo.strip()
    dst_app.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
src_don = root / "donations.json.example"
dst_don = root / "donations.json"
if src_don.exists() and not dst_don.exists():
    shutil.copy(src_don, dst_don)
if url.strip() and dst_don.exists():
    data = json.loads(dst_don.read_text(encoding="utf-8"))
    data["links"] = [{"label": "Donate", "url": url.strip()}]
    dst_don.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

read -rp "GitHub username for CODEOWNERS (without @): " CODEOWNER
if [ -n "$CODEOWNER" ]; then
  sed -i "s/@\[PROJECT_OWNER\]/@$CODEOWNER/g" .github/CODEOWNERS 2>/dev/null || \
    sed -i '' "s/@\[PROJECT_OWNER\]/@$CODEOWNER/g" .github/CODEOWNERS
fi

ABOUT="$PROJECT_NAME - $PROJECT_PURPOSE. Built with agent-project-bootstrap. FOSS MIT."
python3 - "$ABOUT" "$ROOT/docs/GITHUB_ABOUT.md" << 'PY'
import sys
from pathlib import Path
about, path = sys.argv[1], Path(sys.argv[2])
path.write_text(
    f"""# GitHub About Block

## Draft Description (edit to <=350 chars)

{about}

## Topics

Add topics relevant to your project and stack.
""",
    encoding="utf-8",
)
PY

# Prune unused examples/modules
PRUNED=false
if [ "$STACK" = "none" ]; then
  echo "Stack 'none': keeping all examples and modules."
elif [ "$STACK" = "multi" ]; then
  read -rp "Prune unused examples/modules? (y/N): " PRUNE
  if [ "$PRUNE" = "y" ] || [ "$PRUNE" = "Y" ]; then
    PRUNED=true
    echo "Keeping all examples (multi-stack)."
  fi
else
  read -rp "Prune unused examples/modules? (y/N): " PRUNE
  if [ "$PRUNE" = "y" ] || [ "$PRUNE" = "Y" ]; then
    PRUNED=true
    case "$STACK" in
      web) rm -rf examples/python examples/android modules/python modules/android modules/lightroom 2>/dev/null || true ;;
      python) rm -rf examples/web examples/android modules/web modules/android modules/lightroom 2>/dev/null || true ;;
      android) rm -rf examples/web examples/python modules/web modules/python modules/lightroom 2>/dev/null || true ;;
    esac
  fi
fi

python3 scripts/init-stack-sync.py "$STACK" "$ROOT" "$PRUNED"
python3 scripts/sync-design-tokens.py || true
echo "Wrote .cursor/stack-selection.json and synced AGENT_MEMORY active modules."

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
echo "  2. Run scripts/setup-github-repo.sh (or .ps1) for Dependabot alerts, private reporting, branch protection"
echo "     See docs/SECURITY_TRIAGE.md if the script prints a manual checklist (API 422)"
echo "  4. Open Cursor and paste:"
echo ""
echo "  Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md."
echo "  Follow Section 8 Startup Sequence."
echo "  Use BUILD_PLAN.md Sequential lane first; respect AGENT/HUMAN/ADB/AUTO labels."
echo ""
echo "  5. After first push to main, poll required workflows:"
echo "     bash scripts/check-github-ci.sh --wait 300"
echo ""
echo "  6. Install pre-commit hooks and preview ephemeral purge:"
echo "     pip install pre-commit && pre-commit install"
echo "     bash scripts/purge-ephemeral.sh"
echo ""
echo "GitHub About draft: docs/GITHUB_ABOUT.md"
echo "Stack selection: .cursor/stack-selection.json"
