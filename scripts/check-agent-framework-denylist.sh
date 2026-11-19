#!/usr/bin/env bash
# Fail if compromised agent-framework 1.26.1/1.26.2 or unexpected .pth hooks appear.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=lib/resolve-python.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/resolve-python.sh"
exec "$PY" "$ROOT/scripts/lib/agent_framework_denylist.py"
