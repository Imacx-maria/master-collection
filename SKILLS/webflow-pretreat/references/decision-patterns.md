# Decision Patterns — Layout Compensation Reasoning

Load this when SKILL.md's Scan → Compensate → Verify step fires. This file teaches three things:

1. **How to scan** source CSS for body-dependent layout before you wrap.
2. **Which patterns** require compensation, and what the minimum compensating CSS looks like.
3. **How to verify**, after wrap, that every detected pattern was addressed.

**Every site is different.** Read the CSS, apply the four scan questions below, determine what adjustments THIS SPECIFIC SITE needs. Do not copy rules blindly from one site to another. Class names in worked examples are illustrative — the principle applies, the class names do not transfer.

---

## Step 1 — How to Scan Source CSS for Body-Dependent Layout

Before moving any content inside `fb-page-wrapper`, read the source site CSS top-to-bottom and ask these four reasoning questions. The answers tell you which patterns require compensation.

### Question 1 — The Cascade Question

*Which rules assume `<body>` is the direct parent of content, so that their declarations reach descendants via CSS inheritance?*

Wrapper insertion moves every content element one level deeper. Any rule whose selector is body-relative — `body { ... }`, `body > *`, `body:has(...)` — now applies to a non-wrapper ancestor. Typography (`font-family`, `font-size`, `font-weight`, `color`, `line-height`, `text-transform`) inherits; reset it on `.fb-page-wrapper` or descendants fall back to the paste-pipeline baseline (often Arial / browser defaults).

### Question 2 — The Containing-Block Question

*Which positioned elements expected `<body>` (or the viewport) as their containing block or scrolling ancestor? After wrap, is that still true?*

- `position: sticky` climbs to the nearest scrolling ancestor. Wrapper `overflow: hidden` creates a new scroll container that breaks sticky. `overflow: clip` does NOT create a scroll container — sticky still works.
- `position: fixed` positions against the viewport UNLESS an ancestor has `transform`, `filter`, `perspective`, `will-change`, or `contain: layout`. Any of those on the wrapper re-roots fixed positioning and silently breaks full-viewport layers.
- `position: absolute` climbs to the nearest positioned ancestor. If the wrapper has no `position`, behavior is unchanged. If the wrapper later gains `position: relative`, absolute descendants re-anchor.

### Question 3 — The Sibling Question

*Which sibling pairs were body-level siblings and relied on that sibling relationship — z-index layering, reveal-footer stacking, or flow-order layouts?*

z-index only creates a new stacking context when combined with `position`, `opacity < 1`, `transform`, `filter`, or a few others. If the wrapper acquires any stacking-context-forming property, sibling z-index values that worked at body level re-root and may invert. The reveal-footer pattern (body-level content wrapper with `overflow: clip` stacks above a body-level footer with `position: relative`) is the canonical case: siblings are preserved after wrap, but their shared parent changes from `<body>` to `.fb-page-wrapper`.

### Question 4 — The Viewport-Sizing Question

*Which body-level content relies on `height: 100vh` / `100svh` / `100dvh`, or `height: 100%` that traverses up to `<html>`?*

`100vh` / `100svh` / `100dvh` size against the viewport regardless of ancestor — unaffected by wrap. `height: 100%` climbs the ancestor chain: body → html. After wrap, `.fb-page-wrapper` becomes an intermediate ancestor. If it lacks a defined height, percentage-height descendants collapse.

### What to output from the scan

Before proceeding to Step 2, write a short internal list: *"Pattern A applies because rule X at CSS L60-66 does Y; Pattern B applies because rule Z at CSS L152-157 does W; Pattern C does not apply because no sibling pair at body level."* The scan's output is this pattern-to-rule map. Every item in the map is a compensation commitment.

### Wrapper impact boundary — what the scan may and may not change

Wrapper insertion can affect CSS behavior through a bounded set of mechanisms:

- cascade inheritance from `body` / `html`;
- containing blocks for `absolute` / `fixed` positioning and percentage-based dimensions or offsets;
- scroll containers and sticky positioning through `overflow`;
- stacking contexts and z-index sibling relationships;
- selector topology (`body > *`, adjacent/general siblings, body-level order);
- `height: 100%` chains that now pass through the inserted wrapper.

Wrapper insertion does **not** justify arbitrary component-local changes. Do not rewrite, strip, resize, or reinterpret media/hover details merely because a wrapper was inserted. `object-fit`, `object-position`, `background-size`, `background-position`, `width`, `height`, `aspect-ratio`, `overflow`, `transform`, `transition`, inline styles, class chains, `data-w-id`, and hover/mouse event wiring must remain source-faithful unless a declared L-rule explicitly changes them and the manifest names that rule.

Important nuance: a media element with `height: 100%` can be affected if its ancestor height chain changes; in that case compensate the ancestor chain, not the media rule. A media element with the same box, same CSS, same asset, and same hover script should render and animate the same after wrapping.

---

## Step 2 — Pattern Catalog (Illustrative — principle applies to any Webflow export)

Detect whether each pattern applies to this site via Step 1. When it applies, add the minimum CSS to `fb-styles-site`.

### Pattern A — Body Inheritance Root (illustrative: MNZ sets font-family on `body`)

- **Detect:** The source site CSS contains a rule whose selector is `body` (or `html, body`) that sets a cascade-sensitive property — typography (`font-family`, `font-size`, `font-weight`, `line-height`, `text-transform`), `color`, or another inherited property.
- **Reason:** Every text node inside `.fb-page-wrapper` inherits those values through the cascade from `<body>`. Webflow's paste baseline (`body { font-family: Arial, sans-serif }` in `webflow.css`) is a competing rule. If the paste pipeline normalizes body rules or Webflow Designer applies its own body defaults, the site loses its typography — descendants fall back to Arial.
- **Compensate:** Duplicate the body-selector inherited declarations onto `.fb-page-wrapper` so the cascade still reaches descendants from one level down. Duplicate, don't move — the source `body { ... }` rule stays intact in HEAD inline `<style>` (L-1 Option B is unchanged).

Illustrative addition to `fb-styles-site`:

```css
.fb-page-wrapper {
  font-family: Ppmori Extra Bold, sans-serif;
  font-size: 1rem;
  font-weight: 700;
  line-height: 1;
  text-transform: uppercase;
  color: var(--black);
}
```

Illustrative — principle applies to any Webflow export whose site CSS sets typography, color, or other inherited properties on the `body` selector. Class names in the declaration list come from the source's actual values; selector is always `.fb-page-wrapper`.

### Pattern B — Reveal Footer (illustrative: MNZ `.footer-parent` after `.wrapper`)

- **Detect:** A main content wrapper (`position: relative`, or whose positioning causes z-index stacking) in the source sits BEFORE a footer element that is in normal document flow with `position: relative` (NOT sticky, NOT fixed). Content's background covers the footer until the user scrolls past.
- **Reason:** The pattern works via z-index stacking between siblings in normal flow. The content wrapper's z-index (explicit or implicit) makes it visually cover the footer. As the user scrolls past, the footer below in flow becomes visible. Moving both inside `fb-page-wrapper` preserves the sibling relationship — but if the wrapper acquires a stacking-context-forming property, the siblings' z-index values re-root.
- **Compensate:** Ensure the main content container has `position: relative` and a `z-index` (e.g., `z-index: 1`) that stacks it above the footer. Do NOT add `position: sticky` or `position: fixed` to the footer — it must remain in natural document-flow position. Keep `.fb-page-wrapper` stacking-context-neutral (no `transform`, `filter`, `opacity < 1`, `will-change`).
- **Common mistake:** Adding `position: sticky; bottom: 0` to the footer. This repositions the footer near the viewport bottom instead of its natural document-flow position, breaking the reveal. The source CSS almost always has `position: relative` on the footer — preserve that.

Illustrative (MNZ):

```css
.fb-page-wrapper { overflow: clip; }
.wrapper { position: relative; z-index: 1; }
/* .footer-parent keeps its original position: relative — NO sticky override */
```

