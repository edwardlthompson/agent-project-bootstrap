#!/usr/bin/env bash
# Fail on wfx-loot IOCs or CI npm ci without --ignore-scripts.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=lib/resolve-python.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/resolve-python.sh"
exec "$PY" "$ROOT/scripts/lib/wfx_loot_iocs.py"
