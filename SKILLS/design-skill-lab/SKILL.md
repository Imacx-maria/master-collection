---
name: design-skill-lab
description: |
  Unified design workflow with 12 distinct visual styles. Always use when the user asks to build, design, or style any web page, landing page, component, dashboard, e-commerce, portfolio, blog, or app — even if no style is specified. Triggers on style names: brutalist, editorial, technical-refined, jocril, luxury, bento, playful, warm, sanctuary, spritify, memoir, basalt, warm-editorial, or descriptors like "AI product", "literary tech", "SaaS site", "dev tool", "hotel site", "kids site", "agency site", "calming UI", "blog design".

  Runs a mandatory 4-phase workflow: ANALYSE (extract inspiration qualities without copying), TRANSLATE (derive a project-specific DESIGN.md that diverges from the library default in at least 2 tokens), BUILD (implement), REVIEW (style-aware critique + universal checks). Never skip phases. Never copy reference images or templates verbatim. Replaces 12 individual design skills.
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

A unified design workflow with 12 style libraries. The workflow always runs in 4 phases — `ANALYSE → TRANSLATE → BUILD → REVIEW`. Each style library contains tokens (YAML `DESIGN.md`), craft guide (prose reference), and style-specific review checks.

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

**Step 3.0.07 — Surface-context check (conditional).** Before generating any markup that places **a card / testimonial / quote / panel / callout inside a section with the OPPOSITE surface mode** (light card in dark section, or dark card in light section), OR uses **JS-driven reveal animations** (`.reveal { opacity: 0 }`, scroll-triggered fades), load `references/build-tactics.md` § Tactic 17.

Tactic 17 is the contract that catches the two most user-visible defects from the oneshot stress test (Spritify hero testimonial invisible; Warm Editorial dark section text inheritance):

- **17.3 Per-surface colour tokens** — components that can sit on multiple surface contexts must declare their `background` AND `color` as a unit, never inherit from parent context. Token names are surface-scoped (`--text-on-surface-light`), not hierarchy-scoped (`--text-default`).
- **17.4 Progressive-enhancement gate for reveals** — `.reveal { opacity: 0 }` must be gated by `.js-ready` class added by JS as the FIRST line of the IIFE. Without this, JS failure leaves content permanently invisible.
- **17.6 Audit test (mental flip)** — before delivery, mentally flip every surface in the build. Any text that becomes invisible was inherited instead of scoped. Refactor.

The 17.7 checklist is the contract; failures here are the highest-severity bugs the skill has shipped (2/11 builds in the oneshot run had this defect).

This step pairs with `base-principles.md` Q17 (audit lens — "is the colour scoped?"). Tactic 17 is the build lens — "scope it now, before markup."

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
| 12 | **Custom / Freestyle** | When none of the above fit | Uses base principles below, derive a fresh DESIGN.md bottom-up |

## Auto-Detection Rules

Skip the menu when context is clear. These map brief cues to a **starting** library — Phase 2 still has to derive a diverged project DESIGN.md.

- **AI product / AI assistant / agent / co-pilot / literary-tech / "warm but technical"** → Style 11 (Warm Editorial)
- **SaaS / dev tool / dashboard / technical product (cool/clinical leaning)** → Style 3 (Technical Refined). Jocril projects (detected by path or mention) also map here.
- **E-commerce / product pages** → Style 4 (Basalt) — but check if the brand calls for Style 6 (Creative Studio) or Style 8 (Playful Bento) first
- **Blog / newsletter / writing** → Style 5 (Memoir)
- **Portfolio / showcase of work** → Style 2 (Editorial)
- **Crisis / vulnerable users / healthcare / legal aid** → Style 10 (Sanctuary). If trauma-informed, load `references/trauma-informed.md` from the design-reviewer skill.
- **Kids / family** → Style 9 (Spritify); energetic adult brand → Style 8 (Playful Bento)
- **Hotel / spa / wellness / interior design** → Style 7 (Warm Serene)
- **Agency / studio / creative services** → Style 6 (Creative Studio)
- **Brutalist / edgy / high-contrast / poster-like** → Style 1 (Neo-Brutalist)
- User says "fun" or "energetic" without kid context → Style 8 (Playful Bento)

If still ambiguous after these rules, ask one question (see Phase 1).

