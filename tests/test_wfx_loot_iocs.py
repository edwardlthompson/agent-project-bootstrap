"""wfx-loot IOC scanner and npm ci --ignore-scripts gate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from wfx_loot_iocs import check_iocs, check_npm_ci_ignore_scripts, check_repo  # noqa: E402


class WfxLootTests(unittest.TestCase):
    def test_repo_clean(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_detects_ci_script_and_audit_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".ci-abcd12.sh").write_text("#!/bin/sh\nexit 42\n", encoding="utf-8")
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "build-audit-deadbeef.yml").write_text("name: x\non: push\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "wfx-audit.md").write_text("probe\n", encoding="utf-8")
            errors = check_iocs(root)
            self.assertTrue(any(".ci-abcd12.sh" in e for e in errors), errors)
            self.assertTrue(any("build-audit" in e for e in errors), errors)
            self.assertTrue(any("wfx-audit.md" in e for e in errors), errors)

    def test_npm_ci_requires_ignore_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "ci.yml").write_text("run: npm ci\n", encoding="utf-8")
            self.assertTrue(check_npm_ci_ignore_scripts(root))
            (wf / "ci.yml").write_text("run: npm ci --ignore-scripts\n", encoding="utf-8")
            self.assertEqual(check_npm_ci_ignore_scripts(root), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-wfx-loot-iocs.sh", text)


if __name__ == "__main__":
    unittest.main()
