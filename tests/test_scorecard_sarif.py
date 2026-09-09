"""Scorecard SARIF classifier matches the SECURITY_TRIAGE table."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from scorecard_sarif import check_docs, classify, classify_rule  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class ScorecardSarifTests(unittest.TestCase):
    def test_known_rules(self) -> None:
        self.assertEqual(classify_rule("PinnedDependencies"), ("dismiss", "HUMAN"))
        self.assertEqual(classify_rule("TokenPermissions"), ("fix", "AGENT"))
        self.assertEqual(classify_rule("VulnerabilitiesID"), ("dismiss", "HUMAN"))
        self.assertEqual(classify_rule("Binary-Artifacts"), ("defer", "HUMAN"))
        self.assertEqual(classify_rule("BrandNewCheck"), ("defer", "HUMAN"))

    def test_sarif_results(self) -> None:
        sarif = {
            "runs": [
                {
                    "tool": {"driver": {"rules": [{"id": "t", "name": "TokenPermissions"}]}},
                    "results": [{"ruleId": "t"}],
                }
            ]
        }
        self.assertEqual(classify(sarif), [{"check": "TokenPermissions", "action": "fix", "owner": "AGENT"}])

    def test_docs_aligned(self) -> None:
        self.assertEqual(check_docs(ROOT), [])
        wf = (ROOT / ".github/workflows/scorecard.yml").read_text(encoding="utf-8")
        self.assertIn("scorecard_sarif.py", wf)

    def test_empty_sarif_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.sarif"
            path.write_text(json.dumps({"runs": []}), encoding="utf-8")
            self.assertEqual(classify(json.loads(path.read_text(encoding="utf-8"))), [])


if __name__ == "__main__":
    unittest.main()
