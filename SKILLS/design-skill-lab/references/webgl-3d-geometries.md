# WebGL / 3D Geometry Catalog

A vocabulary of 6 geometric primitives the skill picks from when `dimension` is `shader-accents` or `3d-scene`. Without this catalog, every 3D build defaults to "blob" — same shader, same shape, same vibe. Different libraries call for different geometries; this file is the contract.

Loaded by the agent in Phase 3 Step 3.0.09 alongside `webgl-3d-tactics.md`. The build agent picks ONE geometry per project (do not stack — see § Anti-stacking rule at the bottom).

---

## How to choose

Use **library + brief** to map. If multiple geometries fit, prefer the one that's already in the per-library default column; if none fit cleanly, use Geometry 1 (Distorted Blob) — the safest atmospheric default.

| # | Geometry | Vibe | Default-of |
|---|---|---|---|
| 1 | Distorted Blob | soft, atmospheric, organic | warm-editorial, atmospheric-protocol, sanctuary-tech |
| 2 | Wireframe Geode | technical, instrument-like, geometric | technical-refined, basalt |
| 3 | Crystal / Octahedron | edgy, prismatic, bold | neo-brutalist, creative-studio, playful-bento |
| 4 | Plane Displacement | calm, horizon-like, ambient | warm-serene-luxury (subtle), warm-editorial (subtle) |
| 5 | Torus Knot | mathematical, considered, premium-tech | atmospheric-protocol (alt), technical-refined (alt) |
| 6 | Particle Ribbon | kinetic, signal-as-line | creative-studio (kinetic alt), technical-refined (data viz) |

**Containment strategy** — every build picks one of:
- **fullscreen-fixed** (`position: fixed; inset: 0; z-index: -2;`) — canvas sits behind the entire page. Requires the legibility scrim contract (`webgl-3d-tactics.md` § Sub-guard 3a). Best for dark-mode-only pages.
- **hero-absolute** (`position: absolute; inset: 0;` inside `.hero`) — canvas only renders inside the hero element. No fullscreen scrim needed because content below the hero is unaffected. Best for light-mode pages with a dark hero band.

Pick the containment per page colour-mode, not per geometry. All 6 geometries support both.

---

## 1. Distorted Blob — `IcosahedronGeometry` + noise displacement

**Vibe.** Soft, atmospheric, organic. Reads as a slowly breathing presence in space. The default for "we want WebGL but it shouldn't compete with content."

**Three.js primitive**
```js
new THREE.IcosahedronGeometry(radius, detail)
// shader-accents: radius 1.6, detail 60
// 3d-scene:      radius 1.6, detail 80   (more verts = smoother distortion)
```

**Shader character.** Vertex shader displaces along normal by domain-warped noise (single layer warped twice — never an FBM stack, per restraint). Fragment shader maps noise distortion to colour bands + adds fresnel rim glow. Final `col *= 0.55` luminance ceiling.

**Animation.** Slow Y rotation at `~0.04 rad/s`. Mouse adds ±0.18 rad of tilt. Scroll adds up to 0.25 rad of inflation. Breathing: `0.94 + 0.06 * sin(t * 0.55)`.

**Position.** Off-centre upper-right (e.g. `(2.4, 1.0, -1.2)`) so content owns the centre column.

**Library fit.** Native default for warm-editorial, atmospheric-protocol, sanctuary-tech. Acceptable for basalt, technical-refined as the calm option. Refuse for memoir, spritify.

**Anti-patterns.**
- ❌ Centred — competes with text
- ❌ Bright (no luminance cap) — text overlay fails contrast
- ❌ FBM noise stack — costs perf without visible benefit at this radius

**Bundle delta.** ≈ 0 KB (pure shader on a primitive that ships with Three.js core).

---

## 2. Wireframe Geode — `DodecahedronGeometry` + `EdgesGeometry` overlay

**Vibe.** Technical, instrument-like, geometric. Low-poly faceted form with edges drawn as lines. Reads as a precision artefact — calipers, satellite, schematic.

