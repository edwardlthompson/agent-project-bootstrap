#!/usr/bin/env python3
"""Gate: golden-path orphans (skeleton) with --baseline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from orphan_gate import check  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(ROOT))
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="JSON baseline of accepted finding ids",
    )
    args = parser.parse_args(argv)
    code, msg = check(Path(args.root).resolve(), baseline_path=args.baseline)
    print(msg)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
