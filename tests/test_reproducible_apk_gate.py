"""Reproducible APK wiring stays in feature-gate."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ReproducibleApkGateTests(unittest.TestCase):
    def test_feature_gate_runs_reproducible_apk_check(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-reproducible-apk.sh", text)
        self.assertIn("android-reproducible-apk", text)


if __name__ == "__main__":
    unittest.main()
