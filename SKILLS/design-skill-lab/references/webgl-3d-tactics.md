# WebGL / 3D Tactics

The **technical contract** per `dimension` tier. Loaded after `webgl-3d-principles.md`. Principles tell you whether to build 3D; tactics tell you exactly what code to ship.

If you are reading this without having read principles first, stop and read principles. Tactics without principles produce demos, not designs.

---

## Tier 1 — `shader-accents`

Fragment shaders only. No imported 3D models. No camera, no lights, no scene graph beyond a single fullscreen plane (or a small offscreen `<canvas>`).

### What ships

- A single `<canvas>` element behind (or beside) DOM content.
- Either:
  - **Vanilla WebGL2** — direct `gl.compileShader` for ultra-light shader-only effects (~5-15 KB JS).
  - **Three.js `ShaderMaterial` on `PlaneGeometry`** — when you want Three.js's uniform/attribute plumbing without the scene weight (~150 KB JS gzipped, but you get free `iResolution`, `iTime`, mouse, scroll uniforms).
- GLSL fragment shader doing one of: noise gradient, Voronoi cells, fluid distortion on hover, scroll-reactive wave, kinetic background.
- Uniforms updated per RAF (request animation frame) with `time`, `mouse`, `scroll`, `resolution`.

### What does NOT ship at this tier

- ❌ `GLTFLoader`, `OBJLoader`, `FBXLoader` — no model imports.
- ❌ `PerspectiveCamera`, `OrbitControls` — no 3D navigation.
- ❌ `DirectionalLight`, `AmbientLight`, shadow maps — no lighting.
- ❌ `EffectComposer` / postprocessing — single shader pass only.
- ❌ Physics, audio, multi-scene composition.

If the brief calls for any of those, the tier is wrong — escalate to `3d-scene` or step back to `none`.

### Bundle budget

≤ 200 KB compressed total for the 3D path. If using vanilla WebGL2: ~10-20 KB including the shader. If using Three.js `ShaderMaterial`: ~150 KB (Three.js core, tree-shaken to renderer + plane geometry + ShaderMaterial only).

### Skeleton — vanilla WebGL2 fragment shader

```js
// shader-accent.js — IIFE-wrapped, gated by feature detect
(function () {
  if (!hasWebGL()) return; // see Guard 1 in principles
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return; // Guard 2

  const canvas = document.querySelector('[data-shader-canvas]');
  if (!canvas) return;
  const gl = canvas.getContext('webgl2', { antialias: false, alpha: true });
  if (!gl) return;

  const vs = `#version 300 es
  in vec2 a_pos; out vec2 v_uv;
  void main() { v_uv = a_pos * 0.5 + 0.5; gl_Position = vec4(a_pos, 0, 1); }`;

  const fs = `#version 300 es
  precision highp float;
  in vec2 v_uv; out vec4 fragColor;
  uniform float u_time; uniform vec2 u_resolution; uniform vec2 u_mouse;
  // <— project's actual shader logic, tuned to DESIGN.md tokens
  void main() {
    vec2 uv = v_uv;
    float n = sin(uv.x * 8.0 + u_time * 0.4) * 0.5 + 0.5;
    fragColor = vec4(vec3(n) * vec3(0.95, 0.93, 0.88), 1.0); // parchment-tinted noise
  }`;

  // ... compile, link, bind buffer, RAF loop, resize handler, IntersectionObserver pause ...
})();
```

The actual shader content is determined by the DESIGN.md tokens (accent colour, mood). The skill does NOT ship a generic "AI gradient" — it generates a shader tuned to the project's palette and library mood (warm-editorial → parchment noise; technical-refined → grid grain; brutalist → high-contrast Voronoi).

### Skeleton — Three.js ShaderMaterial path

Use this when the project ALREADY has Three.js (e.g., page has both shader background + a `3d-scene` hero) — no point loading two different WebGL stacks.

```js
import { Scene, OrthographicCamera, WebGLRenderer, PlaneGeometry, ShaderMaterial, Mesh, Vector2 } from 'three';
// orthographic camera, fullscreen plane, ShaderMaterial with uniforms{u_time, u_mouse, u_resolution}
```

---

## Tier 2 — `3d-scene`

