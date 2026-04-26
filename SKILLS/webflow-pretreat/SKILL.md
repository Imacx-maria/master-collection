---
name: webflow-pretreat
description: Use when transforming a raw Webflow export ZIP into a pretreated ZIP for FlowBridge converter intake. Triggers on "pre-treat", "pretreat this export", "prepare this webflow.zip", "process this export", "run the pretreat skill", or any .webflow.zip file path. The output is a ZIP whose HTML body has one wrapper child and whose CSS/scripts/assets are restructured for Webflow clipboard paste. This skill carries its own lessons, experiments ledger, and verification gates — it is an auto-research loop: every failure becomes a numbered lesson with origin label, every run is a bounded experiment with pre-declared hypothesis and metric. Cowork is for control-plane checks only; full real-fixture pretreatment runs require Claude Code on Legion or Codex CLI.
version: 6
---

# Webflow Pre-Treat — Auto-Research Skill

You receive one raw Webflow export ZIP and return one complete pretreated Webflow ZIP. The pretreated ZIP is the only successful deliverable — JSON manifests, extracted folders, notes, or partial page outputs are evidence only, never a substitute for the ZIP.

This skill is **self-contained** — its lessons, verification gates, scripts, experiments log, and templates all live inside this folder. No reads from `docs/` of the host project are required; the host project may still cross-reference this skill's lessons if it chooses to.

This skill is **auto-research by design**. Every run is a bounded experiment with pre-declared hypothesis, metric, scope, single-change, and keep/discard criteria. Every failure mode promotes to a numbered lesson in `references/lessons.md` with an origin label (S/C/W/E). Every rule has a verification gate that runs at authoring time (lint) and runtime (manifest). New fixtures added later continue the learning loop under the same protocol.

## Training vs Production — Two Forms

This skill ships in two forms. Both share the same technical core (`references/`, `scripts/`, the L-rules, the SV gates, the HALT discipline) but differ in ceremony:

- **Training (this folder, `Flowbridge-claude/AI_OS/SKILLS/webflow-pretreat/`):** carries the `Before You Run` discipline gate (7 fields + Protected Set), `Auto-Research Loop`, `experiments/EXP-NNN.md` logging. Maria invokes it inside bounded experiments to evolve rules, fix probes, and accumulate the lesson ledger.
- **Production (`MASTER-COLLECTION/SKILLS/webflow-pretreat/`):** stripped of training-only ceremony. End users in Claude Code invoke it with a single sentence ("Pretreat my-export.webflow.zip") and receive a pretreated ZIP. No `Before You Run` gate, no Protected Set, no `experiments/` writes.

**Sync direction is one-way: training → production.** When a learning here warrants promotion (new L-rule, probe fix, workflow refinement), the technical core syncs verbatim and the production SKILL.md / MEMORY.md are regenerated per the spec in `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-25/303-plan-fork-training-vs-production-skill.md`. Never reverse — bug reports from end users become training experiments first, then promote.

## Reference Index — Just-In-Time Loading

Load a reference only when you hit its situation. SKILL.md stays lean so invocation cost is low.

| When you need to... | Load |
|---|---|
| Handle `@font-face`, fluid typography, `@media` routing, reveal overlays, IX2 initial states, lazy video, script runtime, CMS stubs, or anchor tagging | `references/lessons.md` |
| Migrate HEAD custom code, inline site CSS, place embeds, reason about IX3 capability gaps, preserve Webflow native element markers | `references/webflow-constraints.md` |
| Decide `local-preview` vs `webflow-paste` output mode, consult archived mechanical-path evidence, inventory paste-contract hazards | `references/mechanical-consultation.md` |
| Scan source CSS for body-dependent layout, choose compensating CSS, run the post-wrap self-verify checklist | `references/decision-patterns.md` |
| Run Structural Verification Gate (SV-1..SV-20) + Mandatory Output Manifest attestation | `references/verification-gate.md` |
| Run output-mode contract probe on source + output | `scripts/paste_contract_probe.py` |
| Run component fidelity fingerprint probe (L-22) | `scripts/component_fidelity_probe.py` |
| Run visible text/glyph fidelity probe (L-34) | `scripts/content_fidelity_probe.py` |
| Verify lessons/gates/manifest are in sync at authoring time | `scripts/lesson_surface_lint.py` |
| Verify local asset references are not broken | `scripts/asset_ref_check.py` |
| Bootstrap a new experiment prompt | `templates/EXPERIMENT-TEMPLATE.md` |
| Emit a regression report at end of run | `templates/REGRESSION-REPORT-BLOCK.md` |
| Emit a HALT report when a gate fails | `templates/HALT-REPORT-TEMPLATE.md` |
| See what the skill already knows | `MEMORY.md` (always loaded) + `references/lessons.md` |
| See what experiments have been run | `experiments/` (append-only, EXP-NNN.md per run) |

