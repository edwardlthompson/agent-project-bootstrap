#!/usr/bin/env python3
"""Sync AGENT_MEMORY module checkboxes and emit .cursor/stack-selection.json."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MODULE_LINES = {
    "android": "Android / F-Droid",
    "web": "Web / PWA",
    "python": "Python",
    "node": "Node API",
    "lightroom": "Lightroom Classic",
}

PARALLEL_NOTES = {
    "web": "Sprint 1 Parallel: Web PWA scope only (`examples/web/**`)",
    "python": "Sprint 1 Parallel: Python CLI scope only (`examples/python/**`)",
    "android": "Sprint 1 Parallel: Android FOSS scope only (`examples/android/**`)",
    "node": "Sprint 1 Parallel: Node API scope only (`examples/node/**`)",
    "multi": "Sprint 1 Parallel: one agent per active stack; no overlapping paths",
    "none": "Sprint 1 Parallel: scope per AGENT_MEMORY active modules",
}


def active_modules(stack: str) -> list[str]:
    if stack in ("multi", "none"):
        return list(MODULE_LINES.keys())
    if stack in MODULE_LINES:
        return [stack]
    return list(MODULE_LINES.keys())


def sync_agent_memory(root: Path, stack: str) -> None:
    path = root / "AGENT_MEMORY.md"
    text = path.read_text(encoding="utf-8")
    active = set(active_modules(stack))
    for key, label in MODULE_LINES.items():
        mark = "x" if key in active else " "
        pattern = rf"^- \[.\] {re.escape(label)}"
        text = re.sub(pattern, f"- [{mark}] {label}", text, count=1)
    path.write_text(text, encoding="utf-8")


def write_stack_selection(root: Path, stack: str, pruned: bool) -> None:
    cursor_dir = root / ".cursor"
    cursor_dir.mkdir(exist_ok=True)
    payload = {
        "stack": stack,
        "pruned": pruned,
        "active_modules": active_modules(stack),
        "parallel_scope_note": PARALLEL_NOTES.get(stack, PARALLEL_NOTES["none"]),
        "selected_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    (cursor_dir / "stack-selection.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: init-stack-sync.py <stack> <root> <pruned:true|false>", file=sys.stderr)
        sys.exit(1)
    stack, root_s, pruned_s = sys.argv[1], sys.argv[2], sys.argv[3]
    root = Path(root_s)
    sync_agent_memory(root, stack)
    write_stack_selection(root, stack, pruned_s.lower() == "true")


if __name__ == "__main__":
    main()
