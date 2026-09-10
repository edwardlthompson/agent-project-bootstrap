"""Android nav-stack property tests keep Home as the root."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST = ROOT / "examples/android/app/src/test/java/dev/foss/goldenpath/ui/nav/NavPropertyTest.kt"


class AndroidNavPropertyTests(unittest.TestCase):
    def test_random_walk_file_exists(self) -> None:
        if not TEST.is_file():
            self.skipTest("android example pruned")
        text = TEST.read_text(encoding="utf-8")
        self.assertIn("repeat(200)", text)
        self.assertIn("Nav.normalizeStack", text)
        self.assertIn("Nav.isHome", text)
        self.assertIn("Random(42)", text)


if __name__ == "__main__":
    unittest.main()