Illustrative — other sites use different class names, different containment strategies, different stacking orders.

### Pattern C — Sticky Sections

- **Detect:** Elements with `position: sticky` inside the content.
- **Reason:** `overflow: hidden` on an ancestor creates a new scroll container that breaks sticky. `overflow: clip` does NOT create a scroll container, so sticky still works with `overflow: clip`.
- **Compensate:** Use `overflow: clip` on `.fb-page-wrapper` (not `overflow: hidden`). If the original site's wrapper already had `overflow: clip`, preserve that on the original wrapper class; do NOT re-declare on `.fb-page-wrapper` unless you created the wrapper yourself.

### Pattern D — Fixed Navigation

- **Detect:** Nav elements with `position: fixed`.
- **Reason:** Fixed elements position against the viewport UNLESS an ancestor has `transform`, `filter`, `perspective`, or `will-change`. `overflow: clip` does NOT break fixed positioning.
- **Compensate:** Do NOT add `transform`, `filter`, `perspective`, `will-change`, or `contain: layout` to `.fb-page-wrapper` or any ancestor of fixed elements. The wrapper must remain a neutral structural parent.

### Pattern E — Full-Viewport Fixed Backgrounds

- **Detect:** Elements with `position: fixed; width: 100%; height: 100vh` (tickers, background layers, full-viewport overlays).
- **Reason:** These still work inside a wrapper as long as the wrapper doesn't create a containing block for fixed positioning. `overflow: clip` clips without creating a containing block.
- **Compensate:** `overflow: clip` on the wrapper is sufficient. These elements remain viewport-relative.

### Pattern F — Z-Index Stacking Contexts

- **Detect:** Multiple sibling elements with z-index values that create intentional layering (e.g., content at `z-index: 1` above footer at `z-index: 0`).
- **Reason:** Moving these inside a wrapper preserves relative stacking as long as the stacking context is maintained. Any stacking-context-forming property on the wrapper (`transform`, `filter`, `opacity < 1`, `will-change: transform`) re-roots the context.
- **Compensate:** Keep `.fb-page-wrapper` stacking-context-neutral. If sibling z-index relationships exist, ensure they survive the wrap. Do not give `.fb-page-wrapper` a `z-index`.

### Pattern G — Viewport-Height Chains (`height: 100%` rooted at html/body)

- **Detect:** Content elements with `height: 100%` (as opposed to `100vh`) whose effective height relies on the `html { height: 100% } body { min-height: 100% }` chain from Webflow's normalize.
- **Reason:** `.fb-page-wrapper` inserts between body and the content; if it has no declared height, `height: 100%` descendants collapse to zero.
- **Compensate:** If the site relies on `height: 100%` traversal, add `min-height: 100%` or `height: 100%` to `.fb-page-wrapper`. More commonly, sites use `100vh` and this pattern does not apply — only add the compensation when the scan surfaces it.

---

## Step 3 — Self-Verify Checklist (walk this after wrap, before declaring output complete)

These are reasoning prompts, not mechanical tick-boxes. Answer each for the current site's actual scan output.

