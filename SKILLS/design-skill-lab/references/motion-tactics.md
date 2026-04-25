# Motion Tactics

Load in **Phase 3** whenever `style-tuning.axes.motion.value` is `medium` or `high`. Skip if `low` (CSS transitions are sufficient — no orchestration needed).

This file defines the technical contract per motion tier. Without it, "high" is interpreted as "more CSS animations" — which is medium dressed up. Real "high" requires GSAP-tier orchestration and a different mental model.

---

## Tier definitions — what each value commits to

### `motion: low`
**No file needed.** CSS `transition` on hover/focus, occasional `transform: translateY()` on cards. Static page otherwise. No JS animation runtime.

Examples: brutalist landing pages, editorial portfolios, sanctuary-tech, anything where the type carries the weight.

### `motion: medium`
**Load this file's "Medium contract" section.** CSS animations (`@keyframes`) for ambient motion (float, pulse, gradient-shift) + IntersectionObserver for scroll-reveal. No JS animation library required. Ships with native APIs only.

Examples: warm-editorial defaults, technical-refined, basalt-ecommerce, most product sites.

### `motion: high`
**Load this file's "High contract" section.** GSAP-tier orchestration: ScrollTrigger sequences, SplitText character/word reveals, parallax layers, scroll-driven storytelling, FLIP transitions, MotionPath. Animation runtime ships with the page (~30–60kb).

Examples: agency sites, brand showcases, immersive landing pages, anything that wants to feel "designed-by-a-studio" rather than "built-by-a-team".

---

## Decision rule — when to commit to `high`

Before generating any markup with `motion: high`, verify:

- [ ] User explicitly chose `high` in the style-tuning interview, OR delegated and the brief explicitly mentions agency / immersive / GSAP / "wow factor" / scroll-driven storytelling.
- [ ] Page has at least 3 distinct motion moments planned (hero entrance + scroll sequence + transition between sections is the minimum). One animated element does not justify GSAP weight.
- [ ] Performance budget allows ~30–60kb of JS for animation. If the page is performance-critical (LCP <2.5s on 3G), drop to `medium` and document the trade-off.
- [ ] Reduced-motion fallback is part of the plan, not an afterthought (see §Accessibility).

If any of these fail, demote to `medium` and note the reason in the delivery summary.

---

## Medium contract — CSS-only orchestration

### Allowed techniques

- `transition` on hover / focus / aria-state changes (200–400ms typical, ease-out or cubic-bezier(.2,.7,.2,1))
- `@keyframes` for ambient loops: `float`, `pulse`, `gradient-shift`, `shimmer`. Loop duration 3–10s, `ease-in-out`, `infinite`.
- `IntersectionObserver` for scroll-reveal. Pattern: opacity 0 → 1 + transform translateY(16–24px) → 0, 600ms cubic-bezier(.2,.7,.2,1), threshold 0.1–0.15, unobserve after first reveal.
- View Transitions API (`document.startViewTransition`) for page-to-page navigation if the framework supports it.
- `prefers-reduced-motion` media query disables all of the above.

### Forbidden at this tier

- ❌ External animation libraries (GSAP, Motion One, Anime.js, Framer Motion). If you reach for one, either commit to `high` or stay CSS-only.
- ❌ Scroll-driven JS sequences with multiple synchronized properties (that's `high`'s job).
- ❌ Parallax that depends on scroll position math.
- ❌ Character-by-character text reveals (CSS-only attempts always look amateur — defer to `high` with SplitText).

### Pre-build checklist

- [ ] `prefers-reduced-motion: reduce` query is present and disables all keyframe loops + scroll-reveals
- [ ] No `IntersectionObserver` polyfill needed (modern browsers only — document if supporting <Edge 79)
- [ ] All transitions are ≤500ms (longer feels sluggish on UI)
- [ ] All ambient loops are ≥3s (faster reads as anxious)
- [ ] No animation depends on a layout that breaks at narrow widths

---

## High contract — GSAP-tier orchestration

### Stack choice

Project default: **GSAP 3.12+** with the plugins Webflow supports natively. This matches the Flowbridge / Flow-Goodies workflow and ships with predictable license terms (free core; Club GSAP adds the premium plugins).

```html
<!-- Core (free, ~25kb gzipped) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/ScrollTrigger.min.js"></script>

<!-- Free plugins worth using anywhere -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/Flip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/Observer.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/EasePack.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/MotionPathPlugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/CustomEase.min.js"></script>
```

