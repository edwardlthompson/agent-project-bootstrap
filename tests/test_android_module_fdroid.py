"""Android MODULE.md F-Droid rows stay aligned with Golden Path metadata."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "modules/android/MODULE.md"


class AndroidModuleFdroidTests(unittest.TestCase):
    def test_fdroid_rows_name_shipped_paths(self) -> None:
        text = MODULE.read_text(encoding="utf-8")
        self.assertIn("dev.foss.goldenpath.yml", text)
        self.assertIn("antifeatures.yml", text)
        self.assertIn("fastlane/metadata/android/en-US/", text)
        self.assertIn("ANDROID_SIGNING.md", text)
        self.assertIn("unifiedpush.md", text)


if __name__ == "__main__":
    unittest.main()
