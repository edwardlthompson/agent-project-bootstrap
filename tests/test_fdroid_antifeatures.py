"""FOSS Golden Path ships an empty F-Droid AntiFeatures list."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class FdroidAntiFeaturesTests(unittest.TestCase):
    def test_template_defaults_empty(self) -> None:
        text = (ROOT / "examples/android/metadata/antifeatures.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("AntiFeatures: []", text)
        self.assertIn("Tracking", text)
        recipe = (ROOT / "examples/android/metadata/dev.foss.goldenpath.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("AntiFeatures: []", recipe)
        self.assertNotIn("Tracking:", recipe)


if __name__ == "__main__":
    unittest.main()
