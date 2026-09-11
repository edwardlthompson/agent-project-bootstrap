"""Waiting-on-a-person HUMAN/ADB automation match + dry handlers."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from human_task_waiting_docs import (  # noqa: E402
    automate_openssf_gap_list,
    automate_winget_checklist,
)
from human_task_waiting_gh import (  # noqa: E402
    automate_pages_custom_domain,
    automate_private_vuln_reporting,
    automate_push_protection,
)

ROOT = Path(__file__).resolve().parent.parent

WAITING = (
    ("HUMAN", "Approve/merge Release Please 1.3.0 when workflows allow (#4)"),
    ("HUMAN", "Lightroom Plug-in Manager load smoke (#29)"),
    ("HUMAN", "Private vulnerability reporting dry-run (#42)"),
    ("HUMAN", "Baseline-1 / Silver OpenSSF gap list (no fake claims) (#79)"),
    ("HUMAN", "Winget submission checklist (never auto-submit) (#153)"),
    ("HUMAN", "Secret scanning push protection enablement check (#180)"),
    ("HUMAN", "GitHub Pages custom domain checklist (optional) (#192)"),
    ("ADB", "TalkBack device checklist (non-Compose / uiautomator) (#15)"),
    ("ADB", "UnifiedPush end-to-end with FOSS distributor (#16)"),
    ("ADB", "Preferred display mode test on multi-refresh phones (#72)"),
    ("ADB", "Android foldable / multi-window nav persist smoke (#90)"),
    ("ADB", "Theme change persists across process death (#120)"),
    ("ADB", "Screen density / font-scale instrumented smoke (#127)"),
)


class WaitingAutomationTests(unittest.TestCase):
    def test_rules_match_waiting_rows(self) -> None:
        from human_task_automation import ADB_RULES, HUMAN_RULES

        for owner, task in WAITING:
            rules = HUMAN_RULES if owner == "HUMAN" else ADB_RULES
            matched = any(pattern.search(task) for pattern, _kind, _handler in rules)
            self.assertTrue(matched, f"no rule for {owner}: {task}")

    def test_openssf_gap_list_writes_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / ".bestpractices.json").write_text(
                '{"OSPS-AC-01.01": "Met", "code_of_conduct_status": "Met"}\n',
                encoding="utf-8",
            )
            result = automate_openssf_gap_list(root, {})
            self.assertEqual(result.exit_code, 0)
            text = (root / "docs" / "OPENSSF_GAP_LIST.md").read_text(encoding="utf-8")
            self.assertIn("Do not claim Met yet", text)
            self.assertIn("OSPS-AC-01.01", text)

    def test_push_protection_enabled(self) -> None:
        with mock.patch("human_task_waiting_gh.subprocess.run") as run:
            run.return_value = mock.Mock(returncode=0, stdout="enabled\n", stderr="")
            result = automate_push_protection(ROOT, {})
            self.assertEqual(result.exit_code, 0)

    def test_private_vuln_enabled(self) -> None:
        with mock.patch("human_task_waiting_gh.subprocess.run") as run:
            run.return_value = mock.Mock(
                returncode=0,
                stdout='{"enabled":true}',
                stderr="",
            )
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "SECURITY.md").write_text("See security/advisories\n", encoding="utf-8")
                result = automate_private_vuln_reporting(root, {})
                self.assertEqual(result.exit_code, 0)

    def test_pages_optional_domain(self) -> None:
        with mock.patch("human_task_waiting_gh.subprocess.run") as run:
            run.return_value = mock.Mock(
                returncode=0,
                stdout='{"html_url":"https://example.github.io/x/","cname":null,"https_enforced":true}',
                stderr="",
            )
            result = automate_pages_custom_domain(ROOT, {})
            self.assertEqual(result.exit_code, 0)
            self.assertIn("no custom domain", result.reason)

    def test_winget_checklist_on_example(self) -> None:
        result = automate_winget_checklist(ROOT, {})
        self.assertEqual(result.exit_code, 0, result.reason)


if __name__ == "__main__":
    unittest.main()
