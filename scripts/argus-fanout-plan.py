#!/usr/bin/env python3
"""Plan a fleet fanout from a brief (touches nothing)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from fleet_fanout import plan_brief  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: argus-fanout-plan.py briefs/<name>.md", file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.is_file():
        path = ROOT / args[0]
    try:
        plan = plan_brief(ROOT, path)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
