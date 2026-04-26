# Lessons — webflow-pretreat

**Iteration 2 curated lesson corpus.** This file inlines 26 of 30 canonical L-rules from `docs/LESSONS.md`. The 4 excluded rules are listed at the bottom under "Excluded Rules" with the reason for exclusion. When adding a new L-rule discovered in an experiment, append it here AND update the matching gate entry in `verification-gate.md` AND register the manifest row in `SKILL.md`. Then run `scripts/lesson_surface_lint.py` — it MUST pass before the next run.

**Anti-lessons (MUST NEVER be re-broadened):**
- **L-7** — Overlay scoping. Never emit global `.bg-whipe` collapse CSS. Never neutralize `.bg-whipe` combo elements like `.bg-whipe.bg-grey`. Scope per-element only.
- **L-8** — IX2 initial-state inline styles. Never blanket-strip. Preserve by default; transport critical initial states via `fb-styles-site` keyed by stable selectors.
- **L-25** — Scoped-interaction fix discipline. Never re-broaden scoped fixes to wide rules.

---

## L-1 — @font-face Preservation, Option B: Opaque-Blob Inlining + Single Source of Truth (KEEP; policy locked 2026-04-17)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Webflow exports ship the site CSS as `css/[sitename].webflow.css`, linked from HEAD via `<link rel="stylesheet">`. That CSS file contains `@font-face` declarations for every variant the site uses (often variant-named families like `"Ppmori Extra Bold"` with their own `font-weight`), alongside `:root` variables, tag selectors, class rules, `@keyframes`, and Webflow-native `@media` breakpoints. The pre-treated HTML needs a faithful preview render (for visual verification before paste) AND needs the converter to see class rules (which the converter extracts from body `<style>` embeds, NOT from HEAD). Webflow's paste pipeline consumes only the converter-produced clipboard JSON; it never reads the pre-treated HTML's HEAD.

**Rule — Option B, locked 2026-04-17:**

1. **Preserve every `@font-face` block verbatim** — no canonicalization, no family-name rewrites, no weight rewrites. Source bytes win.
2. **Inline the full site CSS into HEAD as a single `<style>` block.** Opaque-blob inlining — whatever is in `css/[sitename].webflow.css` goes into HEAD inline `<style>`. No content-aware filtering, no selective extraction, no branching on rule type.
3. **Remove the `<link>` to the site CSS from HEAD AND delete `css/[sitename].webflow.css` from the output ZIP.** Single source of truth. No disk copy to drift against. No `<link>` to create a second render path.
4. **Rewrite relative `url()` paths** in the inlined CSS (`../images/` → `images/`, `../fonts/` → `fonts/`) since the inlined CSS is now relative to `index.html` instead of `css/`. Verify with SV-14: no processed HTML may contain `url('../...')`, `url("../...")`, or `url(../...)`.
5. **`@font-face` must NEVER appear inside a `w-embed` `<style>` block** — Hard Rule #2 of SKILL.md. It crashes Webflow Designer at paste time. `@font-face`'s only valid location in the pre-treated output is the HEAD inline `<style>`.
6. **Class rules / `:root` / `@keyframes` that the converter needs** are additionally extracted into the body-level `fb-styles-site w-embed` block in every output mode, including `webflow-paste`. This is duplication between HEAD inline (preview-only) and `fb-styles-site` (converter-piped) — expected, and harmless because the two serve different consumers. Complete `@font-face` at-rules must be filtered out before `fb-styles-site` is written; immediately after the host is assembled, the L-1.5 fast-fail probe must confirm `<mode>-font-face-absence-in-fb-styles-site` PASS before any later manifest or ZIP work. Audit 154 made this a hard Mode B contract: a paste artifact that renders locally only because site class CSS is HEAD-only is not paste-shaped and must fail before conversion.

**Why this replaces the old mechanical canonicalization:** The prior mechanical TS runner stripped `@font-face` before inlining and then partially rewrote `font-family` / `font-weight` at usage sites (e.g. `"Ppmori Extra Bold"` → `"Ppmori"` + `font-weight: 800`). That produced two simultaneous failure modes: (1) the browser had no `@font-face` to register — every font fell back to system defaults, causing visible layout breaks on MNZ (RECENT POST wrapping, heavier menu text); (2) rewrites landed inconsistently — linked file got weight 800 while the `fb-styles-site` embed kept weight 700, causing M-2 divergence. The retired weight-preservation constraint was an attempt to patch failure mode (2) without addressing (1). Option B sidesteps both by touching nothing inside `@font-face` and by removing the linked file so no second source of truth can exist.

**Why opaque-blob inlining (vs. "inline only `@font-face`"):** A rule that treats the site CSS as an opaque blob generalizes across arbitrary Webflow exports — every one of them ships `css/[sitename].webflow.css` as a single file, and the rule works identically no matter what's inside (nested `@media`, `@supports`, `@container`, `@scope`, `unicode-range` variants, interleaved comments, whatever). A content-aware rule ("extract only `@font-face`") requires the skill to parse CSS structure and branch on rule shapes — and every branch is a place the skill can get it wrong on a site it hasn't seen. MNZ is a stress test, not the target. The skill must work on any export.

**Why drop the `<link>` (vs. keep it for "belt and suspenders"):** The browser dedupes `@font-face` internally by `src` URL, so having the declarations in both HEAD inline and a linked file provides zero additional safety. It only creates a place where the two can drift. Deleting the link + deleting the file removes the drift surface entirely.

**Reference implementations:**
- Skill-authored rule: `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` L-1 (canonical, Option B, lock date 2026-04-17).
- Historical mechanical implementation (retired reference only): `src/pre-treatment/css-transforms.ts` font canonicalization subsystem. Do NOT resurrect.

**Evidence of why canonicalization was retired:**
- Canonicalization failure analysis: `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-16/043-audit-fresh-mnz-three-way-parity.md` "Typography Drift" section.
- Option A → Option B pivot (SV-5 contradiction + scope decision): `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-17/052-skill-bug-exp-003-sv5-vs-l1-head-policy.md`.

---

## L-2 — Non-Canonical @media Routing (KEEP)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Webflow has 6 native responsive breakpoints: `max-width: 479px`, `max-width: 767px`, `max-width: 991px`, `min-width: 1280px`, `min-width: 1440px`, `min-width: 1920px`. Rules at these exact widths are "canonical" and live in site CSS. Rules at any other breakpoint are "non-canonical" and need a different destination.

**Rule:** Partition `@media` rules during pre-treatment:
- Canonical-breakpoint rules stay in the inlined `fb-styles-site w-embed` host.
- Non-canonical rules move to a separate `fb-media-site w-embed` host, nested inside `fb-custom-code` per L-12 (the single hidden container for all pre-treatment-injected embeds).

**Why:** Webflow Designer will not apply arbitrary breakpoint rules to pasted content the way it applies canonical-breakpoint rules. Routing them to a separate embed host preserves them without polluting the canonical pipeline.

**Reference implementation:** `src/pre-treatment/css-transforms.ts` (@media partitioning subsystem).

**L-2.1 — Atomic fluid-typography cascade (sub-rule of L-2):** Whenever a source `<style>` block contains an unconditional rule targeting a root-level selector (`html`, `:root`, or `body`) for a cascade-sensitive property (`font-size`, `font-family`, `color`), AND one or more `@media` rules in the SAME source block override that exact selector+property pair, treat the whole set as a single fluid-typography cascade. Emit the entire cascade into `fb-media-site` as a contiguous run at the TOP of its `<style>` block, preserving original source order (unconditional rule first, `@media` rules after). Do NOT leave the unconditional rule in any other embed. This prevents CSS cascade inversion from DOM-separated `w-embed` blocks — the root cause of P-1 (MNZ fluid typography broken, 046-result).

---

## L-4 — Webflow Baseline + Native Component CSS Surface (KEEP; promoted 2026-04-19, extended 2026-04-20)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Webflow exports rely on `normalize.css` and `webflow.css` for baseline geometry, tag behavior, and native Webflow component state CSS. The pre-treatment skill intentionally treats these files as Webflow baselines rather than the site-specific CSS blob governed by L-1. However, converted local preview and the body-embed paste path do not get those baseline links for free. If the skill removes or ignores them without recreating the needed surface, browser defaults and missing native state rules leak in: `body` margin becomes `8px`, paragraph top margins reappear, full-bleed content starts at `x=8/y=8`, width calculations lose Webflow's border-box baseline, and native widgets drift. MNZ L-5c rerun exposed both finer classes: omitting Webflow tabs base CSS meant `.w-tab-pane { display: none; }` / `.w--tab-active { display: block; }` were absent, and omitting Webflow's paragraph top-margin reset meant source `p { margin-bottom: 0; }` still inherited browser default `margin-top: 1em`, adding exactly 38/35/44px of page-height drift.

**Rule:** Inject the minimum Webflow baseline floor into `fb-styles-site`, before extracted site tag/class rules:

```css
html { height: 100%; }
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; min-height: 100%; }
a { color: inherit; text-decoration: inherit; }
img { max-width: 100%; vertical-align: middle; display: inline-block; }
p { margin-top: 0; }
```

Geometry resets (`html`, global `box-sizing`, `body` margin/min-height) are unconditional. The `a`, `img`, and `p` resets may be omitted only when an equivalent or stronger source site rule already exists. For paragraphs, `margin-bottom` may remain source-owned, but `margin-top: 0` must be supplied when the source does not explicitly set it.

**Native component extension (L-4 native surface):** If the source DOM contains Webflow-native component classes whose behavior depends on `css/webflow.css` state rules, copy the required native component rules into `fb-styles-site` as well. This is source-aware extraction, not a full-file dump. At minimum:

- If source contains `.w-tabs`, `.w-tab-content`, `.w-tab-pane`, or `.w--tab-active`, `fb-styles-site` must include the Webflow tabs base rules:
  - `.w-tab-content { position: relative; display: block; overflow: hidden; }`
  - `.w-tab-pane { position: relative; display: none; }`
  - `.w--tab-active { display: block; }`
- Apply the same principle for future native components (`w-slider`, `w-dropdown`, `w-nav`, `w-lightbox`, `w-dyn-*`, etc.): extract the Webflow base rules required for the source's present native state classes so local preview and paste-visible CSS do not rely on vanished HEAD links.

Do NOT dump full `normalize.css` or full `webflow.css` blindly; do NOT inject Webflow's default typography/color values (`font-family: Arial`, `font-size: 14px`, `line-height: 20px`, `color: #333`) unless a separate fixture proves the source lacks its own text rules. The correct move is a required native-component subset based on classes actually present in the source DOM. If the source site already defines `html`, `body`, paragraph, heading, or text-class typography, any added Webflow default body typography rule is a regression even when it loses in the cascade; it creates inheritance surprises for unclassed text and masks the real root cause in font-size audits.

**Manifest row:** L-4 carries a runnable parsed-CSS check against `fb-styles-site`: confirm the baseline floor exists or is explicitly source-overridden where allowed, and confirm source-present native component base rules exist. Missing geometry resets are a hard FAIL. Missing paragraph `margin-top: 0` when the source contains `<p>` elements and does not set it itself is a hard FAIL. Missing `.w-tab-pane { display: none; }` / `.w--tab-active { display: block; }` when the source contains Webflow tabs is a hard FAIL.

**Failure mode this prevents:** Codex BigBuns and Srta Colombia comparison outputs both booted without critical runtime errors but had full-bleed geometry drift because the baseline floor was absent: `body` retained browser default `8px` margin and Webflow nav sizing drifted without border-box. This is an S-origin skill-output problem, not a browser quirk.

**Evidence:** `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-19/116-audit-bigbuns-vs-codex-bigbuns-pretreated-index-root-pages-parity.md`; `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-19/116-audit-srta-colombia-vs-codex-skill-output-index-root-pages-parity.md`; historical seed `AI_OS/AI_DECISION_LOG.md` Decision 7.

---

## L-5 — Lazy Video De-Lazification (KEEP; split into L-5a, L-5b, and L-5c)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

The L-5 label covers three related but distinct operations. Keep the L-5 anchor to avoid renumbering; label the sub-cases:

### L-5a — Lazy Video `data-src` Copy (KEEP)

**Pattern:** Webflow exports use an IntersectionObserver lazy-loader script that copies `data-src` → `src` at runtime when the video scrolls into view. That script does not run in Webflow Designer, so `<video><source data-src="...">` elements show nothing because the browser never loads what has no `src`.

**Rule:** For every `<video><source>` with `data-src` attribute and no/empty `src`, copy `data-src` into `src` while preserving `data-src` (the published-site lazy loader still uses it at runtime). Do not overwrite an existing non-empty `src`.

**Generalization:** Applies to every Webflow export using lazy backgrounds or inline video — this is the mechanical pattern at `src/pre-treatment/core.ts:185-186, 710-734`.

**Mark touched elements** with a `data-flowbridge-inline-*` attribute for idempotence per L-6.

**Verification:** every `<source data-src>` inside a `<video>` has a non-empty `src` equal to `data-src`, and touched sources carry an idempotence marker. This is SV-15.

### L-5b — Lazy / Preload Attribute Strip on Autoplay Videos (KEEP)

**Pattern:** Webflow exports with autoplay backgrounds sometimes carry `loading="lazy"` or `preload="none"` on `<video>` elements. In a pasted context, the video never starts.

**Rule:** Strip `loading="lazy"` and `preload="none"` from `<video>` elements whose intent is autoplay (has `autoplay` attribute). Mark touched elements with a `data-flowbridge-inline-*` attribute for idempotence per L-6.

**Verification:** every autoplay `<video>` has zero `loading="lazy"` and zero `preload="none"` attributes after pre-treatment, and touched videos carry an idempotence marker. This is SV-15.

### L-5c — Retained Lazy-Loader Runtime Idempotence (KEEP; 2026-04-20)

**Pattern:** Some exports ship a runtime lazy-loader body that queries `video.lazy`, copies each child `source.dataset.src` into `source.src`, calls `video.load()`, removes the `lazy` class, and unobserves the video. After L-5a has already copied `data-src` into `src`, preserving that body verbatim can reload already de-lazified videos. In local browser audits this appears as repeated `Media net::ERR_ABORTED` cancellations even though the video eventually has a valid `currentSrc`.

**Rule:** When L-5a touches any `<source>` in a processed page, every retained lazy-video loader body for that page must be idempotent against `data-flowbridge-inline-video-src="true"` or existing `src === data-src`. It may keep the observer shape and may still load videos that were not de-lazified by L-5a, but it must not call video.load() for a video whose sources are already de-lazified. It should remove the `lazy` class from already-ready videos without forcing a reload.

**Verification:** SV-15 checks both the static source/src parity and the retained lazy-loader body. If any processed page has `data-flowbridge-inline-video-src="true"` markers and also retains executable code that targets `video.lazy`, the retained body must include an idempotence guard before any `video.load()` call. A page that passes static L-5a/L-5b but can still reload already-marked videos fails L-5.

**Relation to L-5a/L-5b:** L-5a addresses `<source>` children, L-5b addresses `<video>` attributes, and L-5c addresses the retained runtime script that would otherwise repeat L-5a at browser time. All three can apply to the same `<video>` element. None supersedes the others.

---

## L-6 — `data-flowbridge-inline-*` Idempotence Markers (KEEP)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** INFORMATIONAL

**Pattern:** Pre-treatment can be run more than once (rerun scenarios, partial fixes, etc.). Without markers, a second run re-applies transformations and corrupts the output.

**Rule:** Every element that pre-treatment touches (inline style injection, lazy strip, overlay neutralization) gets a `data-flowbridge-inline-<reason>` attribute. The runner checks the attribute before acting; if present, skip.

---

## L-7 — Static Overlay Neutralization (ANTI-LESSON, UNIVERSAL)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Mechanical bug (historical, MNZ Creative):** The TS runner injected a global CSS rule `.bg-whipe { height: 0% !important }` to neutralize static reveal overlays. On MNZ, `.bg-whipe` is also the BASE class of a color-combo chain (`.bg-whipe.bg-grey` = grey footer/menu background). The global rule collapsed six real footer/menu elements to zero height.

The MNZ spelling (`.bg-whipe`) was incidental. Other templates use `.page-curtain`, `.loader`, `.hero-overlay`, `.intro-curtain`, etc. The underlying anti-pattern is independent of class name. L-7 must fire on any source-DOM class, not a fixture-specific whitelist.

**Anti-pattern (universal):** emitting into any output style host (`fb-styles-site`, `fb-styles-{library}`) a CSS rule of the form

```css
.{any-source-class} { display: none | visibility: hidden | height: 0* | opacity: 0 }
```

where `{any-source-class}` is a class that appears in the source DOM and `.{any-source-class}` is a simple class-chain selector (no descendants, no attribute selectors, no pseudo-classes — those are more specific and out of scope for this anti-pattern).

**Why it's wrong regardless of class name:**
1. Any source class might be the base of a combo chain used elsewhere with a legitimate purpose (as `.bg-whipe` proved on MNZ: base for `.bg-whipe.bg-grey` menu/footer elements).
2. Any source class might be the target of a source IX2 animation that handles reveal natively — a global CSS collapse races with or overrides IX2 runtime.
3. Inline IX2 initial-state `style=""` attributes on source elements are sufficient (L-8); a layered global CSS collapse with `!important` wins the cascade and breaks the reveal.

**Rule:** do not emit global class-based collapse CSS on any source-DOM class. If an overlay element genuinely requires neutralization for wrapper-compensation reasons (rare), do it per-element:
- Identify the exact element (by position, parent, source order — NOT class).
- Verify its class chain in source DOM is solo (not a combo base) — enumerate source DOM.
- Verify it is NOT a `data-w-id` IX2 animation target.
- Apply `style="..."` inline on that element only.
- Record it in the Mandatory Output Manifest L-7 row with evidence of all three verifications.

**Default posture:** do not neutralize at all. Source IX2 runtime handles reveals.

**Secondary check:** do not emit inline collapse `style=""` attributes with `!important` or `pointer-events: none` on source elements whose class list contains ≥ 2 non-framework classes (combo chain) AND which are `data-w-id` IX2 targets. This catches the rarer pattern where the skill layers inline collapse on top of an IX2 subject's legitimate initial state. Source-origin IX2 starts without `!important` are exempt (covered by L-8 preservation).

