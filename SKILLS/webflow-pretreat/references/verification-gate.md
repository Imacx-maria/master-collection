# Structural Verification Gate (SV-1 through SV-18)

Mandatory. Load this file at the end of every run before claiming the skill is done. The skill run is NOT complete until every check below has reported with structural evidence.

Every previous "✅ L-X preserved" regression in this project shipped because a checkbox was ticked from a count alone. Ticking a box is not a check — running the procedure below is.

Each check specifies: the property being verified, the procedure (actual command or structural query), the pass criterion (structural, not countable), the failure mode (what the check catches), and the evidence format the report must include. **If a check fails, the output is INVALID — do not zip, do not report success, do not claim "shipped". Fix the source and re-run the gate.**

---

## SV-1 — @font-face placement is exactly one location (HEAD inline per L-1 Option B)

**Property:** Every `@font-face` block in the pre-treated output lives in exactly one location: the HEAD inline `<style>` block of `index.html`. Under L-1 Option B, the site CSS file `css/[sitename].webflow.css` is inlined into HEAD then deleted from the output ZIP, so no disk copy exists to duplicate against. `@font-face` must NOT appear in any `w-embed` `<style>` block (Hard Rule #2), must NOT appear in any other body `<style>` block, and must NOT appear in any CSS file on disk. The count in HEAD inline `<style>` must equal the count in the original export's `css/[sitename].webflow.css`.

**Procedure:**

```bash
# Count total @font-face in index.html
grep -c '@font-face' index.html

# Count inside HEAD <style>
python3 -c "
import re
html = open('index.html').read()
head = re.search(r'<head.*?</head>', html, re.S).group(0)
total = 0
for m in re.finditer(r'<style[^>]*>(.*?)</style>', head, re.S):
    total += m.group(1).count('@font-face')
print('HEAD @font-face count:', total)
"

# Count inside fb-media-site (must be 0)
python3 -c "
import re
html = open('index.html').read()
m = re.search(r'class=\"fb-media-site[^\"]*\"[^>]*>\s*<style[^>]*>(.*?)</style>', html, re.S)
print('fb-media-site @font-face count:', m.group(1).count('@font-face') if m else 0)
"

# Count inside any other w-embed <style> (must be 0)
python3 -c "
import re
html = open('index.html').read()
total = 0
for m in re.finditer(r'class=\"[^\"]*w-embed[^\"]*\"[^>]*>\s*<style[^>]*>(.*?)</style>', html, re.S):
    total += m.group(1).count('@font-face')
print('w-embed @font-face count (all embeds):', total)
"

# Confirm css/[sitename].webflow.css is absent on disk — list any site CSS still shipped
ls css/*.webflow.css 2>/dev/null || echo 'no css/*.webflow.css on disk (expected under L-1 Option B)'

# Original export count for reference — read from the unmodified fixture ZIP
# (compare against HEAD count above)
```

**Pass criterion:** HEAD inline `<style>` count equals the original export's `css/[sitename].webflow.css` count AND every other location count is zero (w-embed `<style>` blocks, other body `<style>` blocks, any `css/*.webflow.css` file on disk). Duplication across any two locations is ALWAYS a fail. Zero `@font-face` anywhere is a fail unless the original export also had zero.

**Failure mode this catches:** 047 shipped with 10 `@font-face` = 5 in HEAD `<style data-flowbridge-inline-css="site">` + 5 duplicates mid-body, and zero in `fb-media-site`. Total count = 10 satisfied the shallow "grep -c = 10 ✅" check. SV-1 would have failed on the duplication across two locations. Under Option B, the additional failure mode caught is "HEAD has N `@font-face` AND a stray `css/[sitename].webflow.css` remains on disk with M more" — both counts non-zero = fail.

**Evidence format:**

```
Original export @font-face in css/[sitename].webflow.css: N
HEAD <style>: A           (lines X-Y per block)
fb-media-site <style>: B  (must be 0)
Other w-embed <style>: C  (must be 0)
Other body <style>: D      (must be 0)
css/*.webflow.css files still on disk: [list or "none"] (must be "none")
VERDICT: A == N and B == C == D == 0 and no site CSS on disk  →  PASS / FAIL (which and why)
```

**Manifest row format:** L-1.1, L-1.2, L-1.3 (Mandatory Output Manifest, SKILL.md §Mandatory Output Manifest — Before You Zip) — SV-1's evidence feeds the per-location `@font-face` counts + the `css/*.webflow.css`-on-disk check; all three rows must PASS for SV-1 to PASS.

---

## SV-2 — @font-face family-name policy compliance

**Property:** Every `@font-face` in the pre-treated output uses the family-naming policy specified by L-1 in the CURRENT SKILL.md. If L-1 says "preserve original variant names" (e.g. `Ppmori Extra Bold`), verify that. If L-1 says "canonicalize to base family + numeric weight" (e.g. `Ppmori` + `font-weight: 800`), verify that. Either way, verify consistency across all `@font-face` blocks AND all usage sites.

**Procedure:**

```bash
# Extract every @font-face family-name value
python3 -c "
import re
html = open('index.html').read()
for m in re.finditer(r'@font-face\s*\{[^}]*\}', html, re.S):
    body = m.group(0)
    fam = re.search(r'font-family:\s*([^;]+);', body)
    weight = re.search(r'font-weight:\s*([^;]+);', body)
    src = re.search(r'src:\s*url\(([^)]+)\)', body)
    print(f'family={fam.group(1).strip() if fam else \"?\"} | weight={weight.group(1).strip() if weight else \"?\"} | src={src.group(1).strip() if src else \"?\"}')
"

# Extract every font-family usage in styles.html / fb-styles-site
grep -oE 'font-family:[^;}]*' styles.html 2>/dev/null | sort -u
grep -oE 'font-family:[^;}]*' index.html | sort -u
```

**Pass criterion:** read SKILL.md's current L-1 rule. Either:

- **Policy A (preserve variants):** every @font-face family name matches a variant-named family that appears verbatim in at least one usage site. No canonicalized base names exist as @font-face families. No usage sites reference a family name that has no matching @font-face.
- **Policy B (canonicalize to base):** every @font-face uses a base family name (e.g. `Ppmori`, not `Ppmori Extra Bold`) paired with an explicit numeric `font-weight`. Every usage site references a base family name and specifies an explicit `font-weight` matching the variant. Zero variant-named families exist in the output.

Whichever policy L-1 declares, declarations and usage sites must agree. Mismatches between policy declarations and what the output actually contains are fails.

**Failure mode this catches:** the skill declares one policy but the output implements the other, or mixes them. Specifically: styles.html still uses `Ppmori Extra Bold` while @font-face has been canonicalized to `Ppmori`, or vice versa.

**Evidence format:**

```
L-1 policy (read from SKILL.md line ___): [Policy A | Policy B]
@font-face family set: {...}
font-family usage set (styles.html): {...}
font-family usage set (fb-styles-site): {...}
VERDICT: policy agreement  →  PASS / FAIL (which mismatch)
```

**Manifest row format:** L-1 family-name policy is captured alongside L-1.1..L-1.4 rows in the manifest; SV-2's evidence (policy read + @font-face family set + usage set + mismatch list) is the narrative attached to those rows when a mismatch fires.

---

## SV-3 — Fluid-typography cascade atomicity (L-2.1)

**Property:** If the source contained an unconditional `html { font-size: ... }` (or `:root` / `body` equivalent) AND one or more `@media` overrides for that exact selector+property pair, all of them must live as a contiguous run at the TOP of `fb-media-site`'s `<style>` block, in original source order. The unconditional base rule must not appear anywhere else in the file.

**Procedure:**

```bash
# Confirm fb-media-site has the cascade
python3 -c "
import re
html = open('index.html').read()
m = re.search(r'class=\"fb-media-site[^\"]*\"[^>]*>\s*<style[^>]*>(.*?)</style>', html, re.S)
if not m:
    print('FAIL: no fb-media-site embed')
else:
    style = m.group(1)
    unconditional = re.findall(r'(?:^|[^@])\s*(html|:root|body)\s*\{[^}]*font-size[^}]*\}', style)
    at_media = re.findall(r'@media[^{]*\{[^{}]*(?:html|:root|body)[^{}]*font-size[^{}]*\}[^{}]*\}', style)
    print(f'fb-media-site unconditional font-size rules: {len(unconditional)}')
    print(f'fb-media-site @media font-size rules: {len(at_media)}')
"

# Confirm unconditional rule NOT in any other embed
grep -n 'html\s*{\s*font-size' index.html
```

**Pass criterion:** `html { font-size }` unconditional rule exists in fb-media-site's `<style>` exactly once AND appears nowhere else in `index.html`. All matching `@media` overrides are in the same `<style>` block, appearing after the unconditional rule.

**Failure mode this catches:** 046 shipped with the unconditional `html { font-size: 1.125rem }` in a DOM-later embed than the `@media` overrides — cascade inversion made fluid typography dead at every breakpoint 480–1919px.

**Evidence format:**

```
fb-media-site <style> first rule: [verbatim]
fb-media-site @media overrides: N, rule order [verbatim list]
Other locations of html{font-size}: [line numbers or "none"]
VERDICT: cascade atomic  →  PASS / FAIL
```

**Manifest row format:** L-2.1 row in the Mandatory Output Manifest — SV-3's evidence (fb-media-site first rule, @media override order, other-location hits) feeds the L-2.1 row's Result + Evidence columns.

---

## SV-4 — Embed host structure (role-based, L-12 Option A + L-13)

**Property (L-12 Option A, 2026-04-17; role-based enumeration per L-13 — see L-13 at `docs/LESSONS.md:210-221`):** `<body>`'s first child is `<div class="fb-page-wrapper">`. `fb-page-wrapper` direct children, by role:

(a) FIRST direct child is `<div class="fb-custom-code" style="display:none">` — the single hidden embed container;
(b) REMAINING direct children are the original body's content siblings in source order (at least one; multiple allowed when L-13 stacking, reveal-footer, or z-index sibling relationships require — e.g. MNZ `nav` + `wrapper` + `footer-parent`);
(c) ZERO naked `<script>` elements at `fb-page-wrapper` level (every `<script>` lives inside `fb-scripts.w-embed` inside `fb-custom-code` per L-15);
(d) ZERO orphan embed hosts outside `fb-custom-code` (no `fb-media-site`, `fb-styles-*`, `fb-scripts`, or author `styles` embed as a sibling of `fb-custom-code`).

`fb-custom-code` contains, in order: `fb-styles-site`, any `fb-styles-[library]` hosts (e.g. `fb-styles-splide`), `fb-media-site`, `styles` (author's original embed if present), `fb-scripts`. Each embed div has class `w-embed`.

**Procedure:** parse the HTML (BeautifulSoup, or regex if you must) and walk the DOM to confirm the above tree. Do not rely on line-by-line grep. Enumerate `fb-page-wrapper` direct children and verify each falls under a role in (a)/(b); surface any child that fails to match either (a)/(b) or matches (c)/(d).

**Pass criterion:** (a) AND (b) AND (c) AND (d) all hold. Classes are as specified, `w-embed` is present on each embed div. Exactly one `fb-page-wrapper`, one `fb-custom-code`, one `fb-media-site` — nested inside `fb-custom-code`.

**Failure mode this catches:** previous sessions produced outputs with two `fb-custom-code` siblings, or `fb-media-site` as a sibling of `fb-custom-code` instead of nested inside it (pre-Option-A topology), or orphan `<div class="styles w-embed">` as a sibling of `fb-page-wrapper` instead of inside it, OR naked `<script>` elements at wrapper level (pre-L-15 pattern, EXP-005.b conditional finding). Exact-two-child wording (retired) would have FAILED MNZ's valid three-content-sibling structure under L-13.

**Evidence format:** the actual DOM tree, listed to the depth of `fb-page-wrapper` → direct children → direct children. Report class names and element order verbatim.

**Manifest row format:** L-11, L-12, L-13 rows in the Mandatory Output Manifest — SV-4's DOM-tree evidence splits across those three rows (body-single-child for L-11, embed-host-nesting for L-12, source-content-sibling-order for L-13).

---

## SV-5 — HEAD content + disk CSS policy (per L-1 Option B)

**Property:** Under L-1 Option B, HEAD carries the full inlined site CSS as a single `<style>` block and the original linked CSS file is removed from both HEAD and the output ZIP. Specifically:

1. `<head>` contains NO `<link rel="stylesheet" href="css/[sitename].webflow.css">` or any other `<link>` pointing to a local `css/*.css` file.
2. `<head>` contains exactly ONE `<style>` block carrying the full inlined site CSS — `@font-face` blocks, `:root` variables, tag selectors, class rules, `@keyframes`, native `@media` blocks, all of it. Treat the site CSS file as an opaque blob; whatever was in it is in this HEAD `<style>` verbatim (minus the relative-URL rewrites per L-1 step 4). Additional HEAD `<style>` blocks are not permitted unless the skill explicitly emits them for a documented reason; unexplained extras are a fail.
3. `css/[sitename].webflow.css` does NOT exist on disk in the output ZIP.
4. `css/normalize.css` and `css/webflow.css` are not inlined as full files and their local HEAD links do not count as valid preview evidence. They may remain on disk as pass-through assets under L-18, but output HEAD still has zero local `css/*.css` links. The converter-visible baseline evidence is the L-4 floor inside `fb-styles-site`, verified by SV-8.

**Procedure:**

```bash
# List every <link> in HEAD
python3 -c "
import re
html = open('index.html').read()
head = re.search(r'<head.*?</head>', html, re.S).group(0)
for m in re.finditer(r'<link[^>]*>', head):
    print(m.group(0))
"

# List every <style> in HEAD with size summary and rule-kind breakdown
python3 -c "
import re
html = open('index.html').read()
head = re.search(r'<head.*?</head>', html, re.S).group(0)
for i, m in enumerate(re.finditer(r'<style[^>]*>(.*?)</style>', head, re.S)):
    body = m.group(1)
    first_rule = body.strip().split('{')[0].strip()[:80] if body.strip() else '(empty)'
    has_font_face = '@font-face' in body
    has_root = ':root' in body
    has_keyframes = '@keyframes' in body
    has_media = '@media' in body
    print(f'[{i}] bytes={len(body)} @font-face={has_font_face} :root={has_root} @keyframes={has_keyframes} @media={has_media} first_rule={first_rule!r}')
"

# Confirm the site CSS file is gone from disk
ls css/*.webflow.css 2>/dev/null || echo 'no css/*.webflow.css on disk (expected)'

# For size sanity, compare HEAD <style> bytes to original site CSS file bytes (in fixture)
# They should be similar (allowing for url() rewrites shortening strings slightly)
```

**Pass criterion:** zero `<link>` to local `css/*.css` in HEAD AND exactly one HEAD `<style>` block AND that block's size is consistent with the original site CSS file's size AND `css/[sitename].webflow.css` does not exist in the output ZIP. HEAD `<style>` containing class rules / `:root` / `@keyframes` / native `@media` is EXPECTED and PASSES under Option B — these are the site CSS's original contents and that's where they live now. The pre-Option-A prohibition ("no project class CSS in HEAD") is REPEALED. A browser preview that passes only because `normalize.css` or `webflow.css` remains linked in HEAD is not acceptable evidence; L-4 must pass in `fb-styles-site`.

**Failure mode this catches:** (a) HEAD retains a `<link href="css/...webflow.css">` — inlining didn't happen; (b) HEAD retains `normalize.css` / `webflow.css` links that mask missing L-4 baseline in local browser but vanish from the converter path; (c) HEAD has zero or two+ `<style>` blocks with site CSS — partial or duplicated inlining; (d) `css/[sitename].webflow.css` still exists in the output ZIP alongside the HEAD inline — two sources of truth, drift possible; (e) HEAD `<style>` size is dramatically smaller than the source CSS file size — content-aware filtering snuck in somewhere.

**Evidence format:**

```
HEAD <link> to css/*.css: [list or "none"]
HEAD <style> blocks: [count, bytes, rule-kind breakdown per block]
Original site CSS file size (for comparison): [bytes]
css/[sitename].webflow.css on disk: [yes|no] (must be no)
VERDICT: head reflects Option B inlining  →  PASS / FAIL (which property failed)
```

**Manifest row format:** L-1.2, L-1.3 rows in the Mandatory Output Manifest — SV-5's evidence (HEAD `<link>` inventory + HEAD `<style>` block count/size + disk-CSS absence) populates L-1.2 (single HEAD `<style>`) and L-1.3 (zero linked local CSS); the `css/*.webflow.css` disk-absence is already covered by L-1.1.

---

## SV-6 — @font-face count preserved from source, embed hosts unique

**Property:** The pre-treatment preserves every `@font-face` block from the source CSS verbatim — neither introducing new blocks nor dropping source blocks. Under L-1 Option B (opaque-blob inline), the `@font-face` count in the pre-treated `index.html`'s HEAD inline `<style>` equals the `@font-face` count in the source fixture's `css/[sitename].webflow.css`. Source-origin duplicates (e.g. Webflow exports that declare `@font-face` twice with different quoting conventions — see KF-5 in `docs/EXPERIMENTS.md`) pass through verbatim; SV-6 does NOT flag them because they are not skill-introduced. Every named embed host (`fb-page-wrapper`, `fb-custom-code`, `fb-styles-site`, `fb-media-site`, `fb-scripts`, plus any `fb-styles-[library]` hosts the site requires) appears exactly once.

**Scope note:** SV-6 compares the pre-treated `index.html` HEAD `<style>` against the SOURCE fixture ZIP's `css/[sitename].webflow.css`. Under Option B the source CSS file is deleted from the OUTPUT working folder — so the comparison reference is the original fixture ZIP, unpacked to a temp location (or read directly from the ZIP via `unzip -p`). SV-1 enforces that no `css/*.webflow.css` file exists on disk in the output; SV-6 does NOT duplicate that check. SV-6's sole `@font-face` check is: did the skill preserve the source count and not introduce new per-key duplicates?

**Procedure:**

```bash
# @font-face count preservation (skill drift check)
python3 -c "
import re, sys, zipfile

def faces(s):
    seen = {}
    total = 0
    for m in re.finditer(r'@font-face\s*\{([^}]*)\}', s, re.S):
        total += 1
        body = m.group(1)
        fam = re.search(r'font-family:\s*[\"\\']?([^;\"\\']+)[\"\\']?\s*;', body)
        wt  = re.search(r'font-weight:\s*([^;]+);', body)
        st  = re.search(r'font-style:\s*([^;]+);', body)
        src = re.search(r'src:\s*url\([\"\\']?([^)\"\\']+)[\"\\']?\)', body)
        key = (
            (fam.group(1).strip().lower() if fam else '?'),
            (wt.group(1).strip() if wt else '?'),
            (st.group(1).strip() if st else '?'),
            # Normalize url() — strip ../ prefix so source (../fonts/x.ttf) matches output (fonts/x.ttf)
            (re.sub(r'^(\.\./)+', '', src.group(1).strip()) if src else '?'),
        )
        seen[key] = seen.get(key, 0) + 1
    return total, seen

# Source: original fixture ZIP
# Adjust path to the fixture under test
src_zip = sys.argv[1] if len(sys.argv) > 1 else 'fixtures/<fixture>.webflow.zip'
with zipfile.ZipFile(src_zip) as z:
    css_name = next(n for n in z.namelist() if re.search(r'/css/[^/]+\.webflow\.css$', n))
    src_text = z.read(css_name).decode('utf-8', 'replace')

out_text = open('index.html', encoding='utf-8').read()

src_total, src_keys = faces(src_text)
out_total, out_keys = faces(out_text)

print(f'Source @font-face count: {src_total}')
print(f'Output HEAD @font-face count: {out_total}')

fail = False
if src_total != out_total:
    print(f'FAIL: skill changed total count ({src_total} -> {out_total})')
    fail = True

for k, v in out_keys.items():
    sv = src_keys.get(k, 0)
    if v > sv:
        print(f'FAIL: skill-introduced duplicate key={k} source={sv} output={v}')
        fail = True

# Source-origin duplicates (informational, NOT a FAIL)
for k, v in src_keys.items():
    if v > 1:
        print(f'NOTE: source-origin duplicate (pass-through per KF-5) key={k} count={v}')

print('SV-6 @font-face: ' + ('FAIL' if fail else 'PASS'))
"

# Embed host uniqueness (unchanged)
for host in fb-page-wrapper fb-custom-code fb-styles-site fb-media-site fb-scripts; do
  echo "$host: $(grep -c "class=\"$host" index.html) occurrences"
done
# Library-specific hosts (zero or more): match class="fb-styles-<something>"
grep -oE 'class="fb-styles-[a-z0-9-]+ w-embed"' index.html | sort -u | while read cls; do
  host=$(echo "$cls" | sed -E 's/class="(fb-styles-[a-z0-9-]+) w-embed"/\1/')
  if [ "$host" != "fb-styles-site" ]; then
    echo "$host: $(grep -c "class=\"$host " index.html) occurrences (library host)"
  fi
done
```

**Pass criterion:** Output HEAD `<style>` `@font-face` count equals source fixture's `css/[sitename].webflow.css` `@font-face` count AND no unique-key (family-normalized, weight, style, src-path-normalized) appears in the output more times than in the source AND every named embed host occurs exactly once (except `fb-styles-*` additional named embeds which may have ≥1).

**Failure mode this catches:** A skill that silently drops, introduces, or mutates `@font-face` blocks during inlining — the exact class of drift Option B's opaque-blob rule is designed to eliminate. The pre-Option-B 047 regression (5 `@font-face` in HEAD + 5 mid-body duplicates that did NOT exist in source) would FAIL because `out_total > src_total`. Source-origin duplicates (KF-5) do NOT fail because they increase both `out_total` and `src_total` equally, and the per-key counts match. If `out_total != src_total`, the skill has drifted from opaque-blob and the root cause is in the skill, not the source.

**Evidence format:**

```
Duplicate @font-face blocks: [list with counts, or "none"]
Embed host counts: [host: count per host]
VERDICT: unique  →  PASS / FAIL
```

**Manifest row format:** L-14 row in the Mandatory Output Manifest (source-origin `@font-face` duplicates pass-through, informational) — SV-6's per-key count parity evidence + embed-host uniqueness feeds the L-14 row's Evidence; skill-introduced duplicates (out_total > src_total) fail this gate AND fail the L-14 pass-through invariant.

---

## SV-7 — Skill contradiction detection

**Property:** The skill's own rules, as written in SKILL.md and its references, agree with the structural state of the output. If L-1 says "@font-face in HEAD inline `<style>`" AND a general checklist item says "migrate all HEAD custom code to body embeds", those two rules contradict and no compliant output exists. The skill has a bug.

**Procedure:** read SKILL.md's L-rule pointers AND `references/lessons.md` L-1, L-2, L-2.1, L-7, L-8 AND the Verification Checklist items in SKILL.md (each `- [ ]` line). For each lesson, list the invariants it asserts. For each checklist item, list the invariants IT asserts. Cross-reference — flag any pair whose simultaneous satisfaction is structurally impossible.

**Pass criterion:** no contradictions found. If any contradiction is found, THE SKILL IS BROKEN — do not work around it, do not ship, do not claim success. Write a skill-contradiction report and hand back per CLAUDE.md rule 17.

**Failure mode this catches:** at the time this gate was first authored (2026-04-17), SKILL.md had a known contradiction: Verification Checklist required "Head custom code migrated (no custom `<style>`, `<link>`, or `<script>` left in `<head>`)" while L-1 required "@font-face blocks are present in the HEAD inline `<style>` and the linked `css/*.webflow.css` file". Both could not be true simultaneously. This contradiction is why 047's output shows `@font-face` in HEAD AND duplicates mid-body: the skill resolved an impossibility by duplicating.

**Evidence format:**

```
Rules audited: [L-1, L-2, L-2.1, L-7, L-8, + checklist line numbers]
Contradictions found: [pair-by-pair description or "none"]
VERDICT: skill coherent  →  PASS / FAIL (which contradiction, stop-ship)
```

**Extension (2026-04-19, EXP-010):** SV-7 also fires on Mandatory Output Manifest contradictions. Specifically: (a) any L-rule documented in `references/lessons.md` or `docs/LESSONS.md` that touches the artifact but has NO corresponding row in SKILL.md's manifest row inventory is a contradiction (rule asserts a property the skill is not structurally checking) — FAIL. (b) Any manifest row in SKILL.md's inventory referencing an L-rule that does NOT exist in `references/lessons.md` or `docs/LESSONS.md` is a contradiction (skill is checking a property no rule defines) — FAIL.

**(c) Aspirational-row detection (post-classification, 2026-04-19, EXP-011):** SV-7 clause (c) fires when an L-rule classified `ARTIFACT-TOUCHING` (per the classification model in `docs/LESSONS.md`) has a manifest row in SKILL.md but the row's Check Command column is empty, describes a non-mechanical assertion, or references a command that is demonstrably unrunnable. ARTIFACT-TOUCHING rules MUST carry a runnable grep / parsed-DOM assertion / file diff. Rules classified `INFORMATIONAL`, `VERIFICATION-ONLY`, or `AUTHORING-PROCESS` are EXEMPT from clause (c); their manifest rows are expected to carry an `INFORMATIONAL` tag in the Property column instead of a check command, and this is not a contradiction. Rules classified `SUPERSEDED` or `PASTE-SIDE` are handled by clause (d) and are not read by clause (c).

**(d) Excluded-class detection (2026-04-19, EXP-011):** SV-7 clause (d) fires when (i) an L-rule classified `SUPERSEDED` appears as a manifest row without a `SUPERSEDED → L-N` annotation naming its superseding rule, OR (ii) an L-rule classified `PASTE-SIDE` appears in the pre-zip manifest row inventory at all (paste-side rules belong to the SV-P* gate set and MUST NOT appear in the pre-zip manifest). SUPERSEDED rules may be referenced in SKILL.md's historical notes but must not carry a live manifest row.

**Runtime:** clauses (a)–(d) run together during SV-7 self-check. `scripts/lesson_surface_lint.py` is the authoring-time gate for row existence, classification sync, clause (c) vague/non-mechanical check text, clause (d) excluded-class drift, Gate Report Template sync, lesson index sync, and mirror byte-identity. Any clause firing is FAIL; the self-check HALTs and writes a contradiction report per CLAUDE.md rule 17. Run this extension after every skill patch by reading the L-rule list plus each rule's classification tag from `docs/LESSONS.md` and the manifest row inventory from SKILL.md and cross-referencing.

**Manifest row format:** L-21 row in the Mandatory Output Manifest (Manifest contract self-check) — SV-7's Extension is the enforcement mechanism for L-21. SV-7 PASS requires zero rule↔row contradictions; L-21 PASS requires the manifest itself be complete.

---

## SV-8 — Webflow Baseline + Native Component CSS Surface (L-4)

**Property:** `fb-styles-site` contains the minimum Webflow baseline floor, tag resets, and source-required native Webflow component base CSS needed after the converter/paste path drops or ignores `normalize.css` / `webflow.css` HEAD links: zero body margin, global border-box sizing, html/body height chain, link inheritance, image display/max-width reset, paragraph top-margin reset, and native state rules such as tabs display state when the source uses Webflow Tabs.

**Procedure:** parse every processed HTML file. Locate `div.fb-styles-site.w-embed > style`, then assert its CSS contains:

- `html { height: 100%; }`
- a global border-box rule for `*` plus pseudo-elements, or an equivalent selector set;
- `body { margin: 0; min-height: 100%; }`
- `a { color: inherit; text-decoration: inherit; }`, unless a stronger source site rule for `a` is present;
- `img { max-width: 100%; vertical-align: middle; display: inline-block; }`, unless stronger source site image rules are present.
- `p { margin-top: 0; }`, unless a stronger source site paragraph top-margin rule is present.

Then scan the source DOM for Webflow-native component classes that require `webflow.css` state/base rules. At minimum, if the source contains `.w-tabs`, `.w-tab-content`, `.w-tab-pane`, or `.w--tab-active`, assert `fb-styles-site` contains:

- `.w-tab-content { position: relative; display: block; overflow: hidden; }`
- `.w-tab-pane { position: relative; display: none; }`
- `.w--tab-active { display: block; }`

Then scan `fb-styles-site` for Webflow default body typography/color declarations. If the source site CSS already defines root/body/text typography, `fb-styles-site` must NOT contain an injected baseline rule equivalent to `body { font-family: Arial; font-size: 14px; line-height: 20px; color: #333; }` or a subset that introduces default `font-size: 14px` / `line-height: 20px` on `body`. L-4 permits geometry/tag/native-component baselines, not default Webflow text styling.

For local-browser smoke when available, also assert `getComputedStyle(document.body).marginTop === "0px"` and representative full-bleed content starts at `x=0/y=0`. If paragraphs exist, assert representative `p` elements compute `marginTop === "0px"`. If tabs exist, also assert inactive `.w-tab-pane` elements compute to `display: none` and do not add document height.

**Pass criterion:** all mandatory geometric resets are present in `fb-styles-site`; non-geometric `a` / `img` / `p` resets are present or explicitly superseded by source site CSS; source-present native component rules are present; no synthetic Webflow default body typography/color rule exists when source typography exists. A page that starts at browser default `8px` body margin is always FAIL. A page with paragraphs whose top margin falls back to browser default because Webflow's `p { margin-top: 0; }` baseline was omitted is FAIL. A page with Webflow Tabs in source but missing `.w-tab-pane { display: none; }` / `.w--tab-active { display: block; }` in `fb-styles-site` is always FAIL. A page with source typography plus an added `body { font-size: 14px; line-height: 20px; }` baseline is FAIL under L-23, even if later CSS overrides it for common classes.

**Failure mode this catches:** Codex BigBuns and Srta Colombia outputs removed/ignored baseline CSS and leaked browser defaults: body margin `8px`, full-bleed content shifted to `x=8/y=8`, nav widths/padding computed without Webflow's border-box baseline, and scroll rhythm drifted. MNZ Codex L-5c rerun exposed the native-component/tag-reset variant: missing Webflow tabs base CSS left inactive `.w-tab-pane` elements vulnerable, and missing paragraph top-margin reset let browser default `p` margins add exact page-height drift even though visible content looked mostly correct. Local browser can look "mostly alive" while geometry, tag defaults, or native component state is already wrong.

**Evidence format:**

```
fb-styles-site baseline:
  html height: present/missing
  border-box: present/missing
  body margin/min-height: present/missing
  a reset: present/source-overridden/missing
  img reset: present/source-overridden/missing
  p margin-top reset: present/source-overridden/missing
  native component base rules: [tabs present -> w-tab-pane/w--tab-active present|missing; other w-* present -> checked rules]
  default body typography/color: absent/present/source-premise-recorded
Browser smoke, if run: body.margin=[value], p.marginTop=[value], representative root rect=[x,y,w,h], inactive tab pane display=[value]
VERDICT: L-4 baseline + native component CSS → PASS / FAIL
```

**Manifest row format:** L-4 row in the Mandatory Output Manifest — SV-8's parsed CSS evidence populates the L-4 row. Missing geometry resets or source-required native component state rules FAIL the manifest. The default-body-typography scan also feeds L-23; unexpected default typography FAILs L-23 and should be cited in the L-4 evidence as the baseline boundary violation.

---

## SV-9 — Naked-Script Floor (L-15 + L-15A)

**What it checks:** Zero `<script>` elements exist as direct children of `fb-page-wrapper`. Every `<script>` in the output HTML must be a descendant of EITHER `fb-scripts.w-embed` (source HEAD + body CDN libraries and inline init/defer bodies, inside `fb-custom-code`, inside `fb-page-wrapper`) OR `fb-runtime.w-embed` (exactly the external `<script src="js/webflow.js">` reference, direct child of `fb-page-wrapper`, AFTER all source-content siblings — per L-15A 2026-04-18 EXP-009).

**Why structural, not count-based (rule 13):** a count of `<script>` tags is presence, not placement. SV-9 must verify PLACEMENT — CDN + inline init scripts are inside `fb-scripts` inside `fb-custom-code`; the local Webflow runtime is inside `fb-runtime` sibling to source content.

**How to check (DOM-aware, not grep):**

Use BeautifulSoup (`html.parser`) on every output HTML file. For each file:

1. `soup.find("div", class_="fb-page-wrapper")` → wrapper.
2. `[c for c in wrapper.find_all(recursive=False) if c.name == "script"]` → MUST be empty list.
3. `fb_custom = wrapper.find("div", class_="fb-custom-code", recursive=False)` → not None; `fb_custom.parent is wrapper`.
4. `fb_scripts = fb_custom.find("div", class_="fb-scripts", recursive=False)` → not None; `fb_scripts.parent is fb_custom`.
5. `fb_runtime = wrapper.find("div", class_="fb-runtime", recursive=False)` → present when the source has an external `js/webflow.js` reference; `fb_runtime.parent is wrapper`; when present it must be positioned AFTER the last source-content direct child (SV-13-B verifies this).
6. `all_scripts = soup.find_all("script")` → every element has either `fb_scripts` OR `fb_runtime` in its ancestor chain. CDN libraries + inline init/defer bodies from source HEAD and body live inside `fb_scripts`. The one external `<script src="js/webflow.js">` reference lives inside `fb_runtime` (not inside `fb_scripts`) — SV-9-C does NOT require the runtime script inside `fb_scripts` under the L-15A carve-out; that placement is governed by SV-13-B.
7. jQuery script (src attr contains "jquery") appears BEFORE any other inline init script whose content contains `Webflow.require` / `Webflow.init` / `window.Webflow` within `fb_scripts`.
8. Build a normalized source script inventory from HEAD + body for every processed page. Excluding only the L-19-forbidden inline runtime IIFE and the L-15A local `webflow.js` carve-out, every preserved CDN `src` and every preserved inline body fingerprint must appear inside output `fb-scripts`. Missing HEAD `defer` bodies are FAIL.
9. Run the output-mode probe and require `<mode>-library-cdn-dedupe` PASS. Multiple CDN scripts for the same runtime family (for example Splide v3 and v4, or two jQuery core versions) are a FAIL; keep the compatible source version and record any dropped duplicate in manifest evidence.
9. Validate inline `<script type="application/ld+json">` bodies separately from executable JavaScript: the body must parse as JSON and contain JSON-LD shape (`@context` on an object, or an array of JSON-LD objects). Valid JSON-LD is metadata and is preserved without the L-16 executable runner. Any output script typed as JSON-LD whose body contains executable JavaScript, or any source executable body retagged as JSON-LD, is FAIL because it silently disables the code.

**Failure mode:** if any of 1-7 fail, DO NOT zip. DO NOT claim shipped. Fix the skill (not the output — rule 14) and re-run.

**Evidence format for the result doc:** paste the BeautifulSoup output showing (a) count of wrapper-direct-child `<script>` elements, (b) `fb_scripts` child `<script>` count (CDN + inline inits), (c) `fb_runtime` child `<script>` count (should be exactly 1 when an external `js/webflow.js` reference is present), (d) jQuery / preserved inline-init ordering evidence respecting L-19's inline-content prohibition (external `<script src="js/webflow.js">` present inside `fb-runtime`, zero inline module IIFE), (e) source HEAD+body script inventory parity with output `fb-scripts`. Count matching alone is NOT evidence — placement and inventory accounting are.

**Manifest row format:** L-15, L-15A rows in the Mandatory Output Manifest — SV-9's evidence (wrapper-direct `<script>` count, `fb-scripts` placement, `fb-runtime` placement, jQuery/webflow.js ordering, and `<mode>-library-cdn-dedupe`) splits across L-15 (CDN + inline init inside `fb-scripts.w-embed`, no duplicate runtime CDN families) and L-15A (webflow.js late placement inside `fb-runtime.w-embed`).

---

## SV-10 — Multi-Dependency Init Gating Structural Check (L-16)

**Property:** Every retained inline init/custom-code `<script>` inside `fb-scripts.w-embed` that references one or more runtime globals OR immediately queries, mounts onto, animates, observes, or binds to source DOM is wrapped in the L-16 multi-dependency runner shape. The `need[]` array is a non-strict superset of every global referenced in the original body and may be empty for selector-only bodies; bodies that immediately touch page DOM include required/optional selector readiness evidence. Required selectors must exist before `fbRun`; optional selectors only require DOM parsed before `fbRun`. The wrapper preserves the original body verbatim inside `fbRun`; the polling loop is bounded (50ms × 200 = 10s cap) and warns on timeout. The accepted emitted shape is per-body: the executable body itself lives inside the wrapper. A shared helper preamble with raw executable bodies left outside `fbRun` is a FAIL. This includes HEAD `defer` DOM-binding bodies, kept GSAP/ScrollTrigger exceptions, and arbitrary source custom code, not only third-party component libraries. Bare CDN `<script src>` elements are NOT wrapped in the runner (they are loads, not inits) and valid `application/ld+json` metadata scripts are NOT executable JS; both are still accounted for by SV-9 placement/inventory.

**Procedure:** parse every inline `<script>` (no `src` attribute) inside `fb-scripts.w-embed`. For each:

1. List the runtime globals the original body references (scan for `window.<X>`, `jQuery`/`$`, `Webflow`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, site-defined globals, any other library global the source uses). `need[]` may be empty only when no runtime globals are referenced.
2. Confirm the wrapper shape is present — `need = [...]`, `fbReady`, `fbRun`, `setTimeout`-recursion (or `requestAnimationFrame`) with a bounded counter, `console.warn` on timeout. `setInterval` is rejected by the probe and is not a valid L-16 polling primitive. The original executable body must sit inside that wrapper, not beside it.
3. Confirm `need[]` is a non-strict superset of the globals listed in step 1.
4. If the original body immediately queries, mounts onto, animates, observes, or binds to source DOM selectors (jQuery `$('<selector>')`, `document.querySelector(All)`, `new Splide(...)` over selected roots, `gsap.to('<selector>')`, `ScrollTrigger.create({ trigger: '<selector>' })`, `document.querySelector('.menu-dropdown').addEventListener(...)`, Swiper/Embla/Flickity/Lottie mount roots, custom widget roots), classify each selector as required or optional and confirm the wrapper encodes that classification. Required: the selector is dereferenced without a null guard, mounted as the primary library root, or drives visible behavior that exists on that page; the runner waits for DOM parsed plus selector presence. Optional: the code uses guarded/null-safe lookup, `querySelectorAll` loops that may legitimately be empty, or progressive enhancement that can no-op on pages without that element; the runner waits for DOM parsed but does not require selector presence.
5. Confirm the original init body lives inside `fbRun` and is byte-identical to the source init (no mutations beyond wrapping).

**Pass criterion:** for every retained inline init/custom-code script, `need[]` ⊇ detected-globals (possibly empty for selector-only bodies) AND required DOM selectors are represented in `requiredSelectors[]` (or equivalent) with DOM-ready + presence gating AND optional DOM selectors are represented in `optionalSelectors[]`/DOM-ready evidence without presence gating AND the runner shape matches L-16 AND the body inside `fbRun` matches the source. CDN `<script src>` tags and valid JSON-LD metadata scripts are skipped for runner shape; they still pass SV-9 placement/inventory separately.

**Failure mode this catches:** single-global gate races — retained code fires after the first listed global exists but before other required libraries/custom globals have loaded (e.g., code that touches both `Webflow` and `Splide` but gates on `Webflow` alone), causing silent no-op at paste time. It also catches DOM-order races introduced by moving source body-end or HEAD-defer custom code into early `fb-scripts`: MNZ section 2 had `window.Splide` and `$` ready but `.slider2` not yet parsed, so the init selected zero elements and mounted nothing; Srta Colombia had a HEAD `<script defer>` menu click-forwarder that was captured but not emitted. The same race applies to kept GSAP/ScrollTrigger exception code whose targets/triggers are not parsed yet. Pre-L-16 single-global template at `references/lessons.md` (old `waitForDep(name, cb)` shape) is a FAIL under SV-10 for any multi-global init; post-EXP-016 globals-only wrappers are FAIL for any retained body that immediately depends on source DOM selectors.

**Evidence format:**

```
Inline inits in fb-scripts: N
Per-init:
  [i] detected globals: [list]  need[]: [list]  requiredSelectors[]: [list/N/A]  optionalSelectors[]: [list/N/A]  dom-ready-gate: yes/no/N/A  required-presence-gate: yes/no/N/A  superset-ok: yes/no  shape-ok: yes/no  body-verbatim: yes/no
CDN <script src> (skipped, SV-9 only): M
VERDICT: every init wrapped per L-16  →  PASS / FAIL (which init, which property)
```

**Manifest row format:** L-16 row in the Mandatory Output Manifest — SV-10's per-init detected-globals + `need[]` superset + required/optional selector classification + runner-shape + body-verbatim evidence directly populates the L-16 row's Result + Evidence.

---

## SV-11 — Library Style Host Extraction (L-17)

**Property:** For every third-party component library detected in the source (by library root class presence in body DOM OR by library-specific CDN script in `fb-scripts`), the output satisfies:

(a) ≥1 `fb-styles-[library-slug]` host exists inside `fb-custom-code`, placed before `fb-media-site` in the canonical order (after `fb-styles-site`, before `fb-media-site`, before `fb-scripts`);
(b) the host contains the migrated library CSS payload from every source HEAD stylesheet/style block owned by that library, OR contains the moved source `<link>` with an explicit fetch-fallback note in manifest evidence. If the source has a library root/JS but no explicit HEAD CSS link, infer the deterministic same-package stylesheet only when the package/version/source URL makes that inference unambiguous, fetch/inline it, and record the inference. A visibility fallback without core library CSS markers is FAIL;
(c) ZERO library `<link rel=stylesheet>` or `<style>` nodes remain in `<head>` for that library;
(d) the host's `<style>` content contains a static Designer-visibility fallback with `visibility: visible !important` AND `opacity: 1 !important` on the library root selector + at least one source-present inner-standard-class selector (Splide: `.splide__track`; Swiper: `.swiper-wrapper`; etc.). Runtime-state-only selectors such as `.splide.is-initialized` / `.splide.is-rendered` are library runtime evidence, not static-visible fallback evidence.

**Procedure:** (1) enumerate libraries present in the source by scanning body DOM for known root classes (`.splide`, `.swiper`, `.lenis`, `.lottie`, `.embla`, `.flickity`, any future library) AND by scanning `fb-scripts` for library CDN script `src` URLs; (2) enumerate source HEAD `<link rel=stylesheet>` and `<style>` nodes owned by each detected library; (3) if a root/JS signal exists but no HEAD CSS source exists, decide whether same-package CSS inference is deterministic (same CDN package + version/path convention); if yes, fetch and inline it, if no, HALT rather than emit fallback-only CSS; (4) for each detected library, locate the matching `fb-styles-[slug]` host inside `fb-custom-code`; (5) confirm the host contains each migrated/inferred stylesheet/style payload (fetched CSS bytes preferred; moved source `<link>` only when fetch fallback is recorded); (6) confirm core CSS markers exist for that library (examples: Splide `.splide__track` + `.splide__list`, Swiper `.swiper-wrapper` + `.swiper-slide`, Flickity `.flickity-viewport`, Embla `.embla__container` when present in the package CSS); (7) confirm HEAD contains no residual `<link rel=stylesheet>` or `<style>` nodes owned by that library; (8) parse the host's `<style>` content for the fallback rule — regex or BeautifulSoup-parse the CSS for `visibility: visible !important` AND `opacity: 1 !important` on the library root + ≥1 source-present inner class, and verify the fallback is not satisfied solely by runtime-added state classes.

**Pass criterion:** (a) AND (b) AND (c) AND (d) hold for every detected library, and the host contains library core CSS markers beyond the fallback rule. Missing host, missing migrated/inferred CSS/link payload, residual HEAD node, fallback-only host, missing core markers, non-deterministic CSS inference, or missing fallback are each FAIL on their own.

**Failure mode this catches:** Splide / Swiper / Lottie CSS left in HEAD where Webflow's paste pipeline ignores it → City Girl Guide blank, Blog blank on MNZ paste (EXP-005.c symptom). A local-browser audit can mask this because Chrome loads the residual HEAD CDN before the converter path drops head-only custom code. A fallback-only `fb-styles-[library]` host is also insufficient: visibility fallback does not replace the library's core CSS. Library root hidden before hydration (library's own `opacity: 0`) without the Designer fallback → component invisible in Designer canvas even though paste succeeded structurally. It also catches runtime-dependent false fallbacks such as `.splide.is-initialized, .splide.is-rendered`, which only apply after JS hydration and therefore do not meet Mode B's static-visible claim.

**Evidence format:**

```
Libraries detected: [list with detection signal — root-class vs CDN vs both]
Per-library:
  <library>:
    host: fb-styles-<slug> present inside fb-custom-code [yes/no, position relative to other hosts]
    migrated payload: [source HEAD CSS markers / inferred same-package CSS URL + markers / moved <link> href + fetch-fallback note / missing]
    core CSS markers: [present markers / missing]
    HEAD residue: [list of residual <link>/<style> owned by <library>, or "none"]
    fallback: [fallback CSS excerpt or "missing"; include whether it targets source-present root/inner selectors or only runtime-added state selectors]
VERDICT: (a) AND (b) AND (c) AND (d) for every library  →  PASS / FAIL (which library, which property)
```

**Manifest row format:** L-17 row in the Mandatory Output Manifest — SV-11's per-library (host present + migrated CSS/link payload + HEAD residue + fallback selectors) evidence populates the L-17 row; detected-library count must equal host count, every source HEAD library stylesheet/style must be accounted for in the host, and every library with a hydrate-and-hide runtime must carry the Designer-visibility fallback.

---

## SV-12 — ZIP Inventory Parity (L-18)

**Property:** The output ZIP is flat at the Webflow root (no orphan top-level folder). Every source-ZIP entry that is not a declared-mutation target is present in the output ZIP with identical relative path (minus the single stripped root prefix, if the source-ZIP had one) and byte-identical content. Every local asset reference introduced or rewritten by pre-treatment resolves to a file in the output root. Declared mutations are `index.html` (any processed HTML) and, under L-1 Option B, the single-file deletion of `css/[sitename].webflow.css`. No `index-local.html` sibling is emitted (L-19 narrowed 2026-04-18 EXP-008).

**Procedure:** (1) enumerate source-ZIP entry list from the fixture; (2) if ALL source entries share one common top-level folder prefix, subtract that prefix from each entry path; (3) enumerate output-ZIP entry list; (4) diff the two lists with the declared-mutation carve-outs applied; (5) for every non-mutated entry present in both, compare byte content (SHA256 or byte-for-byte compare) to confirm the skill did not silently rewrite it; (6) parse processed HTML and inline CSS for local URL references (`src`, `href`, `poster`, `srcset`, inline `style=url(...)`, `<source src>`, CSS `url(...)`); ignore external URLs, data URIs, fragments, mail/tel links, and page anchors; (7) normalize each local reference relative to the HTML file's root and confirm it exists in the output entry list; (8) compare missing-reference lists against the raw source fixture. If a missing source reference has exactly one same-directory deterministic candidate after URL-decoding, Unicode normalization, case-folding, and punctuation/separator equivalence, rewrite to that candidate and record the repair. If no unique candidate exists, preserve the source reference, label it source-premise broken, and do not invent a filename.

**Pass criterion:** diff result is empty (after carve-outs), every non-mutated entry's byte content matches between source and output, and there are zero skill-introduced broken local references. Source-premise broken references that are unchanged and have no unique deterministic repair may pass SV-12 only when explicitly listed as source-premise defects in evidence; they remain a promotion/audit HOLD item until the source fixture or asset naming is corrected. Extra entries in output (skill invented a directory, or emitted an `index-local.html` sibling that L-19 narrowed no longer permits) are a FAIL. Missing entries in output (skill dropped a non-mutated asset) are a FAIL. Byte drift on a non-mutated entry is a FAIL. Any local reference that existed in source but resolved there and no longer resolves after pre-treatment is FAIL.

**Failure mode this catches:** Single-root ZIP not stripped → `index.html` nested at `sitename/index.html` in the output, asset URLs `fonts/X.ttf` fail to resolve from HTML root. Dropped `fonts/`, `images/`, `js/`, `documents/`, or media assets → preview broken, re-import broken. Skill silently mutated a non-HTML/CSS file (rare but possible) → byte drift on what should be a pass-through. CSS URL rewrites, HTML path rewrites, or prefix stripping create references to files that do not exist. Filename encoding/case/separator mismatches stay invisible if the check only compares file lists and never dereferences asset URLs. Empty XscpData `payload.assets[]` is a downstream clipboard rule and is not a valid reason for omitted ZIP assets.

**Evidence format:**

```
Source-ZIP entries: N (common root prefix: "<prefix>" or "none")
Output-ZIP entries: M
Declared mutations: index.html + [additional HTML] + css/[sitename].webflow.css (Option B delete)
Extra in output (not in source, not a declared mutation): [list or "none"]
Missing in output (in source, not mutated): [list or "none"]
Byte drift on non-mutated entries: [list or "none"]
Local asset references checked: N
Deterministic repairs applied: [list or "none"]
Skill-introduced broken refs: [list or "none"]
Source-premise broken refs still unresolved: [list or "none"]
VERDICT: inventory parity  →  PASS / FAIL (which entry, which property)
```

**Manifest row format:** L-18 row in the Mandatory Output Manifest — SV-12's source-vs-output entry diff + byte drift list + declared-mutation carve-out (L-1 Option B site CSS delete) + local asset reference reconciliation populates the L-18 row's Result + Evidence; any entry in output not in source (or vice versa, absent carve-out), any byte drift, or any skill-introduced broken local reference FAILs L-18.

---

## SV-17 — Wrapper Impact Boundary + Component-Local Fidelity (L-22)

**Property:** The output preserves source component-local media and hover/mouse interaction details unless a declared L-rule intentionally changes them. Wrapper insertion may change only ancestry-dependent behavior: body/html inheritance, containing blocks, percentage dimensions/offsets, scroll containers/sticky, stacking contexts, sibling selector/order relationships, and `height: 100%` ancestor chains.

**Procedure:**

1. Build source fingerprints for every processed HTML page before wrapper assembly:
   - media elements: `<img>`, `<picture>`, `<video>`, `<source>`;
   - visible CSS background-image containers;
   - hover/mouse/pointer interaction targets (`:hover` selectors, `data-w-id`, inline event attributes, scripts/selectors containing `mouseenter`, `mouseleave`, `mouseover`, `mouseout`, `mousemove`, `hover`, `pointer`);
   - relevant attributes, class chains, inline styles, local asset refs, and source CSS declarations for `object-fit`, `object-position`, `background-size`, `background-position`, `width`, `height`, `aspect-ratio`, `overflow`, `transform`, `transition`, `opacity`, `filter`, `clip-path`.
2. Build the same fingerprints from the output, ignoring generated `fb-*` hosts and the wrapper boundary itself.
3. Diff source vs output fingerprints.
4. For every delta, require a declared L-rule citation that explains the mutation (examples: L-5 lazy video `src`, L-7 overlay neutralization, L-8 narrow IX2 edit, L-16 readiness wrapping, L-18 deterministic asset-reference repair).

**Pass criterion:** zero unexplained deltas. A changed `object-fit`, `background-size`, image asset ref, inline style, class chain, `data-w-id`, hover selector, or mouse/pointer script body without an explicit L-rule citation is FAIL. If a media component changes because a percentage-height ancestor chain changed, the compensation must target the ancestor chain; rewriting the media fit/crop rule is not a valid L-22 explanation.

**Failure mode this catches:** careless "recreation" where the skill leaves the broad wrapper shape correct but silently alters small component details: hover images stop following mouse targets, `object-fit: cover` no longer fills the allocated box, background-image containers lose `cover`/positioning, or source event wiring is dropped. Those failures are not acceptable wrapper side effects unless the ancestry mechanism is proven and compensated.

**Evidence format:**

```
Component fingerprints checked:
  media elements: N
  background-image containers: N
  hover/mouse targets/scripts: N
Unexplained deltas:
  [list selector/path, property/attr/script fingerprint, source value, output value, cited L-rule or "none"]
Declared-rule deltas:
  [list delta + L-rule row]
VERDICT: L-22 component-local fidelity → PASS / FAIL
```

**Manifest row format:** L-22 row in the Mandatory Output Manifest — run `scripts/component_fidelity_probe.py` and paste its JSON result into the Result + Evidence columns. `missingCount=0` and `addedCount=0` PASS; any missing/added fingerprint must cite a specific intentional L-rule mutation row, otherwise the L-22 row FAILs.

---

## SV-13-A — Webflow runtime external reference preserved, never inlined (L-19 narrowed, local-preview mode)

**Output-mode scope:** SV-13-A is the runtime gate for `local-preview` mode. In explicit `webflow-paste` mode, the runtime contract flips: the artifact must contain ZERO `fb-runtime` hosts while preserving the same relative `js/webflow.js` reference count as the source inside `fb-scripts`; SV-18 / `paste_contract_probe.py` owns the Mode B output probe.

**Gate:** The local-preview artifact (`index.html`) contains EXACTLY ONE external `<script src="js/webflow.js"></script>` reference. The local-preview artifact contains ZERO inline `<script>` blocks whose content contains the Webflow module IIFE signature (`(()=>{var e={1361:` or equivalent — whatever module registry prefix the current export ships) OR contains all three of `Webflow.push`, `Webflow.require`, `Webflow.define` concurrently AND length > 50,000 chars (the 071 crash mechanism).

**Primary detection:**

```bash
# External reference: expect exactly 1
grep -c 'src="js/webflow.js"' index.html
# Inline module IIFE: expect 0
grep -c 'var e={1361:' index.html
```

The external-ref count must be 1 (not 0 — that would be a regression to the pre-EXP-008 broad strip; not >1 — duplicate references break source-order preservation). The inline IIFE count must be 0.

**Secondary detection:** parse every inline `<script>` (no `src` attribute) inside the output. For each, check content length and presence of `Webflow.push`+`Webflow.require`+`Webflow.define`. Any match > 50000 chars with all three symbols = FAIL (module IIFE inlined, 071 crash mechanism reintroduced).

**Status on local-preview failure:** DISCARD — either webflow.js is stripped (pre-EXP-008 regression: local preview breaks again) or the module IIFE is inlined (071 crash returns at publish). This is a hard gate for local-preview promotion.

**Linked lesson:** L-19 (narrowed 2026-04-18 EXP-008). Placement of the external reference is governed by SV-13-B (see below), not SV-13-A.

**Manifest row format:** L-19 row in the Mandatory Output Manifest — in local-preview mode, SV-13-A's evidence (`grep -c 'src="js/webflow.js"' index.html` = 1 + `grep -c 'var e={1361:' index.html` = 0 + module-IIFE signature absence) populates the L-19 row's Result; the row FAILs on either zero-or-multiple external refs OR any inline module-IIFE body. In webflow-paste mode, L-19 cites the SV-18 Mode B runtime contract evidence from `pretreat-manifest.json`.

---

## SV-13-B — Local Webflow runtime late placement (L-15A, 2026-04-18 EXP-009, local-preview mode)

**Output-mode scope:** SV-13-B applies to `local-preview` mode. In `webflow-paste` mode, there should be no `fb-runtime` late host to place; the source relative `js/webflow.js` reference is preserved inside `fb-scripts` and SV-18 verifies that Mode B runtime shape instead.

**Gate:** The sole external `<script src="js/webflow.js"></script>` reference executes AFTER all `.fb-page-wrapper` source-content children parse. Early placement inside `fb-scripts` inside the first `fb-custom-code` FAILS — that was the audit-082 regression on MNZ where IX2 hydration missed section 04 opacity, menu height, and footer transform targets.

**Procedure (DOM-aware structural check):**

1. Parse the output `index.html` structurally (BeautifulSoup `html.parser` or equivalent).
2. Locate `.fb-page-wrapper`. Exactly one occurrence expected.
3. Locate exactly one `<script src>` element whose normalized basename is `webflow.js` AND whose `src` is a relative path (NOT absolute HTTP(S)). Exactly one match expected.
4. **FAIL** if that script is a descendant of the early `fb-scripts.w-embed` host inside the first `fb-custom-code` — early placement is the EXP-008 regression.
5. Enumerate `.fb-page-wrapper` direct element children.
6. Exclude the first `fb-custom-code` host from the enumeration; also exclude the `fb-runtime` host (if present) from the enumeration. The remaining direct element children are the source-content siblings.
7. Let `lastContentEnd` = the parsed end-position (e.g., BeautifulSoup `sourceline` + `sourcepos` for the closing tag of the last source-content sibling, OR byte-offset / character-offset from the parsed document tree).
8. Let `scriptStart` = the parsed start-position of the `<script src="js/webflow.js">` tag.
9. **PASS iff** `scriptStart > lastContentEnd` — the runtime script is positioned AFTER the last source-content sibling ends.

**Future preferred host shape (Posture 1, locked):** the `<script src="js/webflow.js">` element is a child of `<div class="fb-runtime w-embed" style="display:none">`, which is itself a direct child of `.fb-page-wrapper` positioned after source-content siblings. This is the emission target for EXP-009 onward.

**Legacy compatibility (Posture 2, audit-comparison only):** the `<script src="js/webflow.js">` is a direct `<body>` child immediately after `.fb-page-wrapper` closes — the passing reconstructed `index-local.html` shape prior to L-19 narrowing. SV-13-B PASSES both postures during audit comparison; production emission must use Posture 1.

**Concrete "after" definition:** the script's parsed `startIndex` (or equivalent DOM-position metric) must be GREATER than the `endIndex` of the last source-content sibling inside `.fb-page-wrapper`, OR greater than the `endIndex` of `.fb-page-wrapper` when the script is a direct `<body>` child (Posture 2).

**Failure mode this catches:** EXP-008 (session 081) placed `js/webflow.js` inside early `fb-scripts` inside the first `fb-custom-code` — before `nav`, `wrapper`, and `footer-parent` parse. IX2 hydration found no targets. Audit-082 confirmed: `.tabs-blog.w-tabs` stuck at opacity 0 instead of reaching 1; `.nav-child.left` stuck at 720×48 instead of 720×480; `.hero-title.pull` transform `none` instead of `matrix(1,0,0,1,0,72.5703)`. SV-13-A passed (external ref present, module IIFE absent); SV-13-B would have failed on two independent checks (descendant of early `fb-scripts` AND script start-index before last source-content end-index).

**Status on local-preview failure:** DISCARD — runtime hydration will miss IX2 targets against an empty DOM. This is a hard local-preview promotion gate.

**Optional runtime smoke (follow-up guard, not a replacement):** after the static gate passes, open the output `index.html` in a headless browser, wait for `DOMContentLoaded` + one animation frame, evaluate `Boolean(window.Webflow) && typeof window.Webflow.require === 'function'` and `document.querySelectorAll('[data-w-id]').length`. Scroll to the fixture's reveal trigger and assert a gate-selector opacity changes above `0.5` in the 75–100% scroll band. Runtime smoke is a secondary guard; the static `startIndex > lastContentEnd` check is the hard pre-paste assertion.

**Linked lesson:** L-15A (2026-04-18 EXP-009) in `docs/LESSONS.md` L-15 section; L-12 exception (narrow `fb-runtime` carve-out from "all embeds inside `fb-custom-code`" invariant); L-19 placement scope-note.

**Manifest row format:** L-15A row in the Mandatory Output Manifest — in local-preview mode, SV-13-B's parsed-DOM evidence (`scriptStart > lastContentEnd`, `fb-runtime.w-embed` is direct child of `.fb-page-wrapper` AFTER source-content siblings, runtime script NOT a descendant of early `fb-scripts`) populates the L-15A row; any of those three sub-assertions failing FAILs L-15A. In webflow-paste mode, L-15A is N/A and SV-18 owns the Mode B runtime absence check.

---

## SV-14 — No upward-relative CSS URLs after inlining (L-1)

**Property:** After the site CSS file is inlined into HTML, CSS asset URLs must resolve from the HTML file's root, not from the old `css/` folder. No processed HTML file may contain `url('../...')`, `url("../...")`, or `url(../...)`.

**Procedure:**

```bash
grep -nE "url\\(['\"]?\\.\\./" index.html styles.html 2>/dev/null || echo "no upward-relative CSS URLs"
```

**Pass criterion:** zero grep hits in every processed HTML file. Expected rewritten shapes include `url('fonts/...')`, `url("fonts/...")`, `url(fonts/...)`, `url('images/...')`, `url("images/...")`, or `url(images/...)`.

**Failure mode this catches:** the skill correctly inlines `css/[sitename].webflow.css` but leaves the CSS-authored `../fonts/...` / `../images/...` paths intact. Once the CSS lives in HTML, those paths resolve outside the export root and local preview loses fonts/backgrounds.

**Manifest row format:** L-1.4 row in the Mandatory Output Manifest — SV-14's grep evidence (`grep -cE "url\(['\"]?\.\./"` across processed HTML → 0) is the L-1.4 row's Check command; any non-zero count FAILs L-1.4.

---

## SV-15 — Lazy video de-lazification executed (L-5 / L-5c)

**Property:** Lazy video source URLs are loadable without relying on runtime lazy-loader code, autoplay videos are not suppressed by lazy/preload hints, and retained lazy-loader runtime bodies are idempotent after pre-treatment.

**Procedure:** parse every processed HTML file and verify:

- every `<source data-src>` inside a `<video>` has a non-empty `src` equal to `data-src`;
- touched sources carry `data-flowbridge-inline-video-src="true"` or an equivalent `data-flowbridge-inline-*` marker;
- every `<video autoplay>` has no `loading="lazy"` and no `preload="none"`;
- touched autoplay videos carry `data-flowbridge-inline-video-autoplay="true"` or an equivalent `data-flowbridge-inline-*` marker.
- if any processed page contains `data-flowbridge-inline-video-src="true"` and a retained executable script that targets `video.lazy`, that retained body has an idempotence guard before any `video.load()` call. The guard must skip reload when child sources already have `src === data-src` or carry the L-5a marker. A retained body that blindly calls `video.load()` after L-5a markers exist is FAIL.

**Optional browser promotion check:** open the output in a browser and inspect every visible `<video>` that was touched by L-5. `currentSrc` must be non-empty and `readyState >= 2`. Media `net::ERR_ABORTED` events are blocking only when they correlate with an empty `currentSrc`, `readyState < 2`, missing visible media, or a converted-only retry/reload pattern caused by a non-idempotent retained lazy-loader.

**Pass criterion:** all static checks are true, including retained lazy-loader idempotence when applicable. A file with zero lazy videos passes with "N/A — no lazy video sources".

**Failure mode this catches:** the skill documentation says L-5 exists, but the actual output still ships `<source data-src="...">` with no `src`, leaving videos blank until a runtime lazy-loader runs. It also catches the subtler post-L-5a failure where the static source copy works but the retained lazy-loader reloads already de-lazified videos and produces avoidable media request cancellations.

**Manifest row format:** L-5 row in the Mandatory Output Manifest — SV-15's evidence (per-video source/src parity + autoplay attr checks + idempotence markers + retained lazy-loader idempotence when applicable) populates the L-5 row; the row PASSes with "N/A — no lazy video sources" when the fixture has no `<video data-src>` elements.

---

## SV-16 — RETIRED 2026-04-18 (EXP-008 L-19 narrowing)

**Status:** RETIRED. This gate is obsolete under L-19 narrowed (EXP-008, 2026-04-18).

**Reason:** SV-16 checked that the paste artifact was runtime-free while an optional `index-local.html` sibling carried the external webflow.js reference for local preview. Under L-19 narrowed, `index-local.html` is no longer emitted — `index.html` is the single HTML deliverable and carries the external `<script src="js/webflow.js">` reference itself. Runtime-present paste artifact and local-preview coherence are now covered by:

- **SV-13-A:** external webflow.js reference preserved exactly once, module IIFE never inlined.
- **SV-13-B:** local Webflow runtime late-placement structural check (L-15A, 2026-04-18 EXP-009).
- **SV-12:** no `index-local.html` sibling in output ZIP.

**Do not reintroduce SV-16 without a separate design decision.** If EXP-008 FAILS (runtime crash reproduces with external src), the correct response is a structural redesign of the local-preview axis — not a resurrected conditional-loader sibling (Maria's no-hacks rule, 2026-04-18).

**Historical reference:** original SV-16 gate text lives in git history prior to commit landing EXP-008 narrowing (session 081, branch `codex/039-fix-mnz-audit-findings`). SV numbering is not renumbered; subsequent SV cross-references remain stable.

---

## SV-18 — Output Mode Contract + Pretreat Manifest

**Property:** The artifact on disk matches its declared output mode and carries a machine-readable `pretreat-manifest.json` that agrees with `index.html`.

**Procedure:** run the paste-contract probe against the raw source root/ZIP and the pretreated output root:

```bash
python3 AI_OS/SKILLS/webflow-pretreat/scripts/paste_contract_probe.py \
  --source-root <raw export root or zip> \
  --output-root output/{lane}_{source-slug}-file_output \
  --mode <local-preview|webflow-paste> \
  --write-manifest \
  --fail-on-contract
```

`--mode` is mandatory. Do not rely on a default or on a stale `pretreat-manifest.json` written by a previous run in a different mode.

For every output mode, the probe must report:

- zero `@font-face` at-rules inside the converter-visible `fb-styles-site` embed (`<mode>-font-face-absence-in-fb-styles-site` PASS). `@font-face` belongs only in the pretreated HTML HEAD inline style per L-1; an embed copy is an L-24 Designer crash hazard and a pre-zip HALT.
- non-baseline source site class selectors are present in converter-visible `fb-styles-site` (`<mode>-site-css-carried` PASS). HEAD-only class/layout CSS is a contract FAIL because the converter does not transport HEAD CSS, and local-preview must not hide that failure behind browser-loaded HEAD styles.
- L-7 overlay neutralization stays per-element and narrow (`<mode>-overlay-neutralization-scope` PASS): no global CSS rule may collapse `.bg-whipe`, and no `.bg-whipe` combo element such as `.bg-whipe.bg-grey` may receive neutralizing `height:0` / `pointer-events:none` inline styles.
- L-5 lazy-video handling is load-safe (`<mode>-lazy-video-idempotence` PASS): output video `data-src` sources are materialized, autoplay blockers are stripped, required L-5a markers exist, and retained `video.lazy` loaders do not call `video.load()` before an already-de-lazified guard.

For `webflow-paste` mode, the probe must report:

- zero IX-shaped source-content inline `style=""` attributes in output;
- required initial visual states are still transported after raw inline-style neutralization. For MNZ-class failures this includes the closed `.nav-child.left` panel, hidden `.nav-link.one` / `.nav-link.two` / `.nav-link.three`, exact-class pure-overlay `.bg-whipe` collapsed width/height states, collapsed `.img-parent.top-size` width/height pairs, `.recent-info-parent` transform state, and component-root exceptions such as `.slider2` with a library visibility fallback instead of hidden inline opacity. Transport CSS must be cascade-dominant; a rule that exists but loses to later or more-specific source class CSS is still a FAIL;
- D-007 menu/overlay anchors are explicitly named, not only implied. If the source contains menu-shell companions such as `.menu-bar-whipe`, the probe row `mode-b-d007-anchor-safety` must PASS: the closed-nav shell is still transported, exact `.bg-whipe` overlays keep their collapsed first frame, and combo backgrounds such as `.bg-whipe.bg-grey` stay out of the pure-overlay transport path;
- zero `fb-runtime` hosts, source-parity relative `js/webflow.js` references preserved inside `fb-scripts`, and zero inline Webflow engine IIFE bodies;
- host topology is valid (`<mode>-host-topology` PASS): exactly one `fb-custom-code` hidden host and exactly one `fb-media-site` host for each processed output, with no split style/script host surface;
- Webflow-global inline code is publish-safe (`<mode>-webflow-global-readiness` PASS): no bare `Webflow.env(`, `Webflow.push(`, or `Webflow.require(` outside an L-16 runner or a safe `window.Webflow = window.Webflow || []; window.Webflow.push(...)` queue;
- output `data-w-id` count equals source count unless a written source-premise exception exists;
- `fb-custom-code style="display:none"` remains when the host exists;
- transported `data-flowbridge-ix-state` CSS does not permanently hide/collapse content-bearing roots in static-visible Mode B. Any marker rule with `opacity:0`, `visibility:hidden`, `display:none`, zero size, or offscreen transform on an element with text/media/link descendants is a FAIL unless it is documented closed chrome or has a verified runtime-independent static-visible fallback;
- relative font URLs are reported as WARN under the current reported-only font policy, not silently accepted;
- the HTML-side subset of L-24 is clean: no `@font-face` in body embeds and no converter-visible paste style host intentionally carries `animation-play-state` toward styleLess serialization;
- `pretreat-manifest.json` exists, parses, declares `schema`, `outputMode`, `animationClaim`, `probesRun`, and no FAIL `contractChecks[]`.

SV-18 also treats runtime-gated readiness guards as a paste-boundary hazard. A `webflow-paste` artifact must not depend on `html.w-mod-js:not(.w-mod-ix2)`, `html.w-mod-js:not(.w-mod-ix3)`, `.w-mod-ix2`, or `.w-mod-ix3` selectors to reveal core content after paste. If the converter output IX payload is empty, any native `styleLess` record carrying hidden/collapsed declarations derived from those guards is a C-origin failure named `runtime-gated-native-style-promotion`.

For `local-preview` mode, the probe must report one local runtime surface (`fb-runtime` + relative `js/webflow.js`), zero inlined Webflow module IIFE signatures, and preserved source `data-w-id` count.

**Pass criterion:** the probe exits 0 and the generated `pretreat-manifest.json` contains no `contractChecks[].status == "fail"`. A run that omits output mode or reuses a stale manifest declaration from another mode is invalid before any PASS/FAIL interpretation begins and must be rerun with an explicit mode. `webflow-paste` mode fails closed by default; `--fail-on-contract` is still shown in runtime commands for readability, and `--advisory` is allowed only for exploratory diagnostics. WARN rows must be copied into `MANIFEST.md` evidence and the final report. A run that omits output mode or reuses a stale manifest declaration from another mode is invalid before any PASS/FAIL interpretation begins and must be rerun with an explicit mode. `webflow-paste` mode fails closed by default; `--fail-on-contract` is still shown in runtime commands for readability, and `--advisory` is allowed only for exploratory diagnostics. WARN rows must be copied into `MANIFEST.md` evidence and the final report.

**Failure mode this catches:** v4.1 proved generated style records can look clean while raw `style` attributes survive through converter `node.data.xattr` and freeze the published Webflow page. Audit 154 proved a second Mode B failure: local HTML can look styled because source class CSS remains in HEAD while `fb-styles-site` lacks those selectors, so the converter/published Webflow output loses core layout CSS. Session 156 proved a third Mode B failure: a library fallback can target only runtime-added initialized/rendered state classes, making the static-visible claim depend on JS hydration. Session 159 proved a fourth Mode B failure: `mode-b-inline-ix-clean` can pass by deleting all IX initial states, leaving the target menu open on load. The named D-007 addendum closes the probe gap where that same family could still be discussed only in prose: menu-shell companions such as `.menu-bar-whipe` and exact `.bg-whipe` pure overlays are now explicit contract anchors rather than implied side effects of other rows. Session 169 proved a fifth Mode B failure: `mode-b-initial-state-transport` can pass while a content-bearing root such as `.tabs-blog.w-tabs` is transported to permanent `opacity:0` and the runtime that would reveal it is absent. A sixth failure class is mode drift: a `local-preview` artifact gets generated and reused as if it were paste-safe because nobody declared the output mode explicitly. SV-18 inspects the pretreated HTML surface before converter transport, not only the generated style records after conversion, and it must prove deletion was paired with equivalent state transport without contradicting `static-visible`.

**Manifest row format:** L-21 row in the Mandatory Output Manifest — cite the exact `paste_contract_probe.py` command, the generated `pretreat-manifest.json` path, the output mode, every FAIL/WARN contract row, and source/output `data-w-id` counts. Any FAIL contract row fails L-21 and halts zip creation. L-24 additionally records the crash-hazard subset checked at this stage and points to the downstream converter invariant probe for XscpData-only hazards.

---

## SV-19 — Mode-B Transport Protocol (L-31) — Runtime-Gated Class-Specific CSS Fallback for IX2-Hidden Initial States (`webflow-paste` only)

**Property:** In `webflow-paste` mode, every IX2-hidden initial-state target detected by `paste_contract_probe.detect_mode_b_targets` carries an L-31 runtime-gated CSS fallback in `fb-styles-site` (or in `fb-styles-{library}` for component-root targets with a `component_fallback_host` annotation). The fallback's selector has the shape `html:not(.w-mod-ix2) <target.selector>` and its body carries the same canonical declarations the probe extracted into `target.required`. The L-7 anti-broaden probe row stays PASS because the runtime-gate prefix excludes L-31 rules from the L-7 candidate set: `parse_simple_class_chain_selector` rejects any selector containing characters outside `[A-Za-z0-9._-]`, and the prefix introduces `:`, ` `, `(`.

**Procedure:** run the paste-contract probe in full mode and assert both transport rows PASS while L-7 anti-broaden and L-8 inline preservation stay PASS:

```bash
python3 AI_OS/SKILLS/webflow-pretreat/scripts/paste_contract_probe.py \
  --source-root <raw export root or zip> \
  --output-root output/{runner}_{source-slug}-file_output \
  --mode webflow-paste \
  --write-manifest \
  --fail-on-contract
```

Required PASS rows:

- `contractChecks[].id == "mode-b-initial-state-transport"` — zero `missing` targets; every detected mode-B target either `transported` (L-31 CSS hit) or `component-root-fallback` (library host hit) per `summarize_initial_state_target`'s classification ladder.
- `contractChecks[].id == "mode-b-d007-anchor-safety"` — covered by the general L-31 mechanism: the menu-shell + child overlay co-transport pattern is satisfied through per-target rules (`html:not(.w-mod-ix2) .nav-child.left { transform: translate3d(-100%,0,0); }` and `html:not(.w-mod-ix2) .bg-whipe { height: 0%; }` together discharge the anchor pair).
- `contractChecks[].id == "webflow-paste-overlay-neutralization-scope"` — STAYS PASS with `skill-injected=0`. L-31 must NEVER re-broaden L-7. The runtime-gate prefix is the mechanical guarantee — verified against `parse_simple_class_chain_selector` in EXP-005.
- `contractChecks[].id == "mode-b-inline-ix-preserved"` — STAYS PASS. L-31 ADDS CSS transport; L-8 inline preservation (164/164 IX-shaped + 35/35 `data-w-id` on MNZ) is unchanged.

**Pass criterion:** all four rows PASS. The L-7 row is the anti-broaden guardrail — even one skill-injected pure class-chain collapse rule that matches a source-DOM class is HALT (re-shipping the original L-7 regression family). The transport rows are the L-31 efficacy check. The L-8 row is the anti-regression check ensuring L-31 did not silently strip the inline state it was supposed to mirror.

**Failure mode this catches:** EXP-002 baseline (Session 290) showed 7 of 8 hardcoded mode-B targets `preserved-inline` with no CSS transport — Webflow paste-side canonicalization could silently drop the inline `style=""` on overlay/hidden-on-load elements, causing the first paint after paste to render the overlay visible (the d007 menu / `.bg-whipe` / `nav-child.left` family of regressions traced through Sessions 159, 160, 164, 169) until IX2 booted and re-applied the hidden state. EXP-004's universalized detector expanded the missing-target count to 84 across 24 unique class chains. SV-19 enforces L-31's runtime-gated CSS transport for every detected target so the first paint matches the IX2 starting state regardless of paste-side inline drop, while the L-7 cross-check ensures the fix does not re-ship the original anti-lesson.

**Manifest row format:** L-21 row in the Mandatory Output Manifest — cite the `paste_contract_probe.py` command, the generated `pretreat-manifest.json` path, the count of L-31 rules emitted into `fb-styles-site` (and per library host where annotated), the FAIL→PASS transitions on `mode-b-initial-state-transport` and `mode-b-d007-anchor-safety`, the `webflow-paste-overlay-neutralization-scope` evidence (`skill-injected=0`), and the `mode-b-inline-ix-preserved` evidence (IX-shaped + `data-w-id` counts unchanged from L-8 baseline). Any FAIL on the transport rows OR any non-zero `skill-injected` count on the L-7 row OR any drop on the L-8 preservation counts halts zip creation.

---

## SV-20 — Visible Text / Glyph Fidelity (L-34)

**Scope:** Both `webflow-paste` and `local-preview` modes. Source content is read-only; any body-text, `<title>`, meta-content, or source-content-attribute mutation is a hard FAIL.

**Procedure:** Run `scripts/content_fidelity_probe.py` with `--source-root <raw-zip-or-folder> --output-root <output-folder> --fail-on-contract --write-manifest`. Exit 0 = PASS; any non-zero exit = FAIL, ZIP must not ship.

```powershell
python AI_OS\SKILLS\webflow-pretreat\scripts\content_fidelity_probe.py `
  --source-root fixtures\<fixture>.webflow.zip `
  --output-root output\{runner}_{source-slug}-file_output `
  --fail-on-contract --write-manifest
```

**PASS criterion:** Exit 0. Manifest row `content-fidelity-text-glyph` status=`pass`. Zero changed body-text channels, zero missing/added text items in the diff.

**FAIL criterion:** Any of:
- Body text node mutation (e.g. `®` → `🍔`, case change, spelling "correction")
- `<title>` reorder or rewording (even if "improvement")
- `<meta>` description/og/twitter content changed
- `alt`, `title`, `placeholder`, `aria-label` attribute value changed
- Any `data-*` user-authored attribute value changed

**Evidence format:** Paste the probe's `details.changedSamples` array (≤5 items) showing `[channel@path] source → output` with exact values. If exit 0, paste the `evidence` string.

**Failure mode this catches:** BigBuns 2026-04-26: 3× `®` (U+00AE) → `🍔` (U+1F354) in `<span class="mc-fade-text">` and `<span class="mc-logo-footer">`. Señorita Colombia 2026-04-26: 3 pages had `<title>` rewritten (index.html reordered; 2 detail pages had titles generated from scratch and a source typo `Bellza` was corrected). Both mutations passed all 4 prior probes because none checked visible-text fidelity. Root cause: implicit model "thematic helpfulness" — no prompt authorised the edits; skill lacked an explicit "do not edit content" statement. L-34 + SV-20 close that gap.

**Manifest row id:** `content-fidelity-text-glyph`

---

## Browser Promotion Gate — Required Before PASS / KEEP

SV-1..SV-18 plus the manifest prove the pretreated ZIP's structural contract. They do not prove the result deserves a PASS/KEEP recommendation. Before reporting PASS/KEEP on a fixture, run a browser promotion pass against a three-way baseline:

1. **Live original** when available, to catch current CMS/runtime behavior.
2. **Raw export served locally** from the raw ZIP extraction, to separate source-export defects from skill defects.
3. **Pretreated output served locally** from the just-produced output folder/ZIP.

Use the same serving protocol and viewport set for raw and pretreated. At minimum capture desktop, tablet, and mobile screenshots; exercise real user-facing menu breakpoints; collect console errors and failed requests; check image/media loads; sample scroll/section geometry; and record runtime/library markers that matter to the page (`w-mod-ix3`, `Webflow`, `Splide`/Swiper/GSAP init markers, active slides, transforms, menu state). If the live site has CMS-expanded content that the raw export lacks, classify that as source/live drift and do not blame the skill without raw-export evidence.

**Promotion rule:** Structural manifest PASS can ship a ZIP, but the audit verdict is only PASS/KEEP when the browser promotion pass has credible evidence and no critical output-only regressions. Single-breakpoint, no-screenshot, no-menu-click, or raw-export-unchecked audits are PARTIAL even when every structural row passes.

**Failure origin:** output wrong vs raw export = `S-origin`; raw and output share the defect vs live = source/export drift; output correct but converter/paste differs = `C-origin` or `W-origin`; browser/server/tooling instability = `E-origin`.

---

## Paste-Side SV Gates — DEF-14 (SV-P1..SV-P6)

SV-1..SV-18 prove the pretreated ZIP's structural invariants and declared output-mode posture. They do **not** prove Webflow accepted the clipboard payload, preserved the Designer DOM shape, emitted the expected published CSS, resolved images, or maintained vertical rhythm. When a paste/publish failure is in scope, run the paste-side gates below **before** adding new skill or converter rules.

Every paste-side failure report must assign one primary origin label:

- `S-origin` — skill output is wrong before the converter sees it.
- `C-origin` — converter/XscpData is wrong.
- `W-origin` — Webflow paste/publish mutates otherwise-correct input.
- `E-origin` — environment, manual step, credential, browser, network, or tooling issue.

Mixed failures may list secondary labels, but the primary label owns the next experiment. Do not design the fix until the origin is labeled.

### SV-P1 — XscpData Structure

**Property:** The converter output is valid `@webflow/XscpData` with the expected wrapper/code-host shape and no known Webflow Designer crash hazards.

**Check:** parse the clipboard JSON and verify: `type === "@webflow/XscpData"`; `payload.assets` exists and is an empty array; the top-level element set has one `fb-page-wrapper` root for the pasted page; `fb-custom-code` exists under that wrapper; every expected HtmlEmbed node (`fb-styles-site`, any `fb-styles-[library]`, `fb-media-site`, `fb-scripts`) is present with payload content intact; no source script is emitted as a naked wrapper child. Also run repo-root `python3 scripts/converter_invariant_probe.py <xscpdata.json>` and require `designer-crash-hazards` plus `static-image-asset-binding` PASS: no HtmlEmbed `@font-face`, no non-string HtmlEmbed `meta.html`, no `animation-play-state` in `styleLess`/variants, no `main_pressed` / `main_focused`, no multiple pseudo-state variant types in one style, no multiple nth-child `@raw` variants in one style, no raw IX2 `selector` / `selectorGuids`, no populated `payload.assets[]`, no unsafe local Image `src`/`srcset`/lazy-attr or CSS/embed image URLs, and no hosted Image `src` missing `data.img.id` before direct copy.

**Origin hint:** FAIL here is usually `C-origin` unless the pretreated source already lacked the required hosts (`S-origin`).

### SV-P2 — Designer DOM / Navigator Shape

**Property:** After paste, Webflow Designer's DOM/Navigator matches the intended structural shape.

**Check:** inspect Designer/Navigator or an exported Designer DOM snapshot after paste. Confirm the root wrapper, direct content siblings, source order, all embed hosts inside `fb-custom-code`, and no orphan embeds or naked scripts. Record the ancestor chain for every custom-code host; a count alone is not evidence.

**Origin hint:** XscpData correct + Designer DOM mutated = `W-origin`; XscpData already wrong = `C-origin`; pretreated source already wrong = `S-origin`.

### SV-P3 — Published CDN CSS Property Diff

**Property:** The published `*.webflow.shared.*.css` contains the bounded CSS properties the pipeline intended to preserve.

**Check:** fetch the compiled Webflow CDN CSS and compare property-level evidence against the pretreated source for: font-family names, `@font-face` registration and canonicalization, native and non-native `@media` preservation, wrapper-compensation rules, class `font-weight` declarations, overlay CSS, IX2 initial-state CSS, and library fallback CSS. Report exact selectors/properties and the pretreated-vs-CDN values.

**Origin hint:** pretreated source correct + XscpData correct + CDN differs = `W-origin`; XscpData omitted the CSS = `C-origin`; source omitted the CSS = `S-origin`.

### SV-P4 — Runtime Console

**Property:** Designer preview and published page have no critical project-caused runtime errors.

**Check:** collect browser console output after paste/preview and after publish. Classify each message as critical project-caused error, third-party benign warning, expected Webflow noise, or environment issue. Errors that stop Webflow, IX2/IX3, library init, image loading, or custom scripts are critical.

**Origin hint:** dependency/init ordering bugs can be `S-origin` or `C-origin`; Webflow-only runtime mutations are `W-origin`; browser/account/network issues are `E-origin`.

### SV-P5 — Image URL Resolution

**Property:** All image and CSS asset URLs resolve after conversion and publish.

**Check:** enumerate URLs from XscpData, published HTML, and compiled CSS. Every URL must resolve to a Webflow CDN/uploaded asset or intentional external URL. No accidental root-relative `images/foo.jpg`, `../images/foo.jpg`, missing upload mapping, or CSS `url()` 404 is allowed. Include HTTP status and final resolved URL for failures.

**Origin hint:** missing upload/relink in XscpData = `C-origin`; dropped asset from pretreated ZIP = `S-origin`; Webflow CDN/publish rewrite failure = `W-origin`; auth/network failure = `E-origin`.

### SV-P6 — Vertical Rhythm / Section-Height Smoke

**Property:** Paste/publish preserves gross layout rhythm before deeper visual parity work.

**Check:** at bounded viewports, compare original, pretreated preview, Designer canvas, and published page for section top offsets, section heights, footer reveal behavior, sticky section behavior, viewport-height chains, scroll-snap anchors, and next-section exposure. Capture the viewport/runtime context for both original and converted targets: `window.innerWidth`, `window.innerHeight`, computed `html.fontSize`, representative text `fontSize` / `lineHeight`, computed `100vh` / `100svh`, fixed nav height, `document.documentElement.className`, and `w-mod-ix` / `w-mod-ix3` presence. This is a smoke gate, not a full pixel audit: it catches compression, hidden sections, wrong wrapper containment, reveal-footer breakage, and responsive-unit/runtime-context illusions early.

**Origin hint:** pretreated preview already wrong = `S-origin`; pretreated preview correct but XscpData/Designer shape wrong = `C-origin`; Designer/published mutation only = `W-origin`; screenshot tooling/browser instability = `E-origin`.

**Paste-side report template:**

```
## Paste-Side Verification Gates

Primary origin label: S-origin / C-origin / W-origin / E-origin
Secondary labels, if any: [...]

| Check | Verdict | Evidence |
|---|---|---|
| SV-P1 XscpData structure + L-24 crash hazards | PASS/FAIL/N/A | [wrapper/code-host payload evidence + `designer-crash-hazards` + `static-image-asset-binding` invariant results] |
| SV-P2 Designer DOM/Navigator shape | PASS/FAIL/N/A | [ancestor chains + source order] |
| SV-P3 Published CDN CSS property diff | PASS/FAIL/N/A | [selector/property pretreated vs CDN values] |
| SV-P4 Runtime console | PASS/FAIL/N/A | [critical errors + classification] |
| SV-P5 Image URL resolution | PASS/FAIL/N/A | [URL/status/final target list] |
| SV-P6 Vertical rhythm/section-height smoke | PASS/FAIL/N/A | [viewport + section top/height evidence] |

Overall: [paste-side PASS only if every in-scope SV-P gate passes]
Next owner: [skill / converter / Webflow observation / environment]
```

---

## Gate Report Template

The skill's final output MUST include a Structural Verification Gate section formatted like this:

```
## Structural Verification Gate

| Check | Verdict | Evidence |
|---|---|---|
| SV-1 @font-face placement | PASS/FAIL | [totals + per-location counts + line numbers] |
| SV-2 family-name policy | PASS/FAIL | [policy read + @font-face set + usage set + mismatch list] |
| SV-3 fluid cascade atomicity | PASS/FAIL | [fb-media-site block content + other-location hits] |
| SV-4 embed host structure | PASS/FAIL | [DOM tree to depth 3] |
| SV-5 HEAD cleanliness | PASS/FAIL | [HEAD <link> list + <style> summary] |
| SV-6 duplicates | PASS/FAIL | [dup list + host counts] |
| SV-7 skill contradiction | PASS/FAIL | [contradictions found list] |
| SV-8 Webflow baseline CSS surface (L-4) | PASS/FAIL | [fb-styles-site baseline floor evidence + body margin smoke if run] |
| SV-9 naked-script floor | PASS/FAIL | [wrapper-direct <script> count + fb_scripts placement + jQuery / preserved inline-init ordering] |
| SV-10 multi-dep init gating (L-16) | PASS/FAIL | [per-init detected-globals + need[] + required/optional selectors + shape + body-verbatim] |
| SV-11 library style host extraction (L-17) | PASS/FAIL | [per-library host + migrated/inferred payload + core CSS markers + HEAD residue + fallback excerpt] |
| SV-12 ZIP inventory parity (L-18) | PASS/FAIL | [source vs output entry diff + byte drift list + local asset reference reconciliation] |
| SV-13-A Webflow runtime external ref preserved, never inlined (L-19 narrowed, local-preview mode) | PASS/FAIL/N/A | [local-preview: `grep -c 'src="js/webflow.js"' index.html` = 1 + `grep -c 'var e={1361:' index.html` = 0; webflow-paste: N/A, covered by SV-18 Mode B runtime preservation / no-engine-IIFE checks] |
| SV-13-B Local Webflow runtime late placement (L-15A, EXP-009, local-preview mode) | PASS/FAIL/N/A | [local-preview: scriptStart vs lastContentEnd evidence from DOM-aware parse; NOT a descendant of early `fb-scripts`; `fb-runtime` host present as direct child of `fb-page-wrapper` after source-content siblings OR body-end-equivalent Posture 2; webflow-paste: N/A, covered by SV-18 Mode B zero-`fb-runtime` + source-runtime-preserved checks] |
| SV-14 no upward-relative CSS URLs (L-1) | PASS/FAIL | [grep evidence across processed HTML] |
| SV-15 lazy video de-lazification (L-5) | PASS/FAIL | [per-video source/src and autoplay attr evidence] |
| SV-16 RETIRED 2026-04-18 (EXP-008 L-19 narrowing) | N/A | [gate retired — coverage moved to SV-13-A + SV-13-B (L-15A late-placement, EXP-009) + SV-12; `index-local.html` no longer emitted] |
| SV-17 wrapper impact boundary + component-local fidelity (L-22) | PASS/FAIL | [source vs output component-fidelity fingerprint diff; every allowed delta cites an L-rule row] |
| SV-18 output mode contract + pretreat manifest | PASS/FAIL | [`paste_contract_probe.py` command, output mode, `pretreat-manifest.json` path, FAIL/WARN contract rows, source/output `data-w-id` counts] |
| SV-19 mode-B transport (L-31) | PASS/FAIL/N/A | [webflow-paste only: probe `mode-b-initial-state-transport` PASS with zero missing + `mode-b-d007-anchor-safety` PASS; cross-check `webflow-paste-overlay-neutralization-scope` STAYS PASS with skill-injected=0; anti-regression `mode-b-inline-ix-preserved` STAYS PASS; count of L-31 rules emitted into fb-styles-site (and per library host); local-preview: N/A — L-31 fires only in webflow-paste] |
| SV-20 visible text/glyph fidelity (L-34) | PASS/FAIL | [`content_fidelity_probe.py --fail-on-contract` exit 0 + manifest row `content-fidelity-text-glyph` status=pass; if FAIL: changedSamples excerpt (channel, path, source→output)] |

Overall: [PASS if all checks PASS, else FAIL — ship=NO]
```

**If overall is FAIL, do not re-zip, do not claim the skill ran, do not hand back as complete. Fix and re-run.**

For audit recommendations, append the Browser Promotion Gate result separately. A structural PASS without the browser promotion evidence can be reported as "ZIP produced / structural PASS" but not as PASS/KEEP.
