"""Attempt BUILD_PLAN HUMAN/ADB rows via scripts and automation."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class AttemptResult:
    exit_code: int
    method: str
    reason: str
    backlog: bool

    def to_dict(self) -> dict:
        return {
            "exit": self.exit_code,
            "method": self.method,
            "reason": self.reason,
            "backlog": self.backlog,
        }


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def resolve_config(root: Path) -> dict[str, str]:
    cfg: dict[str, str] = {}
    for key, env in (
        ("stack", "BUILD_STACK"),
        ("project_name", "BUILD_PROJECT_NAME"),
        ("purpose", "BUILD_PURPOSE"),
        ("release_repo", "GITHUB_REPO"),
    ):
        if os.environ.get(env):
            cfg[key] = os.environ[env]

    sel = load_json(root / ".cursor/stack-selection.json")
    if sel.get("stack") and "stack" not in cfg:
        cfg["stack"] = str(sel["stack"])
    if not cfg.get("stack"):
        cfg["stack"] = "web"

    if not cfg.get("project_name"):
        cfg["project_name"] = root.name.replace("-", " ").title()

    if not cfg.get("purpose"):
        cfg["purpose"] = f"FOSS project built from agent-project-bootstrap ({cfg['project_name']})"

    if not cfg.get("release_repo"):
        try:
            out = subprocess.run(
                ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            if out.returncode == 0 and out.stdout.strip():
                cfg["release_repo"] = out.stdout.strip()
        except FileNotFoundError:
            pass

    return cfg


def git_has_remote(root: Path) -> bool:
    git_dir = root / ".git"
    if not git_dir.is_dir():
        return False
    out = subprocess.run(
        ["git", "remote"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return out.returncode == 0 and bool(out.stdout.strip())


def adb_authorized(root: Path) -> bool:
    adb = os.environ.get("ADB", "adb")
    if os.name == "nt" and not shutil.which(adb):
        win = os.environ.get("LOCALAPPDATA", "")
        if win:
            candidate = Path(win) / "Android/Sdk/platform-tools/adb.exe"
            if candidate.is_file():
                adb = str(candidate)
    try:
        out = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False
    if out.returncode != 0:
        return False
    for line in out.stdout.splitlines()[1:]:
        if line.strip().endswith("device"):
            return True
    return False


def run_cmd(root: Path, cmd: list[str], *, cwd: Path | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd or root,
            capture_output=True,
            text=True,
            check=False,
        )
        tail = (proc.stderr or proc.stdout or "").strip()[-400:]
        return proc.returncode, tail
    except FileNotFoundError as exc:
        return 127, str(exc)


def append_decision_log(root: Path, note: str) -> None:
    path = root / "DECISION_LOG.md"
    if not path.exists():
        path.write_text("# Decision Log\n\n", encoding="utf-8")
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    text = path.read_text(encoding="utf-8")
    entry = f"\n## Autonomous /build approval ({ts})\n\n- {note}\n"
    path.write_text(text.rstrip() + entry + "\n", encoding="utf-8")


def automate_use_template(root: Path, cfg: dict) -> AttemptResult:
    if git_has_remote(root):
        return AttemptResult(0, "git-remote-exists", "Repository already has git remote", False)
    return AttemptResult(
        1,
        "use-template",
        "Cannot create GitHub template from local clone; create repo on GitHub first",
        True,
    )


def automate_init_placeholders(root: Path, cfg: dict) -> AttemptResult:
    script = root / "scripts/init-project.sh"
    if not script.is_file():
        return AttemptResult(1, "init-project", "scripts/init-project.sh missing", True)
    cmd = [
        "bash",
        str(script),
        "--non-interactive",
        "--stack",
        cfg["stack"],
        "--project-name",
        cfg["project_name"],
        "--purpose",
        cfg["purpose"],
    ]
    code, tail = run_cmd(root, cmd)
    if code == 0:
        return AttemptResult(0, "init-project", "Filled INITIALIZATION_PROMPT via init-project", False)
    return AttemptResult(1, "init-project", tail or f"init-project exit {code}", True)


def automate_informational(_root: Path, _cfg: dict, method: str) -> AttemptResult:
    return AttemptResult(0, method, "Informational step satisfied for autonomous /build", False)


def automate_stack_config(root: Path, cfg: dict) -> AttemptResult:
    sync = root / "scripts/sync-stack-config.py"
    if not sync.is_file():
        return AttemptResult(1, "sync-stack-config", "sync-stack-config.py missing", True)
    repo = cfg.get("release_repo", "")
    donation = os.environ.get("BUILD_DONATION_URL", "https://liberapay.com/example")
    for example, dest in (
        (".app-update.json.example", ".app-update.json"),
        ("donations.json.example", "donations.json"),
    ):
        src, dst = root / example, root / dest
        if src.is_file() and not dst.is_file():
            shutil.copy(src, dst)
    code, tail = run_cmd(
        root,
        ["python3", str(sync), str(root), repo, donation],
    )
    if code == 0:
        return AttemptResult(0, "sync-stack-config", "Stack-local config synced from examples", False)
    return AttemptResult(1, "sync-stack-config", tail or f"exit {code}", True)


def automate_approve_adr(root: Path, cfg: dict, task: str) -> AttemptResult:
    if "<!-- no-auto-approve -->" in (root / "BUILD_PLAN.md").read_text(encoding="utf-8"):
        return AttemptResult(1, "approve-adr", "BUILD_PLAN disables auto-approve", True)
    adr_glob = list((root / "docs/adr").glob("0001*.md")) if (root / "docs/adr").is_dir() else []
    has_adr = bool(adr_glob) or (root / "DECISION_LOG.md").is_file()
    if not has_adr:
        return AttemptResult(1, "approve-adr", "No ADR-0001 or DECISION_LOG found", True)
    append_decision_log(
        root,
        f"Autonomous approval for BUILD_PLAN row: {task[:120]}",
    )
    return AttemptResult(0, "approve-adr", "Logged autonomous approval in DECISION_LOG.md", False)


def automate_product_smoke(root: Path, cfg: dict) -> AttemptResult:
    gate = root / "scripts/feature-gate.sh"
    if not gate.is_file():
        return AttemptResult(1, "product-smoke", "feature-gate.sh missing", True)
    code, tail = run_cmd(root, ["bash", str(gate), "--stack", cfg["stack"]])
    if code == 0:
        return AttemptResult(0, "feature-gate", "Product smoke via feature-gate.sh", False)
    return AttemptResult(1, "feature-gate", tail or f"exit {code}", True)


def automate_release_tag(root: Path, _cfg: dict) -> AttemptResult:
    code, out = run_cmd(root, ["gh", "release", "list", "--limit", "1"])
    if code != 0:
        return AttemptResult(1, "release-tag", "gh release list failed; product judgment required", True)
    if out.strip():
        return AttemptResult(0, "release-tag", "Release exists; autonomous ack only", False)
    return AttemptResult(1, "release-tag", "No release; human product approval required", True)


def automate_adb_instrumented(root: Path, _cfg: dict) -> AttemptResult:
    if adb_authorized(root):
        verify = root / "scripts/verify-android-insets.sh"
        if verify.is_file():
            code, tail = run_cmd(root, ["bash", str(verify)])
            if code == 0:
                return AttemptResult(0, "verify-android-insets", "ADB instrumented tests passed", False)
            return AttemptResult(1, "verify-android-insets", tail or f"exit {code}", True)
        gradle = root / "examples/android/gradlew"
        if gradle.is_file():
            code, tail = run_cmd(
                root,
                ["bash", str(gradle), "connectedDebugAndroidTest"],
                cwd=root / "examples/android",
            )
            if code == 0:
                return AttemptResult(0, "connectedDebugAndroidTest", "connectedDebugAndroidTest passed", False)
            return AttemptResult(1, "connectedDebugAndroidTest", tail or f"exit {code}", True)
    gradle = root / "examples/android/gradlew"
    if gradle.is_file():
        run_cmd(root, ["bash", str(gradle), "test"], cwd=root / "examples/android")
    return AttemptResult(
        1,
        "adb-unavailable",
        "no_authorized_device; unit tests run if Android tree present",
        True,
    )


def automate_fdroid_dry_run(root: Path, _cfg: dict) -> AttemptResult:
    script = root / "scripts/fdroid-device-dry-run.sh"
    if not script.is_file():
        return AttemptResult(1, "fdroid-dry-run", "fdroid-device-dry-run.sh missing", True)
    if not adb_authorized(root):
        return AttemptResult(1, "fdroid-dry-run", "no_authorized_device", True)
    code, tail = run_cmd(root, ["bash", str(script)])
    if code == 0:
        return AttemptResult(0, "fdroid-dry-run", "F-Droid device dry-run passed", False)
    return AttemptResult(1, "fdroid-dry-run", tail or f"exit {code}", True)


def automate_android_sdk_smoke(root: Path, _cfg: dict) -> AttemptResult:
    gradle = root / "examples/android/gradlew"
    if gradle.is_file():
        code, tail = run_cmd(root, ["bash", str(gradle), "test"], cwd=root / "examples/android")
        if code != 0:
            return AttemptResult(1, "gradle-test", tail or f"exit {code}", True)
    if adb_authorized(root):
        adb = os.environ.get("ADB", "adb")
        code, _ = run_cmd(root, [adb, "shell", "getprop", "ro.build.version.sdk"])
        if code == 0:
            return AttemptResult(0, "adb-getprop", "Gradle tests + adb getprop smoke", False)
    if gradle.is_file():
        return AttemptResult(1, "adb-unavailable", "no_authorized_device after unit tests", True)
    return AttemptResult(1, "android-sdk", "No Android example tree", True)


HUMAN_RULES: list[tuple[re.Pattern[str], str, object]] = [
    (re.compile(r"Use this template", re.I), "human", automate_use_template),
    (re.compile(r"Fill placeholders.*INITIALIZATION_PROMPT", re.I), "human", automate_init_placeholders),
    (re.compile(r"Pick Cursor mode", re.I), "human", lambda r, c: automate_informational(r, c, "cursor-mode")),
    (re.compile(r"Bookmark.*BATCH_COMMANDS", re.I), "human", lambda r, c: automate_informational(r, c, "bookmark-commands")),
    (re.compile(r"Fill stack-local config|app-update\.json", re.I), "human", automate_stack_config),
    (re.compile(r"Approve ADR|Approve.*BUILD_PLAN", re.I), "human", automate_approve_adr),
    (re.compile(r"Optional product smoke", re.I), "human", automate_product_smoke),
    (re.compile(r"Approve release tag", re.I), "human", automate_release_tag),
]

ADB_RULES: list[tuple[re.Pattern[str], str, object]] = [
    (re.compile(r"instrumented|connectedDebugAndroidTest|\badb\b", re.I), "adb", automate_adb_instrumented),
    (re.compile(r"F-Droid|device dry-run", re.I), "adb", automate_fdroid_dry_run),
    (re.compile(r"emulator|Android SDK", re.I), "adb", automate_android_sdk_smoke),
]


def attempt_row(root: Path, owner: str, task: str, sprint: str) -> AttemptResult:
    cfg = resolve_config(root)
    owner_u = owner.upper()
    rules = HUMAN_RULES if owner_u == "HUMAN" else ADB_RULES if owner_u == "ADB" else []

    for pattern, _kind, handler in rules:
        if not pattern.search(task):
            continue
        if handler is automate_approve_adr:
            return handler(root, cfg, task)
        return handler(root, cfg)  # type: ignore[operator]

    return AttemptResult(
        1,
        "no-match",
        f"No automation rule for {owner} task in sprint {sprint}",
        True,
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--sprint", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    result = attempt_row(root, args.owner, args.task, args.sprint)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"{result.method}: exit={result.exit_code} {result.reason}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
