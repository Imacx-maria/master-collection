# Gradient Tactics

Load in **Phase 3** whenever the chosen style or brief specifies a gradient as a load-bearing visual element — atmospheric backdrops, glass border shells, glow blooms, mesh fields, or animated colour flows. Skip if gradients are decorative-only (e.g. a single subtle button hover).

This file is the **technique playbook**. Style files name *which* recipe to reach for; this file owns the *how*. Without it, "gradient" gets interpreted as `linear-gradient(45deg, red, blue)` and ships flat. Real modern gradients are layered, often animated, and chosen against a performance/feel matrix — that decision lives here.

**Read alongside `motion-tactics.md`** when the gradient is animated. The two files overlap on GPU-only discipline and `prefers-reduced-motion` fallbacks; tactics are not duplicated here.

---

## The decision tree — pick the recipe before writing CSS

Three questions, in order:

1. **Static or animated?** Static = composition-only (layered radials, grain overlay, gradient border). Animated = motion is part of the look (smoky flow, breathing bloom, shader field).
2. **If animated — what runtime?** CSS `background-position` shift / CSS `@property` / WebGL shader / SVG `feTurbulence`. Each has a different perf and feel cost; the comparison table below decides.
3. **Light-mode or dark-mode?** Dark-mode gradients can be saturated and luminous because the surface is absorbing. Light-mode gradients must be desaturated and bounded or they read as muddy poster art. The recipes below note where they apply.

If the brief doesn't specify these three, ask before writing markup. "Gradient" alone is not a spec.

---

## Recipe 1 — Layered radial mesh (the "fake mesh" hack)

**What it is.** Multiple `radial-gradient()` declarations stacked in `background-image`, each with low opacity, positioned at different points, blending into an organic mesh. Replaces the deprecated `conic-gradient` mesh attempts and the (still-unshipped) CSS `mesh-gradient` proposal.

**When to reach for it.** Atmospheric backdrops where you want the *feel* of a Photoshop mesh (Stripe-style fluid colour) without WebGL weight. The Nexus screenshot's blue planet-glow blooms are this recipe. Works in dark mode (saturated blooms on near-black) and light mode (desaturated washes on warm cream).

**Dark-mode pattern:**

```css
.bloom-backdrop {
  background-color: #030508;
  background-image:
    radial-gradient(ellipse 60% 40% at 20% 30%, rgba(99, 102, 241, 0.18), transparent 60%),
    radial-gradient(ellipse 50% 35% at 80% 70%, rgba(139, 92, 246, 0.15), transparent 65%),
    radial-gradient(ellipse 40% 30% at 50% 90%, rgba(59, 130, 246, 0.12), transparent 70%);
  background-repeat: no-repeat;
  background-attachment: fixed;
}
```

Three blooms is the sweet spot. Five+ blobs muddies into a single grey wash. Each bloom needs ≥40% transparent fade so they overlap without seam lines.

**Light-mode pattern (desaturated, bounded):**

```css
.bloom-backdrop-light {
  background-color: #FAFAF7;
  background-image:
    radial-gradient(ellipse 50% 40% at 25% 20%, rgba(254, 215, 170, 0.40), transparent 60%),
    radial-gradient(ellipse 45% 35% at 75% 80%, rgba(254, 202, 202, 0.30), transparent 65%);
  background-repeat: no-repeat;
}
```

