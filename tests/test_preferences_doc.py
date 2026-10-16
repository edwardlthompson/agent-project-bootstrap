"""docs/PREFERENCES.md keeps coding + security guardrails."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PreferencesDocTests(unittest.TestCase):
    def test_patterns_and_security(self) -> None:
        text = (ROOT / "docs/PREFERENCES.md").read_text(encoding="utf-8")
        lower = text.lower()
        self.assertIn("dev, test, and prod", lower)
        self.assertIn(".env", text)
        self.assertIn("tests only", lower)
        self.assertIn("API-key", text)
        self.assertIn("rate limit", lower)
        self.assertIn("input validation", lower)
        self.assertIn("refuse", lower)
        self.assertIn("THREAT_MODEL", text)
        self.assertIn("FILE_SIZE_GUIDE", text)


if __name__ == "__main__":
    unittest.main()
