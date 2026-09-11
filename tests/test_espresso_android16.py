"""Espresso 3.7+ pin is required for Android 16 instrumented tests."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class EspressoAndroid16Tests(unittest.TestCase):
    def test_gradle_pins_espresso_37(self) -> None:
        gradle = ROOT / "examples/android/app/build.gradle.kts"
        if not gradle.is_file():
            self.skipTest("android example pruned")
        text = gradle.read_text(encoding="utf-8")
        self.assertRegex(text, r"espresso-core:3\.(7|[89]|[1-9][0-9])\.")

    def test_feature_gate_runs_espresso_check(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-espresso-android16.sh", text)
        self.assertIn("android-espresso-16", text)
        hints = (ROOT / "scripts/lib/gate_hints.json").read_text(encoding="utf-8")
        self.assertIn("android-espresso-16", hints)


if __name__ == "__main__":
    unittest.main()
