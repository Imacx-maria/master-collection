# Style Tuning

The skill picks a style library; **Style Tuning lets the user fine-tune 10 plain-language design questions (plus an 11th conditional axis for trauma-informed work)** before the project DESIGN.md is derived. The user never sees library names — the skill maps the 10 answers to the closest library internally and uses it as a base.

Load this in **Phase 2 Step 2.1** — BEFORE any library is chosen. The interview answers drive the library mapping in Step 2.2.

---

## When to use Style Tuning — BLOCKING INTERVIEW

**This is a blocking interactive step. The skill CANNOT proceed to Step 2.2 (library mapping) without explicit user response on every question (1–10, plus optional 11 if trauma-informed).**

**Silence is NOT consent to defaults.** Absence of an answer means the agent must ask. The agent MUST wait for the user to respond before generating any markup or DESIGN.md content.

This is the same enforcement tone as Phase 4.7 (self-correction loop) — it exists because the failure mode (skipping the interview, deciding internally, then shipping) was observed in real builds. The interview is what turns the skill from "auto-apply 11 fixed styles" into "user-directed hybridisation". Skipping it is a critical failure mode.

### What blocks vs. what doesn't

| Situation | Blocked? |
|---|---|
| User has not yet been asked the 10 questions | YES — must ask now |
| User was asked but hasn't responded | YES — must wait |
| User responded "you decide" / "let Claude choose" on every axis | NO — proceed (their delegation is the answer) |
| User responded with explicit values + "you decide" mix | NO — proceed (mixed delegation is valid) |
| User explicitly said "skip the interview, just build" | NO — but log the override in provenance as `interview-skipped: user-requested`; this is the only acceptable bypass |

**Universal escape per axis: every question offers `you decide` as a valid response.** The user can delegate any individual axis to the skill — but the delegation itself is an explicit answer, recorded in the manifesto as `user-delegated`. The agent never makes an axis decision silently.

**Library is never asked, never announced.** The user does not pick a library, does not see library names, and is never asked to confirm one. The skill maps the 9 answers to libraries internally in Step 2.2 (≥6/9 matches → that library is base; <6/9 → mix top 2-3) and records the mapping in `provenance.library-derivation` for audit only. The user judges the *output*, not the *label*.

---

## The interview format (prescribed — do not improvise)

The interview is **library-agnostic and silent on library mapping**. The user does not pick a library, does not see library names, does not need to know what `Spritify` or `Technical Refined` mean. They answer 9 plain-language questions about the look they want. The skill maps the answers to libraries internally in Step 2.2 (≥6/9 → base library; <6/9 → mix top 2-3 libraries; tied low → Custom / Freestyle). The user is never shown the chosen library and never asked to confirm one.

The agent **copies the template below verbatim** and presents it as a single message. Then the agent **stops and waits for a response**.

### Template

