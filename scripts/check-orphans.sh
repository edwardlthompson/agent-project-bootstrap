#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/resolve-python.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/resolve-python.sh"
BASELINE_ARGS=()
if [ "${1:-}" = "--baseline" ]; then
  BASELINE_ARGS=(--baseline "${2:?}")
  shift 2
fi
exec "$PY" "$ROOT/scripts/check-orphans.py" "${BASELINE_ARGS[@]}" "${1:-$ROOT}"
