#!/usr/bin/env python3
"""Emit a tight Current State paste block from session-state + AGENT_MEMORY."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _tail_lines(path: Path, n: int) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    return lines[-n:] if len(lines) > n else lines


def main() -> int:
    warnings: list[str] = []
    parts: list[str] = ["# Current State", ""]

    md = ROOT / ".agent" / "session-state.md"
    js = ROOT / ".cursor-session-state.json"
    if md.is_file():
        parts.append("## Session state (.agent/session-state.md)")
        parts.append(md.read_text(encoding="utf-8", errors="replace").rstrip())
        parts.append("")
    elif js.is_file():
        parts.append("## Session state (.cursor-session-state.json excerpt)")
        try:
            data = json.loads(js.read_text(encoding="utf-8"))
            keys = (
                "active_sprint",
                "sequential_step",
                "current_feature",
                "last_files_touched",
                "last_gate_exit",
                "strikes",
                "notes",
                "unreleased_excerpt",
                "open_human_adb_rows",
            )
            excerpt = {k: data.get(k) for k in keys if k in data}
            parts.append("```json")
            parts.append(json.dumps(excerpt, indent=2))
            parts.append("```")
            parts.append("")
        except (OSError, ValueError, UnicodeError) as exc:
            warnings.append(f"JSON session-state unreadable: {exc}")
    else:
        warnings.append("No .agent/session-state.md or .cursor-session-state.json")

    mem = ROOT / "AGENT_MEMORY.md"
    if mem.is_file():
        parts.append("## AGENT_MEMORY (last 20 lines)")
        parts.extend(_tail_lines(mem, 20))
        parts.append("")
    else:
        warnings.append("AGENT_MEMORY.md missing")

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    sys.stdout.write("\n".join(parts).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