## Before You Run — Experiment Discipline Gate

This skill executes only inside a bounded experiment. Every invoking prompt must declare all seven fields below. If ANY field is missing, ambiguous, or conflicts with the downstream task, **STOP**. Write `experiments/EXP-DRAFT-discipline-violation.md` noting the missing sections, and hand back.

1. **Hypothesis** — a falsifiable statement about what the skill should produce on this fixture.
2. **Metric** — pass/fail criteria referencing SV-1..SV-18 (plus SV-P1..SV-P6 if paste-side is in scope), with an origin label anticipated for any failure: `S-origin` (skill output wrong), `C-origin` (converter defect), `W-origin` (Webflow paste/publish mutation), `E-origin` (environment/tooling).
3. **Scope** — which L-rules, embed hosts, and files are in-bounds. Everything else stays unchanged.
4. **One change** — exactly one of: `skill-applied-to-new-fixture`, `specific-skill-update`, `read-only-diagnostic`. Not two.
5. **Keep/discard criteria** — pre-declared action for PASS, FAIL, PARTIAL outcomes.
6. **Output mode** — exactly one of `local-preview` or `webflow-paste`, plus why that mode matches the downstream task. If the artifact will touch the minimal converter, Webflow Designer paste, or published Webflow, use `webflow-paste`. `local-preview` is reserved for explicit runtime-diagnostic runs.
7. **Runner** — exactly one of `claude` or `codex`. This determines the output prefix and default tooling (PowerShell vs WSL/bash).

### Baseline Capture Gate (Regression Protocol)

For any change that could affect a fixture output, the invoking prompt must also declare a **Protected Set**: the concrete list of SV rows, manifest rows, and paste-parity anchors that are currently PASS and must stay PASS after the change. See `templates/REGRESSION-REPORT-BLOCK.md` for the exact format.

If the Protected Set is missing for a fixture-affecting change, **STOP** with the same violation protocol. Docs-only edits that cannot alter any fixture output surface are exempt; lesson/gate/reference edits are NOT exempt because they can flip gate status silently.

## Mandatory Input Contract

Input is exactly one `.zip` file path — a raw Webflow export. Nothing else is valid input. **Refuse and HALT** if the invoking prompt:

- Hands you loose HTML/CSS/font files and asks you to hand-build a fixture
- Points at a `fixtures/<name>/` folder with no ZIP
- Points at a previous pretreated output folder as input (produces Franken-artifacts)
- Asks you to skip extraction and operate on a pre-extracted working folder

Write `experiments/EXP-DRAFT-input-violation.md` naming the bypass and hand back.

## Source Content Immutability — non-negotiable

Pre-treatment is **structural-only**. The skill restructures HTML, migrates CSS, wraps embeds, gates IX runtime, and preserves assets. The skill does NOT — under any circumstance — alter the content of:

- Body text nodes
- `<title>`, `<meta>` description/og/twitter tags
- `alt`, `title`, `placeholder`, `aria-label` attributes
- `data-*` attributes that hold user-authored content

Read-only means read-only. Even if the source text appears wrong, mis-spelled, mis-branded, off-theme, or obviously a typo — **DO NOT FIX IT**. The skill's job is restructuring, not editing.

Mutation modes that have appeared in past failures and are explicitly banned:
- Replacing `®` with thematic emojis (BigBuns 2026-04-26 incident)
- Reordering or "improving" `<title>` SEO content (Señorita Colombia 2026-04-26 incident — 3 pages affected)
- Swapping case for "consistency" (e.g. `BurGers` → `burgers`)
- Adding emojis next to brand names "to match site theme"
- Translating attribute text "for accessibility"
- Fixing typos or spelling in source text (`Bellza` → `Belleza` is banned even if it is a typo)

If the workflow encounters source text that seems wrong, report it in MANIFEST.md as an INFORMATIONAL note and preserve it byte-for-byte. Do not edit. Ever.

The L-34 probe (`scripts/content_fidelity_probe.py`) enforces this. Any failure of L-34 means the skill mutated source content and the output ZIP must NOT ship.

## Lane Parameter — Runner

The invoking prompt's `Runner:` field determines:

- **Output path prefix:** `output/{runner}_{source-slug}-file_output.zip` and its matching extracted sibling folder.
- **Default tooling:** `claude` → PowerShell examples; `codex` → WSL/bash tooling (`mktemp -d`, `unzip`, `zip`, `find`, `rg`). Both lanes produce identical artifact contracts.
- **Reporting:** report the exact Windows path to the output ZIP first, before any explanation.
- **Lane isolation:** never delete, overwrite, copy from, inspect for generation, or patch the other lane's output. Cross-lane comparison is a separate explicit task with its own invoking prompt.

## Workflow

