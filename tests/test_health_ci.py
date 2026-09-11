"""Health CI snapshot skips Release Please branches."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from health_ci import (  # noqa: E402
    ci_red_one_liner,
    failed_required_from_runs,
    filter_runs,
    format_run,
    print_ci_snapshot,
)


class FilterRunsTests(unittest.TestCase):
    def test_drops_release_please_branch(self) -> None:
        runs = [
            {"headBranch": "release-please--branches--main", "name": "Dependency Review"},
            {"headBranch": "main", "name": "CI", "status": "completed", "conclusion": "success"},
        ]
        kept = filter_runs(runs)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["name"], "CI")

    def test_format_line(self) -> None:
        line = format_run(
            {
                "status": "completed",
                "conclusion": "success",
                "displayTitle": "feat: x",
                "name": "CI",
                "headBranch": "main",
            }
        )
        self.assertIn("main", line)
        self.assertIn("CI", line)

    def test_failed_required_names(self) -> None:
        runs = [
            {"name": "CI", "conclusion": "failure", "headBranch": "main"},
            {"name": "CodeQL", "conclusion": "success", "headBranch": "main"},
            {"name": "Feature Gate", "conclusion": "failure", "headBranch": "main"},
        ]
        failed = failed_required_from_runs(
            runs, ["CI", "Security Scan", "CodeQL", "Feature Gate"]
        )
        self.assertEqual(failed, ["CI", "Feature Gate"])

    def test_ci_red_one_liner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gh = root / ".github"
            gh.mkdir()
            (gh / "required-checks.json").write_text(
                '{"required_status_checks":["CI","CodeQL"]}',
                encoding="utf-8",
            )
            runs = [{"name": "CI", "conclusion": "failure", "headBranch": "main"}]
            line = ci_red_one_liner(root, runs)
            self.assertIn("CI red", line)
            self.assertIn("CI", line)

    def test_print_ci_snapshot_fail_soft_without_gh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # _gh returns empty when gh missing; print_ci_snapshot must exit 0
            self.assertEqual(print_ci_snapshot(Path(tmp)), 0)


if __name__ == "__main__":
    unittest.main()
