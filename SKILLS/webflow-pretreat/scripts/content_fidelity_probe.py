#!/usr/bin/env python3
"""Visible text/glyph fidelity probe for L-34.

Compares the visible text content of source vs output HTML byte-for-byte after
a tightly-defined whitespace normalization step. Detects skill-introduced
mutations of body text, <title>, meta description/og/twitter tags, and
source-content attributes (alt/title/placeholder/aria-label/data-* except
data-w-*).

Pre-treatment is structural-only. The skill must not mutate user-authored
content. This probe enforces that invariant.

Origin: BigBuns 2026-04-26 (3x ®->1F354 burger emoji) + Senorita Colombia
2026-04-26 (<title> reorder) — both passed all 4 prior probes because none
checked visible-text fidelity. See L-34 in references/lessons.md.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SCHEMA_ROW_ID = "content-fidelity-text-glyph"

# Tags whose subtree is excluded from body-text comparison.
SKIP_TAGS = {"script", "style", "template", "noscript"}

# FlowBridge-injected hosts whose subtree is excluded (skill-generated content).
# fb-page-wrapper is intentionally NOT excluded — it's a positioning host whose
# descendants are user content. The embed hosts below carry only skill output.
SKIP_HOST_CLASS_PREFIXES = ("fb-styles-", "fb-media-")
SKIP_HOST_CLASSES = {"fb-scripts", "fb-runtime", "fb-custom-code"}

# Source-content attributes on body elements.
BODY_CONTENT_ATTRS = {"alt", "title", "placeholder", "aria-label"}

# data-* attributes are included as content EXCEPT Webflow runtime attrs.
DATA_W_PREFIX = "data-w-"
# Skill-managed data-flowbridge-* attrs are also excluded (per L-32).
DATA_FB_PREFIX = "data-flowbridge-"

# Head meta tags whose `content` attribute carries source content.
META_NAME_KEYS = {
    "description",
    "twitter:title",
    "twitter:description",
    "twitter:card",
}
META_PROPERTY_KEYS = {
    "og:title",
    "og:description",
    "og:site_name",
    "twitter:title",
    "twitter:description",
}

# Generic head <meta> entries that are NOT source content (charset, viewport,
# generator, etc.) are simply absent from the keys above and therefore ignored.

# HTMLParser void tags that don't take an end tag.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

WS_RE = re.compile(r"\s+")
NBSP = " "


def normalize_text(text: str) -> str:
    """Decode entities, normalize NBSP, collapse whitespace, strip.

    Compared as Unicode codepoint sequence after this normalization. Any
    codepoint diff (including emoji, accented Latin, ASCII case) is a FAIL.
    """
    if not text:
        return ""
    decoded = html_lib.unescape(text)
    # NBSP is a "real" character but treat it as whitespace for fidelity:
    # source authors and converters can interchange NBSP/space without
    # signalling a content mutation. The plan's worked example #4 (Burger&nbsp;time
    # vs Burger time) requires this collapse.
    decoded = decoded.replace(NBSP, " ")
    collapsed = WS_RE.sub(" ", decoded)
    return collapsed.strip()


# ---------------------------------------------------------------------------
# Document inventory
# ---------------------------------------------------------------------------

@dataclass
class DocumentTexts:
    """Collected visible-text channels for a single HTML document."""
    body_text: str = ""
    title: str = ""
    metas: list[tuple[str, str]] = field(default_factory=list)
    body_attrs: list[tuple[str, str, str]] = field(default_factory=list)
    # body_attrs items: (tag, attr_name, normalized_value)


class _SkipFrame:
    """Tracks one skip-subtree boundary on the parser stack."""
    __slots__ = ("tag", "depth")

    def __init__(self, tag: str) -> None:
        self.tag = tag
        # depth of nested same-tag opens, decremented on each close
        self.depth = 1


class TextExtractor(HTMLParser):
    """HTMLParser that emits visible-text channels per L-34."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_body = False
        # Stack of (tag) frames for skip subtrees (script/style/fb-hosts...)
        self._skip_stack: list[_SkipFrame] = []
        self._in_title = False
        self._title_buffer: list[str] = []
        self._body_buffer: list[str] = []
        self.title: str = ""
        self.metas: list[tuple[str, str]] = []
        self.body_attrs: list[tuple[str, str, str]] = []

    # ---- helpers ----
    def _attrs_dict(self, attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {name.lower(): (value or "") for name, value in attrs}

    def _classes(self, attr: dict[str, str]) -> list[str]:
        return attr.get("class", "").split()

    def _is_skip_host(self, attr: dict[str, str]) -> bool:
        for cls in self._classes(attr):
            if cls in SKIP_HOST_CLASSES:
                return True
            for prefix in SKIP_HOST_CLASS_PREFIXES:
                if cls.startswith(prefix):
                    return True
        return False

    def _in_skip(self) -> bool:
        return bool(self._skip_stack)

    def _record_body_attrs(self, tag: str, attr: dict[str, str]) -> None:
        for name, value in attr.items():
            if name in BODY_CONTENT_ATTRS:
                norm = normalize_text(value)
                if norm:
                    self.body_attrs.append((tag, name, norm))
            elif name.startswith("data-"):
                # Skip Webflow runtime + skill-managed namespaces.
                if name.startswith(DATA_W_PREFIX):
                    continue
                if name.startswith(DATA_FB_PREFIX):
                    continue
                norm = normalize_text(value)
                if norm:
                    self.body_attrs.append((tag, name, norm))

    def _record_meta(self, attr: dict[str, str]) -> None:
        content = attr.get("content", "")
        norm = normalize_text(content)
        if not norm:
            return
        name = attr.get("name", "").lower()
        prop = attr.get("property", "").lower()
        if name in META_NAME_KEYS:
            self.metas.append((f"name:{name}", norm))
        if prop in META_PROPERTY_KEYS:
            self.metas.append((f"property:{prop}", norm))

    # ---- HTMLParser overrides ----
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_open(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_open(tag, attrs, self_closing=True)

    def _handle_open(self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool) -> None:
        tag = tag.lower()
        attr = self._attrs_dict(attrs)

        if tag == "head":
            self.in_head = True
        elif tag == "body":
            self.in_body = True

        # Already inside a skip subtree: just track depth so we exit cleanly.
        if self._in_skip():
            if not self_closing and tag not in VOID_TAGS:
                self._skip_stack.append(_SkipFrame(tag))
            return

        # Open new skip subtree?
        is_skip_tag = tag in SKIP_TAGS
        is_skip_host = self.in_body and self._is_skip_host(attr)
        if is_skip_tag or is_skip_host:
            if not self_closing and tag not in VOID_TAGS:
                self._skip_stack.append(_SkipFrame(tag))
            return

        # Title: collect text content
        if self.in_head and tag == "title":
            self._in_title = True
            self._title_buffer = []
            return

        # Meta in head
        if self.in_head and tag == "meta":
            self._record_meta(attr)
            return

        # Body element: record content attrs (alt/title/placeholder/aria-label/data-*)
        if self.in_body:
            self._record_body_attrs(tag, attr)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._in_skip():
            # Pop one skip frame when its tag closes (matches innermost-open style).
            top = self._skip_stack[-1]
            if top.tag == tag:
                self._skip_stack.pop()
            # Else: malformed nesting, ignore the close (safe).
            return

        if self._in_title and tag == "title":
            self.title = normalize_text("".join(self._title_buffer))
            self._title_buffer = []
            self._in_title = False
            return

        if tag == "head":
            self.in_head = False
        elif tag == "body":
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if self._in_skip():
            return
        if self._in_title:
            self._title_buffer.append(data)
            return
        if self.in_body:
            self._body_buffer.append(data)

    def finalize(self) -> DocumentTexts:
        body_text = normalize_text(" ".join(self._body_buffer))
        return DocumentTexts(
            body_text=body_text,
            title=self.title,
            metas=list(self.metas),
            body_attrs=list(self.body_attrs),
        )


def extract_document(html: str) -> DocumentTexts:
    parser = TextExtractor()
    parser.feed(html)
    parser.close()
    return parser.finalize()


# ---------------------------------------------------------------------------
# File iteration
# ---------------------------------------------------------------------------

def _strip_common_top_folder(paths: dict[str, str]) -> dict[str, str]:
    """If every path shares the same top-level folder, strip it.

    Webflow export ZIPs sometimes wrap content in `<site-slug>/`; the matching
    extracted folder is usually flattened. Without this, a clean output would
    be flagged as 'all files missing + all files added'.
    """
    if not paths:
        return paths
    tops = {p.split("/", 1)[0] for p in paths if "/" in p}
    has_root_files = any("/" not in p for p in paths)
    if has_root_files or len(tops) != 1:
        return paths
    top = next(iter(tops)) + "/"
    return {p[len(top):]: html for p, html in paths.items() if p.startswith(top)}


def iter_html_files(root: Path) -> dict[str, str]:
    """Return {relative_path: html_string} for all HTML files under root.

    root may be a directory, a single .html file, or a .zip archive.
    A single shared top-level folder (e.g. `<site-slug>/`) is stripped so
    folder-extracted and ZIP-wrapped variants of the same export pair cleanly.
    """
    out: dict[str, str] = {}
    if root.is_file() and root.suffix.lower() == ".zip":
        with zipfile.ZipFile(root) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith(".html"):
                    out[name] = archive.read(name).decode("utf-8", errors="replace")
        return _strip_common_top_folder(out)
    if root.is_file():
        out[root.name] = root.read_text(encoding="utf-8", errors="replace")
        return out
    for path in sorted(root.rglob("*.html")):
        rel = str(path.relative_to(root)).replace("\\", "/")
        out[rel] = path.read_text(encoding="utf-8", errors="replace")
    return _strip_common_top_folder(out)


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compare_documents(
    source_files: dict[str, str],
    output_files: dict[str, str],
) -> dict[str, Any]:
    """Compare visible-text channels between source and output documents.

    Returns a result dict suitable for the `details` block of the manifest row,
    plus a top-level `status` and `evidence` summary.
    """
    source_docs = {p: extract_document(h) for p, h in source_files.items()}
    output_docs = {p: extract_document(h) for p, h in output_files.items()}

    all_paths = sorted(set(source_docs) | set(output_docs))

    missing_from_output: list[dict[str, str]] = []
    added_in_output: list[dict[str, str]] = []
    changed_samples: list[dict[str, str]] = []

    source_text_nodes = 0
    output_text_nodes = 0

    for path in all_paths:
        s = source_docs.get(path)
        o = output_docs.get(path)

        if s is None and o is not None:
            # File added by skill (typically not allowed for content files,
            # but skill-injected hosts won't contain visible text → empty).
            if o.body_text or o.title or o.metas or o.body_attrs:
                added_in_output.append({
                    "path": path,
                    "kind": "file-added-with-content",
                    "text": (o.body_text[:120] or o.title or "<has metas/attrs>")[:120],
                })
            continue
        if o is None and s is not None:
            if s.body_text or s.title or s.metas or s.body_attrs:
                missing_from_output.append({
                    "path": path,
                    "kind": "file-missing",
                    "text": (s.body_text[:120] or s.title or "<has metas/attrs>")[:120],
                })
            continue

        # Both present.
        # body text: per-file equality
        source_text_nodes += int(bool(s.body_text)) + int(bool(s.title)) + len(s.metas) + len(s.body_attrs)
        output_text_nodes += int(bool(o.body_text)) + int(bool(o.title)) + len(o.metas) + len(o.body_attrs)

        if s.body_text != o.body_text:
            changed_samples.append({
                "path": path,
                "channel": "body",
                "source": _truncate(s.body_text, 200),
                "output": _truncate(o.body_text, 200),
            })

        if s.title != o.title:
            changed_samples.append({
                "path": path,
                "channel": "title",
                "source": s.title,
                "output": o.title,
            })

        # metas: bag diff per (kind, value)
        s_metas = Counter(s.metas)
        o_metas = Counter(o.metas)
        for item, count in (s_metas - o_metas).items():
            kind, value = item
            for _ in range(count):
                missing_from_output.append({
                    "path": path,
                    "kind": f"meta:{kind}",
                    "text": value,
                })
        for item, count in (o_metas - s_metas).items():
            kind, value = item
            for _ in range(count):
                added_in_output.append({
                    "path": path,
                    "kind": f"meta:{kind}",
                    "text": value,
                })

        # body attrs: bag diff per (tag, attr, value)
        s_attrs = Counter(s.body_attrs)
        o_attrs = Counter(o.body_attrs)
        for item, count in (s_attrs - o_attrs).items():
            tag, attr_name, value = item
            for _ in range(count):
                missing_from_output.append({
                    "path": path,
                    "kind": f"attr:{tag}@{attr_name}",
                    "text": value,
                })
        for item, count in (o_attrs - s_attrs).items():
            tag, attr_name, value = item
            for _ in range(count):
                added_in_output.append({
                    "path": path,
                    "kind": f"attr:{tag}@{attr_name}",
                    "text": value,
                })

    failed = bool(missing_from_output or added_in_output or changed_samples)
    if failed:
        evidence_parts = []
        if changed_samples:
            evidence_parts.append(f"{len(changed_samples)} channel(s) with text mutation")
        if missing_from_output:
            evidence_parts.append(f"{len(missing_from_output)} text item(s) missing from output")
        if added_in_output:
            evidence_parts.append(f"{len(added_in_output)} text item(s) added in output")
        evidence = "L-34 fidelity FAIL: " + "; ".join(evidence_parts)
        status = "fail"
    else:
        status = "pass"
        evidence = (
            f"L-34 fidelity OK: {len(source_docs)} document(s) compared; "
            f"{source_text_nodes} source text channel(s) match output."
        )

    return {
        "id": SCHEMA_ROW_ID,
        "status": status,
        "evidence": evidence,
        "details": {
            "sourceTextNodeCount": source_text_nodes,
            "outputTextNodeCount": output_text_nodes,
            "missingFromOutput": missing_from_output[:50],
            "addedInOutput": added_in_output[:50],
            "changedSamples": changed_samples[:50],
        },
    }


def _truncate(text: str, n: int) -> str:
    if len(text) <= n:
        return text
    return text[:n] + "..."


# ---------------------------------------------------------------------------
# Manifest write
# ---------------------------------------------------------------------------

def upsert_manifest_row(output_root: Path, row: dict[str, Any]) -> Path:
    """Append (or replace) the contractChecks row with id=SCHEMA_ROW_ID."""
    if not output_root.is_dir():
        raise SystemExit("--write-manifest requires --output-root to be a directory")
    manifest_path = output_root / "pretreat-manifest.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Existing pretreat-manifest.json is invalid JSON: {exc}")
    else:
        data = {
            "schema": "flowbridge.pretreat-manifest.v1",
            "contractChecks": [],
        }
    checks = data.setdefault("contractChecks", [])
    for i, existing in enumerate(checks):
        if isinstance(existing, dict) and existing.get("id") == SCHEMA_ROW_ID:
            checks[i] = row
            break
    else:
        checks.append(row)
    manifest_path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def run_self_test() -> int:
    """Ten in-memory cases covering the worked examples from plan 330."""
    failures: list[str] = []

    def assert_compare(label: str, src: dict[str, str], out: dict[str, str], expect: str) -> None:
        result = compare_documents(src, out)
        if result["status"] != expect:
            failures.append(
                f"{label}: expected {expect}, got {result['status']}; "
                f"evidence={result['evidence']}; details={json.dumps(result['details'])[:300]}"
            )

    # 1. Identical body
    assert_compare(
        "1-identical",
        {"index.html": "<html><body><p>Hello world</p></body></html>"},
        {"index.html": "<html><body><p>Hello world</p></body></html>"},
        "pass",
    )
    # 2. Whitespace-only diff
    assert_compare(
        "2-whitespace",
        {"index.html": "<html><body><p>Hello  world</p></body></html>"},
        {"index.html": "<html><body><p>Hello\n  world</p></body></html>"},
        "pass",
    )
    # 3. Single-char body mutation
    assert_compare(
        "3-case-mutation",
        {"index.html": "<html><body><p>Hello world</p></body></html>"},
        {"index.html": "<html><body><p>Hello World</p></body></html>"},
        "fail",
    )
    # 4. Emoji injection (BigBuns case)
    assert_compare(
        "4-emoji-injection",
        {"index.html": "<html><body><p>BigBuns&#174;</p></body></html>"},
        {"index.html": "<html><body><p>BigBuns\U0001F354</p></body></html>"},
        "fail",
    )
    # 5. Title reorder (Senorita case)
    assert_compare(
        "5-title-reorder",
        {"index.html": "<html><head><title>A | B</title></head><body>x</body></html>"},
        {"index.html": "<html><head><title>B | A</title></head><body>x</body></html>"},
        "fail",
    )
    # 6. Legitimate skill-injected wrapper
    assert_compare(
        "6-wrapper-injection",
        {"index.html": "<html><body><div>x</div></body></html>"},
        {"index.html": '<html><body><div class="fb-page-wrapper"><div>x</div></div></body></html>'},
        "pass",
    )
    # 7. HTML entity decode equivalence
    assert_compare(
        "7-entity-decode",
        {"index.html": "<html><body><p>&copy; 2024</p></body></html>"},
        {"index.html": "<html><body><p>© 2024</p></body></html>"},
        "pass",
    )
    # 8. Alt-text mutation
    assert_compare(
        "8-alt-mutation",
        {"index.html": '<html><body><img alt="Logo"></body></html>'},
        {"index.html": '<html><body><img alt="Brand Logo"></body></html>'},
        "fail",
    )
    # 9. Webflow data-w-id ignored (and added-only output is fine)
    assert_compare(
        "9-data-w-ignored",
        {"index.html": '<html><body><div>x</div></body></html>'},
        {"index.html": '<html><body><div data-w-id="abc-1">x</div></body></html>'},
        "pass",
    )
    # 10. Embed host content ignored (fb-styles-site subtree skipped)
    assert_compare(
        "10-embed-host-ignored",
        {"index.html": "<html><body><p>x</p></body></html>"},
        {"index.html": (
            '<html><body><div class="fb-styles-site">'
            "<style>.foo { color: red; }</style>some skill text"
            '</div><p>x</p></body></html>'
        )},
        "pass",
    )

    # Bonus: NBSP collapses to space (worked example #4 in plan)
    assert_compare(
        "B-nbsp-collapse",
        {"index.html": "<html><body><p>Burger&nbsp;time</p></body></html>"},
        {"index.html": "<html><body><p>Burger time</p></body></html>"},
        "pass",
    )

    if failures:
        print("content-fidelity self-test: FAIL")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("content-fidelity self-test: PASS (11 cases)")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="L-34 content fidelity probe: verify visible text is preserved byte-for-byte (after whitespace normalization).",
    )
    parser.add_argument("--source-root", type=Path, help="Source export folder, HTML file, or .zip.")
    parser.add_argument("--output-root", type=Path, help="Pretreated output folder, HTML file, or .zip.")
    parser.add_argument("--write-manifest", action="store_true", help="Append/update content-fidelity-text-glyph row in pretreat-manifest.json.")
    parser.add_argument("--fail-on-contract", action="store_true", help="Exit 1 if any FAIL row.")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory self-test cases.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        return run_self_test()
    if not args.source_root or not args.output_root:
        # Schema-only mode (no source/output) per plan section 1.3.
        print(json.dumps({
            "id": SCHEMA_ROW_ID,
            "status": "schema-only",
            "evidence": "Provide --source-root and --output-root to run; --self-test for unit tests.",
        }, indent=2))
        return 0

    source_files = iter_html_files(args.source_root)
    output_files = iter_html_files(args.output_root)
    row = compare_documents(source_files, output_files)

    print(json.dumps(row, indent=2, sort_keys=True))

    if args.write_manifest:
        path = upsert_manifest_row(args.output_root, row)
        print(f"manifest updated: {path}", file=sys.stderr)

    if args.fail_on_contract and row["status"] == "fail":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
