""" /upgrade --deep is documented with Sacred protections. """

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DeepUpgradeTests(unittest.TestCase):
    def test_deep_language(self) -> None:
        for rel in (".cursor/commands/upgrade.md", "docs/help/UPGRADE.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("--deep", text)
            self.assertIn("Reformat", text)
            self.assertIn("Sacred", text)
            self.assertIn("do all", text.lower())
            self.assertIn("examples/", text)


if __name__ == "__main__":
    unittest.main()
