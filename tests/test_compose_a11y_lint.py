"""Compose accessibility lint IDs stay wired into feature-gate."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ComposeA11yLintTests(unittest.TestCase):
    def test_lint_xml_and_gradle_enable_a11y_ids(self) -> None:
        lint = ROOT / "examples/android/app/lint.xml"
        if not lint.is_file():
            self.skipTest("android example pruned")
        xml = lint.read_text(encoding="utf-8")
        gradle = (ROOT / "examples/android/app/build.gradle.kts").read_text(encoding="utf-8")
        for issue in (
            "ContentDescription",
            "ClickableViewAccessibility",
            "LabelFor",
            "KeyboardInaccessibleWidget",
        ):
            self.assertIn(f'id="{issue}"', xml)
            self.assertIn(f'error += "{issue}"', gradle)
        self.assertIn("abortOnError = true", gradle)

    def test_feature_gate_runs_compose_a11y_script(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-compose-a11y-lint.sh", text)
        self.assertIn("android-compose-a11y", text)
        hints = (ROOT / "scripts/lib/gate_hints.json").read_text(encoding="utf-8")
        self.assertIn("android-compose-a11y", hints)


if __name__ == "__main__":
    unittest.main()