**Evidence of the bug:** `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-16/041-result-mnz-html-css-fidelity-forensic-audit.md` — six collapsed `.bg-whipe.bg-grey` elements on the converted published site.

**Regression anchor:** six `.bg-whipe.bg-grey` elements on MNZ must survive with non-zero height. Universal equivalent: zero global class-based collapse rules targeting any source-DOM class in any output style host.

**Sync surface:** `SKILL.md` Mandatory Output Manifest L-7 row; `references/verification-gate.md` SV-3; `scripts/paste_contract_probe.py` `overlay_neutralization_scope_check` + `summarize_overlay_neutralization` (enumerates source-DOM classes class-agnostically).

---

## L-8 — IX2 Initial-State Stripping (ANTI-LESSON, NARROW)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Mechanical bug:** The TS runner stripped every inline style containing a vendor-prefix transform quadruple (`-webkit-transform:` + `-moz-transform:` + `-ms-transform:` + `transform:`) plus standalone `opacity: 0`. On MNZ this flattened 137 transforms and 9 opacities to zero — killing hero/loading page-load choreography on elements that are legitimately opacity:0 / transformed before their entrance animation runs.

**Narrow rule:** Preserve IX2 initial-state inline styles by default. Strip ONLY when ALL of the following hold:
1. The element is a nav/menu closed-state shell (`.navbar`, `.menu-wrapper`, `.hamburger-menu`, etc.).
2. It has NO runtime trigger that reopens it (no IX2/GSAP script flips its state).
3. Without stripping, it would permanently cover content or block editing.

**Bulk preservation floor:** AI output must retain ≥80% of the source's inline transform and opacity declarations. For MNZ: ≥110 of 137 transforms, ≥7 of 9 opacities.

**Mode B transport addendum (2026-04-20, Session 160; tightened 2026-04-21, Session 164 Loop 6):** `webflow-paste` mode cannot leave raw IX-shaped `style=""` attributes on source-content elements because the converter may serialize them as `node.data.xattr`. But deleting them without replacement is also wrong: Session 159 proved it opens MNZ's nav on first load and erases reveal starts. In Mode B, copy each required initial visual state into converter-visible CSS in `fb-styles-site`, keyed by a stable selector, before removing the raw inline style. Prefer a source-unique `data-flowbridge-ix-state="ixs-N"` marker when existing classes or `data-w-id` are not unique enough, but the final transport selector must be cascade-dominant against source class defaults. A lower-specificity marker rule can still lose to `.nav-child.left` or another source class rule; use a selector at least as specific as the class chain or `!important` on the transported first-frame declarations. Preserve first-frame declaration pairs together, including `width` + `height` collapsed image states. A raw inline state may be `preserved-inline` only when a future converter contract explicitly allows it; otherwise required states must be cascade-safe `converted-to-css/embed`. `converted-css-cascade-risk` and `stripped-without-equivalent-transport` are hard L-8/SV-18 failures.

**Mode B static-visible safety addendum (2026-04-21, Session 169):** transport is not enough when the transported first frame hides real content and Mode B suppresses `js/webflow.js`. A `data-flowbridge-ix-state` rule that sets `opacity:0`, `visibility:hidden`, `display:none`, zero width/height, or an offscreen transform on a content-bearing root (text/media/link descendants) creates a permanent blank surface. MNZ section 4 proved this with `.tabs-blog.w-tabs`: the blog grid/cards existed in the DOM, but `[data-flowbridge-ix-state="ixs-128"] { opacity:0 !important; }` hid the entire tabs root while Mode B had no runtime to reveal it. In `webflow-paste`, either emit a visible static fallback for such roots or halt and require `local-preview` / interaction-preserving output. The probe row `mode-b-static-visible-ix-state-safety` is a hard L-8/SV-18 failure if unsafe hidden/collapsed content-bearing markers remain.

**Regression anchors (MNZ):**
- `.hero-parent` — opacity: 0 + transform quadruple (translate3d + scale3d + rotate)
- `.recent-info-parent` — opacity: 0 + transform quadruple
- `.span-text.in-one` — opacity: 0 + transform quadruple
- `.parent.flex.intro` — opacity: 0
- `.img-parent.intro` — opacity: 0 + transform quadruple
- `.img-parent.recent-post` — opacity: 0 (or width: 0rem)
- `.img-parent.top-size` — paired `width: 100%` + `height: 0rem` collapsed first frame
- `.align-right` — opacity: 0
- `.parent.flex-split.info-bar.text-white` — opacity: 0

**Evidence of the bug:** same forensic audit — hero and loading choreography flattened across all hero-band elements.

**Earlier decision superseded:** `AI_OS/AI_DECISION_LOG.md` Decision 2 (2026-04-13) ruled "strip by vendor-prefix fingerprint." That was correct at the time for nav-menu shells but was applied too broadly. L-8 narrows it.

### L-8 addendum — IX2 initial-state vs component-root hidden-before-hydration (2026-04-17)

L-8's preservation floor treats inline `opacity: 0` as sacred by default. That is correct when the only purpose of the inline style is an IX2 entrance animation. It is wrong when the element is also a component-library root whose configuration happens in Webflow Designer.

**Distinguish by structural role, not class-name regex:**

