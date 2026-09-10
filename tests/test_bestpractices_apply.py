"""OpenSSF apply URLs map JSON keys onto as=edit proposals."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from bestpractices_apply import (  # noqa: E402
    HUMAN_LEFTOVER,
    PRIVATE_REPORT,
    apply_url,
    form_key,
    load,
    proposals,
)

ROOT = Path(__file__).resolve().parent.parent


class BestpracticesApplyTests(unittest.TestCase):
    def test_osps_key(self) -> None:
        self.assertEqual(form_key("OSPS-AC-01.01_status"), "osps_ac_01_01_status")

    def test_passing_has_met_rows(self) -> None:
        fields = proposals(load(ROOT), "passing")
        self.assertEqual(fields.get("description_good_status"), "Met")
        self.assertEqual(fields.get("enhancement_responses_status"), "Met")
        self.assertIn("crypto_published_status", fields)
        self.assertNotIn("osps_ac_01_01_status", fields)

    def test_baseline_has_osps(self) -> None:
        fields = proposals(load(ROOT), "baseline-1")
        self.assertEqual(fields.get("osps_br_01_02_status"), "Met")

    def test_homepage_and_report_url(self) -> None:
        fields = proposals(load(ROOT), "passing")
        self.assertEqual(fields.get("homepage_url_status"), "Met")
        self.assertEqual(
            fields.get("report_url"),
            "https://github.com/edwardlthompson/agent-project-bootstrap/issues",
        )
        self.assertNotIn("know_secure_design_status", fields)

    def test_private_report_is_url(self) -> None:
        fields = proposals(load(ROOT), "passing")
        justification = fields.get("vulnerability_report_private_justification", "")
        self.assertTrue(justification.startswith("https://"))
        self.assertEqual(justification, PRIVATE_REPORT)
        self.assertIn("/security/advisories/new", justification)
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn(PRIVATE_REPORT, security)

    def test_human_leftover_keys(self) -> None:
        self.assertEqual(HUMAN_LEFTOVER["vulnerability_report_private_status"], "Met")
        self.assertEqual(HUMAN_LEFTOVER["vulnerability_report_private_justification"], PRIVATE_REPORT)
        self.assertNotIn("know_secure_design_status", HUMAN_LEFTOVER)

    def test_url_justification_not_truncated(self) -> None:
        long_url = "https://example.invalid/" + ("x" * 80)
        fields = proposals(
            {"vulnerability_report_private_justification": long_url},
            "passing",
        )
        self.assertEqual(fields["vulnerability_report_private_justification"], long_url)

    def test_forced_leftover_uses_project_edit(self) -> None:
        url = apply_url("passing", HUMAN_LEFTOVER, overrides="vulnerability_report_private_*")
        self.assertIn("/14564/passing/edit?", url)
        self.assertIn("overrides=vulnerability_report_private_", url)
        self.assertIn("security%2Fadvisories%2Fnew", url)


if __name__ == "__main__":
    unittest.main()
