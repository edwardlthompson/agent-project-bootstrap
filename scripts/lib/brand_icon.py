"""Brand icon resolution and gate helpers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PLACEHOLDER_BYTES = 400
TEMPLATE_STOCK_SHA256 = (
    "ec5e9f9a50291c3e9833cfc1e7bcda87954097bebe26726bb63b0922a9461f99"
)
ECOSYSTEM_HINTS = (
    "examples/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png",
    "examples/web/public/icon-512.png",
    "public/manifest.webmanifest",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_brand(root: Path) -> dict | None:
    path = root / "branding" / "brand.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def resolve_icon(root: Path) -> Path | None:
    brand = load_brand(root)
    if brand and brand.get("icon"):
        candidate = root / str(brand["icon"])
        if candidate.is_file():
            return candidate
    canonical = root / "branding" / "assets" / "app-icon-1024.png"
    if canonical.is_file():
        return canonical
    for rel in ECOSYSTEM_HINTS:
        path = root / rel
        if path.is_file() and path.suffix.lower() in {".png", ".ico", ".icns"}:
            return path
    return None


def classify(root: Path) -> tuple[str, str]:
    """Return (state, message). States: owned|inherited|missing|placeholder."""
    icon = resolve_icon(root)
    if icon is None:
        return "missing", "BRAND-ICON-MISSING: no resolvable app icon PNG"
    size = icon.stat().st_size
    if icon.suffix.lower() == ".svg" or size < PLACEHOLDER_BYTES:
        return (
            "placeholder",
            f"BRAND-ICON-PLACEHOLDER: {icon.as_posix()} is stub/under {PLACEHOLDER_BYTES} bytes",
        )
    digest = sha256_file(icon)
    brand = load_brand(root)
    if brand and str(brand.get("icon_sha256", "")).lower() != digest:
        return (
            "placeholder",
            f"brand.json icon_sha256 mismatch for {icon.as_posix()}",
        )
    if digest == TEMPLATE_STOCK_SHA256 and brand and brand.get("source") != "owned":
        return "inherited", "BRAND-ICON-INHERITED: icon_sha256 still matches template stock"
    # Template repo itself is owned stock
    if digest == TEMPLATE_STOCK_SHA256:
        product = root / "branding" / "product.json"
        if product.is_file():
            try:
                mode = json.loads(product.read_text(encoding="utf-8")).get("mode")
            except json.JSONDecodeError:
                mode = None
            if mode == "template":
                return "owned", f"OK: template stock icon ({icon.as_posix()})"
        return "inherited", "BRAND-ICON-INHERITED: replace icon and update icon_sha256"
    return "owned", f"OK: owned icon ({icon.as_posix()})"


def check(root: Path) -> tuple[int, str]:
    state, msg = classify(root)
    brand = load_brand(root)
    if brand is None:
        return 1, "missing branding/brand.json"
    if state in {"missing", "placeholder", "inherited"}:
        return 1, msg
    return 0, msg
