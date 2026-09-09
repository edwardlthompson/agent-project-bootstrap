"""Release R8 + Android 17 memory-limit guardrails for the Golden Path example."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "examples" / "android"
APP_GRADLE = ANDROID / "app" / "build.gradle.kts"
PROGUARD = ANDROID / "app" / "proguard-rules.pro"
MANIFEST = ANDROID / "app" / "src" / "main" / "AndroidManifest.xml"
GRADLE_PROPS = ANDROID / "gradle.properties"
BROAD_KEEP = "-keep public class *"


class AndroidRuntimeBudgetTests(unittest.TestCase):
    def test_release_enables_r8_optimize_defaults(self) -> None:
        if not APP_GRADLE.is_file():
            self.skipTest("android example pruned")
        text = APP_GRADLE.read_text(encoding="utf-8")
        self.assertIn("isMinifyEnabled = true", text)
        self.assertIn("isShrinkResources = true", text)
        self.assertIn("proguard-android-optimize.txt", text)
        self.assertNotIn("proguard-android.txt", text.replace("proguard-android-optimize.txt", ""))

    def test_proguard_rules_are_narrow(self) -> None:
        if not PROGUARD.is_file():
            self.skipTest("android example pruned")
        text = PROGUARD.read_text(encoding="utf-8")
        active = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        self.assertTrue(any(line.startswith("-keepattributes") for line in active))
        for line in active:
            self.assertNotIn(BROAD_KEEP, line)
            self.assertFalse(line.startswith("-dontoptimize"))
            self.assertFalse(line.startswith("-dontshrink"))
            self.assertFalse(line.startswith("-dontobfuscate"))

    def test_manifest_has_no_large_heap(self) -> None:
        if not MANIFEST.is_file():
            self.skipTest("android example pruned")
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertNotIn("largeHeap", text)
        self.assertIn("android:name=\".GoldenPathApplication\"", text)

    def test_r8_full_mode_not_disabled(self) -> None:
        if not GRADLE_PROPS.is_file():
            self.skipTest("android example pruned")
        text = GRADLE_PROPS.read_text(encoding="utf-8")
        self.assertNotIn("android.enableR8.fullMode=false", text.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
