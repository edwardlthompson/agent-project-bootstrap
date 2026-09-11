"""Winget publish loop hashes real files and never submits."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from winget_publish_loop import main, sha256_file, write_manifest  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class WingetPublishLoopTests(unittest.TestCase):
    def test_hashes_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            x64 = root / "app-x64.zip"
            x64.write_bytes(b"x64-bytes")
            out = root / "manifest.stub.yaml"
            path = write_manifest(
                out,
                pkg_id="Foss.GoldenPath",
                version="1.2.3",
                installers=[("x64", x64, "https://example.com/releases/1.2.3/app-x64.zip")],
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn(sha256_file(x64), text)
            self.assertIn("Architecture: x64", text)
            self.assertEqual(main(["--x64", str(x64), "--out", str(out), "--version", "1.2.3"]), 0)

    def test_missing_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "manifest.stub.yaml"
            self.assertEqual(main(["--x64", str(Path(tmp) / "gone.zip"), "--out", str(out)]), 1)

    def test_script_refuses_submit(self) -> None:
        sh = (ROOT / "scripts" / "winget-publish-loop.sh").read_text(encoding="utf-8")
        self.assertIn("Does not submit", sh)
        self.assertIn("validate-winget-stub.sh", sh)
        self.assertIn("[HUMAN]", sh)
        self.assertIn("--from-release", sh)
        self.assertIn("gh release download", sh)


if __name__ == "__main__":
    unittest.main()
