#!/usr/bin/env python3
"""Compare source/output media and interaction component fingerprints for L-22.

This is a deterministic helper for the AI pre-treatment skill. It does not
decide whether a changed component is acceptable; it inventories the component
surface and fails on unexplained deltas so the manifest must cite an L-rule
when the skill intentionally changed a component.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


MEDIA_TAGS = {"img", "picture", "source", "video", "audio", "svg", "canvas", "iframe"}
INTERESTING_STYLE_PROPS = {
    "object-fit",
    "object-position",
    "background-image",
    "background-size",
    "background-position",
    "width",
    "height",
    "aspect-ratio",
    "overflow",
    "transform",
    "transition",
    "opacity",
    "filter",
    "clip-path",
}
INTERESTING_ATTRS = {
    "src",
    "srcset",
    "sizes",
    "poster",
    "data-src",
    "data-w-id",
    "href",
    "style",
}
EVENT_ATTR_RE = re.compile(r"^on(?:mouse|pointer|mouseenter|mouseleave|mouseover|mouseout|mousemove|click)", re.I)
HOVER_MOUSE_RE = re.compile(r"(?:hover|mouse|pointer)", re.I)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
IGNORED_OUTPUT_HOST_CLASSES = {"fb-custom-code", "fb-runtime"}
ASSET_REF_ATTRS = {"src", "srcset", "poster", "data-src", "href"}
SRCSET_DESCRIPTOR_RE = re.compile(r"^(?:\d+(?:\.\d+)?w|\d+(?:\.\d+)?x)$")


@dataclass
class ComponentFinding:
    file: str
    tag: str
    classes: tuple[str, ...]
    attrs: dict[str, str]
    style_props: dict[str, str]

    def key(self) -> str:
        payload = {
            "tag": self.tag,
            "classes": self.classes,
            "attrs": self.attrs,
            "style": self.style_props,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass
class ComponentParser(HTMLParser):
    file_path: str
    findings: list[ComponentFinding] = field(default_factory=list)
    _skip_depth: int = 0

    def __post_init__(self) -> None:
        super().__init__(convert_charrefs=True)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth and tag.lower() not in VOID_TAGS:
            self._skip_depth -= 1

    def _handle_tag(self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool) -> None:
        tag = tag.lower()
        attr = {name.lower(): value or "" for name, value in attrs}
        classes = tuple(cls for cls in attr.get("class", "").split() if not cls.startswith("fb-"))

        starts_ignored_host = bool(IGNORED_OUTPUT_HOST_CLASSES & set(attr.get("class", "").split()))
        if starts_ignored_host and not self_closing and tag not in VOID_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            if not self_closing and tag not in VOID_TAGS:
                self._skip_depth += 1
            return

        style_props = interesting_style_props(attr.get("style", ""))
        interesting_attrs = {
            name: value
            for name, value in attr.items()
            if name in INTERESTING_ATTRS or EVENT_ATTR_RE.match(name)
        }
        interesting_attrs = normalize_attrs(interesting_attrs)
        interesting = (
            tag in MEDIA_TAGS
            or bool(style_props)
            or "data-w-id" in attr
            or any(EVENT_ATTR_RE.match(name) for name in attr)
            or any(HOVER_MOUSE_RE.search(cls) for cls in classes)
        )
        if interesting:
            self.findings.append(
                ComponentFinding(
                    file=self.file_path,
                    tag=tag,
                    classes=classes,
                    attrs=interesting_attrs,
                    style_props=style_props,
                )
            )


def interesting_style_props(style: str) -> dict[str, str]:
    props: dict[str, str] = {}
    for raw in style.split(";"):
        if ":" not in raw:
            continue
        name, value = raw.split(":", 1)
        name = name.strip().lower()
        if name in INTERESTING_STYLE_PROPS:
            props[name] = normalize_css_value(value)
    return props


def normalize_css_value(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def normalize_attrs(attrs: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for name, value in attrs.items():
        if name.startswith("data-flowbridge-"):
            continue
        if name == "style":
            out[name] = normalize_css_value(value)
        elif name == "srcset":
            out[name] = normalize_srcset(value)
        elif name in ASSET_REF_ATTRS:
            out[name] = normalize_asset_ref(value)
        else:
            out[name] = value.strip()
    if out.get("src") == out.get("data-src"):
        # L-5 materializes lazy sources. Keep data-src as the identity anchor,
        # and do not make the added src a component-fidelity delta.
        out.pop("src", None)
    return out


def normalize_asset_ref(value: str) -> str:
    value = value.strip()
    split = urlsplit(value)
    if split.scheme or value.startswith(("#", "//")):
        return value
    path = unquote(split.path)
    normalized_path = re.sub(r"[\s_()\-]+", "-", path).casefold()
    suffix = ""
    if split.query:
        suffix += f"?{split.query}"
    if split.fragment:
        suffix += f"#{split.fragment}"
    return normalized_path + suffix


def normalize_srcset(value: str) -> str:
    parts: list[str] = []
    for raw in value.split(","):
        candidate = raw.strip()
        if not candidate:
            continue
        bits = candidate.rsplit(None, 1)
        if len(bits) == 2 and SRCSET_DESCRIPTOR_RE.match(bits[1]):
            parts.append(f"{normalize_asset_ref(bits[0])} {bits[1]}")
        else:
            parts.append(normalize_asset_ref(candidate))
    return ", ".join(parts)


def iter_html_files(root: Path) -> list[tuple[str, str]]:
    if root.is_file() and root.suffix.lower() == ".zip":
        out: list[tuple[str, str]] = []
        with zipfile.ZipFile(root) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith(".html"):
                    out.append((name, archive.read(name).decode("utf-8", errors="replace")))
        return out
    if root.is_file():
        return [(str(root), root.read_text(encoding="utf-8", errors="replace"))]
    out = []
    for path in sorted(root.rglob("*.html")):
        out.append((str(path.relative_to(root)), path.read_text(encoding="utf-8", errors="replace")))
    return out


def inventory(root: Path) -> list[ComponentFinding]:
    findings: list[ComponentFinding] = []
    for file_path, text in iter_html_files(root):
        parser = ComponentParser(file_path)
        parser.feed(text)
        findings.extend(parser.findings)
    return findings


def compare(source_root: Path, output_root: Path) -> dict[str, Any]:
    source_findings = inventory(source_root)
    output_findings = inventory(output_root)
    source_counts = Counter(finding.key() for finding in source_findings)
    output_counts = Counter(finding.key() for finding in output_findings)
    missing = source_counts - output_counts
    added = output_counts - source_counts
    return {
        "sourceCount": len(source_findings),
        "outputCount": len(output_findings),
        "missingCount": sum(missing.values()),
        "addedCount": sum(added.values()),
        "missingSamples": sample_counter(missing),
        "addedSamples": sample_counter(added),
    }


def sample_counter(counter: Counter[str]) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for key, count in counter.most_common(8):
        samples.append({"count": count, "fingerprint": json.loads(key)})
    return samples


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        source = base / "source"
        good = base / "good"
        bad = base / "bad"
        for path in (source, good, bad):
            path.mkdir()
        (source / "index.html").write_text(
            '<main><img class="hero-img" src="images/a.jpg" style="object-fit: cover; width: 100%; height: 100%"></main>',
            encoding="utf-8",
        )
        (good / "index.html").write_text(
            '<div class="fb-page-wrapper"><div class="fb-custom-code" style="display:none"><style>.x{}</style></div>'
            '<main><img class="hero-img" src="images/a.jpg" style="object-fit: cover; width: 100%; height: 100%"></main></div>',
            encoding="utf-8",
        )
        (bad / "index.html").write_text(
            '<div class="fb-page-wrapper"><main><img class="hero-img" src="images/a.jpg" '
            'style="object-fit: contain; width: 100%; height: 100%"></main></div>',
            encoding="utf-8",
        )
        good_result = compare(source, good)
        bad_result = compare(source, bad)
        assert good_result["missingCount"] == 0 and good_result["addedCount"] == 0
        assert bad_result["missingCount"] == 1 and bad_result["addedCount"] == 1
    print("component-fidelity self-test: PASS")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare FlowBridge L-22 component fidelity fingerprints.")
    parser.add_argument("--source-root", type=Path, help="Raw source export folder, HTML file, or ZIP.")
    parser.add_argument("--output-root", type=Path, help="Pretreated output folder, HTML file, or ZIP.")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        return run_self_test()
    if not args.source_root or not args.output_root:
        raise SystemExit("Provide --source-root/--output-root or --self-test.")
    result = compare(args.source_root, args.output_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["missingCount"] == 0 and result["addedCount"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
