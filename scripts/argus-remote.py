#!/usr/bin/env python3
"""Argus remote console CLI (disabled by default)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from argus_remote import handle_command, status  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] == "status":
        code, msg = status(ROOT)
        print(msg)
        return code
    if args[0] == "cmd" and len(args) >= 3:
        code, msg = handle_command(ROOT, args[1], " ".join(args[2:]))
        if msg:
            print(msg)
        return code
    print("usage: argus-remote.py status | cmd <user_id> <text>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