```
1. Validate the invoking prompt against Before You Run gate (all 7 fields + Protected Set if applicable).
2. Validate the input against Mandatory Input Contract.
3. Extract the ZIP to a TEMPORARY working folder outside output/. Never mutate the source ZIP.
4. Load references/mechanical-consultation.md if output-mode or paste-contract evidence matters.
5. For every HTML file in the extracted export, classify per L-27 BEFORE transformation:
   - Parse <body>, count content-bearing children (tags excluding <script>/<style>/<link>/<meta>/<title>).
   - If content-element count is 0 AND at least one <script> child exists: classify as CMS template stub.
     Do NOT pre-treat; preserve byte-for-byte; record in pretreat-manifest.json under passthroughClassification.l27Stubs.
   - A body with zero children of ANY kind is NOT an L-27 stub. HALT with malformed-export diagnostic.
6. For every non-stub HTML file, run the Per-Element Transformations pass (lessons.md L-5, L-28, L-30, L-31 if webflow-paste mode) BEFORE wrapper assembly. Record each as applied / N-A in the session log.
7. For every non-stub HTML file, apply every transformation, reasoning about each decision
   (consult references/ as the table above indicates).
7a. For `webflow-paste` mode only, emit L-31 mode-B transport CSS into `fb-styles-site` (and into `fb-styles-{component_fallback_host}` for annotated targets) per `references/lessons.md` L-31 ("How to apply"). Invoke `python3 scripts/paste_contract_probe.py --source-root <raw zip or root> --mode webflow-paste --write-manifest <temp.json>` to obtain `inventories[0].modeBTargets`, then bucket targets by `tuple(target.classes)`. **Non-collision buckets** (one distinct `tuple(required)`): emit a single runtime-gated class-chain rule (`html:not(.w-mod-ix2) <selector> { <decls>; }`). **Collision buckets** (≥2 distinct `tuple(required)`, per L-31 collision-handling addendum, EXP-006): assign one marker per unique `required` tuple from a global sequential counter `ix-state-{N}`; for each source HTML element matching the bucket's class chain, identify which `required` tuple matches its inline `style=""` (substring on the canonical fragment) and add `data-flowbridge-ix-state="ix-state-{N}"` to that element (idempotent per L-6 — do not overwrite an existing marker); replace the would-be class-chain rules with marker-keyed runtime-gated rules (`html:not(.w-mod-ix2) [data-flowbridge-ix-state="ix-state-{N}"] { <decls>; }`). Group all L-31 rules into a contiguous block at the end of the host with comment header `/* L-31 mode-B transport (webflow-paste) */`. Skip entirely in `local-preview` mode.
7b. For `webflow-paste` mode only, emit L-33 IX3 name hints as `flowbridge-ix3-name-hints.json` at the output root. This file is advisory metadata for the mechanical converter: it may suggest human-readable names for IX3 interactions/actions whose source export only exposes opaque IDs, but it MUST NOT mutate `js/webflow.js`, inline IX data, interaction IDs, timeline IDs, action IDs, targets, timings, or bindings. If no confident semantic name exists, omit that ID from the hints map; still emit the schema file with empty maps.
8. Immediately after assembling fb-styles-site, run the L-1.5 fast-fail check:
   python3 scripts/paste_contract_probe.py \
     --source-root <raw export root or zip> \
     --output-root <current output root> \
     --mode <local-preview|webflow-paste> \
     --write-manifest --fail-on-contract
   If <mode>-font-face-absence-in-fb-styles-site fails, write HALT-REPORT.md and STOP.
9. Run the Structural Verification Gate (references/verification-gate.md), including SV-18 output-mode contract probing.
10. Produce pretreat-manifest.json beside index.html, produce `flowbridge-ix3-name-hints.json` at the output root when L-33 applies, then produce the Mandatory Output Manifest (see below).
    Run each L-rule row's check command; populate results. If ANY row FAILs, write HALT-REPORT.md and STOP.
11. Confirm full-site coverage: every source ZIP entry is present in the output tree after the single allowed
    root-prefix normalization, except declared mutations/deletions.
12. Only if all gates and manifest rows PASS: write output/{runner}_{source-slug}-file_output.zip
    (MANIFEST.md and pretreat-manifest.json included) and its matching extracted sibling folder.
13. Verify the ZIP exists on disk: Test-Path (PowerShell) or ls (bash). Validate ZIP integrity when tooling is available.
14. If verdict is PASS/KEEP, run the Browser Promotion Gate (verification-gate.md) against live original,
    raw export, and pretreated output. Structural PASS without browser evidence is PARTIAL only.
15. Append an entry to experiments/EXP-NNN.md with the Before You Run declaration + verdict + Protected Set diff.
16. Report: exact Windows path to the output ZIP FIRST. If HALT, report the HALT-REPORT path first and state
    that no paste-test artifact exists.
```

## Mandatory Output Contract

