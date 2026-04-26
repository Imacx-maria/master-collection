---
name: design-skill-lab
description: |
  Unified design workflow with 15 distinct visual styles plus an opt-in WebGL / Three.js layer. Always use when the user asks to build, design, or style any web page, landing page, component, dashboard, e-commerce, portfolio, blog, or app — even if no style is specified. Triggers on style names: brutalist, editorial, technical-refined, luxury, bento, playful, warm, sanctuary, spritify, memoir, basalt, warm-editorial, atmospheric-protocol, protocol, atmospheric, adaptive-ai-console, ai-console, linear-like, motion-directed, spatial-portfolio, hushed, hushed-premium-saas, whisper, ElevenLabs-like, or descriptors like "AI product", "literary tech", "SaaS site", "dev tool", "hotel site", "kids site", "agency site", "calming UI", "blog design", "Stripe-like", "Neuform-like", "Linear-like", "ElevenLabs-like", "voice AI", "premium consumer tech", "Apple-adjacent", "cognitive tools", "manifesto product", "protocol infrastructure", "creative technologist portfolio", "Webflow specialist showcase". Also triggers on 3D / WebGL / Three.js / shader / particle / configurator / "AI-product hero" briefs — covered by the conditional `dimension` axis (none / shader-accents / 3d-scene).

  Runs a mandatory 4-phase workflow: ANALYSE (extract inspiration qualities without copying), TRANSLATE (derive a project-specific DESIGN.md that diverges from the library default in at least 2 tokens), BUILD (implement), REVIEW (style-aware critique + universal checks). Never skip phases. Never copy reference images or templates verbatim. Replaces 15 individual design skills.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Design System Picker

A unified design workflow with 15 style libraries. The workflow always runs in 4 phases — `ANALYSE → TRANSLATE → BUILD → REVIEW`. Each style library contains tokens (YAML `DESIGN.md`), craft guide (prose reference), and style-specific review checks.

## The Non-Negotiable Rules

These exist because the failure mode is "every output looks the same":

1. **Never copy reference images literally.** Extract system qualities (grid, contrast, rhythm, type pairing, composition, motion) — not pixels.
2. **Never copy the style library DESIGN.md verbatim.** It is a starting point. The project-specific DESIGN.md (produced in Phase 2) **must diverge in at least 2 tokens** from the library default (accent color, type pairing, spacing density, shape system, or radius scale).
3. **Never skip Phase 4 (review).** The review pass is obligatory before delivery, not optional polish.
4. **Anti-pattern — preset literalness:** if the final output shares >80% of tokens with the library's default DESIGN.md, it's template copy, not design. Diverge or switch libraries.

## The 4-Phase Workflow

### Phase 1 — ANALYSE

Goal: understand the real job before choosing a style.

**Step 1.0 — Override detection (run first).** Scan the user's prompt and any attachments for override triggers:
- Explicit colors (hex codes, named brand colors, color descriptions, palette images)
- Explicit fonts (font family names, font files, brand guideline references)
- Image / screenshot references (uploaded images, mood boards, Pinterest)
- URL / website references (live sites, "like X" comparisons)

If any trigger fires, **load `references/user-overrides.md`** and follow the matching protocol. Overrides change how Phase 2's divergence rule applies — read the file before proceeding. The protocol covers detection, fidelity scale (Inspired / Adapted / Faithful), and how user-provided constraints count as divergences.

If no triggers fire, proceed to Step 1.1 with the standard workflow.

**Step 1.1 — If the user provided an inspiration image, URL, or visual reference:** load `references/inspiration-analysis.md` and produce a 5–8 line briefing that extracts:
- 2–3 dominant color tokens (hex approximations)
- typography category (geometric sans, editorial serif, grotesk, mono-first, etc.)
- spacing density (tight, medium, generous)
- compositional logic (grid, asymmetry, poster, reading-column)
- mood keywords (3–5 words)

Never describe the image as "the target" — describe it as "the direction".

**Step 1.2 — If the user gave a text brief only:** extract intent:
- audience and emotional state
- primary user action
- business context (landing page, dashboard, portfolio, etc.)
- any stated constraints (brand colors, existing fonts)

**Step 1.3 — If the brief is too vague to proceed,** ask one tight question framed around output type, not aesthetics jargon:
- *"Should this feel bold, warm, technical, editorial, or calming?"*
- *"Is this a product surface, a gallery, a poster, or a publication?"*

Never open a full style interview. One question, then move on.

