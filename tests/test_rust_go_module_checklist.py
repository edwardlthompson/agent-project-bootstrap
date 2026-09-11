"""Rust/Go MODULE.md child-activation checklists stay aligned with Dependabot + examples."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUST = ROOT / "modules/rust/MODULE.md"
GO = ROOT / "modules/go/MODULE.md"


class RustGoModuleChecklistTests(unittest.TestCase):
    def test_rust_activation_checklist(self) -> None:
        text = RUST.read_text(encoding="utf-8")
        self.assertIn("## Activation Checklist", text)
        self.assertIn("examples/rust/", text)
        self.assertIn("cargo", text.lower())
        self.assertIn(".github/dependabot.yml", text)
        self.assertIn("directory: /examples/rust", text)
        self.assertIn("child-activation", text.lower())

    def test_go_activation_checklist(self) -> None:
        text = GO.read_text(encoding="utf-8")
        self.assertIn("## Activation Checklist", text)
        self.assertIn("examples/go/", text)
        self.assertIn("gomod", text.lower())
        self.assertIn(".github/dependabot.yml", text)
        self.assertIn("directory: /examples/go", text)
        self.assertIn("child-activation", text.lower())

    def test_examples_present_on_template(self) -> None:
        self.assertTrue((ROOT / "examples/rust").is_dir())
        self.assertTrue((ROOT / "examples/go").is_dir())


if __name__ == "__main__":
    unittest.main()
