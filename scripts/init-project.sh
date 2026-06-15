#!/usr/bin/env bash
# Post-template clone customization helper
# Usage: scripts/init-project.sh [options]
#   --stack web|python|android|node|multi|none
#   --project-name NAME  --purpose TEXT  --interval INTERVAL
#   --release-repo OWNER/REPO  --donation-url URL  --codeowner USER
#   --prune  --no-prune
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

usage() {
  cat <<'EOF'
Usage: scripts/init-project.sh [options]
  --stack STACK          web|python|android|node|multi|none
  --project-name NAME
  --purpose TEXT
  --interval INTERVAL    off|daily|weekly|monthly|on_session
  --release-repo OWNER/REPO
  --donation-url URL
  --codeowner USER       GitHub username without @
  --prune                Prune unused examples/modules without prompting
  --no-prune             Never prune (overrides --prune)
  -h, --help
EOF
}

STACK=""
PROJECT_NAME=""
PROJECT_PURPOSE=""
INTERVAL=""
RELEASE_REPO=""
DONATION_URL=""
CODEOWNER=""
PRUNE_FLAG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --stack) STACK="${2:-}"; shift 2 ;;
    --project-name) PROJECT_NAME="${2:-}"; shift 2 ;;
    --purpose) PROJECT_PURPOSE="${2:-}"; shift 2 ;;
    --interval) INTERVAL="${2:-}"; shift 2 ;;
    --release-repo) RELEASE_REPO="${2:-}"; shift 2 ;;
    --donation-url) DONATION_URL="${2:-}"; shift 2 ;;
    --codeowner) CODEOWNER="${2:-}"; shift 2 ;;
    --prune) PRUNE_FLAG="yes"; shift ;;
    --no-prune) PRUNE_FLAG="no"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

echo "=== agent-project-bootstrap init ==="
echo ""

if [ -z "$PROJECT_NAME" ]; then
  read -rp "Project name: " PROJECT_NAME
fi
if [ -z "$PROJECT_PURPOSE" ]; then
  read -rp "One-line purpose: " PROJECT_PURPOSE
fi
if [ -z "$STACK" ]; then
  read -rp "Primary stack (web/python/android/node/multi/none): " STACK
fi
STACK="${STACK:-none}"
case "$STACK" in
  web|python|android|node|multi|none) ;;
  *)
    echo "Invalid stack '$STACK'; defaulting to none (keep all examples)."
    STACK=none
    ;;
esac
if [ -z "$INTERVAL" ]; then
  read -rp "Template update check interval (off/daily/weekly/monthly/on_session) [weekly]: " INTERVAL
fi
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


if [ -z "$RELEASE_REPO" ]; then
  read -rp "GitHub owner/repo for app release checks (OWNER/REPO) [skip]: " RELEASE_REPO
fi
if [ -z "$DONATION_URL" ]; then
  read -rp "Donation URL [skip]: " DONATION_URL
fi

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

if [ -z "$CODEOWNER" ]; then
  read -rp "GitHub username for CODEOWNERS (without @): " CODEOWNER
fi
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
  if [ "$PRUNE_FLAG" = "yes" ]; then
    PRUNED=true
    echo "Keeping all examples (multi-stack)."
  elif [ "$PRUNE_FLAG" = "no" ]; then
    echo "Skipping prune (--no-prune)."
  else
    read -rp "Prune unused examples/modules? (y/N): " PRUNE
    if [ "$PRUNE" = "y" ] || [ "$PRUNE" = "Y" ]; then
      PRUNED=true
      echo "Keeping all examples (multi-stack)."
    fi
  fi
else
  if [ "$PRUNE_FLAG" = "yes" ]; then
    PRUNED=true
    case "$STACK" in
      web) rm -rf examples/python examples/android examples/node modules/python modules/android modules/node modules/lightroom 2>/dev/null || true ;;
      python) rm -rf examples/web examples/android examples/node modules/web modules/android modules/node modules/lightroom 2>/dev/null || true ;;
      android) rm -rf examples/web examples/python examples/node modules/web modules/python modules/node modules/lightroom 2>/dev/null || true ;;
      node) rm -rf examples/web examples/python examples/android modules/web modules/python modules/android modules/lightroom 2>/dev/null || true ;;
    esac
  elif [ "$PRUNE_FLAG" = "no" ]; then
    echo "Skipping prune (--no-prune)."
  else
    read -rp "Prune unused examples/modules? (y/N): " PRUNE
    if [ "$PRUNE" = "y" ] || [ "$PRUNE" = "Y" ]; then
      PRUNED=true
      case "$STACK" in
        web) rm -rf examples/python examples/android examples/node modules/python modules/android modules/node modules/lightroom 2>/dev/null || true ;;
        python) rm -rf examples/web examples/android examples/node modules/web modules/android modules/node modules/lightroom 2>/dev/null || true ;;
        android) rm -rf examples/web examples/python examples/node modules/web modules/python modules/node modules/lightroom 2>/dev/null || true ;;
        node) rm -rf examples/web examples/python examples/android modules/web modules/python modules/android modules/lightroom 2>/dev/null || true ;;
      esac
    fi
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
echo "  3. Open Cursor and paste:"
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
