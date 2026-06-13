#!/usr/bin/env bash
# License compliance checks for active example stacks (requires deps installed)
# Usage: check-license-compliance.sh [web|python|all]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

STACK="${1:-all}"
ERRORS=0
ALLOWED="MIT;ISC;Apache-2.0;BSD-2-Clause;BSD-3-Clause;0BSD;Unlicense;CC0-1.0"

if [ ! -f LICENSE ]; then
  echo "MISSING: LICENSE"
  ERRORS=$((ERRORS + 1))
fi

if [ ! -f THIRD_PARTY_LICENSES.md ]; then
  echo "MISSING: THIRD_PARTY_LICENSES.md"
  ERRORS=$((ERRORS + 1))
fi

check_web() {
  if [ ! -f examples/web/package.json ]; then
    return 0
  fi
  if [ ! -d examples/web/node_modules ]; then
    echo "ERROR: examples/web/node_modules missing — run npm ci before license check"
    ERRORS=$((ERRORS + 1))
    return 0
  fi
  cd examples/web
  if ! npx --yes license-checker --production --excludePrivatePackages --onlyAllow "$ALLOWED"; then
    echo "ERROR: Web dependencies include disallowed licenses"
    ERRORS=$((ERRORS + 1))
  else
    echo "Web license check passed"
  fi
  cd "$ROOT"
}

check_python() {
  if [ ! -f examples/python/pyproject.toml ]; then
    return 0
  fi
  cd examples/python
  if ! command -v uv &>/dev/null; then
    echo "ERROR: uv not found — required for Python license check"
    ERRORS=$((ERRORS + 1))
  elif ! uv sync --locked --all-extras 2>/dev/null; then
    echo "ERROR: examples/python deps not synced — run uv sync --locked first"
    ERRORS=$((ERRORS + 1))
  elif ! uv run pip-licenses --format=csv --with-urls >/dev/null 2>&1; then
    echo "ERROR: pip-licenses failed — install dev extras"
    ERRORS=$((ERRORS + 1))
  else
    echo "Python license listing available"
  fi
  cd "$ROOT"
}

case "$STACK" in
  web) check_web ;;
  python) check_python ;;
  all)
    check_web
    check_python
    ;;
  *)
    echo "Usage: $0 [web|python|all]"
    exit 1
    ;;
esac

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi

echo "License compliance check passed"