**Three.js primitive**
```js
const baseGeo  = new THREE.DodecahedronGeometry(radius, 0);    // detail 0 = pure 12-face form
const edgesGeo = new THREE.EdgesGeometry(baseGeo);             // edge lines for wireframe overlay
const mesh     = new THREE.Mesh(baseGeo, fillMat);             // semi-translucent fill
const wire     = new THREE.LineSegments(edgesGeo, lineMat);    // crisp edge highlights
mesh.add(wire);
```

**Shader character.** Fill material is a `ShaderMaterial` with very low opacity (~0.18-0.25) — just enough to give the form some volume. Edge material is `LineBasicMaterial` with the library accent colour (full opacity). The result reads as "transparent crystal with glowing edges." NO noise displacement — the geometry's faceting is the visual signal.

**Animation.** Slow combined-axis rotation: Y at `0.06 rad/s`, X at `0.025 rad/s`. Mouse adds tilt. NO breathing pulse — geometric primitives shouldn't feel alive, they should feel built.

**Position.** Can be centred (the wireframe is naturally "transparent" — text reads through). Larger radius works (~2.4-3.0). Off-centre also fine.

**Library fit.** Native default for technical-refined (instrument register), basalt (clean precision). Acceptable for atmospheric-protocol, sanctuary-tech. Refuse for spritify, warm-serene-luxury.

**Anti-patterns.**
- ❌ Wireframe rendered ON TOP of solid fill — kills the "translucent crystal" effect, reads as solid object with messy lines
- ❌ Detail > 0 on `DodecahedronGeometry` — subdivides the faces, defeats the angular character
- ❌ Bloom on edges — line geometry + bloom = hairy artefacts. Keep bloom off this geometry, OR bloom only the fill (selective bloom).

**Bundle delta.** ≈ 0 KB.

---

## 3. Crystal / Octahedron — `OctahedronGeometry` with sharp facets

**Vibe.** Edgy, prismatic, bold. Sharp diamond/crystal form with high-contrast fresnel and faster rotation. Reads as a focal object, not background atmosphere.

**Three.js primitive**
```js
new THREE.OctahedronGeometry(radius, 0)  // detail 0 = pure 8-face octahedron
// or use 1 for slightly more facets, never higher
```

