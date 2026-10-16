"""Oct 2026 Cursor registry + integrations docs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CursorFeaturesOct2026Tests(unittest.TestCase):
    def test_registry_entries(self) -> None:
        data = json.loads(
            (ROOT / "docs/CURSOR_FEATURE_REGISTRY.json").read_text(encoding="utf-8")
        )
        ids = {e["id"] for e in data["entries"]}
        self.assertIn("skills.custom-modes", ids)
        self.assertIn("skills.split-to-prs", ids)
        self.assertIn("bots.security-review", ids)

    def test_integrations_doc(self) -> None:
        text = (ROOT / "docs/CURSOR_INTEGRATIONS.md").read_text(encoding="utf-8")
        self.assertIn("Custom Modes", text)
        self.assertIn("split-to-prs", text)


if __name__ == "__main__":
    unittest.main()