1. **Body inheritance (Pattern A).** Did my scan identify any `body` (or `html, body`) rule that sets typography, color, or a cascade-sensitive property? If yes, is there a corresponding rule on `.fb-page-wrapper` in `fb-styles-site` carrying those declarations? If no body rule exists in the source, answer "not applicable, source defines typography on specific classes, not on body."
2. **Sticky (Pattern C).** Did my scan identify any `position: sticky` element? If yes, is `.fb-page-wrapper` compatible — `overflow: clip` or no overflow declaration, NOT `overflow: hidden`? If no sticky elements found, answer "not applicable."
3. **Fixed (Patterns D, E).** Did my scan identify any `position: fixed` element? If yes, does any new ancestor (`.fb-page-wrapper` or anything I inserted) set `transform`, `filter`, `perspective`, `will-change`, or `contain: layout`? If yes, those properties must be removed — fixed positioning is broken. If no fixed elements, answer "not applicable."
4. **Reveal-footer (Pattern B).** Did my scan identify a body-level content wrapper + sibling footer in normal flow? If yes, does the wrapped structure still allow the reveal behavior — content wrapper has `position: relative` + `z-index`, footer has `position: relative` (not sticky, not fixed), `.fb-page-wrapper` is stacking-context-neutral? If no reveal pattern, answer "not applicable."
5. **Z-index siblings (Pattern F).** Did my scan identify z-index sibling pairs that were body-level in the source? If yes, is `.fb-page-wrapper` stacking-context-neutral (no `transform`, no `opacity < 1`, no `filter`, no `will-change: transform`)? If no z-index sibling pairs, answer "not applicable."
6. **Component-local fidelity (L-22).** For media and hover/mouse interaction components that the wrapper scan did NOT classify as body-dependent, did class lists, attributes, inline styles, source asset refs, `object-fit` / `background-size` declarations, transitions/transforms, `data-w-id`, and script bodies/selectors remain unchanged? If any changed, is the change tied to a specific L-rule manifest row? If no, stop — this is careless recreation, not wrapper compensation.

If any answer is "no" or "unknown," stop and resolve before declaring output complete. An unaddressed body-dependent rule is a paste-side layout regression waiting to happen.

---

## Note on scope

The Scan → Compensate → Verify loop is for wrapper-insertion side effects on the CSS layout system. It is NOT a general "check every CSS rule" pass. The four scan questions target the specific class of rule whose behavior wrapper insertion changes. Rules that are unaffected by wrap (class-scoped typography, component-scoped positioning with no ancestor dependency) do not need compensation.

---

## Script Emission Policy — Three-Class Partition (L-15 + L-15A, 2026-04-18 EXP-009)

Every `<script>` tag found in the source HEAD and body gets classified into exactly one of three classes. Each class has one canonical destination host. The original `<script>` tags are removed from their source positions after emission.

### The three classes + destinations

| Class | Detection | Destination host | Dep-gate runner (L-16)? |
|---|---|---|---|
| **CDN library** | `src` is absolute HTTP(S) or known CDN host (`jquery`, `cdn.jsdelivr.net`, `unpkg`, `cdnjs`, `greensock`, etc.) | `fb-scripts.w-embed` inside `fb-custom-code`. Source order preserved — jQuery first, library CDNs next. | NO (load, not init) |
| **Inline init / detector / deferred body** | No `src` attribute. Body references runtime globals (`Webflow`, `jQuery`/`$`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, `window.<X>`) OR installs document/listener/selector work (`DOMContentLoaded`, `click`, `scroll`, `IntersectionObserver`, `querySelector`, etc.). Includes HEAD `<script defer>` bodies. | `fb-scripts.w-embed` inside `fb-custom-code`, AFTER the CDN loads they depend on. | YES when the body references runtime globals OR immediately touches source DOM. Use L-16 `need[]` + required/optional selector readiness; `need[]` may be empty. |
| **Local Webflow runtime** | Relative `script[src]` whose normalized basename is `webflow.js`. NOT an absolute HTTP(S) URL. Exactly one such element per page. | `fb-runtime.w-embed` that is a DIRECT CHILD of `fb-page-wrapper`, positioned AFTER all source-content siblings (`nav`, `wrapper`, `footer-parent`, or fixture-equivalent). NOT inside `fb-scripts`. NOT inside `fb-custom-code`. | NO (external reference = load, not init) |

A fourth implicit class — **local Webflow runtime (inline IIFE)** — is detected by an inline script containing the Webflow module-IIFE signature and all three of `Webflow.push`, `Webflow.require`, `Webflow.define`, length > 50,000 chars. This inline form is forbidden by L-19 (the 071 crash mechanism). It is NOT a placement candidate — it is a hard fail.

**Metadata script note:** valid `<script type="application/ld+json">` bodies are not executable JavaScript. Preserve them as metadata only when the body parses as JSON and has JSON-LD shape (`@context` on an object, or an array of JSON-LD objects). If a body contains executable JavaScript or fails JSON parsing, do not retag/preserve it as JSON-LD; classify it as executable source code or HALT. Misclassified JSON-LD silently disables code.

