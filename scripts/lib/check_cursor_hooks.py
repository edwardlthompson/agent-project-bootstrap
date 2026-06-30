"""Validate .cursor/hooks.json and optional smoke tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FORBIDDEN_EVENTS = frozenset(
    {
        "beforeSubmitPrompt",
        "afterAgentThought",
        "preCompact",
    }
)

REQUIRED_HOOKS = (
    "sessionStart",
    "beforeShellExecution",
    "afterFileEdit",
    "subagentStart",
    "beforeMCPExecution",
)


def hooks_disabled(root: Path) -> bool:
    bp = root / "BUILD_PLAN.md"
    if not bp.is_file():
        return False
    return "<!-- cursor-hooks: off -->" in bp.read_text(encoding="utf-8")


def load_hooks(root: Path) -> dict:
    path = root / ".cursor/hooks.json"
    if not path.is_file():
        raise FileNotFoundError("missing .cursor/hooks.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError("hooks.json version must be 1")
    return data


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if hooks_disabled(root):
        return errors
    try:
        data = load_hooks(root)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]

    hooks = data.get("hooks") or {}
    for event in hooks:
        if event in FORBIDDEN_EVENTS:
            errors.append(f"forbidden hook event: {event}")

    for event in REQUIRED_HOOKS:
        entries = hooks.get(event) or []
        if not entries:
            errors.append(f"missing hook event: {event}")
            continue
        for entry in entries:
            cmd = entry.get("command", "")
            script = root / cmd
            if not script.is_file():
                errors.append(f"hook script missing: {cmd}")

    return errors


def run_guard(root: Path, command: str) -> dict:
    payload = json.dumps({"command": command})
    proc = subprocess.run(
        ["bash", ".cursor/hooks/before-shell-guard.sh"],
        input=payload,
        capture_output=True,
        text=True,
        cwd=root.as_posix(),
        check=False,
    )
    if proc.returncode != 0 and proc.stdout.strip():
        pass
    out = proc.stdout.strip() or proc.stderr.strip()
    if not out:
        return {"permission": "allow"}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"permission": "allow"}


def smoke(root: Path) -> list[str]:
    errors: list[str] = []
    if hooks_disabled(root):
        return errors
    allow = run_guard(root, "git status")
    if allow.get("permission") == "deny":
        errors.append("smoke: git status should be allowed")

    deny = run_guard(root, "git push origin main")
    if deny.get("permission") != "deny":
        errors.append("smoke: git push should be denied without session approval")

    state = root / ".cursor-session-state.json"
    backup = None
    if state.is_file():
        backup = state.read_text(encoding="utf-8")
    try:
        state.write_text(
            json.dumps({"destructive_ops_approved": ["git push"]}, indent=2) + "\n",
            encoding="utf-8",
        )
        ok = run_guard(root, "git push origin main")
        if ok.get("permission") != "allow":
            errors.append("smoke: git push should be allowed with destructive_ops_approved")
    finally:
        if backup is None:
            if state.is_file():
                state.unlink()
        else:
            state.write_text(backup, encoding="utf-8")

    return errors


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    errors = validate(root)
    if args.smoke:
        errors.extend(smoke(root))

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("Cursor hooks check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
