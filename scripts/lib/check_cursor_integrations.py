"""Validate Cursor FOSS integration artifacts and tier compliance."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILLS = ("validate-bootstrap", "parallel-scope", "watch-gates-autofix")
AGENTS = ("verifier", "gate-fixer", "explorer")
COMMAND_SKILL = {
    "gates.md": "validate-bootstrap",
    "scope.md": "parallel-scope",
    "fix.md": "watch-gates-autofix",
}

COMMERCIAL_LIVE = (
    ".cursor/BUGBOT.md",
    ".cursor/environment.json",
    ".cursor/approval-policies",
)

FOSS_EXAMPLES = (
    ".cursor/mcp.foss.example",
    ".cursor/hooks.json",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_artifacts(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in FOSS_EXAMPLES:
        if not (root / rel).is_file():
            errors.append(f"missing: {rel}")

    for name in SKILLS:
        skill = root / f".cursor/skills/{name}/SKILL.md"
        if not skill.is_file():
            errors.append(f"missing skill: {name}")
            continue
        body = read_text(skill)
        if "See also:" not in body:
            errors.append(f"skill {name} missing See also: link")

    for name in AGENTS:
        agent = root / f".cursor/agents/{name}.md"
        if not agent.is_file():
            errors.append(f"missing agent: {name}")

    for cmd, skill in COMMAND_SKILL.items():
        path = root / ".cursor/commands" / cmd
        if not path.is_file():
            errors.append(f"missing command: {cmd}")
            continue
        if skill not in read_text(path):
            errors.append(f"{cmd} missing skill pointer for {skill}")

    registry = root / "docs/CURSOR_FEATURE_REGISTRY.json"
    if not registry.is_file():
        errors.append("missing docs/CURSOR_FEATURE_REGISTRY.json")
    else:
        try:
            data = json.loads(read_text(registry))
            entries = data.get("entries") or []
            if not entries:
                errors.append("registry has no entries")
            for entry in entries:
                if "distribution_tier" not in entry:
                    errors.append(f"registry entry missing distribution_tier: {entry.get('id')}")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid registry JSON: {exc}")

    return errors


def validate_tier(root: Path, tier: str) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    if tier == "foss":
        for rel in COMMERCIAL_LIVE:
            path = root / rel
            if path.exists():
                errors.append(f"foss tier: commercial live file present: {rel}")
        # Live .cursor/mcp.json is gitignored and OK locally; fail only if tracked.
        mcp = root / ".cursor/mcp.json"
        if mcp.is_file():
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", ".cursor/mcp.json"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            if tracked.returncode == 0:
                errors.append(
                    "foss tier: .cursor/mcp.json is tracked — keep live MCP config gitignored"
                )

    if tier == "commercial":
        for rel in (".cursor/BUGBOT.md", ".cursor/environment.json"):
            if not (root / rel).is_file():
                warnings.append(f"commercial tier: {rel} not activated (copy from *.commercial.example)")

    sel = root / ".cursor/stack-selection.json"
    manifest = root / ".cursor/cursor-features.json"
    if sel.is_file() and manifest.is_file():
        try:
            sel_tier = json.loads(read_text(sel)).get("distribution_tier", "foss")
            man_tier = json.loads(read_text(manifest)).get("distribution_tier", "foss")
            if sel_tier != man_tier:
                errors.append("cursor-features.json tier mismatch with stack-selection.json")
            if sel_tier != tier:
                errors.append(f"stack-selection tier {sel_tier} != requested --tier {tier}")
        except json.JSONDecodeError:
            errors.append("invalid stack-selection or cursor-features JSON")

    if tier == "foss":
        for warn in warnings:
            print(f"WARN: {warn}", file=sys.stderr)
    else:
        for warn in warnings:
            print(f"WARN: {warn}", file=sys.stderr)

    return errors


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--tier", default="foss", choices=("foss", "commercial"))
    args = parser.parse_args()
    root = Path(args.root).resolve()

    errors = validate_artifacts(root)
    errors.extend(validate_tier(root, args.tier))

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"Cursor integrations check passed (tier={args.tier})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
