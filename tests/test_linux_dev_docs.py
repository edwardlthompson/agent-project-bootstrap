"""LINUX_DEV.md and .envrc.example stay aligned with local-compute env knobs."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "LINUX_DEV.md"
ENVRC = ROOT / ".envrc.example"
NEEDLES = (
    "BOOTSTRAP_CHECK_JOBS",
    "FEATURE_GATE_JOBS",
    "inotify",
    "direnv",
    "check-local-compute",
    "LOCAL_MODELS.md",
)


class LinuxDevDocTests(unittest.TestCase):
    def test_doc_and_envrc_exist(self) -> None:
        self.assertTrue(DOC.is_file())
        self.assertTrue(ENVRC.is_file())

    def test_core_knobs_documented(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        envrc = ENVRC.read_text(encoding="utf-8")
        for needle in NEEDLES:
            self.assertIn(needle, text, needle)
        self.assertIn("BOOTSTRAP_CHECK_JOBS", envrc)
        self.assertIn("FEATURE_GATE_JOBS", envrc)
        self.assertIn("FEATURE_GATE_SCOPE", envrc)
        self.assertNotIn("OPENAI_API_KEY", text)
        self.assertNotIn("0.0.0.0", text)


if __name__ == "__main__":
    unittest.main()