## File Map

```
design-skill-lab/
├── SKILL.md                              # this file — workflow orchestrator
├── references/
│   ├── base-principles.md                # universal rules (typography, a11y, spacing)
│   ├── build-tactics.md                  # tactical do/don't recipes for build moment (17 tactics: 1-13 always-on; 14 dark-mode, 15 mobile-nav, 16 component-reusability, 17 surface-context conditional)
│   ├── inspiration-analysis.md           # how to extract from an image without copying
│   ├── user-overrides.md                 # detection + protocol for user colors/fonts/URL/image, fidelity scale
│   ├── style-tuning.md                   # 9-question interview + per-library defaults table (Phase 2.1)
│   ├── layout-patterns.md                # bento vs uniform vs list, alignment rules, span vocabulary
│   ├── motion-principles.md              # design lens for motion: taxonomy, 4 pillars, canonical duration table, easing intent, C.U.R.E. audit, WCAG 2.2.2/2.3.1, pattern catalog (Phase 3 Step 3.0.04)
│   ├── motion-tactics.md                 # technical contract per motion tier (medium=CSS+IO, high=GSAP+ScrollTrigger+SplitText+Flip) (Phase 3 Step 3.0.05)
│   ├── loader-patterns.md                # page-loader contract per page-load value (subtle / functional / branded-intro); 9 recipes; 4 mandatory failure-mode guards (Phase 3 Step 3.0.06)
│   ├── typography-safety.md              # tier+modifier model, language adjustments, failure modes
│   ├── sidecar-contract.md               # .design.md → tokens.json + tailwind.config.js transform spec (Phase 4.8.1)
│   ├── scripts/
│   │   └── generate-sidecars.py          # auto-generator for sidecars; deterministic transform from .design.md frontmatter
│   ├── styles/                           # 12 style libraries
│   │   ├── neo-brutalist.md              # craft guide (prose)
│   │   ├── neo-brutalist.design.md       # tokens YAML + rationale
│   │   ├── editorial-portfolio.md
│   │   ├── editorial-portfolio.design.md
│   │   ├── technical-refined.md
│   │   ├── technical-refined.design.md
│   │   ├── warm-editorial.md
│   │   ├── warm-editorial.design.md
│   │   └── ... (same pattern for all 12)
│   └── style-reviews/                    # per-style review lenses
│       ├── neo-brutalist.md
│       ├── editorial-portfolio.md
│       ├── warm-editorial.md
│       └── ... (same pattern for all 12)
```

## Quick Reference — When to Load What

| Situation | Load |
|-----------|------|
| User provides colors / fonts / image / URL | `references/user-overrides.md` (run first in Phase 1) |
| User mentions image/inspiration | `references/inspiration-analysis.md` |
| `style-tuning.axes.motion` is `medium` or `high` | `references/motion-principles.md` FIRST (Phase 3 Step 3.0.04 — design lens, vocabulary, duration table, C.U.R.E.), then `references/motion-tactics.md` (Phase 3 Step 3.0.05 — technical contract; medium=CSS-only, high=GSAP) |
| `style-tuning.axes.page-load` is anything other than `none` | `references/loader-patterns.md` (Phase 3 — pattern map + 9 recipes + 4 mandatory failure-mode guards) |
| Build mixes light/dark surfaces (light card in dark section, etc.) OR uses reveal animations | `references/build-tactics.md` § Tactic 17 (Phase 3 — surface-scoped colour tokens + `.js-ready` reveal gate) |
| About to build markup with grids/cards | `references/layout-patterns.md` (Phase 3 — pick pattern deliberately) |
| Chosen a library, starting build | `references/styles/<style>.md` + `.design.md` |
| About to deliver, pre-review | `references/style-reviews/<style>.md` |
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

## Adding New Styles

To add a new design style:
1. Create `references/styles/<n>.md` (craft guide: tokens, typography rules, color palette, component patterns, anti-patterns, template reference)
2. Create `references/styles/<n>.design.md` (YAML front matter tokens + rationale prose, following the DESIGN.md spec)
3. Create `references/style-reviews/<n>.md` (5–8 style-specific review questions)
4. Add a row to the Style Menu table above
5. Add auto-detection rules if applicable
6. Optionally add HTML templates in `assets/templates/<n>/`
