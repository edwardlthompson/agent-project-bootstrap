"""Icon factory tests that do not require Blender."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples" / "blender"
SCHEMA = ROOT / "schemas" / "golden-path" / "icon-manifest.schema.json"
if not (EX / "cli.py").is_file():
    raise unittest.SkipTest("blender example pruned")
if str(EX) not in sys.path:
    sys.path.insert(0, str(EX))

from cli import run as cli_run  # noqa: E402
from cycles_device import cycles_device  # noqa: E402
from manifest import load_manifest  # noqa: E402
from qa import qa_png, write_stub_png  # noqa: E402


class IconFactoryTests(unittest.TestCase):
    def test_sample_manifest(self) -> None:
        jobs = load_manifest(EX / "fixtures" / "icon-manifest.sample.json")
        self.assertGreaterEqual(len(jobs), 2)
        self.assertTrue(all("seed" in j and "camera" in j for j in jobs))
        self.assertTrue(any(j["lighting"]["area_lights"] for j in jobs))

    def test_sample_matches_schema_required(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        sample = json.loads((EX / "fixtures" / "icon-manifest.sample.json").read_text(encoding="utf-8"))
        required = schema["$defs"]["job"]["required"]
        self.assertIn("jobs", sample)
        for job in sample["jobs"]:
            for key in required:
                self.assertIn(key, job)

    def test_missing_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(
                json.dumps({"jobs": [{"id": "x", "camera": {"location": [1, 0, 0], "look_at": [0, 0, 0]}}]}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_manifest(path)

    def test_empty_jobs_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.json"
            path.write_text(json.dumps({"jobs": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_manifest(path)
            code = cli_run(["--stub", "--manifest", str(path), "--out", tmp])
            self.assertEqual(code, 2)

    def test_stub_png_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "a.png"
            write_stub_png(png, size=64)
            info = qa_png(png)
            self.assertTrue(info["ok"], info)
            self.assertEqual(info["width"], 64)
            self.assertGreater(info["alpha_ratio"] or 0, 0.02)

    def test_optix_env(self) -> None:
        self.assertEqual(cycles_device({"BLENDER_CYCLES_DEVICE": "OPTIX"}), "OPTIX")
        self.assertEqual(cycles_device({}), "CPU")

    def test_resume_uses_content_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            manifest = EX / "fixtures" / "icon-manifest.sample.json"
            self.assertEqual(cli_run(["--stub", "--limit", "1", "--manifest", str(manifest), "--out", str(out)]), 0)
            first = (out / "hero-yaw-0.png").read_bytes()
            self.assertEqual(
                cli_run(["--stub", "--limit", "1", "--resume", "--manifest", str(manifest), "--out", str(out)]),
                0,
            )
            self.assertEqual((out / "hero-yaw-0.png").read_bytes(), first)
            (out / "hero-yaw-0.png.sha256").write_text("deadbeef\n", encoding="utf-8")
            self.assertEqual(
                cli_run(["--stub", "--limit", "1", "--resume", "--manifest", str(manifest), "--out", str(out)]),
                0,
            )


if __name__ == "__main__":
    unittest.main()
