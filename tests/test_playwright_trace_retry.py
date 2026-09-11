"""Playwright keeps trace-on-retry for CI flake triage."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "examples" / "web" / "playwright.config.ts"


class PlaywrightTraceTests(unittest.TestCase):
    def test_trace_on_first_retry(self) -> None:
        text = CFG.read_text(encoding="utf-8")
        self.assertIn('trace: "on-first-retry"', text)
        self.assertRegex(text, r"retries:\s*process\.env\.CI \? 2")


if __name__ == "__main__":
    unittest.main()