**Premium plugins (Club GSAP — paid).** Webflow Enterprise includes Club GSAP licensing for the user's hosted projects, but the build itself is portable. If the user is on Webflow paid plans these are valid; otherwise document that the project requires a Club GSAP membership.

| Plugin | Why use | License |
|---|---|---|
| **SplitText** | Character / word / line text reveals. The single most effective "feels designed" move. | Club |
| **ScrollSmoother** | Adds inertia to native scroll. Use sparingly — can break native browser scroll behaviour. | Club |
| **DrawSVG** | Animates `stroke-dashoffset` on SVG paths. Great for line illustrations and signature reveals. | Club |
| **MorphSVG** | Morphs one SVG path into another. Used for icon transitions and shape storytelling. | Club |
| **ScrambleText** | Character-shuffle reveal for headlines. Use once per page, ideally in hero. | Club |
| **CustomBounce / CustomWiggle** | Pre-shaped easings for impact moments. Better than hand-tuned cubic-bezier. | Club |
| **Inertia / Physics2D / PhysicsProps** | Throwable / spring-driven UI. Required for Draggable cards and physics-based hero illustrations. | Club |
| **MotionPathHelper** | Visual editor for MotionPath curves. Build-time only — strip from production. | Club |

### Six core techniques for `high`

#### 1. Scroll-driven hero entrance
Stagger headline lines, supporting paragraph, CTA, and hero illustration on page load. Use `gsap.timeline()` with cubic-bezier or CustomEase, durations 0.6–1.2s, stagger 0.08–0.12s.

```js
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.9 }});
tl.from(".hero-headline", { y: 40, opacity: 0 })
  .from(".hero-lead", { y: 24, opacity: 0 }, "-=0.6")
  .from(".hero-cta", { y: 16, opacity: 0 }, "-=0.5")
  .from(".hero-illus", { scale: 0.96, opacity: 0, duration: 1.2 }, "-=0.8");
```

#### 2. SplitText line/word reveal on section headlines
Most-used premium plugin. Character splits look gimmicky; word and line splits look editorial. Default to **lines**.

```js
const split = new SplitText(".section-headline", { type: "lines", linesClass: "line" });
gsap.from(split.lines, {
  scrollTrigger: { trigger: ".section-headline", start: "top 80%" },
  yPercent: 100,
  opacity: 0,
  duration: 0.9,
  stagger: 0.08,
  ease: "power3.out"
});
```

Wrap each `.line` in `overflow: hidden` on the parent for the "rolling-up from below the line" effect.

#### 3. ScrollTrigger pinned sequences
Pin a section while a sequence plays out. Use for product reveals, before/after comparisons, multi-step explainers.

```js
gsap.timeline({
  scrollTrigger: {
    trigger: ".pinned-section",
    start: "top top",
    end: "+=200%",
    scrub: 0.5,
    pin: true
  }
})
.to(".step-1", { opacity: 0 })
.from(".step-2", { opacity: 0 }, "<")
.to(".step-2", { opacity: 0 })
.from(".step-3", { opacity: 0 }, "<");
```

Budget: at most one pinned sequence per page. Multiple pins compound and feel jarring.

#### 4. Parallax depth layers
Background, midground, foreground all scroll at different rates. ScrollTrigger handles the math.

```js
gsap.utils.toArray(".parallax-layer").forEach(layer => {
  const depth = parseFloat(layer.dataset.depth) || 0.3;
  gsap.to(layer, {
    yPercent: -50 * depth,
    ease: "none",
    scrollTrigger: { trigger: layer, start: "top bottom", end: "bottom top", scrub: true }
  });
});
```

Markup: `<div class="parallax-layer" data-depth="0.6">…</div>`. Depth 0.2–0.4 = subtle, 0.5–0.8 = obvious, >1 = inverse direction.

#### 5. FLIP transitions for layout changes
When a card expands, a list item reorders, or a tab switches — use Flip plugin instead of CSS transitions for buttery layout interpolation.

```js
const state = Flip.getState(".cards");
// mutate the DOM (sort, filter, expand)
Flip.from(state, { duration: 0.6, ease: "power2.inOut", absolute: true });
```

#### 6. CustomEase for signature easing
Generic eases (power2, sine) feel default. CustomEase + a hand-tuned curve is the difference between "animated" and "designed".

