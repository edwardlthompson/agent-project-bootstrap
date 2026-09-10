"""Golden Path web Playwright baseline covers the homepage canvas."""

from __future__ import annotations

import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "examples/web/e2e/app.spec.ts-snapshots"
SPEC = ROOT / "examples/web/e2e/app.spec.ts"
HOMEPAGE = "homepage-chromium.png"


def _png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


class WebVisualSnapshotTests(unittest.TestCase):
    def test_homepage_baseline_exists(self) -> None:
        spec = SPEC.read_text(encoding="utf-8")
        self.assertIn('toHaveScreenshot("homepage.png"', spec)
        self.assertNotIn("settings-panel.png", spec)
        self.assertNotIn("about-panel.png", spec)
        self.assertNotIn("feedback-panel.png", spec)
        path = SNAP / HOMEPAGE
        self.assertTrue(path.is_file(), f"missing {path}")
        size = _png_size(path)
        self.assertIsNotNone(size, f"not a PNG: {HOMEPAGE}")
        assert size is not None
        self.assertGreater(size[0], 8, HOMEPAGE)
        self.assertGreater(size[1], 8, HOMEPAGE)
        self.assertGreater(path.stat().st_size, 1024, HOMEPAGE)

    def test_android_panel_tags_match_web(self) -> None:
        android = ROOT / "examples/android/app/src/main/java/dev/foss/goldenpath/ui"
        settings_path = android / "settings/SettingsScreen.kt"
        if not settings_path.is_file():
            self.skipTest("android example pruned")
        settings = settings_path.read_text(encoding="utf-8")
        about = (android / "about/AboutScreen.kt").read_text(encoding="utf-8")
        feedback = (android / "feedback/FeedbackScreen.kt").read_text(encoding="utf-8")
        self.assertIn('testTag("settings-panel")', settings)
        self.assertIn('testTag("about-panel")', about)
        self.assertIn('testTag("feedback-panel")', feedback)


if __name__ == "__main__":
    unittest.main()
