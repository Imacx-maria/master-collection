# Liquid Glass Modifier Review Checks

Load during Phase 4 when `effects.liquid-glass === true`.

Run **in addition to** the host style's review checks — this is a modifier overlay, not a replacement.

---

## Review Checks

1. **Provenance declares `effects.liquid-glass` and the variant.**
   DESIGN.md must have `provenance.effects.liquid-glass: true` and `provenance.effects.variant` set to one of `regular | clear | prominent`. Variant must be explicit — `regular` is the default but cannot be inferred.
   How to verify: grep `provenance.effects` in DESIGN.md; both keys must be present.
   Severity: **Major**

2. **Compatibility matrix tier was respected — or refused-style single-element override is documented.**
   Applying glass to a refused style without the single-element override is a delivery-blocking spec violation. If the host style is in the Native or Conditional tier, proceed. If refused: verify `provenance.effects.override: single-element-rule` exists and that exactly one glass element is present.
   How to verify: cross-reference host style against the matrix in `references/effects/liquid-glass.md`. Count elements with `backdrop-filter` in the build file.
   Severity: **Critical**

3. **Sanctuary Tech is NOT the host style.**
   Hard-refuse — no override path exists. Glass in Sanctuary Tech adds translucency, blur, and fluid morphing: all three are stress signals in the trauma-informed contract. No user request, no provenance note, no single-element rule overrides this.
   How to verify: `grep -i "sanctuary" DESIGN.md` must not appear alongside `liquid-glass: true`. If both present: return error, do not proceed with the review.
   Severity: **Critical**

4. **Every glass element is a chrome or overlay layer, not body content.**
   Glass on body content, large text containers, or structural sections fails contrast at variable scroll positions. Every eligible element must be answerable as "chrome layer" or "overlay layer" — nav, modal, popover, toast, sticky bar, lightbox chrome, hero image overlay.
   How to verify: for each element with `backdrop-filter`, confirm it maps to the eligible-elements list in `references/effects/liquid-glass.md` § Eligible elements. Manual: open the page at 3 scroll positions and read all text through each glass surface.
   Severity: **Critical**

5. **Glass surface count is within viewport budget.**
   Stacked glass surfaces create nested blur compositing cost and visual muddying. Budget: mobile (≤768px) ≤3 simultaneous; tablet (769–1199px) ≤5; desktop (≥1200px) ≤8. Count visible-on-screen, not total in DOM — a sticky nav + open modal + tooltip = 3.
   How to verify: count elements with `backdrop-filter` visible simultaneously at 375px, 768px, and 1440px viewport widths. Flag if any tier is over budget.
   Severity: **Major**

6. **Blur radius is within range: 8–12px mobile, 12–24px desktop. Hard ceiling 24px.**
   Below 8px the blur reads as a visual artifact. Above 24px the surface loses foreground/background distinction and compositing cost spikes. The 24px ceiling applies globally; a documented marquee-modal exception (single elevated modal) is the only allowed exceedance.
   How to verify: `grep -E "blur\([0-9]+(px|rem)\)" <build-file>` — all values must be 8–24px. Flag out-of-range values. Check `-webkit-backdrop-filter` as well as `backdrop-filter`.
   Severity: **Major**

7. **No `backdrop-filter` animation or transition.**
   Animating the blur radius re-rasterizes the blur region every frame — GPU-intensive jank on all tiers. Opacity, transform, and color transitions on the glass surface are permitted; interpolating `backdrop-filter` itself is not.
   How to verify: `grep -E "transition.*backdrop-filter|@keyframes.*backdrop-filter|animate.*backdrop" <build-file>` must return zero matches.
   Severity: **Critical**

8. **`prefers-reduced-transparency: reduce` block exists with solid fallback.**
   Users who set this system preference have visibility or cognitive load reasons. The block must set `backdrop-filter: none` and provide a solid `background` using `--glass-fallback-bg` or the host style's equivalent solid surface token (e.g., `--surface-elev-2`).
   How to verify: `grep "prefers-reduced-transparency" <build-file>` must return ≥1 match. Inspect the block: `backdrop-filter: none` and a solid background must both be present.
   Severity: **Critical**

9. **`prefers-reduced-motion: reduce` block exists for any glass morphing animation.**
   Morphing glass elements (fluid scaling, blur-on-focus, card transforms) can trigger motion sickness. Required whenever any `transition` or animation is applied to a glass element. Block must disable `transition` on glass selectors.
   How to verify: if any glass element has `transition` or an animation class, `grep "prefers-reduced-motion" <build-file>` must return ≥1 match. Inspect the block: `transition: none` on glass selectors.
   Severity: **Critical**

