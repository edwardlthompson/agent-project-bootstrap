#!/usr/bin/env bash
# beforeMCPExecution: audit-only log. Never block. Fail-open.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
HOOK_INPUT="$(cat)"
export HOOK_INPUT
python3 - "$ROOT" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
try:
    data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
except Exception:
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

log = root / ".cursor/mcp-audit.log"
log.parent.mkdir(parents=True, exist_ok=True)
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
tool = data.get("tool_name") or data.get("name") or "unknown"
server = data.get("server") or data.get("mcp_server") or "unknown"
line = f"{ts} server={server} tool={tool}\n"
try:
    with log.open("a", encoding="utf-8") as fh:
        fh.write(line)
except OSError:
    pass
print(json.dumps({"permission": "allow"}))
PY
