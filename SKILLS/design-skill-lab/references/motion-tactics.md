# Motion Tactics

Load in **Phase 3 Step 3.0.05** whenever `style-tuning.axes.motion.value` is `medium` or `high`. Skip if `low` (CSS transitions are sufficient — no orchestration needed).

This file defines the **technical contract** per motion tier. Without it, "high" is interpreted as "more CSS animations" — which is medium dressed up. Real "high" requires GSAP-tier orchestration and a different mental model.

**Read `motion-principles.md` BEFORE this file.** Tactics without principles produces mechanical "more animation" — not design. Principles defines vocabulary (animation vs micro-interaction vs functional motion), the canonical duration table, easing intent, C.U.R.E. audit framework, GPU-only properties, and WCAG criteria. This file is the *how*; principles is the *what and why*.

**See also: `loader-patterns.md`** — page loaders are a separate concern (governed by Axis 9 `page-load`, not this file's `motion` axis). A page can have `motion: low` + `page-load: branded-intro`, or `motion: high` + `page-load: none`. They are orthogonal. Branded intro loaders DO count toward this file's "3 distinct motion moments" budget when justifying GSAP at the High tier (see Decision rule below).

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
- [ ] Page has at least 3 distinct motion moments planned (hero entrance + scroll sequence + transition between sections is the minimum). One animated element does not justify GSAP weight. **A `page-load: branded-intro` loader counts as one moment** — pair it with hero entrance + at least one scroll moment to clear the bar.
- [ ] Performance budget allows ~30–60kb of JS for animation. If the page is performance-critical (LCP <2.5s on 3G), drop to `medium` and document the trade-off. **A branded loader adds 600-2500ms of perceived load time on top of GSAP weight** — factor this in.
- [ ] Reduced-motion fallback is part of the plan, not an afterthought (see §Accessibility). Loaders skip entirely under reduced motion (see `loader-patterns.md` § Failure 4).

If any of these fail, demote to `medium` and note the reason in the delivery summary.

---

## Medium contract — CSS-only orchestration

### Duration & easing — pull from principles

Durations and easing intent are **canonical in `motion-principles.md`** (§ Temporal design and § Easing). Do not invent values. Quick recap for the medium tier:

- Hover / micro-interaction: 150–250ms, ease-out
- UI transitions (dropdown, tooltip): 200–300ms, ease-out
- Modal entrance: 300–400ms, ease-out
- Hero scroll reveal: 600–900ms, ease-out signature curve
- Ambient loops: 3–10s, ease-in-out, infinite

If the brand calls for a duration outside these ranges, document the exception in DESIGN.md as a brand-driven decision — not "I felt 450ms was right".

### GPU-only rule — non-negotiable

Animate **only** `transform` and `opacity` (and `filter` / `clip-path` with awareness). These are handled by the compositor and run on the GPU at 60fps. Animating Layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`, `border-width`, `font-size`) forces full re-layout per frame and produces jank.

The full forbidden list and substitution patterns are in `motion-principles.md` § Performance. The summary: if the property changes the size or position of a box in the layout flow, don't animate it — animate a `transform` on a wrapper instead.

### Allowed techniques

- `transition` on hover / focus / aria-state changes (durations per principles table, ease-out for entering, `cubic-bezier(.2,.7,.2,1)` is the skill's default signature ease)
- `@keyframes` for ambient loops: `float`, `pulse`, `gradient-shift`, `shimmer`. Loop duration 3–10s, `ease-in-out`, `infinite`.
- `IntersectionObserver` for scroll-reveal. Pattern: opacity 0 → 1 + transform translateY(16–24px) → 0, 600–900ms ease-out, threshold 0.1–0.15, unobserve after first reveal.
- View Transitions API (`document.startViewTransition`) for page-to-page navigation if the framework supports it.
- `prefers-reduced-motion` media query disables all of the above.

### Forbidden at this tier

- ❌ External animation libraries (GSAP, Motion One, Anime.js, Framer Motion). If you reach for one, either commit to `high` or stay CSS-only.
- ❌ Scroll-driven JS sequences with multiple synchronized properties (that's `high`'s job).
- ❌ Parallax that depends on scroll position math.
- ❌ Character-by-character text reveals (CSS-only attempts always look amateur — defer to `high` with SplitText).
- ❌ **Reveal animations gated only by `.reveal { opacity: 0 }` without a JS-ready guard.** If JS fails or runs late, content stays invisible. Required pattern below.

### Required pattern — progressive-enhancement gate for reveals

Every reveal animation in the medium tier (and high tier) must use the `.js-ready` progressive-enhancement gate. The hidden initial state (`opacity: 0`) only applies once JS confirms it can run the animation. If JS fails for any reason — error, blocked script, slow network — content stays fully visible.

```css
/* WITHOUT .js-ready gate, .reveal stays at opacity:0 forever if JS fails */
.js-ready .reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 600ms cubic-bezier(.2,.7,.2,1),
              transform 600ms cubic-bezier(.2,.7,.2,1);
}
.js-ready .reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```js
(function() {
  // STEP 1 — Mark JS as ready FIRST. This enables the .reveal hidden state in CSS.
  // Any line above this that throws will leave .reveal fully visible (graceful fallback).
  document.documentElement.classList.add('js-ready');

  // STEP 2 — Defensive: if IntersectionObserver missing (very old browsers), show everything.
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    return;
  }

  // STEP 3 — Respect prefers-reduced-motion (skip animation, show immediately).
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    return;
  }

  // STEP 4 — Standard observer.
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
})();
```