```js
CustomEase.create("verum-out", "M0,0 C0.2,0 0.1,1 1,1");
gsap.to(".hero-cta", { y: 0, ease: "verum-out", duration: 1 });
```

### Anti-patterns at this tier

- ❌ **GSAP for everything**, including hover states. Hover is still CSS. GSAP is for orchestration, not state.
- ❌ **Multiple ScrollTrigger.create() calls without batching.** Use `gsap.utils.toArray().forEach()` or a single timeline with multiple triggers.
- ❌ **Parallax on mobile.** Always `ScrollTrigger.matchMedia({"(min-width: 768px)": ...})`. Mobile parallax is jank.
- ❌ **Animations that block LCP.** Hero entrance starts after `DOMContentLoaded`, not on `load`. The headline must paint before GSAP overrides it.
- ❌ **Pinned sections taller than the viewport.** Pin only sections shorter than `100vh` — taller pins create scroll dead-zones.
- ❌ **Scrub: true with heavy timelines.** Scrub recomputes every frame; keep tweened properties to ≤4 simultaneously per scrub timeline.

### Pre-build checklist

- [ ] GSAP version pinned (3.12+ at time of writing — verify current LTS at build time)
- [ ] All required plugins listed in delivery summary (especially Club GSAP plugins — license implication)
- [ ] `prefers-reduced-motion: reduce` disables all GSAP animations OR replaces them with instant-state versions
- [ ] No animation runs before `DOMContentLoaded` (avoid LCP regression)
- [ ] Mobile fallback: complex sequences (parallax, pin, scrub) gated behind `matchMedia("(min-width: 768px)")`
- [ ] `gsap.config({ trialWarn: false })` in dev builds; production should not log warnings
- [ ] All `ScrollTrigger` instances have `markers: false` in production (markers are dev-only)
- [ ] Bundle size measured: GSAP core + plugins should not exceed ~80kb gzipped total

---

## Webflow-specific notes

When the build will deploy on Webflow:

- Club GSAP is **bundled** with paid Webflow plans — premium plugins work without separate licensing on Webflow-hosted sites.
- Webflow's native interactions (IX2) can coexist with custom GSAP, but should not target the same elements. Pick one orchestration layer per element.
- Inject GSAP CDN scripts in **Project Settings → Custom Code → Footer**, not in the page-level Embed (so they load once across the site).
- For Flow-Goodies / Flowbridge integrations, GSAP is already loaded — don't re-import. Check `window.gsap` before initializing.

---

## Accessibility — `prefers-reduced-motion`

Non-negotiable at every tier above `low`.

```js
// At the top of any GSAP setup
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  gsap.set("*", { clearProps: "all" });
  // OR: replace timelines with instant-state versions
  return;
}
```

For CSS-only motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

The reduced-motion fallback is **not** "no animation" — content must still appear. Replace 600ms reveals with 0ms reveals (instant), not "never reveal".

---

## Performance budget per tier

| Tier | JS budget | LCP impact | First-input delay |
|---|---|---|---|
| low | 0 | none | none |
| medium | <5kb (IntersectionObserver polyfill if needed) | none | none |
| high | 30–80kb (GSAP + plugins) | <100ms if loaded after LCP | <50ms |

If `high` pushes the page above 80kb of animation JS, demote to `medium` for the parts that don't need GSAP and reserve GSAP for the 2–3 signature moments.

---

## Audit questions (Phase 4 motion lens)

When `motion != low`, run these in addition to the style-specific review:

1. **Does each animation serve the content?** "It moves because it can" is not a reason. If removing the animation doesn't reduce comprehension, cut it.
2. **Does the page work with motion disabled?** Test with `prefers-reduced-motion: reduce`. Content should still be readable, navigable, and complete.
3. **Is GSAP doing what CSS could do?** Hover lifts, simple fades, ambient float — these are CSS jobs. GSAP for orchestration only.
4. **Is mobile motion appropriate?** Parallax and pin sequences should be desktop-only or simplified on mobile. Test at 375px width.
5. **Does the hero entrance block LCP?** Headline text must paint within LCP budget (<2.5s on 3G). If GSAP is hiding the headline before reveal, the headline isn't in the LCP — that's a regression.
6. **Is there a single signature motion moment?** A page with 12 equal-weight animations has no hierarchy. One memorable moment > many minor ones.
7. **Are easings consistent across the page?** Mixing power2, power3, expo, and elastic on the same page reads as un-designed. Pick 1–2 eases and a CustomEase signature; stick with them.