Light-mode opacities are 2–3× higher than dark-mode (because the warm cream substrate doesn't absorb the colour). Use pastel/desaturated stops; saturated colours on light backgrounds always read as cheap.

**Pre-build checklist:**
- [ ] No more than 3–4 radial layers (more = mud)
- [ ] Each layer fades to `transparent` at ≥60% radius (hard stops create seam lines)
- [ ] Background-color set as fallback (gradients can fail to render in some embed contexts)
- [ ] If full-bleed: `background-attachment: fixed` so the bloom doesn't scroll with content (parallax illusion, free)
- [ ] Test against actual content above the gradient — if text contrast drops below 4.5:1 over any bloom centre, reduce the bloom opacity
- [ ] **Every opaque card sitting ON TOP of the bloom backdrop has its own `box-shadow` (typically `0 25px 50px -12px rgba(0,0,0,0.40)` or accent-tinted equivalent).** Without a shadow, the bloom shows past the card edges and the eye reconstructs an apparent "ghost outline" offset from the card — the page reads as broken. The shadow softens the card-to-bloom transition so the bloom looks like ambient light rather than an unintended halo. This is the highest-frequency Bloom-recipe regression. **Mechanical check:** `grep "box-shadow" <build-file>` — every card class on the page must have one.

---

## Recipe 2 — Smoky linear flow

**What it is.** A wide `linear-gradient` (often diagonal) animated via `background-position` shift, producing the impression of slow atmospheric movement. The Neuform "Cognitive Calibration" screenshot's wavy field is this recipe (with grain overlay layered on top).

**When to reach for it.** When you want motion in the backdrop but can't afford WebGL weight. Pairs with serif-editorial typography where the gradient acts as ambient texture, not feature. Dark-mode native; rarely works in light-mode without dropping saturation to near-grey.

**Static base:**

```css
.flow-backdrop {
  background:
    linear-gradient(135deg,
      #030508 0%,
      #0a0a14 25%,
      #1a1530 50%,
      #0a0a14 75%,
      #030508 100%);
  background-size: 400% 400%;
}
```

The 400% size is the trick — the gradient is much wider than the viewport, so animating `background-position` slides different colour zones into view without the gradient endpoints ever showing.

**Animation — CSS shift (low cost):**

```css
.flow-backdrop {
  animation: flow-shift 30s ease-in-out infinite;
}
@keyframes flow-shift {
  0%, 100% { background-position: 0% 50%; }
  50%      { background-position: 100% 50%; }
}
@media (prefers-reduced-motion: reduce) {
  .flow-backdrop { animation: none; background-position: 50% 50%; }
}
```

15–30 seconds is the right range. <10s feels anxious; >60s reads as broken (user can't perceive the motion).

**Animation — `@property` API (modern, cleaner):**

```css
@property --flow-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 135deg;
}
.flow-backdrop {
  background: linear-gradient(var(--flow-angle), #030508, #1a1530, #030508);
  transition: --flow-angle 8s ease-in-out;
}
.flow-backdrop:hover { --flow-angle: 225deg; }
```

`@property` lets the browser interpolate the angle directly — no background-position hack needed. Browser support is good (Chrome 85+, Safari 16.4+, Firefox 128+), but the `background-size: 400%` shift has wider support for older targets.

**Pre-build checklist:**
- [ ] `background-size: 400%` (or larger) — smaller and the gradient endpoints become visible
- [ ] Animation duration 15–30s (the human-perceptible-but-not-anxious range)
- [ ] Easing is `ease-in-out` (not `linear` — linear motion feels mechanical)
- [ ] `prefers-reduced-motion` disables the animation and pins to a midpoint
- [ ] Maximum two flow gradients on a single page (more compounds into chaos)

---

## Recipe 3 — Grainy gradient (SVG feTurbulence overlay)

**What it is.** An SVG noise texture layered over a gradient via `mix-blend-mode: overlay` (or a transparent PNG). Adds an analog/film-grain quality that prevents the gradient from looking digitally clean. The Neuform smoky field uses this — without it, the gradient would look generic.

**When to reach for it.** Editorial / serif-driven styles where the gradient is supposed to feel printed or atmospheric, not synthetic. Dark mode benefits more (grain reads on near-black); light mode usage requires reducing grain opacity to ~20%.

**SVG-inline pattern (sharp, scalable, controllable):**

```html
<div class="grainy-backdrop">
  <svg class="grain" xmlns="http://www.w3.org/2000/svg">
    <filter id="noiseFilter">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <rect width="100%" height="100%" filter="url(#noiseFilter)" opacity="0.4"/>
  </svg>
  <!-- gradient layers behind -->
</div>
```

```css
.grainy-backdrop { position: relative; }
.grainy-backdrop .grain {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  mix-blend-mode: overlay;
  opacity: 0.3;
  pointer-events: none;
}
```

**Tuning the grain:**

| Knob | Effect | Sweet range |
|---|---|---|
| `baseFrequency` | Grain size | 0.65 (coarse) → 1.2 (fine) |
| `numOctaves` | Grain complexity | 1 (smooth) → 4 (gritty) |
| `opacity` (rect) | Grain density | 0.3 (subtle) → 0.6 (overt) |
| `mix-blend-mode` | Grain colour behaviour | `overlay` (accent contrast), `soft-light` (subtle), `multiply` (darker grain), `screen` (lighter grain) |

**Animation — shifting noise seed:**

```html
<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="0">
  <animate attributeName="seed" from="0" to="100" dur="6s" repeatCount="indefinite"/>
</feTurbulence>
```

**⚠️ Cost.** `feTurbulence` is CPU-rendered, not GPU. Animating the seed at full-bleed costs 5–15% CPU on a mid-tier laptop. **Default to static grain** (the human eye reads it as moving anyway because of the layered gradient underneath). Animate only if the brief explicitly calls for shimmering noise.

**Pre-build checklist:**
- [ ] Grain `opacity` ≤0.5 (anything heavier obscures content)
- [ ] `pointer-events: none` so the grain doesn't intercept clicks
- [ ] Static seed by default; animate only with documented reason
- [ ] Test contrast over the grain — grain reduces effective contrast by ~5-10%
- [ ] Grain SVG sized to viewport, not larger (no perf benefit, costs memory)

---

## Recipe 4 — WebGL shader gradient (Stripe / Luma class)

**What it is.** A full-bleed `<canvas>` running a GLSL fragment shader that computes the colour of every pixel per frame using mathematical noise (Perlin, Simplex, Worley) modulated by time. Gives the *liquid* look that no CSS can match.

**When to reach for it.** When the brief says "Stripe-like," "fluid backdrop," "shader gradient," or when motion needs to feel organic across a 4K viewport at 60fps. Always pair with a CSS gradient fallback (slower devices, reduced-motion users, JS-disabled).

**Stack options — pick one:**

| Library | Size | Ergonomics | When |
|---|---|---|---|
| Vanilla WebGL2 | ~0kb | Manual | When you have a single specific shader and don't need scene management |
| `regl` | ~30kb | Functional API | One-off shader work, no DOM bridging |
| `three.js` (with `ShaderMaterial`) | ~150kb | Full scene graph | When the page already loads three.js for other reasons (3D, particles) |
| `<gl-transitions>` / shadergradient.co | varies | Pre-built | Prototyping or when the brief literally references one of these libraries |

**Vanilla pattern (orthographic full-bleed shader):**

```html
<canvas id="gl-bg" class="fixed inset-0 -z-10 pointer-events-none"></canvas>
```

```js
const canvas = document.getElementById('gl-bg');
const gl = canvas.getContext('webgl2', { alpha: true, antialias: true, premultipliedAlpha: false });
canvas.width  = window.innerWidth  * Math.min(window.devicePixelRatio, 2);
canvas.height = window.innerHeight * Math.min(window.devicePixelRatio, 2);

const vert = `#version 300 es
in vec2 a_pos; out vec2 v_uv;
void main(){ v_uv = a_pos * 0.5 + 0.5; gl_Position = vec4(a_pos, 0.0, 1.0); }`;

const frag = `#version 300 es
precision highp float;
in vec2 v_uv; out vec4 outColor;
uniform float u_time;
// 2D simplex noise (paste any standard impl — Ashima Arts is canonical)
float snoise(vec2 v){ /* … */ }
void main(){
  vec2 uv = v_uv * 2.0 - 1.0;
  float n = snoise(uv * 1.5 + vec2(u_time * 0.05, u_time * 0.03));
  vec3 c1 = vec3(0.012, 0.02, 0.031);   // surface
  vec3 c2 = vec3(0.388, 0.4, 0.945);    // accent indigo
  vec3 c3 = vec3(0.561, 0.278, 0.682);  // accent violet
  vec3 col = mix(c1, mix(c2, c3, smoothstep(-0.3, 0.6, n)), smoothstep(0.0, 0.8, n));
  outColor = vec4(col, 0.6);
}`;

// Build program, bind quad, request animation frame, update u_time. Standard WebGL boilerplate omitted.
```

**Cost & gating.**

| Concern | Recipe |
|---|---|
| DPR clamp | `Math.min(window.devicePixelRatio, 2)` — never render at 3× on Retina, GPU dies |
| Reduced motion | Skip `requestAnimationFrame`, render one frame, leave canvas static |
| Mobile | Either drop to a CSS gradient fallback OR halve the noise complexity (`uv * 0.8` instead of `* 1.5`) |
| Battery | Pause the loop on `document.visibilitychange` when tab is hidden |
| Fallback | Always render a CSS gradient on the parent element so WebGL failure (context loss, no GPU, blocked) leaves a designed background, not nothing |

**Pre-build checklist:**
- [ ] DPR clamped to 2 max
- [ ] `prefers-reduced-motion` renders single static frame
- [ ] Page hidden → loop paused (`document.visibilitychange`)
- [ ] CSS gradient fallback on the canvas's parent (`background-image: …`)
- [ ] Canvas has `pointer-events: none` and lives behind content (`z-index: -1` or `position: fixed; inset: 0; z-index: 0;` with content at `z-index: 1`)
- [ ] No DOM in the WebGL render loop — every per-frame DOM read trashes performance
- [ ] Mobile fallback documented (drop to CSS gradient at <768px or halve shader complexity)

---

## Recipe 5 — Particle / dot-matrix field (the DESIGN_2 atmosphere)

**What it is.** A WebGL or canvas-2D scene of thousands of dots (or short lines) breathing/drifting with a noise-driven offset. Reads as "data," "signal," or "consciousness" depending on density and motion. Sister technique to Recipe 4 — same WebGL infrastructure, different shader output.

**When to reach for it.** Technical / protocol / cognitive-themed surfaces where you want quiet ambient signal rather than loud colour flow. The DESIGN_2 spec's dot-matrix particle field is this exactly.

**Core knobs:**

| Knob | Range | Effect |
|---|---|---|
| Particle count | 800 (sparse) → 5000 (dense) | Mood: meditative ↔ alive |
| Particle radius | 0.5–2.0 px | Smaller = "data," larger = "stars" |
| Spacing pattern | Grid (rigid) ↔ Poisson disk (organic) | Mood: technical ↔ natural |
| Motion type | Breathing pulse ↔ Pointer drift ↔ Noise flow | See below |
| Colour | Monochrome white at 30–60% opacity ↔ Two-stop gradient sampled per dot | Restraint ↔ richness |

**Breathing pulse motion (slow, ambient):**

```glsl
// Per-vertex shader, dots placed on a grid
uniform float u_time;
attribute vec2 a_pos;
varying float v_pulse;
void main(){
  float dist = length(a_pos);
  v_pulse = 0.5 + 0.5 * sin(u_time * 0.4 - dist * 3.0);
  gl_Position = vec4(a_pos, 0.0, 1.0);
  gl_PointSize = 1.5 + v_pulse * 1.0;
}
```

```glsl
// Fragment
varying float v_pulse;
void main(){
  vec2 c = gl_PointCoord - 0.5;
  float a = smoothstep(0.5, 0.0, length(c));
  gl_FragColor = vec4(1.0, 1.0, 1.0, a * v_pulse * 0.4);
}
```

**Pointer-reactive drift** (subtle, optional):

```js
canvas.addEventListener('pointermove', (e) => {
  const x = (e.clientX / innerWidth) * 2 - 1;
  const y = -((e.clientY / innerHeight) * 2 - 1);
  gl.uniform2f(u_pointerLoc, x, y);
});
```

```glsl
uniform vec2 u_pointer;
// In vertex shader: offset particle position toward/away from pointer
vec2 toPointer = u_pointer - a_pos;
vec2 driftedPos = a_pos + toPointer * 0.02 * (1.0 - length(toPointer));
```

Cap the drift at ~2% of the canvas — anything stronger looks like a swarm following the cursor and breaks the meditative quality.

**Pre-build checklist:** same as Recipe 4 (WebGL gating), plus:
- [ ] Particle count ≤3000 on mobile (each particle = one vertex; 10k particles = noticeable mobile lag)
- [ ] If grid layout: clamp to viewport so off-screen particles don't render
- [ ] Pointer drift gated behind a CSS media query for fine-pointer devices (`@media (pointer: fine)`) — touch users get static breathing only

---

## Recipe 6 — Gradient border shell (premium hairline frame)

**What it is.** A wrapper element with a gradient `background` and a slightly inset content surface, producing a 1–2px gradient frame that fades along its length. Both DESIGN_1 and DESIGN_2 use this; it's promoted here because any glass-card style benefits from it.

**Pattern:**

```html
<div class="gradient-shell">
  <div class="card-content"><!-- card body --></div>
</div>
```

```css
.gradient-shell {
  padding: 1px;
  border-radius: 32px;
  background: linear-gradient(to top,
    rgba(255,255,255,0.10) 0%,
    rgba(255,255,255,0.02) 50%,
    transparent 100%);
}
.card-content {
  background: #0A0D14;
  border-radius: 31px;  /* slightly smaller than shell */
  padding: 32px;
}
```

**Variations:**

- **Top-light shell** (default for cards on dark): bright at top, fading to transparent — reads as if light is hitting the top edge.
- **Bottom-light shell**: bright at bottom — reads as if the card is rising from a glow.
- **Accent-tinted shell**: replace `rgba(255,255,255,…)` with `rgba(99,102,241,…)` (or whatever accent) for subtle brand-coloured edge highlight.
- **Conic shell** (premium): `conic-gradient(from 180deg, …)` for a swept-light look. Higher complexity; use for hero panels only.

**Critical detail.** The inner radius MUST be exactly 1px less than the outer radius (matching the padding). Mismatched radii produce a visible step where the inner surface meets the gradient — the most common implementation defect.

**Pre-build checklist:**
- [ ] Inner border-radius = outer border-radius − padding
- [ ] Shell padding 1px (hairline) or 2px (more visible) — never 3px+ unless the brief calls for thick gradient borders
- [ ] Background-color on `.card-content` is opaque (or the shell shows through in a confusing way)
- [ ] Don't combine with a `border: 1px solid` on the inner — pick one or the other

---

## Recipe 7 — Saturated section band (the "Cohere purple" pattern)

**What it is.** A full-bleed section with a deeply saturated, single-hue gradient (or near-solid colour with subtle gradient depth) that breaks an otherwise white/neutral page rhythm. The saturation lives **inside the section**, not across the whole page — it's a chapter break, not a backdrop. White product cards / screenshots float within the saturated environment, gaining maximum chromatic contrast.

**When to reach for it.** Light-canvas pages (white, cream, off-white) that need dramatic visual punctuation between sections without changing the page's overall register. Enterprise-tech pages (Cohere-class), product showcase sections, pricing emphasis, or any moment where a single section needs to carry maximum visual weight. The technique earns the page the right to stay restrained elsewhere — by reserving saturation for these bands, every other section reads as deliberately calm.

**Pattern:**

```css
.section-band--saturated {
  /* Full-bleed inside an otherwise white page */
  width: 100vw;
  margin-left: calc(50% - 50vw);

  /* Deep purple/violet gradient — Cohere-style */
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, #4C1D95 0%, transparent 70%),
    linear-gradient(180deg, #2E1065 0%, #1E0744 100%);

  padding: 96px 32px;
  color: #FAFAF7; /* light text on saturated band */
}

.section-band--saturated .product-card {
  background: #FFFFFF;
  border-radius: 22px;
  /* Card carries its own elevation INSIDE the band */
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.40);
}
```

**Hue choices.** Deep purple/violet (`#2E1065`, `#4C1D95`) is the default — it carries authority without commercial cliché. Other defensible choices:
- **Deep teal/petrol** (`#0F3B47`) — medical, scientific, infrastructure.
- **Burnt amber/terracotta** (`#7C2D12`) — editorial, cultural, hospitality.
- **Navy ink** (`#1E1B4B`) — institutional, finance, advisory.

Avoid pure red, bright orange, or saturated yellow — they overshoot from "chapter break" to "alarm".

**Composition rules:**

1. **One band per page (max two).** Three or more saturated sections destroy the punctuation effect — the band stops being a chapter break and starts being noise.
2. **White content INSIDE the band, not outside.** Product cards, screenshots, testimonials sit on the saturated surface. The saturation is the frame, not the subject.
3. **Tight section transitions.** Don't fade the band into the surrounding white. Hard edges (or a single 80px gradient transition zone) — the punctuation comes from the contrast, not from blending.
4. **Cards inside the band MUST carry their own shadow.** Without shadow, the saturated background bleeds past card edges and the eye reconstructs ghost outlines (same regression as Recipe 1's bloom-without-card-shadow).
5. **Maintain the page's signature radius inside the band.** If the rest of the page uses 22px card radius, the band's product cards use 22px too. The band changes colour, not vocabulary.

**Light-mode discipline.** This recipe is a light-mode tactic specifically — saturated bands inside dark pages don't work the same way (they read as a different theme, not a chapter break). For dark pages that need section punctuation, use Recipe 1 (layered radial mesh) at lower opacity instead.

**Pre-build checklist:**
- [ ] Page uses a light/neutral canvas as default — band is the exception, not the rule
- [ ] One band per page (two max for very long pages)
- [ ] Band uses full-bleed (`width: 100vw; margin-left: calc(50% - 50vw)`) — half-width saturated sections look like a CSS bug
- [ ] White content cards inside the band carry `box-shadow` for elevation against the saturated surface
- [ ] Text inside the band passes 4.5:1 contrast against the deepest part of the gradient
- [ ] Text colour scoped to the band — no `color: inherit` from page's default dark text (otherwise text becomes invisible). Cross-reference: build-tactics.md Tactic 17.
- [ ] Hue choice documented in provenance — "deep purple chosen for institutional-tech register" not "I picked a colour I liked"

---

## Performance comparison (when in doubt, this table decides)

| Technique | Runtime | CPU cost | GPU cost | Setup complexity | Right for |
|---|---|---|---|---|---|
| Static layered radials (R1) | None | None | Trivial | Low | Atmospheric backdrops, glow blooms |
| CSS background-position shift (R2) | CSS animation | Low (causes paints) | Medium | Low | Slow ambient motion, no JS budget |
| `@property` interpolation | CSS transition | Low | Low (compositor-friendly when `<color>`/`<angle>`) | Medium | Hover effects, modern targets |
| SVG `feTurbulence` static (R3) | None (one-shot render) | Medium (initial render) | None | Low | Grain texture, analog feel |
| SVG `feTurbulence` animated | SMIL or JS | High (5–15% CPU full-bleed) | None | Medium | Shimmering grain — use sparingly |
| WebGL shader (R4, R5) | requestAnimationFrame | Low (mostly GPU) | High but isolated | High | Liquid backdrops, particle fields, anything Stripe-like |

**The general rule:** prefer the simplest technique that achieves the look. Reach for WebGL only when CSS+SVG demonstrably can't hit the brief. A layered radial backdrop with grain overlay handles ~80% of "modern atmospheric gradient" briefs without a single line of JS.

---

## Light-mode discipline

Every recipe above defaults to dark-mode examples because dark surfaces forgive saturation. Light-mode requires three adjustments:

1. **Drop saturation by 30–50%.** Pure `#6366F1` indigo on a cream backdrop reads as a poster ad. The same hue at 40% saturation reads as ambient atmosphere.
2. **Increase opacity by 1.5–3×.** Light surfaces don't absorb gradient light the way dark surfaces do. A bloom at `0.18` opacity that works on `#030508` needs `0.40+` to be visible on `#FAFAF7`.
3. **Add bounded edges.** Light-mode gradients that bleed to the page edge often look like printer mistakes. Confine them inside cards, hero containers, or fade them out before the section boundary.

When a light-mode style says "atmospheric gradient," the right move is usually a single soft-radial wash inside a hero container, not a full-page mesh. If the brief insists on full-page mesh in light mode, push back — it's almost always wrong.

---

## Anti-patterns

- ❌ **Five+ radial blobs in one mesh.** Always muddies into a single grey wash. Three is the sweet spot.
- ❌ **`linear-gradient(45deg, #ff0000, #0000ff)`.** Saturated rainbow gradients are a 2014 dribble cliché. Modern gradients use 2–3 stops in adjacent hues with significant opacity variation.
- ❌ **Animating `background-image` directly.** Browsers can't interpolate gradient stops in `background-image` (without `@property`). Use `background-position` shift OR `@property` — never naive `transition: background-image`.
- ❌ **WebGL backdrop with no fallback.** Context loss, mobile GPUs, blocked WebGL contexts, reduced-motion users — all require a CSS-only fallback. Always.
- ❌ **Animated `feTurbulence` at full-bleed by default.** CPU killer. Static grain reads as moving anyway because of the gradient layers underneath; only animate the seed if explicitly briefed.
- ❌ **Mixed gradient-border shell and solid border on the same card.** Pick one. Two stacked treatments produce a visible step.
- ❌ **Particle field >5000 particles on mobile.** Each particle is a vertex; mobile GPUs throttle hard above ~3000.
- ❌ **Bloom at >25% opacity behind body text.** Drops contrast below WCAG AA without warning. Always test text contrast over the bloom centre, not just the page average.

---

## Audit questions (Phase 4 gradient lens)

When the build uses any gradient as a load-bearing visual element:

0. **🛑 CARDINAL — Does every card sitting on top of an animated/atmospheric gradient backdrop have a `box-shadow`?** This is the highest-frequency regression of any gradient-backed style (especially Bloom). Without a shadow, the bloom/flow/particle backdrop bleeds past the card edges and the eye reconstructs an apparent "ghost outline" offset from the actual card — the page reads as broken even though the markup is valid. Mechanical check before delivery: `grep -E "(\.gradient-shell|\.card|\.shell-content|\.[a-z]+-card)\s*\{" <build-file> | xargs -I {} grep -L box-shadow {}` — any class without `box-shadow` is a defect. Fix by adding `box-shadow: 0 25px 50px -12px rgba(0,0,0,0.40)` (neutral) or accent-tinted variant for hero/featured cards.

1. **Is the gradient choice deliberate?** A static layered-radial backdrop vs. a WebGL shader is a 100kb+ JS difference. The brief or DESIGN.md should justify the runtime choice — "we picked WebGL because the brief asked for Stripe-like fluidity," not "I added a shader."
2. **Does it fall back gracefully?** Disable JavaScript: does the page still have the intended gradient feel via CSS? Disable the WebGL canvas: does the parent's CSS gradient carry the look?
3. **`prefers-reduced-motion` respected?** Animated gradients (any technique) must pin to a static state under reduced motion. Test it.
4. **Contrast preserved?** Run text contrast checks at the brightest point of the gradient (bloom centre, flow midpoint), not just the page average. Bloom-driven contrast loss is the most common gradient-related accessibility regression.
5. **Mobile parity acceptable?** WebGL shaders run, but at what cost? If mobile drops below 30fps, demote to CSS fallback for `<768px`.
6. **Recipe consistency with style guide.** If the style guide names "Bloom backdrop," the build should use the layered-radial recipe, not a freelance interpretation. Don't substitute a WebGL shader for a documented CSS recipe (or vice versa) without flagging.
7. **Grain opacity ≤0.5.** Heavier grain reduces text contrast and reads as image artifacting.
8. **Maximum two animated gradients per page.** Multiple animated backgrounds compound; the eye loses track of motion priority and the page feels nervous.