- **IX2 initial-state.** `data-w-id` references an IX2 entrance animation whose starting state is `opacity: 0`. The designer does not need to see this element visible in Designer; designing *the hidden starting state* is the point. **Preserve** — standard L-8 behavior.
- **Component-root hidden-before-hydration.** The element is a third-party component library root (splide, swiper, w-slider, lottie wrapper, embla, flickity, etc.) whose children follow a library-imposed structural shape (track/list/slide, wrapper/slide, etc.) AND whose runtime script reshapes the DOM on hydration. Designer-side configuration is mandatory — the designer must add slides, set counts, adjust options. An invisible component root blocks configuration. **Strip** the inline `opacity: 0`; the component library manages its own hidden-before-ready state.
- **Both apply (component root with a `data-w-id` IX2 entrance, e.g. MNZ's `<div data-w-id="..." style="opacity:0" class="splide slider2">`).** **Strip** the inline opacity, **preserve** the `data-w-id` and the IX2 animation config. IX2's runtime engine re-applies the starting state when it boots; the inline style is redundant for IX2 purposes but would otherwise block Designer configuration. Designer configurability wins the tie-break.

**Principle for telling component roots apart from ordinary IX2 initial states:** structural role, not class-name list. A component root is recognized by (a) its children's library-imposed shape, (b) a runtime script in the export that hydrates/reshapes it, and (c) the fact that the designer must interact with its contents in Designer. The class name (`splide`, `w-slider`, `swiper-container`, etc.) is evidence of structural role, not a trigger. Do not ship this as a regex list of component class names — reason about each element's structural role individually.

**Illustrative (MNZ):** `<div data-w-id="063f05db-f4b9-a377-5c7d-26df664f29a1" style="opacity:0" class="splide slider2">` is both IX2-animated and a splide component root. Correct pretreatment strips the inline `opacity: 0` and preserves the `data-w-id` + IX2 animation config. Illustrative — principle applies to any component library whose roots hydrate at runtime and are configured in Designer.

### L-8 addendum — Mode-B target detection is class-name-agnostic (2026-04-25, EXP-004)

The probe rows `mode-b-initial-state-transport` and `mode-b-d007-anchor-safety` previously enumerated targets from a hardcoded MNZ-derived catalog (`nav-child-left-closed`, `bg-whipe-overlay-collapsed`, `nav-link-one|two|three-hidden`, `slider2-component-root`, `img-parent-top-size-collapsed`, `recent-info-parent-offset`). EXP-004 replaced that catalog with a structural detector in `paste_contract_probe.py` (`detect_mode_b_targets`) that scans source HTML for elements whose inline `style=""` carries a hidden-on-load declaration (display:none, visibility:hidden|collapse, opacity:0, off-screen translate, zero-scale transform, fully-clipped clip-path, or zero-collapse on a sizing property) and whose style is IX-shaped per the existing vendor-prefix transform / opacity / size-zero fingerprint OR carries `data-w-id`. The element must have at least one non-framework class token and must not itself be an `fb-*` host.

The detected target list is per-source: every fixture (MNZ, Señorita Colombia, future templates) emits its own catalog without skill code change. Mode-B class names like `.bg-whipe`, `.nav-child.left`, or `.menu-bar-whipe` remain valid evidence anchors but are no longer scope-defining; the rule body that names them is illustrative, not exhaustive.

**Open design question carried into EXP-005:** the d007 anchor row still hardcodes the MNZ class chains `("nav-child", "left")`, `("bg-whipe",)`, and `menu-bar-whipe` for the legacy MNZ menu-overlay co-transport pattern. Generalising it to "any `menu-bar-*` shell co-transports its hidden-on-load child overlays" overlaps with L-31 emission logic and is deferred to EXP-005 alongside the L-31 author step.

---

## L-9 — Source Library Preservation as Pre-Treatment Evidence (KEEP; reframed 2026-04-19 EXP-019)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pipeline boundary (set by EXP-019):** Pre-treatment is the AI reasoning pass over the raw Webflow export ZIP. It chooses or creates the correct wrapper shape, places source code and existing embeds into the canonical embed structure, names hosts correctly, preserves source libraries and runtime evidence, and adds only the compensations necessary so that moving content into the new structure does not change the intended visual/runtime behavior. The later converter/Webflow stage owns IX2-to-IX3 and IX3-to-IX3 behavior conversion. **Pre-treatment does NOT decide that conversion and does NOT classify source libraries by downstream Webflow-native representability.**

**Pattern:** Webflow exports ship GSAP-family library CDNs (GSAP core, SplitText, ScrollTrigger, ScrollSmoother, DrawSVG, MorphSVG, Flip, etc.) plus any associated inline init bodies as part of the source runtime. These libraries are the source site's behavior evidence. Some of the behavior they drive is representable in Webflow's IX2/IX3 panels; some is not. That classification is a downstream converter/Webflow concern — pre-treatment has no way to re-create the runtime behavior for the converter if the libraries were dropped at this stage. The BigBuns 108 diagnostic proved this empirically: removing GSAP/SplitText/ScrollTrigger from the raw fixture reproduced the exact Webflow-runtime `TypeError: Cannot read properties of undefined (reading 'timeline')`; restoring those three CDNs cleared the TypeError, flipped `w-mod-ix3` from false to true, and made guarded content visible again.

**Rule — pre-treatment must preserve source-shipped library/runtime dependencies:**

1. **Preserve source-shipped CDN tags.** Every `<script src>` in the source export whose `src` matches a source-shipped runtime library (GSAP family, jQuery, Splide, Lenis, Swiper, Lottie, Embla, Flickity, and any other library the source references) is preserved in the pre-treated output. Pre-treatment MAY relocate the `<script>` into the correct embed host — for the GSAP family and other CDN libraries, that is `fb-scripts.w-embed` inside `fb-custom-code` per L-15; the local Webflow runtime has the L-15A late-placement carve-out. Pre-treatment MUST NOT strip a source-shipped library based on downstream Webflow-native convertibility.
2. **Preserve source-shipped inline init bodies.** Every retained inline init/body associated with a source-shipped library (GSAP timelines, SplitText instantiations, ScrollTrigger registrations, Splide/Lenis/Swiper inits, plugin bridges, detectors, arbitrary custom-code bodies) is preserved as source evidence. Bodies that reference runtime globals or immediately touch source DOM are wrapped per L-16; bodies that do neither are placed inside `fb-scripts.w-embed` in source order. Pre-treatment MUST NOT delete a source inline init body on the theory that the final interaction "could be" re-expressed in Webflow's IX2/IX3 panels.
3. **Record relocations in the manifest.** When a source-shipped library tag or retained inline body is moved from its original location, the Mandatory Output Manifest (SKILL.md §Mandatory Output Manifest — Before You Zip) records the original location, the new host, the source-order index, and the dependency reason (which globals the host owns and which retained inline body consumes them). This is what makes the move auditable rather than a silent drop.
4. **HALT on documented incompatibility; never silently strip.** If a specific source library cannot be preserved safely because of a named, documented concrete pre-treatment/converter incompatibility, the skill writes `HALT-REPORT.md` or annotates the incompatibility in the manifest with the incompatibility evidence and hands back to Maria. Preservation is the default; removal requires a written justification that another experiment can challenge.
5. **Generate-new ≠ preserve-source-shipped.** This rule does NOT bless synthesizing new GSAP or custom interaction code for native-capable Webflow interactions. SKILL.md Hard Rule #3 continues to ban that generation step. L-9's scope is preservation of what the source export already ships, not authoring of new custom code.

**Failure mode this prevents:** 108 diagnostic (`AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-19/108-result-cross-fixture-skill-repair-diagnostic.md`) captured the BigBuns failure: the current skill saw a source export that had no live author GSAP init, classified source-shipped GSAP/SplitText/ScrollTrigger CDNs as "IX2/IX3-representable therefore stripable", and dropped them. The Webflow runtime then crashed on `timeline` with `gsap=undefined`; `w-mod-ix3` stayed false; BigBuns' FOUC guard left the page black. The skill was making a downstream conversion-stage decision with pre-treatment-stage information.

**Verification gate:** the Mandatory Output Manifest row L-9 carries a runnable preservation check — enumerate GSAP-family `<script src>` elements in the source fixture ZIP and in the output `fb-scripts.w-embed`, assert output count is ≥ source count for the GSAP-family set. Any shortfall MUST be matched by a named HALT-REPORT.md incompatibility entry; an unexplained drop is a hard FAIL and the skill has not finished. See SKILL.md §Mandatory Output Manifest — Before You Zip for the full row.

**Historical note:** the pre-2026-04-19 L-9 body was titled "GSAP Bloat Strip With IX2/IX3-Impossibility Exceptions" and asked pre-treatment to classify source GSAP usage as native-representable vs exception and strip the native-representable cases. That framing required pre-treatment to own the IX conversion decision, which it does not. 108 diagnostic on BigBuns exposed the concrete regression. Full prior body preserved in git history prior to EXP-019.

**Evidence:** `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-19/108-result-cross-fixture-skill-repair-diagnostic.md` (BigBuns isolation + revert experiment); `AI_OS/AI_DECISION_LOG.md` Decision 8 (original L-9 rationale, superseded by EXP-019).

---

## L-11 — Single-Root `fb-page-wrapper` (KEEP)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Webflow Designer paste expects a single root element. Multi-root HTML silently drops secondary trees.

**Rule:** Ensure every pretreated page has exactly one child of `<body>`: an element whose class list includes `fb-page-wrapper` and that contains everything. If the source already has a single-root wrapper as the sole body child, reuse that element, add the `fb-page-wrapper` class to it, and inject the pre-treatment hosts into that same root. Do **not** wrap it again. If the source body is multi-root, create a neutral wrapper and nest all source body children inside.

---

## L-12 — `fb-custom-code` Host Contract (KEEP; Option A locked 2026-04-17)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Pasted content needs hidden embed hosts for compensation CSS, extracted site CSS, non-canonical `@media` rules, library overrides, and init scripts. These are `w-embed` divs.

**Rule — Option A (all embeds inside one hidden container):** `fb-custom-code` is THE single hidden container (`style="display:none"`) for every pre-treatment-injected embed. All embed hosts nest INSIDE `fb-custom-code`:

- `fb-styles-site` — canonical-breakpoint site CSS + `:root` variables + L-4 baseline floor + wrapper-compensation CSS
- `fb-styles-[library]` — library-specific style overrides; class name is descriptive of the library (`fb-styles-splide`, `fb-styles-lenis`, etc.)
- `fb-media-site` — non-canonical `@media` rules + fluid-typography cascades (L-2 / L-2.1)
- `fb-scripts` — library CDNs and dependency-gated init scripts (L-3)

`fb-custom-code` itself is the first direct child of `fb-page-wrapper` and carries all embeds. After it come the preserved visible content children for that root:

- when L-11 reuses an existing single-root wrapper, these are that wrapper's original direct children, in source order;
- when L-11 synthesizes a neutral wrapper for a multi-root body, these are the source body's original direct children, in source order.

No embed host is a sibling of `fb-custom-code`.

**Library naming:** descriptive class names following the `fb-styles-[library]` template. The previous generic name `fb-library-styles` is retired — it conveyed nothing about which library the embed served. When a new library requires an embed (e.g. Swiper, Embla, Lottie, Lenis), name it `fb-styles-swiper`, `fb-styles-embla`, etc.

**Why Option A (single hidden container):** one hidden container makes the "all my pre-treatment additions live here" contract visible in a single DOM node. The previous mixed shape — some embeds inside `fb-custom-code`, some as siblings — created an internal contradiction (was `fb-custom-code` the parent container or a sibling?) and a place where skill updates could disagree with each other. Option A resolves both. The `display: none` on `fb-custom-code` does not suppress the CSS embeds' effect — browsers parse `<style>` content regardless of ancestor visibility — so nesting every style, media, and script embed under a single hidden container is zero-risk for CSS or script behavior and a large clarity win: the pre-treatment injection surface lives in exactly one DOM node.

**Ordering inside `fb-custom-code`:** `fb-styles-site` first (canonical breakpoints + `:root` + wrapper compensation), then any `fb-styles-[library]` blocks, then `fb-media-site` (non-canonical `@media` + fluid type), then `fb-scripts` LAST. Source-order preserved within each embed. Scripts run after all style blocks are parsed.

**L-12 exception — L-15A runtime late host (2026-04-18 EXP-009):** one narrow exception exists to the "all pre-treatment-injected embed hosts live inside `fb-custom-code`" invariant. A late `fb-runtime.w-embed` host may appear as a direct child of `fb-page-wrapper`, positioned AFTER all source-content siblings, carrying exactly the external `<script src="js/webflow.js"></script>` reference. The exception is justified by runtime hydration semantics — Webflow's IX2 engine hydrates against already-parsed source content and misses targets when it boots early. The exception is narrow, machine-checkable by SV-13-B, and does NOT broaden to any other embed class. All style hosts (`fb-styles-site`, `fb-styles-[library]`, `fb-media-site`), author-scripts host (`fb-scripts`), and inline init bodies remain inside `fb-custom-code`. See L-15A (2026-04-18) for the placement rule.

---

## L-13 — Multi-Root Content Siblings Under `fb-page-wrapper` ("ideally rooted" hedge) (KEEP)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** L-11 requires `body` to have exactly one element child (`fb-page-wrapper`), but some Webflow exports author layouts where nav, main content wrapper, and footer need to be direct siblings of a common root with specific z-index / reveal-footer / stacking-context relationships. Forcing them into a single content div would break the stacking; hoisting them above `fb-page-wrapper` would violate L-11.

**Rule (hedge, not break):** `fb-page-wrapper` IS the single child of `body`. Inside `fb-page-wrapper`:

- `fb-custom-code` is the first element child (per L-12 Option A; carries all pre-treatment-injected embed hosts).
- Source body's original direct children follow as **multi-root content siblings in source order**. On MNZ Creative these are `nav`, `wrapper`, `footer-parent` — three direct siblings of `fb-custom-code`, order preserved from source, z-index and reveal-footer stacking intact.

**When multi-root is required vs when to collapse:** if the source body already has a single content root (one element child containing everything visible), reuse that root as `fb-page-wrapper` directly — add the class, inject `fb-custom-code` as its first child, and do not synthesize a second wrapper around it. If the source body has multiple content siblings AND they rely on sibling relationships for stacking (reveal-footer pattern, z-index chains, fixed-position sibling contexts), preserve them as siblings under the synthesized `fb-page-wrapper`. Do not wrap those siblings into an extra synthetic content div — that changes containing blocks and can break layout.

**Source-order discipline:** multi-root siblings MUST preserve source order. Re-ordering can flip z-index relationships (`position: relative` + default z-index stacks by source order). Verify via BeautifulSoup direct-children enumeration before shipping.

**Evidence:** EXP-005.b PASS (2026-04-17) — MNZ output preserves `nav`, `wrapper`, `footer-parent` as siblings after `fb-custom-code`; reveal-footer stacking confirmed in Designer inspection. EXP-005.b.1 part 2 (064) re-verified source-order preservation.

---

## L-14 — `@font-face` Format-Invariant Source-Origin Duplication (KEEP — treat as pass-through)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** INFORMATIONAL

**Pattern:** Webflow's exporter occasionally emits the same `@font-face` block twice per font in the compiled site CSS, with different quoting conventions: unquoted family name + double-quoted format string vs single-quoted family + single-quoted format. The duplication is format-invariant — it appears regardless of whether the font is served as `truetype` or `opentype`:

- **MNZ Creative:** `format("truetype")` + `format('truetype')` pairs — 5 duplicate pairs, 10 blocks total, 5 unique keys
- **Señorita Colombia:** `format("opentype")` + `format('opentype')` pairs — same structure, 5 duplicate pairs, 10 blocks, 5 unique keys

**Rule:** Under L-1 Option B (opaque-blob), source-origin `@font-face` duplicates pass through verbatim into HEAD inline `<style>`. SV-6 (narrowed 2026-04-17 to Option α) classifies them as "source-origin, not skill-introduced" by comparing source CSS `@font-face` counts to output `@font-face` counts — per-key count parity required, any skill-introduced increase FAILs.

Webflow's paste pipeline canonicalizes quoted/unquoted family variants at paste time (KF-2), so source-origin duplicates resolve to a single font registration in the compiled `*.webflow.shared.*.css` — no production impact.

**DO NOT add a dedup mutation to L-1.** The opaque-blob invariant is what makes Option B generalize across format variants. Adding content-aware dedup re-introduces the fragility that Option A's family-name canonicalization had (family lookups brittle across quoting conventions, variant spellings, Unicode normalization). Format-invariance is a property of the opaque-blob approach.

**Future format variants:** `woff`, `woff2`, and anything else the Webflow exporter emits will exhibit the same quirk. SV-6 α's key-normalization ((family-lowercased, weight, style, url-path) WITHOUT `format()` in the key) already handles this — no skill updates needed when new format variants appear.

**Evidence:** KF-5 (MNZ truetype, EXP-003.2 SV-6 FAIL → Option α narrowing, 2026-04-17). KF-6 (Señorita Colombia opentype, EXP-004 PASS, 2026-04-17). SV-6 canonical procedure in `references/verification-gate.md`.

---

## L-15 — Uniform Script Wrapping (KEEP; introduced 2026-04-17 EXP-005.b.1 PASS)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Before EXP-005.b.1, SKILL.md had an internal contradiction (rule 17): L198 + L253 said `fb-custom-code` contains "every pre-treatment-injected embed" / "ALL embed hosts," but the Target Structure example emitted jQuery CDN + inline Webflow init `<script>` tags OUTSIDE `fb-custom-code`, as direct children of `fb-page-wrapper`. MNZ outputs correctly reproduced the contradictory Target Structure: 2 bare `<script>` tags surfaced as `fb-page-wrapper` direct children in EXP-005.b, failing the clean-structure principle.

Architect ruling (Maria, 2026-04-17): resolve by uniform wrapping. No classifier between "runtime" / "library" / "content" scripts. Judgment calls don't scale across fixtures — Webflow exports carry many script shapes (CDN refs, inline runtime init, dependency-gated inits, w-mod detection, component library inits) and any classifier produces edge cases per fixture. Uniform wrap eliminates the decision tree.

**Current rule after L-15A:** Every preserved source `<script>` element from HEAD and body is accounted for structurally. CDN libraries and inline init/detector/deferred bodies are emitted inside a single `<div class="fb-scripts w-embed">`, which is itself nested inside `fb-custom-code`. The export's relative `js/webflow.js` runtime is the L-15A/L-19 exception: it is preserved as exactly one external `<script src>` reference in a late `fb-runtime.w-embed` after source content and is never inlined. No separate preview artifact. The following structural invariants hold for every pre-treated output:

- **SV-9-A:** zero `<script>` direct children of `fb-page-wrapper`
- **SV-9-B:** `fb-custom-code` is direct child of `fb-page-wrapper`
- **SV-9-C:** `fb-scripts` is direct child of `fb-custom-code`
- **SV-9-D:** every source HEAD + body script is accounted for: CDN libraries and inline init/defer bodies live inside `fb-scripts`; the single relative `js/webflow.js` runtime lives inside late `fb-runtime`; zero inlined webflow.js module IIFE content; no naked scripts anywhere.
- **SV-9-E:** source-order preserved within `fb-scripts` for CDN libraries and inline bodies — jQuery source-order index < preserved inline init source-order index when both exist.

HEAD-origin scripts (e.g. Webflow's `w-mod-js` / `w-mod-touch` detection, site-authored `<script defer>` click-forwarders, analytics stubs, or inline body detectors) are source evidence and must be inventoried. If retained, they are emitted into `fb-scripts` unless they are the L-15A `js/webflow.js` runtime carve-out or the L-19-forbidden inline runtime IIFE. They execute later than their HEAD-position origin would imply, so any body that immediately touches DOM must use L-16 selector readiness. Srta Colombia proved this: a HEAD `<script defer>` binding `.menu-dropdown` to `.menu-btn.click()` was captured but not emitted, breaking the menu-forwarder on one detail page.

**Why uniform, not selective:** a classifier-based approach (e.g. "wrap library CDNs + inits inside `fb-scripts`, leave runtime scripts as wrapper-direct children") was proposed and rejected. Every classifier has edge cases. Every "leave as-is" exception is a seam where SKILL.md can drift. Uniform wrapping collapses the decision surface to a single rule and matches the Webflow-native HtmlEmbed-with-script mechanism.

**Why this doesn't break jQuery / init order:** `fb-scripts` preserves source order within its child list for CDN libraries and inline bodies. If source had `<head> w-mod </head> <body> ... jquery.js ... init </body>`, the resulting `fb-scripts` preserves that dependency order. The external `<script src="js/webflow.js">` reference is the L-15A carve-out and executes later from `fb-runtime` after source content parses; inline bodies that need `Webflow` wait through L-16. Inlining the Webflow module IIFE remains forbidden.

**SV-9 is a structural floor, not a stylistic preference.** Any pre-treated output that produces a naked `<script>` direct child of `fb-page-wrapper`, or scatters scripts across siblings, or reorders dependencies inside `fb-scripts`, fails SV-9 and is DISCARD.

**Evidence:** EXP-005.b (2026-04-17) PASS-conditional — surfaced the SKILL.md L198/L253 vs Target Structure contradiction; script-placement boundary folded into .b.1. EXP-005.b.1 part 1 (063, 2026-04-17) PASS — patched SKILL.md Target Structure + `decision-patterns.md` Script-Emission-Policy section + `verification-gate.md` SV-9 "Naked-Script Floor." EXP-005.b.1 part 2 (064, 2026-04-17) PASS — re-run on MNZ, 8/8 scripts inside fb-scripts, jQuery idx 1 < webflow idx 2, zero wrapper-direct scripts, 137/137 L-8 transforms preserved, wrapper-compensation Step 3 walkthrough 5 PASS + 1 N/A.

**Related gates:** SV-9-A..E in `references/verification-gate.md` §SV-9 (line ~348). Target Structure in `AI_OS/SKILLS/webflow-pretreat/SKILL.md` §L196-240 (post-063 patch). Script-Emission-Policy in `references/decision-patterns.md`.

### L-15 Addendum — Local Webflow Runtime Late Placement (2026-04-18 audit-083 / EXP-009)

L-15's uniform script wrapping is correct for CDN libraries and inline init bodies. It is WRONG for the one script class whose execution hydrates IX2 against already-parsed page content: the local Webflow runtime `js/webflow.js`. Audit-082 (2026-04-18 file-URL browser audit) caught the regression — early placement inside `fb-scripts` inside the first `fb-custom-code` puts the runtime before `nav`, `wrapper`, and `footer-parent` parse, so IX2 hydration misses every target. Section 04 reveal, menu open height, and footer transform all failed on MNZ. Audit-083 confirmed the three-class partition.

**Core L-15 rule remains:** CDN library scripts and inline init scripts live in `fb-scripts.w-embed` inside the top `fb-custom-code`. Preserve source order inside that host. Apply L-16 dependency-gating to inline init bodies.

**Carve-out:** a relative local runtime script whose `src` path ends in `webflow.js` is NOT emitted into early `fb-scripts`. It emits as a late runtime script after all `.fb-page-wrapper` source-content children parse, inside a dedicated `fb-runtime.w-embed` host that is itself a direct child of `fb-page-wrapper`, positioned AFTER all source-content siblings.

**Three-class detection and placement:**

| Class | Detection | Destination | Why |
|---|---|---|---|
| CDN library | `src` absolute HTTP(S) or known CDN (`jquery`, `cdn.jsdelivr.net`, `unpkg`, `cdnjs`, `greensock`) | `fb-scripts.w-embed` inside first `fb-custom-code` | Loads a library; no populated-body dependency at execution time. |
| Inline init / detector / deferred body | No `src` AND references runtime globals (`Webflow`, `jQuery`/`$`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, `window.<global>`) OR installs document/listener/selector work (`DOMContentLoaded`, `click`, `scroll`, `IntersectionObserver`, `querySelector`, etc.). Includes HEAD `<script defer>` bodies. | `fb-scripts.w-embed` inside first `fb-custom-code`, L-16 gated when globals or selectors are present | Can register listeners or poll for globals early; L-16 handles runtime and selector/DOM ordering. |
| Local Webflow runtime (external src) | Relative `script[src]` whose normalized basename is `webflow.js`, NOT HTTP(S) | `fb-runtime.w-embed` direct child of `fb-page-wrapper`, AFTER all source-content siblings | Hydrates IX2 / runtime state against existing DOM; early placement misses hydration targets. |
| Local Webflow runtime (inline IIFE) | Inline script containing Webflow module IIFE signature AND all three of `Webflow.push`, `Webflow.require`, `Webflow.define`, length > 50,000 chars | DO NOT emit | L-19 crash mechanism; hard fail, not a placement candidate. |

**Future preferred host shape (Posture 1, locked 2026-04-18 architect ruling):**

```html
<div class="fb-page-wrapper">
  <div class="fb-custom-code" style="display:none">
    <div class="fb-styles-site w-embed">...</div>
    <div class="fb-styles-[library] w-embed">...</div>
    <div class="fb-media-site w-embed">...</div>
    <div class="fb-scripts w-embed">
      <!-- CDN libraries + inline init bodies only; webflow.js is NOT here -->
    </div>
  </div>

  <!-- source-content siblings in source order -->
  <div class="nav">...</div>
  <div class="wrapper">...</div>
  <div class="footer-parent">...</div>

  <!-- late runtime host, AFTER all source-content siblings -->
  <div class="fb-runtime w-embed" style="display:none">
    <script src="js/webflow.js"></script>
  </div>
</div>
```

**Why Posture 1 not Posture 2 (body-end child after wrapper closes):** Posture 1 keeps `.fb-page-wrapper` as the single `<body>` child, preserving L-11's paste invariant. Posture 1 uses the proven `w-embed` host mechanism (same clipboard-survivability profile as `fb-styles-[library]` under L-17). Posture 2 would put a bare `<script>` as direct `<body>` child — untested structural territory at the Webflow paste consumer. Posture 1 requires a narrow L-12 exception (see L-12 above); the exception is machine-checkable and justified by runtime hydration semantics.

**Self-verify checklist (run before declaring output complete):**

1. Exactly one external `<script src="js/webflow.js"></script>` exists in the output.
2. Zero inline Webflow module-IIFE bodies are present.
3. The external `js/webflow.js` script is NOT a descendant of the early `fb-scripts` host.
4. The external `js/webflow.js` script's document position is AFTER the last source-content direct child of `.fb-page-wrapper`, or the script appears immediately after `.fb-page-wrapper` in body-end-equivalent shape.
5. CDN library scripts remain in `fb-scripts.w-embed` and preserve source order before their inline init bodies.
6. Inline init/defer bodies from HEAD and body remain in `fb-scripts.w-embed`; any runtime-global body is L-16 dependency-gated, and any selector/listener body is L-16 selector-gated even when `need[]` is empty.
7. No source-content direct children (`nav`, `wrapper`, `footer-parent`, or fixture-equivalent content siblings) move relative to each other.

**Sync Surface (this addendum anchors to):**

- `AI_OS/SKILLS/webflow-pretreat/SKILL.md` §Hard Rules (webflow.js placement rule), §Target Structure (example HTML with `fb-runtime` sibling), §Verification Checklist (SV-13-B line).
- `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` §Script Handling (three-class taxonomy integrated into universal placement rule), L-19 cross-ref.
- `AI_OS/SKILLS/webflow-pretreat/references/decision-patterns.md` §Script Emission Policy (three-class decision table replaces uniform-wrap policy).
- `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` SV-9 clarification (SV-9-C still applies to CDN + inline init; runtime governed by SV-13-B); SV-13 split into SV-13-A (external-ref + IIFE-absence) and SV-13-B (late placement procedure).
- `AI_OS/SKILLS/webflow-pretreat/references/webflow-constraints.md` §"Preserve webflow.js as an external src reference" (placement-qualifier sentence pointing to SV-13-B).
- All five skill files above must also land byte-identical in the `.claude/skills/webflow-pretreat/` project mirror AND `C:\Users\maria\.claude\skills\webflow-pretreat\` user-global mirror (Skill tool loads from user-global at runtime).
- `docs/LESSONS.md` L-12 exception paragraph (above) + L-19 placement scope-note (below).

**Cross-references:** L-12 exception (above) — narrow exception to "all embeds inside one hidden container"; L-19 placement scope-note (below) — L-19's external-ref preservation rule was placement-incomplete, this addendum completes it; L-11 single-root paste invariant — preserved because `fb-runtime` is another child of `fb-page-wrapper`, not a `<body>` sibling.

**Evidence:** audit-082 (file-URL browser audit, 2026-04-18) caught the regression on three gates (`.tabs-blog.w-tabs` opacity stuck at 0, `.nav-child.left` dimensions 720×48 instead of 720×480, `.hero-title.pull` transform `none` instead of `matrix(1,0,0,1,0,72.5703)`). Audit-083 (2026-04-18) confirmed the three-class hypothesis by inventory and position diff. EXP-009 (2026-04-18, session 085) lands this addendum.

---

## L-16 — Universal Runtime + DOM-Ready Init Gating (KEEP; introduced 2026-04-18 from 068 mechanical-extraction audit)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Any retained inline custom-code script can depend on more than one runtime global — any combination of `Webflow`, `jQuery` / `$`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, plus any future library or site-defined global. It can also depend on source DOM selectors even when it has no runtime global dependency, especially HEAD `<script defer>` bodies that bind events after parse. This includes third-party library inits, GSAP/ScrollTrigger exception code that cannot be represented in Webflow IX2/IX3 panels, plugin bridges, detectors, DOM click-forwarders, and arbitrary source custom code. A single-global gate races: `Webflow` exists but jQuery is still loading → init fires, silently no-ops. A globals-only gate also misses selector-only scripts.

**Rule:** After moving any non-CDN inline executable `<script>` from HEAD or body into `fb-scripts.w-embed`, read the script body with comments and dead-bridge code stripped, enumerate **every** runtime global it references, and wrap the body in ONE bounded polling runner that resolves only when every required global is present. `need[]` may be empty when the script has no runtime global dependency. If the retained code immediately queries, mounts onto, animates, observes, or binds to page DOM (`$('.slider2')`, `document.querySelector(...)`, `new Splide(selectedEl)`, `gsap.to('.hero-title', ...)`, `ScrollTrigger.create({ trigger: '.section' })`, `document.querySelector('.menu-dropdown').addEventListener(...)`, Swiper/Embla/Flickity/Lottie mount roots, custom widget roots, etc.), classify each selector as required or optional. Required selectors are dereferenced without a guard, mounted as primary component roots, or drive visible behavior that exists on the source page; the runner waits for DOM parsed and selector presence. Optional selectors are guarded/null-safe, `querySelectorAll` loops that may legitimately be empty, or progressive-enhancement/page-specific controls; the runner waits for DOM parsed but does not require presence. Warn on timeout. Apply only to inline scripts/custom-code bodies — CDN `<script src>` tags are loads, not inits; do NOT wrap them in the dep-gate runner (L-15 still places the `<script src>` element itself inside `fb-scripts`). Valid `application/ld+json` scripts are metadata only when their bodies parse as JSON-LD; executable code must never be mislabeled as JSON-LD. The accepted emitted shape is per-body: the retained executable body itself lives inside `fbRun`; a shared helper preamble with raw executable bodies left outside that wrapper is not L-16-compliant.

Publish-safe Webflow global rule: an inline body that touches `Webflow.env`, `Webflow.push`, or `Webflow.require` must not call bare `Webflow.*` as a top-level expression. Either wrap the retained body in the L-16 runner with `Webflow` in `need[]`, or use the safe Webflow queue preamble (`window.Webflow = window.Webflow || []; window.Webflow.push(function(){ ... });`). A bare `Webflow.push(...)` is not safe if the published page executes the embed before Webflow defines the global.

Runner shape (50ms × 200 = 10s cap, bounded):

```js
(function () {
  const need = [/* array of detected global names */];
  const requiredSelectors = [/* required source selectors for immediate DOM mounts, or [] */];
  const optionalSelectors = [/* optional/guarded source selectors, or [] */];
  const fbDepsReady = () => need.every(n => window[n]);
  const fbNeedsDom = () => requiredSelectors.length || optionalSelectors.length;
  const fbDomReady = () => !fbNeedsDom() || document.readyState !== "loading";
  const fbSelectorsReady = () => requiredSelectors.every(s => document.querySelector(s));
  const fbReady = () => fbDepsReady() && fbDomReady() && fbSelectorsReady();
  const fbRun = () => {
    /* original init body goes here, unmodified */
  };
  if (fbReady()) fbRun();
  else {
    let t = 0;
    (function poll() {
      if (fbReady()) { fbRun(); return; }
      if (++t > 200) {
        console.warn('fb-init timeout:', {
          globals: need.filter(n => !window[n]),
          selectors: requiredSelectors.filter(s => !document.querySelector(s))
        });
        return;
      }
      setTimeout(poll, 50);
    })();
  }
})();
```

50ms × 200 = 10s bounded cap using `setTimeout`-recursion. `setInterval` is rejected by the verification probe (`scripts/paste_contract_probe.py` `has_l16_wrapper`) and must not be used in L-16 runners; `setTimeout`-recursion guarantees each tick waits for the previous iteration to complete, preventing queued-callback bursts when heavy init bodies (SplitText, ScrollTrigger, Lenis, Splide) run under thread pressure.

**Why:** A single-global gate (L-3 / pre-L-16 template) was written for the simplest case — one library dependency. Real Webflow exports carry retained code that touches jQuery + Webflow + Splide in a single block, or Webflow + Lenis, or gsap + ScrollTrigger, or custom globals plus DOM selectors. Gating on only the first-detected global lets the runner fire while a later dependency is still loading; the resulting silent no-op looks like a skill bug at paste time. EXP-016 added the second race class: moving source body-end custom code into early `fb-scripts` can make it execute before the component/animation/widget DOM exists. MNZ section 2 proved it with Splide: `window.Splide` and `$` were ready, but `.slider2` had not parsed yet, so the init mounted zero elements and the slider never received `is-initialized`. Srta Colombia proved the HEAD-defer variant: a HEAD `<script defer>` menu-forwarder was captured but dropped, so `.menu-dropdown` no longer triggered `.menu-btn`. Splide and the menu forwarder are proof cases, not the scope.

**How to apply:** (1) scan every retained inline script/custom-code body from HEAD and body for `window.<X>`, `jQuery` / `$`, `Webflow`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, site-defined globals, and any other explicit runtime reference; (2) build `need[]` as the superset of detected globals, possibly `[]`; (3) scan the body for selectors that exist in the source body and are used immediately as mount roots, animation targets, ScrollTrigger triggers, observers, listeners, or custom widget roots (`$('.slider2')`, `document.querySelectorAll('.swiper')`, `document.querySelector('.menu-dropdown').addEventListener(...)`, `gsap.to('.hero-title', ...)`, `ScrollTrigger.create({ trigger: '.section' })`, etc.); (4) split selectors into `requiredSelectors[]` and `optionalSelectors[]`; (5) emit one wrapper per retained executable body, with the original body inside `fbRun`; (6) `fbReady()` must require globals, DOM parsed when any selector is involved, and every required selector present; (7) leave the `<script>` element's position inside `fb-scripts.w-embed` unchanged (L-15 uniform wrapping still governs structural placement). Valid JSON-LD metadata scripts are parsed as JSON-LD and preserved without the executable runner.

**Anchors in skill files:** `references/lessons.md` Script Handling section (dep-gate runner template replaces the single-name template); `references/verification-gate.md` SV-10; `references/decision-patterns.md` Pattern I; `SKILL.md` Verification Checklist + Target Structure.

**Evidence:** 068 Codex audit §M-11 diffed the mechanical multi-global runner at `core.ts:556-596` against the current skill's single-global template at `references/lessons.md:242-258` and classified the gap as PARTIAL. 069 landed the multi-dependency shape as L-16. `AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-19/118-audit-srta-colombia-vs-claude-skill-output-index-root-pages-parity.md` added the HEAD-defer/selector-only preservation failure.

---

## L-17 — Library Style Host Extraction + Designer Visibility Fallback (KEEP; introduced 2026-04-18 from 068 mechanical-extraction audit)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Third-party component libraries (Splide, Swiper, Embla, Flickity, Lottie, Lenis, any future library loaded via HEAD `<link rel=stylesheet>` or HEAD `<style>` block) need their CSS migrated into a named `fb-styles-[library-slug]` embed host nested inside `fb-custom-code`, PLUS a static Designer-visibility fallback so component roots render during Designer canvas authoring when the library runtime does not execute.

**Rule:** For every detected library (by root-class presence in body DOM — e.g. `.splide`, `.swiper`, `.lenis`, `.lottie` — OR by library-specific CDN script in `fb-scripts`):

1. Move all HEAD `<link rel=stylesheet>` and HEAD `<style>` blocks owned by that library into a new HtmlEmbed named `fb-styles-[library-slug]` nested inside `fb-custom-code`, placed BEFORE `fb-media-site` (after `fb-styles-site`, before any other `fb-styles-[library]` blocks in canonical order). Fetch CDN stylesheet bytes and inline them into the host when possible; if fetch is unavailable, move the original `<link>` into the host and record the fetch fallback in manifest evidence.
   - If a root/JS signal exists but no explicit HEAD CSS exists, infer same-package core CSS only when the package/version/path makes that stylesheet deterministic. Fetch and inline it, then record the inferred URL and core markers. If inference is not deterministic, HALT instead of emitting fallback-only CSS.
   - The host must contain core library CSS markers beyond the fallback (examples: Splide `.splide__track` + `.splide__list`, Swiper `.swiper-wrapper` + `.swiper-slide`, Flickity `.flickity-viewport`). Host presence plus fallback is not enough.
2. Remove the original HEAD nodes.
3. Emit a static Designer visibility fallback inside the same host: `.<library-root>, .<library-root>__<inner-standard-classes> { visibility: visible !important; opacity: 1 !important; }` — `!important` is required because the library's own CSS ships `opacity: 0` that would otherwise win. The fallback must target selectors already present in the source DOM. Runtime-added state selectors such as `.splide.is-initialized` or `.splide.is-rendered` may remain in library CSS, but they do NOT satisfy the fallback because Mode B cannot require runtime hydration for baseline visibility.

**Why:** HEAD library CSS is paste-invisible — Webflow's clipboard consumer reads body embeds, not HEAD. The library runtime does not execute in Designer canvas, so components that hide themselves before hydration stay invisible for the designer. MNZ evidence: blank City Girl Guide (Splide slider) and blank Blog (Webflow Tabs + library CSS dependencies) after paste, both surfaced during EXP-005.c. EXP-014 added the sharper failure mode: a local browser can still look correct if the library CDN link remains in HEAD, but the converter/paste path loses that head-only dependency. Session 156 exposed the next narrower failure: a fallback on `.splide.is-initialized, .splide.is-rendered` is still runtime-dependent and leaves Mode B static visibility hostage to initialization. The fallback must target the library root AND at least one inner-standard-class selector (Splide: `.splide__track`, Swiper: `.swiper-wrapper`, etc.) so both the outer container and the first layer of children become Designer-visible without runtime-added state classes.

**How to apply:** Detect by library root class presence in body DOM OR by library-specific CDN script detection in `fb-scripts`. For each detected library, perform the extract/infer → host → fallback sequence. The host must be self-sufficient for the converter path: migrated/inferred core CSS/link payload first, visibility fallback second, zero residual library CSS in HEAD. A fallback-only host, or a host with no core CSS markers, is a FAIL. Generalization: any library whose runtime reshapes children must get a visibility fallback; this is the shape, not the closed list. Splide, Swiper, Embla, Flickity, Lottie → always. Lenis → optional (smooth-scroll runtime does not hide children before hydration).

**Host naming:** `fb-styles-` + lowercase library slug — `fb-styles-splide`, `fb-styles-swiper`, `fb-styles-lenis`, `fb-styles-lottie`. Do NOT use `fb-library-styles` (retired mechanical name, L-12 Option A).

**Anchors in skill files:** `references/lessons.md` Library Handling section (full fallback CSS templates); `references/verification-gate.md` SV-11; `references/decision-patterns.md` Pattern H; `SKILL.md` Verification Checklist line (Splide-fallback item upgraded to L-17/SV-11 cross-ref) + Target Structure example (`.splide__track` + visibility fallback inside `fb-styles-splide`).

**Evidence:** 068 Codex audit §M-13 identified the mechanical collection at `core.ts:672-708` + Splide fallback at `core.ts:88-93, 928-943` as PARTIAL — current skill had the Splide fallback checklist line at `SKILL.md:267` without an SV gate and without the HEAD library style-node migration rule. 069 lands the full extraction + fallback contract as L-17. EXP-014 (2026-04-19) found a false PASS in EXP-012.b MNZ output: `fb-styles-splide` existed with fallback CSS only while the Splide core stylesheet remained in HEAD; the manifest row checked host presence but not migrated payload or HEAD residue. Cross-lane audit 124 added the next guardrail: Codex Srta had fallback/author overrides but no Splide core CSS markers. L-17/SV-11 now explicitly fails fallback-only hosts, missing core markers, non-deterministic CSS inference, and residual HEAD library CSS.

---

## L-18 — ZIP Root and Asset Preservation (KEEP; introduced 2026-04-18 from 068 mechanical-extraction audit)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** Webflow export ZIPs may contain a single top-level folder prefix (marketplace templates especially — e.g. `sitename/index.html`, `sitename/css/...`). Output ZIP must be flat at the Webflow root AND must preserve every non-mutated entry byte-for-byte so relative URLs resolve and re-import works.

**Rule:** On re-zip:

1. Strip exactly ONE common root prefix if and only if ALL source entries share it. Do not strip if entries are mixed-root or already flat.
2. Every file not mutated by pre-treatment is copied byte-for-byte — same path (minus the stripped prefix), same bytes, same mtime if the ZIP tool preserves it. Applies to `fonts/`, `images/`, `js/`, `documents/`, media, and any other non-HTML/CSS asset.
3. Every local asset reference in processed HTML/CSS resolves against the output root after prefix stripping and URL rewrites. If a raw source reference is already broken, repair only when there is exactly one same-directory deterministic candidate after URL-decoding, Unicode normalization, case-folding, and punctuation/separator equivalence. If there is no unique candidate, preserve the source reference and label it as source-premise broken; do not invent a filename.
4. Mutated files (`index.html`, any other processed HTML, potentially `css/*.css` under L-1 Option B's site-CSS deletion) go to their expected flat paths.
5. Current skill runs write exactly one deterministic output pair per lane + source under `output/`: `output/{lane}_{source-slug}-file_output.zip` and `output/{lane}_{source-slug}-file_output/`, where `{lane}` is `claude` or `codex`. Reruns delete and replace that same pair.
6. No extra directories, no renamed directories, no synthetic folders invented by the skill. Timestamped `fresh-runs`, `current-skill`, `rerun`, backup ZIPs, and comparison ZIPs are historical only and not valid current-skill outputs.

**Why:** Incorrect root stripping breaks relative URL resolution from `index.html` (fonts/images 404 on preview). Missing non-mutated entries break preview and break re-import into Webflow. M-19 is infrastructure — not the proximal cause of MNZ's current visual regressions, but required correctness that Option B's opaque-blob rule assumes.

**Carve-out for L-1 Option B:** `css/[sitename].webflow.css` IS deleted from the output ZIP (L-1 step 5 — single source of truth, HEAD inline wins). This is a declared deletion, not a preservation failure. SV-12 treats it as a carve-out. Source-premise broken asset refs may be recorded without failing the structural ZIP, but they keep the audit in HOLD/PARTIAL until fixed or explained; any skill-introduced broken local ref is FAIL. Empty downstream `payload.assets[]` is a clipboard/XscpData crash-safety rule only; it never authorizes removing source asset files from the pretreated ZIP/folder.

**Anchors in skill files:** `SKILL.md` Mandatory Output Contract (L-18 rule summary — three bullets); `references/verification-gate.md` SV-12 (inventory parity check).

**Evidence:** 068 Codex audit §M-19 was the only operation strictly classified MISSING — mechanical `index.ts:57-84, 101-117, 139-162` strips single top-level folder + preserves all non-mutated entries, current skill has no explicit rule. 069 lands it as L-18.

---

## L-19 — Never Inline Webflow's Runtime (`js/webflow.js`) — External Src Reference Preserved (NARROWED 2026-04-18 EXP-008)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Finding:** Webflow exports contain a local `js/webflow.js` file (the Webflow runtime engine — IX2/IX3 engine, module registry, animation utilities). Pre-071 SKILL.md instructed the skill to INLINE this file's content into `fb-scripts`. When the pre-treated content was pasted into Webflow Designer and published, Webflow's publisher *also* injected its own current-version CDN runtime bundle (`webflow.[hash].js`). The two versions were different builds with incompatible module registry signatures (MNZ: `{1361:...}`, published CDN: `{487:...}`). The CDN runtime called `window.Webflow.define` on the inline version's implementation; the argument protocol differed between versions → `TypeError: t is not a function` at runtime. IX2 initialization crashed. Menus, scroll animations, and all Webflow interactions failed.

**Evidence:** `audit/2026-04-18-mnz-paste-071/14-console-log.txt` lines 8–22 (jQuery.Deferred exception + Uncaught TypeError); `11-skill-export-index.html` line 3476 (inline IIFE, modules `{1361:...}`); `13-published-page.html` line 1457:69337 (`r.define` from inline version); CDN fetch `webflow.7fdf50bc.1d5fbd5ff04e4f5b.js` first 300 chars (modules `{487:...}`).

**Rule (narrowed 2026-04-18 EXP-008):** When pre-treating a Webflow export:

1. **NEVER INLINE** `js/webflow.js` module content into `index.html`. The 071 crash mechanism is an inline IIFE — the module registry runs at parse time and registers its `Webflow.define` against the global before the publisher's CDN runtime arrives. Inlining is forbidden.
2. **PRESERVE the external `<script src="js/webflow.js"></script>` reference verbatim.** It sits inside the late `fb-runtime.w-embed` host per L-15A, after all source-content siblings have parsed. Exactly one external reference — no duplicates, no strip.
3. **No `index-local.html` sibling is emitted.** `index.html` is the single HTML deliverable for both paste and local preview.
4. The `js/webflow.js` file itself is preserved byte-identical in the output ZIP (L-18 asset preservation).

**Why narrow, not broad strip:** the 071 crash was caused by inline module content running at parse time, not by an external `<script src>` tag. An external reference loads asynchronously and is subject to the publisher's paste/publish pipeline — which may deduplicate Webflow-asset paths, allow the CDN runtime to register first, or otherwise prevent the double-load collision. EXP-008 on 2026-04-18 is the decisive paste+publish measurement for this narrowing. If EXP-008 FAILS (runtime crash reproduces with external src), L-19 reverts to broad strip and the local-preview axis becomes a structural redesign problem.

**Clarification of prior error:** `js/webflow.js` contains the IX2/IX3 runtime ENGINE, not the IX2/IX3 animation DATA. The data (animation configs, keyframe defs) lives in inline `Webflow.push(...)` init scripts in the export body. Those init scripts must be preserved and wrapped with the L-16 multi-dep runner (gating on `Webflow` global). Preserving the external reference restores the runtime engine in local preview without reintroducing the inline-IIFE crash.

**Detection heuristic:** `<script src="js/webflow.js">` — a relative-path `<script src>` ending in `webflow.js` with no `https://` prefix. Path-based; no content inspection needed. Verify exactly ONE such reference exists in late `fb-runtime.w-embed`, and zero inline `<script>` blocks contain the module IIFE signature (`(()=>{var e={1361:` or equivalent). See SV-13 in `references/verification-gate.md` for the rewritten gate spec.

**Sync surface (narrowed):** `SKILL.md` Hard Rule #1, §Target Structure, §Mandatory Output Contract, §Verification Checklist; `references/lessons.md` script-handling table row + L-19 addendum; `references/decision-patterns.md` §Script Emission Policy; `references/verification-gate.md` SV-13 (rewritten: grep count 1), SV-12 (carve-out removed), SV-9 (phrasing updated), SV-16 (retired); `references/webflow-constraints.md` §"Preserve webflow.js as an external src reference" (added 2026-04-18 after Phase 1 SV-7 STOP — previously undeclared, caught the third contradiction); `docs/LESSONS.md` L-19 (this entry), L-15 body line ~272 + SV-9-D line ~277 (L-15 cross-references to L-19; added 2026-04-18 after Phase 1 SV-7 STOP).

**L-19 addendum — local-preview posture under narrowing (2026-04-18 EXP-008):** with the external webflow.js reference preserved, `index.html` carries the Webflow runtime engine when opened locally over HTTP. IX2 reveals fire, Splide hydrates, `window.Webflow` is defined, menu transforms resolve — all without emitting a separate `index-local.html` sibling. Runtime smoke tests and structural paste checks target the same file. The 077/079 tradeoff posture (paste-artifact runtime-free + optional index-local preview sibling) is superseded by this narrowing, pending EXP-008 confirmation.

**EXP-008 outcome annotation (2026-04-18 audit-082 / audit-083 / EXP-009):** Provisional. EXP-008 (session 081) reached 17/17 SV structural PASS but audit-082 (file-URL browser audit) caught runtime FAIL on three gates — section 04 opacity, menu height, footer transform. Audit-083 (2026-04-18) isolated the cause: L-15's uniform script wrapping placed `js/webflow.js` inside early `fb-scripts` inside the first `fb-custom-code`, before source-content children parse. L-19's external-ref preservation rule is correct in substance but was placement-incomplete. EXP-009 lands L-15A (runtime late placement) + SV-13-B to re-establish runtime parity without reintroducing the 071 inline-IIFE crash mechanism.

**L-19 placement scope-note (2026-04-18 EXP-009):** L-19 above (steps 1–4) correctly forbids inline Webflow runtime content and preserves exactly one external `<script src="js/webflow.js">` reference, but its placement requirement was incomplete. The external reference must execute AFTER all `.fb-page-wrapper` source-content children parse — otherwise IX2 hydrates against an empty DOM. See L-15A (2026-04-18) for the three-class partition and the `fb-runtime.w-embed` late host shape. SV-13-B in `references/verification-gate.md` enforces the late-placement structurally. This note narrows the placement rule; it does NOT change the inline-content prohibition (never inline the module IIFE) or the exactly-one-external-reference rule.

---

## L-20: Fixture Premise Verification Before Adding a New Skill Rule
**Maturity:** YOUNG (recent or narrow-scenario rule; keep explicit evidence requirements until another scenario exercises it.)

**Classification:** AUTHORING-PROCESS

**The bug this prevents:** Adding a skill rule to fix a failure mode that does not exist in any known fixture. Session 077 added Hard Rule #3 / L-1 step 8 (cross-source `@font-face` dedup pass) based on the premise that MNZ had `@font-face` in both `css/[sitename].webflow.css` AND a HEAD `<style>` preload block. Executing the rule during Op 9 revealed: raw MNZ `index.html` HEAD has **0** `@font-face` blocks. The assumed failure mode does not exist. The rule was reverted (Option C, session 077 / 078).

**The rule:** Before adding any new skill mutation to fix an observed failure, verify the failure mode is present in at least one known fixture by inspecting the raw fixture ZIP directly. Do not implement a fix for a hypothesis — confirm the evidence first.

**Verification procedure:**
1. State the assumed root cause as a testable condition: "fixture X has `@font-face` in BOTH site CSS AND raw HEAD `<style>`."
2. Run the check: `unzip -p fixture.zip '*/index.html' | grep -c '@font-face'` and `unzip -p fixture.zip '*/css/*.webflow.css' | grep -c '@font-face'`.
3. If the fixture does NOT exhibit the failure mode: reclassify the observed count/value difference by its true origin (`W-origin`, `C-origin`, etc.) and add a DEF item if a fix is needed for a future fixture. Do NOT implement a skill rule.
4. Only if the failure mode IS confirmed in the fixture: proceed with rule design, bounded to that specific failure pattern.

**Evidence:** Session 077 / 078 investigation. MNZ site CSS: 10 `@font-face` (5 unique × 2 L-14 format-variant pairs). MNZ raw HEAD: 0 `@font-face`. "11 vs 6" discrepancy = W-origin (Webflow publisher canonicalization + webflow-icons CDN), not S-origin. Rule reverted.

**Sync surface:** `SKILL.md` §Before You Run (experiment discipline gate requires hypothesis verification); `references/lessons.md` §Pointer Index (L-20).

---

## L-21: Output Manifest Self-Attestation Contract (2026-04-19, EXP-010; output-mode manifest extended 2026-04-20)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** VERIFICATION-ONLY

**Why this exists:** Sessions before EXP-010 produced artifacts where the skill returned "done" but had silently skipped mid-pipeline transformations (L-1 step 4, L-5, L-16, L-17). Post-hoc SV caught the gaps but only after the artifact was already on disk and trusted. The failure class is "Claude declares completion without structural proof of completion." This recurs on every site because the skill's reasoning is non-deterministic and post-hoc verification is too late to prevent shipping a bad artifact.

**Rule:** The skill cannot finalize an output artifact (cannot zip) without first producing `pretreat-manifest.json` beside `index.html` and a `MANIFEST.md` at `output/{lane}_{source-slug}-file_output/MANIFEST.md` containing one row per L-rule that touches the artifact. `pretreat-manifest.json` declares `schema`, `outputMode`, `animationClaim`, `probesRun`, and explicit `contractChecks[]`. Each `MANIFEST.md` row carries a live check command, its captured output, and a PASS/FAIL verdict. If any row is FAIL or any `pretreat-manifest.json` contract check is FAIL, the skill writes `HALT-REPORT.md` instead of zipping and stops.

**Output-mode addendum (2026-04-23):** output mode is itself a hard contract input, not a convenience default. Every run must declare exactly one mode. An ambiguous request such as "fresh ZIP" or "current-skill ZIP" is not enough. If the downstream target is `minimal-converter-4-1.html`, Webflow Designer paste, or live Webflow verification, the run must declare `webflow-paste`; `local-preview` is reserved for explicit preview-only / runtime-diagnostic output or another explicitly declared runtime-aware downstream lane. `paste_contract_probe.py` must receive `--mode` explicitly; missing or stale mode declarations halt the run instead of silently defaulting to `local-preview`.

**Self-attestation:** the manifests are generated by running mechanical structural checks against the artifact the skill just produced. The checks are deterministic (grep, parsed-DOM assertion, file diff, `paste_contract_probe.py`) — they cannot be hand-waved by Claude. The skill's reasoning produces the artifact; the manifest checks attest that the reasoning's output meets each L-rule and output-mode contract.

**Aspirational rules are a regression risk.** Any L-rule documented in `references/lessons.md` or `docs/LESSONS.md` that touches the artifact MUST have a corresponding manifest row in SKILL.md's manifest inventory. If a rule exists without a row, SV-7 fires (rules disagree with themselves about what completion means). Either patch the L-rule to include a structural check, or mark the L-rule as informational-only.

**Sync surface:** `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (manifest spec + Manifest row inventory + Informational/superseded list + Procedure for the skill); `AI_OS/SKILLS/webflow-pretreat/scripts/paste_contract_probe.py` (SV-18 machine probe + `pretreat-manifest.json` writer); `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` (SV-7 Extension fires on missing rows; SV-18 cross-references the output-mode manifest); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (L-21 entry + pointer); `AI_OS/SKILLS/webflow-pretreat/references/decision-patterns.md` (final-phase pointer); `docs/LESSONS.md` (this entry, canonical); `docs/EXPERIMENTS.md` EXP-010 row + KF-8.

**What this does not do:** L-21 does not extract Claude's transformation reasoning to mechanical scripts. Claude still does the work. L-21 only requires that Claude prove the work happened structurally before declaring done. Adaptive reasoning across sites is preserved.

**Evidence:** EXP-010 (session 086, 2026-04-19) lands this contract. Predecessors: EXP-009 (session 085) landed L-15A runtime late placement but did not address the truncated-execution failure class; truncated-execution symptoms had accumulated across L-1 step 4 (url() rewrites skipped), L-5 (lazy-video markers missing), L-16 (dep-gate runner omitted on multi-global inits), L-17 (library host missing). Manifest contract is the structural fix.

---

## L-22: Wrapper Impact Boundary + Component-Local Fidelity Preservation (KEEP; introduced 2026-04-19)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** The pre-treatment skill inserts or normalizes a single root wrapper so the converter receives one body child. That can legitimately change CSS behavior only through a bounded set of browser mechanisms: inherited values from `body` / `html`; containing blocks for positioned elements and percentage dimensions/offsets; scroll containers and sticky positioning through `overflow`; stacking contexts and z-index sibling relationships; selector topology such as `body > *` or sibling selectors; and `height: 100%` ancestor chains.

**Rule:** Before wrapper assembly, build a source fidelity inventory for media and hover/mouse interaction components. After wrapper assembly, every inventoried detail that is not classified as wrapper-affected must remain source-faithful. This includes:

- media nodes and asset refs: `<img>`, `<picture>`, `<video>`, `<source>`, CSS `background-image` containers, `src`, `srcset`, `sizes`, `poster`, inline `style`, local `url(...)` refs;
- fit/crop and box declarations: `object-fit`, `object-position`, `background-size`, `background-position`, `width`, `height`, `aspect-ratio`, `overflow`;
- component animation declarations: `transform`, `transition`, `opacity`, `filter`, `clip-path`;
- interaction wiring: `data-w-id`, source class chains, inline event attributes, `:hover` selectors, and retained script bodies/selectors using `mouseenter`, `mouseleave`, `mouseover`, `mouseout`, `mousemove`, `hover`, `pointer*`, or jQuery/DOM event binding.

**Compensation boundary:** If the wrapper changes a containing block or percentage-height chain, compensate the ancestor relationship. Do not "fix" the symptom by rewriting the media element's fit/crop declarations. For example, if an image originally had `width: 100%; height: 100%; object-fit: cover`, and its parent box is still meant to be the same size, those declarations must stay the same. A failed hover image animation is not explained by wrapper insertion unless the source hover/mouse script target, selector readiness, `data-w-id`, or containing block was actually changed and documented.

**Why this exists:** Maria observed a hover image regression where the image no longer filled its container (`cover`/100% fit drift) and the mouse-hover animation stopped working. Wrapper insertion can explain positioning, reveal footers, sticky sections, z-index, and percentage-height chains. It does not justify careless recreation of component-local media/hover details. The skill must first map exact source behavior, then alter only the subset affected by wrapper insertion or another declared L-rule.

**Research basis:** MDN documents that containing blocks affect positioned element offsets and percentage dimensions; `position: fixed` normally uses the viewport unless transformed/filter/perspective ancestors establish a containing block; `overflow: hidden/auto/scroll` creates scroll-container behavior while `overflow: clip` does not; stacking contexts are created by properties such as opacity, transform, positioned z-index, containment, and related triggers; `object-fit` controls how replaced content such as images/videos fills its own content box. These mechanisms define the wrapper impact boundary. They do not authorize changing unrelated `object-fit`, `background-size`, hover event wiring, or asset refs.

**Verification:** Add an L-22 manifest row. Compare source vs output component-fidelity fingerprints for every processed page after ignoring inserted `fb-*` hosts and the wrapper boundary. Assert zero unexplained deltas for inventoried media/hover components. Any delta must cite the exact L-rule row that intentionally changed it (for example L-5 lazy video `src`, L-7 overlay neutralization, L-8 narrow IX2 edit, L-16 script readiness wrapping, or L-18 deterministic asset-reference repair). Uncited deltas are FAIL.

**Sync surface:** `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (source mapping inventory, verification checklist, manifest row L-22); `AI_OS/SKILLS/webflow-pretreat/references/decision-patterns.md` (wrapper impact boundary and self-check); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (skill-local L-22); `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` (SV-17); `docs/LESSONS.md` (this entry, canonical).

---

## L-23: Responsive-Unit / Viewport-Runtime Diagnostic Boundary (KEEP; introduced 2026-04-21)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** ARTIFACT-TOUCHING

**Pattern:** A published conversion can look like it has "smaller fonts" even when the relevant CSS font-size declarations are identical to the original. Webflow exports often use a root fluid-typography cascade such as `html { font-size: 1.125rem; }` plus `@media` overrides with `calc(...rem + ...vw)`. Because `rem` inside the `calc()` resolves against the browser default root size, the computed `html` font-size is viewport-width driven; viewing the converted site in a narrower tab, iframe, Designer canvas, or published preview makes every rem-based text element shrink proportionally. Separately, sections using `height: 100vh` can differ by the exact fixed-nav height when the original and converted tabs have different `window.innerHeight`, dynamic toolbar state, or IX/Lenis runtime initialization state. Missing `w-mod-ix` is a runtime/interaction signal, not proof that a font-size rule changed.

**Rule:** Do not "fix" perceived small text or full-height section drift by rewriting source responsive units. Preserve source-authored fluid typography and viewport-height CSS unless a declared L-rule names a specific mutation.

1. **Fluid typography stays source-faithful.** Root-level `html`, `:root`, and `body` typography cascades remain governed by L-2.1: keep the unconditional rule and matching `@media` overrides together, in source order, and do not add a new clamp/floor unless the source already had one or Maria explicitly chooses a design mutation outside parity work.
2. **No synthetic Webflow default typography.** L-4 may inject the minimum geometry/tag/native-component baseline, but it must not add `body { font-family: Arial; font-size: 14px; line-height: 20px; color: #333; }` or any subset of those typography/color defaults when source typography exists. This applies even if a later source rule overrides the default; the extra rule is a hidden inheritance surface and a false lead in audits.
3. **Viewport-height CSS stays source-faithful.** Source declarations such as `.section-main.full-height { height: 100vh; }` must not be rewritten to `100svh`, `100dvh`, or `calc(100vh - nav)` during pre-treatment or conversion unless the source already expresses that relationship or a separate rule/explicit user instruction declares a design mutation. A 49-56px mismatch that equals the fixed nav height is diagnostic evidence to classify, not automatic permission to mutate CSS.
4. **Runtime marker evidence precedes fixes.** When the original has `w-mod-ix` / `w-mod-ix3` and the converted/published artifact does not, classify animation/initial-state effects under the runtime/IX lane (L-8/L-9/L-15/L-16/L-19 and future interaction conversion), not as a font-size correction. Missing IX may explain first-frame transforms, opacity, menu state, or measured section geometry, but it does not justify changing the root font-size cascade.
5. **Published-vs-original reports must capture context.** Before assigning a small-font or section-height failure to the skill or converter, record `window.innerWidth`, `window.innerHeight`, computed `html.fontSize`, representative text computed `fontSize`/`lineHeight`, `100vh`/`100svh` computed values, fixed nav height, `document.documentElement.className`, and `w-mod-ix` / `w-mod-ix3` presence for both original and converted targets. Then assign the primary origin label: `S-origin`, `C-origin`, `W-origin`, or `E-origin`.

**Verification:** Add an L-23 manifest row for every output that touches CSS routing or baseline injection. Compare source CSS against converter-visible output CSS after expected routing:

- root fluid typography declarations (`html`, `:root`, `body` font-size cascades) are present in the L-2.1-approved location and not duplicated later in a way that inverts the cascade;
- no synthetic Webflow default body typography/color declaration exists unless the source lacked text rules and the manifest names that premise;
- source `height: 100vh` / `min-height: 100vh` declarations on site selectors are preserved byte-for-byte except for normal formatting/longhand serialization, with no unapproved `svh`/`dvh`/nav-subtraction rewrite;
- any reported published section-height or font-size mismatch includes the viewport/runtime evidence listed above before proposing a mutation.

**Failure mode this prevents:** Repeated audits misclassify a responsive-unit illusion as a broken `.text-regular` font-size rule, then propose changing source fluid typography or viewport-height CSS in the skill/converter. The real failures are usually (a) viewport/context mismatch, (b) an injected default body typography rule that should never have existed, or (c) missing IX/runtime initialization. L-23 keeps those lanes separated.

**Sync surface:** `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (verification checklist + manifest row L-23); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (skill-local L-23); `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` (SV-8 typography-default check + SV-P6 viewport/runtime evidence); `docs/LESSON_INDEX.md` (L-23 row); `docs/LESSONS.md` (this entry, canonical).

---

## L-24: Webflow Designer Crash-Hazard Pre-Paste Blacklist (KEEP; introduced 2026-04-21 from Flowbridge-rebuild-clean)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** VERIFICATION-ONLY

**Pattern:** The old `Flowbridge-rebuild-clean` repo already discovered a class of payload shapes that can crash Webflow Designer or make paste unusable before visual QA even begins. Those lessons were scattered across old AGENTS notes, clipboard-spec tables, extractor comments, and QA indexes. The current project must carry them as one explicit pre-paste blacklist, with ownership split by artifact stage:

- pre-treatment owns the HTML/body-embed surfaces it can emit;
- the converter owns `@webflow/XscpData` clipboard surfaces;
- paste-side verification owns the final "this JSON is safe to put on the clipboard" evidence.

**Rule:** Never offer direct paste / direct copy for an artifact that contains any known Designer crash hazard. The blacklist is additive; absence of one hazard is not evidence the payload is safe if another hazard remains.

1. `@font-face` inside any body embed / HtmlEmbed payload is forbidden. `@font-face` belongs only in the pre-treated HTML HEAD inline style per L-1. In the clipboard payload, HtmlEmbed `meta.html` must not contain `@font-face`.
2. `payload.assets[]` must stay empty. Images are uploaded and relinked before paste; clipboard asset injection is a known crash surface. This rule applies to XscpData only and does not change L-18: source image/font/media/document files must still exist in the pretreated ZIP and extracted output folder.
3. `animation-play-state` must not appear in generated `styleLess` or style variants. The old clean repo found this property unsafe in nth-child / variant contexts; preserve source CSS for preview, but do not serialize it as a Webflow style record.
4. Generated style variant keys must not use the old crashing pseudo-state names `main_pressed` or `main_focused`. If a future state serializer exists, it must use a Webflow-safe representation proven by paste evidence.
5. A single style must not combine multiple pseudo-state variant types such as hover + focus/pressed/visited. The old clean repo proved multiple pseudo-state types in one style can crash Designer.
6. A single style must not contain more than one nth-child variant whose `styleLess` uses `@raw<|...|>` values.
7. IX2 action items must not carry raw `selector` / `selectorGuids` targeting into clipboard interaction data. The safe pattern from the old repo converted selector targeting to Webflow element/class references before paste.
8. HtmlEmbed `meta.html` must be a string, not an object or structured node. Malformed embed metadata makes the clipboard payload unsafe.
9. Direct copy is disabled when local image references remain in Image nodes (`src`, `srcset`, lazy-load attrs), CSS, or HtmlEmbed URLs after the upload/relink step, or when a hosted Image `src` lacks the matching Webflow `data.img.id` binding. A diagnostic JSON download may still be allowed, but not clipboard paste. The safety scanner must stay URL-aware: absolute hosted image URLs are not local failures, even when encoded filenames contain spaces, parentheses, or other punctuation that can otherwise produce local-looking suffix fragments such as `%201.avif`.

**Verification:** L-24 is a verification-only consolidation rule because the actual mutations are owned by existing stage-specific rules: L-1 owns font placement, L-8 owns IX state cleanup, L-18 owns asset preservation/upload premises, and the converter owns XscpData serialization. The required evidence is:

- pre-treatment manifest/checklist cites the HTML-side subset: zero `@font-face` in body embeds and no converter-visible style host intentionally carrying `animation-play-state` into paste-bound style extraction;
- converter invariant probe reports the `designer-crash-hazards` and `static-image-asset-binding` checks as PASS for any XscpData offered for direct copy: `python3 scripts/converter_invariant_probe.py <xscpdata.json>`;
- direct-copy UI remains disabled when the probe or safety gate reports these hazards. JSON download remains diagnostic-only and must not be described as paste-ready.

**Failure mode this prevents:** Maria pasted a current converter output into Webflow Designer and got Webflow's "Something went wrong" crash dialog. Re-reading `Flowbridge-rebuild-clean` showed those crashes had already been learned: `@font-face` in HtmlEmbed, `payload.assets[]`, unsafe pseudo variant keys/combinations, `animation-play-state` in styleLess/variants, nth-child `@raw` variant combinations, and IX2 `selector` / `selectorGuids` were all known no-go surfaces. L-24 exists so that history is not left in the old repo or in chat memory.

**Evidence carried forward:** `../Flowbridge-rebuild-clean/src/lib/AGENTS.md` crash/fail rules; `../Flowbridge-rebuild-clean/docs/architecture/WEBFLOW-CLIPBOARD-SPEC.md` crash table; `../Flowbridge-rebuild-clean/docs/qa/2026-04-11-reference-paste-test-results-index.md` highest-risk findings; `../Flowbridge-rebuild-clean/src/lib/css-extractor.ts` `animation-play-state` guard; `../Flowbridge-rebuild-clean/src/lib/ix2-extractor.ts` selector/selectorGuids conversion.

**Sync surface:** `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (Hard Rules, verification checklist, manifest row L-24); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (skill-local L-24); `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` (SV-18/SV-P1 L-24 evidence); `docs/LESSON_INDEX.md` (L-24 row); `scripts/converter_invariant_probe.py` (`designer-crash-hazards` and `static-image-asset-binding` invariants); `minimal-converter-4-1.html` (direct-copy safety gate).

---

## L-25: Scoped-interaction fix discipline (KEEP — anti-lesson; introduced 2026-04-21 from Flowbridge-rebuild-clean)
**Maturity:** MATURE (carried forward across repeated project lessons, fixture audits, and current skill gate surfaces; retain unless a future fixture or paste-side probe contradicts it.)

**Classification:** AUTHORING-PROCESS

**Pattern:** An interaction pair type (for example Topic-Hover) is failing in a fixture. The operator identifies the broken interaction, writes a dual-timeline fix (or a selector rewrite, or a timeline retune), and applies it at a selector scope broader than the pair type that was actually broken. The broader scope sweeps up unrelated interaction pair types that were already working, and the commit ships a lateral-move regression: the originally-broken pair now works, but a previously-working pair (color-wipe, image-reveal, text-reveal, etc.) is silently destroyed. Regression is only discovered on paste test or post-publish QA — after the fix has been shipped and the scoped evidence is already contaminated.

**Origin / evidence:** `Flowbridge-rebuild-clean` session 2026-03-10, Prompt 042. A Topic-Hover dual-timeline fix was applied at a global selector scope instead of scoping to the Topic-Hover pair-type selector only. Consequence: the fix landed, Topic-Hover worked, and the repo's color-wipe interactions — which had no relationship to Topic-Hover — stopped working. Classic lateral-move regression. The behavioural principle existed in CLAUDE.md Key Rule 3 (scope discipline) and Rule 18 (origin-classify before fixing), but the interaction-specific application pattern was not encoded as an L-rule and so was rediscoverable on every future interaction session.

**Rule:** Interaction / selector / timeline fixes apply to the specific interaction pair type only, scoped by the minimum selector that uniquely identifies that pair. Before committing any interaction fix:

1. Name the exact interaction pair type you are fixing (for example Topic-Hover, color-wipe, image-reveal), and the minimum selector that identifies only that pair's elements in the fixture.
2. Verify the fix's selector does not match elements belonging to any OTHER interaction pair type in the same fixture. If the selector is broader than the failing pair type, narrow it — do not widen the fix to "handle more cases."
3. Re-run every paste parity anchor for OTHER interaction pair types in the same fixture after the fix lands. Read the current Protected Set declared in the session prompt's Baseline Capture Gate; re-run the SV rows that cover non-target interactions. Zero newly-failing parity anchors is the bar.
4. If the scoped fix cannot be expressed without touching a broader selector (the only working patch requires mutating shared interaction infrastructure), STOP. This is not a surgical fix — it is a structural change. Escalate under the 2-strike rule (`~/.claude/rules/escalation.md`) and require explicit user decision before proceeding.

**Failure-mode example (from the origin incident):** Fixing Topic-Hover's missing second timeline by editing the shared IX2 timeline entrypoint — instead of scoping the fix to the Topic-Hover interaction's `data-w-id` pair or its unique class chain. The shared entrypoint is executed by every pair type. Editing it changed color-wipe's first-keyframe resolution, and color-wipe stopped wiping. The lateral-move was invisible in the Topic-Hover verification screenshot, because color-wipe lived in a different section.

**Classification rationale:** L-25 is a process / anti-lesson rule. It has no artifact surface of its own — the skill does not emit a specific HTML/CSS structure to satisfy L-25, and there is no pretreat-manifest row that "checks" L-25 the way L-11 or L-22 check physical output. Instead, L-25 is enforced upstream by the Regression Protocol's Protected Set check (`docs/governance/REGRESSION-PROTOCOL.md` step 13 — zero-tolerance lateral-move rejection) and by the Baseline Capture Gate declared in `SKILL.md` → Before You Run. Compliance evidence lives in the session's `## Regression Report` block, not in a manifest row.

**Relationship to other rules:** L-25 is a concretization of CLAUDE.md Key Rule 3 (scope discipline: modify only what the task requires) and Key Rule 18 (origin-classify before designing a fix). It is upstream of any future interaction-touching L-rule — when an L-rule is authored that mutates interaction CSS, IX state, timeline shape, or event wiring, the authoring session MUST cite L-25 as a constraint and declare the scoped selector boundary in the rule body.

**Evidence carried forward:** `../Flowbridge-rebuild-clean/` session log 2026-03-10 Prompt 042 (Topic-Hover dual-timeline fix → color-wipe regression); CLAUDE.md Key Rule 3 and Key Rule 18; `~/.claude/rules/escalation.md` 2-strike rule; `docs/governance/REGRESSION-PROTOCOL.md` zero-tolerance Protected Set check.

**Sync surface:** `docs/LESSON_INDEX.md` (L-25 row, process/anti-lesson classification); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (skill-local L-25 pointer); `docs/governance/REGRESSION-PROTOCOL.md` (Protected Set check enforces compliance); `docs/LESSONS.md` (this entry, canonical). No `SKILL.md` manifest row — this is a process rule without artifact surface; enforcement is via the Regression Report block in session result files.

---

## L-27 — CMS Template Stub Detection and Passthrough
**Maturity:** YOUNG (recent or narrow-scenario rule; keep explicit evidence requirements until another scenario exercises it.)

**Date added:** 2026-04-22
**Origin:** srta-colombia first skill run (session 187) + gap-fix loop iteration 4 (session 192)
**Classification:** ARTIFACT-TOUCHING

**Rule:** When a source HTML page's `<body>` contains zero content-bearing elements — only `<script>`, `<style>`, `<link>`, `<meta>`, `<title>`, `<!--comments-->`, and whitespace text nodes — classify the file as a **CMS template stub** and pass it through the output ZIP byte-for-byte. Do NOT apply pre-treatment: no `fb-page-wrapper` creation, no embed host restructuring, no script splitting, no CSS inlining. Record the passthrough in `MANIFEST.md` and `pretreat-manifest.json`.

**Detection algorithm:**

```
For each source HTML file:
  body = parse <body> element
  content_elements = body.find_all(element for element in body.children
                                    if element is tag
                                    and element.name NOT IN {"script", "style", "link", "meta", "title"})
  script_children = body.find_all("script", recursive=False)
  if len(content_elements) == 0 AND len(script_children) > 0:
      classify as CMS template stub → passthrough
  else:
      apply full pre-treatment
```

A body with `<p>Hello</p>` is NOT a stub (has a content element). A body with only `<script>` tags IS a stub. A truly empty body (no children at all) is out-of-scope for this rule — treat as malformed export and halt with report.

**Rationale:** Webflow CMS Collection detail pages ship as template skeletons in the static export. Their visible content is hydrated at publish time by Webflow's runtime from CMS Collection data. The static export file contains only `<script>` bootstrappers that the CMS runtime consumes. Applying pre-treatment creates a `fb-page-wrapper` with only `fb-custom-code` + `fb-runtime` direct children — no source-content sibling between them — which fails L-13's structural invariant. Passthrough is faithful to the export's intent: the file's content is not static, the converter/paste pipeline wouldn't do anything meaningful with it, and preserving the bytes lets the user make their own downstream decision.

**Scope:**

- L-27 applies to pages with script-only bodies. Bodies with any content element get regular pre-treatment.
- Scripts inside a stub are NOT L-15 wrapped, NOT L-16 dep-gated — because the file is not processed at all. Their relative script references (`js/webflow.js` etc.) resolve against the output root only if L-18 asset preservation copies those assets (which it does by default).
- L-27 stubs do NOT count as "processed HTML files" for L-15A (`fb-runtime` host count), L-13 (wrapper content siblings), L-12 (embed host placement), or any other structural manifest row that assumes pre-treated target structure.
- Mode A/B runtime-presence probe rows exclude L-27 stubs symmetrically. A byte-passthrough stub may keep its source-position `js/webflow.js` reference without failing processed-page runtime checks.
- L-4 / L-1 / L-17 / L-16 / L-15 / L-15A / L-13 / L-12 / L-11 / L-2 / L-2.1 all receive a "processed HTML only" scope by implication — CMS stubs bypass them.
- L-18 (asset preservation) still applies: non-processed files are copied byte-for-byte as part of the general asset copy step.
- L-20 (fixture premise verification before adding a rule) was applied — the premise ("CMS template detail pages in Webflow exports have script-only bodies") is verified in srta-colombia `detail_comunicado-de-prensa.html`.

**Failure mode this prevents:** A Webflow export with one or more CMS Collection detail page templates would halt the skill on L-13 failure ("no content siblings under `fb-page-wrapper`"), even though the export is valid and the file's content is publish-time hydrated, not statically missing. The halt is a false positive — the file isn't broken, the skill just had no rule for this anatomy. L-27 gives the skill the rule.

**Counter-rule guard:** L-27 detection must be strict. A page with even one content element (e.g. a lone `<div>` placeholder) is pre-treated normally. A truly empty body (zero children of any kind) is NOT a stub — it's a malformed export and should halt with a diagnostic report, not silently passthrough. The detection rule depends on the presence of at least one `<script>` child to prove the body is a CMS template skeleton, not broken HTML.

**Sync surface:** `docs/LESSON_INDEX.md` (L-27 row); `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (Workflow step 5 pointer + Mandatory Output Manifest L-27 row + L-13 scope-carve-out note); `AI_OS/SKILLS/webflow-pretreat/scripts/paste_contract_probe.py` (Mode A/B runtime-presence rows exclude L-27 stubs symmetrically when counting `js/webflow.js` references on processed pages). No `references/*.md` edit — this is a new rule whose primary surface is the skill's Workflow, not a reference doc.

---

## L-28 — CMS Template-Page Link Role Tagging
**Maturity:** YOUNG (recent or narrow-scenario rule; keep explicit evidence requirements until another scenario exercises it.)

**Date added:** 2026-04-23
**Origin:** srta-colombia paste test after handoff 249 (Dynamo transform shipped, purple wrappers render, but `about-link` pastes as `href="#"` URL instead of "Page → Current Candidatas 2025"); research 250 (`AI_OS/SESSION-PROMPTS/SESSIONS/2026-04-23/250-research-cms-link-page-binding.md`) confirmed W-origin cross-site binding strip is deliberate Webflow behavior.
**Classification:** ARTIFACT-TOUCHING

**Rule:** In every processed HTML page, for every `<a>` whose nearest ancestor carries the class `w-dyn-item` AND whose `href` passes the filter below: set the attribute `data-fb-link-role="template-page"` and mark the touched `<a>` with `data-flowbridge-link-role-tagged="true"` for L-6 idempotence. Do NOT modify the anchor's `href`, classes, text content, or any other existing attribute. Do NOT alter anchors outside the `w-dyn-item` ancestor scope. Do NOT change XscpData shape — the attribute travels via the converter's existing `xattr` preservation path, which already preserves `data-*` attributes unchanged.

**Detection algorithm:**

```
For each processed HTML page:
  For each <a> element in the document:
    ancestor = a.find_parent(class_="w-dyn-item")
    if ancestor is None:
      skip
    href = (a.get("href") or "").strip()
    if href.startswith(("http://", "https://", "//", "mailto:", "tel:", "javascript:")):
      skip
    if href.startswith("#") and len(href) > 1:
      skip  # intra-page fragment to a specific id — legitimate URL link
    if a.get("data-flowbridge-link-role-tagged") == "true":
      skip  # already tagged; L-6 idempotence
    a["data-fb-link-role"] = "template-page"
    a["data-flowbridge-link-role-tagged"] = "true"
```

An anchor with empty `href`, `href="#"`, `href="./"`, `href="./{path}"`, or slug-pattern `href="/{slug}/{slug}"` passes the filter and gets tagged. The filter is allow-by-default for anchors inside `w-dyn-item`: any href that is not an absolute URL, non-HTTP scheme, or fragment-id anchor is treated as a template-page binding candidate. This is safe because Webflow's export is lossy — the pre-treatment skill cannot distinguish a "Page → Collection Template Page" binding from a lossy `#` placeholder by href content alone, and the structural position (anchor inside `w-dyn-item`) is the only reliable universal signal.

**Rationale:** Webflow's export HTML is lossy with respect to CMS link bindings. An exported `<a href="#" class="about-link">` carries zero information that the intended target was "Page → Current Candidatas 2025" (or any other Collection Template Page). Webflow's clipboard paste pipeline deliberately strips page/CMS-template bindings on cross-site paste — documented in Webflow Help Center under "Copy and paste between sites" — because Collection IDs are project-specific hex values that cannot be resolved at paste time. Neither the archived `converter-playground.html` nor `minimal-converter-4-1.html` can recover this binding from the lossy HTML: both emit `link: {url: "#", target: ""}` for `<a href="#">` anchors. The fix lives one hop downstream in the MASTER-COLLECTION Designer Extension app, which uses the Designer API `linkElement.setSettings('page', templatePage, metadata)` after the user has bound the Collection List to a Collection (so the Collection Template Page exists as a `Page` object retrievable via the Pages API). The pre-treatment skill's job is to emit a universal structural signal that MASTER-COLLECTION can detect post-paste. `data-fb-link-role="template-page"` is that signal; the converter preserves it as `xattr`; Webflow paste carries it through because `data-*` attributes are retained verbatim on Elements.

**Scope:**

- L-28 applies to anchors inside Collection List items (anchors whose nearest ancestor carries class `w-dyn-item`). These are the only DOM positions where a Webflow export represents a "Page → Collection Template Page" link shape.
- Does NOT apply to static anchors outside any `w-dyn-item`, navigation menu anchors in the site chrome, or anchors whose `href` is a fully-qualified URL (`http://`, `https://`, protocol-relative `//`) or a non-HTTP scheme (`mailto:`, `tel:`, `javascript:`).
- Does NOT apply to intra-page fragment anchors such as `href="#about"` which target an in-page section by id — those are legitimate URL links and must not be retagged as template-page bindings.
- A page with zero `<a>` descendants inside any `w-dyn-item` records the transformation as "N/A — no Collection List items carrying anchors". A page with such anchors but none passing the href filter records "applied — 0 of N anchors matched filter".
- The transformation is idempotent per L-6: an anchor already carrying `data-flowbridge-link-role-tagged="true"` is not re-tagged.
- L-28 is additive only: the rule never removes, rewrites, or reorders anchors or their attributes. L-22 component-fidelity probe catches any uncited delta.

**Failure mode this prevents:** Without L-28, every Webflow template that uses Collection Template Page links (srta-colombia, MNZ Creative, big-buns, future fixtures) requires the end user to manually re-link every such anchor in the Designer Settings panel after paste. Because switching link mode from URL to Page in the freshly-pasted Settings panel crashes Webflow Designer in the zombie-paste state (observed srta-colombia 2026-04-23, W-origin Webflow Designer bug), manual re-link is not even a viable workaround. L-28 provides the universal signal that lets MASTER-COLLECTION relink programmatically via the Designer API, bypassing the Settings panel and its crash.

**Counter-rule guard:** L-28 must not overreach. The ancestor check is strict (`w-dyn-item` class only — not any dynamo-family class, not any CMS-adjacent ancestor). The href filter is exhaustive: absolute URLs, protocol-relative URLs, schemes (`mailto:`, `tel:`, `javascript:`), and fragment-id anchors with non-empty id are explicitly skipped. Tagging a nav-menu anchor or an external-URL anchor would cause MASTER-COLLECTION to attempt `setSettings('page', …)` on an anchor that has no Collection Template Page target, which would fail at relink time. The manifest row's second assertion (no `<a>` outside `w-dyn-item` carries `data-fb-link-role="template-page"`) catches this regression; SV-7's extension treats any failure there as a pre-zip HALT.

**Sync surface:** `docs/LESSON_INDEX.md` (L-28 row); `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (Per-Element Transformations L-28 entry + Mandatory Output Manifest L-28 row); `.claude/skills/webflow-pretreat/SKILL.md` and `C:/Users/maria/.claude/skills/webflow-pretreat/SKILL.md` (Claude-runtime mirrors — must stay byte-identical to AI_OS master per lesson-surface lint); `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (Codex lane Non-Negotiables pointer so the comparison lane applies the same rule). No `references/*.md` edit — this is a new rule whose primary surface is the skill's Per-Element Transformations section and Mandatory Output Manifest row, not a reference doc (same pattern as L-27). No `scripts/paste_contract_probe.py` extension required yet — the manifest row's parsed-DOM enumeration is reproducible inline; extend the probe only if a future fixture proves drift between inline check and programmatic probe.

---

## L-30 — IX Runtime Data Inlined for Converter Extraction (`webflow-paste` only)

**Date added:** 2026-04-24
**Origin:** Session 281 empirical test during 280-plan-ix-lane2-port. `scripts/ix-empirical-check.ts` against MNZ Creative and bigbuns pretreated outputs returned `ix3.interactions=0` and `ix2.interactions=0` even though both source exports ship non-trivial animation graphs. Root cause traced: the IX2 `Webflow.require("ix2").init({events:{...},actionLists:{...}})` payload for MNZ and the IX3 `getInstance();...register([...],[...])` / `.registerTimelines([...])` payloads for bigbuns both live ONLY inside `js/webflow.js` (the source webflow.js bundle contains engine + data concatenated). `minimal-converter-4-1.html`'s IX extractors (`extractIX2ExportData` at line 569 and `extractIX3ClipboardData` at line 530) scan HTML only — they never reach into the `js/webflow.js` sidecar, so the converter's `payload.ix3` stayed empty and no animations shipped into the XscpData clipboard.
**Classification:** ARTIFACT-TOUCHING
**Maturity:** YOUNG (introduced 2026-04-24; tested only on MNZ. Promote to MATURE after Srta Colombia or BigBuns confirms behavior in a fixture that ships an IX data payload.)

**Pattern:** Modern Webflow exports bundle both the IX runtime ENGINE (the module IIFE/webpack runtime) AND the page-specific IX DATA (the `Webflow.require("ix2").init({...})` call plus any `getInstance().register([...])` / `.registerTimelines([...])` calls for IX3) into a single `js/webflow.js` file. At publish time the browser runtime self-executes and reads the data. In a paste target that does NOT execute JavaScript, the IX data must be extracted from `js/webflow.js` and presented to the converter somewhere the converter's HTML-only regex extractors can see it.

This rule is the carve-out that reconciles three prior rules:

- Hard Rule #1 / L-19: "never inline `js/webflow.js` content into `index.html`." That rule targets the runtime ENGINE (module IIFE body, webpack bootstrap). Inlining the engine duplicates `window.Webflow` between source and publisher CDN and crashes with `TypeError: t is not a function`.
- L-15A: preserve the external `<script src="js/webflow.js">` reference in the mode-approved host. That reference remains.
- L-9: preserve source-shipped runtime libraries verbatim; pre-treatment does not classify by downstream convertibility. That also remains.

L-30 distinguishes the DATA from the ENGINE. Only the data — the arguments of the `.init(...)` and `.register(...)` / `.registerTimelines(...)` calls — is extracted and inlined. The engine (module IIFE, webpack bootstrap, runtime globals) is never inlined.

**Rule — pre-treatment emits an IX-data inline script in `webflow-paste` mode:**

1. **Mode gate.** This rule fires ONLY in `webflow-paste` mode. In `local-preview` mode the runtime loads `js/webflow.js` and executes the calls natively, so duplicating the data inline would cause double-registration. Do NOT emit the inline IX-data script in `local-preview`.

2. **Source scan.** Open the source export's `js/webflow.js` and locate, in order:
   - The first match of `/Webflow\.require\(["']ix2["']\)\.init\(/` — call this `ix2InitStart`.
   - The first match of `/\.getInstance\(\);?/` — record its index; from there, the first following `/\.register\(\[/` is `ix3RegisterStart` and any subsequent `/\.registerTimelines\(\[/` within the same call chain is `ix3TimelinesStart`.

   For each match found, read from the opening `(` through the matching closing `)` using balanced-bracket walking (strings and escapes respected — reuse the same algorithm `minimal-converter-4-1.html:findMatchingJsBracket` uses so the extraction is semantically identical to the converter's parser). The payload to preserve is the call statement in full: `Webflow.require("ix2").init({...});` or `window.Webflow.require("ix3").getInstance().register([...], [...]);` / `.registerTimelines([...]);` depending on what the source contains.

3. **Payload shape.** Emit the extracted call(s) verbatim inside a single `<script>` tag (no `type` attribute, executable JS). Preserve the source character sequence byte-for-byte inside the call arguments — do NOT reformat, re-indent, alphabetize keys, replace quotes, or expand minified identifiers. The call payload contains opaque IDs and object shapes the converter parses; any rewrite risks changing meaning.

4. **Placement.** The inline `<script>` is placed inside the existing `fb-scripts.w-embed` host AFTER the `<script src="js/webflow.js">` reference and AFTER any retained source inline init bodies. Source-order stays source-faithful; the inline IX data is a skill-introduced compensation, not a source element. Record its origin in the manifest.

5. **Non-inlining guarantees (L-19 carve-out).** The inline `<script>` must NOT contain:
   - The webflow.js module IIFE (no `var e={` / `var __webpack_modules__` / `!function(e){` module bootstrap).
   - Any `Webflow` constructor, plugin registration, or runtime boot code.
   - Any code outside the narrow `.init(...)` / `.register(...)` / `.registerTimelines(...)` call statements themselves.

   Assertion: `grep -c 'var e={[0-9]\+:' output/{lane}_{source-slug}-file_output/index.html` → 0. L-19 still passes.

6. **Zero-data sources.** Some exports (plain static sites, e.g. Señorita Colombia) have neither `Webflow.require("ix2").init(` nor `.register([` in their `js/webflow.js`. In that case emit nothing — the inline IX-data script is absent and the manifest row records `ixDataScript: none (source has no IX data)`. This is not a failure; it is the correct outcome for an animation-free source.

7. **No mutation of the source file.** `js/webflow.js` inside the output ZIP is NOT modified. L-9 + L-15A continue to preserve the source file and the HTML reference to it. L-30 extracts-and-duplicates the DATA; the source file stays intact.

**Why the data duplication is safe:**

- In `webflow-paste`, the HTML is consumed by a non-executing parser (`minimal-converter-4-1.html` DOMParser + regex extract). The inline `<script>` body is never run; it is only scanned for string patterns. The fact that both `js/webflow.js` and the inline script contain the same `.init(...)` call creates no runtime double-registration because the runtime never runs here.
- The same pretreated artifact never boots the Webflow runtime during paste; `fb-page-wrapper` + `fb-scripts` are passive data structures for the converter to walk.
- Webflow Designer receives XscpData built from the extracted IX data. Once pasted, Designer owns the interactions panel and the source `js/webflow.js` is dropped entirely at paste time.

**Failure mode this prevents:** Session 281 `scripts/ix-empirical-check.ts` output — MNZ returned `ix3.interactions=0 ix3.timelines=0 ix2.interactions=0` after pretreatment; same for bigbuns. Without this rule, every webflow-paste ZIP produced for any site that ships IX2 or IX3 animations results in a static clipboard paste with no interactions. Pasting such an XscpData into Webflow Designer results in a visually correct layout with zero animation panels — which is indistinguishable (to a non-expert reviewer) from a successful run and silently ships "works but dead" outputs.

**Verification gate (L-30 manifest row):**

- Source-present condition: the source ZIP's `js/webflow.js` contains at least one of `Webflow.require("ix2").init(` OR `.register([` (after `getInstance()`).
- In `webflow-paste` mode, if source-present, assert the pretreated `index.html` contains the corresponding inline call(s) and the outer `<script src="js/webflow.js">` reference:
  - `grep -c 'Webflow\.require("ix2")\.init(' output/.../index.html` → ≥ source count (typically ≥1)
  - `grep -cE '\.register\(\[' output/.../index.html` → ≥ IX3 source count
  - `grep -cE '\.registerTimelines\(\[' output/.../index.html` → ≥ IX3 timeline source count
  - `grep -c 'var e={[0-9]\+:' output/.../index.html` → 0 (L-19 engine-absence guard)
  - `grep -c 'src="js/webflow.js"' output/.../index.html` → preserved (L-15A)
- Source-absent condition: manifest row records `ixDataScript: none`; no inline IX call assertion is run. L-30 is N/A for that fixture.
- In `local-preview` mode: assert zero skill-introduced inline `Webflow.require("ix2").init(` calls in `index.html` (the mode suppression guard). The runtime reads from `js/webflow.js` itself.

**Sync surface:** `docs/LESSONS.md` (this body); `docs/LESSON_INDEX.md` (new L-30 row; rule-count bump L-1..L-30); `AI_OS/SKILLS/webflow-pretreat/SKILL.md` (Hard Rule #1 carve-out language, Mode B description, new Per-Element entry + Mandatory Output Manifest row + Before-You-Zip checklist item); `AI_OS/SKILLS/webflow-pretreat/references/lessons.md` (L-30 entry); `AI_OS/SKILLS/webflow-pretreat/references/verification-gate.md` (L-30 gate row); `.claude/skills/webflow-pretreat/SKILL.md` + `~/.claude/skills/webflow-pretreat/SKILL.md` (Claude-runtime mirrors — sync to master). Codex lane (`AI_OS/SKILLS/webflow-pretreat/SKILL.md`) gets the Non-Negotiables pointer in a separate dual-lane pass if Maria authorizes it.

**L-30/L-16 readiness note (2026-04-25):** L-30 IX data scripts may use the publish-safe Webflow queue shape `window.Webflow = window.Webflow || []; window.Webflow.push(function(){ ... });` instead of the full L-16 `need[]`/`requiredSelectors`/`fbRun` runner when the body is IX data registration only and has no DOM selector dependency. This queue is readiness-safe because it defers `Webflow.require(...)` until Webflow drains the queue. `paste_contract_probe.py` treats this shape as satisfying `mode-b-l16-readiness`; a bare top-level `Webflow.require(...)`, `Webflow.push(...)`, or `Webflow.env(...)` remains a FAIL.

---

## L-31 — Mode-B Transport Protocol for IX2-Hidden Initial States (`webflow-paste` only)

**Date added:** 2026-04-25
**Origin:** EXP-001 Stage 3 (Session 289) surfaced 7 of 8 hardcoded IX2-hidden initial-state targets as `preserved-inline` with no transport mechanism. EXP-002 (Session 290) confirmed the gap persisted after the four contradiction fixes — same 7 missing on the hardcoded MNZ catalog, only `slider2-component-root` PASSing via `component-root-fallback` in `fb-styles-splide`. EXP-004 (2026-04-25) replaced the hardcoded catalog with a structural detector (`paste_contract_probe.detect_mode_b_targets`) that scans source HTML for elements whose inline `style=""` carries a hidden-on-load declaration gated by IX-shape OR `data-w-id`. MNZ's detected target count rose from 8 hardcoded to 94 dynamic (24 unique class chains); the synthetic `.page-curtain` fixture confirmed class-name-agnosticism (94 targets, 14 `page-curtain` instances mirroring MNZ's 14 `bg-whipe`). `mode-b-initial-state-transport` FAIL count rose from 7 missing to 84 missing — broader detection coverage, same family of failure: L-8 alone preserves the inline `style=""` correctly but Webflow's paste pipeline can silently drop those attributes on overlay/hidden-on-load elements, leaving the element visible-on-load on the first paint after paste before IX2 boots and re-applies the hidden state.
**Classification:** ARTIFACT-TOUCHING
**Maturity:** MATURE (cross-scenario validated 2026-04-25 via MNZ + synthetic page-curtain: 85 targets across multiple class-chain patterns, multiple triggering signature families, collision-handling via F-1 markers, class-name-agnosticism via synthetic. Future organic fixtures with mode-b targets will reinforce; their absence does not regress maturity.)

**Pattern:** Inline `style=""` attributes preserving IX2 initial states (collapsed overlays, hidden nav children, off-screen translate quadruples, zero-scale transforms, fully-clipped clip-paths, zero-collapse sizing) survive pretreatment per L-8 but are subject to silent drop by Webflow's paste-side canonicalization. The probe rows `mode-b-initial-state-transport` and `mode-b-d007-anchor-safety` enumerate every target where the hazard is structurally detectable (post-EXP-004: `detect_mode_b_targets` walks `html.style_attrs`, applies the hidden-on-load signature filter, and emits one target dict per qualifying element with `selector`, `classes`, `required`, optional `component_fallback_host`).

**Rule:** For every element the probe detects via `detect_mode_b_targets`, in addition to preserving the inline `style=""` per L-8, the skill MUST also emit a **runtime-gated, source-class-specific CSS rule** in `fb-styles-site` (or in the appropriate `fb-styles-{library}` host when the target carries a `component_fallback_host` annotation) carrying the same canonical declarations the probe extracted into `target.required`.

**Runtime-gating selector:** prefix the L-31 selector with `html:not(.w-mod-ix2)`. Webflow's runtime adds `.w-mod-ix2` to `<html>` once IX2 boots; before that moment the L-31 rule is active (overlay correctly hidden even if Webflow paste dropped the inline `style=""`). Once IX2 is active the prefix no longer matches and the rule disengages — the cascade falls back to source CSS, and IX2's own runtime `style.setProperty(...)` calls override anything the cascade settles on for properties IX2 actively animates. For properties IX2 does not animate (the rare case where the hidden-on-load state was IX2-stamped on a descendant of a timelined ancestor but the timeline only animates other properties), the source CSS provides the post-boot value.

**Selector shape:** `html:not(.w-mod-ix2) <target.selector>` where `<target.selector>` is the source element's class-chain (e.g. `.nav-child.left`, `.img-parent.recent-post`, `.bg-whipe`, `.heading-small.newbit.btm`). This shape is chosen because (a) it is higher-specificity than any source class CSS rule on the same chain (`selector_specificity` returns `(0, K+2, 1)` vs source's `(0, K, 0)`), so `summarize_css_transport.transport_property_is_cascade_safe` returns True; (b) it is class-name-agnostic — the runtime-gate prefix is universal, the class chain comes from per-fixture detection; (c) it is invisible to the L-7 anti-broaden probe — `parse_simple_class_chain_selector` rejects any selector containing characters outside `[A-Za-z0-9._-]`, and `:` / ` ` / `(` are present in the runtime-gate prefix, so L-31 rules are never enumerated as L-7 candidates.

**Declaration shape:** copy each declaration from `target.required` (canonical CSS-shaped fragments emitted by `mode_b_required_fragments` — short forms like `transform: translate3d(-100%, 0, 0)`, `width: 0rem`, `height: 0%`, `opacity: 0`). Semicolon-delimited. **No `!important`** — specificity already wins via the runtime-gate prefix; adding `!important` would block IX2's runtime `style.setProperty` from overriding the static rule for properties IX2 actively animates.

**Idempotence (L-6):** emit one rule per unique `(target.selector, tuple(target.required))` pair. Targets that share both selector and declaration set produce a single rule; targets that share selector but differ in declarations produce separate rules.

**Library-fallback host routing:** when `target.component_fallback_host` is set (e.g. `fb-styles-splide` for `.splide.slider2` opacity:0), emit the L-31 rule into that library host instead of `fb-styles-site`. This preserves the EXP-002 baseline path where `slider2-component-root` PASSes via `component-root-fallback`, and keeps library-owned hidden-state semantics co-located with their library host.

**What L-31 does NOT do:**
- Does NOT remove or modify the source inline `style=""` attribute (L-8 still governs IX2 runtime evidence preservation; the inline IX-shape count and `data-w-id` count must remain unchanged).
- Does NOT emit selectors more specific than the source class chain (no descendant chains added beyond the `html:not(.w-mod-ix2)` prefix; no `nth-of-type`, no attribute selectors beyond what the architect-approved Option 2 specified).
- Does NOT use `!important` (would block IX2 runtime override; specificity is already sufficient via the runtime-gate prefix).
- Does NOT touch elements without IX-shape OR `data-w-id` evidence (the `detect_mode_b_targets` filter already excludes static utility-class collapses such as a plain `<div style="display:none">` placeholder that is not an IX2 target).
- Does NOT fire in `local-preview` mode — the local Webflow runtime executes IX2 natively from `js/webflow.js`, so a static fallback would race IX2 boot and could shadow the runtime's intended starting state. L-31 is `webflow-paste`-only.

**Anti-lesson boundaries:**
- **L-7 (overlay neutralization scope, ANTI-LESSON UNIVERSAL):** L-31's `html:not(.w-mod-ix2)` prefix excludes its rules from L-7's pure-class-chain candidate set, verified mechanically via `parse_simple_class_chain_selector`. The runtime-gate ensures any single-class target (e.g. `.bg-whipe`) that is also a combo base elsewhere (`.bg-whipe.bg-grey` menu chrome) is collapsed only during the brief pre-IX2 paint window — measured in frames on a post-paste page. The original L-7 regression (Session 041) was a *permanent* published-site collapse with `!important`. L-31 is NOT that.
- **L-8 (IX2 initial-state stripping, ANTI-LESSON NARROW):** L-31 ADDS CSS transport; it does NOT strip the inline state. L-8's preservation floor (≥80% of source IX2 inline declarations preserved; on MNZ this is 164/164 IX-shaped + 35/35 data-w-id) holds unchanged after L-31 runs. The `mode-b-inline-ix-preserved` probe row stays PASS.
- **L-25 (scoped interaction fix discipline, ANTI-LESSON):** L-31's selectors are derived per-target from source detection, not broadened to general class patterns. Each emitted rule names exactly one source class chain plus the runtime-gate prefix.

**How to apply (skill workflow):**
1. After the per-element transformations pass (SKILL.md workflow step 6) and before completing `fb-styles-site` assembly (step 7), invoke `python3 scripts/paste_contract_probe.py --source-root <raw export root or zip> --mode webflow-paste --write-manifest <temp.json>` (no `--fail-on-contract` — we are using the probe as a detector, not yet validating output) and read `inventories[0].modeBTargets` from the produced manifest.
2. For each unique `(selector, tuple(required))` pair across the target list, build a CSS rule of the form `html:not(.w-mod-ix2) <selector> { <decl-1>; <decl-2>; ... }`. Iterate the pairs in deterministic order (sort by `(selector, required)`).
3. Group all L-31 rules into a contiguous block at the end of `fb-styles-site` with a comment header `/* L-31 mode-B transport (webflow-paste) */`. Library-host targets (those whose target dict carries `component_fallback_host`) emit into the named `fb-styles-{library}` host instead of `fb-styles-site`, in their own block with the same comment header.
4. Re-run the probe in step 8 (L-1.5 fast-fail) and again at SV-18 to confirm `mode-b-initial-state-transport` and `mode-b-d007-anchor-safety` PASS while `webflow-paste-overlay-neutralization-scope` STAYS PASS.
5. Manifest row L-31: cite the probe command + the FAIL→PASS transition + the count of L-31 rules emitted into `fb-styles-site` (and per library host where annotated) + `webflow-paste-overlay-neutralization-scope` evidence (`skill-injected=0`).

**Failure mode this prevents:**
- Webflow paste-side canonicalization can silently drop inline `style=""` on hidden-on-load overlays. Without L-31, the first paint after paste shows the overlay visible (the d007 / `.bg-whipe` / `nav-child.left` family of regressions traced in Sessions 159, 160, 164, 169) until IX2 boots and re-applies the hidden state. With L-31, the first paint shows the overlay correctly hidden via the runtime-gated CSS; IX2 boot is then a smooth animation start, not a flash-of-visible-content.
- Specifically: MNZ `nav-child.left` open-on-load (the d007 anchor regression in EXP-002 baseline), `.bg-whipe` overlay flash on slider/menu shells, `.img-parent.recent-post` width-collapsed stutter (Sample 6 from the post-EXP-004 mini-audit), `.recent-info-parent` translate flash, `.heading-small.newbit.btm` translate quadruple flash on hero/blog text rows, and 79 other detected targets across MNZ.

**Verification gate (L-31 manifest row):** `python3 scripts/paste_contract_probe.py --source-root <raw> --output-root <out> --mode webflow-paste --write-manifest --fail-on-contract` → `contractChecks[].id == "mode-b-initial-state-transport"` PASS (zero `missing` targets) AND `contractChecks[].id == "mode-b-d007-anchor-safety"` PASS. Cross-check (anti-broaden guardrail): `contractChecks[].id == "webflow-paste-overlay-neutralization-scope"` STAYS PASS with `skill-injected=0`. Anti-regression: `contractChecks[].id == "mode-b-inline-ix-preserved"` STAYS PASS (L-8 preservation floor unchanged).

**Sync surface:** `references/lessons.md` (this body); `SKILL.md` Mandatory Output Manifest L-31 row + workflow step 6 amendment + new step 7a; `references/verification-gate.md` SV-19 body + Gate Report Template row; `MEMORY.md` ledger entry + curated count bump (26 → 27).

### L-31 collision-handling addendum (added 2026-04-25, EXP-006)

**Pattern (collision):** When `detect_mode_b_targets` returns multiple targets sharing the same source class chain BUT with distinct `required` declaration sets (e.g. MNZ's 26 `.arrow-ab` slider arrows split 25/1 between `transform: translate3d(-100%, 0, 0)` for left-side arrows and `transform: translate3d(100%, 0, 0)` for right-side arrows), a single class-chain-keyed CSS rule cannot carry both first-frame states — CSS source order makes the later rule shadow the earlier one for the same property. The probe row `mode-b-initial-state-transport` correctly classifies these as `converted-css-cascade-risk` because for any given target, the rule with its required fragment may be shadowed by the other rule with the opposite fragment. EXP-005 left this gap unfilled (25 of 85 MNZ targets remained missing).

**Rule (collision-mode emission):** When the skill's L-31 emission step (SKILL.md Step 7a) groups targets by source class chain, it MUST detect collision groups and switch those to per-element `data-flowbridge-ix-state="ix-state-{N}"` marker emission instead of a class-chain rule. Concretely:

1. **Group detection.** After fetching `inventories[0].modeBTargets` (or `output.modeBTargets`), bucket targets by `tuple(target.classes)`. For each bucket, compute the set of distinct `tuple(target.required)` values.
2. **Non-collision bucket (1 distinct required set):** emit single class-chain-keyed CSS rule per the original L-31 rule (`html:not(.w-mod-ix2) <selector> { <decls>; }`). This is the EXP-005 path — unchanged.
3. **Collision bucket (≥2 distinct required sets):**
   - Assign one marker per unique `required` tuple, drawing IDs from a global sequential counter `ix-state-{N}` (N = 1, 2, ...) across the entire output file.
   - For each source HTML element matching the bucket's class chain, identify which `required` tuple matches its inline `style=""` value (substring match on the canonical fragment) and add `data-flowbridge-ix-state="ix-state-{N}"` to that element.
   - Replace the would-be class-chain CSS rules (one per `required` tuple, which would have collided) with marker-keyed CSS rules: `html:not(.w-mod-ix2) [data-flowbridge-ix-state="ix-state-{N}"] { <decls>; }`. Do NOT emit class-chain rules for collision buckets — they would still match all elements and shadow the marker rules.

**Marker namespace:** `data-flowbridge-ix-state` lives in the existing `data-flowbridge-*` attribute family per skill-authoring convention (see L-8 Mode B static-visible safety addendum which already uses `data-flowbridge-ix-state="ixs-N"` for the legacy marker-attribute path). The new EXP-006 emission uses `ix-state-{N}` as the value pattern (hyphenated to mirror the prompt example) — same DOM attribute key, slightly different value naming. Both forms are recognized by `ix_state_markers_in_selector` in the probe.

**Specificity:** an attribute selector `[data-flowbridge-ix-state="ix-state-N"]` has CSS specificity `(0, 1, 0)` — LOWER than a multi-class-chain like `.foo.bar` `(0, 2, 0)`. The runtime-gate prefix `html:not(.w-mod-ix2)` adds 1 type + 1 pseudo-class, bringing the marker rule total to `(0, 2, 1)`. For collision-prone single-class chains (e.g. `.arrow-ab` is one class = source CSS specificity `(0, 1, 0)`), the marker rule wins. For multi-class collision chains (rare; would require a chain like `.foo.bar` with collision), this works because (a) the elements with markers are a subset of elements matching the class chain, and (b) the runtime-gate disengages once IX2 boots so source CSS comes back.

**Why this does not re-broaden L-7:** marker-keyed selectors `[data-flowbridge-ix-state="ix-state-N"]` are NOT pure class chains, so `parse_simple_class_chain_selector` rejects them — the L-7 anti-broaden probe never enumerates them as candidate global class-collapses. Same probe-side guarantee as the runtime-gate prefix.

**Why this does not break the static-visible-class-state-safety check:** the same F-2 probe helper `strip_runtime_gate_prefix` (added in EXP-006) discharges runtime-gated selectors from BOTH `mode-b-static-visible-class-state-safety` AND `mode-b-static-visible-ix-state-safety`. Marker rules with the runtime-gate prefix are recognized as discharged across both safety paths.

**Anti-regression evidence (EXP-006 KEEP, MNZ + synthetic):** with collision-mode emission active for `.arrow-ab` (25 ix-state-1 markers + 1 ix-state-2 marker), `mode-b-initial-state-transport` reports `transported=85; missing=0` on both fixtures. Class-state-safety: 0 hazards. IX-state-safety: 26 markers detected, 0 hidden/collapsed (because the runtime-gate prefix discharges them), 0 unsafe. L-7 anti-broaden: 0 skill-injected. L-8 floor: 164/164 inline IX preserved.

**Idempotence (L-6) for marker emission:** if the source element already has a `data-flowbridge-ix-state` attribute (from a previous skill run on the same input, or from a hand-pretreatment), do NOT overwrite. The skill emission must be idempotent per L-6.

---

## L-32 — `data-flowbridge-*` namespace convention (AUTHORING-PROCESS)

**Classification:** AUTHORING-PROCESS

**Maturity:** MATURE (introduced 2026-04-25 via P0 retrospective; codifies a convention practiced consistently across L-5, L-6, L-28, L-30, L-31 since 2026-04 — explicit naming of an already-established pattern)

**Rule:** Every HTML data attribute introduced by this skill MUST be prefixed `data-flowbridge-*`. No exceptions. Existing instances:

- `data-flowbridge-inline-video-src` (L-5a marker)
- `data-flowbridge-inline-video-autoplay` (L-5b marker)
- `data-flowbridge-link-role-tagged` (L-28 idempotence marker)
- `data-flowbridge-ix-data-inline` (L-30 idempotence marker)
- `data-flowbridge-ix-state` (L-31 collision marker, EXP-006)
- (future markers: same prefix mandatory)

The companion `data-fb-*` short-prefix is RESERVED for **role/semantic** attributes consumed by downstream tooling, not for skill-internal idempotence:

- `data-fb-link-role` (L-28 — read by MASTER-COLLECTION post-paste relinker)
- (future role attributes consumed by downstream Designer Extension or runtime: same `data-fb-*` short prefix)

**Why this exists:** without explicit namespace rules, future L-rules introducing data attributes can pick `data-fb-foo`, `data-pretreat-bar`, `data-flow-baz` ad-hoc. Fragmentation makes it impossible to grep "all skill-introduced markers", breaks `normalize_attrs()` in `component_fidelity_probe.py` (which whitelists `data-flowbridge-*` for fidelity-delta exclusion), and confuses downstream consumers (Designer Extension can't reliably distinguish skill markers from source DOM).

**Anti-pattern:** introducing a new data attribute named `data-fb-{thing}` for a skill-internal idempotence marker (those should be `data-flowbridge-{thing}`). The `data-fb-*` short prefix is reserved for **published roles**, not internal state.

**Conflict resolution:** if a role attribute is needed AND an idempotence marker is needed for the same concern, emit BOTH:
- `data-fb-link-role="template-page"` (role, consumed by post-paste relinker)
- `data-flowbridge-link-role-tagged="true"` (idempotence, prevents skill from re-tagging)

Per L-28 precedent.

**Sync surface:** this rule applies to:
- Any new emission logic in `SKILL.md` workflow steps
- Any new probe (component_fidelity_probe `normalize_attrs` whitelist, asset_ref_check `FLOWBRIDGE_MARKER_PREFIX` constant)
- Any future L-rule that introduces a marker

**No manifest row required:** this is AUTHORING-PROCESS — process rule for rule-authors, not artifact-touching. Compliance is verified at PR/commit time when adding a new rule, not at runtime when running the skill. The `lesson_surface_lint.py` schema accepts AUTHORING-PROCESS as a recognized classification (along with INFORMATIONAL, VERIFICATION-ONLY, ARTIFACT-TOUCHING).

**Provenance:** retrospectively codified from item C1 in `experiments/POST-SHIP-RETROSPECTIVE-INPUT.md`, P0 batch 2026-04-25.

---

## L-33 — IX3 Name Hints for Mechanical Converter Consumption (`webflow-paste` only)

**Date added:** 2026-04-26
**Origin:** C-origin handoff from BigBuns IX3 naming investigation. The source `js/webflow.js` and L-30 inline IX3 data preserve working IDs and timelines but can expose only opaque export names (`i-*`, `ix3-*`, `ta-*`). The mechanical converter can synthesize fallback names, but AI pre-treatment has better semantic context from DOM class names, designer screenshots, and page structure. The fix is an advisory sidecar file, not mutation of IX data.
**Classification:** ARTIFACT-TOUCHING
**Maturity:** NEW (schema/consumer introduced 2026-04-26; needs more organic fixture evidence before promotion to mature).

**Rule:** In `webflow-paste` mode, the skill MUST emit `flowbridge-ix3-name-hints.json` at the output root. The file suggests human-readable names for IX3 interactions and actions so the downstream converter can keep IDs intact while making the Webflow Interactions panel legible. If no confident hints exist, emit the schema with an empty `pages` map or empty per-page maps rather than inventing names.

**Required schema:**

```json
{
  "schema": "flowbridge/ix3-name-hints",
  "version": 1,
  "source": "webflow-pretreat",
  "pages": {
    "index.html": {
      "interactions": {
        "i-0d09c993": "mc-loop-text-effect"
      },
      "actions": {
        "ta-2445dfc1": "stagger-text-loop-one"
      }
    }
  }
}
```

Use normalized ZIP-relative HTML paths as `pages` keys (`index.html`, `about.html`, `cms/foo.html`). For single-page outputs, still use the explicit page key instead of a global unscoped map. The converter may support root-level maps as a compatibility fallback, but the skill must write the page-scoped schema above.

**What the skill may infer:**

- Interaction names from trigger type plus target semantics: page load, scroll trigger class, hover target, `[ani="..."]`, dominant class prefix, and nearby source labels.
- Action names from action targets: class chains (`mc-loop-text.one`), semantic `ani` attributes (`ani="intro"`), repeated SplitText/stagger patterns, image targets, nav/header/footer target names.
- Designer-style slugs when the evidence is strong: `mc-loop-text-effect`, `mc-intro-load`, `mc-scroll-section`, `mc-btn-hover`, `stagger-text-loop-one`.

**Hard boundaries:**

- Do NOT change interaction IDs, timeline IDs, action IDs, targets, timings, properties, `js/webflow.js`, or the L-30 inline IX data.
- Do NOT invent hints for IDs that do not exist in preserved IX3 evidence (`js/webflow.js` or the extracted L-30 inline data).
- Do NOT emit a hint when the semantic name is low-confidence. The converter fallback is preferable to confident-looking fiction.
- Do NOT use fixture-specific conditionals. BigBuns names are examples of naming style, not hardcoded site rules.
- Suggested names must be ASCII, non-empty, ≤80 characters, and contain no control characters or path-forbidden characters (`/ \ < > : " | ? *`).

**Application boundary:** The converter consumes this file mechanically after extracting IX3 data and after its own fallback naming. If a valid hint exists for an ID, the converter replaces only the `name` field. IDs and binding fields remain untouched.

**Failure mode this prevents:** Webflow Designer's IX3 panel can show `i-0d09c993` / `ta-2445dfc1` even though the interaction still works. That makes manual review and post-paste repair almost impossible. L-33 lets the AI lane provide semantic labels while preserving the converter's mechanical safety boundary.

**Verification gate (L-33 manifest row):**

- In `webflow-paste`, parse `output/{runner}_{source-slug}-file_output/flowbridge-ix3-name-hints.json`.
- Assert `schema == "flowbridge/ix3-name-hints"` and `version == 1`.
- Enumerate IX3 IDs from source `js/webflow.js` or from the L-30 inline IX data. Assert every key under `pages.*.interactions` appears in the source interaction ID set and every key under `pages.*.actions` appears in the source action ID set.
- Assert every value is a non-empty string ≤80 chars and contains no control/path-forbidden chars.
- In `local-preview`, assert the sidecar file is absent.

**Sync surface:** `references/lessons.md` (this body); `SKILL.md` workflow step 7b + output-mode wording + Mandatory Output Manifest L-33 row; converter consumer in `minimal-converter-4-1.html`; regression tests in `tests/minimal-converter-4-1-paste-proof.test.ts`.

---

## L-34 — Visible Text / Glyph Fidelity (KEEP; introduced 2026-04-26 from BigBuns + Señorita Colombia incident)

**Maturity:** YOUNG (introduced from one cycle of evidence; promote to MATURE after a second clean cycle on organic fixtures with strong themes)

**Classification:** ARTIFACT-TOUCHING (hard FAIL stops ZIP)

**Evidence:** BigBuns paste 2026-04-26: source `<span class="mc-fade-text">®</span>` was rewritten to `<span class="mc-fade-text">🍔</span>` in three locations. Audit 329 confirmed S-origin (skill output mutated source). Señorita Colombia paste same date: 3 pages had `<title>` mutated — source `Concurso Nacional de Belleza | Colombia` was rewritten to `Señorita Colombia | Concurso Nacional de Belleza` (index.html); two sub-pages had titles generated from scratch and a typo (`Bellza`) was silently corrected. Both mutations passed all 4 existing probes (paste_contract, component_fidelity, asset_ref, lesson_surface_lint) because none checked visible-text fidelity. Root cause: implicit/emergent model behavior — no explicit prompt authorised the mutations; skill had no "leave text alone" instruction, creating a vacuum the model filled with "thematic helpfulness."

**Rule:** The skill MUST preserve, byte-for-byte after whitespace normalization, all visible text in source HTML. Specifically:
- `<body>` text nodes (excluding `<script>`, `<style>`, `<template>`, `<noscript>`, and `fb-*` skill-injected hosts).
- `<head>` text in `<title>` and `<meta>` description/og/twitter content attributes.
- `alt`, `title`, `placeholder`, `aria-label` attributes on body elements.
- `data-*` attributes that hold user-authored content (Webflow `data-w-*` runtime attrs are exempted; `data-flowbridge-*` skill-managed attrs also exempted per L-32).

**Anti-pattern (banned):**
- Replacing decorative glyphs (`®`, `™`, `©`, `°`) with thematic emojis.
- Reordering `<title>` for SEO "improvement".
- Editing `alt` text to be more "accessible".
- Translating any text.
- Fixing typos, case inconsistencies, or formatting in source content.

**If source content seems wrong:** preserve it byte-for-byte. Note it in MANIFEST.md as INFORMATIONAL. Do not edit.

**Verification:** `scripts/content_fidelity_probe.py` with `--source-root <source> --output-root <output> --fail-on-contract`. Exit 0 = PASS. Any non-zero exit blocks ZIP.

**Probe row id:** `content-fidelity-text-glyph` in `pretreat-manifest.json`.

**Sync surface:** `SKILL.md` §Source Content Immutability, `MEMORY.md` Anti-lessons section, `references/verification-gate.md` SV gate row, `pretreat-manifest.json` row id `content-fidelity-text-glyph`, `docs/LESSONS.md`, `docs/LESSON_INDEX.md`.

---

## Excluded Rules (appendix — not authoritative for this skill)

These four rules from `docs/LESSONS.md` are tracked for historical context but do NOT fire manifest rows or gates in the webflow-pretreat skill. They remain authoritative in the host project if consumed from `docs/LESSONS.md`.

- **L-3** — SUPERSEDED by L-16 (Universal Runtime + DOM-Ready Init Gating). Kept in canonical file for history.
- **L-10** — SUPERSEDED by L-15 + L-15A (Uniform Script Wrapping). Kept in canonical file for history.
- **L-26** — VERIFICATION-ONLY, converter-owned (Designer parity via native `styleLess`). No pretreatment manifest row. Owned by the downstream minimal converter and `converter_invariant_probe.py`.
- **L-29** — PASTE-SIDE mutation (Webflow rewrites all `w*`-prefixed classes, not just `w-`). Not pretreatment artifact-touching.

The full canonical bodies live at:
`C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\LESSONS.md`
