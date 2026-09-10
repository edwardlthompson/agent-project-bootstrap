"""feature-catalog.json lists the Golden Path navigation stack."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "schemas/golden-path/feature-catalog.json"


class FeatureCatalogNavigationTests(unittest.TestCase):
    def test_navigation_is_catalogued(self) -> None:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        nav = next(f for f in data["features"] if f["id"] == "navigation")
        self.assertEqual(nav["spec"], "docs/features/navigation.md")
        self.assertEqual(set(nav["stacks"]), {"web", "android"})
        self.assertIn("examples/web/src/nav", nav["detect"]["web"])
        self.assertTrue(
            any("ui/nav" in p for p in nav["detect"]["android"]),
        )


if __name__ == "__main__":
    unittest.main()