The `.js-ready` gate is the failure-mode fix for the Spritify oneshot bug, where the hero testimonial card shipped invisible when JS hadn't run yet. **This pattern is also documented in build-tactics.md Tactic 17.4** as part of the surface-context contract — they're the same defect class (content invisible despite valid markup).

### Pre-build checklist

- [ ] `prefers-reduced-motion: reduce` query is present and disables all keyframe loops + scroll-reveals
- [ ] No `IntersectionObserver` polyfill needed (modern browsers only — document if supporting <Edge 79)
- [ ] All transitions are ≤500ms (longer feels sluggish on UI)
- [ ] All ambient loops are ≥3s (faster reads as anxious)
- [ ] No animation depends on a layout that breaks at narrow widths
- [ ] **If reveal animations used: `.js-ready` gate present in CSS** (`.js-ready .reveal { opacity: 0 }`, not bare `.reveal { opacity: 0 }`)
- [ ] **If reveal animations used: JS adds `js-ready` class to `document.documentElement` as the FIRST line** of the IIFE (before any other logic that could throw)
- [ ] **If reveal animations used: IntersectionObserver fallback present** (if API missing → show everything)
- [ ] **Disable-JS test passes**: page renders fully readable in DevTools with JS disabled

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

**⚠️ Critical CDN behaviour:** the public CDN (`cdn.jsdelivr.net/npm/gsap@3.12/dist/<plugin>.min.js`) loads Club plugins without throwing errors but they **run in trial mode** for unlicensed origins (`file://`, custom domains, GitHub Pages, Vercel free, etc.). In trial mode, the constructor returns an object that does NOT animate. The bug is silent — no console error, no thrown exception, just no animation. **Every Club plugin used in a build that may deploy outside Webflow paid plans needs a fallback chain.** See § "SplitText is Club GSAP — fallback chain required for standalone deploys" under Technique 2 for the canonical pattern.

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

##### ⚠️ SplitText is Club GSAP — fallback chain required for standalone deploys

**The CDN trap:** `https://cdn.jsdelivr.net/npm/gsap@3.12/dist/SplitText.min.js` exists and the `<script>` tag loads without error, but the plugin **runs in trial mode** for unlicensed origins. In trial mode:
- On `gsap.com`, `localhost`, and Webflow paid domains → SplitText works normally
- On standalone HTML files (`file://`, custom domains, GitHub Pages, Vercel free, etc.) → SplitText constructor returns an object but **does not animate** — text stays in initial state forever