**Source-shipped GSAP-family `<script>` bundles** (GSAP core, SplitText, ScrollTrigger, ScrollSmoother, DrawSVG, MorphSVG, Flip, etc.) are CDN libraries in class 1 above: preserved inside `fb-scripts.w-embed` in source order per L-15, dep-gate N/A (CDN = load, not init). Associated source inline init bodies are class 2: preserved inside `fb-scripts.w-embed` in source order after their CDN, wrapped in the L-16 `need[]` runner when they reference runtime globals and in required/optional selector readiness when they immediately target source DOM. **Pre-treatment does not strip source-shipped GSAP-family scripts based on downstream Webflow-native convertibility** — that classification is the converter/Webflow stage's concern (L-9 reframed 2026-04-19 EXP-019, `docs/LESSONS.md`). The IX2/IX3-impossibility scan described in `references/webflow-constraints.md` §IX2/IX3 Exceptions is retained as observational reference for the downstream converter/Webflow stage; at pre-treatment it does NOT gate preservation.

### Why three classes, not uniform wrap

The original L-15 "uniform wrap, no classifier" rule was correct for CDN libraries and inline init bodies — both run against a DOM that parses fully after they execute anyway (DOM-ready-aware code waits; listeners fire on matching events later). It was WRONG for the local Webflow runtime because `js/webflow.js` hydrates IX2 against DOM that is already parsed at the moment it executes. Early placement inside `fb-scripts` inside the first `fb-custom-code` puts the runtime BEFORE `nav`/`wrapper`/`footer-parent` parse, so IX2 boots against an empty DOM and misses every hydration target. Audit-082 (file-URL browser audit, 2026-04-18) proved this on MNZ — section 04 stuck at opacity 0, menu left panel stuck at 720×48, footer transform `none`. Audit-083 confirmed the three-class partition isolates the cause cleanly; every other script class is unaffected.

Three classes, not more: the classifier is structural (where the script comes from, what it needs, what it hydrates against) rather than per-fixture judgment. MNZ's eight scripts, Señorita Colombia's thirteen, and any future export all partition by the same three signals — no per-fixture re-decision, no regression risk.

### Posture 1 (future preferred) vs Posture 2 (body-end fallback)

**Posture 1 (locked, emit by default):** `fb-runtime.w-embed` as the last direct child of `fb-page-wrapper`, after source-content siblings. Preserves L-11 (`fb-page-wrapper` is the single `<body>` child) and uses the proven `w-embed` host mechanism (same clipboard-survivability as `fb-styles-[library]` under L-17). Requires a narrow L-12 exception (documented in `docs/LESSONS.md` L-12 above and L-15A).

**Posture 2 (compatibility-pass only):** `<script src="js/webflow.js">` as a direct `<body>` child immediately after `.fb-page-wrapper` closes. Used only in legacy reconstructed reference artifacts (e.g. `index-local.html` shape prior to L-19 narrowing). The SV-13-B gate passes both postures during audit comparison; production emission is Posture 1.

### Procedure during emission

1. Walk source HEAD + body. Enumerate every `<script>` element (both `src="..."` CDN references and inline), including `defer`, `async`, `type`, and data attributes. HEAD-origin scripts are part of the source inventory; do not capture them into scratch variables and forget to emit them.
2. Classify each script into one of the three classes above.
3. CDN libraries + inline init/defer bodies → concatenate in source order into `fb-scripts.w-embed` content, nested inside `fb-custom-code`. Inline bodies that reference runtime globals OR immediately touch source DOM get the L-16 `need[]` + required/optional selector runner wrapper. Valid JSON-LD metadata is preserved as metadata and is not runner-wrapped.
4. Local Webflow runtime → emit inside `fb-runtime.w-embed` as a direct child of `fb-page-wrapper`. Position AFTER all source-content siblings.
5. `fb-custom-code` stays as the FIRST direct child of `fb-page-wrapper` (unchanged from L-12 Option A).
6. Source-content siblings (from L-13) stay in the middle in source order.
7. `fb-runtime` is the LAST direct child of `fb-page-wrapper` when a local webflow.js runtime is present.
8. Remove the original `<script>` tags from their source positions.
9. Before manifest, compare a normalized source script inventory (HEAD + body, excluding the L-19-forbidden inline runtime IIFE and the L-15A local `webflow.js` carve-out) against output `fb-scripts`: every preserved inline body fingerprint and CDN `src` must be accounted for. Missing HEAD defer bodies are an L-15 FAIL, not an acceptable page-specific omission.

