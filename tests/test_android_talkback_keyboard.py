"""TalkBack names and keyboard smoke live in instrumented UI tests."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST = ROOT / "examples/android/app/src/androidTest/java/dev/foss/goldenpath/TalkBackKeyboardUiTest.kt"
SCREEN = ROOT / "examples/android/app/src/main/java/dev/foss/goldenpath/ui/GoldenPathScreen.kt"


class AndroidTalkBackKeyboardTests(unittest.TestCase):
    def test_instrumented_uses_content_description_and_click(self) -> None:
        if not TEST.is_file():
            self.skipTest("android example pruned")
        text = TEST.read_text(encoding="utf-8")
        self.assertIn("onNodeWithContentDescription", text)
        self.assertIn("Settings", text)
        self.assertIn("Back", text)
        self.assertIn("performClick", text)
        self.assertIn("settings-panel", text)

    def test_chrome_icons_have_content_descriptions(self) -> None:
        if not SCREEN.is_file():
            self.skipTest("android example pruned")
        text = SCREEN.read_text(encoding="utf-8")
        self.assertIn("contentDescription = stringResource(R.string.settings_open)", text)
        self.assertIn("contentDescription = stringResource(R.string.nav_back)", text)


if __name__ == "__main__":
    unittest.main()