10. **Mandatory shadow anchor present on every glass surface.**
    Glass without a shadow loses spatial grounding — the element reads as floating noise against the backdrop. Shadow is the anchor that makes the surface read as intentional chrome, and it provides the depth cue when transparency is removed by the `prefers-reduced-transparency` fallback.
    How to verify: `grep -E "(\.lg-|backdrop-filter)\s*\{[^}]*\}" <build-file> | grep -v box-shadow` must return zero matches. Every glass selector must have `box-shadow`.
    Severity: **Critical**

11. **Manual contrast spot-check on glass surfaces holding text.**
    The blur backdrop makes the worst-case background unpredictable — any pixel in the scrollable content can appear behind the glass. WCAG minimum: 4.5:1 for body text (≤24px normal, ≤18.66px bold), 3:1 for large text.
    How to verify: manually inspect at the brightest point of the background visible under body-size text through the glass. Use browser DevTools eyedropper to pick the worst-case background pixel, then check contrast ratio in the DevTools color picker or an external tool. Must be ≥4.5:1 for body text.
    Severity: **Critical**

12. **(Conditional — WebGL track active) All four failure-mode guards present.**
    A glass shader without all four guards is a delivery-blocking defect. Required guards match `references/webgl-3d-tactics.md`: (1) WebGL feature detect with DOM fallback, (2) `prefers-reduced-motion` static frame, (3) SEO/a11y DOM mirror — real content in DOM, canvas `aria-hidden="true"`, (4) 8s load timeout.
    How to verify: grep each guard in the build file. All four must be present. Skip this check if the project is on the CSS-only track.
    Severity: **Critical** (if WebGL track active)

13. **(Conditional — WebGL track active) Shader bundle weight ≤200 KB compressed.**
    200 KB compressed is the shader-accents tier budget. Exceeding it pushes LCP past 3s on median mobile connections.
    How to verify: `gzip -c <js-bundle> | wc -c` — must be ≤204800 bytes. Or: Network panel filtered to JS, sum compressed sizes for the shader module.
    Severity: **Major** (if WebGL track active)

14. **Refused-style override (if used): single-element rule respected and provenance documented.**
    The single-element override is valid only when it is truly isolated and intentional. Two glass elements on a refused style is a pattern — a pattern means the style system has glass in it, which defeats the refusal.
    How to verify: count elements with `backdrop-filter` in the build — must be exactly 1. Verify DESIGN.md has `provenance.effects.override: single-element-rule` and `provenance.effects.override-element` names the specific element.
    Severity: **Major**

---

### Light-mode glass — the 5-rule check (conditional)

