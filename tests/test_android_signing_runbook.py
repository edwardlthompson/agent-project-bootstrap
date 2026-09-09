"""Android signing runbook stays wired into feature-gate."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from android_signing_runbook import check  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class AndroidSigningRunbookTests(unittest.TestCase):
    def test_repo_passes(self) -> None:
        self.assertEqual(check(ROOT), [])

    def test_feature_gate_runs_check(self) -> None:
        text = (ROOT / "scripts/feature-gate.sh").read_text(encoding="utf-8")
        self.assertIn("check-android-signing-runbook.sh", text)
        self.assertIn("android-signing-runbook", text)

    def test_missing_runbook_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn("missing", " ".join(check(Path(tmp))).lower())


if __name__ == "__main__":
    unittest.main()
