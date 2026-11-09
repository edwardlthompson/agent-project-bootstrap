"""UX contract gate with optional baseline + fixture admission."""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE_EXCLUDES = (
    "**/*.md",
    "*.mdx",
    "*.txt",
    "LICENSE*",
    "docs/**",
    ".cursor/rules/**",
)

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_baseline(root: Path) -> dict:
    path = root / "ux-baseline.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _load_rule(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    data: dict = {"fixtures": {}}
    for raw in text.splitlines():
        if ":" not in raw or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        k, _, v = raw.partition(":")
        key = k.strip()
        val = v.strip().strip('"').strip("'")
        if indent >= 2 and key in {"pass", "fail"}:
            fixtures = data.get("fixtures")
            if not isinstance(fixtures, dict):
                data["fixtures"] = {}
            data["fixtures"][key] = val
        elif indent == 0:
            # Mapping keys with empty values (e.g. `fixtures:`) stay dicts.
            if not val and key == "fixtures":
                data["fixtures"] = {}
            else:
                data[key] = val
    return data


def admit_fixtures(root: Path) -> list[str]:
    """Every rule must have pass+fail fixtures; fail fixture must match pattern."""
    errors: list[str] = []
    rules_dir = root / "argus" / "ux" / "rules"
    if not rules_dir.is_dir():
        return errors
    for path in sorted(rules_dir.glob("*.yaml")):
        rule = _load_rule(path)
        fixtures = rule.get("fixtures") or {}
        if not isinstance(fixtures, dict):
            errors.append(f"{path.name}: fixtures must be a mapping")
            continue
        for kind in ("pass", "fail"):
            rel = fixtures.get(kind)
            if not rel:
                errors.append(f"{path.name}: missing fixtures.{kind}")
                continue
            fpath = root / str(rel)
            if not fpath.is_file():
                errors.append(f"{path.name}: missing fixture file {rel}")
                continue
            pattern = rule.get("pattern")
            if not pattern:
                continue
            # Unescape common YAML double-backslashes for regex
            pat = str(pattern).replace("\\\\", "\\")
            text = fpath.read_text(encoding="utf-8")
            matched = re.search(pat, text) is not None
            if kind == "fail" and not matched:
                errors.append(f"{path.name}: fail fixture does not match pattern")
            if kind == "pass" and matched:
                errors.append(f"{path.name}: pass fixture unexpectedly matches pattern")
    return errors


def scan_findings(root: Path) -> list[dict]:
    """Part 2: fixture admission only in-repo; product scan expands later."""
    _ = root
    return []


def markdown_excluded(path: Path) -> bool:
    name = path.name.lower()
    if name.endswith(".md") or name.endswith(".mdx") or name.endswith(".txt"):
        return True
    parts = {p.lower() for p in path.parts}
    if "docs" in parts or ".cursor" in parts and "rules" in parts:
        return True
    if name.startswith("license"):
        return True
    return False


def check(root: Path, *, use_baseline: bool = True) -> tuple[int, str]:
    admit_errs = admit_fixtures(root)
    if admit_errs:
        return 1, "UX fixture admission failed: " + "; ".join(admit_errs)
    baseline = load_baseline(root) if use_baseline else {}
    findings = scan_findings(root)
    if not findings:
        if baseline == {}:
            return 0, "OK: ux fixtures admitted; ux-baseline.json empty (no baseline yet)"
        return 0, "OK: no UX findings"
    open_findings = [f for f in findings if f.get("id") not in baseline]
    if not open_findings:
        return 0, f"OK: {len(findings)} UX finding(s) baselined"
    return 1, f"UX drift: {len(open_findings)} new finding(s)"
