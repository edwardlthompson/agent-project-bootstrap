#!/usr/bin/env bash
# Automated README health: relative links resolve, markdown tables lint, encoding.
# Usage: scripts/check-readme-health.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERRORS=0

run_check() {
  if ! "$@"; then
    ERRORS=$((ERRORS + 1))
  fi
}

echo "=== README health check ==="

if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else PY=python3; fi

$PY - "$ROOT/README.md" "$ROOT" << 'PY'
import re, sys
from pathlib import Path

readme = Path(sys.argv[1])
root = Path(sys.argv[2])
text = readme.read_text(encoding="utf-8")
errors = []
for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
    target = m.group(1).strip()
    if target.startswith(("http://", "https://", "mailto:", "#")):
        continue
    path = (readme.parent / target.split("#")[0]).resolve()
    if not path.exists():
        errors.append(f"broken relative link: {target}")
if errors:
    for e in errors[:20]:
        print(f"FAIL: {e}")
    sys.exit(1)
print("OK   README relative links resolve")
PY

run_check bash scripts/check-markdown-tables.sh
run_check bash scripts/check-file-encoding.sh

if [ "$ERRORS" -gt 0 ]; then
  echo "${ERRORS} README health check(s) failed"
  exit 1
fi
echo "README health check passed"
