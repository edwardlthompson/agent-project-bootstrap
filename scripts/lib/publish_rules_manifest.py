"""Build rules.manifest.json from argus/rules/**."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def _parse_simple_yaml(text: str) -> dict:
    """Minimal YAML subset for rule files when PyYAML is absent."""
    data: dict = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [
                p.strip().strip('"').strip("'")
                for p in inner.split(",")
                if p.strip()
            ]
        elif val in {"true", "false"}:
            data[key] = val == "true"
        elif val.isdigit():
            data[key] = int(val)
        else:
            data[key] = val
    return data


def load_rule(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        loaded = yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}
    return _parse_simple_yaml(text)


def tree_sha256(root: Path) -> str:
    rules_dir = root / "argus" / "rules"
    h = hashlib.sha256()
    for path in sorted(rules_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix().encode()
            h.update(rel)
            h.update(path.read_bytes())
    return h.hexdigest()


def build_manifest(root: Path) -> dict:
    rules_dir = root / "argus" / "rules"
    rules = []
    for path in sorted(rules_dir.glob("*.yaml")):
        data = load_rule(path)
        rules.append(
            {
                "id": data.get("id", path.stem),
                "version": str(data.get("version", "0")),
                "min_contract": data.get("min_contract", 2),
                "stacks": data.get("stacks") or [],
                "fix_class": data.get("fix_class", "agent"),
                "yolo_safe": bool(data.get("yolo_safe", False)),
            }
        )
    contract = {}
    cpath = root / "argus.contract.json"
    if cpath.is_file():
        contract = json.loads(cpath.read_text(encoding="utf-8"))
    return {
        "manifest_version": 1,
        "contract_version": contract.get("contract_version", 2),
        "published": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tree_sha256": tree_sha256(root),
        "rules": rules,
    }


def write_manifest(root: Path) -> Path:
    out = root / "rules.manifest.json"
    out.write_text(
        json.dumps(build_manifest(root), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return out
