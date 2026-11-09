"""BASE_EXCLUDES: markdown fixtures must yield zero UX findings."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

import ux_contract_gate as ux_mod  # noqa: E402
from ux_contract_gate import markdown_excluded, scan_findings  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class UxExclusionTests(unittest.TestCase):
    def test_markdown_is_excluded(self) -> None:
        self.assertTrue(markdown_excluded(Path("docs/UX_LAW.md")))
        self.assertTrue(markdown_excluded(Path("README.md")))
        self.assertFalse(markdown_excluded(Path("examples/web/src/app.ts")))

    def test_markdown_tree_has_zero_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "note.md").write_text("# hex #ff00aa\n", encoding="utf-8")
            (root / "ux-baseline.json").write_text("{}", encoding="utf-8")
            self.assertEqual(scan_findings(root), [])

    def test_yaml_fallback_loads_fixtures(self) -> None:
        prev = ux_mod.yaml
        try:
            ux_mod.yaml = None
            self.assertEqual(ux_mod.admit_fixtures(ROOT), [])
            code, msg = ux_mod.check(ROOT)
            self.assertEqual(code, 0, msg)
        finally:
            ux_mod.yaml = prev


if __name__ == "__main__":
    unittest.main()
