#!/usr/bin/env bash
# beforeShellExecution: deny destructive commands unless session approved. Fail-open on errors.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
HOOK_INPUT="$(cat)"
export HOOK_INPUT
python3 - "$ROOT" <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
try:
    data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
except Exception:
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

command = (data.get("command") or "").strip()
if not command:
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

if "<!-- cursor-hooks: off -->" in (root / "BUILD_PLAN.md").read_text(encoding="utf-8"):
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

deny_path = root / ".cursor/hooks/shell-denylist.txt"
patterns: list[str] = []
if deny_path.is_file():
    for line in deny_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line.lower())

approved: list[str] = []
for name in (".cursor-session-state.json", ".cursor-session-state"):
    state_path = root / name
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            approved = state.get("destructive_ops_approved") or []
        except json.JSONDecodeError:
            pass
        break

cmd_lower = command.lower()
for pat in patterns:
    if pat in cmd_lower:
        for ok in approved:
            if ok.lower() in cmd_lower or ok.lower() in ("git push",) and "git push" in cmd_lower:
                print(json.dumps({"permission": "allow"}))
                sys.exit(0)
        print(
            json.dumps(
                {
                    "permission": "deny",
                    "user_message": f"Blocked destructive command (hook): {command[:120]}",
                    "agent_message": "Use /push or /ship for git push approval; set destructive_ops_approved in session state.",
                }
            )
        )
        sys.exit(0)

print(json.dumps({"permission": "allow"}))
PY
