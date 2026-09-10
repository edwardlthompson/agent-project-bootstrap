"""feature-catalog.json lists the optional Lightroom stack."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "schemas/golden-path/feature-catalog.json"


class FeatureCatalogLightroomTests(unittest.TestCase):
    def test_lightroom_plugin_is_optional_stack(self) -> None:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        feat = next(f for f in data["features"] if f["id"] == "lightroom-plugin")
        self.assertEqual(feat["stacks"], ["lightroom"])
        self.assertIn("examples/lightroom/Info.lua", feat["detect"]["lightroom"])
        self.assertTrue(feat["spec"].startswith("docs/features/"))


if __name__ == "__main__":
    unittest.main()
