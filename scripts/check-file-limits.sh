#!/usr/bin/env bash
# Enforce file line limits: 250 for views, 150 for logic
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VIEW_LIMIT=250
LOGIC_LIMIT=150
ERRORS=0

check_view_paths() {
  local label="$1"
  shift
  while IFS= read -r -d '' file; do
    lines=$(wc -l < "$file" | tr -d ' ')
    if [ "$lines" -gt "$VIEW_LIMIT" ]; then
      echo "FAIL [$label] $file: $lines lines (max $VIEW_LIMIT)"
      ERRORS=$((ERRORS + 1))
    fi
  done
}

echo "Checking view file limits (max $VIEW_LIMIT lines)..."
check_view_paths "view" < <(find "$ROOT" -type f \( \
  -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*_view.*" \
  -o -path "*/examples/web/src/components/*.ts" \
  -o -path "*/examples/android/app/src/main/java/*/ui/*/*.kt" \
  -o -path "*/examples/android/app/src/main/java/*/ui/GoldenPath*.kt" \
  \) ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/.git/*" ! -path "*/dist/*" -print0 2>/dev/null)

echo "Checking logic file limits (max $LOGIC_LIMIT lines)..."
while IFS= read -r -d '' file; do
  lines=$(wc -l < "$file" | tr -d ' ')
  if [ "$lines" -gt "$LOGIC_LIMIT" ]; then
    echo "FAIL [logic] $file: $lines lines (max $LOGIC_LIMIT)"
    ERRORS=$((ERRORS + 1))
  fi
done < <(find "$ROOT/examples" -type f \( -name "*.ts" -o -name "*.py" -o -name "*.kt" \) \
  ! -name "*.test.*" ! -name "*.spec.*" \
  ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/.git/*" \
  ! -path "*/examples/web/src/components/*" \
  ! -path "*/examples/android/app/src/main/java/*/ui/GoldenPath*.kt" \
  ! -path "*/examples/android/app/src/main/java/*/ui/*/*.kt" \
  ! -path "*/examples/web/src/main.ts" \
  -print0 2>/dev/null)

if [ "$ERRORS" -gt 0 ]; then
  echo "$ERRORS file(s) exceed line limits"
  exit 1
fi

echo "All file line limits OK"