```
Quick design interview — 10 questions before I build.

Pick one option per question, or write "you decide" for any question you don't have an opinion on (I'll pick based on the brief). You can also reply "you decide for all" to delegate everything.

────────────────────────────────────────

1. COLOR MODE — light, dark, or both?
   • light — light backgrounds, dark text (most sites)
   • dark — dark backgrounds, light text (premium tech, terminals)
   • both — both modes with a toggle (pick only if users will live in this for hours)
   • you decide

2. FONTS — what kind?
   • sans — modern, clean
   • serif — editorial, literary
   • mix — display serif + body sans (magazine / premium feel)
   • you decide

3. LAYOUT — how should things sit on the page?
   • grid-based — predictable columns, things line up
   • loose — off-grid, breakouts, intentional asymmetry
   • you decide

4. CONTENT WIDTH — how wide should content sit?
   • narrow — reading-first, content-heavy
   • standard — default for most sites
   • wide — image-led, hospitality, agency
   • full-bleed — edge-to-edge spectacle, immersive
   • you decide

5. CORNERS — sharp or rounded?
   • sharp — 0px corners, edge-driven, brutalist
   • soft — gently rounded (~8-12px), balanced, contemporary
   • rounded — generous round (~16-24px), friendly, playful
   • you decide

6. MOTION — how much animation?
   • low — hover transitions only, almost nothing else moves
   • medium — above + scroll reveals + section transitions
   • high — chained timelines, parallax, micro-interactions everywhere
   • you decide

7. COLOR LOUDNESS — how saturated should the palette be?
   • muted — desaturated, near-grey, editorial restraint
   • balanced — mid saturation, default product feel
   • vibrant — full saturation, high-energy
   • monochrome — single hue + neutrals
   • you decide

8. IMAGERY — what kind of visuals?
   • photographic — real photos (people, places, products)
   • illustrative — illustrations, drawn art
   • abstract — shapes, gradients, geometric patterns
   • type-only — no imagery, typography carries the page
   • 3d — ThreeJS / WebGL particles, shaders
   • you decide

9. PAGE LOAD — what should happen before the page appears?
   • none — page just appears, no loader (fastest, default for most product sites)
   • subtle — quick fade-in or content-aware shimmer (refined polish, no spectacle)
   • functional — skeleton blocks, spinner, or progress bar while content loads (apps, feeds, dashboards, slow assets)
   • branded intro — full-screen logo / curtain wipe / signature reveal (agency, portfolio, marketing splash)
   • you decide

10. WEBGL / 3D — should the page include a live geometric backdrop?
    • none — no WebGL, no 3D. The page is flat. Default for most product, marketing, blog, and e-commerce sites.
    • shader-accents — animated fragment shader behind the page (warm noise, kinetic gradient, hover distortions, no imported 3D models). +~200 KB bundle, big atmosphere lift, low perf cost.
    • 3d-scene — full Three.js scene with one geometric figure (blob, crystal, wireframe geode, torus knot, etc.), bloom postprocessing, scroll-reactive. +~2 MB bundle, real perf cost. Best for AI products, brand showcases, premium tech, agencies.
    • you decide

{conditional: append axis 11 if trauma-informed mode is active OR copy will be auto-generated}

11. TONE — how should the writing sound?
    • playful — casual, energetic, light
    • professional — direct, factual, neutral
    • serious — formal, considered, weighted
    • clinical — precise, sterile, observational
    • empowering — strength-based, agency-focused, supportive
    • you decide

────────────────────────────────────────

Quick paths:
  • "you decide for all" → I make every choice based on the brief
  • "skip interview" → I run with sensible defaults (logged as user-requested skip)
```

### What was cut from earlier versions, and why

Previous versions of this skill asked 12 axes. Five were cut after observed user-facing failures (page-load was added back in a later iteration as Axis 9 once it became clear loaders were being silently invented):

- **Type weight** (light-airy / regular / bold) — cut. Weight is a consequence of the chosen library + type pairing, not a meaningful standalone question. Asking it forces design jargon.
- **Framing** (open / contained / panelled / floating) — cut. Even designers struggle to name what these mean. The library + corners choice already telegraph the answer.
- **Grid strength** (strong / subtle / loose) — cut. Designer-only concept. Folded into the simplified Layout question (grid-based / loose).
- **Surface density** (airy / balanced / dense) — cut. Non-designers don't think in these terms. Density is a consequence of layout + content, decided internally.
- **Card corners + Button corners as separate axes** — merged into single Corners question. Most projects use the same radius family across both. The rare register split (sharp surfaces + pill controls) is now an internal skill decision, not a user prompt.

Layout was simplified from 5 sub-types to 2 (grid-based / loose). The skill picks the specific sub-type (uniform grid, asymmetric, bento, poster, column-narrow) internally based on the chosen library and content type.


### Parsing the response

The agent parses the user's reply and produces the tuning manifesto:

