"""Web MODULE.md checklists stay aligned with the Golden Path."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "modules/web/MODULE.md"


class WebModuleChecklistTests(unittest.TestCase):
    def test_shipped_checklist_rows(self) -> None:
        text = MODULE.read_text(encoding="utf-8")
        self.assertIn("check-design-cohesion.sh", text)
        self.assertIn("check-lighthouse-floors.sh", text)
        self.assertIn("src/locales/es.json", text)
        self.assertIn("Settings-only home chrome", text)
        self.assertIn("Settings/About/Feedback visual snapshots", text)
        self.assertIn("a11y ≥ 0.95", text)


if __name__ == "__main__":
    unittest.main()
