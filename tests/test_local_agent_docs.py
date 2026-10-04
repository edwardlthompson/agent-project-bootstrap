"""Local-agent docs and Ollama Modelfiles stay present."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = (
    ROOT / "docs" / "LOCAL_MODELS.md",
    ROOT / "docs" / "help" / "LOCAL_AGENT.md",
    ROOT / "docs" / "help" / "LOCAL_TROUBLESHOOTING.md",
    ROOT / "docs" / "help" / "SESSION_START.md",
    ROOT / "docs" / "help" / "VSCODE_COMMANDS.md",
)
NEEDLES = (
    "OLLAMA_FLASH_ATTENTION",
    "24 GB",
    "Anthropic",
    "XML",
    "templates/ollama",
)
MODELS = (
    "Modelfile.qwen3-coder-30b-64k",
    "Modelfile.qwen3.6-27b-64k",
    "Modelfile.qwen2.5-coder-32b-32k",
    "Modelfile.qwen2.5-coder-14b-32k",
    "Modelfile.qwen2.5-coder-7b-16k",
)


class LocalAgentDocTests(unittest.TestCase):
    def test_docs_exist(self) -> None:
        for path in DOCS:
            self.assertTrue(path.is_file(), path.as_posix())

    def test_local_models_needles(self) -> None:
        text = (ROOT / "docs" / "LOCAL_MODELS.md").read_text(encoding="utf-8")
        for needle in NEEDLES:
            self.assertIn(needle, text, needle)
        self.assertIn("does **not** require Ollama", text)

    def test_modelfiles(self) -> None:
        base = ROOT / "templates" / "ollama"
        self.assertTrue(base.is_dir())
        for name in MODELS:
            path = base / name
            self.assertTrue(path.is_file(), name)
            body = path.read_text(encoding="utf-8")
            self.assertIn("PARAMETER num_ctx", body)
            self.assertIn("Anthropic-style XML", body)
            self.assertNotIn("OPENAI_API_KEY", body)


if __name__ == "__main__":
    unittest.main()
