#!/usr/bin/env python3
"""Dry-run (default) or --apply custom Ollama model create for local agents."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from local_resources import ollama_up  # noqa: E402
from recommend_local_model import format_text, ollama_tags, recommend  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Set up a local Ollama agent model (dry-run default).")
    p.add_argument(
        "--apply",
        action="store_true",
        help="Run ollama create when base model is already present (never auto-pull).",
    )
    args = p.parse_args(argv)
    try:
        rec = recommend()
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(format_text(rec))
    print()
    print("XML hard rule: Anthropic-style tool calls only (see docs/help/LOCAL_AGENT.md).")
    print(f"Cline: Provider=Ollama, Model={rec.custom_name}, Context Window={rec.num_ctx}")

    if not ollama_up():
        print("WARN: Ollama not up on 127.0.0.1:11434 — start it, then re-run.", file=sys.stderr)
        if args.apply:
            return 1
        return 0

    modelfile = ROOT / rec.modelfile
    if not modelfile.is_file():
        print(f"FAIL: missing Modelfile {rec.modelfile}", file=sys.stderr)
        return 1

    tags = ollama_tags()
    base_ok = rec.primary in tags or rec.primary.split(":")[0] in tags
    if not args.apply:
        print("Dry-run only. When ready:")
        print(f"  ollama pull {rec.primary}")
        print(f"  python3 scripts/agent-run.py setup-local -- --apply")
        return 0

    if not base_ok:
        print(f"FAIL: base model not local. Pull first:\n  ollama pull {rec.primary}", file=sys.stderr)
        print(f"Then: ollama create {rec.custom_name} -f {rec.modelfile}", file=sys.stderr)
        return 1

    if not shutil.which("ollama"):
        print("FAIL: ollama binary not on PATH", file=sys.stderr)
        return 1
    try:
        proc = subprocess.run(
            ["ollama", "create", rec.custom_name, "-f", str(modelfile)],
            cwd=str(ROOT),
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL: ollama create: {exc}", file=sys.stderr)
        return 1
    if proc.returncode != 0:
        print("FAIL: ollama create exited non-zero", file=sys.stderr)
        return proc.returncode
    print(f"Created custom model: {rec.custom_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
