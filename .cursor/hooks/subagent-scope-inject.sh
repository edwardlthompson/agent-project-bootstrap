#!/usr/bin/env bash
# subagentStart: inject parallel scope lock when present. Fail-open.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python3 - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
lock = root / ".cursor/parallel-scope-lock.json"
if not lock.is_file():
    sys.exit(0)
try:
    data = json.loads(lock.read_text(encoding="utf-8"))
    agents = data.get("agents") or []
    scopes = [f"{a.get('id','?')}: {a.get('scope','')}" for a in agents[:8]]
    if scopes:
        msg = "Parallel scope lock active. Stay inside assigned scope only. " + "; ".join(scopes)
        print(json.dumps({"user_message": msg}))
except Exception:
    pass
sys.exit(0)
PY
