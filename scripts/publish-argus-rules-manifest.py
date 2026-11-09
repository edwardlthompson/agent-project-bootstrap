#!/usr/bin/env python3
"""Publish rules.manifest.json from argus/rules (CI on main)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from publish_rules_manifest import write_manifest  # noqa: E402


def main() -> int:
    path = write_manifest(ROOT)
    print(f"Wrote {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
