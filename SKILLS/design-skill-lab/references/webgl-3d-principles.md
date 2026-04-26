# WebGL / 3D Principles

The **design lens** for WebGL and Three.js. Loaded BEFORE `webgl-3d-tactics.md`. Tactics tell you HOW to wire `GLTFLoader`; principles tell you WHEN 3D earns its place and what trade-offs you just took on.

This file pairs with the `dimension` axis in `style-tuning.md`. Three tiers:

- `none` — no WebGL, no 3D. Default. The browser paints DOM and that's the end of it.
- `shader-accents` — fragment shaders on a fullscreen plane or a small canvas. Noise gradients, liquid hover distortions, kinetic backgrounds. **No imported 3D models.**
- `3d-scene` — full Three.js scene: imported GLB models, PBR materials, scroll-driven camera path, possibly a hero 3D object that the user can interact with.

There is no `immersive` tier. WebXR, multiplayer, complex physics, ray tracing, Pixel Streaming — these are explicitly out of scope. The research is unambiguous: AI ships those broken. Don't promise what the skill can't honestly deliver.

---

## When 3D earns its place

3D is a force multiplier for the right brief and a tax on the wrong one. Default to `none`. Reach for `shader-accents` or `3d-scene` only when at least ONE of the following is true:

1. **The product IS the 3D thing.** Configurators (furniture, sneakers, bottles, watches), 3D-data dashboards (warehouse heatmaps, network topology), CAD viewers, in-browser games, brand experiences whose entire pitch is "you have to see it move".
2. **The brand is paying the 3D tax deliberately.** Premium tech, AI tools, retro-futurist agencies, hospitality with cinematic ambition. The user expects the load time. The brand earns the tax.
3. **The 3D is a controlled accent, not the load.** A shader background that adds atmosphere; a small hero object that anchors the page; a single scroll-driven camera move. The DOM still does the work; 3D is the polish.

If none of those are true and the brief says "make it look modern" — ship `none` with strong motion + typography. That is the lower-risk, higher-conversion choice for 90% of projects.

### Anti-patterns — 3D for 3D's sake

The research is explicit (Category 3): the #1 AI-coded 3D failure is **3D where DOM would do**. Recognise these smells and refuse:

- ❌ **A spinning logo cube on a startup landing page.** Adds 2-5 MB of bundle for an effect a CSS gradient could carry better.
- ❌ **A particle field behind text that costs 30+ FPS on mobile.** Now the headline is unreadable.
- ❌ **A scroll-driven 3D scene that hijacks scroll and breaks browser back/forward.** Almost always a misclick.
- ❌ **3D content with no DOM equivalent.** Search engines see nothing, screen readers see nothing, and the brief was for a marketing site — you just nuked the page's job.
- ❌ **A "premium feel" 3D model when the asset budget is one designer's afternoon.** A bad 3D model looks worse than no 3D model.

---

## Library choice — Three.js vs Unity vs Pixel Streaming

The skill defaults to **Three.js**. The research's table makes the case unambiguously for marketing, e-commerce, dashboards, and brand sites:

| Factor | Three.js | Unity WebGL | Pixel Streaming |
|---|---|---|---|
| Asset download | 2-5 MB | 15-50 MB | 0 (video stream) |
| Load time | 2-6 s | 8-30 s | Near-instant |
| SEO | Crawlable (DOM coexists) | Black box | Black box |
| Mobile perf | Strong | Constrained | Network-dependent |
| Best for | Most web work | Browser games, simulations | Enterprise, VR/AR, industrial |

The skill writes Three.js. If the brief truly needs Unity (existing engine codebase, complex AI, physics-heavy game) or Pixel Streaming (luxury preview, ray tracing, VR), the skill flags this in delivery and refers the user to a specialist — it does not attempt those builds.

**WebGPU vs WebGL2:** the runtime targets WebGL2 by default. WebGPU is opt-in via `dimension.webgpu: true` in the manifesto and only used when (a) the project commits to dropping pre-WebGPU browsers, or (b) the brief uses compute shaders for genuine GPGPU work (point clouds, particle physics, real-time data filtering). TSL (Three Shader Language, Three.js r170+) is the recommended shader authoring path when WebGPU is on, because it transpiles to both WGSL and GLSL.

**React Three Fiber:** if the project's primary stack is React, the skill emits R3F (`@react-three/fiber` + `@react-three/drei`) instead of vanilla Three.js. The principles in this file apply identically to both — R3F is a renderer for React, not a different engine.

---

## The performance budget — non-negotiable

The research's hard number: **page load >10 seconds = catastrophic retention drop, regardless of how impressive the 3D is**. The skill enforces a per-tier budget:

| Tier | Compressed bundle | LCP target | Mobile FPS floor |
|---|---|---|---|
| `none` | n/a | <2.5 s | 60 |
| `shader-accents` | ≤ 200 KB extra (no Three.js core if shader-only) | <3 s | 60 |
| `3d-scene` | ≤ 2 MB (Three.js + GLB + textures, after Draco + KTX2) | <4 s | 30 |

If the build can't hit these numbers, the tier downgrades automatically. There is no "but the brand wants it" override — a site that doesn't load is the most expensive design failure possible.