**Step 1.4 — If overrides were detected,** ask the fidelity question (per `user-overrides.md`) when an image or URL was provided. Skip this question if the user has already specified fidelity in their prompt, or if intent is unambiguous (e.g., they only provided color hex codes — fidelity doesn't apply). Default to **Inspired** if not asked.

**Step 1.5 — Liquid Glass detection (conditional).** Scan two sources for the trigger lexicon: (a) the user's prompt text, and (b) the inspiration briefing produced by Step 1.1 (when an image or URL was provided). Trigger lexicon: "glass", "liquid glass", "Apple-style", "frosted", "translucent nav", "iOS 26", or similar visual-surface language implying translucent chrome. Image-led briefs frequently imply Liquid Glass without naming it — the inspiration briefing's mood keywords are the second signal. If either source hits, set `effects.liquid-glass = true` in style-tuning. Surface this back to the user explicitly: "Liquid Glass detected — applying as modifier. Compatibility-checked in Phase 2."

This step exists because Liquid Glass is a modifier, not a style — it cannot be detected by style-library auto-detection rules. The modifier flag must be set before Phase 2 so the compatibility matrix runs before a library is committed to. Missing this detection means a glass brief arrives at Phase 3 without the compatibility check, and incompatible style+glass combinations ship silently — and image-led briefs frequently imply glass without naming it explicitly, so the lexicon scan must run on both prompt text and Step 1.1's briefing output.

### Phase 2 — TRANSLATE

Goal: pick a style library and derive a project-specific `DESIGN.md`.

**Step 2.1 — Select the style library.** Use the style menu below. Auto-detect when context is clear; present the menu otherwise. If overrides were detected in Phase 1, use the URL/image reference to inform library choice (per `inspiration-analysis.md` mapping).

**Step 2.2 — Load the library.** Read two files:
- `references/styles/<style>.md` (craft guide, 200–900 lines of prose — implementation details)
- `references/styles/<style>.design.md` (tokens + rationale — the contract)

**Step 2.3 — Derive a project-specific DESIGN.md.** Produce a fresh DESIGN.md for this project that inherits the library's spirit but diverges in at least 2 tokens.

**Without overrides:** pick any 2+ from this list:
- shift the accent color
- swap one half of the type pairing
- tighten or loosen the spacing scale
- change the radius system (sharp ↔ soft)
- introduce a secondary influence from another library (dominant + one secondary max)

**With overrides (from `references/user-overrides.md`):**
- User-provided colors count as **one** divergence (color axis) — apply verbatim
- User-provided fonts count as **one** divergence (typography axis) — apply verbatim
- The second divergence must be **orthogonal** (not in the same axis as the override). E.g., if user provided colors, the second divergence must be in typography, spacing, radius, or composition — not another color shift.
- Fidelity = **Adapted** counts as 1 divergence (composition diverges from reference)
- Fidelity = **Faithful** waives the rule entirely — document the waiver in the provenance section

State the divergences explicitly at the top of the DESIGN.md in the Provenance section (per `user-overrides.md` template) or as a "Divergences from library: ..." line if no overrides apply.

**Step 2.4 — Combination rule.** If combining two libraries, pick one dominant and one secondary. Never more. Avoid `neo-brutalist` + `warm-serene-luxury` unless the brief explicitly asks for that tension.

**Step 2.5 — Override compatibility check.** If user-provided fonts/colors are incompatible with the chosen library's identity (e.g., humanist sans inside Brutalist, warm pastels inside Sanctuary Tech), flag this and either: (a) escalate to user with a switch-library proposal, or (b) accept the override and document the trade-off in provenance. Don't force-fit silently.

**Step 2.6 — Modifier compatibility check (conditional).** If `effects.liquid-glass === true`, load `references/effects/liquid-glass.md` § Compatibility matrix and run the host style against it.

- **Native tier** (Atmospheric Protocol, Adaptive AI Console, Creative Studio): proceed. Glass is a natural fit — load the modifier in Phase 3.
- **Conditional tier** (Technical Refined, Warm Serene Luxury, Editorial Portfolio, Motion-Directed Spatial Portfolio, Hushed Premium SaaS): load the per-style constraint from the matrix (element scope, max count). Surface the constraint to the user before Phase 3.
- **Refused tier — non-Sanctuary** (Neo-Brutalist, Memoir, Basalt, Spritify, Playful Bento, Warm Editorial): surface the single-element-or-style-switch choice: "This style system doesn't host glass natively. Options: (a) limit glass to a single isolated chrome element, or (b) switch to [nearest native style]."
- **Sanctuary Tech — hard refuse**: respond: "Liquid Glass is not available for Sanctuary Tech. The trauma-informed design contract prohibits visual complexity that increases cognitive load." No override path.

This step exists to prevent glass being applied to incompatible styles without acknowledgement. The compatibility matrix encodes real structural reasons (dark-mode-only glass over a light-mode editorial style, glass over reading columns that fail contrast, glass surface count in trauma-informed contexts). Skipping this check means the review in Phase 4 finds the violations after the build — which is expensive to fix.

### Phase 3 — BUILD

Goal: implement using the project DESIGN.md as the source of truth.

**Step 3.0.04 — Load motion principles (conditional).** If `style-tuning.axes.motion.value` is `medium` or `high`, load `references/motion-principles.md` BEFORE `motion-tactics.md`. Skip if `low` (the universal hover-transition rule in `base-principles.md` is enough).

The file defines the **design lens** for motion: vocabulary (animation vs micro-interaction vs functional motion), Saffer's Four Pillars per micro-interaction (Trigger / Rules / Feedback / Loops & Modes), the canonical duration table (button feedback 80–100ms → success celebration 600–1000ms), the 100ms perception threshold + 20% Weber-Fechner rule, easing intent (ease-out for entering, ease-in for leaving permanent, ease-in-out for in-bounds), spring physics vs fixed timing, the GPU-only rule (transform + opacity), the C.U.R.E. audit framework (Context / Usefulness / Restraint / Emotion), WCAG criteria 2.2.2 (5-second pause) and 2.3.1 (3-flash rule), and a pattern catalog (shake-for-error, pull-to-refresh, FLIP, parallax depth, etc.).

This step exists because `motion-tactics.md` alone is mechanical — "load GSAP, animate things". Without principles first, the skill ships motion that compiles but isn't designed. Read principles → classify the moments → then apply tactics.

**Step 3.0.05 — Load motion tactics (conditional).** If `style-tuning.axes.motion.value` is `medium` or `high`, load `references/motion-tactics.md`. Skip if `low` (CSS transitions are sufficient — no orchestration contract needed).

The file defines the **technical contract** per tier: `medium` = CSS animations + IntersectionObserver only, no JS animation library; `high` = GSAP 3.12+ orchestration with ScrollTrigger / SplitText / Flip / parallax / FLIP / CustomEase + Webflow's Club GSAP plugin set (DrawSVG, MorphSVG, ScrambleText, Inertia, Physics2D, MotionPathHelper, ScrollSmoother). The pre-build checklist at the bottom is the contract — including the `prefers-reduced-motion` fallback (non-negotiable at every tier above `low`).

This step exists because `motion: high` was being interpreted as "more CSS animations" — which is `medium` dressed up. Real `high` requires a different mental model and a JS animation runtime; the file makes that contract explicit before markup is generated.

**Step 3.0.06 — Load loader patterns (conditional).** If `style-tuning.axes.page-load.value` is anything other than `none`, load `references/loader-patterns.md`. Skip if `none` (no loader markup, no JS, no failure surface — the browser paints natively).

The file is the technical contract for page loaders — a separate concern from in-page motion. It covers: the 4 primitives every loader reduces to (rotation / translation / opacity-scale / content-mimic); the per-role pattern map (subtle → fade-in or shimmer; functional → skeleton / spinner / progress bar; branded-intro → curtain / DrawSVG / SplitText / mask reveal); 9 full recipes with GSAP code; the four mandatory failure-mode patterns (max-timeout safeguard, LCP-safe overlay, `.js-ready` gate, reduced-motion skip); per-library default recipes; and Webflow injection notes.

This step exists because `page-load` was being silently invented when `motion` was `high` — usually a generic spinner with no failure-mode coverage. The two highest-severity loader bugs ("loader never resolves" and "page hidden behind loader breaks LCP") are the contract this file enforces. Without it, any loader the skill ships is one CDN failure away from being broken.

**Tier-coupling note:** `motion: low` + `page-load: functional` or `branded-intro` is allowed but flagged. Build as specified, surface a one-line warning in delivery summary, log in `provenance.tuning-conflicts`. See `style-tuning.md` § Tier-coupling rule for the contract. The only auto-demote is when trauma-informed mode is active + Sanctuary Tech library — page-load is forced to `none` or `subtle` regardless of user pick (rationale in `loader-patterns.md`).

**Step 3.0.07 — Surface-context check (conditional).** Before generating any markup that places **a card / testimonial / quote / panel / callout inside a section with the OPPOSITE surface mode** (light card in dark section, or dark card in light section), OR uses **JS-driven reveal animations** (`.reveal { opacity: 0 }`, scroll-triggered fades), OR derives a **non-default theme** (light variant of a dark-only style, dark variant of a light-only style) OR introduces a **theme-toggle**, load `references/build-tactics.md` § Tactic 17 — and additionally § Tactic 18 when the build crosses theme boundaries (the inversion failures Tactic 18 catches are not covered by Tactic 17).

Tactic 17 is the contract that catches two recurring user-visible defect classes (mixed-surface text inheritance and JS-gated reveal failures):

- **17.3 Per-surface colour tokens** — components that can sit on multiple surface contexts must declare their `background` AND `color` as a unit, never inherit from parent context. Token names are surface-scoped (`--text-on-surface-light`), not hierarchy-scoped (`--text-default`).
- **17.4 Progressive-enhancement gate for reveals** — `.reveal { opacity: 0 }` must be gated by `.js-ready` class added by JS as the FIRST line of the IIFE. Without this, JS failure leaves content permanently invisible.
- **17.6 Audit test (mental flip)** — before delivery, mentally flip every surface in the build. Any text that becomes invisible was inherited instead of scoped. Refactor.

The 17.7 checklist is the contract; failures here are the highest-severity bug class the skill can ship — visible content that should be visible, but isn't.

This step pairs with `base-principles.md` Q17 (audit lens — "is the colour scoped?"). Tactic 17 is the build lens — "scope it now, before markup."

**Step 3.0.08 — Load gradient tactics (conditional).** If the chosen style is **Atmospheric Protocol** (gradient atmosphere is the load-bearing visual element), OR the brief calls for any non-trivial gradient backdrop (atmospheric mesh, glow blooms, smoky linear flow, animated colour fields, WebGL shader gradients, glass border shells, or grain overlays), load `references/gradient-tactics.md`. Skip if gradients are decorative-only (a single subtle button hover, a 2-stop linear inside a card).

The file is the **technique playbook** for gradients. Without it, "gradient" gets interpreted as `linear-gradient(45deg, red, blue)` and ships flat. It covers six recipes (layered radial mesh, smoky linear flow, SVG `feTurbulence` grain, WebGL shader, particle dot-matrix field, gradient border shell), a runtime-vs-feel decision tree, performance comparison table, light-mode vs dark-mode discipline, and an audit checklist. Atmospheric Protocol's three named atmosphere variants (Bloom / Flow / Particle) each map to specific recipes in this file — load it whenever that style is picked.

**Step 3.0.09 — Load WebGL / 3D principles + tactics + geometries (conditional).** If `style-tuning.axes.dimension.value` is `shader-accents` or `3d-scene`, load `references/webgl-3d-principles.md` FIRST, then `references/webgl-3d-tactics.md`, then `references/webgl-3d-geometries.md` (geometry catalog — pick a primitive deliberately rather than defaulting to "blob"). Skip entirely if `none` (the default for ~90% of projects — no WebGL code, no Three.js bundle, no failure-mode surface).

`webgl-3d-principles.md` defines the **design lens** for 3D: when 3D earns its place vs the 3D-for-3D's-sake anti-pattern, the Three.js / Unity / Pixel Streaming pick rationale (research-backed: Three.js wins for marketing, e-commerce, dashboards on bundle and SEO grounds), per-tier perf budget (`shader-accents` ≤ 200 KB compressed, `3d-scene` ≤ 2 MB), the four mandatory failure-mode guards (WebGL feature detect, `prefers-reduced-motion`, DOM mirror for SEO/a11y, 8s load timeout), the C.U.R.E. test for 3D moments (Context / Usefulness / Restraint / Emotion), and the sustainability obligations (offscreen pause, tab-hidden pause, idle FPS cap).

`webgl-3d-tactics.md` defines the **technical contract** per tier: `shader-accents` = vanilla WebGL2 fragment shader on a fullscreen plane OR Three.js `ShaderMaterial` on `PlaneGeometry`, no model loaders / no camera / no lights; `3d-scene` = Three.js r170+ with `GLTFLoader` + Draco + KTX2, GSAP `ScrollTrigger` or `@react-three/scroll-rig` for camera, `MeshStandardMaterial`, optional ONE merged post-processing pass (never a stack), GLB-only assets (no FBX/OBJ), mobile LOD, DPR cap at 2. The pre-build checklist at the bottom is the contract — including all four failure-mode guards and the WebXR / multiplayer / physics out-of-scope refusal.

`webgl-3d-style-fit.md` is the **per-library compatibility matrix** — which of the 14 libraries host 3D well (Creative Studio, Playful Bento, Warm Editorial natively shader-accents; Basalt for product configurators; Technical Refined for data viz; Adaptive AI Console for shader-accent floating layers; Motion-Directed Spatial Portfolio natively for 3d-scene spatial heroes), which soft-refuse (Memoir, Spritify), and which hard-refuse (Sanctuary Tech in trauma-informed mode forces `dimension: none` regardless of user pick).

`webgl-3d-geometries.md` is the **geometry catalog** — 6 primitives (distorted blob, geometric solid, particle field, ribbon/wave, glass refraction surface, spatial type) with per-primitive perf budget and per-library fit notes. Loaded after tactics so the build agent picks a geometry deliberately rather than defaulting to "always blob".

**Tier-coupling rule:** `dimension: 3d-scene` requires `motion: medium` minimum. A static 3D scene reads as broken, not as deliberate. If user picked `motion: low` + `dimension: 3d-scene`, surface a tier-coupling warning in delivery, build as specified, log in `provenance.tuning-conflicts`. The only auto-demote is when trauma-informed mode is active OR the library is Sanctuary Tech — `dimension` is forced to `none` regardless of user pick (rationale: cognitive load, GPU thermal throttling on older devices used by vulnerable users).

This step exists because the research is unambiguous on the failure mode: AI-coded 3D ships broken when there's no contract. Bundle balloons past the 10-second LCP cliff; mobile FOV clips; `prefers-reduced-motion` is ignored; the DOM has no fallback for users without WebGL; idle 3D drains battery off-screen. The principles classify the moment; the tactics specify the code; the style-fit matrix prevents 3D being layered onto registers it would defeat. Without this trio, "add WebGL" produces a demo, not a design.

**Step 3.0.10 — Load Liquid Glass modifier (conditional).** If `effects.liquid-glass === true`, load `references/effects/liquid-glass.md`. The file defines the CSS track (default) and the WebGL/SDF refraction track (gated).

- **CSS track (always):** mandatory CSS pattern (translucent bg + `-webkit-backdrop-filter` + `backdrop-filter` + hairline border + shadow anchor), `prefers-reduced-transparency` fallback, `prefers-reduced-motion` fallback, optional gradient border shell (cross-reference `references/gradient-tactics.md` § Recipe 6).
- **WebGL refraction track (gated):** only if `style-tuning.axes.dimension.value === 'shader-accents'` AND user opted in. The four mandatory failure-mode guards from `references/webgl-3d-tactics.md` apply identically — do not re-implement, cross-reference.

This step exists because the modifier has two distinct implementation paths with different complexity and failure surfaces. Loading the modifier file after the style craft guide (but before BUILD) ensures the build agent has the complete token vocabulary and fallback contract before markup is generated.

**Step 3.0 — Load layout patterns.** Before generating markup for any section with multiple items, load `references/layout-patterns.md`. Decide explicitly per section: bento, uniform grid, list, or hero+supporting. Don't default to `auto-fit minmax(...)` — this produces orphan rows and visual misalignment.

For each multi-item section, document the decision in your build:
- `<!-- Layout: uniform grid 4×2 (8 team members, equal weight) -->`
- `<!-- Layout: bento — hero 6×2 + wide 6×1 + 3×1 + tall 3×2 + wide 6×1 + full 12×1 (6 features, hierarchy required) -->`

This forces deliberate choice.

**Step 3.1 — Build with the chosen patterns.**
- The library's craft guide provides component patterns, motion vocabulary, anti-patterns, and asset locations — consult it as reference.
- The project DESIGN.md provides the tokens — CSS custom properties, type definitions, spacing scale.
- When a template exists in the library's `assets/`, use it as structural scaffolding, but apply the project DESIGN.md tokens — never the library defaults.

**Step 3.2 — Alignment consistency pass.**
Before marking BUILD done, scan the output for:
- Section headers that are centred → grids below should be centred too (or both left-aligned)
- All sections use the same `max-width` container
- Inside bento: spans add up correctly (Σ cols×rows == 12 × max_row)

Follow the universal base principles in `references/base-principles.md` regardless of style.

### Phase 4 — REVIEW

Goal: catch regressions to library defaults, missed divergences, structural issues.

**Step 4.1 — Spec lint (programmatic gate).** Run the official `DESIGN.md` linter against the project's `DESIGN.md` file before any other review step. This catches schema violations, broken token references, invalid color/dimension values, and missing required sections.

```bash
npx @google/design.md lint <path-to-DESIGN.md>
```

The linter returns structured JSON. Treat any `error` as a hard blocker — fix and re-run before proceeding. `warning` should be addressed unless there's a documented reason to keep it (note the reason in the delivery summary).

If `npx` or the linter is unavailable in the environment, document that lint was skipped and proceed — but flag this clearly in delivery so a human can re-validate later.

**Step 4.2 — Style-specific review.** Load `references/style-reviews/<style>.md` and run the checklist. Each style has its own failure modes (e.g., technical-refined: "is the accent focused or flooding the UI?").

**Step 4.3 — Universal review.** Invoke the `design-reviewer` skill as a subroutine. Run the abbreviated checklist (first impression, hierarchy, typography, color, grid, accessibility). Fix anything labeled Critical before claiming completion.

**Step 4.4 — Layout integrity audit.** Run the layout-specific checks from `references/base-principles.md` § Layout Integrity (questions 11–16). Specifically verify:
- Each section's grid alignment matches its header alignment (both centred or both left-aligned)
- No orphan rows in any uniform grid (`items_count % columns == 0` at every breakpoint)
- If bento was used: at least 2 distinct span sizes, total span coverage adds up correctly, hero card holds the most important content
- Sequential content (timelines, schedules) uses uniform grid or list — never bento
- All sections share the same `max-width` container
- **Lists use the right width for their content shape.** Horizontal row lists (schedules, line items, comparison rows) span the full container — not a narrow reading-width column. Reading lists (prose, FAQs, articles) use ~720px. See `layout-patterns.md` Pattern C1 vs C2.

If any check fails, refactor before delivery — these are visible bugs, not style preferences.

**Step 4.5 — Divergence audit.** Verify the project DESIGN.md actually diverges from the library default in at least 2 tokens. If it doesn't, refactor before delivery.

**Step 4.5b — Effects review (conditional).** If `effects.liquid-glass === true`, load `references/style-reviews/effects/liquid-glass.md` and run the 14-check checklist. Run this in addition to the host style's review checks — it's a modifier overlay, not a replacement.

Treat any **Critical** severity failure as a delivery blocker — fix before proceeding to Step 4.6. Treat **Major** as a required fix unless there's a documented reason to accept it in provenance. **Minor** findings are advisory.

This step exists because the modifier introduces failure modes not covered by the host style's review (backdrop-filter animation, missing reduced-transparency fallback, WebGL guard completeness). A build that passes the style review but skips the modifier review can ship glass that animates backdrop-filter every frame, lacks a11y fallbacks, or has an undeclared override on a refused style.

**Step 4.6 — Deliver.** State explicitly:
- style library chosen
- divergences applied
- project DESIGN.md (front matter tokens)
- layout patterns used per section (bento / uniform N-col / list / hero+supporting)
- lint result (PASS / WARN with notes / SKIPPED with reason)
- review findings addressed

## Style Menu

Present this when context isn't clear enough to auto-detect. If context makes the choice obvious, skip the menu and state which style you're using.

| # | Style | Best For | Signature Look |
|---|-------|----------|----------------|
| 1 | **Neo-Brutalist** | Bold landing pages, edgy brands, tech showcases | Anton + Roboto Mono, sharp corners, grid backgrounds, grayscale images |
| 2 | **Editorial Portfolio** | Photography/art portfolios, creative professionals | Compressed uppercase Inter, hover-reveal panels, off-white #f4f3f0 |
| 3 | **Technical Refined** | Developer tools, SaaS dashboards, technical products | Geist Sans/Mono, teal #2DD4CD accents, dashed borders |
| 4 | **Basalt E-Commerce** | Luxury beauty, skincare, fashion, lifestyle shops | EB Garamond + Inter, grayscale products, split-layout pages |
| 5 | **Memoir Blog** | Writer portfolios, newsletters, content platforms | Manrope + Source Serif italic, creamy #F4F2F0, blog card grids |
| 6 | **Creative Studio** | Agency sites, design studios, brand showcases | Dark charcoal #2d2f2e + coral #ff531f, full-color imagery, rounded cards |
| 7 | **Warm Serene Luxury** | Boutique hotels, wellness/spa, interior design | DM Serif Display + Onest, #FAFAFA, numbered items (01), imagery-driven warmth |
| 8 | **Playful Bento** | Marketing sites, creative tools, energetic brands | Bold bento grids, hierarchy-aware cards, vibrant colors |
| 9 | **Spritify** | Kids products, family brands, fun apps | League Spartan, switchable color schemes, playful components |
| 10 | **Sanctuary Tech** | Crisis support, healthcare, legal aid, privacy tools | Monospace type, dashed borders, muted tones, generous whitespace |
| 11 | **Warm Editorial** | AI products, technical writing, thoughtful tools | Anthropic Serif weight 500, parchment #F5F4ED, terracotta #C96442, ring shadows, light/dark chapter alternation |
| 12 | **Atmospheric Protocol** | Cognitive tools, protocol infrastructure, manifesto products, Stripe/Neuform/Nexus-class landings | Instrument Serif 400 with italic continuation, Inter UI, JetBrains Mono data, dark `#030508` canvas, glass cards with hairline gradient border shells, three atmosphere variants (Bloom indigo / Flow violet / Particle WebGL) |
| 13 | **Adaptive AI Console** | AI/product consoles, Linear-class operational tools, agent dashboards, AI-native productivity surfaces | Inter Variable + Berkeley Mono, near-black `#0d0e10` surfaces, indigo-violet `#7170ff` accent, dense operational rows, command palette, AI composer, accountable generated-action surfaces (dark-mode-native) |
| 14 | **Motion-Directed Spatial Portfolio** | Creative-technologist portfolios, Webflow specialist showcases, spatial product studios, premium digital portfolios | Inter Tight oversized thin display + Cormorant Garamond italic accent, JetBrains Mono metadata, near-black cinematic stage, grayscale media, scroll-keyframe page architecture, one project-specific shock accent (dark-mode-native) |
| 15 | **Hushed Premium SaaS** | Voice / audio AI (ElevenLabs-class), premium consumer tech, refined SaaS launches, Apple-adjacent product categories | Manrope/Waldenburg weight 200–300 whisper-thin display, Inter body with positive letter-spacing (+0.14–0.18px), achromatic palette with warm-stone surface (`#F5F2EF`), multi-layer shadow stacks at sub-0.1 opacity, asymmetric warm-stone CTA (30px radius, `12px 20px 12px 14px`, warm-tinted shadow `rgba(78,50,23,0.04)`) |
| 16 | **Custom / Freestyle** | When none of the above fit | Uses base principles below, derive a fresh DESIGN.md bottom-up |

## Auto-Detection Rules

Skip the menu when context is clear. These map brief cues to a **starting** library — Phase 2 still has to derive a diverged project DESIGN.md.

- **AI product / AI assistant / agent / co-pilot / literary-tech / "warm but technical"** → Style 11 (Warm Editorial) for editorial/marketing surfaces; **Style 13 (Adaptive AI Console)** for the actual product console / dashboard / agent UI (Linear-class operational surface — distinguishes the marketing page from the product-inside-the-page).
- **Linear-like / agent dashboard / AI-product console / command palette UI / dense operational rows / "Linear meets Cursor" / AI composer surface** → Style 13 (Adaptive AI Console). Dark-mode-native; if the brief asks for light mode, reach for Style 3 (Technical Refined) instead.
- **Creative-technologist portfolio / Webflow specialist showcase / spatial product studio / scroll-keyframed case study / "cinematic dark portfolio" / "Apple-like product reveal" / motion-directed reveal** → Style 14 (Motion-Directed Spatial Portfolio). When picked, expect `motion: high` and consider `dimension: shader-accents` for the spatial hero. Editorial Portfolio (Style 2) is the lighter, image-first alternative when motion budget is `low` or `medium`.
- **Cognitive tool / protocol infrastructure / manifesto product / "Stripe-like" / "Neuform" / "Nexus" / treasury orchestration / "editorial dark" / serif-with-data-chrome** → Style 12 (Atmospheric Protocol). When picked, also load `references/gradient-tactics.md` (the atmosphere is load-bearing).
- **SaaS / dev tool / dashboard / technical product (cool/clinical leaning)** → Style 3 (Technical Refined). Jocril projects (detected by path or mention) also map here.
- **Voice AI / audio AI / "ElevenLabs-like" / premium consumer tech / Apple-adjacent SaaS / refined SaaS launch / "whisper-quiet premium" / "lightness as authority" / boutique creator tools** → Style 15 (Hushed Premium SaaS). Light-mode-native; the defining choice is whisper-weight display (200–300). When the brief asks for premium SaaS that is neither hospitality (Style 7) nor energetic (Style 9), this is the lane. If the brief leans technical/dev-tool, prefer Style 3 (Technical Refined) instead.
- **E-commerce / product pages** → Style 4 (Basalt) — but check if the brand calls for Style 6 (Creative Studio) or Style 8 (Playful Bento) first
- **Blog / newsletter / writing** → Style 5 (Memoir)
- **Portfolio / showcase of work** → Style 2 (Editorial)
- **Crisis / vulnerable users / healthcare / legal aid** → Style 10 (Sanctuary). If trauma-informed, load `references/trauma-informed.md` from the design-reviewer skill.
- **Kids / family** → Style 9 (Spritify); energetic adult brand → Style 8 (Playful Bento)
- **Hotel / spa / wellness / interior design** → Style 7 (Warm Serene)
- **Agency / studio / creative services** → Style 6 (Creative Studio)
- **Brutalist / edgy / high-contrast / poster-like** → Style 1 (Neo-Brutalist)
- User says "fun" or "energetic" without kid context → Style 8 (Playful Bento)
- **3D / WebGL / Three.js / shader / particle field / configurator / "AI-product hero"** → keep the library auto-detected by other cues (most likely Creative Studio, Warm Editorial, or Technical Refined for data viz). The dimension axis (axis 10) is always asked, so the user explicitly chooses `none` / `shader-accents` / `3d-scene` — but if their brief language strongly implies a tier, surface that recommendation alongside the question. Never auto-pick `3d-scene` without explicit user confirmation — it's a 2 MB bundle commitment.

If still ambiguous after these rules, ask one question (see Phase 1).

## File Map

```
design-skill-lab/
├── SKILL.md                              # this file — workflow orchestrator
├── references/
│   ├── base-principles.md                # universal rules (typography, a11y, spacing)
│   ├── build-tactics.md                  # tactical do/don't recipes for build moment (18 tactics: 1-13 always-on; 14 dark-mode, 15 mobile-nav, 16 component-reusability, 17 surface-context, 18 interactive-state coverage in derived themes — all conditional)
│   ├── inspiration-analysis.md           # how to extract from an image without copying
│   ├── user-overrides.md                 # detection + protocol for user colors/fonts/URL/image, fidelity scale
│   ├── style-tuning.md                   # 9-question interview + per-library defaults table (Phase 2.1)
│   ├── layout-patterns.md                # bento vs uniform vs list, alignment rules, span vocabulary
│   ├── motion-principles.md              # design lens for motion: taxonomy, 4 pillars, canonical duration table, easing intent, C.U.R.E. audit, WCAG 2.2.2/2.3.1, pattern catalog (Phase 3 Step 3.0.04)
│   ├── motion-tactics.md                 # technical contract per motion tier (medium=CSS+IO, high=GSAP+ScrollTrigger+SplitText+Flip) (Phase 3 Step 3.0.05)
│   ├── loader-patterns.md                # page-loader contract per page-load value (subtle / functional / branded-intro); 9 recipes; 4 mandatory failure-mode guards (Phase 3 Step 3.0.06)
│   ├── gradient-tactics.md               # gradient technique playbook: 6 recipes (layered radial mesh, smoky linear flow, SVG feTurbulence grain, WebGL shader, particle dot-matrix, gradient border shell), runtime-vs-feel decision tree, performance comparison, light/dark discipline (Phase 3 Step 3.0.08, conditional)
│   ├── webgl-3d-principles.md            # design lens for WebGL/3D: when 3D earns its place, Three.js vs Unity vs Pixel Streaming, perf budget per tier, four mandatory failure-mode guards, C.U.R.E. test for 3D, sustainability (Phase 3 Step 3.0.09, conditional)
│   ├── webgl-3d-tactics.md               # technical contract per dimension tier: shader-accents (vanilla WebGL2 fragment shader OR Three.js ShaderMaterial, ≤200 KB) | 3d-scene (Three.js r170+ + GLTFLoader + Draco + KTX2 + GSAP ScrollTrigger, ≤2 MB); 4 failure-mode guards as code; pre-build checklist; out-of-scope refusal list (Phase 3 Step 3.0.09, conditional)
│   ├── webgl-3d-style-fit.md             # per-library 3D compatibility matrix; soft-refuse (Memoir, Spritify) and hard-refuse (Sanctuary Tech + trauma-informed) rules; library-swap suggestion protocol (Phase 3 Step 3.0.09, conditional)
│   ├── webgl-3d-geometries.md            # geometry catalog — 6 primitives (blob, geometric solid, particle field, ribbon/wave, glass refraction, spatial type) with per-primitive perf + per-library fit; prevents "always blob" default (Phase 3 Step 3.0.09, conditional)
│   ├── typography-safety.md              # tier+modifier model, language adjustments, failure modes
│   ├── sidecar-contract.md               # .design.md → tokens.json + tailwind.config.js transform spec (Phase 4.8.1)
│   ├── scripts/
│   │   └── generate-sidecars.py          # auto-generator for sidecars; deterministic transform from .design.md frontmatter
│   ├── styles/                           # 15 style libraries — each has .md (craft) + .design.md (tokens) + auto-generated .tokens.json + .tailwind.config.js sidecars
│   │   ├── neo-brutalist.md              # craft guide (prose)
│   │   ├── neo-brutalist.design.md       # tokens YAML + rationale
│   │   ├── neo-brutalist.tokens.json     # auto-generated W3C tokens
│   │   ├── neo-brutalist.tailwind.config.js  # auto-generated Tailwind v3 config
│   │   ├── editorial-portfolio.md
│   │   ├── editorial-portfolio.design.md
│   │   ├── technical-refined.md
│   │   ├── technical-refined.design.md
│   │   ├── warm-editorial.md
│   │   ├── warm-editorial.design.md
│   │   ├── atmospheric-protocol.md
│   │   ├── atmospheric-protocol.design.md
│   │   ├── adaptive-ai-console.md        # NEW — Linear-class AI console
│   │   ├── adaptive-ai-console.design.md
│   │   ├── motion-directed-spatial-portfolio.md  # animation-led dark portfolio
│   │   ├── motion-directed-spatial-portfolio.design.md
│   │   ├── hushed-premium-saas.md        # NEW — whisper-weight premium SaaS (ElevenLabs-class)
│   │   ├── hushed-premium-saas.design.md
│   │   └── ... (same pattern for all 15)
│   ├── effects/                          # modifier effects (conditional — Phase 3 Step 3.0.10, Phase 4 Step 4.5b)
│   │   └── liquid-glass.md              # Liquid Glass modifier: CSS + WebGL tracks, 14-style compatibility matrix, override protocol
│   └── style-reviews/                    # per-style review lenses
│       ├── neo-brutalist.md
│       ├── editorial-portfolio.md
│       ├── warm-editorial.md
│       ├── atmospheric-protocol.md
│       ├── hushed-premium-saas.md
│       ├── ... (same pattern for all 15)
│       └── effects/                      # modifier effect review checks
│           └── liquid-glass.md           # 14 checks: a11y, perf, scope, WebGL guards (Phase 4 Step 4.5b)
```

## Quick Reference — When to Load What

| Situation | Load |
|-----------|------|
| User provides colors / fonts / image / URL | `references/user-overrides.md` (run first in Phase 1) |
| User mentions image/inspiration | `references/inspiration-analysis.md` |
| `style-tuning.axes.motion` is `medium` or `high` | `references/motion-principles.md` FIRST (Phase 3 Step 3.0.04 — design lens, vocabulary, duration table, C.U.R.E.), then `references/motion-tactics.md` (Phase 3 Step 3.0.05 — technical contract; medium=CSS-only, high=GSAP) |
| `style-tuning.axes.page-load` is anything other than `none` | `references/loader-patterns.md` (Phase 3 — pattern map + 9 recipes + 4 mandatory failure-mode guards) |
| Chosen style is Atmospheric Protocol, OR build needs a gradient as a load-bearing visual element (atmospheric backdrop, mesh, glow blooms, smoky flow, animated colour fields, WebGL gradient, glass border shell) | `references/gradient-tactics.md` (Phase 3 Step 3.0.08 — 6 recipes + decision tree + perf comparison + audit checklist) |
| `style-tuning.axes.dimension` is `shader-accents` or `3d-scene` (3D / WebGL / Three.js / shader / particle / configurator brief) | `references/webgl-3d-principles.md` FIRST (Phase 3 Step 3.0.09 — design lens, perf budget, 4 mandatory failure-mode guards, C.U.R.E. for 3D), then `references/webgl-3d-tactics.md` (technical contract per tier; Three.js r170+ stack, GLB-only, Draco+KTX2, pre-build checklist), then `references/webgl-3d-style-fit.md` (per-library compatibility matrix; hard-refuse for Sanctuary Tech + trauma-informed), then `references/webgl-3d-geometries.md` (6-primitive catalog — pick blob / geometric solid / particle field / ribbon / glass refraction / spatial type deliberately) |
| Build mixes light/dark surfaces (light card in dark section, etc.) OR uses reveal animations | `references/build-tactics.md` § Tactic 17 (Phase 3 — surface-scoped colour tokens + `.js-ready` reveal gate) |
| Build adds a non-default theme (light derivation of a dark-only style, dark derivation of a light-only style) OR introduces a theme-toggle | `references/build-tactics.md` § Tactic 18 (Phase 3 — interactive state coverage in derived themes; mandatory companion to Tactic 17 when crossing theme boundaries) |
| About to build markup with grids/cards | `references/layout-patterns.md` (Phase 3 — pick pattern deliberately) |
| Chosen a library, starting build | `references/styles/<style>.md` + `.design.md` |
| About to deliver, pre-review | `references/style-reviews/<style>.md` |
| `effects.liquid-glass === true` (user mentioned glass, liquid glass, frosted, Apple-style, iOS 26) | `references/effects/liquid-glass.md` (Phase 3 Step 3.0.10 — CSS + WebGL refraction modifier); run compatibility check first in Phase 2 Step 2.6; run `references/style-reviews/effects/liquid-glass.md` in Phase 4 Step 4.5b |
| Universal checks (any style) | `references/base-principles.md` |
| Custom / no library fits | `references/base-principles.md` only; derive DESIGN.md from brief |

## Anti-Patterns (Universal — enforce in every build)

- ❌ **Preset literalness.** Output shares >80% tokens with library default. Always diverge.
- ❌ **Generic AI slop.** Purple gradients on white, Inter everywhere, cookie-cutter rounded cards.
- ❌ **Decorative elements without purpose.** Every accent, border, or icon should earn its place.
- ❌ **Missing `:hover` / `:focus` states.** Non-negotiable.
- ❌ **Layouts that break between 768px and 1024px.** Test mid-widths, not just phone and desktop.
- ❌ **Multiple conflicting font families.** 2 is a pair, 3+ is a mess.
- ❌ **Reference image literalness.** If the output is recognisable as "the inspiration with different content", refactor.
- ❌ **CSS `transform:` on a `.js-ready`-gated element that GSAP will tween (motion: high builds).** Stacks with GSAP's transform, leaves content permanently masked. CSS owns opacity for the pre-JS hide; GSAP owns transform fully. Mechanical check: `grep -E "\.js-ready[^{]*transform"` on the build file must return zero matches before delivery. (motion-tactics.md § Cardinal rule.)
- ❌ **3D where DOM would do.** A spinning cube on a startup landing page, a particle field behind text that costs 30 FPS on mobile, a `3d-scene` hero where a beautifully-typed headline + photo would convert better. The C.U.R.E. test for 3D is non-optional — Context, Usefulness, Restraint, Emotion. If the answer to any is "no", drop the 3D and lean into typography. (webgl-3d-principles.md § Anti-patterns.)
- ❌ **Shipping `dimension > none` without all four failure-mode guards.** WebGL feature detect with DOM fallback, `prefers-reduced-motion` static frame, DOM mirror for SEO/a11y (canvas is `aria-hidden="true"`, real headline/body/CTAs in DOM), 8s load timeout. Missing any one is a delivery-blocking defect. (webgl-3d-tactics.md § Pre-build checklist.)
- ❌ **Fullscreen WebGL backdrop without a legibility scrim.** A bright animated canvas behind text reduces contrast from 12:1 to ~1.4:1 in real builds — far below WCAG AA's 4.5:1. Mandatory two-layer scrim (`.scrim` center-radial + `.scrim-below` past-hero dimmer) when `position: fixed; inset: 0;` canvas sits behind content. Run the contrast spot-check before delivery — pick the darkest pixel under body text, verify ≥ 4.5:1. Compose the WebGL object OFF-CENTRE so the scrim has less work to do. Bloom intensity ≤ 0.8, threshold ≥ 0.30. (webgl-3d-tactics.md § Sub-guard 3a.)
- ❌ **`dimension: 3d-scene` with `motion: low`.** A static 3D scene reads as broken, not as deliberate. Tier-coupling rule — surface a warning, build as specified, log conflict. (webgl-3d-tactics.md § Tier-coupling sanity.)
- ❌ **Forcing 3D into Sanctuary Tech, Memoir, or Spritify against library refusal.** Sanctuary Tech + trauma-informed mode is a hard-refuse — `dimension` is forced to `none` regardless of user pick (cognitive load, GPU thermal throttling on older devices, no-surprise-motion contract). Memoir and Spritify are soft-refuse — warn and confirm before proceeding. (webgl-3d-style-fit.md § Override protocol.)
- ❌ **Glass on dashboard data cells.** Data tables and metric cards holding numeric values require opaque, high-contrast surfaces — translucency makes it impossible to distinguish whether the background texture is part of the metric or behind it. Glass on data cells is forbidden regardless of style tier. (`effects/liquid-glass.md` § Forbidden elements.)
- ❌ **Refused-style override stacking (≥2 glass elements on a refused style).** The single-element rule permits at most one isolated chrome element on a refused style. Two glass elements on a refused style constitutes a pattern — and a pattern means the style system has glass in it, which the refused tier explicitly rejects. Escalate to style switch. (`effects/liquid-glass.md` § Override protocol.)

## Adding New Styles

To add a new design style:
1. Create `references/styles/<n>.md` (craft guide: tokens, typography rules, color palette, component patterns, anti-patterns, template reference)
2. Create `references/styles/<n>.design.md` (YAML front matter tokens + rationale prose, following the DESIGN.md spec)
3. Create `references/style-reviews/<n>.md` (5–8 style-specific review questions)
4. Add a row to the Style Menu table above
5. Add auto-detection rules if applicable
6. Optionally add HTML templates in `assets/templates/<n>/`