Full Three.js scene. Imported GLB models, PBR materials, scroll-driven camera path, optional shader effects on top.

**BEFORE writing the scene init code, pick a geometry from `webgl-3d-geometries.md`.** That catalog defines 6 primitives (blob, wireframe geode, crystal, plane displacement, torus knot, particle ribbon) plus a per-library default table. Never default to "blob" silently — read the geometries file, pick the one that matches the library, and record the choice in `provenance.dimension.geometry`. Combining geometries is forbidden (one allowed exception: Plane Displacement under a primary geometry — see catalog § Anti-stacking rule).

### What ships

- Three.js r170+ (or matching R3F version if React stack).
- `GLTFLoader` + `DRACOLoader` (Draco mesh compression) + `KTX2Loader` (Basis Universal texture compression).
- `PerspectiveCamera`, `Scene`, `WebGLRenderer` with `antialias: true`, `powerPreference: 'high-performance'`, `pixelRatio: Math.min(window.devicePixelRatio, 2)`.
- Lighting: `AmbientLight` + ONE `DirectionalLight`. Shadows opt-in per project, default off.
- Materials: `MeshStandardMaterial` for everything PBR. `MeshBasicMaterial` for unlit decorative meshes.
- Scroll integration: GSAP `ScrollTrigger` (vanilla Three.js stack) or `@react-three/drei` + `@react-three/scroll-rig` (R3F stack).
- Optional: `pmndrs/postprocessing` `EffectComposer` with ONE merged `EffectPass` (bloom + tone mapping at most). Never a stack of passes.

### What does NOT ship at this tier

- ❌ FBX, OBJ, COLLADA imports. GLB only.
- ❌ Uncompressed textures. KTX2 (or at minimum WebP) only.
- ❌ Real-time global illumination, ray-marched volumes, complex post stacks.
- ❌ Physics engines (Cannon, Rapier, Ammo) — out of scope; if the brief needs physics, escalate.
- ❌ WebXR / VR / AR session APIs — out of scope.
- ❌ Multiplayer / WebRTC / WebSocket-driven scenes — out of scope.
- ❌ Audio-reactive scenes beyond a single uniform tied to `<audio>` analyser — anything more complex is out of scope.

### Bundle budget

≤ 2 MB compressed total (Three.js + Draco decoder + KTX2 transcoder + GLB assets + textures, gzipped/brotli).

If the design calls for assets larger than this, the skill must:
1. Re-compress with `gltf-transform` (`npx gltf-transform optimize input.glb output.glb --compress draco --texture-compress ktx2`).
2. If still over budget, reduce poly count, reduce texture resolution, or split into LODs (high-res for hero shot, low-res for scroll).
3. If still over budget, the tier downgrades to `shader-accents` and the asset becomes a hero image.

### File layout

```
src/
  three/
    init.js            # renderer, scene, camera, lighting setup
    loader.js          # GLTFLoader + Draco + KTX2 setup, returns Promise<GLTF>
    scroll-camera.js   # GSAP ScrollTrigger waypoints OR R3F-scroll-rig hooks
    shaders/
      hero-bg.frag     # optional shader-accent layered behind 3d scene
    fallback.html      # DOM equivalent for non-WebGL / reduced-motion / failure-timeout
public/
  models/
    hero.glb           # Draco-compressed
    hero-low.glb       # mobile LOD
  textures/
    diffuse.ktx2
```

### Init skeleton (vanilla Three.js)

```js
import { Scene, PerspectiveCamera, WebGLRenderer, AmbientLight, DirectionalLight } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js';

export async function initScene(canvas) {
  if (!hasWebGL()) return showFallback();
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const renderer = new WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  const scene = new Scene();
  const camera = new PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  scene.add(new AmbientLight(0xffffff, 0.6));
  const dir = new DirectionalLight(0xffffff, 0.8);
  dir.position.set(3, 5, 2);
  scene.add(dir);

  const draco = new DRACOLoader().setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');
  const ktx2 = new KTX2Loader().setTranscoderPath('https://unpkg.com/three@0.170.0/examples/jsm/libs/basis/').detectSupport(renderer);
  const loader = new GLTFLoader().setDRACOLoader(draco).setKTX2Loader(ktx2);

  const isMobile = matchMedia('(max-width: 768px)').matches;
  const url = isMobile ? '/models/hero-low.glb' : '/models/hero.glb';

  const gltf = await Promise.race([
    loader.loadAsync(url),
    new Promise((_, reject) => setTimeout(() => reject('timeout'), 8000)) // Guard 4
  ]).catch(() => null);

  if (!gltf) return showFallback();
  scene.add(gltf.scene);

  if (reducedMotion) {
    renderer.render(scene, camera); // one static frame, then return
    return { scene, camera, renderer, paused: true };
  }
  // ... RAF loop with IntersectionObserver pause + visibilitychange pause ...
}
```

