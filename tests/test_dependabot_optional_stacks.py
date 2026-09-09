"""Dependabot weekly backup covers Cargo and Go modules."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YML = ROOT / ".github/dependabot.yml"


class DependabotOptionalStackTests(unittest.TestCase):
    def test_cargo_and_gomod_are_weekly(self) -> None:
        text = YML.read_text(encoding="utf-8")
        self.assertIn("package-ecosystem: cargo", text)
        self.assertIn("directory: /examples/rust", text)
        self.assertIn("package-ecosystem: gomod", text)
        self.assertIn("directory: /examples/go", text)
        self.assertNotIn("interval: daily", text)


if __name__ == "__main__":
    unittest.main()