Success output is binary: either (A) a verified complete `output/{runner}_{source-slug}-file_output.zip` plus its matching extracted sibling, or (B) a HALT report inside that sibling folder and NO ZIP. JSON files are required evidence inside the output folder; they are never the final deliverable.

**Deterministic basename:** derive `{source-slug}` from the raw Webflow export filename after removing `.zip`, `.webflow`, and obvious duplicate/export suffixes when present. Use lowercase ASCII, hyphens for spaces, no timestamp.

Examples:
- Claude lane on `mnz-creative-original.webflow.zip` → `output/claude_mnz-creative-file_output.zip`
- Codex lane on `srta-colombia-webflow.zip` → `output/codex_srta-colombia-file_output.zip`

Do NOT create `output/fresh-runs/`, timestamped `current-skill-*` names, `rerun` names, backup ZIPs, comparison ZIPs, or alternate output folders. If Maria asks to convert the same lane/source again, replace the same ZIP and folder. If the output is wrong, update the skill and re-run — never hand-patch the generated output (produces Franken-artifacts).

**L-18 — ZIP root and asset preservation:**
- Strip exactly ONE common top-level folder prefix if AND ONLY IF every source-ZIP entry shares it.
- Every file NOT mutated by pre-treatment is copied byte-for-byte.
- Every local asset reference in processed HTML/CSS resolves against the output root after prefix stripping.
- If a raw source local reference is already broken, repair it only when there is exactly one same-directory deterministic candidate after URL-decoding, Unicode normalization, case-folding, and punctuation/separator equivalence. Record the original ref, repaired ref, and evidence in the manifest. If there is no unique candidate, preserve the source ref, label it source-premise broken, and HALT/HOLD instead of inventing a filename.
- No synthetic folders invented by the skill. Declared mutations only.

## Output Mode Contract

This skill has two output modes because it serves two different consumers. `local-preview` keeps source runtime behavior available for browser inspection. `webflow-paste` prepares HTML for a converter that reads static DOM/CSS evidence and does not execute the source runtime, so it must transport paste-critical initial states and suppress runtime-only engine dependencies that would be invisible or unsafe after paste.

Every run declares exactly one of `local-preview` or `webflow-paste`. No silent default.

- **`local-preview`** — preserves source Webflow runtime evidence for local browser verification. One late `fb-runtime.w-embed` with external `js/webflow.js`. IX2 inline start states preserved per L-8. SV-13-A and SV-13-B apply. Not valid input for the current minimal converter.
- **`webflow-paste`** — explicit paste target for the current converter path. Source-runtime-preserved (preserve `js/webflow.js` reference, source scripts, `data-w-id`, IX-shaped source `style=""`). Do NOT convert IX2 to IX3. Extract IX DATA (not engine) from source `js/webflow.js` and inline the `Webflow.require("ix2").init(...)` / `.register([...])` calls as a dedicated `<script>` inside `fb-scripts.w-embed` per L-30. Emit optional converter-readable IX3 naming suggestions in `flowbridge-ix3-name-hints.json` per L-33. An artifact dropping source runtime/IX evidence is a hard FAIL.

## Mandatory Output Manifest — Before You Zip (L-21)

Before zipping, produce `MANIFEST.md` with one row per artifact-touching L-rule. Each row carries L-rule ID + one-line body, PASS/FAIL/WARN/N-A status, Evidence (file path + line, or command + captured output), and anticipated Origin label if FAIL (S/C/W/E).

**If ANY row is FAIL, write `HALT-REPORT.md` and do not zip.** L-21 is a meta-rule enforcing structural attestation; a missing row is treated as FAIL. `scripts/lesson_surface_lint.py` validates this inventory against `references/lessons.md` and `references/verification-gate.md` at authoring time. See `templates/HALT-REPORT-TEMPLATE.md` for the HALT report format.

**Manifest row inventory (current L-rule set):**

