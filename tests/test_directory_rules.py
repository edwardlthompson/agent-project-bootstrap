"""Directory rules playbook exists and requires globs."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DirectoryRulesTests(unittest.TestCase):
    def test_playbook(self) -> None:
        text = (ROOT / "docs/DIRECTORY_RULES.md").read_text(encoding="utf-8")
        self.assertIn("globs", text)
        self.assertIn("AGENTS.md", text)
        self.assertIn("≤3", text)
        self.assertIn("Directory rules reviewed", text)


if __name__ == "__main__":
    unittest.main()
