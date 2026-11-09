#!/usr/bin/env python3
"""Gate: layout / goldenpath entrypoints."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from layout_gate import check  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0] if args else ROOT).resolve()
    code, msg = check(root)
    print(msg)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
