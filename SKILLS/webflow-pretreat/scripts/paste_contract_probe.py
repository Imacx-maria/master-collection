#!/usr/bin/env python3
"""Probe FlowBridge pre-treatment output-mode contracts.

This script is a deterministic consultation/check layer for the AI
pre-treatment skill. It does not transform exports. It inventories source and
output HTML/CSS surfaces, checks the declared output mode, and can write the
machine-readable pretreat-manifest.json beside index.html.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parents[1]
REPO_ROOT = SKILL_DIR.parents[2]

SCHEMA = "flowbridge.pretreat-manifest.v1"
PROFILE_SCHEMA = "flowbridge.pretreat-manifest-profile.v1"

# Phase 1B observability (OPTIMIZATION-PLAN.md). Mutated by main() when --profile
# is passed. Records are appended by _time_call() during build_contract_checks().
_PROFILE_ENABLED: bool = False
_PROFILE_RECORDS: list[dict[str, Any]] = []
FONT_EXTENSIONS = (".woff2", ".woff", ".ttf", ".otf", ".eot")
CANONICAL_MEDIA = {
    "(max-width: 479px)",
    "(max-width: 767px)",
    "(max-width: 991px)",
    "(min-width: 1280px)",
    "(min-width: 1440px)",
    "(min-width: 1920px)",
}
SCRIPT_GLOBALS = (
    "$",
    "jQuery",
    "Splide",
    "gsap",
    "ScrollTrigger",
    "ScrollSmoother",
    "Lenis",
    "Swiper",
    "Webflow",
)
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
MEDIA_TAGS = {"img", "picture", "source", "video", "audio", "svg", "canvas", "iframe"}
INTERACTIVE_TAGS = {"a", "button", "input", "select", "textarea"}
STATIC_HIDDEN_CHROME_CLASSES = (
    ("nav-child", "left"),
    ("nav-link", "one"),
    ("nav-link", "two"),
    ("nav-link", "three"),
)
STATIC_VISIBLE_FORBIDDEN_CLASS_STATE_IDS = {
    "nav-child-left-closed",
    "nav-link-one-hidden",
    "nav-link-two-hidden",
    "nav-link-three-hidden",
    "img-parent-top-size-collapsed",
    "recent-info-parent-offset",
}
COMPONENT_FALLBACK_HOSTS = {
    "splide": "fb-styles-splide",
    "swiper": "fb-styles-swiper",
    "embla": "fb-styles-embla",
    "flickity": "fb-styles-flickity",
    "lottie": "fb-styles-lottie",
}
# L-7 is now class-agnostic (EXP-003 universalization, 2026-04-24). The probe enumerates
# source-DOM classes at runtime and scans output style hosts for collapse rules targeting
# any of them. No fixture-specific class whitelist.
L7_FRAMEWORK_CLASS_PREFIXES = ("w-", "fb-")

# EXP-004 (2026-04-25): mode-B IX2-hidden initial-state target detection is now
# class-name-agnostic. `detect_mode_b_targets(html)` enumerates source elements
# whose `data-w-id` + inline `style=""` carry a hidden-on-load signature and
# emits a per-source target list. The check functions
# `mode_b_initial_state_transport_check` and `mode_b_d007_anchor_check` consume
# that dynamic list. The hardcoded `INITIAL_STATE_TARGETS` constant below is
# retained ONLY as the legacy spec catalog for the out-of-scope check
# `summarize_static_visible_class_state_safety` (probe row
# `mode-b-static-visible-class-state-safety`), which remains untouched per
# EXP-004 scope ("Do NOT modify any other probe check"). Mode-B transport no
# longer reads it.
INITIAL_STATE_TARGETS = [
    {
        "id": "nav-child-left-closed",
        "selector": ".nav-child.left",
        "classes": ("nav-child", "left"),
        "required": ("transform:translate3d(-100%,0,0)", "height:3rem"),
    },
    {
        "id": "bg-whipe-overlay-collapsed",
        "selector": ".bg-whipe",
        "classes": ("bg-whipe",),
        "classMatch": "exact",
        "required": ("width:100%", "height:0%"),
    },
    {
        "id": "nav-link-one-hidden",
        "selector": ".nav-link.one",
        "classes": ("nav-link", "one"),
        "required": ("opacity:0", "transform:translate3d(0,-200%,0)"),
    },
    {
        "id": "nav-link-two-hidden",
        "selector": ".nav-link.two",
        "classes": ("nav-link", "two"),
        "required": ("opacity:0", "transform:translate3d(0,-200%,0)"),
    },
    {
        "id": "nav-link-three-hidden",
        "selector": ".nav-link.three",
        "classes": ("nav-link", "three"),
        "required": ("opacity:0", "transform:translate3d(0,-200%,0)"),
    },
    {
        "id": "slider2-component-root",
        "selector": ".slider2",
        "classes": ("slider2",),
        "required": ("opacity:0",),
        "component_fallback_host": "fb-styles-splide",
    },
    {
        "id": "img-parent-top-size-collapsed",
        "selector": ".img-parent.top-size",
        "classes": ("img-parent", "top-size"),
        "required": ("width:100%", "height:0rem"),
    },
    {
        "id": "recent-info-parent-offset",
        "selector": ".recent-info-parent",
        "classes": ("recent-info-parent",),
        "required": ("transform:translate3d(0,110%,0)",),
    },
]


# EXP-004 (2026-04-25): mode-B target detection signatures.
# An inline style declaration triggers detection when it indicates the element
# is hidden-on-load — display/visibility/opacity collapse, off-screen translate,
# zero-scale transform, fully-clipped clip-path, or zero collapse on a sizing
# property. Vendor-prefixed transforms count toward detection but only the
# canonical `transform` property is emitted as a `required` fragment so CSS
# transport scans (which compare against output style hosts) stay precise.
MODE_B_HIDDEN_SIZING_PROPERTIES = ("width", "height", "max-width", "max-height")
MODE_B_VENDOR_TRANSFORM_PROPERTIES = (
    "transform",
    "-webkit-transform",
    "-moz-transform",
    "-ms-transform",
)


@dataclass
class TextFile:
    path: str
    text: str


@dataclass
class StyleAttrFinding:
    file: str
    tag: str
    classes: list[str]
    attrs: dict[str, str]
    style: str
    classification: str
    ix_declarations: list[str]
    structural_declarations: list[str]


@dataclass
class ElementFinding:
    file: str
    tag: str
    classes: list[str]
    attrs: dict[str, str]
    text_chars: int = 0
    descendant_tag_count: int = 0
    has_media: bool = False
    has_link: bool = False


@dataclass
class HtmlProbe:
    elements: list[ElementFinding] = field(default_factory=list)
    data_w_ids: list[str] = field(default_factory=list)
    style_attrs: list[StyleAttrFinding] = field(default_factory=list)
    source_content_ix_style_attrs: list[StyleAttrFinding] = field(default_factory=list)
    fb_runtime_count: int = 0
    js_webflow_references: int = 0
    inline_module_iife_signatures: int = 0
    fb_custom_code_count: int = 0
    fb_custom_code_display_none: int = 0
    fb_styles_site_css: list[str] = field(default_factory=list)
    fb_media_site_css: list[str] = field(default_factory=list)
    fb_styles_library_css: dict[str, list[str]] = field(default_factory=dict)
    reserved_classes: set[str] = field(default_factory=set)
    inline_scripts: list[dict[str, str]] = field(default_factory=list)
    external_scripts: list[dict[str, str]] = field(default_factory=list)
    video_elements: list[dict[str, Any]] = field(default_factory=list)
    video_sources: list[dict[str, Any]] = field(default_factory=list)


class ProbeParser(HTMLParser):
    def __init__(self, file_path: str) -> None:
        super().__init__(convert_charrefs=True)
        self.file_path = file_path
        self.probe = HtmlProbe()
        self._in_inline_script = False
        self._inline_script_chunks: list[str] = []
        self._div_class_stack: list[set[str]] = []
        self._in_style = False
        self._style_host: str | None = None
        self._style_chunks: list[str] = []
        self._element_stack: list[ElementFinding] = []
        self._video_stack: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=True)

    def handle_data(self, data: str) -> None:
        if self._in_inline_script:
            self._inline_script_chunks.append(data)
        if self._in_style:
            self._style_chunks.append(data)
        if not self._in_inline_script and not self._in_style:
            text = data.strip()
            if text:
                for element in self._element_stack:
                    element.text_chars += len(text)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_inline_script:
            script = "".join(self._inline_script_chunks)
            self.probe.inline_scripts.append({"file": self.file_path, "script": script})
            if is_inline_webflow_module(script):
                self.probe.inline_module_iife_signatures += 1
            self._inline_script_chunks = []
            self._in_inline_script = False
        if tag.lower() == "style" and self._in_style:
            css = "".join(self._style_chunks)
            if self._style_host == "fb-styles-site":
                self.probe.fb_styles_site_css.append(css)
            elif self._style_host == "fb-media-site":
                self.probe.fb_media_site_css.append(css)
            elif self._style_host and self._style_host.startswith("fb-styles-"):
                self.probe.fb_styles_library_css.setdefault(self._style_host, []).append(css)
            self._style_chunks = []
            self._style_host = None
            self._in_style = False
        if tag.lower() == "div" and self._div_class_stack:
            self._div_class_stack.pop()
        if tag.lower() == "video" and self._video_stack:
            self._video_stack.pop()
        normalized_tag = tag.lower()
        for index in range(len(self._element_stack) - 1, -1, -1):
            if self._element_stack[index].tag == normalized_tag:
                del self._element_stack[index:]
                break

    def _handle_tag(self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool) -> None:
        tag = tag.lower()
        attr = {name.lower(): value or "" for name, value in attrs}
        classes = attr.get("class", "").split()
        class_set = set(classes)
        element = ElementFinding(
            file=self.file_path,
            tag=tag,
            classes=classes,
            attrs=attr,
            has_media=tag in MEDIA_TAGS,
            has_link=tag == "a" or bool(attr.get("href")),
        )
        self.probe.elements.append(element)

        for ancestor in self._element_stack:
            ancestor.descendant_tag_count += 1
            if tag in MEDIA_TAGS:
                ancestor.has_media = True
            if tag == "a" or bool(attr.get("href")):
                ancestor.has_link = True

        if tag == "div" and not self_closing:
            self._div_class_stack.append(class_set)

        for cls in classes:
            if cls.startswith("w-") or cls.startswith("w--") or cls.startswith("_w-"):
                self.probe.reserved_classes.add(cls)

        if "data-w-id" in attr:
            self.probe.data_w_ids.append(attr["data-w-id"])

        if "fb-runtime" in class_set:
            self.probe.fb_runtime_count += 1

        if "fb-custom-code" in class_set:
            self.probe.fb_custom_code_count += 1
            if has_display_none(attr.get("style", "")):
                self.probe.fb_custom_code_display_none += 1

        if tag == "script":
            src = attr.get("src", "").strip()
            if src and is_relative_js_webflow(src):
                self.probe.js_webflow_references += 1
            if src:
                self.probe.external_scripts.append({"file": self.file_path, "src": src})
            if not src:
                self._in_inline_script = True
                self._inline_script_chunks = []

        if tag == "video":
            video_record = {"file": self.file_path, "classes": classes, "attrs": attr}
            self.probe.video_elements.append(video_record)
            if not self_closing:
                self._video_stack.append(video_record)

        if tag == "source" and self._video_stack:
            self.probe.video_sources.append({"file": self.file_path, "attrs": attr})

        if tag == "style":
            self._in_style = True
            self._style_chunks = []
            self._style_host = find_style_host(self._div_class_stack)

        if "style" in attr:
            classification, ix_decls, structural_decls = classify_style_attr(attr["style"])
            finding = StyleAttrFinding(
                file=self.file_path,
                tag=tag,
                classes=classes,
                attrs=attr,
                style=attr["style"],
                classification=classification,
                ix_declarations=ix_decls,
                structural_declarations=structural_decls,
            )
            self.probe.style_attrs.append(finding)
            if ix_decls and not is_flowbridge_structural_host(classes):
                self.probe.source_content_ix_style_attrs.append(finding)

        if not self_closing and tag not in VOID_TAGS:
            self._element_stack.append(element)


def is_inline_webflow_module(script: str) -> bool:
    if "var e={1361:" in script or "(()=>{var e={" in script:
        return True
    return len(script) > 50000 and all(token in script for token in ("Webflow.push", "Webflow.require", "Webflow.define"))


def is_relative_url(url: str) -> bool:
    lower = url.strip().strip("'\"").lower()
    return not (
        lower.startswith(("http://", "https://", "//", "data:", "blob:", "mailto:", "tel:", "#"))
        or re.match(r"^[a-z][a-z0-9+.-]*:", lower)
    )


def is_relative_js_webflow(src: str) -> bool:
    normalized = src.strip().strip("'\"").split("?", 1)[0].replace("\\", "/").lower()
    return is_relative_url(src) and normalized.endswith("/webflow.js") or normalized == "js/webflow.js"


def has_display_none(style: str) -> bool:
    for name, value, _raw in parse_declarations(style):
        if name == "display" and value.replace(" ", "").lower() == "none":
            return True
    return False


def is_flowbridge_structural_host(classes: list[str]) -> bool:
    class_set = set(classes)
    return bool({"fb-custom-code", "fb-runtime"} & class_set)


def find_style_host(class_stack: list[set[str]]) -> str | None:
    for class_set in reversed(class_stack):
        for class_name in class_set:
            if class_name in {"fb-styles-site", "fb-media-site"} or (
                class_name.startswith("fb-styles-") and class_name != "fb-styles-site"
            ):
                return class_name
    return None


def parse_declarations(style: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for raw in style.split(";"):
        if ":" not in raw:
            continue
        name, value = raw.split(":", 1)
        name = name.strip().lower()
        value = value.strip()
        if name:
            out.append((name, value, f"{name}: {value}"))
    return out


def classify_style_attr(style: str) -> tuple[str, list[str], list[str]]:
    ix_decls: list[str] = []
    structural_decls: list[str] = []

    for name, value, raw in parse_declarations(style):
        if is_ix_declaration(name, value):
            ix_decls.append(raw)
        else:
            structural_decls.append(raw)

    if ix_decls and not structural_decls:
        classification = "ix-only"
    elif ix_decls and structural_decls:
        classification = "mixed"
    else:
        classification = "structural"
    return classification, ix_decls, structural_decls


def is_ix_declaration(name: str, value: str) -> bool:
    if name in {"transform", "-webkit-transform", "-moz-transform", "-ms-transform"}:
        normalized = value.lower().replace(" ", "")
        return "translate3d(" in normalized and any(
            token in normalized for token in ("scale3d(", "rotatex(", "rotatey(", "rotatez(", "skew(")
        )
    if name == "opacity":
        return value.strip().lower() in {"0", "0.0", ".0"}
    if name in {"width", "height"}:
        return bool(re.fullmatch(r"0(?:\.0+)?(?:px|rem|em|%|vh|vw|vmin|vmax)?", value.strip().lower()))
    return False


def iter_text_files(root: Path) -> list[TextFile]:
    if root.is_file() and root.suffix.lower() == ".zip":
        out: list[TextFile] = []
        with zipfile.ZipFile(root) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith((".html", ".css")):
                    out.append(TextFile(name, archive.read(name).decode("utf-8", errors="replace")))
        return out

    if root.is_file():
        return [TextFile(str(root), root.read_text(encoding="utf-8", errors="replace"))]

    out = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".html", ".css"}:
            out.append(TextFile(str(path.relative_to(root)), path.read_text(encoding="utf-8", errors="replace")))
    return out


L27_NON_CONTENT_TAGS = {"script", "style", "link", "meta", "title"}


class _L27BodyChildScanner(HTMLParser):
    """Walks a single HTML file and records the direct children of <body> (tags only).

    Used solely for L-27 stub classification per docs/LESSONS.md L-27 and
    SKILL.md Workflow step 5: a CMS template stub has zero content-bearing
    body children (excluding script/style/link/meta/title) AND at least one
    <script> child. A body with zero children of any kind is NOT a stub.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._depth_inside_body = 0  # 0 = outside <body>; 1 = direct child level; >1 = deeper
        self._in_body = False
        self.body_seen = False
        self.direct_child_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "body":
            self._in_body = True
            self.body_seen = True
            self._depth_inside_body = 0
            return
        if not self._in_body:
            return
        if self._depth_inside_body == 0:
            self.direct_child_tags.append(tag)
        if tag not in VOID_TAGS:
            self._depth_inside_body += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if not self._in_body:
            return
        if self._depth_inside_body == 0:
            self.direct_child_tags.append(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "body":
            self._in_body = False
            self._depth_inside_body = 0
            return
        if not self._in_body:
            return
        if self._depth_inside_body > 0:
            self._depth_inside_body -= 1


def is_l27_stub(text: str) -> bool:
    """L-27 stub detection mirrored from docs/LESSONS.md L-27 algorithm.

    Returns True iff <body>'s direct tag children include zero
    content-bearing elements (any tag NOT in {script, style, link, meta,
    title}) AND at least one <script> child. A body with no children at
    all is NOT a stub (caller should treat as malformed export).
    """
    scanner = _L27BodyChildScanner()
    try:
        scanner.feed(text)
    except Exception:
        return False
    if not scanner.body_seen or not scanner.direct_child_tags:
        return False
    content_children = [t for t in scanner.direct_child_tags if t not in L27_NON_CONTENT_TAGS]
    script_children = [t for t in scanner.direct_child_tags if t == "script"]
    return len(content_children) == 0 and len(script_children) > 0


def merge_html_probes(probes: list[HtmlProbe]) -> HtmlProbe:
    merged = HtmlProbe()
    for probe in probes:
        merged.elements.extend(probe.elements)
        merged.data_w_ids.extend(probe.data_w_ids)
        merged.style_attrs.extend(probe.style_attrs)
        merged.source_content_ix_style_attrs.extend(probe.source_content_ix_style_attrs)
        merged.fb_runtime_count += probe.fb_runtime_count
        merged.js_webflow_references += probe.js_webflow_references
        merged.inline_module_iife_signatures += probe.inline_module_iife_signatures
        merged.fb_custom_code_count += probe.fb_custom_code_count
        merged.fb_custom_code_display_none += probe.fb_custom_code_display_none
        merged.fb_styles_site_css.extend(probe.fb_styles_site_css)
        merged.fb_media_site_css.extend(probe.fb_media_site_css)
        for host, css_blocks in probe.fb_styles_library_css.items():
            merged.fb_styles_library_css.setdefault(host, []).extend(css_blocks)
        merged.reserved_classes.update(probe.reserved_classes)
        merged.inline_scripts.extend(probe.inline_scripts)
        merged.external_scripts.extend(probe.external_scripts)
        merged.video_elements.extend(probe.video_elements)
        merged.video_sources.extend(probe.video_sources)
    return merged


def inventory_root(root: Path | None) -> dict[str, Any] | None:
    if root is None:
        return None

    files = iter_text_files(root)
    html_files = [file for file in files if file.path.lower().endswith(".html")]
    css_files = [file for file in files if file.path.lower().endswith(".css")]
    html_probes = []
    stub_files: list[str] = []
    for file in html_files:
        parser = ProbeParser(file.path)
        parser.feed(file.text)
        html_probes.append(parser.probe)
        if is_l27_stub(file.text):
            stub_files.append(file.path)
    html = merge_html_probes(html_probes)
    all_text = "\n".join(file.text for file in files)
    source_site_css = "\n".join(file.text for file in css_files if is_source_site_css(file.path))
    fb_styles_site_css = "\n".join(html.fb_styles_site_css)

    detected_mode_b_targets = detect_mode_b_targets(html)

    return {
        "root": str(root),
        "htmlFiles": [file.path for file in html_files],
        "l27StubFiles": stub_files,
        "l27StubCount": len(stub_files),
        "cssFiles": [file.path for file in css_files],
        "dataWIdCount": len(html.data_w_ids),
        "styleAttrCount": len(html.style_attrs),
        "ixInlineStyleAttrs": summarize_style_findings(html.source_content_ix_style_attrs),
        "initialStateTransport": summarize_initial_state_transport(html, detected_mode_b_targets),
        "modeBTargets": detected_mode_b_targets,
        "staticVisibleIxStateSafety": summarize_static_visible_ix_state_safety(html),
        "staticVisibleClassStateSafety": summarize_static_visible_class_state_safety(html),
        "overlayNeutralization": summarize_overlay_neutralization(files, html),
        "domClassSet": sorted(enumerate_source_dom_classes(html)),
        # EXP-003: pre-compute the set of legitimate source-authored class-chain
        # collapse rules so the overlay check can subtract them (source-preserved
        # collapses like `.hide-all { display: none }` are NOT L-7 violations —
        # only skill-injected collapses are).
        "sourceCollapseRules": collect_class_collapse_rules_from_css(source_site_css),
        "lazyVideo": summarize_lazy_video(html),
        "styleAttrClassification": summarize_classifications(html.style_attrs),
        "runtime": {
            "fbRuntimeCount": html.fb_runtime_count,
            "fbRuntimePresent": html.fb_runtime_count > 0,
            "jsWebflowReferences": html.js_webflow_references,
            "inlineModuleIifeSignatures": html.inline_module_iife_signatures,
            "fbCustomCodeCount": html.fb_custom_code_count,
            "fbCustomCodeDisplayNone": html.fb_custom_code_display_none,
            "fbMediaSiteCount": len(html.fb_media_site_css),
        },
        "fonts": {
            "relativeFontUrls": sorted(find_relative_font_urls(all_text)),
            "policy": "reported-only",
        },
        "cssSurface": summarize_css_surface(files),
        "sourceSiteCss": summarize_class_selector_surface(source_site_css),
        "fbStylesSiteCss": summarize_class_selector_surface(fb_styles_site_css),
        "fbStylesLibraryCss": {
            host: summarize_library_css(host, "\n".join(css_blocks))
            for host, css_blocks in sorted(html.fb_styles_library_css.items())
        },
        "scripts": summarize_scripts(html.inline_scripts, stub_files=stub_files),
        "libraryCdnDedupe": summarize_library_cdn_dedupe(html.external_scripts),
        "reservedWebflowClasses": sorted(html.reserved_classes),
        "_probe": html,
    }


def is_source_site_css(path: str) -> bool:
    name = Path(path.replace("\\", "/")).name.lower()
    if name in {"normalize.css", "webflow.css"}:
        return False
    return name.endswith(".css")


def summarize_style_findings(findings: list[StyleAttrFinding]) -> dict[str, Any]:
    return {
        "count": len(findings),
        "ixOnly": sum(1 for finding in findings if finding.classification == "ix-only"),
        "mixed": sum(1 for finding in findings if finding.classification == "mixed"),
        "samples": [style_finding_to_sample(finding) for finding in findings[:8]],
    }


def summarize_classifications(findings: list[StyleAttrFinding]) -> dict[str, int]:
    counts = {"ix-only": 0, "mixed": 0, "structural": 0}
    for finding in findings:
        counts[finding.classification] = counts.get(finding.classification, 0) + 1
    return counts


def style_finding_to_sample(finding: StyleAttrFinding) -> dict[str, Any]:
    return {
        "file": finding.file,
        "tag": finding.tag,
        "classes": finding.classes[:8],
        "classification": finding.classification,
        "ixDeclarations": finding.ix_declarations[:4],
    }


def summarize_initial_state_transport(
    html: HtmlProbe, target_specs: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Build per-target transport summaries against `html`.

    `target_specs` is the list of mode-B targets to evaluate. EXP-004 (2026-04-25):
    callers pass the dynamically-detected source target list via
    `detect_mode_b_targets(source_html)`. When `target_specs` is None we fall
    back to the legacy hardcoded `INITIAL_STATE_TARGETS` for backward
    compatibility, but no current code path relies on that fallback for mode-B
    transport — `build_manifest` resummarizes output's transport against the
    source-derived target list before contract checks run.
    """
    css_text = "\n".join(html.fb_styles_site_css)
    specs = INITIAL_STATE_TARGETS if target_specs is None else target_specs
    targets = [summarize_initial_state_target(target, html, css_text) for target in specs]
    return {
        "targets": targets,
        "sourcePresentCount": sum(1 for target in targets if target["sourceStatePresent"]),
        "transportedCount": sum(1 for target in targets if target["transported"]),
        "modeBTransportedCount": sum(1 for target in targets if target["modeBTransported"]),
        "missingCount": sum(1 for target in targets if target["sourceStatePresent"] and not target["transported"]),
        "missingModeBCount": sum(
            1 for target in targets if target["sourceStatePresent"] and not target["modeBTransported"]
        ),
    }


def summarize_static_visible_ix_state_safety(html: HtmlProbe) -> dict[str, Any]:
    css_text = "\n".join(html.fb_styles_site_css)
    marker_rules = collect_ix_state_css_rules(css_text)
    findings: list[dict[str, Any]] = []
    for element in html.elements:
        marker = element.attrs.get("data-flowbridge-ix-state")
        if not marker:
            continue
        rules = marker_rules.get(marker, [])
        hidden_declarations: list[str] = []
        for rule in rules:
            hidden_declarations.extend(rule["hiddenDeclarations"])
        hidden_declarations = sorted(set(hidden_declarations))
        content_bearing = is_content_bearing_element(element)
        exempt_reason = static_hidden_exemption_reason(element, html)
        unsafe = bool(hidden_declarations) and content_bearing and not exempt_reason
        findings.append(
            {
                "marker": marker,
                "file": element.file,
                "tag": element.tag,
                "classes": element.classes[:8],
                "textChars": element.text_chars,
                "descendantTagCount": element.descendant_tag_count,
                "hasMedia": element.has_media,
                "hasLink": element.has_link,
                "contentBearing": content_bearing,
                "hiddenDeclarations": hidden_declarations[:8],
                "ruleSelectors": [rule["selector"] for rule in rules[:4]],
                "exemptReason": exempt_reason,
                "unsafe": unsafe,
            }
        )
    unsafe_findings = sorted(
        [finding for finding in findings if finding["unsafe"]],
        key=static_visible_unsafe_sort_key,
    )
    hidden_findings = [finding for finding in findings if finding["hiddenDeclarations"]]
    return {
        "markerCount": len(findings),
        "hiddenMarkerCount": len(hidden_findings),
        "unsafeCount": len(unsafe_findings),
        "samples": findings[:12],
        "unsafeSamples": unsafe_findings[:12],
    }


_RUNTIME_GATE_PREFIX_RE = re.compile(
    r"""^\s*
        (?:html(?:\.w-mod-js)?)?         # optional html (with optional .w-mod-js)
        (?:\s*:not\(\s*\.w-mod-ix[23]\s*\))   # mandatory :not(.w-mod-ix2|3) gate
        \s+                              # mandatory descendant combinator (whitespace)
    """,
    re.VERBOSE,
)


def strip_runtime_gate_prefix(selector: str) -> tuple[str, bool]:
    """F-2 (EXP-006): Strip recognized runtime-gate prefix from a CSS selector.

    Returns ``(stripped_selector, was_gated)``. When ``was_gated`` is True, the
    rule only fires before the Webflow IX2/IX3 runtime boots and adds
    ``.w-mod-ix2`` / ``.w-mod-ix3`` to ``<html>``. Static-visible-safety
    checks should be discharged for gated rules: a content-bearing-root hide
    that disengages once the runtime boots is not a permanent invisibility
    hazard.

    Recognized gates (extend if more land later):
      - ``html:not(.w-mod-ix2)``
      - ``html:not(.w-mod-ix3)``
      - ``html.w-mod-js:not(.w-mod-ix2)``
      - ``html.w-mod-js:not(.w-mod-ix3)``
      - bare ``:not(.w-mod-ix2)`` / ``:not(.w-mod-ix3)`` prefixes
    """
    m = _RUNTIME_GATE_PREFIX_RE.match(selector)
    if not m:
        return selector, False
    return selector[m.end():].strip(), True


def summarize_static_visible_class_state_safety(html: HtmlProbe) -> dict[str, Any]:
    css_text = "\n".join(html.fb_styles_site_css)
    findings: list[dict[str, Any]] = []
    rules = iter_css_rules(css_text)
    for target in INITIAL_STATE_TARGETS:
        if target["id"] not in STATIC_VISIBLE_FORBIDDEN_CLASS_STATE_IDS:
            continue
        elements = [
            element
            for element in html.elements
            if target_matches_classes(target, element.classes) and is_content_bearing_element(element)
        ]
        if not elements:
            continue
        for raw_selectors, body in rules:
            hidden_declarations = sorted(set(hidden_static_declarations(body)))
            if not hidden_declarations:
                continue
            selector_parts = [part.strip() for part in raw_selectors.split(",")]
            # F-2 (EXP-006): strip runtime-gate prefix per selector part. A part is a
            # real hazard candidate only if it (a) targets the forbidden class-state
            # AND (b) is NOT runtime-gated. Gated parts disengage once the runtime
            # boots (.w-mod-ix2/.w-mod-ix3 lands on <html>) and the cascade falls
            # back to source CSS — that is the safety mechanism by design.
            ungated_matching_parts = []
            for part in selector_parts:
                stripped, was_gated = strip_runtime_gate_prefix(part)
                test_part = stripped if was_gated else part
                if not selector_part_targets(test_part, [target["selector"]]):
                    continue
                if was_gated:
                    continue  # discharged by runtime gate
                ungated_matching_parts.append(part)
            if not ungated_matching_parts:
                continue
            findings.append(
                {
                    "id": target["id"],
                    "selector": raw_selectors,
                    "hiddenDeclarations": hidden_declarations[:8],
                    "elementCount": len(elements),
                    "contentSamples": [
                        {
                            "file": element.file,
                            "tag": element.tag,
                            "classes": element.classes[:8],
                            "textChars": element.text_chars,
                            "descendantTagCount": element.descendant_tag_count,
                            "hasMedia": element.has_media,
                            "hasLink": element.has_link,
                        }
                        for element in elements[:3]
                    ],
                }
            )
    return {
        "unsafeCount": len(findings),
        "unsafeSamples": findings[:12],
    }


def static_visible_unsafe_sort_key(finding: dict[str, Any]) -> tuple[int, int, int, str]:
    declarations = ",".join(finding["hiddenDeclarations"])
    if any(token in declarations for token in ("display:none", "visibility:hidden", "visibility:collapse", "opacity:0")):
        severity = 0
    elif any(token in declarations for token in ("height:0", "width:0", "max-height:0", "max-width:0")):
        severity = 1
    else:
        severity = 2
    content_weight = finding["descendantTagCount"] + finding["textChars"]
    return (severity, -content_weight, -int(bool(finding["hasMedia"] or finding["hasLink"])), finding["marker"])


def enumerate_source_dom_classes(html: HtmlProbe) -> set[str]:
    """Every non-framework class token appearing on any element in the HTML tree.
    Excludes Webflow framework prefixes (w-*) and FlowBridge pretreat hosts (fb-*)."""
    classes: set[str] = set()
    seen = [html.elements, [attr for attr in html.style_attrs]]
    for bucket in seen:
        for item in bucket:
            for cls in item.classes:
                if not cls:
                    continue
                if any(cls.startswith(pfx) for pfx in L7_FRAMEWORK_CLASS_PREFIXES):
                    continue
                classes.add(cls)
    return classes


def parse_simple_class_chain_selector(selector: str) -> list[str] | None:
    """If `selector` is a simple class-chain (e.g. `.foo`, `.foo.bar`, `.a.b.c`), return
    the list of class tokens in order. Otherwise return None.

    Rejects: tag selectors, IDs, attribute selectors, pseudo-classes/elements,
    descendant/child/sibling combinators, wildcards — anything more specific than
    a pure class chain."""
    sel = selector.strip()
    if not sel or not sel.startswith("."):
        return None
    # Allow only . and [-_a-zA-Z0-9] characters in a class chain selector
    if re.search(r"[^\.\-_a-zA-Z0-9]", sel):
        return None
    tokens = [t for t in sel.split(".") if t]
    if not tokens:
        return None
    # Each token must be a valid CSS identifier
    for t in tokens:
        if not re.fullmatch(r"[A-Za-z_][-_A-Za-z0-9]*", t):
            return None
    return tokens


_COLLAPSE_DETECTORS = {
    "display-none": lambda v: v.strip().lower() == "none",
    "visibility-hidden": lambda v: v.strip().lower() == "hidden",
    "opacity-zero": lambda v: v.strip() in {"0", "0.0", "0%"},
    "height-zero": lambda v: is_zero_css_length(v.strip().lower()),
    "width-zero": lambda v: is_zero_css_length(v.strip().lower()),
    "pointer-events-none": lambda v: v.strip().lower() == "none",
}


def _classify_collapse_declarations(decls: dict[str, Any], *, include_pointer_events: bool) -> list[str]:
    """Return the list of collapse kinds detected in the given declaration dict.
    `decls` is the output of `declarations_by_property`, which maps property name to
    `(value_without_important, important_flag)`. `include_pointer_events=True` adds
    `pointer-events: none` (combo inline check). `include_pointer_events=False`
    restricts to visual collapses (global CSS check — a global `pointer-events: none`
    is often legitimate)."""
    kinds: list[str] = []
    prop_to_kind = {
        "display": "display-none",
        "visibility": "visibility-hidden",
        "opacity": "opacity-zero",
        "height": "height-zero",
        "width": "width-zero",
    }
    if include_pointer_events:
        prop_to_kind["pointer-events"] = "pointer-events-none"
    for prop, kind in prop_to_kind.items():
        entry = decls.get(prop)
        if not entry:
            continue
        # declarations_by_property returns tuple (value, important) OR a plain string in
        # older code paths. Handle both defensively.
        if isinstance(entry, tuple):
            value = entry[0]
        elif isinstance(entry, list):
            value = entry[0] if entry else ""
        else:
            value = str(entry)
        cleaned = strip_important(value) if isinstance(value, str) else str(value)
        if _COLLAPSE_DETECTORS[kind](cleaned):
            kinds.append(kind)
    return kinds


def _contains_important(raw_style: str) -> bool:
    return "!important" in raw_style.lower()


def collect_class_collapse_rules_from_css(css_text: str) -> list[dict[str, Any]]:
    """Scan an arbitrary CSS text blob for top-level simple class-chain rules whose
    body carries a visual collapse property. Returns list of findings, each with
    `selector`, `classes` (token list), and `collapseKinds`. Used for BOTH the
    output-scan (to find candidate L-7 violations) AND the source-scan (to filter
    source-preserved collapses out of the FAIL set)."""
    out: list[dict[str, Any]] = []
    for raw_selectors, body in iter_css_rules(css_text):
        for selector_part in [part.strip() for part in raw_selectors.split(",")]:
            chain = parse_simple_class_chain_selector(selector_part)
            if chain is None:
                continue
            decls = declarations_by_property(body)
            kinds = _classify_collapse_declarations(decls, include_pointer_events=False)
            if not kinds:
                continue
            out.append(
                {
                    "selector": selector_part,
                    "classes": chain,
                    "collapseKinds": kinds,
                }
            )
    return out


def summarize_overlay_neutralization(files: list[TextFile], html: HtmlProbe) -> dict[str, Any]:
    """L-7 universal check summary (EXP-003 rewrite — class-agnostic).

    GLOBAL findings: every top-level (non-@media) simple class-chain CSS rule in any
    output style host (fb-styles-site + fb-styles-{library}) whose body contains
    a visual collapse property (display:none, visibility:hidden, opacity:0, height:0, width:0).
    Rule keeps its class-chain tokens for later intersection with source-DOM classes.

    COMBO findings: every source element in html.style_attrs with ≥ 2 non-framework
    classes AND a data-w-id attribute AND an inline style containing `!important`
    visual collapse properties or `pointer-events: none`. Source-origin IX2 starts
    without `!important` are exempt (covered by L-8)."""
    # Output style hosts only — NOT the full file set. fb-media-site is intentionally
    # excluded because @media-block rules are not "global class-based collapses".
    host_css_blocks: list[tuple[str, str]] = []  # (host_label, css_text)
    for i, block in enumerate(html.fb_styles_site_css):
        host_css_blocks.append((f"fb-styles-site[{i}]", block))
    for lib, blocks in html.fb_styles_library_css.items():
        for i, block in enumerate(blocks):
            host_css_blocks.append((f"fb-styles-{lib}[{i}]", block))

    global_findings: list[dict[str, Any]] = []
    for host_label, css_text in host_css_blocks:
        for raw_selectors, body in iter_css_rules(css_text):
            # Only consider simple class-chain selectors. Comma-separated groups: any part
            # that parses as a simple class-chain is eligible.
            for selector_part in [part.strip() for part in raw_selectors.split(",")]:
                chain = parse_simple_class_chain_selector(selector_part)
                if chain is None:
                    continue
                decls = declarations_by_property(body)
                kinds = _classify_collapse_declarations(decls, include_pointer_events=False)
                if not kinds:
                    continue
                decl_dump: dict[str, str] = {}
                for p in ("display", "visibility", "opacity", "height", "width"):
                    entry = decls.get(p)
                    if entry is None:
                        decl_dump[p] = ""
                    elif isinstance(entry, tuple):
                        decl_dump[p] = entry[0]
                    elif isinstance(entry, list):
                        decl_dump[p] = entry[0] if entry else ""
                    else:
                        decl_dump[p] = str(entry)
                global_findings.append(
                    {
                        "host": host_label,
                        "selector": selector_part,
                        "classes": chain,
                        "collapseKinds": kinds,
                        "declarations": decl_dump,
                    }
                )

    combo_findings: list[dict[str, Any]] = []
    for finding in html.style_attrs:
        non_fw_classes = [c for c in finding.classes if c and not any(c.startswith(p) for p in L7_FRAMEWORK_CLASS_PREFIXES)]
        if len(non_fw_classes) < 2:
            continue
        if "data-w-id" not in (finding.attrs or {}):
            continue
        decls = declarations_by_property(finding.style)
        kinds = _classify_collapse_declarations(decls, include_pointer_events=True)
        if not kinds:
            continue
        # Source-origin IX2 starts are usually !important-free. Only flag if the inline
        # style carries `!important` (skill injection signal) OR uses `pointer-events: none`
        # (not an IX2-runtime-origin property).
        has_important = _contains_important(finding.style)
        has_pointer_events_none = "pointer-events-none" in kinds
        if not (has_important or has_pointer_events_none):
            continue
        combo_findings.append(
            {
                "file": finding.file,
                "tag": finding.tag,
                "classes": finding.classes,
                "nonFrameworkClasses": non_fw_classes,
                "collapseKinds": kinds,
                "hasImportant": has_important,
            }
        )

    return {
        "globalCollapseCount": len(global_findings),
        "comboCollapseCount": len(combo_findings),
        # Full finding lists — the check does its own filtering against source-preserved
        # collapse signatures, so we cannot truncate here without breaking correctness.
        "globalFindings": global_findings,
        "comboFindings": combo_findings,
        # Back-compat preview samples (first 8) for inline evidence strings.
        "globalSamples": global_findings[:8],
        "comboSamples": combo_findings[:8],
    }


def selector_targets_class(selector: str, class_name: str) -> bool:
    return bool(re.search(rf"(?<![-_a-zA-Z0-9])\.{re.escape(class_name)}(?![-_a-zA-Z0-9])", selector))


def summarize_lazy_video(html: HtmlProbe) -> dict[str, Any]:
    data_src_sources = [source for source in html.video_sources if source["attrs"].get("data-src", "").strip()]
    missing_src = [source for source in data_src_sources if not source["attrs"].get("src", "").strip()]
    mismatched_src = [
        source
        for source in data_src_sources
        if source["attrs"].get("src", "").strip()
        and source["attrs"].get("src", "").strip() != source["attrs"].get("data-src", "").strip()
    ]
    marker_sources = [
        source for source in data_src_sources if source["attrs"].get("data-flowbridge-inline-video-src") == "true"
    ]
    blocked_autoplay = [
        video
        for video in html.video_elements
        if "autoplay" in video["attrs"]
        and (
            video["attrs"].get("loading", "").strip().lower() == "lazy"
            or video["attrs"].get("preload", "").strip().lower() == "none"
        )
    ]
    autoplay_markers = [
        video for video in html.video_elements if video["attrs"].get("data-flowbridge-inline-video-autoplay") == "true"
    ]
    retained_loaders = [summarize_lazy_video_script(entry["script"]) for entry in html.inline_scripts]
    retained_loaders = [loader for loader in retained_loaders if loader["targetsVideoLazy"]]

    return {
        "videoCount": len(html.video_elements),
        "dataSrcSourceCount": len(data_src_sources),
        "dataSrcMissingSrcCount": len(missing_src),
        "dataSrcMismatchCount": len(mismatched_src),
        "dataSrcMarkerCount": len(marker_sources),
        "autoplayLazyBlockedCount": len(blocked_autoplay),
        "autoplayMarkerCount": len(autoplay_markers),
        "retainedLazyLoaderCount": len(retained_loaders),
        "unsafeRetainedLazyLoaderCount": sum(1 for loader in retained_loaders if loader["unsafeLoadCall"]),
        "missingSrcSamples": lazy_source_samples(missing_src),
        "mismatchSamples": lazy_source_samples(mismatched_src),
        "blockedAutoplaySamples": lazy_video_samples(blocked_autoplay),
        "retainedLazyLoaderSamples": retained_loaders[:4],
    }


def summarize_lazy_video_script(script: str) -> dict[str, Any]:
    targets_video_lazy = bool(re.search(r"video\.lazy", script))
    load_positions = [match.start() for match in re.finditer(r"(?:\bvideo\s*\.\s*load|\.\s*load)\s*\(", script)]
    guard_patterns = (
        r"data-flowbridge-inline-video-src",
        r"flowbridgeInlineVideoSrc",
        r"getAttribute\s*\(\s*['\"]src['\"]\s*\)",
        r"\.src\s*={2,3}\s*[^;\n]*\.dataset\.src",
        r"\.src\s*={2,3}\s*[^;\n]*getAttribute\s*\(\s*['\"]data-src['\"]\s*\)",
        r"already[^;\n]{0,80}(?:lazy|loaded|src|ready|delaz)",
    )
    guard_positions = [
        match.start()
        for pattern in guard_patterns
        for match in re.finditer(pattern, script, flags=re.I)
    ]
    first_load = min(load_positions) if load_positions else None
    first_guard = min(guard_positions) if guard_positions else None
    guard_before_load = first_load is None or (first_guard is not None and first_guard < first_load)
    return {
        "targetsVideoLazy": targets_video_lazy,
        "loadCallCount": len(load_positions),
        "guardBeforeLoad": guard_before_load,
        "unsafeLoadCall": targets_video_lazy and bool(load_positions) and not guard_before_load,
        "snippet": compact_script_snippet(script),
    }


def compact_script_snippet(script: str) -> str:
    return re.sub(r"\s+", " ", script).strip()[:180]


def lazy_source_samples(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    for source in sources[:6]:
        attrs = source["attrs"]
        samples.append(
            {
                "file": source["file"],
                "dataSrc": attrs.get("data-src", ""),
                "src": attrs.get("src", ""),
                "marker": attrs.get("data-flowbridge-inline-video-src", ""),
            }
        )
    return samples


def lazy_video_samples(videos: list[dict[str, Any]]) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    for video in videos[:6]:
        attrs = video["attrs"]
        samples.append(
            {
                "file": video["file"],
                "loading": attrs.get("loading", ""),
                "preload": attrs.get("preload", ""),
                "marker": attrs.get("data-flowbridge-inline-video-autoplay", ""),
            }
        )
    return samples


def collect_ix_state_css_rules(css_text: str) -> dict[str, list[dict[str, Any]]]:
    rules_by_marker: dict[str, list[dict[str, Any]]] = {}
    for raw_selectors, body in iter_css_rules(css_text):
        hidden_declarations = hidden_static_declarations(body)
        if not hidden_declarations:
            continue
        for selector in [part.strip() for part in raw_selectors.split(",")]:
            # F-2 (EXP-006): runtime-gated rules are discharged. A rule prefixed
            # with `html:not(.w-mod-ix2)` (or sibling gate patterns) only fires
            # before the Webflow runtime boots and disengages once
            # `.w-mod-ix2`/`.w-mod-ix3` lands on `<html>` — so the
            # static-visible-ix-state-safety check, which presumes a permanent
            # hide, must skip it. The same helper governs both the class-state
            # and ix-state safety paths so behavior stays symmetric.
            _, gated = strip_runtime_gate_prefix(selector)
            if gated:
                continue
            for marker in ix_state_markers_in_selector(selector):
                rules_by_marker.setdefault(marker, []).append(
                    {
                        "selector": selector,
                        "hiddenDeclarations": hidden_declarations,
                    }
                )
    return rules_by_marker


def ix_state_markers_in_selector(selector: str) -> list[str]:
    markers: list[str] = []
    for match in re.finditer(r"\[data-flowbridge-ix-state\s*=\s*([\"'])(.*?)\1\s*\]", selector):
        markers.append(match.group(2))
    for match in re.finditer(r"\[data-flowbridge-ix-state\s*=\s*([^\]\s\"']+)\s*\]", selector):
        markers.append(match.group(1))
    return markers


def hidden_static_declarations(style: str) -> list[str]:
    hidden: list[str] = []
    for name, value, _raw in parse_declarations(style):
        clean = strip_important(value).strip().lower()
        if name == "opacity" and is_zero_css_number(clean):
            hidden.append(f"{name}:0")
        elif name == "visibility" and clean in {"hidden", "collapse"}:
            hidden.append(f"{name}:{clean}")
        elif name == "display" and clean == "none":
            hidden.append("display:none")
        elif name in {"width", "height", "max-width", "max-height"} and is_zero_css_length(clean):
            hidden.append(f"{name}:0")
        elif name in {"transform", "-webkit-transform", "-moz-transform", "-ms-transform"} and is_offscreen_transform(clean):
            hidden.append(f"{name}:offscreen-transform")
    return hidden


def is_zero_css_number(value: str) -> bool:
    return value in {"0", "0.0", ".0"}


def is_zero_css_length(value: str) -> bool:
    return bool(re.fullmatch(r"0(?:\.0+)?(?:px|rem|em|%|vh|vw|vmin|vmax)?", value))


def is_offscreen_transform(value: str) -> bool:
    normalized = normalize_css_fragment(value)
    if "translate" not in normalized:
        return False
    return bool(
        re.search(r"translate(?:3d|x|y)?\([^)]*(?:-100%|100%|110%|-110%|100vh|-100vh|100vw|-100vw)", normalized)
    )


def is_content_bearing_element(element: ElementFinding) -> bool:
    if is_flowbridge_structural_host(element.classes):
        return False
    if element.tag in MEDIA_TAGS or element.tag in INTERACTIVE_TAGS:
        return True
    return element.text_chars > 0 or element.has_media or element.has_link


def static_hidden_exemption_reason(element: ElementFinding, html: HtmlProbe) -> str | None:
    if is_flowbridge_structural_host(element.classes):
        return "flowbridge-structural-host"
    if any(class_set_contains(element.classes, classes) for classes in STATIC_HIDDEN_CHROME_CLASSES):
        return "documented-closed-navigation-chrome"
    for root_class, host in COMPONENT_FALLBACK_HOSTS.items():
        if root_class not in element.classes:
            continue
        fallback = summarize_library_css(host, "\n".join(html.fb_styles_library_css.get(host, []))).get("fallback", {})
        if fallback.get("status") == "pass":
            return f"{root_class}-static-visible-fallback"
    return None


def summarize_initial_state_target(target: dict[str, Any], html: HtmlProbe, css_text: str) -> dict[str, Any]:
    required = tuple(target["required"])
    style_matches = [
        finding
        for finding in html.style_attrs
        if target_matches_classes(target, finding.classes)
    ]
    element_matches = [
        element
        for element in html.elements
        if target_matches_classes(target, element.classes)
    ]

    source_state_present = any(style_has_fragments(finding.style, required) for finding in style_matches)
    preserved_inline = source_state_present

    marker_selectors = sorted(
        {
            f'[data-flowbridge-ix-state="{element.attrs["data-flowbridge-ix-state"]}"]'
            for element in element_matches
            if element.attrs.get("data-flowbridge-ix-state")
        }
    )
    class_selectors = target_class_selectors(target)
    css_selectors = marker_selectors + class_selectors
    css_transport = summarize_css_transport(css_text, css_selectors, class_selectors, required)
    converted_css = css_transport["present"]
    converted_css_cascade_safe = css_transport["cascadeSafe"]
    static_visible_fallback = has_static_visible_content_fallback(css_text, element_matches, html)

    component_fallback = False
    fallback_host = target.get("component_fallback_host")
    if fallback_host:
        fallback = summarize_library_css(fallback_host, "\n".join(html.fb_styles_library_css.get(fallback_host, []))).get("fallback", {})
        component_fallback = fallback.get("status") == "pass"

    mode_b_transported = converted_css_cascade_safe or component_fallback or static_visible_fallback

    if converted_css_cascade_safe:
        classification = "converted-to-css/embed"
    elif converted_css:
        classification = "converted-css-cascade-risk"
    elif component_fallback:
        classification = "component-root-fallback"
    elif static_visible_fallback:
        classification = "static-visible-content-fallback"
    elif preserved_inline:
        classification = "preserved-inline"
    elif element_matches:
        classification = "stripped-without-equivalent-transport"
    else:
        classification = "unknown"

    return {
        "id": target["id"],
        "selector": target["selector"],
        "sourceStatePresent": source_state_present,
        "transported": preserved_inline or converted_css or component_fallback,
        "modeBTransported": mode_b_transported,
        "classification": classification,
        "elementCount": len(element_matches),
        "cssSelectorsChecked": css_selectors[:8],
        "cssTransport": css_transport,
        "staticVisibleFallback": static_visible_fallback,
        "requiredFragments": list(required),
    }


def detect_mode_b_targets(html: HtmlProbe) -> list[dict[str, Any]]:
    """EXP-004 (2026-04-25): structural detection of mode-B IX2-hidden initial-state targets.

    A source element qualifies as a mode-B target IFF all of the following hold:
      1. Its inline `style=""` contains at least one hidden-on-load declaration
         (display:none, visibility:hidden|collapse, opacity:0, off-screen
         translate, zero-scale transform, fully-clipped clip-path, or zero
         collapse on a sizing property). [§Detection criteria #2]
      2. The inline style is IX-shaped per `classify_style_attr` (the vendor-prefix
         transform quadruple or other IX2-engine fingerprints) OR the element
         carries a `data-w-id` attribute. This is a narrowing filter that
         excludes static utility-class collapses (e.g. a plain
         `<div style="display:none">` placeholder) which are not IX2 initial
         states.
      3. The element is not itself an `fb-*` structural host (skips
         already-pretreated scaffolding when this probe is re-run on output).
         [§Detection criteria #3]
      4. The element has at least one non-framework class token; without a
         stable class chain we cannot match it across source/output via class
         selectors.

    Skill-prompt divergence (logged in EXP-004 open-questions): the invoking
    prompt's §Detection criteria #1 required `data-w-id` strictly. Primary-source
    evidence (the synthetic self-test fixture, the MNZ Protected Set ratio of
    164 IX-shaped inline styles to 35 `data-w-id`s, and the hardcoded baseline
    catalog itself) showed that requirement systematically excludes legitimate
    IX2 hidden initial states on descendants of timelined ancestors. We
    relaxed criterion #1 to (IX-shaped OR data-w-id) so the dynamic detector
    matches the hardcoded baseline's intent.

    Returns target dicts shape-compatible with `summarize_initial_state_target`'s
    legacy consumer: `id`, `selector`, `classes`, `required`, optional
    `component_fallback_host`. Per-detection provenance is preserved on
    `dynamic`, `hiddenSignatures`, `dataWId`, `ixShaped`, and `sourceFile` keys.

    The returned list is the source-derived target catalog; `build_manifest`
    threads it to output transport scanning so contract-check IDs align.
    """
    targets: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for finding in html.style_attrs:
        if any(cls.startswith("fb-") for cls in finding.classes):
            continue
        signatures = mode_b_hidden_on_load_signatures(finding.style)
        if not signatures:
            continue
        ix_shaped = bool(finding.ix_declarations)
        has_data_w_id = "data-w-id" in finding.attrs
        if not (ix_shaped or has_data_w_id):
            # Narrowing filter: a static utility collapse (e.g. plain
            # `display:none` without IX2 fingerprints and without `data-w-id`)
            # is not a mode-B target. This matches the hardcoded baseline's
            # intent — every legacy entry corresponded to an IX-shaped style
            # or a data-w-id-bearing element.
            continue
        non_framework_classes = [
            cls
            for cls in finding.classes
            if not (cls.startswith("w-") or cls.startswith("_w-") or cls.startswith("fb-"))
        ]
        if not non_framework_classes:
            continue
        class_chain = tuple(non_framework_classes)
        slug = "-".join(class_chain) or finding.tag
        idx = 0
        target_id = f"{finding.tag}-{slug}-{idx}"
        while target_id in seen_ids:
            idx += 1
            target_id = f"{finding.tag}-{slug}-{idx}"
        seen_ids.add(target_id)
        required = tuple(mode_b_required_fragments(finding.style))
        if not required:
            continue
        target: dict[str, Any] = {
            "id": target_id,
            "selector": "." + ".".join(class_chain),
            "classes": class_chain,
            "required": required,
            "dynamic": True,
            "hiddenSignatures": signatures,
            "ixShaped": ix_shaped,
            "dataWId": finding.attrs.get("data-w-id", ""),
            "sourceFile": finding.file,
            "sourceTag": finding.tag,
        }
        for root_class, host in COMPONENT_FALLBACK_HOSTS.items():
            if root_class in class_chain:
                target["component_fallback_host"] = host
                break
        targets.append(target)
    return targets


def mode_b_hidden_on_load_signatures(style: str) -> list[str]:
    """Return labels of hidden-on-load declarations found in `style` (or [] if none).

    Labels are signature-shaped (e.g. `opacity:0`, `transform:offscreen-translate`),
    used for target provenance and the d007 anchor check. They are NOT used as
    CSS-fragment match keys — `mode_b_required_fragments` produces those.
    """
    signatures: list[str] = []
    for name, value, _raw in parse_declarations(style):
        clean = strip_important(value).strip().lower()
        if name == "display" and clean == "none":
            signatures.append("display:none")
        elif name == "visibility" and clean in {"hidden", "collapse"}:
            signatures.append(f"visibility:{clean}")
        elif name == "opacity" and is_zero_css_number(clean):
            signatures.append("opacity:0")
        elif name in MODE_B_VENDOR_TRANSFORM_PROPERTIES:
            if is_offscreen_transform(clean):
                signatures.append(f"{name}:offscreen-translate")
            elif is_zero_scale_transform(clean):
                signatures.append(f"{name}:zero-scale")
        elif name == "clip-path" and is_fully_clipped_clip_path(clean):
            signatures.append("clip-path:inset-full")
        elif name in MODE_B_HIDDEN_SIZING_PROPERTIES and is_zero_css_length(clean):
            signatures.append(f"{name}:0")
    # de-dupe while preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for sig in signatures:
        if sig in seen:
            continue
        seen.add(sig)
        deduped.append(sig)
    return deduped


def mode_b_required_fragments(style: str) -> list[str]:
    """Return the canonical CSS-shaped declarations that triggered hidden-on-load
    detection. Output is fed to `summarize_css_transport` (substring-matched
    after `normalize_css_fragment`), so fragments must be tolerant of
    canonicalization the converter or paste pipeline may apply.

    Specifically: for `transform`, emit ONLY the triggering primitive call
    (e.g. `transform: translate3d(-100%, 0, 0)`) instead of the full source
    value, because Webflow / IX2 canonicalization frequently strips identity
    `scale3d(1,1,1) rotateX(0)...` companions. The hardcoded
    `INITIAL_STATE_TARGETS` baseline used the same short-fragment approach
    and we preserve that contract.
    """
    fragments: list[str] = []
    seen_props: set[str] = set()
    for name, value, _raw in parse_declarations(style):
        clean_value = strip_important(value).strip()
        clean_lower = clean_value.lower()
        canonical_name = "transform" if name in MODE_B_VENDOR_TRANSFORM_PROPERTIES else name
        if canonical_name in seen_props:
            continue
        if name == "display" and clean_lower == "none":
            fragments.append("display: none")
            seen_props.add("display")
        elif name == "visibility" and clean_lower in {"hidden", "collapse"}:
            fragments.append(f"visibility: {clean_lower}")
            seen_props.add("visibility")
        elif name == "opacity" and is_zero_css_number(clean_lower):
            fragments.append("opacity: 0")
            seen_props.add("opacity")
        elif name in MODE_B_VENDOR_TRANSFORM_PROPERTIES:
            primitive = _extract_offscreen_translate(clean_value) or _extract_zero_scale_call(clean_value)
            if primitive:
                fragments.append(f"transform: {primitive}")
                seen_props.add("transform")
        elif name in MODE_B_HIDDEN_SIZING_PROPERTIES and is_zero_css_length(clean_lower):
            fragments.append(f"{name}: {clean_value}")
            seen_props.add(name)
        elif name == "clip-path" and is_fully_clipped_clip_path(clean_lower):
            fragments.append(f"clip-path: {clean_value}")
            seen_props.add("clip-path")
    return fragments


def _extract_offscreen_translate(value: str) -> str | None:
    match = re.search(
        r"translate(?:3d|x|y)?\([^)]*(?:-100%|100%|110%|-110%|100vh|-100vh|100vw|-100vw|-200%|200%)[^)]*\)",
        value,
        re.I,
    )
    return match.group(0) if match else None


def _extract_zero_scale_call(value: str) -> str | None:
    match = re.search(r"scale(?:3d)?\(\s*0(?:\.0+)?(?:[\s,)]|\.0+[\s,)])[^)]*\)?", value, re.I)
    return match.group(0) if match else None


def is_zero_scale_transform(value: str) -> bool:
    normalized = normalize_css_fragment(value)
    if "scale" not in normalized:
        return False
    return bool(re.search(r"scale(?:3d)?\(\s*0(?:[\s,)]|\.0+[\s,)])", normalized))


def is_fully_clipped_clip_path(value: str) -> bool:
    normalized = normalize_css_fragment(value).replace(" ", "")
    return "inset(100%" in normalized


def has_static_visible_content_fallback(css_text: str, elements: list[ElementFinding], html: HtmlProbe) -> bool:
    for element in elements:
        marker = element.attrs.get("data-flowbridge-ix-state")
        if not marker:
            continue
        if not is_content_bearing_element(element):
            continue
        if static_hidden_exemption_reason(element, html):
            continue
        if marker_has_hidden_static_rule(css_text, marker):
            continue
        if marker_has_css_rule(css_text, marker):
            return True
    return False


def marker_has_css_rule(css_text: str, marker: str) -> bool:
    return any(marker in ix_state_markers_in_selector(part.strip()) for raw, _body in iter_css_rules(css_text) for part in raw.split(","))


def marker_has_hidden_static_rule(css_text: str, marker: str) -> bool:
    for raw_selectors, body in iter_css_rules(css_text):
        if not hidden_static_declarations(body):
            continue
        for part in raw_selectors.split(","):
            if marker in ix_state_markers_in_selector(part.strip()):
                return True
    return False


def class_set_contains(classes: list[str], required: tuple[str, ...]) -> bool:
    class_set = set(classes)
    return all(cls in class_set for cls in required)


def target_matches_classes(target: dict[str, Any], classes: list[str]) -> bool:
    required = tuple(target["classes"])
    if target.get("classMatch") == "exact":
        return len(classes) == len(required) and set(classes) == set(required)
    return class_set_contains(classes, required)


def target_class_selectors(target: dict[str, Any]) -> list[str]:
    selector = target["selector"]
    selectors = [selector]
    classes = tuple(target["classes"])
    if len(classes) > 1:
        selectors.append("." + ".".join(classes))
    return sorted(set(selectors))


def style_has_fragments(style: str, fragments: tuple[str, ...]) -> bool:
    normalized = normalize_css_fragment(style)
    return all(normalize_css_fragment(fragment) in normalized for fragment in fragments)


def summarize_css_transport(
    css_text: str,
    selectors: list[str],
    conflict_selectors: list[str],
    fragments: tuple[str, ...],
) -> dict[str, Any]:
    matches = find_css_transport_matches(css_text, selectors, conflict_selectors, fragments)
    safe_matches = [match for match in matches if match["cascadeSafe"]]
    return {
        "present": bool(matches),
        "cascadeSafe": bool(safe_matches),
        "matches": matches[:4],
    }


def find_css_transport_matches(
    css_text: str,
    selectors: list[str],
    conflict_selectors: list[str],
    fragments: tuple[str, ...],
) -> list[dict[str, Any]]:
    normalized_selectors = {normalize_css_fragment(selector) for selector in selectors}
    rules = iter_css_rules(css_text)
    matches: list[dict[str, Any]] = []
    for index, (raw_selectors, body) in enumerate(rules):
        selector_parts_raw = [part.strip() for part in raw_selectors.split(",")]
        selector_parts = [normalize_css_fragment(part) for part in selector_parts_raw]
        if not any(css_selector_matches(part, normalized_selectors) for part in selector_parts):
            continue
        if not style_has_fragments(body, fragments):
            continue

        matched_selector = next(
            raw_part
            for raw_part, normalized_part in zip(selector_parts_raw, selector_parts)
            if css_selector_matches(normalized_part, normalized_selectors)
        )
        transport_declarations = declarations_by_property(body)
        unsafe_properties = [
            prop
            for prop in required_properties(fragments)
            if not transport_property_is_cascade_safe(
                prop,
                fragments,
                index,
                matched_selector,
                transport_declarations,
                rules,
                conflict_selectors,
            )
        ]
        matches.append(
            {
                "selector": matched_selector,
                "ruleIndex": index,
                "specificity": list(selector_specificity(matched_selector)),
                "cascadeSafe": not unsafe_properties,
                "unsafeProperties": unsafe_properties,
            }
        )
    return matches


def transport_property_is_cascade_safe(
    prop: str,
    fragments: tuple[str, ...],
    transport_index: int,
    transport_selector: str,
    transport_declarations: dict[str, tuple[str, bool]],
    rules: list[tuple[str, str]],
    conflict_selectors: list[str],
) -> bool:
    declaration = transport_declarations.get(prop)
    if declaration is None:
        return False
    value, important = declaration
    if important:
        return True

    transport_specificity = selector_specificity(transport_selector)
    for conflict_index, raw_selectors, body in iter_conflicting_property_rules(rules, conflict_selectors, prop, fragments):
        for conflict_selector in [part.strip() for part in raw_selectors.split(",")]:
            if not selector_part_targets(conflict_selector, conflict_selectors):
                continue
            conflict_specificity = selector_specificity(conflict_selector)
            if conflict_specificity > transport_specificity:
                return False
            if conflict_specificity == transport_specificity and conflict_index > transport_index:
                return False
    return True


def iter_conflicting_property_rules(
    rules: list[tuple[str, str]],
    conflict_selectors: list[str],
    prop: str,
    required_fragments: tuple[str, ...],
) -> list[tuple[int, str, str]]:
    conflicts: list[tuple[int, str, str]] = []
    for index, (raw_selectors, body) in enumerate(rules):
        if not any(selector_part_targets(part.strip(), conflict_selectors) for part in raw_selectors.split(",")):
            continue
        declarations = declarations_by_property(body)
        if prop not in declarations:
            continue
        value, important = declarations[prop]
        if important:
            conflicts.append((index, raw_selectors, body))
            continue
        if not declaration_matches_any_required_fragment(prop, value, required_fragments):
            conflicts.append((index, raw_selectors, body))
    return conflicts


def declarations_by_property(style: str) -> dict[str, tuple[str, bool]]:
    declarations: dict[str, tuple[str, bool]] = {}
    for name, value, _raw in parse_declarations(style):
        important = "!important" in value.lower()
        declarations[name] = (strip_important(value), important)
    return declarations


def strip_important(value: str) -> str:
    return re.sub(r"!\s*important", "", value, flags=re.I).strip()


def required_properties(fragments: tuple[str, ...]) -> list[str]:
    props: list[str] = []
    for fragment in fragments:
        if ":" not in fragment:
            continue
        prop = fragment.split(":", 1)[0].strip().lower()
        if prop and prop not in props:
            props.append(prop)
    return props


def declaration_matches_any_required_fragment(prop: str, value: str, fragments: tuple[str, ...]) -> bool:
    normalized_declaration = normalize_css_fragment(f"{prop}:{value}")
    return any(
        normalize_css_fragment(fragment) in normalized_declaration
        for fragment in fragments
        if fragment.split(":", 1)[0].strip().lower() == prop
    )


def selector_part_targets(selector_part: str, expected_selectors: list[str]) -> bool:
    normalized_expected = {normalize_css_fragment(selector) for selector in expected_selectors}
    return css_selector_matches(normalize_css_fragment(selector_part), normalized_expected)


def selector_specificity(selector: str) -> tuple[int, int, int]:
    selector = re.sub(r":where\([^)]*\)", "", selector)
    ids = len(re.findall(r"#[A-Za-z_][\w-]*", selector))
    classes_attrs_pseudos = len(re.findall(r"\.[A-Za-z_-][\w-]*|\[[^\]]+\]|:(?!:)[A-Za-z_-][\w-]*", selector))
    stripped = re.sub(r"#[A-Za-z_][\w-]*|\.[A-Za-z_-][\w-]*|\[[^\]]+\]|:{1,2}[A-Za-z_-][\w-]*\([^)]*\)|:{1,2}[A-Za-z_-][\w-]*", " ", selector)
    elements = len(re.findall(r"(?<![-_])\b[a-zA-Z][a-zA-Z0-9-]*\b", stripped))
    return (ids, classes_attrs_pseudos, elements)


def css_selector_matches(selector_part: str, expected_selectors: set[str]) -> bool:
    return any(
        selector_part == expected
        or selector_part.endswith(expected)
        or selector_part.endswith(" " + expected)
        for expected in expected_selectors
    )


def find_relative_font_urls(text: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r"url\(\s*(['\"]?)([^)'\"\s]+)\1\s*\)", text, re.I):
        url = match.group(2).strip()
        lower = url.split("?", 1)[0].lower()
        if lower.endswith(FONT_EXTENSIONS) and is_relative_url(url):
            found.add(url)
    return found


def summarize_css_surface(files: list[TextFile]) -> dict[str, Any]:
    css_text = "\n".join(file.text for file in files if file.path.lower().endswith((".css", ".html")))
    media_queries = [normalize_media_query(match.group(1)) for match in re.finditer(r"@media\s+([^{]+)\{", css_text)]
    return {
        "fontFaceCount": len(re.findall(r"@font-face\b", css_text, re.I)),
        "mediaRuleCount": len(media_queries),
        "canonicalMediaRuleCount": sum(1 for query in media_queries if query in CANONICAL_MEDIA),
        "nonCanonicalMediaRuleCount": sum(1 for query in media_queries if query and query not in CANONICAL_MEDIA),
        "styleTagCount": len(re.findall(r"<style\b", css_text, re.I)),
    }


def summarize_class_selector_surface(css_text: str) -> dict[str, Any]:
    classes = extract_site_class_selectors(css_text)
    base_classes = extract_site_class_selectors(css_text, exclude_media=True)
    media_trapped = classes - base_classes
    return {
        "cssBytes": len(css_text.encode("utf-8")),
        "siteClassSelectorCount": len(classes),
        "siteClassSelectorSamples": sorted(classes)[:20],
        "siteClassSelectors": sorted(classes),
        # EXP-001 additions for L-1.6 @media-aware check
        "baseSiteClassSelectors": sorted(base_classes),
        "baseSiteClassSelectorCount": len(base_classes),
        "mediaTrappedSelectors": sorted(media_trapped),
        "mediaTrappedSelectorCount": len(media_trapped),
    }


def summarize_library_css(host: str, css_text: str) -> dict[str, Any]:
    root = host.removeprefix("fb-styles-")
    fallback = static_visible_fallback_status(root, css_text)
    return {
        "cssBytes": len(css_text.encode("utf-8")),
        "fallback": fallback,
    }


def static_visible_fallback_status(root: str, css_text: str) -> dict[str, Any]:
    selectors = fallback_selectors_for(root)
    if not selectors:
        return {
            "required": False,
            "status": "not-applicable",
            "evidence": f"No static-visible fallback selector contract is defined for {root}.",
        }

    root_ok = selector_has_declarations(css_text, selectors["root"], ("visibility:visible!important", "opacity:1!important"))
    inner_ok = any(
        selector_has_declarations(css_text, inner, ("visibility:visible!important", "opacity:1!important"))
        for inner in selectors["inner"]
    )
    runtime_only = has_runtime_state_only_fallback(css_text, selectors["root"])

    if root_ok and inner_ok:
        status = "pass"
    else:
        status = "fail"

    evidence = (
        f"{root}: rootStaticVisible={root_ok}; innerStaticVisible={inner_ok}; "
        f"runtimeStateOnlyFallback={runtime_only}; requiredRoot={selectors['root']}; "
        f"requiredInnerAny={','.join(selectors['inner'])}."
    )
    return {
        "required": True,
        "status": status,
        "evidence": evidence,
        "rootStaticVisible": root_ok,
        "innerStaticVisible": inner_ok,
        "runtimeStateOnlyFallback": runtime_only,
    }


def fallback_selectors_for(root: str) -> dict[str, Any] | None:
    if root == "splide":
        return {"root": ".splide", "inner": [".splide__track", ".splide__list"]}
    if root == "swiper":
        return {"root": ".swiper", "inner": [".swiper-wrapper", ".swiper-slide"]}
    if root == "embla":
        return {"root": ".embla", "inner": [".embla__container"]}
    if root == "flickity":
        return {"root": ".flickity", "inner": [".flickity-viewport"]}
    if root == "lottie":
        return {"root": ".lottie", "inner": ["svg", "canvas"]}
    return None


def selector_has_declarations(css_text: str, selector: str, declarations: tuple[str, ...]) -> bool:
    normalized_selector = normalize_css_fragment(selector)
    for raw_selectors, body in iter_css_rules(css_text):
        selector_parts = [normalize_css_fragment(part) for part in raw_selectors.split(",")]
        if normalized_selector not in selector_parts:
            continue
        normalized_body = normalize_css_fragment(body)
        if all(declaration in normalized_body for declaration in declarations):
            return True
    return False


def has_runtime_state_only_fallback(css_text: str, root_selector: str) -> bool:
    normalized_root = normalize_css_fragment(root_selector)
    for raw_selectors, body in iter_css_rules(css_text):
        normalized_body = normalize_css_fragment(body)
        if "visibility:visible!important" not in normalized_body or "opacity:1!important" not in normalized_body:
            continue
        selector_parts = [normalize_css_fragment(part) for part in raw_selectors.split(",")]
        runtime_parts = [
            part
            for part in selector_parts
            if part.startswith(normalized_root + ".") and any(state in part for state in (".is-initialized", ".is-rendered"))
        ]
        if runtime_parts and normalized_root not in selector_parts:
            return True
    return False


def iter_css_rules(css_text: str) -> list[tuple[str, str]]:
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    return [
        (match.group(1).strip(), match.group(2).strip())
        for match in re.finditer(r"([^{}@][^{}]*)\{([^{}]*)\}", css_text)
    ]


def normalize_css_fragment(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().lower())


def strip_media_blocks(css_text: str) -> str:
    """Remove `@media {...}` blocks (balanced braces) from CSS, keeping top-level rules.

    EXP-001 fix (2026-04-24): selectors that exist ONLY inside `@media` blocks are
    correctly routed by L-2 to `fb-media-site`, not `fb-styles-site`. A simple class
    scan that ignores block nesting counts those selectors as expected in
    fb-styles-site, producing a false FAIL on L-1.6 site-css-carried. Stripping
    @media blocks before the class scan gives us the BASE (non-responsive) selector
    set that L-1.6 actually wants.
    """
    out: list[str] = []
    i = 0
    n = len(css_text)
    media_re = re.compile(r"@media\b", re.I)
    while i < n:
        match = media_re.search(css_text, i)
        if match is None:
            out.append(css_text[i:])
            break
        out.append(css_text[i:match.start()])
        brace = css_text.find("{", match.end())
        if brace < 0:
            # malformed @media without opening brace; stop stripping
            break
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            ch = css_text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        i = j  # resume after the balanced @media block
    return "".join(out)


def extract_site_class_selectors(css_text: str, *, exclude_media: bool = False) -> set[str]:
    """Return site class selectors in the CSS.

    When `exclude_media=True`, `@media {...}` blocks are stripped first so that
    selectors which appear ONLY inside `@media` are not counted. This matches the
    L-1.6 intent: base (non-responsive) site class styles travel to `fb-styles-site`;
    responsive overrides travel to `fb-media-site` per L-2 and are not expected in
    `fb-styles-site`.
    """
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    if exclude_media:
        css_text = strip_media_blocks(css_text)
    classes = {
        match.group(1)
        for match in re.finditer(r"(?<![a-zA-Z0-9_-])\.(-?[_a-zA-Z][-_a-zA-Z0-9]*)", css_text)
    }
    return {
        cls
        for cls in classes
        if not (cls.startswith(("w-", "w--", "_w-", "fb-")) or cls.startswith("wf-"))
    }


def normalize_media_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.strip().lower())


def summarize_scripts(inline_scripts: list[dict[str, str]], stub_files: list[str] | None = None) -> dict[str, Any]:
    globals_found: set[str] = set()
    selectors: set[str] = set()
    for entry in inline_scripts:
        script = entry["script"]
        for global_name in SCRIPT_GLOBALS:
            pattern = r"\$\b" if global_name == "$" else rf"\b{re.escape(global_name)}\b"
            if re.search(pattern, script):
                globals_found.add(global_name)
        for match in re.finditer(r"querySelector(?:All)?\(\s*(['\"])(.*?)\1", script):
            selectors.add(match.group(2))
        for match in re.finditer(r"\$\(\s*(['\"])([.#][^'\"]+)\1\s*\)", script):
            selectors.add(match.group(2))
    return {
        "inlineScriptCount": len(inline_scripts),
        "globalsMentioned": sorted(globals_found),
        "selectorSamples": sorted(selectors)[:20],
        "l16Readiness": summarize_l16_readiness(inline_scripts, stub_files=stub_files),
        "unsafeWebflowGlobalAccess": summarize_unsafe_webflow_global_access(inline_scripts, stub_files=stub_files),
    }


def summarize_unsafe_webflow_global_access(
    inline_scripts: list[dict[str, str]],
    stub_files: list[str] | None = None,
) -> dict[str, Any]:
    stub_file_set = set(stub_files or [])
    findings: list[dict[str, Any]] = []
    for index, entry in enumerate(inline_scripts, start=1):
        if entry["file"] in stub_file_set:
            continue
        script = strip_js_comments(entry["script"])
        if "Webflow." not in script:
            continue
        safe_queue = (
            "window.Webflow" in script
            and "window.Webflow || []" in script
            and "window.Webflow.push" in script
        )
        l16_wrapped = has_l16_wrapper(script)
        if safe_queue or l16_wrapped:
            continue
        for line_no, line in enumerate(script.splitlines(), start=1):
            if re.search(r"(?<![\w.])Webflow\.(env|push|require)\s*\(", line):
                findings.append(
                    {
                        "index": index,
                        "file": entry["file"],
                        "line": line_no,
                        "snippet": line.strip()[:180],
                    }
                )
                break
    return {
        "count": len(findings),
        "findings": findings[:10],
        "excludedStubFileCount": len(stub_file_set),
    }


def summarize_library_cdn_dedupe(external_scripts: list[dict[str, str]]) -> dict[str, Any]:
    families: dict[str, list[dict[str, str]]] = {}
    by_file_family: dict[tuple[str, str], list[dict[str, str]]] = {}
    for script in external_scripts:
        family = library_family(script["src"])
        if not family:
            continue
        entry = {
            "file": script["file"],
            "src": script["src"],
            "version": library_version(script["src"]),
        }
        families.setdefault(family, []).append(entry)
        by_file_family.setdefault((script["file"], family), []).append(entry)

    duplicates = {
        f"{file_path}:{family}": entries
        for (file_path, family), entries in sorted(by_file_family.items())
        if len(entries) > 1
    }
    return {
        "familyCounts": {family: len(entries) for family, entries in sorted(families.items())},
        "duplicateFamilyCount": len(duplicates),
        "duplicates": {family: entries[:6] for family, entries in duplicates.items()},
    }


def library_family(src: str) -> str | None:
    normalized = src.lower()
    filename = normalized.split("?", 1)[0].rsplit("/", 1)[-1]
    module = filename[:-3].replace(".min", "") if filename.endswith(".js") else ""
    if "jquery-migrate" in normalized:
        return "jquery-migrate"
    if re.search(r"jquery(?:-|\.|/|@)", normalized):
        return "jquery"
    if "splide" in normalized:
        return "splide"
    if "lenis" in normalized:
        return "lenis"
    if "swiper" in normalized:
        return "swiper"
    if "embla" in normalized:
        return "embla"
    if "flickity" in normalized:
        return "flickity"
    if "lottie" in normalized:
        return "lottie"
    gsap_plugins = {
        "scrolltrigger": "gsap-scrolltrigger",
        "scrollsmoother": "gsap-scrollsmoother",
        "splittext": "gsap-splittext",
        "textplugin": "gsap-textplugin",
        "customease": "gsap-customease",
        "custombounce": "gsap-custombounce",
        "customwiggle": "gsap-customwiggle",
        "draggable": "gsap-draggable",
        "drawsvg": "gsap-drawsvg",
        "morphsvg": "gsap-morphsvg",
        "flip": "gsap-flip",
    }
    if module in gsap_plugins:
        return gsap_plugins[module]
    if "/gsap/" in normalized or "/gsap@" in normalized:
        if module and module != "gsap":
            return f"gsap-{module}"
    if re.search(r"gsap(?:\.min)?\.js|/gsap@|/gsap/", normalized):
        return "gsap-core"
    return None


def library_version(src: str) -> str:
    normalized = src.split("?", 1)[0]
    for pattern in (
        r"@([0-9][^/]+)",
        r"/([0-9]+\.[0-9]+(?:\.[0-9]+)?)/[^/]+\.js",
        r"[-.]([0-9]+\.[0-9]+(?:\.[0-9]+)?)(?:\.min)?\.js",
    ):
        match = re.search(pattern, normalized)
        if match:
            return match.group(1)
    return "unknown"


def normalized_library_src(src: str) -> str:
    return src.strip().split("?", 1)[0].lower()


def summarize_l16_readiness(
    inline_scripts: list[dict[str, str]],
    stub_files: list[str] | None = None,
) -> dict[str, Any]:
    stub_file_set = set(stub_files or [])
    findings = [
        classify_l16_script(entry["script"], index, file_path=entry["file"])
        for index, entry in enumerate(inline_scripts, start=1)
        if entry["file"] not in stub_file_set
    ]
    required = [finding for finding in findings if finding["required"]]
    failing = [finding for finding in required if not finding["wrapped"]]
    return {
        "requiredCount": len(required),
        "failingCount": len(failing),
        "failures": failing[:10],
        "excludedStubFileCount": len(stub_file_set),
        "excludedStubFiles": sorted(stub_file_set)[:10],
    }


def classify_l16_script(script: str, index: int, file_path: str | None = None) -> dict[str, Any]:
    executable = strip_js_comments(script)
    globals_found = script_globals(executable)
    selectors = script_selectors(executable)
    selector_only_dom_ready = bool(selectors) and not globals_found and has_dom_ready_gate(executable)
    required = bool(globals_found or selectors)
    wrapped = has_l16_wrapper(executable) or selector_only_dom_ready
    return {
        "index": index,
        "file": file_path or "",
        "required": required,
        "wrapped": wrapped,
        "globals": globals_found,
        "selectors": selectors[:8],
        "snippet": " ".join(executable.split())[:180],
    }


def strip_js_comments(script: str) -> str:
    script = re.sub(r"/\*.*?\*/", "", script, flags=re.S)
    script = re.sub(r"(^|[^\":])//.*", r"\1", script)
    return script


def script_globals(script: str) -> list[str]:
    found: list[str] = []
    for global_name in SCRIPT_GLOBALS:
        if global_name == "$":
            pattern = r"(?<![\w$])\$\s*(?:\(|\.)"
        else:
            pattern = rf"\b{re.escape(global_name)}\b"
        if re.search(pattern, script):
            found.append(global_name)
    return found


def script_selectors(script: str) -> list[str]:
    selectors: set[str] = set()
    for match in re.finditer(r"querySelector(?:All)?\(\s*(['\"])(.*?)\1", script):
        selectors.add(match.group(2))
    for match in re.finditer(r"\$\(\s*(['\"])([.#\[][^\"]*?)\1\s*\)", script):
        selectors.add(match.group(2))
    return sorted(selectors)


def has_l16_wrapper(script: str) -> bool:
    required_tokens = ("need", "requiredSelectors", "fbRun")
    return all(token in script for token in required_tokens) and ("setTimeout" in script or "requestAnimationFrame" in script)


def has_dom_ready_gate(script: str) -> bool:
    return "DOMContentLoaded" in script or "document.readyState" in script


def build_manifest(
    mode: str,
    source: dict[str, Any] | None,
    output: dict[str, Any] | None,
    write_manifest: bool,
    output_root: Path | None,
) -> dict[str, Any]:
    # EXP-004 (2026-04-25): align output's mode-B target evaluation with the
    # source-derived dynamic catalog so contract-check IDs match across the diff.
    # Without this, source detects targets per its own HTML and output detects
    # targets per its own (typically-different) HTML — IDs would not intersect
    # and `mode-b-initial-state-transport` would silently report "unknown" for
    # every source-required target, masking real failures.
    if source is not None and output is not None and source.get("modeBTargets"):
        output_probe = output.get("_probe")
        if output_probe is not None:
            output["initialStateTransport"] = summarize_initial_state_transport(
                output_probe, source["modeBTargets"]
            )
            output["modeBTargets"] = source["modeBTargets"]
    contract_checks = build_contract_checks(mode, source, output, write_manifest, output_root)
    source_ix_count = source["ixInlineStyleAttrs"]["count"] if source else 0
    output_ix_count = output["ixInlineStyleAttrs"]["count"] if output else 0

    manifest = {
        "schema": SCHEMA,
        "outputMode": mode,
        "animationClaim": "source-runtime-preserved" if mode == "webflow-paste" else "source-runtime-preview",
        "source": scrub_inventory(source),
        "output": scrub_inventory(output),
        "ixShape": {
            "inventoriedStyleAttrs": source_ix_count,
            "neutralizedStyleAttrs": max(source_ix_count - output_ix_count, 0) if source and output else 0,
            "preservedStyleAttrs": output_ix_count,
            "initialStateTransport": output["initialStateTransport"] if output else None,
            "preservedReasons": [],
        },
        "runtime": output["runtime"] if output else None,
        "fonts": output["fonts"] if output else (source["fonts"] if source else {"relativeFontUrls": [], "policy": "reported-only"}),
        "contractChecks": contract_checks,
        "probesRun": probes_run(source, output),
    }
    return manifest


def build_contract_checks(
    mode: str,
    source: dict[str, Any] | None,
    output: dict[str, Any] | None,
    write_manifest: bool,
    output_root: Path | None,
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if output is None:
        checks.append(check("input-probe-only", "warn", "No output root supplied; output-mode contract was not evaluated."))
        return checks

    output_probe: HtmlProbe = output["_probe"]
    source_count = source["dataWIdCount"] if source else None
    output_count = output["dataWIdCount"]
    checks.append(_time_call(font_face_absence_in_fb_styles_site_check, mode, output))
    checks.append(_time_call(site_css_carried_check, mode, source, output))
    checks.append(_time_call(overlay_neutralization_scope_check, mode, source, output))
    checks.append(_time_call(lazy_video_idempotence_check, mode, source, output))
    checks.append(_time_call(library_cdn_dedupe_check, mode, output))
    checks.append(_time_call(host_topology_check, mode, output))
    checks.append(_time_call(webflow_global_readiness_check, mode, output))

    if mode == "webflow-paste":
        source_ix_count = source["ixInlineStyleAttrs"]["count"] if source else None
        output_ix_count = output["ixInlineStyleAttrs"]["count"]
        ix_preserved = source_ix_count is not None and output_ix_count == source_ix_count
        checks.append(
            check(
                "mode-b-inline-ix-preserved",
                "pass" if ix_preserved else "fail",
                f"source IX-shaped style attrs={source_ix_count}; output IX-shaped style attrs={output_ix_count}; policy=preserve source runtime starts.",
            )
        )
        runtime = output["runtime"]
        source_runtime = source["runtime"] if source else None
        runtime_preserved = bool(
            source_runtime
            and runtime["jsWebflowReferences"] == source_runtime["jsWebflowReferences"]
            and runtime["inlineModuleIifeSignatures"] == source_runtime["inlineModuleIifeSignatures"]
        )
        checks.append(
            check(
                "mode-b-runtime-preserved",
                "pass" if runtime_preserved else "fail",
                f"source js/webflow.js refs={source_runtime['jsWebflowReferences'] if source_runtime else None}; output js/webflow.js refs={runtime['jsWebflowReferences']}; source inline module IIFE={source_runtime['inlineModuleIifeSignatures'] if source_runtime else None}; output inline module IIFE={runtime['inlineModuleIifeSignatures']}.",
            )
        )
        checks.append(_time_call(compare_data_w_id_check, source_count, output_count))
        checks.append(
            check(
                "mode-b-structural-hide-preserved",
                structural_hide_status(output_probe),
                structural_hide_evidence(output_probe),
            )
        )
        checks.append(_time_call(mode_b_initial_state_transport_check, source, output))
        checks.append(_time_call(mode_b_d007_anchor_check, source, output))
        checks.append(_time_call(mode_b_static_visible_fallback_check, output))
        checks.append(_time_call(mode_b_static_visible_ix_state_safety_check, output))
        checks.append(_time_call(mode_b_static_visible_class_state_safety_check, output))
        checks.append(_time_call(mode_b_l16_readiness_check, output))
    else:
        runtime = output["runtime"]
        page_count = len(output["htmlFiles"])
        stub_count = output.get("l27StubCount", 0)
        non_stub_page_count = page_count - stub_count
        # L-15A: only non-stub pages emit fb-runtime hosts (stubs are byte-passthrough).
        # L-27 + source preservation: every page (stub OR non-stub) carries exactly one
        # `<script src="js/webflow.js">` reference. Non-stubs carry it inside fb-runtime.w-embed.
        # Stubs preserve it at its source-position (typically end of body) byte-for-byte.
        # Therefore: fbRuntimeCount must equal non_stub_page_count, but jsWebflowReferences
        # must equal total page_count (= non_stub_page_count + stub_count).
        runtime_ok = (
            runtime["fbRuntimeCount"] == non_stub_page_count
            and runtime["jsWebflowReferences"] == page_count
            and runtime["inlineModuleIifeSignatures"] == 0
        )
        checks.append(
            check(
                "local-preview-runtime-present",
                "pass" if runtime_ok else "fail",
                f"fb-runtime={runtime['fbRuntimeCount']}; relative js/webflow.js references={runtime['jsWebflowReferences']}; inline module IIFE={runtime['inlineModuleIifeSignatures']}; expected fb-runtime to equal non-stub page count ({non_stub_page_count} = {page_count} pages - {stub_count} L-27 stubs); expected js/webflow.js references to equal total page count ({page_count}).",
            )
        )
        checks.append(_time_call(compare_data_w_id_check, source_count, output_count))

    font_count = len(output["fonts"]["relativeFontUrls"])
    checks.append(
        check(
            "relative-font-risk-reported",
            "warn" if font_count else "pass",
            f"{font_count} unresolved relative font URL(s) reported; policy=reported-only.",
        )
    )
    checks.append(_time_call(output_mode_declaration_check, mode, output_root, write_manifest))
    checks.append(_time_call(manifest_file_check, output_root, write_manifest, mode))
    return checks


def compare_data_w_id_check(source_count: int | None, output_count: int) -> dict[str, str]:
    if source_count is None:
        return check("data-w-id-preserved", "warn", f"Output has {output_count}; no source root supplied for parity check.")
    return check(
        "data-w-id-preserved",
        "pass" if source_count == output_count else "fail",
        f"source={source_count}; output={output_count}.",
    )


def font_face_absence_in_fb_styles_site_check(mode: str, output: dict[str, Any]) -> dict[str, str]:
    css_blocks = output["_probe"].fb_styles_site_css
    counts = [len(re.findall(r"@font-face\b", css, re.I)) for css in css_blocks]
    total = sum(counts)
    status = "pass" if total == 0 else "fail"
    block_summary = ", ".join(str(count) for count in counts) if counts else "no fb-styles-site style block"
    return check(
        f"{mode}-font-face-absence-in-fb-styles-site",
        status,
        f"fb-styles-site @font-face count={total}; blockCounts=[{block_summary}].",
    )


def structural_hide_status(probe: HtmlProbe) -> str:
    if probe.fb_custom_code_count == 0:
        return "warn"
    return "pass" if probe.fb_custom_code_display_none == probe.fb_custom_code_count else "fail"


def structural_hide_evidence(probe: HtmlProbe) -> str:
    if probe.fb_custom_code_count == 0:
        return "No fb-custom-code host found; structural hide preservation is not applicable to this artifact."
    return f"fb-custom-code display:none hosts={probe.fb_custom_code_display_none}/{probe.fb_custom_code_count}."


def host_topology_check(mode: str, output: dict[str, Any]) -> dict[str, str]:
    # EXP-001 fix (2026-04-24): counts are total across all processed HTML files,
    # not per-file. A multi-page output legitimately reports >1 of each host
    # (one per page). Require (a) both counts >= 1 so we catch a zero-host run,
    # and (b) both counts equal so a missing host on one page still FAILs.
    runtime = output["runtime"]
    custom_count = runtime["fbCustomCodeCount"]
    media_count = runtime["fbMediaSiteCount"]
    status = "pass" if custom_count >= 1 and media_count >= 1 and custom_count == media_count else "fail"
    evidence = (
        f"fb-custom-code hosts={custom_count}; fb-media-site hosts={media_count}; "
        "expected at least one of each host across processed output, and equal counts "
        "(one fb-custom-code + one fb-media-site per HTML file)."
    )
    return check(f"{mode}-host-topology", status, evidence)


def webflow_global_readiness_check(mode: str, output: dict[str, Any]) -> dict[str, str]:
    unsafe = output["scripts"]["unsafeWebflowGlobalAccess"]
    status = "pass" if unsafe["count"] == 0 else "fail"
    evidence = (
        f"unsafe bare Webflow global inline scripts={unsafe['count']}; "
        f"excluded L-27 stub files={unsafe.get('excludedStubFileCount', 0)}."
    )
    findings = unsafe.get("findings") or []
    if findings:
        samples = []
        for finding in findings[:4]:
            samples.append(
                f"#{finding['index']} {finding['file']}:{finding['line']} {finding['snippet']}"
            )
        evidence += " samples: " + "; ".join(samples) + "."
    return check(f"{mode}-webflow-global-readiness", status, evidence)


def mode_b_initial_state_transport_check(source: dict[str, Any] | None, output: dict[str, Any]) -> dict[str, str]:
    """EXP-004 (2026-04-25): consume the source-derived dynamic mode-B target
    catalog. `source["initialStateTransport"]["targets"]` is now built per
    `detect_mode_b_targets(source_html)`. `build_manifest` resummarizes
    `output["initialStateTransport"]["targets"]` against the SAME source-derived
    target list so the per-`id` diff below remains semantically valid.
    """
    if not source:
        return check("mode-b-initial-state-transport", "warn", "No source root supplied for initial-state parity check.")

    source_targets = {target["id"]: target for target in source["initialStateTransport"]["targets"]}
    output_targets = {target["id"]: target for target in output["initialStateTransport"]["targets"]}
    required_ids = [
        target_id
        for target_id, source_target in source_targets.items()
        if source_target["sourceStatePresent"]
    ]
    missing = [
        output_targets[target_id]
        for target_id in required_ids
        if target_id in output_targets and not output_targets[target_id]["modeBTransported"]
    ]
    unknown = [target_id for target_id in required_ids if target_id not in output_targets]
    transported = [
        output_targets[target_id]
        for target_id in required_ids
        if target_id in output_targets and output_targets[target_id]["modeBTransported"]
    ]

    if missing or unknown:
        status = "fail"
    elif required_ids:
        status = "pass"
    else:
        status = "pass"

    transported_summary = ", ".join(
        f"{target['id']}={target['classification']}" for target in transported
    ) or "none"
    missing_summary = ", ".join(
        f"{target['id']}={target['classification']}" for target in missing
    )
    if unknown:
        missing_summary = ", ".join(filter(None, [missing_summary, f"unknown={','.join(unknown)}"]))
    evidence = (
        f"source-required={len(required_ids)}; transported={len(transported)}; "
        f"missing={len(missing) + len(unknown)}; transportedTargets={transported_summary}"
    )
    if missing_summary:
        evidence += f"; missingTargets={missing_summary}"
    return check("mode-b-initial-state-transport", status, evidence + ".")


D007_NAV_CHILD_LEFT_CHAIN: tuple[str, ...] = ("nav-child", "left")
D007_BG_WHIPE_CHAIN: tuple[str, ...] = ("bg-whipe",)
D007_MENU_SHELL_CLASS = "menu-bar-whipe"


def _find_dynamic_target_by_class_chain(
    targets: list[dict[str, Any]] | None, required_classes: tuple[str, ...]
) -> dict[str, Any] | None:
    """Return first dynamic mode-B target whose `classes` superset includes all
    members of `required_classes`. EXP-004 helper for d007's MNZ anchor lookup
    after the per-target IDs became structural (no longer the hardcoded
    `nav-child-left-closed` / `bg-whipe-overlay-collapsed` strings).
    """
    if not targets:
        return None
    for target in targets:
        target_classes = set(target.get("classes", ()))
        if all(req in target_classes for req in required_classes):
            return target
    return None


def mode_b_d007_anchor_check(source: dict[str, Any] | None, output: dict[str, Any]) -> dict[str, str]:
    """EXP-004 (2026-04-25): retained MNZ-specific anchor class chains
    (`nav-child.left`, `bg-whipe`, `menu-bar-whipe`) but adapted to look up
    dynamic targets by class chain rather than by hardcoded IDs. Generalising
    this rule into "menu-bar-* overlays + their hidden children co-transport"
    is flagged as an open design question for EXP-005, where it overlaps with
    L-31 emission logic. See `experiments/EXP-004-modeb-probe-universal.md`
    open-questions section.
    """
    if not source:
        return check("mode-b-d007-anchor-safety", "warn", "No source root supplied for D-007 anchor check.")

    source_probe: HtmlProbe = source["_probe"]
    output_probe: HtmlProbe = output["_probe"]
    source_menu_shells = sum(
        1 for element in source_probe.elements if class_set_contains(element.classes, (D007_MENU_SHELL_CLASS,))
    )
    output_menu_shells = sum(
        1 for element in output_probe.elements if class_set_contains(element.classes, (D007_MENU_SHELL_CLASS,))
    )

    output_target_summaries = {
        target["id"]: target for target in output["initialStateTransport"]["targets"]
    }
    source_target_summaries = {
        target["id"]: target for target in source["initialStateTransport"]["targets"]
    }

    nav_target_spec = _find_dynamic_target_by_class_chain(source.get("modeBTargets"), D007_NAV_CHILD_LEFT_CHAIN)
    bg_target_spec = _find_dynamic_target_by_class_chain(source.get("modeBTargets"), D007_BG_WHIPE_CHAIN)
    nav_output = output_target_summaries.get(nav_target_spec["id"]) if nav_target_spec else None
    bg_output = output_target_summaries.get(bg_target_spec["id"]) if bg_target_spec else None
    nav_source_present = bool(nav_target_spec) and source_target_summaries.get(
        nav_target_spec["id"], {}
    ).get("sourceStatePresent", False)
    bg_source_present = bool(bg_target_spec) and source_target_summaries.get(
        bg_target_spec["id"], {}
    ).get("sourceStatePresent", False)

    # EXP-004: gate "anchors present" on detecting an actual nav-child.left or
    # bg-whipe IX-shaped initial state in source. The legacy hardcoded catalog
    # treated `menu-bar-whipe` shell presence alone as triggering, but with
    # dynamic detection a pretreated source (where IX states already migrated
    # to CSS) carries no anchor targets to verify against — failing on a bare
    # menu shell would be a false positive when the same inventory is fed as
    # both source and output (the run_self_test `good_manifest` assertion).
    anchors_present = bool(nav_source_present or bg_source_present)
    if not anchors_present:
        evidence = (
            f"sourceMenuBarWhipe={source_menu_shells}; outputMenuBarWhipe={output_menu_shells}; "
            "no nav-child.left or bg-whipe IX-shaped initial states detected in source."
        )
        return check("mode-b-d007-anchor-safety", "pass", evidence)

    failures: list[str] = []
    if source_menu_shells and nav_source_present and not (nav_output and nav_output["modeBTransported"]):
        failures.append("menu-bar-whipe present but nav-child.left hidden state is not mode-b transported")
    if bg_source_present and not (bg_output and bg_output["modeBTransported"]):
        failures.append("bg-whipe overlay collapsed state is not mode-b transported")

    evidence = (
        f"sourceMenuBarWhipe={source_menu_shells}; outputMenuBarWhipe={output_menu_shells}; "
        f"navChildLeft={nav_output['classification'] if nav_output else 'missing'}; "
        f"bgWhipe={bg_output['classification'] if bg_output else 'missing'}."
    )
    if failures:
        evidence += " failures: " + "; ".join(failures) + "."
    return check("mode-b-d007-anchor-safety", "fail" if failures else "pass", evidence)


def site_css_carried_check(mode: str, source: dict[str, Any] | None, output: dict[str, Any]) -> dict[str, str]:
    # EXP-001 fix (2026-04-24): compare BASE source selectors (those NOT trapped inside @media)
    # against fb-styles-site selectors. @media-trapped selectors are correctly routed to
    # fb-media-site per L-2 and were causing false FAILs on L-1.6 in EXP-001 (MNZ:
    # heading-slider, hide-mobile, hide-tablet).
    if not source:
        return check(f"{mode}-site-css-carried", "warn", "No source root supplied for source site CSS parity check.")

    source_meta = source["sourceSiteCss"]
    source_base_classes = set(source_meta.get("baseSiteClassSelectors", source_meta["siteClassSelectors"]))
    output_classes = set(output["fbStylesSiteCss"]["siteClassSelectors"])
    media_trapped_count = source_meta.get("mediaTrappedSelectorCount", 0)

    if not source_base_classes:
        return check(f"{mode}-site-css-carried", "warn", "Source contains no non-baseline BASE site CSS class selectors to compare (all selectors are @media-trapped).")

    missing = sorted(source_base_classes - output_classes)
    status = "pass" if not missing else "fail"
    evidence = (
        f"source BASE site class selectors={len(source_base_classes)} "
        f"(plus {media_trapped_count} @media-trapped routed to fb-media-site per L-2); "
        f"fb-styles-site selectors={len(output_classes)}; "
        f"missing from fb-styles-site={len(missing)}"
    )
    if missing:
        evidence += f"; samples={', '.join(missing[:12])}."
    else:
        evidence += "."
    return check(f"{mode}-site-css-carried", status, evidence)


def overlay_neutralization_scope_check(mode: str, source: dict[str, Any] | None, output: dict[str, Any]) -> dict[str, str]:
    """L-7 universal scope check (EXP-003).

    Enumerates source-DOM classes, intersects with the class-chain selectors
    flagged by `summarize_overlay_neutralization`, subtracts source-preserved
    collapse rules (source-authored `.hide-all { display: none }` utility classes
    are legitimate, not skill-injected), and reports count + evidence generically."""
    summary = output["overlayNeutralization"]
    # Source-DOM classes: prefer the source probe's set. Fall back to output's own
    # domClassSet when no source is supplied (defensive — all real runs supply source).
    source_classes = set(source["domClassSet"]) if source and source.get("domClassSet") else set(output.get("domClassSet", []))
    # Source-preserved legitimate collapse rules keyed by (sorted classes tuple, sorted collapse kinds tuple).
    source_collapse_sigs: set[tuple[tuple[str, ...], tuple[str, ...]]] = set()
    if source and source.get("sourceCollapseRules"):
        for r in source["sourceCollapseRules"]:
            sig = (tuple(sorted(r.get("classes", []))), tuple(sorted(r.get("collapseKinds", []))))
            source_collapse_sigs.add(sig)

    # Use FULL finding lists (not the truncated samples) for correctness.
    global_findings_all = summary.get("globalFindings") or summary.get("globalSamples") or []
    combo_findings_all = summary.get("comboFindings") or summary.get("comboSamples") or []

    # Filter global findings: only those whose class-chain intersects source DOM classes
    # AND that do NOT match a source-preserved collapse rule (by class-chain+collapse-kinds
    # signature). Source-preserved collapse rules are legit utility classes authored by
    # the designer — preserving them in fb-styles-site is correct per L-1.
    global_matches: list[dict[str, Any]] = []
    for finding in global_findings_all:
        chain = finding.get("classes", [])
        if source_classes and not any(cls in source_classes for cls in chain):
            continue
        sig = (tuple(sorted(chain)), tuple(sorted(finding.get("collapseKinds", []))))
        if sig in source_collapse_sigs:
            continue
        global_matches.append(finding)

    # Filter combo findings: require non-framework class membership in source DOM.
    combo_matches: list[dict[str, Any]] = []
    for finding in combo_findings_all:
        non_fw = finding.get("nonFrameworkClasses") or [c for c in finding.get("classes", []) if not any(c.startswith(p) for p in L7_FRAMEWORK_CLASS_PREFIXES)]
        if source_classes and not any(cls in source_classes for cls in non_fw):
            continue
        combo_matches.append(finding)

    global_count = len(global_matches)
    combo_count = len(combo_matches)

    status = "pass" if global_count == 0 and combo_count == 0 else "fail"

    source_preserved_count = len(source_collapse_sigs)
    evidence = (
        f"skill-injected class-based collapse rules={global_count}; "
        f"inline combo-class collapses on data-w-id targets={combo_count}; "
        f"source-DOM classes enumerated={len(source_classes)}; "
        f"source-preserved collapse rules excluded={source_preserved_count}."
    )
    samples: list[str] = []
    for finding in global_matches[:4]:
        chain_label = "".join("." + c for c in finding.get("classes", []))
        kinds = ",".join(finding.get("collapseKinds", []))
        samples.append(f"{finding.get('host','')} {chain_label} collapse={kinds}")
    for finding in combo_matches[:4]:
        non_fw = finding.get("nonFrameworkClasses") or finding.get("classes", [])
        chain_label = "".join("." + c for c in non_fw)
        kinds = ",".join(finding.get("collapseKinds", []))
        important = " !important" if finding.get("hasImportant") else ""
        samples.append(f"{finding.get('file','')} {chain_label} inline-collapse={kinds}{important}")
    if samples:
        evidence += " samples: " + "; ".join(samples) + "."
    return check(f"{mode}-overlay-neutralization-scope", status, evidence)


def lazy_video_idempotence_check(mode: str, source: dict[str, Any] | None, output: dict[str, Any]) -> dict[str, str]:
    source_summary = source["lazyVideo"] if source else None
    output_summary = output["lazyVideo"]
    source_required_count = source_summary["dataSrcMissingSrcCount"] if source_summary else 0
    missing_count = output_summary["dataSrcMissingSrcCount"]
    mismatch_count = output_summary["dataSrcMismatchCount"]
    marker_count = output_summary["dataSrcMarkerCount"]
    blocked_autoplay_count = output_summary["autoplayLazyBlockedCount"]
    unsafe_loader_count = output_summary["unsafeRetainedLazyLoaderCount"]
    retained_loader_count = output_summary["retainedLazyLoaderCount"]

    if mode == "webflow-paste" and marker_count == 0:
        failures = []
        if missing_count != source_required_count:
            failures.append(
                f"source-faithful lazy preservation expected {source_required_count} missing src values; output has {missing_count}"
            )
        if mismatch_count:
            failures.append(f"{mismatch_count} video data-src sources have src != data-src")
        status = "pass" if not failures else "fail"
        evidence = (
            f"source lazy data-src missing src={source_required_count}; output missing src={missing_count}; "
            f"src mismatches={mismatch_count}; L-5a markers={marker_count}; policy=preserve source lazy loader."
        )
        if failures:
            evidence += " failures: " + "; ".join(failures) + "."
        return check(f"{mode}-lazy-video-idempotence", status, evidence)

    failures: list[str] = []
    if missing_count:
        failures.append(f"{missing_count} video data-src sources still lack src")
    if mismatch_count:
        failures.append(f"{mismatch_count} video data-src sources have src != data-src")
    if source_required_count and marker_count < source_required_count:
        failures.append(
            f"source required {source_required_count} L-5a copies but output has {marker_count} L-5a markers"
        )
    if blocked_autoplay_count:
        failures.append(f"{blocked_autoplay_count} autoplay videos still carry loading=lazy/preload=none")
    if (source_required_count or marker_count) and unsafe_loader_count:
        failures.append(f"{unsafe_loader_count} retained video.lazy loaders call load() without an early idempotence guard")

    status = "pass" if not failures else "fail"
    evidence = (
        f"source lazy data-src needing copy={source_required_count}; output data-src sources missing src={missing_count}; "
        f"src mismatches={mismatch_count}; L-5a markers={marker_count}; autoplay lazy/preload blockers={blocked_autoplay_count}; "
        f"retained video.lazy loaders={retained_loader_count}; unsafe retained loaders={unsafe_loader_count}."
    )
    if failures:
        evidence += " failures: " + "; ".join(failures) + "."
    samples: list[str] = []
    for sample in output_summary["missingSrcSamples"][:3]:
        samples.append(f"{sample['file']} missing src for data-src={sample['dataSrc']}")
    for sample in output_summary["mismatchSamples"][:3]:
        samples.append(f"{sample['file']} src={sample['src']} data-src={sample['dataSrc']}")
    for sample in output_summary["blockedAutoplaySamples"][:3]:
        samples.append(f"{sample['file']} autoplay blocker loading={sample['loading']} preload={sample['preload']}")
    for loader in output_summary["retainedLazyLoaderSamples"][:3]:
        if (source_required_count or marker_count) and loader["unsafeLoadCall"]:
            samples.append(f"unsafe loader snippet={loader['snippet']}")
    if samples:
        evidence += " samples: " + "; ".join(samples) + "."
    return check(f"{mode}-lazy-video-idempotence", status, evidence)


def library_cdn_dedupe_check(mode: str, output: dict[str, Any]) -> dict[str, str]:
    summary = output["libraryCdnDedupe"]
    duplicate_count = summary["duplicateFamilyCount"]
    status = "pass" if duplicate_count == 0 else "fail"
    family_counts = ", ".join(f"{family}={count}" for family, count in summary["familyCounts"].items()) or "none"
    evidence = f"detected library CDN family counts: {family_counts}; duplicate families={duplicate_count}."
    if duplicate_count:
        samples: list[str] = []
        for family, entries in summary["duplicates"].items():
            versions = ", ".join(f"{entry['version']}:{entry['src']}" for entry in entries[:4])
            samples.append(f"{family} -> {versions}")
        evidence += " duplicates: " + "; ".join(samples) + "."
    return check(f"{mode}-library-cdn-dedupe", status, evidence)


def mode_b_static_visible_fallback_check(output: dict[str, Any]) -> dict[str, str]:
    library_css = output["fbStylesLibraryCss"]
    required = [
        (host, summary["fallback"])
        for host, summary in sorted(library_css.items())
        if summary["fallback"].get("required")
    ]
    if not required:
        return check(
            "mode-b-static-visible-fallbacks",
            "warn",
            "No library style hosts with a static-visible fallback contract were found.",
        )

    failing = [(host, fallback) for host, fallback in required if fallback["status"] != "pass"]
    evidence = "; ".join(f"{host}: {fallback['evidence']}" for host, fallback in required)
    return check("mode-b-static-visible-fallbacks", "fail" if failing else "pass", evidence)


def mode_b_static_visible_ix_state_safety_check(output: dict[str, Any]) -> dict[str, str]:
    safety = output["staticVisibleIxStateSafety"]
    unsafe = safety["unsafeSamples"]
    status = "pass" if safety["unsafeCount"] == 0 else "fail"
    evidence = (
        f"ix-state markers={safety['markerCount']}; hidden/collapsed markers={safety['hiddenMarkerCount']}; "
        f"unsafe content-bearing markers={safety['unsafeCount']}."
    )
    if unsafe:
        samples = []
        for finding in unsafe[:5]:
            class_label = ".".join(finding["classes"]) or finding["tag"]
            hidden_label = ",".join(finding["hiddenDeclarations"]) or "none"
            samples.append(f"{finding['marker']} {class_label} hidden={hidden_label}")
        evidence += " samples: " + "; ".join(samples) + "."
    return check("mode-b-static-visible-ix-state-safety", status, evidence)


def mode_b_static_visible_class_state_safety_check(output: dict[str, Any]) -> dict[str, str]:
    safety = output["staticVisibleClassStateSafety"]
    unsafe = safety["unsafeSamples"]
    status = "pass" if safety["unsafeCount"] == 0 else "fail"
    evidence = f"class-selector frozen IX-start hazards={safety['unsafeCount']}."
    if unsafe:
        samples = []
        for finding in unsafe[:5]:
            hidden_label = ",".join(finding["hiddenDeclarations"]) or "none"
            samples.append(f"{finding['id']} selector={finding['selector']} hidden={hidden_label}")
        evidence += " samples: " + "; ".join(samples) + "."
    return check("mode-b-static-visible-class-state-safety", status, evidence)


def mode_b_l16_readiness_check(output: dict[str, Any]) -> dict[str, str]:
    readiness = output["scripts"]["l16Readiness"]
    failures = readiness["failures"]
    status = "pass" if readiness["failingCount"] == 0 else "fail"
    evidence = (
        f"required inline bodies={readiness['requiredCount']}; unwrapped={readiness['failingCount']}; "
        f"excluded L-27 stub files={readiness.get('excludedStubFileCount', 0)}."
    )
    if failures:
        samples = []
        for failure in failures[:4]:
            globals_label = ",".join(failure["globals"]) or "none"
            selectors_label = ",".join(failure["selectors"]) or "none"
            file_label = failure.get("file") or "unknown-file"
            samples.append(f"#{failure['index']} {file_label} globals={globals_label} selectors={selectors_label}")
        evidence += " samples: " + "; ".join(samples) + "."
    return check("mode-b-l16-readiness", status, evidence)


def manifest_file_check(output_root: Path | None, write_manifest: bool, mode: str) -> dict[str, str]:
    if write_manifest:
        return check("pretreat-manifest-json", "pass", "pretreat-manifest.json will be written by this probe.")
    if output_root is None or output_root.is_file():
        return check("pretreat-manifest-json", "warn", "No output directory supplied for manifest existence check.")
    manifest_path = output_root / "pretreat-manifest.json"
    if not manifest_path.exists():
        return check("pretreat-manifest-json", "fail", f"Missing {manifest_path}.")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - this is a validation diagnostic.
        return check("pretreat-manifest-json", "fail", f"Invalid JSON: {exc}.")
    if data.get("schema") != SCHEMA or data.get("outputMode") != mode:
        return check(
            "pretreat-manifest-json",
            "fail",
            f"Manifest schema/mode mismatch: schema={data.get('schema')!r}; outputMode={data.get('outputMode')!r}.",
        )
    return check("pretreat-manifest-json", "pass", f"{manifest_path} exists and declares {mode}.")


def output_mode_declaration_check(mode: str, output_root: Path | None, write_manifest: bool) -> dict[str, str]:
    expected_claim = "source-runtime-preserved" if mode == "webflow-paste" else "source-runtime-preview"
    if output_root is None:
        return check("output-mode-declaration", "warn", "No output directory supplied for output-mode declaration check.")
    manifest_path = output_root / "pretreat-manifest.json"
    if write_manifest:
        previous_summary = "none"
        if manifest_path.exists():
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                previous_summary = (
                    f"previousDeclared={data.get('outputMode')!r}; "
                    f"previousAnimationClaim={data.get('animationClaim')!r}"
                )
            except Exception as exc:  # noqa: BLE001 - validation diagnostics should capture parse errors.
                previous_summary = f"previousManifestUnreadable={exc}"
        return check(
            "output-mode-declaration",
            "pass",
            f"requested={mode!r}; expectedAnimationClaim={expected_claim!r}; write-manifest=yes; {previous_summary}.",
        )
    if not manifest_path.exists():
        return check(
            "output-mode-declaration",
            "warn",
            f"{manifest_path} does not exist yet; this probe will write it when --write-manifest is used.",
        )
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation diagnostics should capture parse errors.
        return check("output-mode-declaration", "fail", f"Could not parse pretreat-manifest.json: {exc}.")
    declared = data.get("outputMode")
    animation_claim = data.get("animationClaim")
    status = "pass" if declared == mode and animation_claim == expected_claim else "fail"
    return check(
        "output-mode-declaration",
        status,
        f"declared={declared!r}; requested={mode!r}; animationClaim={animation_claim!r}; expectedAnimationClaim={expected_claim!r}.",
    )


def _time_call(fn, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Phase 1B: time the call when profiling, otherwise pass-through.

    Used to wrap each named check-function call site in build_contract_checks().
    Inline check() factory dict-builds are NOT timed (constant-time work; the
    expensive computation is upstream in the named functions).
    """
    if not _PROFILE_ENABLED:
        return fn(*args, **kwargs)
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    if isinstance(result, dict):
        check_id = result.get("id", getattr(fn, "__name__", "unknown"))
        status = result.get("status")
    else:
        check_id = getattr(fn, "__name__", "unknown")
        status = None
    _PROFILE_RECORDS.append({
        "check_id": check_id,
        "duration_ms": round(elapsed_ms, 3),
        "status": status,
    })
    return result


def check(check_id: str, status: str, evidence: str) -> dict[str, str]:
    return {"id": check_id, "status": status, "evidence": evidence}


def probes_run(source: dict[str, Any] | None, output: dict[str, Any] | None) -> list[str]:
    out = []
    if source:
        out.extend(
            [
                "input-runtime-surface",
                "input-ix-marker",
                "input-ix-inline-style-attr",
                "input-initial-state-transport",
                "input-font-url",
                "input-css-surface",
                "input-script-dependency-selector",
                "input-reserved-webflow-class",
            ]
        )
    if output:
        out.extend(
            [
                "output-runtime-surface",
                "output-ix-marker",
                "output-ix-inline-style-attr",
                "output-initial-state-transport",
                "output-font-url",
                "output-font-face-embed-placement",
                "output-site-css-selector-parity",
                "output-overlay-neutralization-scope",
                "output-lazy-video-idempotence",
                "output-library-cdn-dedupe",
                "output-pretreat-manifest",
                "output-static-visible-library-fallback",
                "output-static-visible-ix-state-safety",
                "output-static-visible-class-state-safety",
                "output-l16-readiness",
            ]
        )
    return out


def scrub_inventory(inventory: dict[str, Any] | None) -> dict[str, Any] | None:
    if inventory is None:
        return None
    return {key: value for key, value in inventory.items() if key != "_probe"}


def has_failing_contract(manifest: dict[str, Any]) -> bool:
    return any(row.get("status") == "fail" for row in manifest.get("contractChecks", []))


def write_profile(output_root: Path | None) -> Path | None:
    """Phase 1B: write per-check timing JSON next to the manifest.

    Returns the written path on success, None when output_root is missing or
    not a directory (caller decides whether to warn).
    """
    if output_root is None or not output_root.is_dir():
        return None
    path = output_root / "pretreat-manifest-profile.json"
    payload = {
        "schema": PROFILE_SCHEMA,
        "note": (
            "Per-check wall-clock timing for build_contract_checks(). "
            "Inline check() factory dict-builds are not timed (constant-time). "
            "See _time_call() in paste_contract_probe.py."
        ),
        "checks": _PROFILE_RECORDS,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path


def write_manifest(manifest: dict[str, Any], output_root: Path) -> Path:
    if not output_root.is_dir():
        raise SystemExit("--write-manifest requires --output-root to be a directory")
    path = output_root / "pretreat-manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        source = base / "source"
        good = base / "good"
        bad = base / "bad"
        cascade_bad = base / "cascade-bad"
        hidden_content_bad = base / "hidden-content-bad"
        class_state_bad = base / "class-state-bad"
        font_face_bad = base / "font-face-bad"
        overlay_bad = base / "overlay-bad"
        lazy_loader_bad = base / "lazy-loader-bad"
        library_duplicate_bad = base / "library-duplicate-bad"
        for path in (
            source,
            good,
            bad,
            cascade_bad,
            hidden_content_bad,
            class_state_bad,
            font_face_bad,
            overlay_bad,
            lazy_loader_bad,
            library_duplicate_bad,
        ):
            path.mkdir()
        (source / "css").mkdir()

        ix_transform = (
            "transform: translate3d(0, 100vh, 0) scale3d(0.4, 0.4, 1) "
            "rotateX(0) rotateY(0) rotateZ(-10deg) skew(0, 0);"
        )
        (source / "index.html").write_text(
            f"""
            <nav>
              <div class="nav-child left" style="-webkit-transform:translate3d(-100%, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(-100%, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);height:3rem"></div>
              <div class="menu-bar-whipe"></div>
              <div class="header-bar nav-link one" style="opacity:0;transform:translate3d(0, -200%, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)"></div>
            </nav>
            <div class="bg-whipe" style="width:100%;height:0%"></div>
            <div class="recent-info-parent" style="transform:translate3d(0, 110%, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)">Recent info</div>
            <div class="img-parent top-size" style="width:100%;height:0rem"></div>
            <main data-w-id="ix-1" style="opacity:0; {ix_transform} color:red">Source</main>
            """,
            encoding="utf-8",
        )
        (source / "css" / "site.webflow.css").write_text(
            ".demo-source { color: red; }\n.mc-source { display: block; }\n",
            encoding="utf-8",
        )
        (good / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    [data-flowbridge-ix-state="ixs-1"] { transform: translate3d(-100%, 0, 0) scale3d(1, 1, 1); height: 3rem; }
                    [data-flowbridge-ix-state="ixs-2"] { opacity: 0; transform: translate3d(0, -200%, 0) scale3d(1, 1, 1); }
                    [data-flowbridge-ix-state="ixs-3"] { width: 100%; height: 0%; }
                    [data-flowbridge-ix-state="ixs-4"] { width: 100%; height: 0rem; }
                    [data-flowbridge-ix-state="ixs-5"] { transform: none !important; }
                    .demo-source { color: red; }
                    .mc-source { display: block; }
                  </style>
                </div>
                <div class="fb-styles-splide w-embed">
                  <style>
                    .splide__track { overflow: hidden; }
                    .splide { visibility: visible !important; opacity: 1 !important; }
                    .splide__track { visibility: visible !important; opacity: 1 !important; }
                  </style>
                </div>
                <div class="fb-media-site w-embed"><style></style></div>
              </div>
              <nav>
                <div class="nav-child left" data-flowbridge-ix-state="ixs-1"></div>
                <div class="menu-bar-whipe"></div>
                <div class="header-bar nav-link one" data-flowbridge-ix-state="ixs-2"></div>
              </nav>
              <div class="bg-whipe" data-flowbridge-ix-state="ixs-3"></div>
              <div class="img-parent top-size" data-flowbridge-ix-state="ixs-4"></div>
              <div class="recent-info-parent" data-flowbridge-ix-state="ixs-5">Recent info</div>
              <main data-w-id="ix-1" style="color:red; transform: rotate(45deg)">Good</main>
            </div>
            """,
            encoding="utf-8",
        )
        (font_face_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    @font-face{font-family:Demo;src:url("fonts/Demo.woff2")}
                    .demo { font-family: Demo; }
                  </style>
                </div>
              </div>
              <main data-w-id="ix-1">Font-face bad</main>
            </div>
            """,
            encoding="utf-8",
        )
        (overlay_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    .bg-whipe { height: 0% !important; pointer-events: none !important; }
                    .demo-source { color: red; }
                    .mc-source { display: block; }
                  </style>
                </div>
              </div>
              <main data-w-id="ix-1">
                <div class="bg-whipe bg-grey" style="height: 0% !important; pointer-events: none !important;"></div>
              </main>
            </div>
            """,
            encoding="utf-8",
        )
        (lazy_loader_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    .demo-source { color: red; }
                    .mc-source { display: block; }
                  </style>
                </div>
                <div class="fb-scripts w-embed">
                  <script>
                    document.addEventListener('DOMContentLoaded', function () {
                      document.querySelectorAll('video.lazy').forEach(function (video) {
                        video.querySelectorAll('source[data-src]').forEach(function (source) {
                          source.src = source.dataset.src;
                        });
                        video.load();
                        video.classList.remove('lazy');
                      });
                    });
                  </script>
                </div>
              </div>
              <main data-w-id="ix-1">
                <video class="lazy" autoplay data-flowbridge-inline-video-autoplay="true">
                  <source data-src="videos/demo.mp4" src="videos/demo.mp4" data-flowbridge-inline-video-src="true" type="video/mp4">
                </video>
              </main>
            </div>
            """,
            encoding="utf-8",
        )
        (library_duplicate_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    .demo-source { color: red; }
                    .mc-source { display: block; }
                  </style>
                </div>
                <div class="fb-scripts w-embed">
                  <script src="https://cdn.jsdelivr.net/npm/@splidejs/splide@3.2.2/dist/js/splide.min.js"></script>
                  <script src="https://cdn.jsdelivr.net/npm/@splidejs/splide@4.1.4/dist/js/splide.min.js"></script>
                </div>
              </div>
              <main data-w-id="ix-1">Duplicate library bad</main>
            </div>
            """,
            encoding="utf-8",
        )
        (bad / "index.html").write_text(
            f"""
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-splide w-embed">
                  <style>
                    .splide__track {{ overflow: hidden; }}
                    .splide.is-initialized, .splide.is-rendered {{
                      visibility: visible !important;
                      opacity: 1 !important;
                    }}
                  </style>
                </div>
              </div>
              <nav>
                <div class="nav-child left"></div>
                <div class="menu-bar-whipe"></div>
                <div class="header-bar nav-link one"></div>
              </nav>
              <div class="bg-whipe"></div>
              <main data-w-id="ix-1" style="{ix_transform}">Bad</main>
              <div class="fb-runtime w-embed" style="display:none"><script src="js/webflow.js"></script></div>
            </div>
            """,
            encoding="utf-8",
        )
        (cascade_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    .nav-child.left { transform: translate3d(-100%, 0, 0) scale3d(1, 1, 1); height: 3rem; }
                    [data-flowbridge-ix-state="ixs-2"] { opacity: 0; transform: translate3d(0, -200%, 0) scale3d(1, 1, 1); }
                    [data-flowbridge-ix-state="ixs-3"] { width: 100%; height: 0rem; }
                    .nav-child.left { height: 30rem; }
                  </style>
                </div>
                <div class="fb-styles-splide w-embed">
                  <style>
                    .splide__track { overflow: hidden; }
                    .splide { visibility: visible !important; opacity: 1 !important; }
                    .splide__track { visibility: visible !important; opacity: 1 !important; }
                  </style>
                </div>
              </div>
              <nav>
                <div class="nav-child left" data-flowbridge-ix-state="ixs-1"></div>
                <div class="header-bar nav-link one" data-flowbridge-ix-state="ixs-2"></div>
              </nav>
              <div class="img-parent top-size" data-flowbridge-ix-state="ixs-3"></div>
              <main data-w-id="ix-1">Cascade bad</main>
            </div>
            """,
            encoding="utf-8",
        )
        (hidden_content_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    [data-flowbridge-ix-state="ixs-tabs"] { opacity: 0 !important; }
                  </style>
                </div>
                <div class="fb-styles-splide w-embed">
                  <style>
                    .splide { visibility: visible !important; opacity: 1 !important; }
                    .splide__track { visibility: visible !important; opacity: 1 !important; }
                  </style>
                </div>
              </div>
              <main>
                <div class="tabs-blog w-tabs" data-flowbridge-ix-state="ixs-tabs">
                  <div class="w-layout-grid two-col-grid">
                    <a href="#" class="parent blog-size w-inline-block">
                      <img src="images/post.webp" alt="Post">
                      <div>Visible article title</div>
                    </a>
                  </div>
                </div>
              </main>
            </div>
            """,
            encoding="utf-8",
        )
        (class_state_bad / "index.html").write_text(
            """
            <div class="fb-page-wrapper">
              <div class="fb-custom-code" style="display:none">
                <div class="fb-styles-site w-embed">
                  <style>
                    .nav-child.left { transform: translate3d(-100%, 0, 0) !important; height: 3rem !important; }
                    .img-parent.top-size { width: 100% !important; height: 0rem !important; }
                  </style>
                </div>
              </div>
              <nav>
                <div class="nav-child left">
                  <a href="#"><img src="images/logo.svg" alt="Logo"></a>
                </div>
              </nav>
              <div class="img-parent top-size">
                <img src="images/post.webp" alt="Post">
              </div>
            </div>
            """,
            encoding="utf-8",
        )

        source_inv = inventory_root(source)
        good_inv = inventory_root(good)
        bad_inv = inventory_root(bad)
        cascade_bad_inv = inventory_root(cascade_bad)
        hidden_content_bad_inv = inventory_root(hidden_content_bad)
        class_state_bad_inv = inventory_root(class_state_bad)
        font_face_bad_inv = inventory_root(font_face_bad)
        overlay_bad_inv = inventory_root(overlay_bad)
        lazy_loader_bad_inv = inventory_root(lazy_loader_bad)
        library_duplicate_bad_inv = inventory_root(library_duplicate_bad)

        assert source_inv and source_inv["dataWIdCount"] == 1
        assert source_inv["ixInlineStyleAttrs"]["count"] >= 1
        assert good_inv is not None
        assert bad_inv and bad_inv["ixInlineStyleAttrs"]["count"] == 1
        assert good_inv["fonts"]["relativeFontUrls"] == []

        good_manifest = build_manifest("webflow-paste", good_inv, good_inv, False, good)
        no_anchor_manifest = build_manifest("webflow-paste", source_inv, good_inv, False, good)
        bad_manifest = build_manifest("webflow-paste", source_inv, bad_inv, False, bad)
        cascade_bad_manifest = build_manifest("webflow-paste", source_inv, cascade_bad_inv, False, cascade_bad)
        hidden_content_bad_manifest = build_manifest(
            "webflow-paste", source_inv, hidden_content_bad_inv, False, hidden_content_bad
        )
        class_state_bad_manifest = build_manifest("webflow-paste", source_inv, class_state_bad_inv, False, class_state_bad)
        font_face_bad_manifest = build_manifest("local-preview", source_inv, font_face_bad_inv, False, font_face_bad)
        overlay_bad_manifest = build_manifest("local-preview", source_inv, overlay_bad_inv, False, overlay_bad)
        lazy_loader_bad_manifest = build_manifest("local-preview", source_inv, lazy_loader_bad_inv, False, lazy_loader_bad)
        library_duplicate_bad_manifest = build_manifest(
            "local-preview", source_inv, library_duplicate_bad_inv, False, library_duplicate_bad
        )
        assert not any(row["status"] == "fail" for row in good_manifest["contractChecks"] if row["id"] != "pretreat-manifest-json")
        assert any(row["id"] == "webflow-paste-site-css-carried" and row["status"] in {"pass", "warn"} for row in good_manifest["contractChecks"])
        assert any(
            row["id"] == "mode-b-initial-state-transport" and row["status"] == "pass"
            for row in no_anchor_manifest["contractChecks"]
        )
        assert any(
            row["id"] == "mode-b-d007-anchor-safety" and row["status"] == "pass"
            for row in no_anchor_manifest["contractChecks"]
        )
        assert any(row["id"] == "local-preview-site-css-carried" and row["status"] == "fail" for row in font_face_bad_manifest["contractChecks"])
        assert any(row["id"] == "local-preview-overlay-neutralization-scope" and row["status"] == "fail" for row in overlay_bad_manifest["contractChecks"])
        assert any(
            row["id"] == "local-preview-lazy-video-idempotence" and row["status"] == "fail"
            for row in lazy_loader_bad_manifest["contractChecks"]
        )
        assert any(
            row["id"] == "local-preview-library-cdn-dedupe" and row["status"] == "fail"
            for row in library_duplicate_bad_manifest["contractChecks"]
        )
        assert any(row["id"] == "mode-b-inline-ix-preserved" and row["status"] == "pass" for row in good_manifest["contractChecks"])
        assert any(row["id"] == "mode-b-runtime-preserved" and row["status"] == "pass" for row in good_manifest["contractChecks"])
        assert any(row["id"] == "mode-b-static-visible-fallbacks" and row["status"] == "fail" for row in bad_manifest["contractChecks"])
        assert any(
            row["id"] == "local-preview-font-face-absence-in-fb-styles-site" and row["status"] == "fail"
            for row in font_face_bad_manifest["contractChecks"]
        )

    print("paste-contract self-test: PASS")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe FlowBridge pre-treatment output-mode contracts.")
    parser.add_argument("--source-root", type=Path, help="Raw source export folder, HTML/CSS file, or ZIP.")
    parser.add_argument("--output-root", type=Path, help="Pretreated output folder, HTML/CSS file, or ZIP.")
    parser.add_argument(
        "--mode",
        choices=("local-preview", "webflow-paste"),
        help="Required for real probes. The probe no longer defaults to local-preview.",
    )
    parser.add_argument("--write-manifest", action="store_true", help="Write pretreat-manifest.json to --output-root.")
    parser.add_argument(
        "--fail-on-contract",
        action="store_true",
        help="Exit non-zero if any contract check fails. This is the default for webflow-paste mode.",
    )
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Report contract failures without failing the process. Intended for exploratory probes only.",
    )
    parser.add_argument("--expect-data-w-id", type=int, help="Assert source data-w-id count equals this number.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in probe smoke tests.")
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Time each named contract check and (when --output-root is a directory) write pretreat-manifest-profile.json beside the manifest. Phase 1B observability.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    global _PROFILE_ENABLED
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        return run_self_test()
    if args.mode is None:
        raise SystemExit("Provide --mode local-preview|webflow-paste. The probe no longer defaults to local-preview.")
    _PROFILE_ENABLED = bool(args.profile)
    _PROFILE_RECORDS.clear()

    source = inventory_root(args.source_root)
    output = inventory_root(args.output_root)
    if source is None and output is None:
        raise SystemExit("Provide --source-root, --output-root, or --self-test.")

    if args.expect_data_w_id is not None:
        actual = source["dataWIdCount"] if source else output["dataWIdCount"]
        if actual != args.expect_data_w_id:
            print(f"Expected data-w-id count {args.expect_data_w_id}, got {actual}.", file=sys.stderr)
            return 1

    manifest = build_manifest(args.mode, source, output, args.write_manifest, args.output_root)
    if args.write_manifest:
        write_manifest(manifest, args.output_root)
    if _PROFILE_ENABLED:
        profile_path = write_profile(args.output_root)
        if profile_path is None:
            print(
                "[--profile] No directory --output-root supplied; per-check timings collected but not written.",
                file=sys.stderr,
            )
        else:
            print(f"[--profile] Wrote {profile_path}", file=sys.stderr)

    print(json.dumps(manifest, indent=2, sort_keys=True))
    fail_closed = args.fail_on_contract or (args.mode == "webflow-paste" and not args.advisory)
    if fail_closed and has_failing_contract(manifest):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
