"""Fastlane stays FOSS — no Play supply upload lane."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FASTFILE = ROOT / "examples" / "android" / "fastlane" / "Fastfile"


class FastlaneFossTests(unittest.TestCase):
    def test_no_supply_lane(self) -> None:
        text = FASTFILE.read_text(encoding="utf-8")
        self.assertIn("lane :metadata", text)
        self.assertNotRegex(text, r"lane\s+:supply\b")
        self.assertNotIn("upload_to_play_store", text)
        self.assertIn("no store upload", text.lower())


if __name__ == "__main__":
    unittest.main()