| L-rule | Property | Example check command |
|--------|----------|------------------------|
| L-1.1 | Site CSS file deleted from output | `ls output/{runner}_{source-slug}-file_output/css/*.webflow.css 2>/dev/null \| wc -l` → expect 0 |
| L-1.2 | HEAD has exactly one `<style>` block carrying inlined site CSS | python parse `<head>`, count `<style>` elements, assert == 1 |
| L-1.3 | HEAD has zero `<link>` to the site CSS file `css/[sitename].webflow.css`; framework `<link>` to `css/normalize.css` and `css/webflow.css` MAY remain (preview-only — does not satisfy L-4; see L-4 manifest row) | grep `<head>` for `<link.*css/.*\.webflow\.css` → expect 0 |
| L-1.4 | No upward-relative CSS URLs after inlining | `grep -cE "url\(['\"]?\.\./" output/{runner}_{source-slug}-file_output/index.html` → expect 0 |
| L-1.5 | `@font-face` is absent from converter-visible `fb-styles-site` in every mode | `python3 scripts/paste_contract_probe.py --source-root <raw export> --output-root output/{runner}_{source-slug}-file_output --mode <local-preview\|webflow-paste> --write-manifest --fail-on-contract` → `contractChecks[].id == "<mode>-font-face-absence-in-fb-styles-site"` must PASS with count 0. Any nonzero count is a pre-zip HALT under L-24. |
| L-1.6 | Converter-visible `fb-styles-site` carries source site class CSS (base selectors only) in every mode | same script as L-1.5 → `contractChecks[].id == "<mode>-site-css-carried"` must PASS: source non-baseline site class selector set — **EXCLUDING selectors that appear in the source site CSS exclusively inside `@media` blocks** — minus `fb-styles-site` selector set is empty. `@media`-trapped selectors (e.g. `heading-slider`, `hide-mobile`, `hide-tablet` in MNZ) are correctly routed to `fb-media-site` per L-2 and MUST NOT fail L-1.6; this was a false FAIL surfaced in EXP-001 and resolved here. The check measures whether BASE (non-responsive) styles travel to `fb-styles-site`, not whether responsive overrides are duplicated. |
| L-2 | Native @media blocks preserved verbatim | count @media blocks in HEAD `<style>` vs source CSS, assert equal |
| L-2.1 | Fluid-typography cascade atomic in `fb-media-site` | parse `fb-media-site` `<style>`, assert unconditional root font-size rule is first, followed by `@media` overrides in source order (SV-3) |
| L-4 | Webflow baseline + native component CSS present in `fb-styles-site` | parse `fb-styles-site` `<style>` and assert `html { height: 100% }`, universal `box-sizing: border-box`, `body { margin: 0 }`, `body { min-height: 100% }`. Any missing geometry property = FAIL. Retained HEAD `<link>` to `css/normalize.css`/`css/webflow.css` do NOT satisfy the check. If source DOM contains Webflow Tabs, assert `.w-tab-content`, `.w-tab-pane { display: none }`, `.w--tab-active { display: block }` in `fb-styles-site`. |
| L-5 | Lazy video source behavior is explicit per mode | `python3 scripts/paste_contract_probe.py --mode <local-preview\|webflow-paste> --write-manifest --fail-on-contract` → `contractChecks[].id == "<mode>-lazy-video-idempotence"` must PASS. |
| L-7 | Universal overlay neutralization — no fixture-specific class names | `python3 scripts/paste_contract_probe.py ... --mode <local-preview\|webflow-paste>` → `contractChecks[].id == "<mode>-overlay-neutralization-scope"` must PASS. The probe enumerates every non-framework class appearing in source DOM (`class="..."` attributes, excluding `w-*` and `fb-*` prefixes), then scans every output style host (`fb-styles-site` + each `fb-styles-{library}`) for top-level rules of the form `.{source-class}[.class...] { display: none | visibility: hidden | height: 0* | opacity: 0 }`. Any match is FAIL. Secondary check: any source element with ≥ 2 non-framework classes AND a `data-w-id` attribute AND an inline `style` containing `!important` collapse properties (or `pointer-events: none`) is also FAIL. Zero global class-based collapse CSS + zero combo inline collapses on IX2 targets. This rule fires on ANY class name — `.bg-whipe`, `.page-curtain`, `.loader`, `.hero-overlay`, whatever the source uses. |
| L-8 | IX2 initial-state source evidence preserved | Parse for `data-w-id` elements; assert source inline-state attributes remain unless a named hard-stop exception is documented. In `webflow-paste`, require `mode-b-inline-ix-preserved` PASS: source and output IX-shaped inline style counts match, `data-w-id` counts match. This is not a substitute for L-31: paste-critical first-frame states still need converter-visible Mode B transport/fallback CSS when L-31 detects required targets. |
| L-9 | Source-shipped runtime libraries preserved (not stripped) | enumerate GSAP-family `<script src>` in raw source HTML, count N; enumerate in output `fb-scripts.w-embed`, count M; assert M ≥ N. Any shortfall must be matched row-for-row by a named HALT-REPORT.md incompatibility entry. |
| L-11 | Single-root `fb-page-wrapper` (body has exactly one element child) | parse `<body>`, assert exactly 1 element child whose class list contains `fb-page-wrapper` |
| L-12 | All embed hosts inside first `fb-custom-code` (with L-15A carve-out for fb-runtime) | parsed-DOM enumeration of embed hosts, assert all inside `fb-custom-code` EXCEPT `fb-runtime` (sibling of source content per L-15A) |
| L-13 | Multi-root content siblings preserved in source order under `fb-page-wrapper` (applies to processed HTML only; L-27 CMS template stubs are excluded) | parse `fb-page-wrapper` direct children, assert source-content siblings appear in source order between `fb-custom-code` FIRST and optional `fb-runtime` LAST; skip files classified as CMS template stub per L-27. |
| L-14 | INFORMATIONAL — source-origin `@font-face` duplicates pass through verbatim | source-origin duplicates are NOT skill-introduced; SV-6 α classifies them as pass-through. No check command — this row exists so SV-7 sees the rule is acknowledged. |
| L-15 | Source HEAD + body CDN libraries and inline init/defer bodies emitted in `fb-scripts.w-embed` | parsed-DOM enumeration of source `<script>` elements from HEAD and body vs output; assert every preserved CDN or inline body fingerprint appears in `fb-scripts` in source order. In `webflow-paste`, this includes the original `js/webflow.js` reference; do not inline it. |
| L-16 | Retained inline inits/custom-code source body preservation + dep-gate wrapping | parse each inline executable `<script>` in `fb-scripts` and assert TWO properties: (a) source body fingerprint is preserved verbatim INSIDE `fbRun` — no rewrite, no paraphrase of source executable code; (b) the outer dep-gate wrapper (`need[]` → `fbReady` → `fbRun`) is present whenever the body touches runtime globals (`Webflow.env`, `Webflow.push`, `Webflow.require`, `jQuery`, `gsap`, `$`) or source DOM selectors. "Do not wrap" is about the SOURCE BODY CONTENT — the wrapper STRUCTURE is always required when L-16 globals/selectors are detected. A bare `Webflow.*` call at top-level in fb-scripts without the dep-gate is FAIL (caught by `paste_contract_probe.py` rows `webflow-paste-webflow-global-readiness` and `mode-b-l16-readiness`). Applies in BOTH modes. |
| L-17 | Each detected library has a complete `fb-styles-{slug}` host: migrated/inferred core CSS payload/link, zero HEAD residue, core markers, and strict runtime-independent Designer fallback | enumerate detected libraries (CDN script + body root class); assert matching host contains fetched CSS payload or moved source `<link>`; assert core CSS markers, zero library-owned `<link>/<style>` in HEAD, fallback selectors carry BOTH `visibility: visible !important` and `opacity: 1 !important` on library root + ≥1 source-present inner class. In `webflow-paste`, `contractChecks[].id == "mode-b-static-visible-fallbacks"` must PASS. |
| L-18 | All source assets preserved in output ZIP and local refs reconciled | diff source ZIP file list vs output dir file list and final ZIP file list, assert no missing assets (excluding intentional CSS deletion per L-1), byte-compare non-mutated files, parse local asset refs in processed HTML/CSS, assert zero skill-introduced broken refs. This includes `images/`, `fonts/`, `js/`, `documents/`, and media folders. |
| L-19 | webflow.js external ref only (no inline IIFE) | grep for inline Webflow module-IIFE signature → expect 0; in both modes assert the source external `<script src="js/webflow.js">` reference count is preserved in the mode-approved host. |
| L-20 | Fixture Premise Verification Before Adding a New Skill Rule | INFORMATIONAL meta-rule about rule-authoring process, not artifact properties. Mark as `INFORMATIONAL` in manifest; no runtime check command. Row exists so SV-7 sees the L-rule is acknowledged. |
| L-21 | Manifest contract self-check | this row asserts the manifest itself is complete: every documented ARTIFACT-TOUCHING L-rule has a row above, every informational/superseded rule is accounted for below, and `pretreat-manifest.json` exists with `schema`, `outputMode`, `animationClaim`, `probesRun`, zero FAIL `contractChecks[]`. |
| L-22 | Wrapper impact boundary + component-local media/hover fidelity | `python3 scripts/component_fidelity_probe.py --source-root <raw export> --output-root output/{runner}_{source-slug}-file_output` → exit 0 and report `missingCount=0` + `addedCount=0` after ignoring inserted `fb-*` hosts. Any uncited delta FAILs. |
| L-23 | Responsive-unit / viewport-runtime boundary | parse source site CSS plus output `fb-styles-site` / `fb-media-site`; assert root font-size cascades are present in L-2.1-approved location with no later cascade inversion, assert no synthetic body typography/color when source typography exists, assert source viewport units (`100vh`, `100dvh`) not rewritten unless declared. |
| L-24 | Webflow Designer crash-hazard pre-paste blacklist | reuse SV-1/L-1 evidence to assert zero `@font-face` in body embeds; grep style hosts for `animation-play-state` → expect 0. Converter-side: before direct copy, run `python3 scripts/converter_invariant_probe.py <xscpdata.json>` (repo-root script if present) and require `designer-crash-hazards` and `static-image-asset-binding` invariants PASS. |
| L-25 | AUTHORING — scoped interaction fix discipline | INFORMATIONAL anti-lesson. No runtime check; enforcement is via Regression Report block in session result files and the anti-lesson warning at the top of `references/lessons.md`. |
| L-27 | CMS template stubs (body has zero content-bearing elements and at least one `<script>` child) passed through byte-for-byte; NOT pre-treated; NOT subject to L-11/L-12/L-13/L-15/L-15A/L-16/L-17/L-4/L-1/L-2/L-2.1 gating | for each source HTML file: parse `<body>`, count children that are tags AND NOT in `{script, style, link, meta, title}`; count `<script>` children; if content-element count == 0 AND script-child count > 0, assert output file at same relative path is byte-identical to source AND `pretreat-manifest.json` records it under `passthroughClassification.l27Stubs`; assert no `fb-page-wrapper` was injected. |
| L-28 | Anchors inside `w-dyn-item` carry `data-fb-link-role="template-page"` + L-6 idempotence marker; no anchor outside that ancestor scope carries the role | parsed-DOM enumeration: for each `<a>` whose `find_parent(class_="w-dyn-item")` is not None AND whose `href` is not absolute / scheme-special / fragment-id, assert `data-fb-link-role == "template-page"` AND `data-flowbridge-link-role-tagged == "true"`. Second assertion (counter-rule): for each `<a>` with no `w-dyn-item` ancestor, assert `data-fb-link-role` is absent. |
| L-30 | IX runtime DATA (not engine) extracted from `js/webflow.js` and inlined as `<script>` inside `fb-scripts.w-embed` so converter HTML-only IX extractors can see IX2 and/or IX3 payloads (`webflow-paste` only; `local-preview` suppresses) | **Mode gate:** in `local-preview`, assert zero inline IX data script. **Mode B:** enumerate source `js/webflow.js` call counts `S_init`, `S_reg`, `S_tl`; enumerate output `index.html` inline counts `O_init`, `O_reg`, `O_tl`; assert `O_* >= S_*`. Assert inline IX-data `<script>` is child of `fb-scripts.w-embed` AFTER `<script src="js/webflow.js">`. L-19 engine-absence guard: `grep -cE 'var e=\{[0-9]+:' index.html` → 0. |
| L-31 | Mode-B class-specific CSS fallback for IX2-hidden initial states (`webflow-paste` only). Runtime-gated `html:not(.w-mod-ix2) <target.selector>` rules emitted in `fb-styles-site` (or in `fb-styles-{library}` when the target carries a `component_fallback_host` annotation) for every target detected by `paste_contract_probe.detect_mode_b_targets`. Idempotent per `(selector, required)` pair. No `!important`; specificity wins via the runtime-gate prefix; IX2 runtime overrides remain free to take effect once `.w-mod-ix2` lands on `<html>`. | `python3 scripts/paste_contract_probe.py --source-root <raw export> --output-root output/{runner}_{source-slug}-file_output --mode webflow-paste --write-manifest --fail-on-contract` → assert `contractChecks[].id == "mode-b-initial-state-transport"` PASS with zero `missing` targets; assert `contractChecks[].id == "mode-b-d007-anchor-safety"` PASS; cross-check `contractChecks[].id == "webflow-paste-overlay-neutralization-scope"` STAYS PASS with `skill-injected=0` (L-7 anti-broaden held); anti-regression `contractChecks[].id == "mode-b-inline-ix-preserved"` STAYS PASS (L-8 preservation floor unchanged). Mode gate: in `local-preview`, assert zero L-31 rules emitted (the local Webflow runtime executes IX2 natively and would race a static fallback). |
| L-33 | IX3 human-readable name hints emitted as output-root `flowbridge-ix3-name-hints.json` for the converter to consume mechanically (`webflow-paste` only). The file is advisory: it maps preserved IX3 IDs to suggested names by page path, never changes source IX data or any binding ID. | In `webflow-paste`, parse `output/{runner}_{source-slug}-file_output/flowbridge-ix3-name-hints.json` and assert `schema == "flowbridge/ix3-name-hints"`, `version == 1`, and every key under `pages.*.interactions` / `pages.*.actions` also appears as an IX3 interaction/action ID in source `js/webflow.js` or the L-30 inline IX data. Assert every suggested name is a non-empty string ≤80 chars and contains no control/path-forbidden chars. In `local-preview`, assert the file is absent. |
| L-34 | Visible text / glyph fidelity — all body text nodes, `<title>`, `<meta>` description/og/twitter content, and source-content attributes (alt/title/placeholder/aria-label/data-* except data-w-* and data-flowbridge-*) must be preserved byte-for-byte after whitespace normalization. | `python scripts/content_fidelity_probe.py --source-root <raw-zip> --output-root output/{runner}_{source-slug}-file_output --fail-on-contract --write-manifest` → exit 0; assert manifest row `content-fidelity-text-glyph` status=`pass`; zero `changedSamples`, zero `missingFromOutput`, zero `addedInOutput`. |

