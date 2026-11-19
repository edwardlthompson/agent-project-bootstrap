"""Pinned Node 24.22.3+ after Nov 2026 security releases."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = "24.22.3"


class NodePinTests(unittest.TestCase):
    def test_nvmrc(self) -> None:
        for rel in ("examples/node/.nvmrc", "examples/web/.nvmrc"):
            text = (ROOT / rel).read_text(encoding="utf-8").strip()
            self.assertEqual(text, PIN, rel)

    def test_engines(self) -> None:
        for rel in ("examples/node/package.json", "examples/web/package.json"):
            data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            self.assertIn(PIN, data.get("engines", {}).get("node", ""), rel)

    def test_workflows(self) -> None:
        needle = f'node-version: "{PIN}"'
        for rel in (
            ".github/workflows/ci.yml",
            ".github/workflows/pages.yml",
            ".github/workflows/weekly-health-check.yml",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(needle, text, rel)
            self.assertNotIn('node-version: "22"', text, rel)

    def test_devcontainer(self) -> None:
        text = (ROOT / ".devcontainer/Dockerfile").read_text(encoding="utf-8")
        self.assertIn("javascript-node:1-24-bookworm", text)
        self.assertNotIn("javascript-node:1-22-bookworm", text)


if __name__ == "__main__":
    unittest.main()
