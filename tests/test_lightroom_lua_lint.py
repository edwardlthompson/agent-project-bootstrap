"""Lightroom Lua lint stays in feature-gate and rejects generic require()."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from lightroom_lua_lint import check, check_lua  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class LightroomLuaLintTests(unittest.TestCase):
    def test_repo_passes(self) -> None:
        self.assertEqual(check(ROOT), [])

    def test_feature_gate_runs_check(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-lightroom-lua.sh", text)
        self.assertIn("lightroom-lua-lint", text)

    def test_require_is_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.lua"
            path.write_text('require("io")\n', encoding="utf-8")
            errors = check_lua(path)
            self.assertTrue(any("forbidden" in e for e in errors))

    def test_non_lr_import_is_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.lua"
            path.write_text('import "socket"\n', encoding="utf-8")
            errors = check_lua(path)
            self.assertTrue(any("Lr*" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