**Informational / superseded L-rules (acknowledged; no dedicated check row required):**

- **L-6 (`data-flowbridge-inline-*` idempotence markers)** — soft rerun-protection invariant; a failure here implies the upstream rule (L-5, L-7) already failed. No dedicated row.
- **L-15A (webflow.js runtime placement)** — covered implicitly by L-15 and L-19 rows; no separate check command needed.
- **L-32 (`data-flowbridge-*` namespace convention)** — AUTHORING-PROCESS rule for rule-authors; codifies the data-attribute namespace already practiced across L-5/L-6/L-28/L-30/L-31. No runtime check command — compliance verified at PR/commit time when adding new rules. See `references/lessons.md` L-32 for full body.

Absence of a row for these rules is explicit and intentional — not aspirational. SV-7's Extension (see `references/verification-gate.md`) treats them as acknowledged via this list.

Excluded rules (L-3, L-10, L-26, L-29) live only in the Excluded Rules appendix of `references/lessons.md`; they do NOT fire manifest rows or gates in this skill.

## Auto-Research Loop

This skill grows by running experiments. The loop:

1. **Declare.** Invoking prompt declares the 7 Before You Run fields + Protected Set.
2. **Run.** Skill executes the Workflow. Every decision cites an L-rule or flags a new failure mode.
3. **Attest.** Mandatory Output Manifest + `pretreat-manifest.json` + HALT report if any gate FAILs.
4. **Compare.** Protected Set is re-checked after the run. Any flip from PASS → FAIL is a regression.
5. **Promote.** New failure mode → a new L-rule in `references/lessons.md` with origin label + verification gate ID + manifest row. The `lesson_surface_lint.py` script verifies the new rule is consistent across all three surfaces (lessons, gates, manifest) before the next run.
6. **Log.** Every run appends `experiments/EXP-NNN.md` with the full Before You Run declaration, verdict, Protected Set diff, and any new L-rule.

