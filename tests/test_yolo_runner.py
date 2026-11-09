"""YOLO runner defaults off."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from yolo_runner import is_armed, run  # noqa: E402


class YoloTests(unittest.TestCase):
    def test_template_disarmed(self) -> None:
        self.assertFalse(is_armed(ROOT))
        code, msg = run(ROOT)
        self.assertEqual(code, 0)
        self.assertIn("YOLO off", msg)

    def test_armed_needs_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "yolo.on").write_text("1\n", encoding="utf-8")
            (root / "argus.contract.json").write_text(
                ROOT.joinpath("argus.contract.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            # create required files listed in contract
            for rel in (
                "branding/brand.json",
                "branding/brand.schema.json",
                "branding/assets/app-icon-1024.png",
                "config/tokens.json",
                "ux-baseline.json",
                ".goldenpath.json",
            ):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                if rel.endswith(".png"):
                    path.write_bytes(b"x" * 500)
                else:
                    src = ROOT / rel
                    path.write_text(
                        src.read_text(encoding="utf-8") if src.is_file() else "{}",
                        encoding="utf-8",
                    )
            code, msg = run(root)
            self.assertEqual(code, 1)
            self.assertIn("rules.manifest", msg)


if __name__ == "__main__":
    unittest.main()
