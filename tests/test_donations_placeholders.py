"""donations.json.example keeps international placeholders (not live personal links)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "donations.json.example"


class DonationsPlaceholderTests(unittest.TestCase):
    def test_international_placeholders(self) -> None:
        data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        urls = [str(link.get("url") or "") for link in data.get("links") or []]
        joined = "\n".join(urls)
        for needle in (
            "YOUR_GITHUB_USERNAME",
            "YOUR_USERNAME",
            "YOUR_COLLECTIVE",
            "YOUR_HANDLE",
            "liberapay.com",
            "opencollective.com",
            "paypal.me",
            "github.com/sponsors",
        ):
            self.assertIn(needle, joined, needle)
        docs = (ROOT / "docs/help/DONATIONS.md").read_text(encoding="utf-8")
        self.assertIn("International placeholders review", docs)


if __name__ == "__main__":
    unittest.main()
