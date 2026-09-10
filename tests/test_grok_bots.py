"""docs/GROK_BOTS.md is landed and stays off the FOSS path."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class GrokBotsTests(unittest.TestCase):
    def test_doc_landed(self) -> None:
        text = (ROOT / "docs" / "GROK_BOTS.md").read_text(encoding="utf-8")
        self.assertIn("Not** on the FOSS production path", text)
        self.assertIn("destructive-ops", text)
        self.assertIn("FOSS alternative", text)
        self.assertIn("Android platform scout", text)

    def test_wired(self) -> None:
        boot = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("docs/GROK_BOTS.md", boot)
        start = (ROOT / "docs" / "START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("GROK_BOTS.md", start)


if __name__ == "__main__":
    unittest.main()
