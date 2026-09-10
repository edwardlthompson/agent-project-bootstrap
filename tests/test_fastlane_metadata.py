"""Fastlane Android listing files cover title, descriptions, and lanes."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FL = ROOT / "examples/android/fastlane"


class FastlaneMetadataTests(unittest.TestCase):
    def test_en_us_listing_and_foss_lane(self) -> None:
        if not FL.is_dir():
            self.skipTest("android example pruned")
        locale = FL / "metadata/android/en-US"
        for name in ("title.txt", "short_description.txt", "full_description.txt"):
            self.assertTrue((locale / name).stat().st_size > 0, name)
        self.assertTrue((locale / "changelogs/1.txt").is_file())
        fastfile = (FL / "Fastfile").read_text(encoding="utf-8")
        self.assertIn("lane :metadata", fastfile)
        self.assertNotIn("upload_to_play_store", fastfile)
        appfile = (FL / "Appfile").read_text(encoding="utf-8")
        self.assertIn("dev.foss.goldenpath", appfile)
        verify = (ROOT / "scripts/verify-fdroid-metadata.sh").read_text(encoding="utf-8")
        self.assertIn("fastlane/Fastfile", verify)


if __name__ == "__main__":
    unittest.main()
