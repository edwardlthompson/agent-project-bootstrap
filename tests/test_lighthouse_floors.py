"""Lighthouse CI keeps accessibility and best-practices error floors."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class LighthouseFloorTests(unittest.TestCase):
    def test_floors_are_errors(self) -> None:
        data = json.loads((ROOT / "examples/web/.lighthouserc.json").read_text(encoding="utf-8"))
        assertions = data["ci"]["assert"]["assertions"]
        self.assertEqual(assertions["categories:accessibility"][0], "error")
        self.assertGreaterEqual(assertions["categories:accessibility"][1]["minScore"], 0.95)
        self.assertEqual(assertions["categories:best-practices"][0], "error")
        self.assertGreaterEqual(assertions["categories:best-practices"][1]["minScore"], 0.9)

    def test_feature_gate_runs_floor_script(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-lighthouse-floors.sh", text)
        self.assertIn("web-lighthouse-floors", text)


if __name__ == "__main__":
    unittest.main()