- **Explicit value** (e.g., `2: mix`) → `fonts: mix, source: user-chosen`
- **`you decide`** (or natural-language equivalents like "no idea", "you pick", "no preference") → agent picks based on brief intent, `source: user-delegated`, with one-line rationale recorded
- **Missing axis in response** → re-ask only the missing ones (single follow-up — don't loop more than twice)
- **Contradictory or unrecognised value** → ask once for clarification on that axis only, then accept whatever the user says

After the second reply (if needed), the agent maps the 9 answers to the nearest library (Step 2.2 in SKILL.md), announces it for confirmation, then proceeds to derive the DESIGN.md.

### Tier-coupling rule — motion × page-load

When `motion: low` AND `page-load` is `functional` or `branded-intro`, the combination is permissive but contradictory ("almost nothing moves" + "the page enters with a 2-second curtain wipe"). It can be a coherent design choice — brutalist sites with one signature intro then dead silence are real — but it is more often a misclick.

**Rule (soft warn-and-build):**
1. Build the requested combination as specified — do not auto-demote.
2. Surface a one-line warning in the delivery summary: `Note: motion: low + page-load: branded-intro is unusual. The page will load with a full intro animation, then sit nearly static. Reply "demote loader" to drop to subtle, or "lock motion" to keep as-is.`
3. Record the conflict in `provenance.tuning-conflicts` with `acknowledged: false` until the user responds.
4. The conflict is non-blocking. Build proceeds.

This rule is documented here AND mirrored in `loader-patterns.md` § Tier compatibility. Do not silently demote.

### What the agent must NOT do

- ❌ Decide axes silently and write "I picked X for you" in the build summary
- ❌ Skip the interview because the brief "seems clear"
- ❌ Treat partial response as full response (must follow up on missing axes)
- ❌ Auto-fill `you decide` axes without recording rationale
- ❌ Proceed to Step 2.3 without an interview record in the DESIGN.md frontmatter

---

## The 9 Questions (plus 1 conditional)

Each question has 2-5 options. The user picks one OR writes `you decide`. Library is derived from the answers (Step 2.2 in SKILL.md), never asked.

### 1. Color mode

The most upstream design decision: light, dark, or both?

- **`light`** — Light mode only. Default for most product/marketing surfaces. Page bg = light neutral, surfaces white/off-white, text near-black.
- **`dark`** — Dark mode only. Page bg in #0A0A0A–#141414 range (never pure #000), surfaces slightly lighter, text near-white but not pure white. Sanctuary Tech, Brutalist no-light variant, retro-terminal.
- **`both`** — Both modes shipped, with a toggle or `prefers-color-scheme` media query. Doubles colour-token work. Phase 4.5 audits dark-mode discipline.

**When to push `both`:** dashboards, dev tools, products users sit in for hours.
**When to push `light` only:** marketing landing pages, e-commerce, hospitality, editorial-portfolio.
**When to push `dark` only:** brand commitment to dark aesthetic.

### 2. Fonts

What font character drives the page. Three plain options — the skill decides if a technical/mono pairing is right based on the rest of the answers (e.g., layout=grid + corners=sharp + loudness=monochrome → skill picks mono-leaning fonts internally, even though the user said "sans").

- **`sans`** — Sans family for everything. Clean, modern. Skill picks the specific sans (geometric, humanist, neo-grotesk, mono-style sans like Geist Mono) based on the chosen library and the other axes.
- **`serif`** — Serif family for everything. Editorial, literary, traditional.
- **`mix`** — Display serif + body sans. Magazine register, premium, contemplative.

### 3. Layout

The page-level composition logic, simplified to the user-facing question.

- **`grid-based`** — Predictable columns, things line up, fixed grid honoured. Skill picks the specific sub-type internally (uniform grid, bento-led, poster) based on library + content.
- **`loose`** — Off-grid moments, asymmetry, breakouts. Skill picks the specific sub-type internally (asymmetric editorial, hero+supporting, column-narrow with breakouts).

### 4. Content width

The container max-width across sections.

- **`narrow`** — ~720-800px. Reading-first, memoir, content-heavy.
- **`standard`** — ~1200-1280px. Default for most product surfaces.
- **`wide`** — ~1400-1600px. Image-led, hospitality, agency portfolio.
- **`full-bleed`** — 100vw with internal padding. Spectacle, immersive, hero-driven.

### 5. Corners

Personality telegraph (Wathan: small=neutral, large=playful, none=formal). Single axis applied to surfaces AND controls — the skill keeps them aligned by default. Register splits (e.g., sharp surfaces + pill controls) are decided internally when the chosen library calls for it.

- **`sharp`** — 0px corners. Edge-driven, brutalist, sanctuary-tech, editorial.
- **`soft`** — 8-12px corners. Balanced, contemporary, default product UI.
- **`rounded`** — 16-24px corners. Friendly, approachable, kid/family, marketing energy.

### 6. Motion

Animation budget.

- **`low`** — Hover state colour/opacity transitions (150-250ms). Almost nothing else moves. Editorial, memoir, technical, accessibility-first.
- **`medium`** — Above + scroll reveals (one-time fade-up, GSAP ScrollTrigger), section transitions. Default for most product surfaces.
- **`high`** — Above + chained timelines, parallax, hero animations, micro-interactions on every interactive. Marketing, creative, agency.

### 7. Color loudness

How loud the palette reads.

- **`muted`** — Desaturated, editorial. Tones near grey, deliberate restraint. Memoir, basalt, sanctuary.
- **`balanced`** — Mid saturation. Default product palettes.
- **`vibrant`** — Full saturation, high-energy. Spritify, playful-bento, marketing.
- **`monochrome`** — Single hue (or near-monochrome) + neutrals. Technical-refined, brutalist accent-only.

### 8. Imagery

How visual assets shape the page.

- **`photographic`** — Real photography (people, places, products). Hospitality, lifestyle, e-commerce.
- **`illustrative`** — Custom or stock illustrations. Editorial, kids/family, friendly product.
- **`abstract`** — Shapes, gradients, generative patterns, no representational imagery. Tech, modern brand.
- **`type-only`** — No imagery; typography carries the page. Brutalist, editorial-poster, manifesto sites.
- **`3d`** — ThreeJS / WebGL hero, particle fields, shader effects. Premium tech, retro-futurist, AI tools.

### 9. Page load

What happens before / as the page first becomes visible. This is a separate concern from `motion` (which governs in-page animation). A `motion: low` page can still have a `branded-intro` loader; a `motion: high` page can ship with `page-load: none` if the LCP budget is tight.

The skill maps the user's role choice to a specific visual pattern internally (curtain wipe vs logo reveal vs SplitText reveal vs skeleton+shimmer vs spinner vs progress bar) based on the chosen library + imagery + corners. The user picks the *role*; the skill picks the *pattern*. See `loader-patterns.md` for the mapping table.

- **`none`** — No loader. Browser-native paint. Default for most product surfaces; speed > theatre. The page just appears.
- **`subtle`** — Quick fade-in (~200-400ms) on `body`, or content-aware shimmer on hero image while it decodes. Polish without spectacle. The user notices the page loaded smoothly, never that there *was* a loader.
- **`functional`** — Skeleton blocks (fake layout that mimics final structure), spinner, or progress bar. Communicates "wait, content coming" when the wait is real (heavy assets, async data, predictable structure). Best for apps, dashboards, content feeds.
- **`branded-intro`** — Full-screen loader as a brand statement: logo reveal (DrawSVG stroke animation), curtain wipe (clip-path translation), animated wordmark (SplitText), or signature mask reveal. Adds 600-2000ms before content paints. Use when the brand earns it — agency, portfolio, hero-driven marketing splash. Not for product surfaces.

**When to push `none`:** technical-refined, sanctuary-tech, memoir, anything where every millisecond toward LCP matters more than craft theatre.
**When to push `subtle`:** warm-editorial, basalt, warm-serene-luxury, anything that wants polish but not spectacle.
**When to push `functional`:** dashboards, e-commerce listings with image grids, content feeds, anywhere the wait is real and unpredictable.
**When to push `branded-intro`:** creative-studio, neo-brutalist (signature curtain), spritify (bouncy logo), playful-bento — sites that already commit to motion as identity.

**Tier compatibility (soft warn):** `motion: low` + `page-load: functional` or `branded-intro` is allowed but flagged. The page enters loud and then sits silent. Coherent in some brutalist / single-statement designs; usually a misclick. See "Tier-coupling rule" above.

---

### 10. Dimension (WebGL / 3D depth)

Always asked. Promoted from conditional to mandatory because the failure mode (silently picking `none` and never offering 3D, OR silently picking 3D when the brief doesn't justify it) was observed in real builds. This decision is too consequential — bundle size, LCP, visual register all change — to be a brief-keyword trigger.

The user picks the *tier*; the skill picks the *implementation* per `webgl-3d-tactics.md` (shader content tuned to library + DESIGN.md tokens; scroll integration via GSAP ScrollTrigger or R3F-scroll-rig; mobile LOD selection).

- **`none`** — No WebGL, no 3D. Default for all imagery values except `3d`. The browser paints DOM and that's the end of it.
- **`shader-accents`** — Fragment shaders only. Noise gradients, liquid hover distortions, kinetic backgrounds. ~200 KB bundle ceiling. No imported 3D models, no camera, no lights. Allowed on most libraries; default-on for Creative Studio, Playful Bento, Warm Editorial.
- **`3d-scene`** — Full Three.js scene: imported GLB models (Draco-compressed), KTX2 textures, PBR materials, scroll-driven camera path, optional ONE post-processing pass. ≤ 2 MB compressed bundle. Best for product configurators, brand showcases, genuine 3D data viz.

**There is no `immersive` tier.** WebXR, multiplayer, complex physics, ray tracing, Pixel Streaming are explicitly out of scope. The skill refuses these briefs and refers to a specialist (per `webgl-3d-tactics.md` § Out of scope).

**When to push `none`:** the default for 90% of projects. Marketing landing pages, content sites, dashboards, blogs, e-commerce listings — DOM + strong typography + motion outperform decorative 3D every time.

**When to push `shader-accents`:** AI-product / agency / creative-studio / playful-bento briefs where atmosphere matters. Cheap perf cost, big visual lift.

**When to push `3d-scene`:** the product genuinely IS the 3D thing — configurators, 3D data viz, brand experience showcases. Or the brand is paying the 3D tax deliberately (premium tech, retro-futurist, hospitality with cinematic ambition).

**Hard refusal — Sanctuary Tech + trauma-informed mode:** `dimension` is FORCED to `none` regardless of user pick. Cognitive load, GPU thermal throttling on older devices used by vulnerable users, and the trauma-informed "no surprise motion" contract make 3D contraindicated. Document forced override in provenance. See `webgl-3d-style-fit.md` § Override protocol.

**Library compatibility:** see `webgl-3d-style-fit.md` for the per-library matrix. Memoir refuses 3D (reading-first); Spritify refuses `3d-scene` (kid audience, perf risk); Sanctuary Tech refuses both (trauma-informed).

**Tier coupling:** `dimension: 3d-scene` requires `motion: medium` minimum. A static 3D scene reads as broken, not as deliberate. If user picked `motion: low` + `dimension: 3d-scene`, surface a tier-coupling warning and record the conflict in provenance.

---

## Bonus question (conditional)

### 11. Tone register

Only asked when **trauma-informed mode** is active (Phase 1.0.5 fired) OR when copy will be auto-generated.

- **`playful`** — Casual, energetic, light. Kids, social products.
- **`professional`** — Direct, factual, neutral. SaaS, B2B.
- **`serious`** — Formal, considered, weighted. Legal, finance, news.
- **`clinical`** — Precise, sterile, observational. Medical research, scientific.
- **`empowering`** — Strength-based, agency-focused, supportive. Trauma-informed, healthcare, advocacy.

If trauma-informed mode is active and the user picks `playful` or `clinical`, flag the conflict — those tones can be re-traumatising or alienating. Suggest `empowering` and document if the user overrides.

---

## Effects (not an interview axis — set during Phase 1 detection)

**Liquid Glass effect:** yes / no. Default: no.

This flag is NOT asked in the style interview. It is set automatically in Phase 1 Step 1.5 when the user's prompt contains glass/liquid-glass/frosted/Apple-style/iOS-26 language. It can also be set manually if the user requests glass surfaces after the interview.

When `liquid-glass: true`, the Phase 2 compatibility check (Step 2.6) runs before the build proceeds.

### Per-library liquid-glass defaults

| Style | Offer if | Behavior |
|-------|---------|---------|
| Atmospheric Protocol | Always — it's native | Native tier: glass compatible everywhere chrome appears |
| Adaptive AI Console | Always — it's native | Native tier: glass compatible on command palette, composer, toasts |
| Creative Studio | Always — it's native | Native tier: glass compatible on nav, lightbox, hero overlays |
| Technical Refined | User prompt implies premium floating UI | Conditional: load constraints before build |
| Warm Serene Luxury | User prompt implies premium floating UI | Conditional: load constraints before build |
| Editorial Portfolio | User prompt implies premium floating UI | Conditional: load constraints before build |
| Motion-Directed Spatial Portfolio | User prompt implies premium floating UI | Conditional: load constraints before build |
| Neo-Brutalist | Do not offer | Refused: single-element override only if user names it |
| Memoir Blog | Do not offer | Refused: single-element override only if user names it |
| Sanctuary Tech | Never offer — hard refuse | Hard refuse: reject if user names it, no override |
| Basalt E-Commerce | Do not offer | Refused: single-element override only if user names it |
| Spritify | Do not offer | Refused: single-element override only if user names it |
| Playful Bento | Do not offer | Refused: single-element override only if user names it |
| Warm Editorial | Do not offer | Refused: single-element override only if user names it |

---

## Per-library defaults (10-axis profile)

These are the starting points before user tuning. Each library has been profiled against the 10 questions; the user never sees this table.

| Library | Color mode | Fonts | Layout | Width | Corners | Motion | Loudness | Imagery | Page load | Dimension |
|---|---|---|---|---|---|---|---|---|---|---|
| **Neo-Brutalist** | light | sans | grid-based | wide | sharp | low | monochrome | type-only | branded-intro | none |
| **Editorial Portfolio** | light | mix | loose | wide | sharp | low | muted | photographic | subtle | none |
| **Technical Refined** | both | sans | grid-based | standard | soft | low | monochrome | abstract | none | none |
| **Adaptive AI Console** | dark | sans | grid-based | standard | soft | low | monochrome | abstract | functional | none |
| **Basalt E-Commerce** | light | mix | grid-based | wide | soft | low | muted | photographic | subtle | none |
| **Memoir Blog** | light | mix | loose | narrow | sharp | low | muted | photographic | none | none (refuse 3d-scene) |
| **Creative Studio** | light | mix | loose | wide | soft | high | balanced | photographic | branded-intro | shader-accents |
| **Motion-Directed Spatial Portfolio** | dark | mix | loose | full-bleed | sharp | high | monochrome | 3d | subtle | 3d-scene |
| **Warm Serene Luxury** | light | mix | loose | wide | sharp | medium | muted | photographic | subtle | none |
| **Playful Bento** | light | sans | grid-based | standard | soft | medium | vibrant | abstract | branded-intro | shader-accents |
| **Spritify** | light | sans | grid-based | standard | rounded | high | vibrant | illustrative | branded-intro | none (refuse 3d-scene) |
| **Sanctuary Tech** | dark | sans | loose | narrow | sharp | low | monochrome | type-only | none | none (FORCED — trauma-informed) |
| **Warm Editorial** | both | mix | loose | standard | soft | low | muted | abstract | subtle | shader-accents |
| **Hushed Premium SaaS** | light | mix | loose | wide | rounded | medium | muted | abstract | subtle | none |
| **Custom / Freestyle** | — | — | — | — | — | — | — | — | — | — |

When `Custom / Freestyle` is chosen, the skill skips library mapping entirely and builds DESIGN.md directly from the 10 user answers.

---

## Library mapping logic (Step 2.2 in SKILL.md)

The skill maps the 10 user answers against the per-library defaults table and counts matches per library. Then:

- **Highest match score ≥ 7/10** → that library is the **base**. The skill applies its full system as foundation, then overrides only the specific axes the user answered differently. The chosen library is logged in `provenance.library-derivation`, never announced to the user for confirmation.
- **Highest match score < 7/10** → no clear winner. The skill mixes the **top 2-3 libraries** (those with the highest scores, even if below threshold) to cover the answer set. This produces a genuine hybrid built from the mixture — no single template, constructed from the parts that match.
- **All scores tied at low values** → fall back to **Custom / Freestyle**: build DESIGN.md directly from the 10 user answers without any library template as foundation.

The user NEVER sees the library mapping. It is internal craft, recorded in provenance for audit only. The user sees the output (the DESIGN.md and the build) and judges it on its own merits — they don't have to learn library names to use this skill.

If the user dislikes the result, they course-correct in plain language ("more techy", "less playful", "darker"), and the skill re-maps and rebuilds. They never have to identify which library to switch to.

---

## Tuning protocol — step by step

The agent runs this sequence. **Each step blocks the next.**

1. **Compose the interview message** by copying the prescribed template above verbatim. No library has been chosen at this stage. Axes 1-10 are always asked (including dimension at axis 10). Append axis 11 (tone) only if trauma-informed mode is active OR copy will be auto-generated.

2. **Send the interview as a single message and STOP.** Do not generate any markup, DESIGN.md, library guess, or follow-up reasoning before the user responds. The skill is paused at this point.

3. **Parse the user's response.** Each axis must end up with `source: user-chosen` or `source: user-delegated` (with rationale).

4. **If response is partial** (some axes missing) — send a single follow-up asking only the missing axes. Do not re-ask answered ones. Do not loop more than twice.

5. **Map answers to libraries** using the per-library defaults table:
   - Count match score per library (0-10 axes match).
   - If top score ≥ 7/10 → that library is base; overrides applied for non-matching axes.
   - If top score < 7/10 → mix top 2-3 libraries.
   - Log mapping in `provenance.library-derivation` with method, top scores, and final decision.

6. **Build the tuning manifesto** (YAML format below) with `user-confirmed: true`, per-axis `source` field, and the library derivation block. The user is NOT shown library names; they're recorded for audit only.

7. **Hand off to Step 2.3** with the manifesto as source of truth.

---

## Output format (added to project DESIGN.md frontmatter)

The tuning manifesto records both the **value** chosen for each axis AND the **source** of that value. The `source` field is the audit trail proving the interview happened. Library derivation is internal logging.

Source values:
- `user-chosen` — user wrote an explicit option from the menu
- `user-delegated` — user wrote "you decide" / "you pick" / "no idea" / "no preference"; agent picked, rationale recorded
- `user-skipped` — only valid when user explicitly wrote "skip interview" (bypass mode)

```yaml
---
style-base: creative-studio                # internal — never announced to user
style-secondary: editorial-portfolio       # only present if hybrid mix used
style-tuning:
  user-confirmed: true                     # MUST be true for Phase 4.0 to pass
  interview-mode: full                     # full | partial-followup | user-skipped
  axes:
    color-mode:
      value: both
      source: user-chosen
    fonts:
      value: mix
      source: user-chosen
    layout:
      value: loose
      source: user-chosen
    content-width:
      value: wide
      source: user-chosen
    corners:
      value: soft
      source: user-chosen
    motion:
      value: high
      source: user-chosen
    color-loudness:
      value: balanced
      source: user-chosen
    imagery:
      value: abstract
      source: user-chosen
    page-load:
      value: branded-intro                 # none | subtle | functional | branded-intro
      source: user-chosen
      pattern: curtain-wipe                # internal pick by skill from loader-patterns.md
    dimension:
      value: none                          # none | shader-accents | 3d-scene
      source: user-chosen                  # axis 10 always asked, always has explicit answer
      library: three.js                    # three.js | r3f | webgl-vanilla — only present if value > none
      geometry: 1                          # 1-6 from webgl-3d-geometries.md — only present if value > none
      forced-override: false               # true if library or trauma-informed mode forced the value
    # axis 11 (tone) only present if asked (trauma-informed mode or auto-generated copy)
provenance:
  fidelity: adapted
  trauma-informed-mode: false
  interview-conducted-at: 2026-04-25T16:42:00
  library-derivation:
    method: 10-axis match scoring against per-library defaults
    scores:
      creative-studio: 7
      editorial-portfolio: 4
      technical-refined: 3
      others: <3
    decision: creative-studio is base (≥6/9 threshold met); overrides applied for color-mode (both) and imagery (abstract)
    user-shown-library: false              # always false; library names are internal craft
  tuning-conflicts: []                     # populated only if motion/page-load mismatch detected
divergences-from-library:
  - 2 axes overridden from creative-studio defaults: color-mode (light → both), imagery (photographic → abstract)
---
```

When a tier-coupling conflict exists (e.g., `motion: low` + `page-load: branded-intro`), `tuning-conflicts` is populated:

```yaml
  tuning-conflicts:
    - axes: [motion, page-load]
      values: [low, branded-intro]
      severity: soft-warn
      message: "motion: low + branded intro loader is unusual; page enters loud then sits silent"
      acknowledged: false                  # flips to true after user responds to delivery warning
      resolution: build-as-specified       # build-as-specified | demoted-to-subtle | locked-by-user
```

This block becomes the **source of truth** for Phase 3 (BUILD) and Phase 4 (REVIEW).
- Phase 4.0 (provenance audit) reads `user-confirmed` and the `source` field of every axis.
- Phase 4.5 (divergence audit) reads `divergences-from-library` and validates the build expressed every shift.

If `user-confirmed: false` or the `axes` block is missing or any axis has no `source` field, **Phase 4.0 fails the build**.

---

## Anti-patterns

- ❌ **Asking the user "which library?"** — library names are jargon. Even designers don't always know what `Spritify` means. The skill maps internally.
- ❌ **Announcing the chosen library for confirmation** — same problem. The user can't validate a name they don't know. They validate the *output*, not the *label*.
- ❌ **Forcing 12 prompts on the user.** The skill is capped at 10 questions (11 if trauma-informed); the user can `you decide` any of them.
- ❌ **Hiding the tuning step.** It's BLOCKING. The opt-out is the user's; the offer is mandatory.
- ❌ **Letting unrecognised axes silently fail.** Ask once for clarification, then move on with what you understood.
- ❌ **Mixing tuning with overrides in the prompt.** Tuning = character axes. Overrides (colors/fonts/URL/image) = literal tokens. They are processed in different files (`user-overrides.md` vs this file).
- ❌ **Treating tuning as cosmetic.** A tuning shift is a design decision — document it in provenance, validate in Phase 4.5.
- ❌ **Inventing a loader without asking.** Page-load is Axis 9 — never silently ship a curtain wipe or skeleton. If the axis wasn't answered, follow the missing-axis follow-up rule.
- ❌ **Auto-demoting a tuning conflict.** `motion: low` + `branded-intro` is allowed under the soft warn-and-build rule. Build it, surface the warning, log the conflict in provenance — do not change the user's choice silently.

---

## Quick reference

| Situation | Action |
|---|---|
| User wrote "make me a kindergarten site for tech-genius kids" | Ask the 10 questions. User answers. Skill maps internally — likely Creative Studio + Editorial Portfolio mix. Build. |
| User wrote "agency landing page, energetic" | Ask the 10 questions. Likely Creative Studio base. Build. |
| User wrote "calming legal aid resource for survivors" | Phase 1.0.5 already loaded trauma-informed.md. Ask 9 + axis 10 (tone). Likely Sanctuary Tech base (page-load: none); force tone=empowering if user picks playful/clinical. |
| User wrote "everything custom, freestyle" | Ask the 10 questions. If no library matches ≥7/10, fall back to Custom mode — build DESIGN.md directly from the 10 answers. |
| User wrote "skip interview, just build" | Log `interview-mode: user-skipped`. Pick a starting library from the brief alone. Document the bypass. |
