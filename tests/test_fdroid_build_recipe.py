"""F-Droid build recipe stays next to Fastlane-style metadata."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPE = ROOT / "examples/android/metadata/dev.foss.goldenpath.yml"


class FdroidBuildRecipeTests(unittest.TestCase):
    def test_recipe_is_gradle_git_build(self) -> None:
        text = RECIPE.read_text(encoding="utf-8")
        self.assertIn("RepoType: git", text)
        self.assertIn("subdir: examples/android", text)
        self.assertIn("gradle:", text)
        self.assertIn("License: MIT", text)
        verify = (ROOT / "scripts/verify-fdroid-metadata.sh").read_text(encoding="utf-8")
        self.assertIn("dev.foss.goldenpath.yml", verify)


if __name__ == "__main__":
    unittest.main()
