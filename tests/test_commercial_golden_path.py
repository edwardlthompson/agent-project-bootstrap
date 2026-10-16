"""Commercial Golden Path docs exist; FOSS path unchanged."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CommercialGoldenPathTests(unittest.TestCase):
    def test_playbook(self) -> None:
        text = (ROOT / "docs/COMMERCIAL_GOLDEN_PATH.md").read_text(encoding="utf-8")
        self.assertIn("consent", text.lower())
        self.assertIn("Monetization", text)
        self.assertIn("FOSS", text)
        web = (ROOT / "modules/web/COMMERCIAL.md").read_text(encoding="utf-8")
        self.assertIn("consent", web.lower())
        rule = (ROOT / ".cursor/rules/commercial-compliance.mdc").read_text(
            encoding="utf-8"
        )
        self.assertIn("COMMERCIAL_GOLDEN_PATH", rule)


if __name__ == "__main__":
    unittest.main()