**How the budget is enforced:**

- `3d-scene` REQUIRES Draco-compressed GLB (not glTF JSON, not FBX, not OBJ) and KTX2-compressed textures.
- All 3D assets lazy-load. Hero scene starts decoding ONLY after first paint of DOM.
- Mobile gets a lower-poly LOD or a static fallback image. The skill sets `window.matchMedia('(max-width: 768px)')` and conditionally reduces FOV, DPR cap (max `2`), and shadow quality.
- Post-processing (bloom, depth of field, SSAO) is opt-in per pass, never on by default. One `EffectPass` from `pmndrs/postprocessing`, never a stack.

---

## Fallback strategy — the four mandatory guards

The research's "AI ships broken 3D" failure mode is concrete: 3D loaded with no fallbacks, on hardware that can't render it, with no way out. The skill ships every `dimension > none` build with FOUR mandatory guards. Skipping any one is a delivery-blocking defect.

### Guard 1 — WebGL feature detect with DOM fallback

Before the 3D code runs, detect WebGL support. If unavailable (older browser, GPU disabled, headless test, antivirus blocking canvas), the DOM equivalent renders instead.

```js
function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}
if (!hasWebGL()) document.documentElement.classList.add('no-webgl');
```

The DOM fallback is a real composition (image, gradient, type) — not a "your browser doesn't support 3D" message.

### Guard 2 — `prefers-reduced-motion` static frame

Users with `prefers-reduced-motion: reduce` see ONE static frame of the scene (or the DOM fallback). No camera path, no idle drift, no shader animation. This is WCAG-aligned (2.3.1 / 2.3.3) and respects vestibular-disorder users. Implementation lives in `webgl-3d-tactics.md` § Reduced motion.

### Guard 3 — SEO / a11y DOM mirror

3D content does not replace DOM content. Every 3D scene has a DOM equivalent: alt text, a heading, body copy, visible to crawlers and screen readers. The 3D layers ON TOP. A user who navigates by keyboard or screen reader gets the full page; the 3D is the visible cherry, not the cake.

### Guard 4 — Bundle / load failure timeout

If the 3D scene hasn't initialised within 8 seconds (asset failure, slow CDN, cancelled fetch), the loading state times out and the DOM fallback renders. The user is never staring at a blank canvas. Pairs with `loader-patterns.md` § max-timeout safeguard.

---

## Accessibility in 3D — the human responsibility

Per the research's Category 3 (low AI feasibility): WCAG compliance in 3D is a manual responsibility. The skill does not automate it; it documents it.

- **Keyboard navigation.** If the 3D scene has interactive elements (rotate, zoom, click parts of a model), they must be reachable via Tab + Enter / Space. The DOM mirror handles this — the canvas itself is not focusable; sibling DOM controls are.
- **No deceptive UI.** Don't hide critical CTAs behind a "click to explore" 3D gesture. The CTA exists in DOM; the 3D is decoration.
- **Focus management.** Don't trap focus inside the canvas. Don't auto-scroll on canvas focus.
- **Cognitive load.** Idle camera drift, looping particles, slow auto-rotate — all read as "background noise" to most users and as "moving target I cannot focus on" to users with attention-related conditions. Default to ON-INTERACT motion, not idle.

---

## The C.U.R.E. test for 3D (mirrors motion-principles.md)

Every 3D moment passes this audit before it ships. If any answer is "no" or "I don't know", drop the moment.

- **Context** — Is 3D the right register for THIS brand and THIS audience? A children's literacy tool does not need Three.js.
- **Usefulness** — Does it inform, guide, or delight in a way DOM/CSS could not? Or is it ego art?
- **Restraint** — Is it ONE moment of 3D, or are there four scenes competing for the user's GPU budget?
- **Emotion** — Does it actually feel premium / playful / sci-fi / cinematic, or does it feel like a tech demo?

The hardest of these is **Restraint**. The instinct, especially with AI-assisted code generation, is to layer effects: a shader background AND a hero 3D model AND a particle scroll-trigger AND a scroll-driven camera path. Every layer halves frame rate on mid-tier mobile. Pick one moment per page; let the rest of the design carry the work.

---

## Sustainability

Per the research's "Green Web Development" thread: 3D content has a measurable carbon footprint. Idle 3D rendering on a laptop draws 5-15 W more than DOM-only equivalents. Across millions of page loads, that adds up.

The skill's defaults reflect this:

- 3D pauses when the canvas leaves the viewport (`IntersectionObserver`). No off-screen rendering.
- 3D pauses when the tab is hidden (`document.visibilityState === 'hidden'`).
- Idle FPS caps at 30 unless interaction is active.
- Shaders use the cheapest noise function that meets the visual goal — no overengineered FBM stacks where a single `sin(uv + time)` would do.

These are not optional. They are part of the build contract.

---

## Hand-off to tactics

After reading this file, the build agent loads `webgl-3d-tactics.md`. That file specifies:

- The exact JS module structure per tier
- The four mandatory failure-mode guards as code
- The pre-build checklist
- Style-fit notes (which of the 12 libraries host 3D well — see also `webgl-3d-style-fit.md`)

Principles classify the moment. Tactics build it.
