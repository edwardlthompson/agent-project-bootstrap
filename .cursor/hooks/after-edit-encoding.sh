#!/usr/bin/env bash
# afterFileEdit: UTF-8 encoding check on edited text files. Fail-open.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
HOOK_INPUT="$(cat)"
export HOOK_INPUT
python3 - "$ROOT" <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
try:
    data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
except Exception:
    sys.exit(0)

path_str = data.get("file_path") or data.get("path") or ""
if not path_str:
    sys.exit(0)
path = root / path_str
if not path.is_file():
    sys.exit(0)
text_ext = {".md", ".json", ".yml", ".yaml", ".sh", ".ps1", ".mdc", ".ts", ".tsx", ".py", ".toml", ".html", ".css", ".txt", ".xml", ".gradle", ".kts", ".kt", ".java"}
if path.suffix.lower() not in text_ext and path.name not in (".gitignore", "LICENSE", "AGENTS.md"):
    sys.exit(0)
try:
    proc = subprocess.run(
        ["python3", str(root / "scripts/check-file-encoding.py"), str(path)],
        capture_output=True,
        text=True,
        timeout=5,
        cwd=root,
    )
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "encoding check failed").strip()[:200]
        print(json.dumps({"additional_context": f"Encoding check failed for {path_str}: {msg}"}))
except Exception:
    pass
sys.exit(0)
PY
