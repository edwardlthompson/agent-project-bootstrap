"""Fleet fanout planner tests."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from fleet_fanout import parse_brief, plan_waves, select_repos  # noqa: E402


class FleetFanoutTests(unittest.TestCase):
    def test_parse_requires_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.md"
            path.write_text(
                "---\nbrief: x\nkind: feature\nscope: tag:web\n---\nbody\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                parse_brief(path)

    def test_waves_canary_then_batches(self) -> None:
        repos = [{"slug": f"o/r{i}", "tags": ["web"]} for i in range(10)]
        waves = plan_waves(repos)
        self.assertEqual(len(waves[0]), 1)
        self.assertEqual(len(waves[1]), 3)
        self.assertTrue(all(len(w) <= 5 for w in waves[2:]))

    def test_select_by_tag(self) -> None:
        fleet = [
            {"slug": "a/a", "tags": ["web"]},
            {"slug": "b/b", "tags": ["android"]},
        ]
        self.assertEqual(len(select_repos(fleet, "tag:web")), 1)


if __name__ == "__main__":
    unittest.main()
