"""Lightroom SDK playbook stays wired and versions stay aligned."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from lightroom_sdk_playbook import check  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class LightroomSdkPlaybookTests(unittest.TestCase):
    def test_repo_passes(self) -> None:
        self.assertEqual(check(ROOT), [])

    def test_feature_gate_runs_check(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-lightroom-sdk-playbook.sh", text)
        self.assertIn("lightroom-sdk-playbook", text)

    def test_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lr = root / "examples/lightroom"
            lr.mkdir(parents=True)
            (lr / "Info.lua").write_text("LrSdkVersion = 14.0\nLrSdkMinimumVersion = 6.0\n", encoding="utf-8")
            (lr / "README.md").write_text(
                "| `LrSdkVersion` | **13.0** |\n| `LrSdkMinimumVersion` | **6.0** |\n",
                encoding="utf-8",
            )
            (root / "docs").mkdir()
            (root / "docs/LIGHTROOM_SDK_BUMP.md").write_text(
                (ROOT / "docs/LIGHTROOM_SDK_BUMP.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / "scripts").mkdir()
            (root / "scripts/feature-gate.sh").write_text(
                "check-lightroom-sdk-playbook.sh\n", encoding="utf-8"
            )
            errors = check(root)
            self.assertTrue(any("mismatch" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
