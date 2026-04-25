#!/usr/bin/env python3
"""Check that webflow-pretreat lesson surfaces stay synchronized.

This is an authoring-time control-plane check. It validates the skill's
own references/lessons.md, the skill manifest row inventory in SKILL.md,
and verification-gate.md. It does not inspect or transform Webflow ZIPs.

The skill is auto-contained: this lint reads only from the skill's own
folder (SKILL_DIR/references/lessons.md, SKILL_DIR/SKILL.md,
SKILL_DIR/references/verification-gate.md). It has no dependency on the
host project's docs/ folder or any external mirror — it works identically
whether the skill lives in Flowbridge-claude (training) or MASTER-COLLECTION
(ship) or any other host.
"""

from __future__ import annotations

import hashlib  # noqa: F401  # kept for future use
import re
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parents[1]

# Auto-contained: read from the skill's own files, NOT from the host project's docs/.
LESSONS_MD = SKILL_DIR / "references" / "lessons.md"
SKILL_MD = SKILL_DIR / "SKILL.md"
VERIFY_MD = SKILL_DIR / "references" / "verification-gate.md"

ARTIFACT_TOUCHING = {"ARTIFACT-TOUCHING"}
ACK_ONLY = {"INFORMATIONAL", "SUPERSEDED", "PASTE-SIDE", "AUTHORING-PROCESS", "VERIFICATION-ONLY"}
MECHANICAL_EVIDENCE_RE = re.compile(
    r"(`[^`]+`|python|grep|ls\b|diff\b|hash|parse|parsed-DOM|count|enumerate|compare|assert|"
    r"contractChecks|pretreat-manifest\.json|manifest\.json|file list)",
    re.I,
)
VERDICT_RE = re.compile(r"(assert|expect|PASS|FAIL|require|zero|==|>=|<=|equal|exactly|absent|present|empty)", re.I)
VAGUE_CHECK_RE = re.compile(
    r"(untouched\s*/\s*scoped|checklist evidence|manifest/checklist|human review|probably|should pass|TBD|TODO|"
    r"no dedicated check command)",
    re.I,
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise AssertionError(f"missing file: {path}") from None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def lesson_blocks(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(L-\d+)\b.*$", text, re.M))
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[match.group(1)] = text[start:end]
    return blocks


def classifications(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for rule, block in lesson_blocks(text).items():
        m = re.search(r"^\*\*Classification:\*\*\s*([A-Z-]+)", block, re.M)
        if not m:
            out[rule] = "MISSING"
            continue
        out[rule] = m.group(1).strip()
    return out


def manifest_rows(text: str) -> set[str]:
    rows: set[str] = set()
    in_inventory = False
    for line in text.splitlines():
        if line.startswith("**Manifest row inventory"):
            in_inventory = True
            continue
        if in_inventory and line.startswith("**Informational / superseded"):
            break
        if not in_inventory:
            continue
        m = re.match(r"^\|\s*(L-\d+(?:\.\d+|[A-Z])?)\s*\|", line)
        if m:
            rows.add(m.group(1))
    return rows


def split_markdown_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line.strip().strip("|"):
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def manifest_row_details(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    in_inventory = False
    for line in text.splitlines():
        if line.startswith("**Manifest row inventory"):
            in_inventory = True
            continue
        if in_inventory and line.startswith("**Informational / superseded"):
            break
        if not in_inventory:
            continue
        m = re.match(r"^\|\s*(L-\d+(?:\.\d+|[A-Z])?)\s*\|", line)
        if not m:
            continue
        cells = split_markdown_row(line)
        if len(cells) < 3:
            rows[m.group(1)] = {"property": "", "command": ""}
            continue
        rows[m.group(1)] = {"property": cells[1], "command": cells[2]}
    return rows


def row_base(row: str) -> str:
    m = re.match(r"^(L-\d+)", row)
    return m.group(1) if m else row


def row_covers_rule(row: str, rule: str) -> bool:
    if row == rule:
        return True
    if row.startswith(f"{rule}."):
        return True
    suffix = row[len(rule) :] if row.startswith(rule) else ""
    return bool(suffix and suffix.isalpha())


def gate_headings(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"^##\s+(SV-\d+(?:-[A-Z])?)\b(.*)$", text, re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def template_rows(text: str) -> set[str]:
    m = re.search(r"^## Gate Report Template\b(?P<body>.*)$", text, re.M | re.S)
    if not m:
        return set()
    rows: set[str] = set()
    for line in m.group("body").splitlines():
        row = re.match(r"^\|\s*(SV-\d+(?:-[A-Z])?)\b", line)
        if row:
            rows.add(row.group(1))
    return rows


def index_rows(text: str) -> set[str]:
    rows: set[str] = set()
    for line in text.splitlines():
        m = re.match(r"^\|\s*(L-\d+)\s*\|", line)
        if m:
            rows.add(m.group(1))
    return rows


def check_lesson_manifest_sync(errors: list[str]) -> None:
    lesson_text = read(LESSONS_MD)
    skill_text = read(SKILL_MD)

    classes = classifications(lesson_text)
    rows = manifest_rows(skill_text)

    for rule, cls in sorted(classes.items(), key=lambda item: int(item[0].split("-")[1])):
        if cls == "MISSING":
            errors.append(f"{rule}: missing **Classification:** line in references/lessons.md")
            continue
        if cls in ARTIFACT_TOUCHING and not any(row_covers_rule(row, rule) for row in rows):
            errors.append(f"{rule}: ARTIFACT-TOUCHING but no manifest inventory row covers it")
        if cls not in ARTIFACT_TOUCHING and cls not in ACK_ONLY:
            errors.append(f"{rule}: unknown classification {cls!r}")

    for row in sorted(rows):
        base = row_base(row)
        if base not in classes:
            errors.append(f"{row}: manifest inventory row references missing references/lessons.md rule {base}")


def check_manifest_row_tightness(errors: list[str]) -> None:
    lesson_text = read(LESSONS_MD)
    skill_text = read(SKILL_MD)

    classes = classifications(lesson_text)
    rows = manifest_row_details(skill_text)

    for row, detail in sorted(rows.items(), key=lambda item: (int(row_base(item[0]).split("-")[1]), item[0])):
        base = row_base(row)
        if classes.get(base) not in ARTIFACT_TOUCHING:
            continue
        command = detail["command"]
        if not command.strip():
            errors.append(f"{row}: ARTIFACT-TOUCHING row has an empty check-command column")
            continue
        if VAGUE_CHECK_RE.search(command):
            errors.append(f"{row}: ARTIFACT-TOUCHING row has vague/non-mechanical check text: {command[:120]}")
        if not MECHANICAL_EVIDENCE_RE.search(command):
            errors.append(f"{row}: ARTIFACT-TOUCHING row lacks a mechanical evidence shape in the check-command column")
        if not VERDICT_RE.search(command):
            errors.append(f"{row}: ARTIFACT-TOUCHING row lacks an explicit expected verdict or assertion")


def check_gate_template_sync(errors: list[str]) -> None:
    text = read(VERIFY_MD)
    headings = gate_headings(text)
    rows = template_rows(text)

    if not rows:
        errors.append("verification-gate.md: missing or unparsable Gate Report Template table")
        return

    for gate in sorted(headings, key=lambda g: tuple(int(p) if p.isdigit() else p for p in re.split(r"[-]", g[3:]))):
        if gate not in rows:
            errors.append(f"{gate}: gate heading exists but Gate Report Template has no row")

    for row in sorted(rows):
        if row not in headings:
            errors.append(f"{row}: Gate Report Template row has no matching gate heading")


def main() -> int:
    errors: list[str] = []
    checks = [
        check_lesson_manifest_sync,
        check_manifest_row_tightness,
        check_gate_template_sync,
    ]
    for check in checks:
        try:
            check(errors)
        except AssertionError as exc:
            errors.append(str(exc))

    if errors:
        print("lesson-surface lint: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("lesson-surface lint: PASS")
    print(f"- lessons: {LESSONS_MD}")
    print(f"- skill: {SKILL_MD}")
    print(f"- gate:   {VERIFY_MD}")
    return 0


def run_self_test() -> int:
    weak_command = "grep for `.bg-whipe` rule, assert untouched / scoped per L-7 spec"
    strong_command = (
        "`python3 scripts/paste_contract_probe.py --mode webflow-paste --fail-on-contract` "
        '-> `contractChecks[].id == "<mode>-overlay-neutralization-scope"` must PASS with zero collapse rules.'
    )
    assert VAGUE_CHECK_RE.search(weak_command)
    assert MECHANICAL_EVIDENCE_RE.search(strong_command)
    assert VERDICT_RE.search(strong_command)
    assert split_markdown_row(r"| L-1.1 | Property | `ls a \| wc -l` -> expect 0 |") == [
        "L-1.1",
        "Property",
        r"`ls a \| wc -l` -> expect 0",
    ]
    print("lesson-surface lint self-test: PASS")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(run_self_test())
    sys.exit(main())