Run only if the build ships glass in light mode (either light-only, or via theme-toggle in light state). Each rule from `effects/liquid-glass.md` § 6.5 must be verified independently — failures here are **Major** severity by default (the glass just doesn't read), promoting to **Critical** when the failure makes interactive surfaces invisible.

1. **Background tint ≥ 0.55 alpha** — inspect each light-mode glass surface's computed `background-color`. If alpha is below 0.55, the surface won't read against light backgrounds. Acceptable: `rgba(255,255,255,0.55–0.78)`. Below 0.55: refactor. Above 0.78: drop the modifier (it's solid, not glass).

2. **Hairline border is dark** — inspect each light-mode glass surface's computed `border-color`. White / near-white hairlines (`rgba(255,255,255,*)`) on light backgrounds are invisible. Required: `rgba(20-30, 24-34, 31-40, 0.08–0.16)` range.

3. **`backdrop-filter` blur ≥ 24px** — light needs more blur than dark to commit to the metaphor. Below 24px reads as "out of focus" not "frosted." Hard ceiling at 40px (perf).

4. **`backdrop-filter` includes `saturate(≥1.4)`** — this is the most-skipped rule. Search the build for `backdrop-filter` declarations on light-mode rules; each must include a `saturate()` between 1.4 and 1.65. Without it, the glass reads as grey film, not coloured frost.

5. **Backdrop is busy (gradient / image / mesh)** — inspect what sits behind every light-mode glass surface. If the answer is "flat white" or "flat solid colour," the glass cannot work. Either change the backdrop or drop the modifier for the light variant. Test by temporarily disabling the glass surface — if the page underneath is monochromatic, the glass had nothing to refract.

6. **`prefers-reduced-transparency` fallback handles light mode separately** — verify the media query block has an explicit light-mode fallback that swaps to an opaque background (typically `#FFFFFF` or near-white), not the dark-mode fallback colour. Auto-applied dark fallback colour on a light page is its own contrast disaster.

7. **Theme-toggle persistence works** — if the build has a light/dark toggle, verify (a) initial render respects `localStorage` then `prefers-color-scheme`, (b) the FOUC bootstrap script runs before CSS, (c) the toggle button's accessible label reflects the action ("Switch to light" / "Switch to dark") not the current state.

   How to verify: open the build, toggle theme, reload page — the chosen theme should persist. With localStorage cleared, the system pref should determine initial theme.

   Severity: **Major** if persistence broken; **Critical** if FOUC visible (page flashes wrong theme on load).

8. **Interactive state coverage — every button, link, input, toggle visible in BOTH themes** — this is the single most common ship-defect at this stage. Run the full `build-tactics.md` § Tactic 18 audit. Specifically inspect each primary CTA, secondary button, theme toggle, nav-CTA pill, mobile menu button, and form submit:

   - `color` and `background-color` produce a contrast ratio ≥ 4.5:1 (≥ 3:1 for large text) in BOTH themes
   - `:hover`, `:focus-visible`, `:active`, `:disabled` states all render visibly in BOTH themes
   - No hardcoded `color: #000000`, `color: #FFFFFF`, `color: black`, `color: white` inside any interactive selector that lacks a per-theme override block
   - `::placeholder` and `::selection` colours render legibly in BOTH themes

   How to verify: toggle the theme; for every visible button and link in viewport, inspect → DevTools "Contrast ratio" indicator. Any AA failure on a primary CTA is a delivery blocker.

   Severity: **Critical** for primary CTAs that are invisible (dark-on-dark or light-on-light); **Major** for secondary buttons or non-CTA interactives with the same defect.

### Tier-specific checks (run for each glass element per its declared tier)

Every glass element in the build declares a tier (1 / 2 / 3 / 4) — implicitly via the CSS classes used, explicitly via DESIGN.md `effects.liquid-glass.tier-distribution`. For each element, verify the tier-appropriate contract.

#### Tier 1 — Basic frosted glass

9. **Tier 1: backdrop-filter present + saturate ≥ 150%** — `blur` alone reads as fog. Industry standard is `blur(N) saturate(180%)` minimum. Audit each Tier 1 declaration: the `saturate()` argument must be ≥ 1.5 (or `≥ 150%`).

   Severity: **Major** if missing; "fog look" is a visible quality regression even when nothing else fails.

10. **Tier 1: no pseudo-element overlays** — Tier 1 is single-layer by definition. If a Tier 1 element has `::before` or `::after` adding gradients / highlights, it has silently escalated to Tier 2 without declaration. Either re-declare as Tier 2 in DESIGN.md, or remove the pseudo-elements.

   Severity: **Minor** (provenance / classification mismatch, not a visual defect).

#### Tier 2 — Apple-ish (CSS + pseudo-elements)

11. **Tier 2: `isolation: isolate` on the host** — without it, `mix-blend-mode: screen` on `::before` leaks to ancestor stacking contexts and produces unpredictable composites. Single most common Tier 2 bug. Mechanical check: every Tier 2 selector must declare `isolation: isolate`.

   Severity: **Critical** if missing — visible artefacts on hover / scroll.

12. **Tier 2: `overflow: hidden` on the host** — without it, the pseudo-element gradients paint outside the rounded corners. Mechanical check: every Tier 2 selector must declare `overflow: hidden` or equivalent (`overflow: clip`).

   Severity: **Major** — visible "leak" outside the border-radius.

13. **Tier 2: pseudo-elements have `pointer-events: none`** — without it, `::before`/`::after` swallow click / hover / focus events on the host. Mechanical check: every Tier 2 `::before` and `::after` must declare `pointer-events: none`.

   Severity: **Critical** — interactive Tier 2 surfaces become unclickable.

14. **Tier 2: host `background` is a gradient, not a flat rgba** — the `::before` highlight requires a gradient host background to fuse with; flat tint reads as layered slabs instead of glass. Mechanical check: host `background` (or `background-image`) must be a `linear-gradient(...)` or `radial-gradient(...)`.

   Severity: **Major** — quality defect, not a function defect.

15. **Tier 2: `mix-blend-mode` is `screen` (dark backdrop) or `soft-light` (light backdrop) — never `multiply`** — `multiply` over white surfaces produces near-black holes instead of highlights. Audit each `::before` declaration's blend mode.

   Severity: **Major** — visible inversion.

16. **Tier 2: light-mode adaptation present if theme-toggle ships** — `:root[data-theme="light"] .liquid-glass--tier2::before` must override `opacity` (`0.65 → 0.45`) and `mix-blend-mode` (`screen → soft-light`). Without it, the white-on-white highlight reads too bright in light mode.

   Severity: **Major** — defect specific to light mode.

#### Tier 3 — SVG displacement (gated)

17. **Tier 3: SVG `<filter>` with the referenced ID exists in the document** — `filter: url(#glass-refract)` to a non-existent ID silently no-ops, degrading Tier 3 to Tier 2 without warning. Mechanical check: every `filter: url(#X)` reference must have a matching `<filter id="X">` in the DOM.

   Severity: **Critical** — silent quality degradation.

18. **Tier 3: ONE element per page maximum** — multiple Tier 3 elements compound the filter cost (each `feTurbulence` runs independently) and produce GPU thermal throttling on mid-range mobile within 30 seconds. Audit: count `filter: url(#…)` references in the build that target SVG displacement filters. Must be ≤ 1.

   Severity: **Critical** — performance budget violation.

19. **Tier 3: `feDisplacementMap scale` ≤ 12** — above 12 the underlying text becomes unreadable; above 20 the surface looks broken. Audit: every `feDisplacementMap scale="N"` must satisfy `4 ≤ N ≤ 12`.

   Severity: **Major** — readability defect.

20. **Tier 3: Safari fallback present** — `@supports not (filter: url(#test-id)) { .tier3 { filter: none; } }` or equivalent feature-detect must downgrade Tier 3 to Tier 2 on Safari < 17. Without it, the page silently looks broken on Safari.

   Severity: **Major** — Safari users see worse visual than Tier 2 because the Tier 2 inset shadows + highlights are tuned for the displacement filter being present.

21. **Tier 3: `prefers-reduced-motion` disables the filter** — even static displacement is a vestibular concern for sensitive users. `@media (prefers-reduced-motion: reduce) { .tier3 { filter: none; } }` mandatory.

   Severity: **Major** — a11y violation.

22. **Tier 3: not on text-bearing surfaces** — Tier 3 distorts surface markings, which makes text unreadable. Verify Tier 3 elements are chrome (nav pills, controls, floating cards) — never article text or reading columns.

   Severity: **Critical** — text invisible / unreadable.

#### Tier 4 — WebGL (gated)

The WebGL track has its own four mandatory failure-mode guards in `effects/liquid-glass.md` § 7. Run that checklist; this section's items 17–22 do NOT apply to Tier 4.

23. **Tier 4: all four WebGL guards from `effects/liquid-glass.md` § 7 + `webgl-3d-tactics.md` § Pre-build checklist** — DOM mirror, `prefers-reduced-motion`, WebGL feature detect with DOM fallback, 8s load timeout. Same contract as the `dimension: shader-accents` axis.

   Severity: **Critical** if any guard missing.

## Common Regressions

- Glass applied to body copy containers — blur over scrolling prose fails contrast at mid-scroll and is in the forbidden-elements list
- Missing `box-shadow` on glass surfaces — elements lose spatial grounding and read as broken overlays against the backdrop
- `backdrop-filter` inside a CSS `transition:` property — GPU jank every frame; transition opacity or transform instead
- `-webkit-backdrop-filter` missing alongside `backdrop-filter` — glass silently fails on Safari without the prefix
- `prefers-reduced-transparency` block missing — accessibility violation with no visible signal in Chrome; must set macOS/Windows system preference to catch it in testing
- `prefers-reduced-motion` block missing when glass elements have transitions — easy to skip because the glass "looks fine" in a standard browser test
- Refused-style override with ≥2 glass elements — single-element rule means one; a second glass element makes it a pattern and the override is void
- Variant undeclared in provenance — `regular` is the default but must be explicit for audits
- WebGL refraction track active without DOM mirror — canvas is invisible to screen readers; real content must exist in the DOM with `aria-hidden="true"` on the canvas
- Vibrant or photographic backdrop absent — glass over a flat near-solid background is invisible; verify the backdrop has enough visual complexity before applying the modifier
- Blur radius creeping past 24px on desktop to "look more impressive" — exceeds the hard ceiling; document a marquee-modal exception or bring it back in range
- **Light-mode glass with dark-mode tokens** — light variant ships with `rgba(white, 0.05)` background and white hairline (carried over from dark default); surfaces are invisible. Run the 5-rule light-mode check.
- **Light-mode glass without `saturate()` boost** — most common silent failure; glass reads as grey film instead of coloured frost. Add `saturate(1.45–1.65)` to every light-mode `backdrop-filter` declaration.
- **Light-mode glass over flat-white page** — modifier silently fails because there's nothing to refract. Either add a busy backdrop (atmosphere / gradient / image) or drop the modifier for the light variant.
- **FOUC on theme load** — page renders dark briefly before the toggle JS runs, then flashes to light. Bootstrap script must be inline in `<head>` BEFORE any stylesheets, set `data-theme` on `<html>` synchronously.
- **`prefers-reduced-transparency` light fallback uses dark surface colour** — if the media query block doesn't differentiate light vs dark, the light fallback inherits the dark fallback colour and the page renders with dark cards on light bg. Mandatory: separate fallback per theme.
