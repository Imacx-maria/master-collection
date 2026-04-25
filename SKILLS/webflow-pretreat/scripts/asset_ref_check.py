#!/usr/bin/env python3
"""Parser-backed local asset reference checker for Codex pre-treatment runs."""

from __future__ import annotations

import argparse
import html.parser
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


ASSET_ATTRS = {
    "src",
    "href",
    "poster",
    "data-src",
    "data-poster",
    "data-bg",
    "data-background",
}
SRCSET_ATTRS = {"srcset", "data-srcset"}
FLOWBRIDGE_MARKER_PREFIX = "data-flowbridge-inline-"
CSS_URL_RE = re.compile(r"url\\(\\s*(['\"]?)(.*?)\\1\\s*\\)", re.IGNORECASE | re.DOTALL)
SRCSET_DESCRIPTOR_RE = re.compile(r"^(?:\d+(?:\.\d+)?w|\d+(?:\.\d+)?x)$")


@dataclass
class Ref:
    kind: str
    value: str
    location: str


def is_external_or_nonfile(value: str) -> bool:
    value = value.strip()
    if not value:
        return True
    lower = value.lower()
    if lower.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "blob:")):
        return True
    if lower.startswith("//"):
        return True
    scheme = urlsplit(value).scheme.lower()
    return scheme in {"http", "https"}


def normalize_local_ref(value: str) -> str | None:
    value = value.strip().strip("'\"")
    if is_external_or_nonfile(value):
        return None
    split = urlsplit(value)
    path = unquote(split.path)
    if not path or path == "/":
        return None
    return path.lstrip("/")


def parse_srcset(value: str) -> list[str]:
    refs: list[str] = []
    for part in value.split(","):
        candidate = part.strip()
        if not candidate:
            continue
        bits = candidate.rsplit(None, 1)
        if len(bits) == 2 and SRCSET_DESCRIPTOR_RE.match(bits[1]):
            refs.append(bits[0])
        else:
            refs.append(candidate)
    return refs


class AssetRefParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[Ref] = []
        self.style_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs if name}
        if tag.lower() == "style":
            self.style_depth += 1
        for name, value in attr_map.items():
            if value is None:
                continue
            if name.startswith(FLOWBRIDGE_MARKER_PREFIX):
                continue
            if name in ASSET_ATTRS:
                self.refs.append(Ref(name, value, self.getpos_label(tag, name)))
            elif name in SRCSET_ATTRS:
                for src in parse_srcset(value):
                    self.refs.append(Ref(name, src, self.getpos_label(tag, name)))
            elif name == "style":
                self.collect_css_urls(value, self.getpos_label(tag, name))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style" and self.style_depth:
            self.style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.style_depth:
            self.collect_css_urls(data, self.getpos_label("style", "url"))

    def collect_css_urls(self, css: str, location: str) -> None:
        for match in CSS_URL_RE.finditer(css):
            self.refs.append(Ref("css-url", match.group(2), location))

    def getpos_label(self, tag: str, attr: str) -> str:
        line, col = self.getpos()
        return f"{tag}[{attr}]@{line}:{col + 1}"


def check_refs(html_path: Path, root: Path) -> dict[str, object]:
    parser = AssetRefParser()
    parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))

    local_refs: list[dict[str, str]] = []
    remote_or_ignored = 0
    missing: list[dict[str, str]] = []

    for ref in parser.refs:
        local = normalize_local_ref(ref.value)
        if local is None:
            remote_or_ignored += 1
            continue
        target = (root / local).resolve()
        record = {"kind": ref.kind, "value": ref.value, "path": local, "location": ref.location}
        local_refs.append(record)
        try:
            target.relative_to(root.resolve())
        except ValueError:
            record = {**record, "reason": "escapes root"}
            missing.append(record)
            continue
        if not target.exists():
            missing.append(record)

    return {
        "html": str(html_path),
        "root": str(root),
        "local_refs": len(local_refs),
        "remote_or_ignored_refs": remote_or_ignored,
        "missing_local_refs": missing,
        "status": "PASS" if not missing else "FAIL",
    }


def read_l27_stub_files(root: Path) -> set[str]:
    manifest = root / "pretreat-manifest.json"
    if not manifest.exists():
        return set()
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    files: set[str] = set()
    for section in ("output", "source"):
        for name in data.get(section, {}).get("l27StubFiles", []) or []:
            if isinstance(name, str):
                files.add(name.replace(os.sep, "/"))
    return files


def collect_html_paths(target: Path, root: Path, skipped: set[str]) -> list[Path]:
    if target.is_file():
        rel = target.resolve().relative_to(root.resolve()).as_posix()
        if rel in skipped:
            return []
        return [target]
    if target.is_dir():
        paths = []
        for path in sorted(path for path in target.rglob("*.html") if path.is_file()):
            rel = path.resolve().relative_to(root.resolve()).as_posix()
            if rel not in skipped:
                paths.append(path)
        return paths
    raise FileNotFoundError(f"No such file or directory: {target}")


def check_target(target: Path, root: Path) -> dict[str, object]:
    skipped = read_l27_stub_files(root)
    html_paths = collect_html_paths(target, root, skipped)
    page_results = [check_refs(path.resolve(), root) for path in html_paths]
    missing_total = sum(len(result["missing_local_refs"]) for result in page_results)
    return {
        "target": str(target),
        "root": str(root),
        "html_files": len(page_results),
        "skipped_l27_stub_files": sorted(skipped),
        "pages": page_results,
        "missing_local_refs": missing_total,
        "status": "PASS" if missing_total == 0 else "FAIL",
    }


def main(argv: list[str]) -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("target", type=Path, help="HTML file or directory containing HTML files")
    argp.add_argument("--root", type=Path, default=None)
    argp.add_argument("--json", action="store_true")
    args = argp.parse_args(argv)

    target = args.target.resolve()
    root = (args.root or (target if target.is_dir() else target.parent)).resolve()
    result = check_target(target, root)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"checked: {result['target']}")
        print(f"root: {result['root']}")
        print(f"html_files: {result['html_files']}")
        if result["skipped_l27_stub_files"]:
            print(f"skipped_l27_stub_files: {result['skipped_l27_stub_files']}")
        print(f"missing_local_refs: {result['missing_local_refs']}")
        for page in result["pages"]:
            print(f"page: {page['html']}")
            print(f"  local_refs: {page['local_refs']}")
            print(f"  remote_or_ignored_refs: {page['remote_or_ignored_refs']}")
            print(f"  missing_local_refs: {len(page['missing_local_refs'])}")
            for missing in page["missing_local_refs"]:
                print(f"MISS {page['html']} {missing['location']} {missing['path']}")
        print(result["status"])

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
