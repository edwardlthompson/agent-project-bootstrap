"""Rust/Go About versions must come from Cargo.toml / the Go module."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CliModuleVersionTests(unittest.TestCase):
    def test_rust_uses_cargo_pkg_version(self) -> None:
        cargo_path = ROOT / "examples/rust/Cargo.toml"
        if not cargo_path.is_file():
            self.skipTest("rust example pruned")
        cargo = cargo_path.read_text(encoding="utf-8")
        about = (ROOT / "examples/rust/src/about.rs").read_text(encoding="utf-8")
        self.assertIn('version = "0.1.0"', cargo)
        self.assertIn('env!("CARGO_PKG_VERSION")', about)

    def test_go_reads_build_info_module(self) -> None:
        version_path = ROOT / "examples/go/version.go"
        if not version_path.is_file():
            self.skipTest("go example pruned")
        version = version_path.read_text(encoding="utf-8")
        mod = (ROOT / "examples/go/go.mod").read_text(encoding="utf-8")
        self.assertIn("debug.ReadBuildInfo", version)
        self.assertIn("module github.com/example/agent-bootstrap-hello", mod)


if __name__ == "__main__":
    unittest.main()
