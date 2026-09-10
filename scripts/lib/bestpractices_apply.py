"""Print bestpractices.dev as=edit URLs from .bestpractices.json."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[2]
REPO = "https://github.com/edwardlthompson/agent-project-bootstrap"
BASE = "https://www.bestpractices.dev/en/projects"
JUSTIFY_MAX = 80
PASSING_PREFIXES = (
    "description_good",
    "interact",
    "contribution",
    "documentation_basics",
    "documentation_interface",
    "english",
    "maintained",
    "repo_interim",
    "version_",
    "release_notes",
    "report_",
    "enhancement_responses",
    "vulnerability_report",
    "build",
    "test",
    "warnings",
    "crypto_",
    "delivery_",
    "vulnerabilities_",
    "no_leaked",
    "static_analysis",
    "dynamic_analysis",
    "homepage_url",
)


def form_key(key: str) -> str:
    return key.lower().replace("-", "_").replace(".", "_")


def section_for(key: str) -> str | None:
    if key.startswith("OSPS-") or key.startswith("osps_"):
        return "baseline-1"
    if key.startswith(("code_of_conduct", "documentation_security", "documentation_quick")):
        return "silver"
    if key == "homepage_url" or any(key.startswith(p) for p in PASSING_PREFIXES):
        return "passing"
    return None


def proposals(data: dict, section: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, raw in data.items():
        if section_for(key) != section:
            continue
        value = "" if raw is None else str(raw).strip()
        if not value or value in {"?", "unknown"}:
            continue
        if key.endswith("_justification") and len(value) > JUSTIFY_MAX:
            value = value[: JUSTIFY_MAX - 1] + "…"
        out[form_key(key)] = value
    return out


def apply_url(section: str, fields: dict[str, str]) -> str:
    query = {"as": "edit", "section": section, "url": REPO}
    query.update(fields)
    return f"{BASE}?{urlencode(query)}"


def load(root: Path | None = None) -> dict:
    path = (root or ROOT) / ".bestpractices.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main() -> int:
    data = load()
    for section in ("passing", "baseline-1", "silver"):
        fields = proposals(data, section)
        print(f"# {section} ({len(fields)} fields)")
        print(apply_url(section, fields))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