### What this policy does NOT change

- **Source-shipped GSAP-family libraries and their associated source inline init bodies are PRESERVED inside `fb-scripts.w-embed`** per L-9 (reframed 2026-04-19 EXP-019). Pre-treatment does not strip source-shipped libraries based on downstream Webflow-native convertibility; the converter/Webflow stage owns IX2-to-IX3 and IX3-to-IX3 conversion. SKILL.md Hard Rule #3 continues to ban synthesizing NEW GSAP/custom JS for native-capable interactions — that generation ban is separate from and does not override the preservation rule.
- `js/webflow.js` content semantics are unchanged: never inline the module IIFE (L-19). Only the placement changed — late `fb-runtime` sibling replaces early `fb-scripts` nesting.
- Duplicate library CDN removal stays in force.
- jQuery MUST appear before inline init scripts and any library init code within `fb-scripts`.
- L-16 dep-gate runner scope unchanged: wraps inline init bodies only, NOT CDN `<script src>` tags.

### SV gates that enforce this policy

- **SV-9** (naked-script floor) — zero `<script>` direct children of `fb-page-wrapper`, CDN + inline init scripts live inside `fb-scripts.w-embed`. Runtime script is carved out: governed by SV-13-B, not SV-9-C.
- **SV-10** — L-16 dep-gate runner shape on inline init bodies.
- **SV-13-A** — external webflow.js reference preserved exactly once, module IIFE never inlined.
- **SV-13-B** — late placement structural check on the external webflow.js reference.

### Final procedure phase — Mandatory Output Manifest (L-21, EXP-010)

After every transformation completes and the Structural Verification Gate runs, the skill's final pre-zip phase is the **Mandatory Output Manifest** — see `SKILL.md §Mandatory Output Manifest — Before You Zip`. Produce a row per L-rule that touches the artifact with a live check command + captured result + PASS/FAIL; if ANY row FAILs, write `HALT-REPORT.md` and STOP instead of zipping. This is the structural self-attestation contract; no additional policy lives here — the full spec + inventory is in SKILL.md.

---

## Pattern H — Library Style Migration + Designer-Fallback Emission (L-17)

- **Decision:** When a third-party component library is detected (by root-class presence in body DOM or by library-specific CDN script in `fb-scripts`), first migrate every HEAD stylesheet/style block owned by that library into the library's `fb-styles-[library-slug]` host. If no explicit HEAD stylesheet exists but the JS/root signal makes the same-package stylesheet URL deterministic, fetch and inline that core CSS and record the inference. Then emit a static Designer-visibility fallback iff the library's runtime would reshape children or hide the root before hydration.
- **Migration is mandatory:** the host must carry the library CSS payload. Prefer fetching CDN stylesheets and inlining the CSS bytes inside `<style>`; if fetch is unavailable, move the original source `<link>` into the host and record that fallback. Leaving the library stylesheet in HEAD, leaving any residual HEAD library CSS after host creation, or emitting fallback-only CSS with no core markers is FAIL because the converter/paste path does not rely on HEAD custom code.
- **Always emit fallback:** Splide, Swiper, Embla, Flickity, Lottie — all hide their root / slides before their runtime hydrates. Designer canvas does not run the runtime, so components are invisible for authoring without the fallback.
- **Optional fallback:** Lenis — smooth-scroll library does not hide children or reshape DOM. Fallback is not required; emit only if the library's HEAD CSS contains a visibility rule that blocks Designer editing.
- **Fallback shape:** `.<library-root>, .<library-root>__<inner-standard-classes> { visibility: visible !important; opacity: 1 !important; }`. `!important` is mandatory because the library's own CSS ships `opacity: 0` or `visibility: hidden` that would otherwise win. Include ≥1 inner-standard-class selector (Splide: `.splide__track`; Swiper: `.swiper-wrapper`; Flickity: `.flickity-viewport`) so the first layer of children is also Designer-visible.
- **Host placement:** migrated/inferred CSS/link and fallback go inside the `fb-styles-[library-slug]` HtmlEmbed nested in `fb-custom-code` (L-17 step 1–3). A fallback-only host is FAIL.