### Scroll-driven camera (GSAP ScrollTrigger pattern)

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { CatmullRomCurve3, Vector3 } from 'three';
gsap.registerPlugin(ScrollTrigger);

const waypoints = [
  new Vector3(0, 1, 5), new Vector3(2, 2, 3), new Vector3(0, 3, 1) // tuned per project
];
const curve = new CatmullRomCurve3(waypoints);

ScrollTrigger.create({
  trigger: '[data-scene-section]',
  start: 'top top',
  end: 'bottom bottom',
  scrub: 1,
  onUpdate(self) {
    const p = curve.getPoint(self.progress);
    camera.position.copy(p);
    camera.lookAt(0, 0, 0);
  }
});
```

The ease is set by `scrub: 1` (1-second smoothing). For a more cinematic feel use `scrub: 1.5` or wrap with `gsap.to(camera.position, ...)` per scroll-trigger callback.

---

## The four mandatory failure-mode guards (both tiers)

These are non-negotiable. A `dimension > none` build that ships missing any one is a delivery-blocking defect. The pre-build checklist at the bottom of this file enforces them.

### Guard 1 — WebGL feature detect

```js
function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}
```

Used at the top of every WebGL entry point. If false → DOM fallback. The DOM fallback is a real composition (image / gradient / type), not an apology.

### Guard 2 — Reduced motion

```js
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
```

If true:
- `shader-accents`: don't run the RAF loop. Render one static frame (or nothing — the canvas can stay blank with the DOM behind it visible).
- `3d-scene`: load the scene, render ONE frame, then stop. No camera animation, no idle drift.

`prefers-reduced-motion` may flip during a session (system setting changes, user toggles macOS Reduce Motion). Listen for the `change` event:

```js
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', e => {
  if (e.matches) pauseAllAnimation();
});
```

### Guard 3 — DOM mirror for SEO / a11y AND legibility scrim

The 3D layer does not replace DOM content. The page has its full headline, body, CTAs, image alts in the DOM. The 3D `<canvas>` is `aria-hidden="true"` and decorative. The `<canvas>` element gets a sibling `<div>` (or fallback `<img>`) inside the same container, hidden via `.no-webgl` class.

**Sub-guard 3a — Legibility scrim (NON-NEGOTIABLE for fullscreen WebGL backdrops).**

A bright animated WebGL surface behind text guarantees an accessibility failure unless a scrim sits between them. Real-world failure mode (observed): a blue blob shader rendered behind body copy reduced contrast from 12:1 to ~1.4:1 — text became unreadable. WCAG AA requires 4.5:1 for body, 3:1 for large text. WebGL output cannot be relied on to maintain those ratios.

If the canvas is `position: fixed; inset: 0;` and content sits ON TOP of it (not just inside a hero section), you MUST ship a scrim. Two-layer pattern:

```html
<canvas class="bg-canvas" data-3d-canvas aria-hidden="true"></canvas>
<div class="scrim" aria-hidden="true"></div>
<div class="scrim-below" aria-hidden="true"></div>
<main>...</main>
```

```css
.bg-canvas  { position: fixed; inset: 0; z-index: -2; }
/* Center column darkening — protects body copy at all scroll positions */
.scrim {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    radial-gradient(ellipse 70% 90% at 50% 55%, rgba(0,0,0,0.55), transparent 75%),
    linear-gradient(180deg, rgba(0,0,0,0.55) 0%, transparent 18%, transparent 50%, rgba(0,0,0,0.65) 90%, rgba(0,0,0,0.85) 100%);
}
/* Below-fold dimmer — kicks in once user scrolls past hero */
.scrim-below {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background: linear-gradient(180deg, transparent 0%, transparent 35%, rgba(0,0,0,0.78) 70%, rgba(0,0,0,0.92) 100%);
  opacity: 0; transition: opacity 600ms ease;
}
body.scrolled-past-hero .scrim-below { opacity: 1; }
.no-webgl .scrim, .no-webgl .scrim-below { display: none; }
```

JS toggles `body.scrolled-past-hero` once `scrollY > innerHeight * 0.55`. This means the WebGL is the visual subject of the hero only — below the fold, the scrim layer dims it heavily so services / manifesto / process / CTA all read on near-solid dark.

**Mandatory: a contrast spot-check before delivery.** Take a screenshot of the build at 100% zoom. Pick the darkest WebGL pixel directly under any body text. Use a tool (Stark, browser devtools axe panel, or just eyeball with `webaim.org/resources/contrastchecker/`) to confirm the text-vs-pixel contrast is ≥ 4.5:1 for body, ≥ 3:1 for headlines. If not, the scrim is too weak — increase the center-radial alpha or kick in scrim-below sooner.

**Composition guidance to ease the scrim's job:**
- Position the WebGL object OFF-CENTRE so it sits in negative space (corners, edges) rather than behind text columns.
- Cap the WebGL surface brightness in the fragment shader with a final `col *= 0.55` (or similar) — a max-luminance ceiling.
- Cap bloom intensity ≤ 0.8 and `luminanceThreshold` ≥ 0.30 — bloom spreads bright pixels into adjacent text areas; a permissive bloom threshold is the #1 cause of post-FX legibility failure.
- Avoid pure white particles or stars over a dark background — they read as random noise behind text and tank contrast for anything overlapping.

The DOM mirror itself:

```html
<div class="hero">
  <canvas data-3d-canvas aria-hidden="true"></canvas>
  <noscript><img src="/hero-fallback.jpg" alt="Hero scene"></noscript>
  <div class="hero-content">
    <h1>Real DOM headline</h1>
    <p>Real DOM body copy.</p>
    <a href="/start" class="btn">Start →</a>
  </div>