See `experiments/README.md` for the log contract and `templates/EXPERIMENT-TEMPLATE.md` for the declaration format.

## Non-Negotiables

- Input is exactly one raw `.zip`. Never start from `output/*-file_output/` or loose extracted files.
- Use a temporary working folder outside `output/`. Never mutate the source ZIP.
- Do not resurrect the archived mechanical TS path. This skill is AI-driven reasoning, not rule-based transformation.
- Do not add fixture-specific logic. Every rule must be universal. Fixtures are stress tests, not product-specific targets.
- Preserve source-shipped libraries and inline init bodies per L-9.
- Preserve L-1.5 font crash safety: `@font-face` only in the pretreated HEAD inline style. `fb-styles-site` and every other body embed must contain zero `@font-face`.
- Preserve L-7 overlay scoping: never emit global `.bg-whipe` collapse CSS and never neutralize `.bg-whipe` combo elements. This is an anti-lesson — re-broadening re-ships the MNZ regression.
- Preserve L-8 IX2 inline state preservation: never blanket-strip IX2 initial states. This is an anti-lesson.
- Preserve L-15 source script inventory and order.
- For converter paste runs, always declare `webflow-paste`. Never silently fall back to `local-preview`.
- Keep XscpData `payload.assets[]` empty. This is a clipboard/direct-copy crash guard; pre-treatment still preserves source asset files in the ZIP/folder under L-18.
- HALT is a packaging stop, not a soft warning. If any mandatory row fails, leave only the extracted diagnostic folder plus `HALT-REPORT.md`. Do not create a ZIP just to satisfy an output path.

