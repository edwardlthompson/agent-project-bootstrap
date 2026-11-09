#!/usr/bin/env python3
"""Gate: UX contract with optional --baseline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from ux_contract_gate import check  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(ROOT))
    parser.add_argument(
        "--baseline",
        action="store_true",
        default=True,
        help="Respect ux-baseline.json (default true)",
    )
    parser.add_argument("--no-baseline", action="store_true")
    args = parser.parse_args(argv)
    use_baseline = not args.no_baseline
    code, msg = check(Path(args.root).resolve(), use_baseline=use_baseline)
    print(msg)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