</div>

<style>
  .no-webgl [data-3d-canvas] { display: none; }
  .no-webgl .hero { background-image: url('/hero-fallback.jpg'); }
</style>
```

### Guard 4 — Load timeout

If the 3D scene hasn't initialised within 8 seconds, the DOM fallback renders instead. See the `Promise.race` pattern in the init skeleton above.

This guard catches: slow CDN, cancelled fetch, WAF blocking, asset 404, decoder script failure. Without it, a bad CDN day = a blank hero forever.

---

## Style-fit notes (cross-reference `webgl-3d-style-fit.md`)

Quick map. Full reasoning lives in `webgl-3d-style-fit.md`.

| Library | `dimension` defaults to | Hosts 3D well |
|---|---|---|
| Neo-Brutalist | none (poster type carries) | shader-accents only — high-contrast Voronoi backgrounds |
| Editorial Portfolio | none | rare 3D — only if portfolio item IS the 3D work |
| Technical Refined | none | shader-accents (grid grain), 3d-scene for data viz |
| Basalt E-Commerce | none | 3d-scene as product configurator (the strongest 3D fit) |
| Memoir Blog | none | refuse 3D — reading-first |
| Creative Studio | shader-accents | 3d-scene for showcases |
| Warm Serene Luxury | none | subtle shader-accents (parchment haze) |
| Playful Bento | shader-accents | 3d-scene per bento cell |
| Spritify | none | refuse — kid audience, perf risk too high |
| Sanctuary Tech | FORCED none | refuse — trauma-informed, perf-sensitive, plus DPR/cognitive load concerns |
| Warm Editorial | shader-accents | rare 3d-scene — only if AI product needs to demo 3D output |

---

## Pre-build checklist — the contract

Before ANY `dimension > none` build leaves Phase 3, every one of these must be true. Failure on any item is a delivery-blocking defect, not a "nice-to-have".

**Asset & bundle**
- [ ] Models are GLB (not glTF JSON, not FBX, not OBJ)
- [ ] Models are Draco-compressed (`gltf-transform optimize` ran with `--compress draco`)
- [ ] Textures are KTX2 or WebP (not PNG / JPEG at 4K)
- [ ] Total compressed bundle ≤ tier budget (200 KB for `shader-accents`, 2 MB for `3d-scene`)
- [ ] Mobile has a low-poly LOD or static fallback image
- [ ] DPR cap set to `Math.min(devicePixelRatio, 2)`

**Failure-mode guards**
- [ ] WebGL feature detect at every entry point (Guard 1)
- [ ] `prefers-reduced-motion` honoured (Guard 2) AND listening for `change` event
- [ ] DOM mirror with full content (headline, body, CTAs) — `<canvas>` is `aria-hidden="true"` (Guard 3)
- [ ] 8-second load timeout with DOM fallback (Guard 4)
- [ ] **Legibility scrim** in place if canvas is fullscreen-fixed (Sub-guard 3a) — `.scrim` center-radial + `.scrim-below` for past-hero dimming
- [ ] **Contrast spot-check passed** — pick the darkest pixel under any body text, confirm ≥ 4.5:1 vs text colour. WCAG AA is non-optional.
- [ ] **WebGL object is off-centre** if it lives behind body content — corners/edges, not centre column
- [ ] Fragment shader has a max-luminance ceiling (`col *= 0.55` or similar)
- [ ] Bloom intensity ≤ 0.8, `luminanceThreshold` ≥ 0.30 — permissive bloom spreads bright pixels into text
- [ ] No white particles / stars over dark backgrounds when text overlaps — visual noise tanks contrast

**Performance**
- [ ] `IntersectionObserver` pauses RAF when canvas is offscreen
- [ ] `visibilitychange` pauses RAF when tab is hidden
- [ ] Idle FPS capped at 30 unless interaction is active
- [ ] Postprocessing: zero passes, OR exactly one merged `EffectPass`. Never a stack.

**Accessibility**
- [ ] Canvas is not focusable (`tabindex="-1"` or no tabindex)
- [ ] Interactive 3D actions have keyboard-reachable DOM equivalents (Tab + Enter / Space)
- [ ] No focus traps, no auto-scroll on canvas focus
- [ ] No CTA hidden behind a "click to explore" 3D gesture — CTAs exist in DOM

**Sustainability**
- [ ] Scene pauses when off-screen and when tab hidden (covered above)
- [ ] Idle camera drift / looping particles disabled by default — motion fires on interaction or scroll only

**Tier-coupling sanity**
- [ ] If `dimension: 3d-scene`, then `motion ≥ medium` (a static 3D scene is dead). If `motion: low`, surface a tier-coupling warning per `style-tuning.md`.
- [ ] If trauma-informed mode active → `dimension` forced to `none`. No exceptions.
- [ ] If library is Sanctuary Tech / Memoir / Spritify → `dimension` forced to `none` unless explicit user override; warn if forced override.

---

## What's explicitly out of scope (escalate to specialist)

If the brief requires any of the following, the skill does NOT attempt them. It documents the requirement, ships the closest in-scope alternative, and refers to a specialist:

- Physics simulations (rigid body, soft body, cloth, fluid)
- Multiplayer / networked scenes
- WebXR / VR / AR
- Ray-traced lighting / global illumination
- Generative AI 3D-asset pipeline (Tripo, Meshy, Rodin) — these are workflow tools, not runtime
- Pixel Streaming / Unreal / Unity WebGL
- DICOM / medical imaging / scientific simulation

The research is unambiguous (Category 3): AI ships these broken. Refusing is faster than failing.

---

## Provenance fields

The build records the following in the project DESIGN.md frontmatter under `provenance.dimension`:

```yaml
  dimension:
    tier: 3d-scene                         # none | shader-accents | 3d-scene
    library: three.js                      # three.js | r3f | webgl-vanilla
    webgpu: false                          # opt-in only when stack supports it
    bundle-kb-compressed: 1740             # actual measured value
    lcp-ms-target: 4000
    mobile-lod: true
    guards:
      webgl-detect: true
      reduced-motion: true
      dom-mirror: true
      load-timeout-ms: 8000
    out-of-scope-flagged: []               # array of requested-but-not-built items
```

This block becomes part of the divergence audit (Phase 4.5) — it proves the build met the contract.
