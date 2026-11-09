"""Layout gate — minimal Part 1 checks from .goldenpath.json."""
from __future__ import annotations

from pathlib import Path

from argus_contract import load_contract
from orphan_gate import load_goldenpath


def check(root: Path) -> tuple[int, str]:
    contract = load_contract(root)
    if contract and contract.get("layout_required") is False:
        # Still verify goldenpath entrypoint dirs when present
        gp = load_goldenpath(root)
        if gp is None:
            return 1, "layout: missing .goldenpath.json"
        for stack, paths in (gp.get("entrypoints") or {}).items():
            if stack not in (gp.get("stacks") or []):
                continue
            for rel in paths:
                path = root / rel
                if not path.exists():
                    # Stack may be pruned on children — soft skip if examples/ gone
                    parent = path.parts[0] if path.parts else ""
                    if parent == "examples" and not (root / "examples" / stack).exists():
                        continue
                    return 1, f"layout: missing entrypoint {rel} for stack {stack}"
        return 0, "OK: layout gate (layout_required=false; goldenpath entrypoints checked)"
    return 0, "OK: layout deferred until docs/LAYOUT.md"
