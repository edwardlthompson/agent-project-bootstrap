"""R8 runtime-budget checks run from feature-gate and CI."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class AndroidR8GateTests(unittest.TestCase):
    def test_feature_gate_and_ci_run_r8_script(self) -> None:
        gate = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("check-android-r8.sh", gate)
        self.assertIn("android-r8", gate)
        self.assertIn("check-android-r8.sh", ci)


if __name__ == "__main__":
    unittest.main()
