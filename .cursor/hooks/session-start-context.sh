#!/usr/bin/env bash
# sessionStart: one-line stack / distribution context. Fail-open.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python3 - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
parts: list[str] = []
sel = root / ".cursor/stack-selection.json"
if sel.is_file():
    try:
        data = json.loads(sel.read_text(encoding="utf-8"))
        stack = data.get("stack", "?")
        tier = data.get("distribution_tier", "foss")
        parts.append(f"stack={stack} tier={tier}")
    except json.JSONDecodeError:
        pass
if parts:
    print(json.dumps({"user_message": "Session context: " + ", ".join(parts)}))
sys.exit(0)
PY
