#!/usr/bin/env python3
"""Generate platform design outputs from design-tokens/design-tokens.json."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HEADER = "GENERATED — do not edit; run scripts/sync-design-tokens.py"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_tokens(root: Path) -> dict:
    path = root / "design-tokens" / "design-tokens.json"
    return json.loads(path.read_text(encoding="utf-8"))


def token_hash(tokens: dict) -> str:
    raw = json.dumps(tokens, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def hex_to_compose(name: str, hex_color: str, *, private: bool = False) -> str:
    h = hex_color.lstrip("#")
    prefix = "private val " if private else "val "
    return f"{prefix}{name} = Color(0xFF{h.upper()})"


def camel_case(key: str) -> str:
    parts = key.replace("-", "_").split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def color_role_name(key: str) -> str:
    return camel_case(key)


def generate_css(tokens: dict, digest: str) -> str:
    colors = tokens["color"]
    spacing = tokens["spacing"]
    radius = tokens["radius"]
    typo = tokens["typography"]
    meta = tokens["meta"]

    def vars_block(mode: str) -> list[str]:
        lines = []
        for key, value in colors.items():
            css_key = key.replace("on", "on-").replace("Variant", "-variant")
            css_key = "--gp-color-" + _kebab(key)
            lines.append(f"  {css_key}: {value[mode]};")
        for key, value in spacing.items():
            lines.append(f"  --gp-space-{key}: {value}px;")
        for key, value in radius.items():
            lines.append(f"  --gp-radius-{key}: {value}px;")
        lines.append(f"  --gp-font-sans: {typo['fontFamily']['sans']};")
        for scale_key, scale in typo["scale"].items():
            kebab = _kebab(scale_key)
            lines.append(f"  --gp-text-{kebab}-size: {scale['sizeRem']}rem;")
            lines.append(f"  --gp-text-{kebab}-line: {scale['lineHeight']};")
            lines.append(f"  --gp-text-{kebab}-weight: {scale['weight']};")
        return lines

    light_lines = vars_block("light")
    dark_lines = vars_block("dark")

    parts = [
        f"/* {HEADER} */",
        f"/* source-hash: {digest} */",
        "",
        ":root,",
        '[data-theme="light"] {',
        *light_lines,
        "}",
        "",
        '[data-theme="dark"] {',
        *dark_lines,
        "}",
        "",
        '[data-theme="system"] {',
        *light_lines,
        "}",
        "",
        "@media (prefers-color-scheme: dark) {",
        '  [data-theme="system"] {',
        *dark_lines,
        "  }",
        "}",
        "",
    ]
    return "\n".join(parts)


def _kebab(key: str) -> str:
    out: list[str] = []
    for i, ch in enumerate(key):
        if ch.isupper() and i > 0:
            out.append("-")
        out.append(ch.lower())
    return "".join(out)


def generate_color_kt(tokens: dict, digest: str) -> str:
    colors = tokens["color"]
    light_entries = []
    dark_entries = []
    for key in colors:
        role = color_role_name(key)
        light_entries.append(hex_to_compose(f"Light{role.capitalize() if role[0].islower() else role}", colors[key]["light"]))
        dark_entries.append(hex_to_compose(f"Dark{role[0].upper()}{role[1:]}" if role else role, colors[key]["dark"]))

    # Fix naming: primary -> LightPrimary, DarkPrimary
    light_vals = []
    dark_vals = []
    scheme_light = []
    scheme_dark = []
    for key in colors:
        role = color_role_name(key)
        light_name = f"Gp{role[0].upper()}{role[1:]}"
        dark_name = light_name
        light_vals.append(hex_to_compose(f"GpLight{role[0].upper()}{role[1:]}", colors[key]["light"]))
        dark_vals.append(hex_to_compose(f"GpDark{role[0].upper()}{role[1:]}", colors[key]["dark"]))
        scheme_light.append(f"        {role} = GpLight{role[0].upper()}{role[1:]},")
        scheme_dark.append(f"        {role} = GpDark{role[0].upper()}{role[1:]},")

    lines = [
        f"// {HEADER}",
        f"// source-hash: {digest}",
        "package dev.foss.goldenpath.ui.theme",
        "",
        "import androidx.compose.material3.darkColorScheme",
        "import androidx.compose.material3.lightColorScheme",
        "import androidx.compose.ui.graphics.Color",
        "",
        "// Raw palette",
    ]
    for key in colors:
        role = color_role_name(key)
        cap = role[0].upper() + role[1:]
        lines.append(hex_to_compose(f"GpLight{cap}", colors[key]["light"], private=True))
        lines.append(hex_to_compose(f"GpDark{cap}", colors[key]["dark"], private=True))
    lines.extend([
        "",
        "val LightGoldenPathColors = lightColorScheme(",
        *[f"    {color_role_name(k)} = GpLight{color_role_name(k)[0].upper()}{color_role_name(k)[1:]}," for k in colors],
        ")",
        "",
        "val DarkGoldenPathColors = darkColorScheme(",
        *[f"    {color_role_name(k)} = GpDark{color_role_name(k)[0].upper()}{color_role_name(k)[1:]}," for k in colors],
        ")",
        "",
    ])
    return "\n".join(lines)


def generate_type_kt(tokens: dict, digest: str) -> str:
    scale = tokens["typography"]["scale"]
    entries = []
    for key, val in scale.items():
        entries.append(
            f"    {key} = TextStyle(\n"
            f"        fontSize = {val['sizeSp']}.sp,\n"
            f"        lineHeight = {(val['sizeSp'] * val['lineHeight']):.1f}.sp,\n"
            f"        fontWeight = FontWeight({val['weight']}),\n"
            f"    ),"
        )
    return "\n".join([
        f"// {HEADER}",
        f"// source-hash: {digest}",
        "package dev.foss.goldenpath.ui.theme",
        "",
        "import androidx.compose.material3.Typography",
        "import androidx.compose.ui.text.TextStyle",
        "import androidx.compose.ui.text.font.FontWeight",
        "import androidx.compose.ui.unit.sp",
        "",
        "val GoldenPathTypography = Typography(",
        *entries,
        ")",
        "",
    ])


def generate_dimens_kt(tokens: dict, digest: str) -> str:
    spacing = tokens["spacing"]
    radius = tokens["radius"]
    elevation = tokens["elevation"]
    lines = [
        f"// {HEADER}",
        f"// source-hash: {digest}",
        "package dev.foss.goldenpath.ui.theme",
        "",
        "import androidx.compose.ui.unit.dp",
        "",
    ]
    for key, val in spacing.items():
        name = key[0].upper() + key[1:]
        lines.append(f"val Spacing{name} = {val}.dp")
    lines.append("")
    for key, val in radius.items():
        name = key[0].upper() + key[1:]
        lines.append(f"val Radius{name} = {val}.dp")
    lines.append("")
    for key, val in elevation.items():
        name = key.replace("level", "Level")
        lines.append(f"val Elevation{name} = {val}.dp")
    lines.append("")
    return "\n".join(lines)


def generate_theme_meta(tokens: dict) -> str:
    meta = tokens["meta"]
    payload = {
        "themeColorLight": meta["themeColorLight"],
        "themeColorDark": meta["themeColorDark"],
        "name": meta["name"],
    }
    return json.dumps(payload, indent=2) + "\n"


def write_outputs(root: Path) -> None:
    tokens = load_tokens(root)
    digest = token_hash(tokens)

    web_css = root / "examples" / "web" / "src" / "design-tokens.css"
    theme_meta = root / "examples" / "web" / "src" / "theme-meta.json"
    android_theme = root / "examples" / "android" / "app" / "src" / "main" / "java" / "dev" / "foss" / "goldenpath" / "ui" / "theme"

    web_css.parent.mkdir(parents=True, exist_ok=True)
    android_theme.mkdir(parents=True, exist_ok=True)

    web_css.write_text(generate_css(tokens, digest), encoding="utf-8")
    theme_meta.write_text(generate_theme_meta(tokens), encoding="utf-8")
    (android_theme / "Color.kt").write_text(generate_color_kt(tokens, digest), encoding="utf-8")
    (android_theme / "Type.kt").write_text(generate_type_kt(tokens, digest), encoding="utf-8")
    (android_theme / "Dimens.kt").write_text(generate_dimens_kt(tokens, digest), encoding="utf-8")

    print(f"Synced design tokens (hash {digest})")


def main() -> None:
    root = repo_root()
    if not (root / "design-tokens" / "design-tokens.json").is_file():
        print("Missing design-tokens/design-tokens.json", file=sys.stderr)
        sys.exit(1)
    write_outputs(root)


if __name__ == "__main__":
    main()
