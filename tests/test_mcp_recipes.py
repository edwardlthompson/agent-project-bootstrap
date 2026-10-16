"""MCP recipe docs and example JSON stay valid."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class McpRecipesTests(unittest.TestCase):
    def test_recipes_doc_exists(self) -> None:
        text = (ROOT / "docs/MCP_RECIPES.md").read_text(encoding="utf-8")
        self.assertIn("Context7", text)
        self.assertIn("Next.js", text)
        self.assertIn("mcp-allowlist", text)

    def test_web_example_parses(self) -> None:
        data = json.loads(
            (ROOT / ".cursor/mcp.web.example").read_text(encoding="utf-8")
        )
        self.assertIn("github", data["mcpServers"])
        self.assertIn("depsonar", data["mcpServers"])

    def test_foss_allowlist_documented(self) -> None:
        allow = json.loads(
            (ROOT / ".cursor/mcp-allowlist.json").read_text(encoding="utf-8")
        )
        servers = set(allow.get("servers") or [])
        self.assertIn("github", servers)
        self.assertIn("depsonar", servers)
        self.assertNotIn("context7", {s.lower() for s in servers})


if __name__ == "__main__":
    unittest.main()
