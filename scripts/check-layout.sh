#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/resolve-python.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/resolve-python.sh"
exec "$PY" "$ROOT/scripts/check-layout.py" "${1:-$ROOT}"
