"""Map BUILD_PLAN task text to sprint-smoke probe names."""
from __future__ import annotations

import re
from typing import Iterable

from sprint_smoke_parse import SmokeItem

WORDS: dict[str, tuple[str, ...]] = {
    "web": (
        "web",
        "chrome",
        "lighthouse",
        "snapshot",
        "locale",
        "i18n",
        "vite",
        "playwright",
        "tokeniz",
        "empty state",
        "in-panel",
    ),
    "android": (
        "android",
        "compose",
        "talkback",
        "r8",
        "fdroid",
        "apk",
        "gradle",
        "unifiedpush",
        "rtl",
        "instrumented",
        "nav-stack",
        "runtime-budget",
    ),
    "node": ("node", "openapi spec", "hono"),
    "python": ("python", "mypy", "--feedback"),
    "rust": ("rust", "cargo.toml"),
    "go": (" go", "golang", "/module"),
    "lightroom": ("lightroom", "lua", "lr*"),
    "docs": (
        "docs/",
        "module.md",
        "catalog",
        "adr",
        "tour",
        "coach",
        "skill",
        "runbook",
        "winget",
        "dependabot",
        "scorecard",
        "semgrep",
        "nix",
        "radar",
        "ci-gap",
        "grok",
        "cursor",
        "automations",
        "canvas",
        "template-gap",
        "fastlane",
        "antifeatures",
        "signing",
        "glitchtip",
        "sanitizer",
        "automerge",
    ),
}

_BACKTICK = re.compile(r"`([^`]+)`")


def infer_probes(task: str) -> list[str]:
    lower = f" {task.lower()} "
    found: list[str] = []
    for name, needles in WORDS.items():
        if any(n in lower for n in needles):
            found.append(name)
    if "openapi" in lower and "python" in lower and "node" not in found:
        found.append("python")
    if "openapi" in lower and "node" in lower and "node" not in found:
        found.append("node")
    if not found:
        found.append("docs")
    # Preserve order, unique
    return list(dict.fromkeys(found))


def probes_for_items(items: Iterable[SmokeItem]) -> dict[str, list[str]]:
    return {f"{item.number}:{item.task}": infer_probes(item.task) for item in items}


def backtick_paths(task: str) -> list[str]:
    paths: list[str] = []
    for raw in _BACKTICK.findall(task):
        text = raw.strip()
        if "/" in text or text.endswith((".md", ".json", ".yml", ".yaml", ".html")):
            paths.append(text.split()[0])
    return paths
