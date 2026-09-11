"""agent-run child environment sanitization."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agent_run_env import child_env  # noqa: E402


class AgentRunEnvTests(unittest.TestCase):
    def test_strips_pythonpath(self) -> None:
        env = child_env({"PYTHONPATH": "scripts/lib", "PATH": "/usr/bin", "HOME": "/tmp"})
        self.assertNotIn("PYTHONPATH", env)
        self.assertTrue(env["PATH"] == "/usr/bin" or env["PATH"].endswith("/usr/bin"))

    def test_keeps_unrelated_keys(self) -> None:
        env = child_env({"FOO": "bar", "PATH": "x", "HOME": "/tmp"})
        self.assertEqual(env["FOO"], "bar")

    def test_unix_local_bin_prepended(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            local_bin = home / ".local" / "bin"
            local_bin.mkdir(parents=True)
            env = child_env({"PATH": "/usr/bin", "HOME": str(home)})
            self.assertTrue(env["PATH"].startswith(str(local_bin)))
            self.assertIn("/usr/bin", env["PATH"])