The bug is silent. The build appears to ship with SplitText, the `<script>` tag is there, the constructor doesn't throw, but the user never sees the animation. The skill's previous Creative Studio heavy-motion build hit this exact failure: SplitText "implemented" in code, never visible to the user.

**Required fallback chain.** Every SplitText usage must have a graceful fallback to vanilla word-split that animates equivalently. Pattern:

```js
function revealHeadlineLines(headline) {
  if (!headline) return;

  // Hidden initial state — applied regardless of which path animates
  function setHidden(items) {
    gsap.set(items, { yPercent: 100, opacity: 0 });
  }

  // Reveal animation — same params for both paths
  function reveal(items) {
    gsap.to(items, {
      yPercent: 0,
      opacity: 1,
      duration: 0.9,
      stagger: 0.08,
      ease: SIGNATURE_EASE,
      scrollTrigger: { trigger: headline, start: "top 80%" }
    });
  }

  // Path 1 — SplitText (Club, Webflow paid, gsap.com, localhost)
  if (window.SplitText) {
    try {
      const split = new SplitText(headline, { type: "lines", linesClass: "split-line" });
      // Wrap each line in overflow:hidden via inline span
      split.lines.forEach(line => {
        const wrap = document.createElement("span");
        wrap.style.display = "block";
        wrap.style.overflow = "hidden";
        line.parentNode.insertBefore(wrap, line);
        wrap.appendChild(line);
      });
      // Verify SplitText actually split (trial mode sometimes returns 0 lines)
      if (split.lines && split.lines.length > 0) {
        setHidden(split.lines);
        reveal(split.lines);
        return; // success
      }
    } catch (e) {
      // SplitText present but errored — fall through to vanilla
    }
  }

  // Path 2 — Vanilla word-split fallback (works everywhere, no Club required)
  // Splits text by words, wraps each in span with overflow:hidden parent.
  // Visually equivalent to SplitText word-mode (slightly less precise than line-mode
  // because words wrap mid-line, but reveal effect is the same).
  const text = headline.textContent;
  const words = text.split(/(\s+)/); // keep whitespace as separate items
  headline.textContent = "";
  const items = [];
  words.forEach(word => {
    if (/^\s+$/.test(word)) {
      // Whitespace — append as text node, no animation
      headline.appendChild(document.createTextNode(word));
    } else {
      const wrap = document.createElement("span");
      wrap.style.display = "inline-block";
      wrap.style.overflow = "hidden";
      const inner = document.createElement("span");
      inner.style.display = "inline-block";
      inner.textContent = word;
      wrap.appendChild(inner);
      headline.appendChild(wrap);
      items.push(inner);
    }
  });
  setHidden(items);
  reveal(items);
}
```

**Decision rule** for which path to pursue at build time:

