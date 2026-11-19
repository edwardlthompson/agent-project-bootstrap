"""Template workflows must not use pull_request_target."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"^\s*(on:\s*)?pull_request_target(\s|:|$)", re.M)


class PullRequestTargetTests(unittest.TestCase):
    def test_no_workflow_uses_pull_request_target(self) -> None:
        wf = ROOT / ".github" / "workflows"
        for path in list(wf.glob("*.yml")) + list(wf.glob("*.yaml")):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(PATTERN.search(text), path.name)

    def test_validators_forbid_pull_request_target(self) -> None:
        for rel in (
            "scripts/check-workflow-action-ref-format.sh",
            "scripts/validate-workflow-actions.sh",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("pull_request_target", text, rel)


if __name__ == "__main__":
    unittest.main()
