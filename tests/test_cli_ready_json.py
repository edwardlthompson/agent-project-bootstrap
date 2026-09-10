"""Rust and Go CLIs share a JSON readiness + log contract."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CliReadyJsonTests(unittest.TestCase):
    def test_go_ready_and_log(self) -> None:
        path = ROOT / "examples/go/log.go"
        if not path.is_file():
            self.skipTest("go example pruned")
        log = path.read_text(encoding="utf-8")
        self.assertIn('{"status":"ok"}', log)
        self.assertIn("--ready", log)
        self.assertIn("LogJSON", log)

    def test_rust_ready_and_log(self) -> None:
        path = ROOT / "examples/rust/src/log.rs"
        if not path.is_file():
            self.skipTest("rust example pruned")
        log = path.read_text(encoding="utf-8")
        self.assertIn("ready_json", log)
        self.assertIn("--ready", log)
        self.assertIn("\"status\":\"ok\"", log.replace("\\", ""))


if __name__ == "__main__":
    unittest.main()
