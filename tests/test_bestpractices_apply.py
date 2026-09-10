"""OpenSSF apply URLs map JSON keys onto as=edit proposals."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from bestpractices_apply import form_key, load, proposals  # noqa: E402

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


if __name__ == "__main__":
    unittest.main()
