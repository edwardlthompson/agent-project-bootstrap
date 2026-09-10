"""Golden Path web Playwright baselines cover Settings, About, and Feedback."""

from __future__ import annotations

import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "examples/web/e2e/app.spec.ts-snapshots"
REQUIRED = (
    "homepage-chromium.png",
    "settings-panel-chromium.png",
    "about-panel-chromium.png",
    "feedback-panel-chromium.png",
)
PANEL_SIZES = {
    "settings-panel-chromium.png": (400, 561),
    "about-panel-chromium.png": (512, 585),
    "feedback-panel-chromium.png": (512, 449),
}


def _png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


class WebVisualSnapshotTests(unittest.TestCase):
    def test_settings_about_feedback_baselines_exist(self) -> None:
        spec = (ROOT / "examples/web/e2e/app.spec.ts").read_text(encoding="utf-8")
        self.assertIn('shotPanel(page, panel, "settings-panel.png"', spec)
        self.assertIn('shotPanel(page, panel, "about-panel.png"', spec)
        self.assertIn('shotPanel(page, panel, "feedback-panel.png"', spec)
        self.assertIn("async function freezePanel", spec)
        self.assertIn("async function shotPanel", spec)
        self.assertIn("node.style.width", spec)
        for name in REQUIRED:
            path = SNAP / name
            self.assertTrue(path.is_file(), f"missing {path}")
            size = _png_size(path)
            self.assertIsNotNone(size, f"not a PNG: {name}")
            assert size is not None
            self.assertGreater(size[0], 8, name)
            self.assertGreater(size[1], 8, name)
            self.assertGreater(path.stat().st_size, 1024, name)
            if name in PANEL_SIZES:
                self.assertEqual(size, PANEL_SIZES[name], name)

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
