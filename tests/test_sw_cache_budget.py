"""Offline SW precache budget for /gates canvas."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sw_cache_budget import check, measure, parse_precache, summary_row  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class SwCacheBudgetTests(unittest.TestCase):
    def test_parses_precache_entries(self) -> None:
        text = 'const PRECACHE = ["./", "./index.html", "./icon.svg"];\n'
        self.assertEqual(parse_precache(text), ["./", "./index.html", "./icon.svg"])

    def test_repo_shell_within_budget(self) -> None:
        if not (ROOT / "examples/web/public/sw.js").is_file():
            self.skipTest("web example pruned")
        errors = check(ROOT)
        self.assertEqual(errors, [])
        total, sizes, measure_errors = measure(ROOT)
        self.assertEqual(measure_errors, [])
        self.assertGreater(total, 0)
        self.assertGreaterEqual(len(sizes), 3)
        row = summary_row(ROOT)
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row[0], "sw-cache-budget")
        self.assertTrue(row[1].startswith("Pass"), row[1])


if __name__ == "__main__":
    unittest.main()
