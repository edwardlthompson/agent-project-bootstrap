"""Feature-gate compiles instrumented Android tests without an emulator."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class AndroidInstrumentedCompileTests(unittest.TestCase):
    def test_feature_gate_compiles_androidtest_only(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        start = text.index("if should_run android && [ -f examples/android/gradlew ]")
        end = text.index("if should_run android && [ -d examples/android/metadata ]")
        block = text[start:end]
        self.assertIn(":app:compileDebugAndroidTestKotlin", block)
        self.assertIn("android-compile-androidtest", block)
        self.assertNotIn("connectedDebugAndroidTest", block)
        hints = (ROOT / "scripts/lib/gate_hints.json").read_text(encoding="utf-8")
        self.assertIn("android-compile-androidtest", hints)

    def test_module_docs_name_compile_stage(self) -> None:
        docs = (ROOT / "modules/android/MODULE.md").read_text(encoding="utf-8")
        self.assertIn("compileDebugAndroidTestKotlin", docs)
        self.assertIn("no emulator", docs.lower())


if __name__ == "__main__":
    unittest.main()