## Skill Contradiction Protocol

If rules in this SKILL.md or its references conflict with each other, **STOP**. Do not invent a resolution by hand-patching output. Write `experiments/EXP-DRAFT-skill-contradiction.md` citing the two conflicting rules, and hand back. Resolution happens in the skill itself — commit the fix, then re-run.

## Paths

The skill is **host-project-agnostic**. It runs wherever it is installed. No hardcoded reference to any specific project directory lives inside the skill.

- **Skill root:** wherever this SKILL.md lives. Scripts compute it as `Path(__file__).parents[1]` at runtime.
- **Host project root:** wherever the invoking prompt places `fixtures/`, `output/`, and (optionally) `docs/`. The skill never assumes the project root is `Flowbridge-claude` or any other name.
- **Input ZIP:** absolute path provided by the invoking prompt.
- **Output:** `{host-project-root}\output\{runner}_{source-slug}-file_output.zip` + matching extracted folder. The invoking prompt is responsible for resolving `{host-project-root}`. The skill writes relative to that.
- **Working folder:** temporary, created outside `output/`, deleted after the run.

**Training grounds vs shippable skill** — see MEMORY.md for which folders ship with the skill vs stay in the lab. Short version: `SKILL.md + references/ + scripts/ + templates/` ship. `evals/` and `experiments/` are training artifacts that stay where training happens.
