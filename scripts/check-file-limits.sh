#!/usr/bin/env bash
# Enforce file line limits: 250 for views, 150 for logic
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VIEW_LIMIT=250
LOGIC_LIMIT=150
ERRORS=0

check_files() {
  local pattern="$1"
  local limit="$2"
  local label="$3"

  while IFS= read -r -d '' file; do
    lines=$(wc -l < "$file" | tr -d ' ')
    if [ "$lines" -gt "$limit" ]; then
      echo "FAIL [$label] $file: $lines lines (max $limit)"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(find "$ROOT" -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*_view.*" \) \
    ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/.git/*" ! -path "*/dist/*" -print0 2>/dev/null)
}

check_logic() {
  while IFS= read -r -d '' file; do
    lines=$(wc -l < "$file" | tr -d ' ')
    if [ "$lines" -gt "$LOGIC_LIMIT" ]; then
      echo "FAIL [logic] $file: $lines lines (max $LOGIC_LIMIT)"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(find "$ROOT/examples" -type f \( -name "*.ts" -o -name "*.py" -o -name "*.kt" \) \
    ! -name "*.test.*" ! -name "*.spec.*" ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/.git/*" -print0 2>/dev/null)
}

echo "Checking view file limits (max $VIEW_LIMIT lines)..."
check_files "*.tsx" "$VIEW_LIMIT" "view"

echo "Checking logic file limits (max $LOGIC_LIMIT lines)..."
check_logic

if [ "$ERRORS" -gt 0 ]; then
  echo "$ERRORS file(s) exceed line limits"
  exit 1
fi

echo "All file line limits OK"
