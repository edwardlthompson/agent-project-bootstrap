"""Fleet fanout planner — plan-only; never mutates remotes."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

CAPS = {
    "repos_per_brief": 25,
    "waves_per_hour": 3,
    "batch_after_canary": 5,
    "minutes_per_repo": 60,
    "reverts_halt": 2,
}


@dataclass
class Brief:
    brief: str
    kind: str
    scope: str
    verify: str
    verify_timeout_s: int = 120
    auto: bool = False
    touch: list[str] | None = None
    expect_files: str = ""
    reversible: bool = True


def parse_brief(path: Path) -> Brief:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path}: missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: invalid frontmatter")
    meta: dict = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        key = k.strip()
        val = v.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [
                x.strip().strip('"').strip("'")
                for x in val[1:-1].split(",")
                if x.strip()
            ]
        elif val in {"true", "false"}:
            meta[key] = val == "true"
        elif val.isdigit():
            meta[key] = int(val)
        else:
            meta[key] = val.strip('"').strip("'")
    if not meta.get("verify"):
        raise ValueError(f"{path}: verify: is required and must be a command")
    return Brief(
        brief=str(meta.get("brief") or path.stem),
        kind=str(meta.get("kind") or "feature"),
        scope=str(meta.get("scope") or ""),
        verify=str(meta["verify"]),
        verify_timeout_s=int(meta.get("verify_timeout_s") or 120),
        auto=bool(meta.get("auto", False)),
        touch=list(meta.get("touch") or []),
        expect_files=str(meta.get("expect_files") or ""),
        reversible=bool(meta.get("reversible", True)),
    )


def load_fleet(root: Path) -> list[dict]:
    path = root / "fleet.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    repos = data.get("repos") or []
    return [r for r in repos if isinstance(r, dict) and not r.get("archived")]


def select_repos(fleet: list[dict], scope: str) -> list[dict]:
    """scope: tag:web | slug:owner/repo | never 'everything' by default."""
    if scope.startswith("tag:"):
        tag = scope[4:]
        return [r for r in fleet if tag in (r.get("tags") or [])]
    if scope.startswith("slug:"):
        slug = scope[5:]
        return [r for r in fleet if r.get("slug") == slug]
    raise ValueError(f"scope must be tag:… or slug:… (got {scope!r})")


def plan_waves(repos: list[dict], *, auto: bool = False) -> list[list[dict]]:
    """Canary 1, then 3, then batches of 5 (halved when auto)."""
    batch = 3 if auto else CAPS["batch_after_canary"]
    second = 2 if auto else 3
    capped = repos[: CAPS["repos_per_brief"]]
    if not capped:
        return []
    waves: list[list[dict]] = [[capped[0]]]
    rest = capped[1:]
    if rest:
        waves.append(rest[:second])
        rest = rest[second:]
    while rest:
        waves.append(rest[:batch])
        rest = rest[batch:]
    return waves[: CAPS["waves_per_hour"]]


def plan_brief(root: Path, brief_path: Path) -> dict:
    brief = parse_brief(brief_path)
    fleet = load_fleet(root)
    selected = select_repos(fleet, brief.scope)
    waves = plan_waves(selected, auto=brief.auto)
    return {
        "brief": brief.brief,
        "scope": brief.scope,
        "verify": brief.verify,
        "verify_timeout_s": brief.verify_timeout_s,
        "auto": brief.auto,
        "repos": [r.get("slug") for r in selected],
        "waves": [[r.get("slug") for r in w] for w in waves],
        "caps": CAPS,
        "mode": "plan-only",
        "note": "One branch/PR per repo; halt on canary revert; skips are not failures.",
    }
