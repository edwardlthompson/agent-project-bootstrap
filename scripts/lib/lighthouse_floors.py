"""Keep Lighthouse accessibility and best-practices floors from regressing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FLOORS = {
    "categories:accessibility": 0.95,
    "categories:best-practices": 0.9,
}


def check(root: Path) -> list[str]:
    path = root / "examples/web/.lighthouserc.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    assertions = data.get("ci", {}).get("assert", {}).get("assertions", {})
    errors: list[str] = []
    for key, floor in FLOORS.items():
        spec = assertions.get(key)
        if not isinstance(spec, list) or len(spec) < 2 or spec[0] != "error":
            errors.append(f"{key} must be an error assertion")
            continue
        score = spec[1].get("minScore") if isinstance(spec[1], dict) else None
        if not isinstance(score, (int, float)) or score < floor:
            errors.append(f"{key} minScore must be >= {floor}, got {score}")
    return errors


def main() -> int:
    errors = check(Path.cwd())
    if errors:
        print("\n".join(errors))
        return 1
    print("Lighthouse a11y and best-practices floors passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
