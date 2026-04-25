#!/usr/bin/env python3
"""
generate-sidecars.py — emit tokens.json + tailwind.config.js from a .design.md.

Usage:
    python3 generate-sidecars.py <path-to-design.md> [--out-dir <dir>]

Sidecars are written next to the source unless --out-dir is provided.
Filenames mirror the source basename:
    kindertech-v2.design.md → kindertech-v2.tokens.json + kindertech-v2.tailwind.config.js

Source of truth is the YAML frontmatter block (between --- markers) in the .design.md.
See references/sidecar-contract.md for the full transform spec.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages\n"
    )
    sys.exit(2)


# ─────────────────────────────────────────────────────────────────────────────
# Frontmatter parsing
# ─────────────────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(md_text: str) -> dict:
    """Pull the YAML frontmatter dict out of a .design.md string."""
    match = FRONTMATTER_RE.match(md_text)
    if not match:
        raise ValueError(
            "No YAML frontmatter block found. .design.md must start with --- ... ---"
        )
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"Malformed YAML frontmatter: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must be a mapping at the top level.")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def coerce_dimension(value) -> str:
    """Normalise a dimension value: '16' → '16px', '16px' → '16px'."""
    if isinstance(value, (int, float)):
        return f"{value}px"
    s = str(value).strip()
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return f"{s}px"
    return s


def is_dual_mode_colors(colors: dict) -> bool:
    """Detect whether the colors block uses light:/dark: sub-blocks."""
    if not isinstance(colors, dict):
        return False
    has_modes = any(k in colors for k in ("light", "dark"))
    has_flat = any(
        not isinstance(v, dict) for k, v in colors.items() if k not in ("light", "dark")
    )
    if has_modes and has_flat:
        raise ValueError(
            "colors: block has both flat keys and light:/dark: sub-blocks. "
            "Pick one mode strategy."
        )
    return has_modes


# ─────────────────────────────────────────────────────────────────────────────
# tokens.json emission (W3C-aligned)
# ─────────────────────────────────────────────────────────────────────────────


def colors_to_tokens(colors: dict) -> dict:
    if not colors:
        return {}
    out = {}
    if is_dual_mode_colors(colors):
        for mode in ("light", "dark"):
            if mode not in colors:
                continue
            out[mode] = {
                k: {"$value": v, "$type": "color"} for k, v in colors[mode].items()
            }
    else:
        out["default"] = {
            k: {"$value": v, "$type": "color"} for k, v in colors.items()
        }
    return out


def typography_to_tokens(typography: dict) -> dict:
    if not typography:
        return {}
    out = {}
    for role, props in typography.items():
        if not isinstance(props, dict):
            continue
        token = {}
        if "fontFamily" in props:
            token["fontFamily"] = {
                "$value": props["fontFamily"],
                "$type": "fontFamily",
            }
        if "fontSize" in props:
            token["fontSize"] = {
                "$value": str(props["fontSize"]),
                "$type": "dimension",
            }
        if "fontWeight" in props:
            token["fontWeight"] = {
                "$value": props["fontWeight"],
                "$type": "fontWeight",
            }
        if "lineHeight" in props:
            token["lineHeight"] = {
                "$value": props["lineHeight"],
                "$type": "number",
            }
        if "letterSpacing" in props:
            token["letterSpacing"] = {
                "$value": str(props["letterSpacing"]),
                "$type": "dimension",
            }
        if "textTransform" in props:
            token["textTransform"] = {
                "$value": props["textTransform"],
                "$type": "string",
            }
        out[role] = token
    return out


def dimension_map_to_tokens(block: dict) -> dict:
    if not block:
        return {}
    return {
        k: {"$value": coerce_dimension(v), "$type": "dimension"} for k, v in block.items()
    }


def shadows_to_tokens(shadows: dict) -> dict:
    if not shadows:
        return {}
    return {k: {"$value": v, "$type": "shadow"} for k, v in shadows.items()}


def motion_to_tokens(motion: dict) -> dict:
    if not motion:
        return {}
    out = {}
    for k, v in motion.items():
        if k.startswith("ease"):
            out[k] = {"$value": v, "$type": "cubicBezier"}
        else:
            out[k] = {"$value": coerce_dimension(v) if not str(v).endswith(("ms", "s")) else v, "$type": "duration"}
    return out


def container_to_tokens(container: dict) -> dict:
    if not container:
        return {}
    return {
        k: {"$value": coerce_dimension(v), "$type": "dimension"} for k, v in container.items()
    }


def _json_safe(obj):
    """Recursively coerce YAML-parsed values to JSON-serializable forms.

    Defensive only — the schema convention in sidecar-contract.md requires
    timestamps/dates to be quoted strings in .design.md frontmatter, so this
    branch shouldn't fire in correctly-authored sources. Kept as belt-and-braces
    against schema drift or unusual YAML inputs (sets, tuples in custom tags).
    """
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def build_tokens_json(data: dict) -> dict:
    """Produce the full W3C-aligned tokens.json structure."""
    handled = {"colors", "typography", "rounded", "spacing", "container", "motion", "shadows"}
    extras = {k: _json_safe(v) for k, v in data.items() if k not in handled}

    out = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
    }
    if data.get("colors"):
        out["color"] = colors_to_tokens(data["colors"])
    if data.get("typography"):
        out["typography"] = typography_to_tokens(data["typography"])
    if data.get("rounded"):
        out["borderRadius"] = dimension_map_to_tokens(data["rounded"])
    if data.get("spacing"):
        out["spacing"] = dimension_map_to_tokens(data["spacing"])
    if data.get("shadows"):
        out["shadow"] = shadows_to_tokens(data["shadows"])
    if data.get("motion"):
        out["motion"] = motion_to_tokens(data["motion"])
    if data.get("container"):
        out["container"] = container_to_tokens(data["container"])
    if extras:
        out["extras"] = extras
    return out


# ─────────────────────────────────────────────────────────────────────────────
# tailwind.config.js emission
# ─────────────────────────────────────────────────────────────────────────────


def js_string(s) -> str:
    """Quote a JS string literal safely."""
    if s is None:
        return "''"
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"


def colors_to_tailwind(colors: dict) -> Tuple[dict, Optional[dict], Optional[dict]]:
    """
    Returns (tailwind_colors_dict, css_vars_block_or_None, dark_css_vars_or_None).
    Dual-mode: emit var() references + a CSS custom-properties block (caller writes alongside).
    Single-mode: emit hex values directly.
    """
    if not colors:
        return {}, None, None
    if is_dual_mode_colors(colors):
        tw = {}
        light = colors.get("light", {})
        dark = colors.get("dark", {})
        all_keys = set(light.keys()) | set(dark.keys())
        for k in sorted(all_keys):
            tw[k] = f"var(--color-{k})"
        light_vars = {f"--color-{k}": v for k, v in light.items()}
        dark_vars = {f"--color-{k}": v for k, v in dark.items()}
        return tw, light_vars, dark_vars
    return dict(colors), None, None


def typography_to_tailwind(typography: dict) -> Tuple[dict, dict]:
    """
    Returns (fontSize_dict, fontFamily_dict).
    fontSize values are [size, { lineHeight, letterSpacing, fontWeight }] tuples for Tailwind.
    fontFamily picks unique families and aliases them as 'display' / 'body' / role-named.
    """
    if not typography:
        return {}, {}

    font_size = {}
    families_seen = {}
    for role, props in typography.items():
        if not isinstance(props, dict):
            continue
        size = props.get("fontSize")
        if size is None:
            continue
        meta = {}
        if "lineHeight" in props:
            meta["lineHeight"] = str(props["lineHeight"])
        if "letterSpacing" in props:
            meta["letterSpacing"] = str(props["letterSpacing"])
        if "fontWeight" in props:
            meta["fontWeight"] = str(props["fontWeight"])
        font_size[role] = (str(size), meta)

        family = props.get("fontFamily")
        if family and family not in families_seen.values():
            # First occurrence — assign a Tailwind alias
            alias = "display" if "display" in role or "headline" in role else (
                "body" if family not in families_seen.values() else f"alt-{len(families_seen)}"
            )
            if alias in families_seen:
                alias = f"{alias}-{len(families_seen)}"
            families_seen[alias] = family

    # Heuristic fallback fonts based on family-name keywords
    def fallback_for(family: str) -> list[str]:
        f = family.lower()
        if any(s in f for s in ("serif", "garamond", "fraunces", "playfair", "georgia")):
            return [family, "serif"]
        if "mono" in f or "geist mono" in f or "jetbrains" in f:
            return [family, "monospace"]
        return [family, "sans-serif"]

    font_family = {alias: fallback_for(fam) for alias, fam in families_seen.items()}
    return font_size, font_family


def render_tailwind_config(
    *,
    source_path: str,
    timestamp: str,
    tw_colors: dict,
    css_light_vars: Optional[dict],
    css_dark_vars: Optional[dict],
    font_size: dict,
    font_family: dict,
    rounded: dict,
    spacing: dict,
    shadows: dict,
    motion: dict,
    container: dict,
) -> str:
    lines = [
        "/** @type {import('tailwindcss').Config} */",
        f"/* AUTO-GENERATED from {source_path} on {timestamp}. Do not edit. */",
        "",
    ]
    if css_light_vars or css_dark_vars:
        # Emit the CSS custom-properties block at the top as a comment block
        # so the consumer knows what to put in their globals.css. Tailwind config
        # itself can't inject CSS vars — this is documentation.
        lines.append("/*")
        lines.append(" * Required globals.css companion (dual-mode):")
        lines.append(" *")
        lines.append(" * :root {")
        for k, v in (css_light_vars or {}).items():
            lines.append(f" *   {k}: {v};")
        lines.append(" * }")
        if css_dark_vars:
            lines.append(" * .dark {")
            for k, v in css_dark_vars.items():
                lines.append(f" *   {k}: {v};")
            lines.append(" * }")
        lines.append(" */")
        lines.append("")

    lines.append("export default {")
    lines.append("  content: ['./**/*.{html,js,jsx,ts,tsx}'],")
    dark_mode_value = "'class'" if css_dark_vars else "'media'"
    lines.append(f"  darkMode: {dark_mode_value},")
    lines.append("  theme: {")
    lines.append("    extend: {")

    # colors
    if tw_colors:
        lines.append("      colors: {")
        for k, v in tw_colors.items():
            lines.append(f"        {js_string(k)}: {js_string(v)},")
        lines.append("      },")

    # fontFamily
    if font_family:
        lines.append("      fontFamily: {")
        for alias, stack in font_family.items():
            stack_str = ", ".join(js_string(f) for f in stack)
            lines.append(f"        {js_string(alias)}: [{stack_str}],")
        lines.append("      },")

    # fontSize
    if font_size:
        lines.append("      fontSize: {")
        for role, (size, meta) in font_size.items():
            if meta:
                meta_pairs = ", ".join(f"{k}: {js_string(v)}" for k, v in meta.items())
                lines.append(
                    f"        {js_string(role)}: [{js_string(size)}, {{ {meta_pairs} }}],"
                )
            else:
                lines.append(f"        {js_string(role)}: {js_string(size)},")
        lines.append("      },")

    # borderRadius
    if rounded:
        lines.append("      borderRadius: {")
        for k, v in rounded.items():
            lines.append(f"        {js_string(k)}: {js_string(coerce_dimension(v))},")
        lines.append("      },")

    # spacing
    if spacing:
        lines.append("      spacing: {")
        for k, v in spacing.items():
            lines.append(f"        {js_string(k)}: {js_string(coerce_dimension(v))},")
        lines.append("      },")

    # boxShadow
    if shadows:
        lines.append("      boxShadow: {")
        for k, v in shadows.items():
            lines.append(f"        {js_string(k)}: {js_string(v)},")
        lines.append("      },")

    # transitionDuration / transitionTimingFunction
    if motion:
        durations = {k: v for k, v in motion.items() if not k.startswith("ease")}
        eases = {k.replace("ease-", ""): v for k, v in motion.items() if k.startswith("ease")}
        if durations:
            lines.append("      transitionDuration: {")
            for k, v in durations.items():
                lines.append(f"        {js_string(k)}: {js_string(v)},")
            lines.append("      },")
        if eases:
            lines.append("      transitionTimingFunction: {")
            for k, v in eases.items():
                lines.append(f"        {js_string(k)}: {js_string(v)},")
            lines.append("      },")

    # container
    if container:
        max_width = container.get("max-width")
        padding_x = container.get("padding-x")
        lines.append("      container: {")
        lines.append("        center: true,")
        if padding_x:
            lines.append(f"        padding: {js_string(coerce_dimension(padding_x))},")
        if max_width:
            lines.append("        screens: {")
            lines.append(f"          '2xl': {js_string(coerce_dimension(max_width))},")
            lines.append("        },")
        lines.append("      },")

    lines.append("    },")
    lines.append("  },")
    lines.append("};")
    lines.append("")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser(description="Generate tokens.json + tailwind.config.js from a .design.md")
    ap.add_argument("source", help="Path to .design.md")
    ap.add_argument("--out-dir", default=None, help="Output directory (default: same as source)")
    args = ap.parse_args()

    source = Path(args.source)
    if not source.exists():
        sys.stderr.write(f"ERROR: source not found: {source}\n")
        sys.exit(1)

    text = source.read_text(encoding="utf-8")
    try:
        data = extract_frontmatter(text)
    except ValueError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)

    out_dir = Path(args.out_dir) if args.out_dir else source.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Strip the trailing ".design" off the basename if present so the sidecar
    # filenames don't accumulate extensions: foo.design.md → foo.tokens.json
    stem = source.stem
    if stem.endswith(".design"):
        stem = stem[: -len(".design")]

    tokens_path = out_dir / f"{stem}.tokens.json"
    tailwind_path = out_dir / f"{stem}.tailwind.config.js"

    # Build tokens.json
    tokens = build_tokens_json(data)
    tokens_path.write_text(json.dumps(tokens, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Build tailwind.config.js
    tw_colors, light_vars, dark_vars = colors_to_tailwind(data.get("colors") or {})
    font_size, font_family = typography_to_tailwind(data.get("typography") or {})
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    tailwind_js = render_tailwind_config(
        source_path=str(source.name),
        timestamp=timestamp,
        tw_colors=tw_colors,
        css_light_vars=light_vars,
        css_dark_vars=dark_vars,
        font_size=font_size,
        font_family=font_family,
        rounded=data.get("rounded") or {},
        spacing=data.get("spacing") or {},
        shadows=data.get("shadows") or {},
        motion=data.get("motion") or {},
        container=data.get("container") or {},
    )
    tailwind_path.write_text(tailwind_js, encoding="utf-8")

    print(f"OK {tokens_path}")
    print(f"OK {tailwind_path}")


if __name__ == "__main__":
    main()
