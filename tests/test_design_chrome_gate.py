"""Chrome + chip regression gate for check-design-cohesion."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from design_chrome_gate import check_root  # noqa: E402


class DesignChromeGateTests(unittest.TestCase):
    def test_repo_passes(self) -> None:
        self.assertEqual(check_root(ROOT), [])

    def test_themetoggle_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "examples/web/src/components/ThemeToggle.ts"
            path.parent.mkdir(parents=True)
            path.write_text("export {}", encoding="utf-8")
            self.assertTrue(any("ThemeToggle" in e for e in check_root(root)))

    def test_filterchip_settings_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = (
                root
                / "examples/android/app/src/main/java/dev/foss/goldenpath/ui/settings/SettingsScreen.kt"
            )
            path.parent.mkdir(parents=True)
            path.write_text("FilterChip(selected = true, onClick = {})\n", encoding="utf-8")
            errors = check_root(root)
            self.assertTrue(any("FilterChip" in e for e in errors))

    def test_wired_in_design_cohesion(self) -> None:
        text = (ROOT / "scripts/check-design-cohesion.sh").read_text(encoding="utf-8")
        self.assertIn("design_chrome_gate.py", text)

    def test_child_sprint1_locks_settings_chrome(self) -> None:
        text = (ROOT / "BUILD_PLAN_TEMPLATE.md").read_text(encoding="utf-8")
        sprint1 = text.split("### Sprint 1")[1].split("### Sprint 2")[0]
        self.assertIn("Settings-only chrome", sprint1)
        self.assertIn("check-design-cohesion", sprint1)
        self.assertIn("design_chrome_gate.py", sprint1)
        self.assertIn("no header Theme/About/donate", sprint1)


if __name__ == "__main__":
    unittest.main()
