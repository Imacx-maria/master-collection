# EXP-NNN — {short experiment name}

**Date:** YYYY-MM-DD
**Runner:** claude | codex
**Fixture:** {fixture-slug}
**Source ZIP:** `{absolute path to raw .webflow.zip}`

## Before You Run declaration (required — skill HALTs if any field missing)

### 1. Hypothesis
A falsifiable statement about what the skill should produce on this fixture. Example:
> After L-28 CMS-template-page anchor tagging is applied to every `<a>` inside `w-dyn-item`, the output `pretreat-manifest.json` will show `L-28-check: PASS` with N anchors tagged and zero false positives outside the ancestor scope.

### 2. Metric
Pass/fail criteria referencing SV-1..SV-18 (and SV-P1..SV-P6 if paste-side is in scope). Declare the expected origin label for any anticipated failure:
- `S-origin` — skill output wrong
- `C-origin` — converter defect
- `W-origin` — Webflow paste/publish mutation
- `E-origin` — environment/tooling

Example:
> PASS criteria: SV-18 PASS, Manifest row `L-28-check` PASS, `pretreat-manifest.json` reports anchor count ≥ 1.
> Anticipated failure origin if FAIL: `S-origin` (skill logic bug).

### 3. Scope
Which L-rules, embed hosts, and files are in-bounds. Everything else stays unchanged. Example:
> In bounds: L-28, per-element transformation pass for every non-stub HTML file.
> Out of bounds: L-1..L-27, L-30, all wrapper structure, all script handling, all CSS routing.

### 4. One change
Exactly one of:
- `skill-applied-to-new-fixture` — running existing skill on a new export
- `specific-skill-update` — testing a named rule change
- `read-only-diagnostic` — inspecting output without mutating

### 5. Keep/discard criteria
Pre-declared action for PASS, FAIL, PARTIAL outcomes. Example:
> PASS → accept, update EXP log as KEEP.
> FAIL → no skill update from this experiment; file a separate fix experiment with narrower scope.
> PARTIAL → isolate the failing anchor subset, open an L-rule refinement draft in iteration 2 before re-running.

### 6. Output mode
Exactly one of `local-preview` or `webflow-paste`, plus why:
> `webflow-paste` — downstream task is the minimal converter + Webflow Designer paste verification.

### 7. Runner
`claude` or `codex`. Determines output prefix + default tooling.

## Baseline Capture Gate (required for any fixture-affecting change)

### Protected Set
List every current-state PASS that must stay PASS after this experiment. Example:
- Manifest rows L-1-check..L-27-check: all PASS (from previous EXP-NNN run)
- SV-1..SV-17: all PASS
- Paste parity anchors: `fb-page-wrapper` single root, `@font-face` count in HEAD = 10, Mode B IX data script present with SHA256 {hash}

### Regression Report (filled after the run)
Before → After diff. Any PASS → FAIL flip is a regression and blocks KEEP.

## Verdict (filled after the run)

- **Outcome:** PASS | FAIL | PARTIAL | HALT
- **Manifest rows:** {paste counts}
- **Evidence:** {paths to output ZIP, manifest, HALT report if any}
- **New lesson?** If a new failure mode was promoted to an L-rule, record it here with ID, origin label, gate, and manifest row. Then update `references/lessons.md` and re-run `scripts/lesson_surface_lint.py`.
- **Decision:** KEEP | DISCARD | REQUIRES-REFINEMENT

## Notes
Free-form. What was learned. What surprised. What's the next experiment.
