"""Android RTL/locale stress tests exist for instrumented compile + Robolectric."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTR = ROOT / "examples/android/app/src/androidTest/java/dev/foss/goldenpath/LocaleRtlUiTest.kt"
UNIT = ROOT / "examples/android/app/src/test/java/dev/foss/goldenpath/ui/LocaleRtlTest.kt"


class AndroidLocaleRtlTests(unittest.TestCase):
    def test_instrumented_covers_spanish_and_rtl(self) -> None:
        text = INSTR.read_text(encoding="utf-8")
        self.assertIn('Locale("es")', text)
        self.assertIn('Locale("ar")', text)
        self.assertIn("LAYOUT_DIRECTION_RTL", text)
        self.assertIn("settings_search", text)

    def test_robolectric_uses_locale_qualifiers(self) -> None:
        text = UNIT.read_text(encoding="utf-8")
        self.assertIn('qualifiers = "es"', text)
        self.assertIn("ldrtl", text)


if __name__ == "__main__":
    unittest.main()
