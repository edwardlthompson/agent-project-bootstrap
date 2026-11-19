"""beforeMCPExecution FOSS server allowlist + package pins."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from mcp_allowlist import check_examples, check_repo, decide, load_allowed  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class McpAllowlistTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])
        self.assertIn("github", load_allowed(ROOT))

    def test_allow_and_deny(self) -> None:
        self.assertEqual(decide({"server": "github"}, ROOT)["permission"], "allow")
        self.assertEqual(decide({"server": "evil-exfil"}, ROOT)["permission"], "deny")
        self.assertEqual(decide({}, ROOT)["permission"], "allow")

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-mcp-allowlist.sh", text)

    def test_examples_reject_unpinned_npx(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cursor = root / ".cursor"
            cursor.mkdir()
            (cursor / "mcp-allowlist.json").write_text(
                json.dumps(
                    {
                        "servers": ["github", "depsonar"],
                        "packages": {"depsonar": "4.1.0"},
                        "images": {"ghcr.io/github/github-mcp-server": "v2.2.0"},
                        "banned": ["@modelcontextprotocol/server-github"],
                    }
                ),
                encoding="utf-8",
            )
            bad = {
                "mcpServers": {
                    "github": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-github"],
                    }
                }
            }
            for name in ("mcp.foss.example", "mcp.web.example", "mcp.commercial.example"):
                (cursor / name).write_text(json.dumps(bad), encoding="utf-8")
            errors = check_examples(root)
            self.assertTrue(any("banned" in e or "pin npx" in e for e in errors), errors)

    def test_foss_pins_docker_github_and_depsonar(self) -> None:
        data = json.loads((ROOT / ".cursor/mcp.foss.example").read_text(encoding="utf-8"))
        github = data["mcpServers"]["github"]
        self.assertEqual(github["command"], "docker")
        self.assertIn("ghcr.io/github/github-mcp-server:v2.2.0", github["args"])
        depsonar = data["mcpServers"]["depsonar"]["args"]
        self.assertIn("depsonar@4.1.0", depsonar)


if __name__ == "__main__":
    unittest.main()