| Deploy target | Path |
|---|---|
| Webflow (paid plan with Club bundled) | SplitText — animation is line-precise |
| `localhost` dev / `gsap.com` | SplitText works |
| Standalone HTML file (verification builds, file://) | Vanilla fallback always — SplitText silent fails |
| Custom domain not on Webflow | Vanilla fallback — assume Club not licensed |
| Unknown / building portable artifact | Implement fallback chain (above) — works in all cases |

**Audit test (high tier):** open the build with **Web Inspector / Console** and check for `[SplitText]` warnings. If you see "SplitText only runs free on club domains" or similar trial-mode warning, the fallback chain is needed. If you see no warnings AND `split.lines.length > 0`, SplitText is working.

**Heuristic for new builds:** unless the deploy target is confirmed Webflow paid, **always implement the fallback chain**. The cost is ~30 lines of JS; the benefit is the headline reveal actually animates.

**Same rule applies to other Club plugins:** SplitText, ScrollSmoother, DrawSVG, MorphSVG, ScrambleText, Inertia, Physics2D/PhysicsProps, MotionPathHelper. None work standalone without Club license. Each needs a vanilla fallback OR an honest documented skip ("animation X requires Webflow Club; standalone shows static state").

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
- ❌ **GSAP `gsap.from()` on hero content without `.js-ready` gate or `clearProps`.** If GSAP fails to load (CDN down, blocked, slow), the page hero stays at the `from` state forever. Use `.js-ready` gate on hero opacity, OR use `gsap.set()` to establish the hidden state only after GSAP confirms ready.

### Pre-build checklist

- [ ] GSAP version pinned (3.12+ at time of writing — verify current LTS at build time)
- [ ] All required plugins listed in delivery summary (especially Club GSAP plugins — license implication)
- [ ] `prefers-reduced-motion: reduce` disables all GSAP animations OR replaces them with instant-state versions
- [ ] No animation runs before `DOMContentLoaded` (avoid LCP regression)
- [ ] Mobile fallback: complex sequences (parallax, pin, scrub) gated behind `matchMedia("(min-width: 768px)")`
- [ ] `gsap.config({ trialWarn: false })` in dev builds; production should not log warnings
- [ ] All `ScrollTrigger` instances have `markers: false` in production (markers are dev-only)
- [ ] Bundle size measured: GSAP core + plugins should not exceed ~80kb gzipped total
- [ ] **Hero / above-the-fold content is visible without GSAP**: either use `.js-ready` CSS gate (medium-tier pattern, preferred) OR run `gsap.set(".hero", {opacity: 0})` AFTER confirming `window.gsap` exists. Never start hero in `opacity: 0` purely via CSS without a JS-ready guard.
- [ ] **Disable-JS test passes** (DevTools → Sources → Disable JavaScript → reload): hero is readable, page navigation works, content not gated behind animation

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

When `motion != low`, run these in addition to the style-specific review.

**The principles file owns the design lens.** The full audit checklist (taxonomy classification, four-pillars per micro-interaction, C.U.R.E. framework, easing intent, 3-flash rule) lives in `motion-principles.md` § Audit checklist. Run that first; the questions below are the *tactical* lens that complements it.

1. **C.U.R.E. per moment.** Run Context / Usefulness / Restraint / Emotion against every motion moment in the build. Failure on Usefulness alone = cut. (Full framework: `motion-principles.md` § C.U.R.E.)
2. **Does the page work with motion disabled?** Test with `prefers-reduced-motion: reduce`. Content should still be readable, navigable, and complete.
3. **Is GSAP doing what CSS could do?** Hover lifts, simple fades, ambient float — these are CSS jobs. GSAP for orchestration only.
4. **Is mobile motion appropriate?** Parallax and pin sequences should be desktop-only or simplified on mobile. Test at 375px width.
5. **Does the hero entrance block LCP?** Headline text must paint within LCP budget (<2.5s on 3G). If GSAP is hiding the headline before reveal, the headline isn't in the LCP — that's a regression. The `.js-ready` gate is the fix.
6. **Is there a single signature motion moment?** A page with 12 equal-weight animations has no hierarchy. One memorable moment > many minor ones.
7. **Are easings consistent across the page?** Mixing power2, power3, expo, and elastic reads as un-designed. Pick 1–2 generic curves + 1 signature ease; stick with them. (Easing intent map: `motion-principles.md` § Easing.)
8. **5-second rule (WCAG 2.2.2).** Any auto-running motion >5 seconds must have a pause control OR be gated behind `prefers-reduced-motion`. This applies to: auto-playing video, auto-rotating carousels, persistent background animations. Decorative ambient loops (subtle float, breathing logo at <5% scale change) are usually fine — judgment call.
9. **GPU-only check.** Grep the build for animated `width`, `height`, `top`, `left`, `margin` properties. Replace with `transform` equivalents. Layout-triggering properties on a 60fps animation = jank.
10. **Duration sourced from canonical table.** Every duration in the build either comes from `motion-principles.md` § Temporal design table OR is documented as a brand-driven exception in DESIGN.md.
