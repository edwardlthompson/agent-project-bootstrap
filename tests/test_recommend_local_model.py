"""Hardware recommender tiers without requiring a GPU."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from recommend_local_model import pick_tier, recommend  # noqa: E402


class RecommendLocalModelTests(unittest.TestCase):
    def test_pick_tier_boundaries(self) -> None:
        self.assertEqual(pick_tier(None), "entry")
        self.assertEqual(pick_tier(8192), "entry")
        self.assertEqual(pick_tier(12288), "budget")
        self.assertEqual(pick_tier(24564), "sweet_spot")
        self.assertEqual(pick_tier(48000), "high")

    def test_zero_gpu_json_shape(self) -> None:
        rec = recommend(vram_mib=None, gpu_name=None, ram_gb=16, force_ollama="down", detect_gpu=False)
        data = rec.to_dict()
        self.assertEqual(data["tier"], "entry")
        self.assertIn("primary", data)
        self.assertIn("alternatives", data)
        self.assertIn("warnings", data)
        self.assertTrue(data["warnings"])

    def test_sweet_spot_24gb(self) -> None:
        rec = recommend(vram_mib=24564, gpu_name="NVIDIA RTX 4090", ram_gb=64, force_ollama="down")
        self.assertEqual(rec.tier, "sweet_spot")
        self.assertEqual(rec.primary, "qwen3-coder:30b")
        self.assertEqual(rec.num_ctx, 65536)
        self.assertIn("qwen3-coder-30b-64k", rec.modelfile)

    def test_cli_help(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "recommend_model.py"), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Recommend", proc.stdout)

    def test_cli_json(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "recommend_model.py"), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIn("warnings", data)
        self.assertIn("primary", data)


if __name__ == "__main__":
    unittest.main()
