"""BUILD_PLAN LOCAL/CLOUD venue gate."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agent_venue import (  # noqa: E402
    check_text,
    extract_scope,
    local_scopes_hit_by_files,
    path_under_scope,
    venue_rows,
)


GOOD = """# Build Plan

<!-- local-agent-lane:begin -->
_No local agent items._
<!-- local-agent-lane:end -->

<!-- cloud-agent-lane:begin -->
_No cloud agent items._
<!-- cloud-agent-lane:end -->

1. 🔲 [AGENT][LOCAL] Do local — scope: scripts/
2. 🔲 [AGENT][CLOUD] Do cloud — scope: docs/
"""


class AgentVenueTests(unittest.TestCase):
    def test_good_plan(self) -> None:
        self.assertEqual(check_text(GOOD, label="t"), [])

    def test_missing_venue(self) -> None:
        bad = GOOD.replace("[AGENT][LOCAL]", "[AGENT]")
        errs = check_text(bad, label="t")
        self.assertTrue(any("missing [LOCAL]/[CLOUD]" in e for e in errs))

    def test_missing_scope(self) -> None:
        bad = GOOD.replace(" — scope: scripts/", "")
        errs = check_text(bad, label="t")
        self.assertTrue(any("missing — scope" in e for e in errs))

    def test_overlap(self) -> None:
        bad = GOOD.replace("scope: docs/", "scope: scripts/lib/")
        errs = check_text(bad, label="t")
        self.assertTrue(any("overlap" in e for e in errs))

    def test_extract_scope(self) -> None:
        self.assertEqual(extract_scope("x — scope: examples/web"), "examples/web")

    def test_path_under_scope(self) -> None:
        self.assertTrue(path_under_scope("scripts/lib/a.py", "scripts"))
        self.assertFalse(path_under_scope("docs/a.md", "scripts"))

    def test_local_hit_by_files(self) -> None:
        hits = local_scopes_hit_by_files(GOOD, ["scripts/lib/agent_venue.py"])
        self.assertEqual(hits, ["scripts"])

    def test_repo_plans(self) -> None:
        for name in ("BUILD_PLAN.md", "BUILD_PLAN_TEMPLATE.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            errs = check_text(text, label=name)
            self.assertEqual(errs, [], msg="\n".join(errs))
            self.assertTrue(venue_rows(text) or "_No local agent items._" in text)


if __name__ == "__main__":
    unittest.main()
