# WebGL / 3D × Style Library Compatibility

Not every style library hosts 3D well. This file is the per-library compatibility matrix and the rationale behind each default. Loaded by the agent in Phase 2 when the chosen `dimension` tier is anything other than `none`.

The matrix below is the **default**. The user can override (per `user-overrides.md`), but if the override violates a hard constraint (trauma-informed + 3D, Memoir + 3d-scene), the skill flags it and either escalates to user or refuses the override and documents the trade-off in provenance.

---

## Compatibility matrix

| Library | Default `dimension` | Allows `shader-accents` | Allows `3d-scene` | Hard refuse | Notes |
|---|---|---|---|---|---|
| **Neo-Brutalist** | `none` | ✓ | ✗ | — | Poster type and grid carry the weight. Shader allowed for high-contrast Voronoi / noise-block backgrounds — must read as graphic, not as polish. No 3D models. |
| **Editorial Portfolio** | `none` | ⚠ rare | ⚠ only if it IS the work | — | Off-white #f4f3f0 canvas, photographic imagery. 3D allowed only when a portfolio item is itself a 3D piece — meta-display, not decoration. |
| **Technical Refined** | `none` | ✓ | ✓ data viz | — | Geist/teal palette pairs well with shader grain (subtle grid-aligned noise) or genuine 3D data viz (network topology, warehouse heatmap). Refuse decorative spinning cubes. |
| **Basalt E-Commerce** | `none` | ⚠ rare | ✓ configurator | — | The strongest `3d-scene` fit: product configurators (rotate, customise, inspect). Shader rarely fits — Basalt is grayscale-disciplined, shader noise reads as visual junk. |
| **Memoir Blog** | `none` | ✗ | ✗ | trauma-adjacent? | Reading-first. Cream surfaces, italic serifs, 720px columns. 3D defeats the entire register. Hard refuse unless the brief is a literary AR experiment, in which case escalate. |
| **Creative Studio** | `shader-accents` | ✓ | ✓ showcase | — | Dark charcoal + coral, agency energy. Default-on shader-accent for hero atmosphere. `3d-scene` for case-study showcases. The natural home for both tiers. |
| **Warm Serene Luxury** | `none` | ✓ subtle | ⚠ rare | — | DM Serif + #FAFAFA. Shader allowed only as parchment haze / soft particulate ambience — never high-contrast. `3d-scene` only for hospitality 360° tours; otherwise the photographic register carries it. |
| **Playful Bento** | `shader-accents` | ✓ | ✓ per cell | — | The bento grid was MADE for compartmentalised 3D — each cell can host an independent canvas. Use `InstancedMesh` and aggressive offscreen pause; 6+ canvases on one page will eat mobile GPU. |
| **Spritify** | `none` | ⚠ minimal | ✗ | kid audience | League Spartan, switchable colour schemes, kid-friendly. 3D is a perf risk on family devices (older phones, tablets). Shader allowed only for very small celebratory accents. Hard refuse `3d-scene`. |
| **Sanctuary Tech** | **FORCED `none`** | ✗ | ✗ | trauma-informed | Crisis support / healthcare / legal aid. Trauma-informed mode forces `dimension: none` regardless of user pick. Reasoning: cognitive load, GPU thermal throttling on older devices used by vulnerable users, `prefers-reduced-motion` already non-negotiable in this register. Document the forced override in provenance. |
| **Warm Editorial** | `shader-accents` | ✓ | ⚠ rare | — | Anthropic Serif + parchment + terracotta. The "AI product" register. Default-on shader-accent (warm noise tied to scroll or cursor) reinforces the literary-tech feel. `3d-scene` only when the AI product genuinely demos 3D output — not as decorative polish. |

---

## How to read the columns

- **Default `dimension`** — the value in the per-library defaults table when the user didn't specify. See `style-tuning.md` § Per-library defaults — the `dimension` column.
- **Allows `shader-accents`** — ✓ always allowed; ⚠ allowed with constraints (specified in Notes); ✗ refuse.
- **Allows `3d-scene`** — same scale.
- **Hard refuse** — non-negotiable refusal regardless of user override. Currently only Sanctuary Tech (trauma-informed). Memoir and Spritify are soft-refuse — the skill warns and asks for confirmation.

---

## Override protocol

When the user's `dimension` choice (via brief language, override, or interview) conflicts with the chosen library's default:

### Soft refuse (Memoir, Spritify)

The skill flags the conflict in delivery summary:

> Note: you've asked for `dimension: 3d-scene` on a Memoir-base build. Memoir is reading-first; 3D usually defeats that register. I've built it as requested, but if you want me to drop 3D and lean into typography, reply "drop 3d".

The build proceeds. The conflict is recorded in `provenance.tuning-conflicts`.

### Hard refuse (Sanctuary Tech + trauma-informed)

The skill does NOT build with `dimension > none`. It overrides to `none`, ships the static build, and records:

```yaml
provenance:
  trauma-informed-mode: true
  dimension:
    tier: none
    forced-override: true
    forced-override-reason: trauma-informed mode active; 3D contraindicated for vulnerable users
    user-requested-tier: 3d-scene  # what they asked for
```

This mirrors the page-load auto-demote rule already in `loader-patterns.md`.

### Library swap suggestion

If the user is insistent on 3D and the library refuses, the skill suggests a library that DOES host 3D:

> Memoir doesn't host 3D well — it would fight the reading register. If you want a 3D hero with editorial-feeling typography, the closest fit is Warm Editorial (Anthropic Serif + parchment, hosts shader-accents natively) or Creative Studio (agency-tier, hosts full 3D scenes). Want me to switch?

---

## When `3d-scene` is the right call across libraries

Three universal patterns where `3d-scene` earns its place regardless of library:

1. **Product configurator** — the user manipulates a 3D representation of a real product (furniture, sneakers, watches, glasses, bottles). Best fit: Basalt. Acceptable: Creative Studio, Technical Refined.
2. **Data visualisation that's genuinely 3D** — network topology with thousands of nodes, warehouse occupancy heatmap, financial correlation maps where the third dimension carries information. Best fit: Technical Refined. Acceptable: Creative Studio.
3. **Brand experience site** — agency / studio showreel where the 3D IS the pitch. Best fit: Creative Studio. Acceptable: Warm Editorial (if literary-tech), Playful Bento (if energetic).

Any other "we want a 3D hero" brief should be challenged with: would a beautifully-typed hero with a strong photo or a shader-accent background do the same job for 1/10 the bundle?

---

## When `shader-accents` is the right call across libraries

Easier sell — much smaller perf cost, much wider compatibility. Default-on for Creative Studio, Playful Bento, and Warm Editorial. Allowed everywhere except Memoir, Spritify (minimal-only), and Sanctuary Tech.

The shader's character must match the library:
- **Brutalist** — high-contrast block noise, Voronoi cells, heavy grain. Reads as graphic.
- **Technical Refined** — subtle grid-aligned noise, terminal-style scanline drift. Reads as instrument.
- **Basalt** — almost never; if used, monochrome paper grain only.
- **Creative Studio** — bold gradient flows, fluid distortions on hover. Reads as energy.
- **Warm Serene Luxury** — soft particulate haze, near-imperceptible drift. Reads as atmosphere.
- **Playful Bento** — vibrant noise per bento cell, optional shader-driven hover. Reads as play.
- **Warm Editorial** — warm parchment noise, scroll-reactive subtle distortion. Reads as paper texture.

The skill picks the shader character based on library + DESIGN.md tokens, then implements per `webgl-3d-tactics.md` § Tier 1.

---

## Tier-coupling reminder

A `3d-scene` with `motion: low` is dead — a sculpture, not a scene. The skill enforces:

- `dimension: 3d-scene` requires `motion: medium` minimum
- If user picked `motion: low` + `dimension: 3d-scene`, surface a tier-coupling warning (per `style-tuning.md` Tier-coupling rule). Build as specified; record conflict.

A `shader-accents` build is fine at any motion level — the shader's RAF loop is its own animation budget separate from DOM motion.

---

## Audit trail

The build records library-fit decisions in DESIGN.md provenance:

```yaml
provenance:
  library-derivation:
    base: warm-editorial
  dimension:
    tier: shader-accents
    library-fit-decision: warm-editorial-default-allows-shader-accents
    shader-character: warm-parchment-noise-scroll-reactive
```

When a forced override or library swap happened, the audit trail captures it:

```yaml
provenance:
  dimension:
    tier: none
    forced-override: true
    user-requested-tier: 3d-scene
    forced-override-reason: sanctuary-tech-trauma-informed
```

---

## Liquid Glass — WebGL Refraction Track

When `effects.liquid-glass === true` AND `style-tuning.axes.dimension.value === 'shader-accents'`, the WebGL/SDF refraction track for the Liquid Glass modifier becomes available. This is an opt-in secondary use of the shader-accents WebGL context — it does not replace the primary shader-accents background effect.

**The four mandatory failure-mode guards in this file's pre-build checklist apply identically to the Liquid Glass refraction track.** Do not re-implement them in `references/effects/liquid-glass.md` — cross-reference:

- Guard 1 — WebGL feature detect (with DOM fallback to CSS track)
- Guard 2 — Reduced motion (static frame, no morphing)
- Guard 3 — DOM mirror for SEO / a11y AND legibility scrim
- Guard 4 — Load timeout

**Auto-refuse cases for the refraction track:**
- Mobile-first projects (GPU budget too constrained for backdrop compositing + shader)
- Sanctuary Tech (hard refuse regardless of dimension setting)
- `dimension: 3d-scene` already active (WebGL context conflict)

For the full refraction track implementation contract, see `references/effects/liquid-glass.md` § WebGL/SDF refraction track.