**Shader character.** Fragment shader uses VERY strong fresnel (`pow(1.0 - dot(N, V), 0.8)` — much sharper than the blob's 1.4). Two-tone palette: dark inner facets, bright accent rim. Optional: hue-shift on the rim based on view angle (prismatic effect — `mix(accent, secondaryAccent, fresnel)`). Final `col *= 0.65` ceiling.

**Animation.** Faster than the blob: Y rotation at `0.10 rad/s`, plus an X axis tumble at `0.03 rad/s` for that "floating crystal" feel. Mouse adds substantial tilt (±0.30 rad) — this geometry is the most interactive of the catalog.

**Position.** Often centred or slightly off-centre — this geometry is meant to be looked at. Smaller radius (~1.0-1.4). The crystal is the focal point.

**Library fit.** Native default for neo-brutalist (sharpness matches), creative-studio (bold agency hero), playful-bento (energy). Acceptable for technical-refined as a pop. Refuse for warm-editorial, sanctuary-tech (too aggressive).

**Anti-patterns.**
- ❌ Centred AND large — becomes a desktop screensaver, blocks content
- ❌ Soft fresnel — defeats the entire "crystal" character, reads like an awkward blob
- ❌ Slow rotation — sharp geometry needs energy to read as alive; under 0.06 rad/s reads as broken

**Bundle delta.** ≈ 0 KB.

---

## 4. Plane Displacement — `PlaneGeometry` heightmapped by noise

**Vibe.** Calm, horizon-like, ambient. A subdivided plane with vertices displaced upward by noise. Reads as a topographic landscape, a fluid surface, or a stratified atmosphere depending on tilt and palette.

**Three.js primitive**
```js
new THREE.PlaneGeometry(width, height, segmentsX, segmentsY)
// shader-accents: 12×8, segments 100×60
// 3d-scene:      14×9, segments 140×80
```

**Shader character.** Vertex shader displaces Z by noise lookup at the (x, y) world position, modulated by `uTime` for slow drift. Fragment shader uses noise value to mix between two palette colours + a soft fog at the back edge. NO fresnel (planes don't fresnel meaningfully).

**Animation.** Plane is tilted forward (rotation X ≈ -1.0 rad) so it recedes into the distance like a horizon. Time advances the noise lookup at `0.05 rad/s`. Mouse pans the noise origin by ±0.5. Camera mostly still.

**Position.** Bottom of viewport (`y: -1.5`), large extent (12-14 units wide). Tilted toward camera. Acts as a "ground" rather than a "subject."

**Library fit.** Default subtle option for warm-serene-luxury (parchment haze), warm-editorial (paper-like landscape). Acceptable for atmospheric-protocol as an alt to the blob. Refuse for neo-brutalist (too soft), spritify, basalt (geometry should be more deliberate for ecommerce).

**Anti-patterns.**
- ❌ Horizontal plane (`rotation.x = 0`) — looks like a tablecloth, not a horizon
- ❌ High amplitude displacement — turns into a turbulent landscape, contradicts the "calm" register
- ❌ Frontal camera angle — kills the horizon effect

**Bundle delta.** ≈ 0 KB.

---

## 5. Torus Knot — `TorusKnotGeometry` with parametric rotation

**Vibe.** Mathematical, considered, premium-tech. A self-intersecting parametric curve that rotates slowly. Reads as research, instrument, "complexity rendered legible."

**Three.js primitive**
```js
new THREE.TorusKnotGeometry(radius, tube, tubularSegments, radialSegments, p, q)
// e.g. (1.0, 0.30, 200, 24, 2, 3) — classic 2,3 knot
// (1.0, 0.22, 240, 20, 3, 4) — denser, more woven
```

**Shader character.** Fragment shader uses tangent-based colouring: project view direction onto the tube's local tangent, use that to drive a fresnel-like rim. Two-tone palette: dark base, accent on the curving rim. NO noise — the geometry's mathematical character is the signal.

**Animation.** Y rotation at `0.05 rad/s`, gentle tilt on X at `0.02 rad/s`. NO mouse-driven distortion (it would break the mathematical purity). Mouse only nudges the camera position by ±0.2.

**Position.** Centre or slight off-centre. Radius ~1.0-1.4. Works equally well behind a hero or as an in-page accent.

**Library fit.** Strong alt for atmospheric-protocol (instrument register), technical-refined (mathematical instrument). Acceptable for basalt (research-precision feel). Refuse for spritify, warm-serene-luxury (too cerebral).

**Anti-patterns.**
- ❌ p/q values that produce a trivial knot (e.g. p=1, q=1 → a flat torus) — no visual complexity
- ❌ Noise displacement on the geometry — destroys the parametric character. If you want organic, use the blob.
- ❌ Excessive rotation speed — the knot's value is its readability, not its animation

**Bundle delta.** ≈ 0 KB.

---

## 6. Particle Ribbon — `BufferGeometry` + `Line` with displacement shader

**Vibe.** Kinetic, signal-as-line, flowing. A single continuous line snaking across the viewport, displaced by time-varying noise. Reads as data flow, signal, breath.

**Three.js primitive**
```js
const N = 800;  // shader-accents
// const N = 1600;  // 3d-scene
const positions = new Float32Array(N * 3);
for (let i = 0; i < N; i++) {
  positions[i*3]   = -6 + (12 * i / N);   // x: spread across viewport
  positions[i*3+1] = 0;                    // y displaced in vertex shader
  positions[i*3+2] = 0;
}
const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const ribbon = new THREE.Line(geo, lineShaderMat);
```

**Shader character.** Vertex shader displaces Y by noise of (x, time) — produces a wavy line that drifts. Fragment shader uses a glow-along-line technique: line colour fades from accent at the start to transparent at the end (or pulses alpha based on position). Optional: thicken the line via `LineMaterial` (line2 addon) if you need width control.

**Animation.** Constantly evolving noise — the ribbon never repeats. Time at `0.4 rad/s`. NO mouse interaction, NO scroll. The ribbon is autonomous flow.

**Position.** Spans the viewport width or diagonal. Multiple ribbons CAN coexist (max 3) but each must be independent — never crossing meaningfully (crossing reads as bug).

**Library fit.** Strong alt for creative-studio (kinetic agency hero), technical-refined (data viz signal). Acceptable for atmospheric-protocol as a calmer alt-pulse. Refuse for warm-editorial, warm-serene-luxury, sanctuary-tech (too kinetic for those registers).

**Anti-patterns.**
- ❌ More than 3 ribbons on screen — visual chaos, looks like a glitch
- ❌ Adding particles around the ribbons — undoes the "single signal" point of the geometry. The ribbon is the signal; the rest is silence.
- ❌ Ribbons that loop tightly — turns into a tangle. The flow direction should be readable.

**Bundle delta.** ≈ 5 KB if using Three's core `Line`. ~25 KB if you need `Line2` from addons (for variable width).

---

## Anti-stacking rule

**Pick exactly ONE geometry per project.** Combining (e.g. blob + ribbon, or geode + crystal) destroys the visual reading. The single-signal contract is what separates "designed background" from "tech demo."

The one allowed exception: **a Plane Displacement (Geometry 4) under a primary geometry** — e.g. crystal floating above a horizon plane. This works because the plane is unambiguously "ground" and the primary is unambiguously "subject." Even then, the plane stays subtle (low displacement amplitude, low contrast against bg).

If a brief seems to demand multiple geometries, the right move is usually:
- Pick the most expressive one, drop the rest, OR
- Step down to `dimension: shader-accents` and use a single-pass fragment shader on a plane (atmospheric noise field)

---

## Per-library default geometry table

The skill picks the default automatically when `dimension > none` is selected and no specific geometry is requested. Override is allowed but flagged in provenance.

| Library | Default geometry | Containment | Allowed alts |
|---|---|---|---|
| Neo-Brutalist | 3 (Crystal) | hero-absolute | none — sharpness must dominate |
| Editorial Portfolio | — (geometry rarely fits this register) | — | 4 (Plane), 1 (Blob, very subtle) only if user explicitly asks |
| Technical Refined | 2 (Wireframe Geode) | fullscreen-fixed | 5 (Torus Knot), 6 (Particle Ribbon for data viz) |
| Basalt E-Commerce | — (3D = configurator territory, see `webgl-3d-tactics.md`) | hero-absolute | 2 (Geode), 5 (Torus Knot) for atmospheric brand pages |
| Memoir Blog | refuse | — | refuse |
| Creative Studio | 3 (Crystal) | hero-absolute | 6 (Particle Ribbon), 1 (Blob) |
| Warm Serene Luxury | 4 (Plane Displacement) | fullscreen-fixed (light-page-aware) | 1 (Blob) very subtle only |
| Playful Bento | 3 (Crystal) per cell, OR shader-accents only | per-cell-absolute | 1 (Blob) per cell |
| Spritify | refuse `3d-scene` | — | shader-accents only, geometry irrelevant |
| Sanctuary Tech | FORCED none in trauma-informed mode | — | — |
| Warm Editorial | 1 (Distorted Blob) | fullscreen-fixed | 4 (Plane) very subtle |
| Atmospheric Protocol | 1 (Distorted Blob) | fullscreen-fixed | 5 (Torus Knot), 2 (Geode) |

---

## Provenance fields

Each build records the geometry choice in DESIGN.md frontmatter:

```yaml
provenance:
  dimension:
    tier: 3d-scene
    geometry:
      id: 2                                 # 1-6 from this catalog
      name: wireframe-geode
      containment: fullscreen-fixed         # fullscreen-fixed | hero-absolute | per-cell-absolute
      override-of-default: false            # true if user requested a non-default geometry
      override-reason: ""                   # filled if override-of-default true
```

This block is part of the divergence audit — it proves the geometry was a deliberate choice, not an accidental "default to blob."