## Pattern I — Multi-Dependency Init Gating (L-16)

- **Decision:** When you move an inline executable `<script>` into `fb-scripts.w-embed`, first scan the script body (after comment-stripping and dead-bridge removal) for every runtime global it references — `window.<X>`, `jQuery`/`$`, `Webflow`, `Splide`, `Lenis`, `gsap`, `ScrollTrigger`, `SplitText`, `ScrollSmoother`, `DrawSVG`, `MorphSVG`, `Flip`, site-defined globals, any other library global. Build `need[]` as the superset, allowing `[]` for selector-only scripts. This applies to every retained inline init/custom-code body from HEAD or body: library init, source-shipped GSAP-family inline init body (preserved per L-9 2026-04-19 EXP-019 reframe — not gated on Webflow-native convertibility), detector, plugin bridge, DOM click-forwarder, or arbitrary source custom code. Valid JSON-LD metadata is not executable and skips this runner.
- **Wrap with the L-16 runner:** `need = [...]`, `fbReady = () => need.every(...)`, `fbRun = () => { ...original body... }`, bounded polling loop (50ms × 200 = 10s cap), `console.warn` on timeout listing the missing globals. Original body stays inside `fbRun` verbatim.
- **Selector-ready is part of readiness:** if the retained body immediately queries, mounts onto, animates, observes, or binds to source DOM (`$('.slider2')`, `document.querySelector(All)`, `new Splide(selectedEl)`, `gsap.to('.hero-title', ...)`, `ScrollTrigger.create({ trigger: '.section' })`, `document.querySelector('.menu-dropdown').addEventListener(...)`, Swiper/Embla/Flickity/Lottie roots, custom widget roots), split selectors into required vs optional. Required selectors are dereferenced without guards, mounted as component roots, or drive visible behavior that exists on this source page; these require `document.readyState !== "loading"` plus `document.querySelector(selector)` before `fbRun`. Optional selectors are guarded/null-safe or may legitimately be absent; they require DOM parsed but not presence. This applies even when there are no runtime globals.
- **Do NOT wrap bare CDN `<script src>` tags** in the runner — those are loads, not inits. L-15 still places the `<script src>` element inside `fb-scripts.w-embed`, but the dep-gate runner is for inline init bodies only.
- **Do NOT stack single-global waits.** A script that uses both `Webflow` and `Splide` must gate on `['Webflow', 'Splide']` — not on `'Webflow'` alone. Webflow depending on jQuery internally does NOT guarantee any other library has loaded.
- **Why:** single-global gate races; a script that touches `Webflow` + `Splide` fires after `Webflow` exists but while `Splide` is still loading and silently no-ops. A globals-only gate also races DOM parse when source body-end or HEAD-defer custom code is moved into early `fb-scripts`; MNZ section 2 selected zero `.slider2` nodes and silently mounted nothing, and Srta Colombia's `.menu-dropdown` forwarder proved selector-only bodies need DOM/selector readiness. Splide and the menu forwarder are proof cases, not the scope: kept GSAP/ScrollTrigger exceptions and arbitrary custom code have the same failure mode when their first run depends on DOM targets. Required/optional classification prevents the opposite bug: timing out forever on guarded controls that are legitimately absent on a given page. The mechanical runner (src/pre-treatment/core.ts:556-596) got the global-dependency part right before L-16 landed it into the AI skill; EXP-016 adds universal selector readiness.
