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
        self.assertIn(
            "ghcr.io/github/github-mcp-server:v2.2.0",
            data["mcpServers"]["github"]["args"],
        )
        self.assertIn("depsonar@4.1.0", data["mcpServers"]["depsonar"]["args"])

    def test_foss_allowlist_documented(self) -> None:
        allow = json.loads(
            (ROOT / ".cursor/mcp-allowlist.json").read_text(encoding="utf-8")
        )
        servers = set(allow.get("servers") or [])
        self.assertIn("github", servers)
        self.assertIn("depsonar", servers)
        self.assertNotIn("context7", {s.lower() for s in servers})
        self.assertEqual((allow.get("packages") or {}).get("depsonar"), "4.1.0")
        self.assertIn(
            "ghcr.io/github/github-mcp-server",
            allow.get("images") or {},
        )
        banned = {str(x).lower() for x in allow.get("banned") or []}
        self.assertIn("mcp-server-github", banned)

    def test_pin_policy_documented(self) -> None:
        text = (ROOT / "docs/MCP_RECIPES.md").read_text(encoding="utf-8")
        self.assertIn("Pin policy", text)
        self.assertIn("ghcr.io/github/github-mcp-server", text)
        self.assertIn("MCP Inspector", text)
        self.assertIn("2.16.0", text)

    def test_reference_servers_audit_and_pins(self) -> None:
        text = (ROOT / "docs/MCP_RECIPES.md").read_text(encoding="utf-8")
        self.assertIn("Reference servers (filesystem / git / fetch)", text)
        self.assertIn("@modelcontextprotocol/server-filesystem@2.4.0", text)
        self.assertIn("mcp-server-git==2026.11.18", text)
        self.assertIn("mcp-server-fetch==2026.11.18", text)
        allow = json.loads(
            (ROOT / ".cursor/mcp-allowlist.json").read_text(encoding="utf-8")
        )
        pins = allow.get("optional_min_pins") or {}
        self.assertEqual(pins.get("@modelcontextprotocol/server-filesystem"), "2.4.0")
        self.assertEqual(pins.get("mcp-server-git"), "2026.11.18")
        for name in ("mcp.foss.example", "mcp.web.example"):
            data = json.loads((ROOT / ".cursor" / name).read_text(encoding="utf-8"))
            keys = set(data.get("mcpServers") or {})
            self.assertNotIn("filesystem", keys)
            self.assertNotIn("git", keys)
            self.assertNotIn("fetch", keys)


if __name__ == "__main__":
    unittest.main()
