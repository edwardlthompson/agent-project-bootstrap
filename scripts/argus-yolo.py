#!/usr/bin/env python3
"""YOLO status / give-up helper (off unless yolo.on exists)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from yolo_runner import give_up, run  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args and args[0] == "off":
        reason = " ".join(args[1:]) or "manual off"
        give_up(ROOT, reason)
        print("YOLO off; wrote YOLO-OFF.md")
        return 0
    code, msg = run(ROOT)
    print(msg)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
