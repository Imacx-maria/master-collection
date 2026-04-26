
# Atmospheric Protocol

Editorial-meets-technical dark system for cognitive tooling, protocol infrastructure, and AI products that want to read simultaneously as literary essay and technical artifact — Instrument Serif display headlines (with italic continuation as the signature move), Inter for UI and chrome, JetBrains Mono for data and metrics, glass cards with hairline gradient borders, and a load-bearing atmospheric gradient backdrop chosen from three named variants (Bloom / Flow / Particle).

## Best for

- Cognitive / mental-model / thinking-tool products (Neuform-style)
- Protocol and infrastructure landing pages (Nexus, Stripe-adjacent)
- AI products that want a serious editorial register without going corporate-blue
- Treasury / finance / orchestration platforms that need both authority and atmosphere
- Founder/operator manuals, frameworks, and "manifesto" product pages
- Anything where the page should feel like a research paper crossed with a control panel

**Avoid for:** kid/playful products, dense dashboards (the atmosphere competes with data), e-commerce, anything that needs a bright or saturated palette.

**Light-mode caveat:** the style is **dark-mode native**. A light-mode interpretation IS possible but requires the explicit derivation rules in *Light-Mode Interpretation (Advanced Derivation)* below — and is bound by the 5 light-mode glass rules in `references/effects/liquid-glass.md` § Light-mode adaptation. Don't ship light-mode Atmospheric Protocol without those rules; flat-tint glass and white hairlines evaporate against light backgrounds.

## Quick Start

1. Pick the atmosphere variant first — **Bloom** (radial indigo glows), **Flow** (smoky violet linear shift), or **Particle** (WebGL dot-matrix). The choice locks the accent colour and the backdrop recipe.
2. Build the backdrop using the matching recipe in `gradient-tactics.md` (§ R1 for Bloom, § R2+R3 for Flow, § R5 for Particle). Always include the CSS fallback for Particle.
3. Wrap every card in the **gradient border shell** (`gradient-tactics.md` § R6) — 1px hairline frame fading from `rgba(255,255,255,0.10)` to transparent.
4. **Apply `box-shadow` to every card** — `--shadow-card-soft` for standard cards, `--shadow-card-bloom` (or `--shadow-card-flow`) for the 1–2 hero/featured cards per page. **This is mandatory, not decorative.** Cards without shadow read as ghost outlines because the bloom backdrop bleeds past the card edges and the eye reconstructs an apparent second card. The shadow is what visually anchors the card to the surface.
5. Headline pattern: roman first line, italic continuation on the second. "Better questions. *Better answers.*" Never bold; weight 400 only.
6. Overline pattern: `● ALL CAPS LABEL` in `letter-spacing: 0.10em` Inter Medium, housed in a glass pill.
7. Mono for data only: metric values, system labels, percentages. Never body, never display.
8. **When using `gradient-shell`, never `max-width` the inner `shell-content`.** Constrain the shell wrapper instead — otherwise the shell background gets exposed on the sides.

## Display Typography & Hero Patterns

Atmospheric Protocol uses serif type as research-paper title-page typesetting. Display sizes carry intellectual gravitas; the italic continuation gives the headline a sense of completing its own thought.

**`display-xl` (88px, weight 400, line-height 1.05)** — The hero anchor. One per page. Always centred (the style's hero composition is centred-with-discipline, not asymmetric). Pair with the italic variant on the second line.

**`display-lg` (72px, weight 400, line-height 1.0)** — Smaller hero variant for denser pages or sections that aren't the page-opening hero.

**`headline-lg` (48px, weight 400, line-height 1.10)** — Editorial quote sections — the wide statement that bridges between the 3-card grid and the next major section. Often runs ~80% of container width with italic mid-sentence ("The amateur accepts the first answer. The architect interrogates the premise. *Stop solving the wrong problems at maximum speed.*").

**`headline-md` (32px, weight 400)** — Sub-section openers, occasional card titles when a card needs a serif moment.

**Hero pattern (canonical):**

1. Floating glass nav-pill, fixed top, centred, ~60% viewport width
2. Glass overline tag with leading `●` ("● CORE CAPABILITIES")
3. `display-xl` headline, two lines, second line italic
4. `body-lg` supporting paragraph, max-width ~60ch, centred, in `text-secondary`
5. Optional: a primary pill button below the paragraph (often skipped on first hero — the 3-card grid below acts as the next interaction)
6. 3-card grid (typically `grid-cols-3` on desktop, stacking on mobile)

**Spacing:**

- Section vertical: 96–128px on desktop; 64px on mobile
- Hero vertical padding: 128–160px top, ~80px bottom (creates the "page opens with breathing room" feel)
- Card grid gaps: 24px standard, 16px when cards are dense
- Container max-width: 1280px with 32px page padding
- Body paragraph max-width: 60ch (forces readable line length even on wide viewports)

## Atmosphere Variants

| Variant | Accent | Backdrop recipe | Use when the page feels… |
|---|---|---|---|
| **Bloom** | Indigo `#6366F1` | Layered radial mesh (`gradient-tactics.md` § R1, dark pattern) | Capital-infrastructure, financial, orchestration, "operating at scale" |
| **Flow** | Violet `#8F47AE` | Smoky linear shift + SVG grain (R2 + R3) | Cognitive, philosophical, editorial, "rewriting your thinking" |
| **Particle** | Monochrome white | WebGL dot-matrix breathing (R5) + CSS fallback | Protocol, data, quiet-technical, "system signal" |

**Variant locks the accent.** Bloom builds use indigo for buttons, links, focus halos, data-positive states. Flow builds use violet. Particle builds use no chromatic accent — buttons stay white-on-dark, no glow tints. Mixing accents across a page breaks the atmospheric coherence.

**Variant locks the card shadow.** Bloom hero cards get `0 25px 50px -12px rgba(99,102,241,0.20)`. Flow hero cards get the violet-tinted equivalent. Particle hero cards get neutral black `card-soft`.

## Content Slots

| Slot | Location | Content |
|------|----------|---------|
| `page-title` | `<title>` | Browser tab title |
| `nav-pill` | Top, fixed | Glass capsule with brand mark + 3–4 link items + primary CTA |
| `hero-overline` | Hero | Glass pill with `● LABEL` (Inter, 11px, uppercase, 0.10em tracking) |
| `hero-headline-line-1` | Hero | `display-xl` roman serif |
| `hero-headline-line-2` | Hero | `display-xl` *italic* serif (the continuation) |
| `hero-subhead` | Hero | `body-lg` Inter, max-width 60ch, `text-secondary` |
| `hero-cta` | Hero | Primary white pill button (optional — often deferred to the card grid below) |
| `card-grid` | Below hero | 3 cards on desktop, identical width, varying internal content |
| `card-title` | Card | `card-title` Inter Medium 18px |
| `card-body` | Card | `body-md` Inter 14px in `text-secondary` |
| `card-widget` | Card (lower 60%) | One of: data console, interactive widget, metrics pill cluster |
| `data-pill` | Inside card-widget | Mono text in `data-pill` chrome (system labels, metric values) |
| `editorial-quote` | Mid-page | `headline-lg` serif, 80% container width, italic mid-sentence |
| `author-block` | After quote | Image (b&w portrait, arched container) + identity overline + name + body |
| `footer-cta` | Bottom | Single primary pill button repeating the hero ask |

## Design Tokens Summary

**Colours** (dark mode default — see *Light-Mode Interpretation* below for the light derivation):
- Background: `#030508` (near-black, faint blue undertone)
- Surface card: `#0A0D14` (opaque) / Surface glass: `rgba(3,5,8,0.80)` (translucent + 12px blur)
- Text: `#FFFFFF` / `#A1A1AA` / `#71717A` / `#52525B`
- Borders: `rgba(255,255,255,0.05–0.12)`, always 0.67px stroke
- Accent: `#6366F1` (Bloom) / `#8F47AE` (Flow) / monochrome white (Particle)
- Focus: `#3898EC` (a11y only)

**Typography:**
- Display: Instrument Serif, Source Serif 4 fallback, weight 400 only, italic for continuation
- UI/body: Inter, weights 400/500
- Data: JetBrains Mono / IBM Plex Mono, weight 400
- Display line-height: 1.0–1.10 (tight)
- Body line-height: 1.55–1.60 (research-paper readable)
- Overlines: 11px, weight 500, `letter-spacing: 0.10em`, uppercase

**Layout:**
- Container: 1280px max, 32px page padding
- Section vertical: 96–128px desktop
- Card grid: 3 cols desktop, stacking mobile, 24px gap
- Body max-width: 60ch

**Depth:**
- Glass blur: 12px standard, 24px for hero panels
- Border opacity: 5% (hairline) / 8% (soft) / 12% (strong)
- Shadows: neutral black for standard cards; accent-tinted only on hero/featured cards

The Liquid Glass effect formalizes this style's existing glass treatment as a portable modifier — see `references/effects/liquid-glass.md`. When applied to Atmospheric Protocol, the modifier reuses this style's `surface-glass`, `pad-glass`, and `card-glass` tokens verbatim — no parallel vocabulary. The modifier adds: (a) explicit Regular / Clear / Prominent variants with documented alpha + blur tiers, (b) a mandatory `prefers-reduced-transparency` fallback block, (c) the optional WebGL/SDF refraction track when `style-tuning.axes.dimension.value === 'shader-accents'` and the user opts in. This is a native tier pairing — Atmospheric Protocol is one of three styles for which Liquid Glass requires no compatibility override.

For complete values, see the YAML frontmatter in `atmospheric-protocol.design.md`.

## Signature Patterns

### Italic continuation headline
Every hero (and most major section openers) uses a two-line headline where the first line is roman Instrument Serif and the second line is the italic of the same family. The italic is not emphasis — it's the headline finishing the thought. Reads as a single sentence with a typographic shift mid-stride.

```html
<h1 class="display-xl">
  Better questions.<br>
  <em class="italic">Better answers.</em>
</h1>
```

### Status-dot overline
Section labels are housed in glass pills with a leading `●` character. The dot is character-level (Unicode `●`), not an SVG — it should match the text colour exactly and respect text spacing.

```html
<span class="overline-tag">● CORE CAPABILITIES</span>
```

### Gradient border shell + mandatory shadow
Every card wears a 1px gradient frame fading from `rgba(255,255,255,0.10)` at top to transparent at bottom, **plus a drop shadow** that anchors it against the bloom backdrop. The shadow is not optional — it's the second half of the recipe. Full recipe in `gradient-tactics.md` § R6.

```css
.gradient-shell {
  padding: 1px;
  border-radius: 32px;
  background: linear-gradient(to top,
    rgba(255,255,255,0.10) 0%,
    rgba(255,255,255,0.02) 50%,
    transparent 100%);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.40);  /* MANDATORY */
}
.gradient-shell--accent {
  background: linear-gradient(to top,
    rgba(99,102,241,0.30) 0%,
    rgba(99,102,241,0.05) 50%,
    transparent 100%);
  box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.20);  /* accent-tinted for hero/featured */
}
.gradient-shell > .card { border-radius: 31px; background: #0A0D14; }
```

**Why mandatory.** The bloom backdrop is fixed-positioned and full-bleed. A card sitting on top of it without a shadow has no visual separation from the bright bloom areas behind it — the bloom bleeds past the card edges, the eye reconstructs an apparent "ghost outline" offset from the card, and the page reads as buggy. The shadow softens the card-to-bloom transition so the bloom looks like deliberate ambient light rather than an unintended halo. Mechanical check before delivery: `grep "box-shadow" <build-file>` — every card class must have one.

For accent-tinted variants (Bloom hero cards), swap the gradient to `rgba(99,102,241,…)` for indigo or `rgba(143,71,174,…)` for violet, and use the matching accent-tinted shadow.

### Mono data chrome inside cards
Card lower-halves frequently house a "control panel" widget — system label in mono, metric values in mono, occasional toggle or slider. The chrome reads as if you're peering into the product's actual interface. Use `data-pill` for metric values and `overline` for status labels.

```html
<div class="card">
  <h3 class="card-title">Velocity Extraction</h3>
  <p class="body-md">Accelerate input-to-action ratios.</p>
  <div class="card-widget">
    <div class="flex justify-between">
      <span class="overline">● PROCESSING SPEED</span>
      <span class="data-pill">99.9%</span>
    </div>
    <!-- meter / signal bar / etc -->
    <button class="button-secondary w-full">EXECUTE ⌘</button>
  </div>
</div>
```

### Glass nav-pill, fixed centred
Navigation lives in a single glass capsule, centred at the top of the viewport, fixed during scroll. Width responds to content (no full-width nav bar). The pill itself uses `surface-glass` background + 12px backdrop blur + hairline border.

## Image Guidelines

- **Style:** Black-and-white photography. Portrait shots (founders, authors, thought leaders) work best in arched containers (top corners rounded, bottom corners square). High-contrast b&w; never colour-toned, never sepia.
- **Avoid:** Stock photography, illustrations (the style has no illustration vocabulary — use type and chrome instead), 3D renders, geometric pattern backgrounds.
- **Product visuals:** Don't use product screenshots. Use the in-card widget pattern instead — show *fragments* of the product as glass widgets, not full screenshots.
- **Iconography:** Linear stroke 1.5px (Lucide, Phosphor light, Solar). Never filled icons except the leading `●` status dot. Never illustrative or 3D icons.

## Responsive Behavior

- **Desktop (>1024px):** Full layout, 3-column card grid, max display type at 88px, atmosphere at full intensity
- **Tablet (768–1024px):** 2-column card grid, display drops to 64–72px, atmosphere unchanged
- **Mobile (<768px):** Single column, hamburger nav (replaces nav-pill), display drops to 48px, atmosphere simplified — Particle variant drops shader complexity by 50%, Bloom/Flow variants halve the number of bloom layers
- **Section padding:** Reduces from 128px → 96px → 64px proportionally
- **Container:** 1280px → fluid below 1280px → 16px page padding on mobile

## Customization

The two divergence axes most commonly used:

1. **Variant choice (locked at build time)** — Bloom / Flow / Particle. This is the primary axis. Pick based on the page's emotional register (financial-orchestration / cognitive-philosophical / quiet-technical-data).
2. **Accent shift (within variant)** — Bloom can ship with indigo, deep blue, or steel cyan. Flow can ship with violet, deep magenta, or dusty rose. Particle stays monochrome. Document the chosen accent in DESIGN.md.

Optional axes:

3. **Italic discipline** — The signature italic-continuation pattern can be relaxed to "italic for one keyword per headline" if the brand reads too literary. Don't drop italic entirely — it's the typographic identity.
4. **Card density** — Default is 3 columns with substantial padding (32px). Denser product pages can drop to 4 columns with 20px padding, but the gradient border shell stays mandatory.
5. **Mono presence** — Default is "data only." Heavier-product pages can extend mono to one or two UI labels (input placeholders, button kbd hints). Never let mono enter body or display.

## Light-Mode Interpretation (Advanced Derivation)

Atmospheric Protocol is dark-mode native because the load-bearing element is the gradient atmosphere — and atmospheres read with intensity on dark canvases. A light-mode interpretation IS possible (canonical reference build: `_tests/design-skill-lab/oneshot/atmospheric-protocol-light-dark.html`), but it diverges from the default in 5+ tokens, not 2. Treat it as an **advanced derivation** rather than a parameter switch.

### When to derive light mode

- The brief requires a `theme-toggle` UX (e.g., user-controlled or system-aware).
- The product context is one where light mode is the cultural expectation (productivity surfaces, financial dashboards, document tools) but the visual register specifically required is Atmospheric Protocol.

### When NOT to derive light mode

- The brief simply says "light mode" with no specific reason — pick a natively-light style instead (Warm Editorial, Editorial Portfolio, Memoir Blog).
- Trauma-informed contexts — light mode here adds cognitive load on top of the atmosphere; switch to Sanctuary Tech.
- E-commerce or any imagery-led brief — atmosphere distracts from product images regardless of theme.

### The required token deltas (from dark default → light derivation)

| Token | Dark default | Light derivation |
|---|---|---|
| `--color-bg` | `#030508` | `#F4F1EA` (warm parchment — **never pure white**, kills glass) |
| `--color-surface-card` | `#0A0D14` | `#FFFFFF` |
| `--color-surface-glass` | `rgba(3,5,8,0.80)` | `rgba(255,255,255,0.62)` (≥0.55 mandatory) |
| `--color-text-primary` | `#FFFFFF` | `#14181F` (never pure black) |
| `--color-border-hairline` | `rgba(255,255,255,0.05)` | `rgba(20,24,31,0.10)` (DARK hairline, mandatory) |
| `--color-accent-bloom` | `#6366F1` | `#4A4FE0` (deeper, more saturated) |
| `--color-accent-flow` | `#8F47AE` | `#7B2FA8` (deeper) |
| Atmosphere bloom opacity | 0.18 / 0.14 / 0.10 | 0.22 / 0.18 / 0.10 (slightly stronger to push colour through glass) |
| Atmosphere overall `opacity` | 1.0 | 0.55 (dim so dark text on top stays legible) |
| Grain `mix-blend-mode` | `overlay` | `multiply` |
| Grain `opacity` | 0.35 | 0.18 |
| Glass `backdrop-filter` blur | `blur(16px)` | `blur(28px)` (stronger) |
| Glass `backdrop-filter` saturate | n/a | `saturate(1.55)` (mandatory boost) |

These deltas are derived from the 5 mandatory light-mode glass rules — see `references/effects/liquid-glass.md` § Light-mode adaptation. Skipping any one ships glass that's invisible against the light canvas.

### Compatibility notes

- **Do NOT switch to flat white (`#FFFFFF`) page backgrounds.** Light-mode glass requires a busy backdrop (gradient, mesh, image). Atmosphere stays — just dimmed. A flat-white Atmospheric Protocol page is broken by definition.
- **`prefers-reduced-transparency` fallback is mandatory in BOTH modes** but especially in light — without backdrop-filter, the surfaces fall back to opaque `--color-surface-card` (white). Verify the page still reads as Atmospheric Protocol with the fallback active (it should — the type system and atmosphere carry the identity).
- **Variant choice:** Bloom is the safest atmosphere variant for light-mode derivation (radial colour mesh translates well). Flow (smoky linear shift) reads best dimmed at 0.45–0.50 opacity. Particle (WebGL dot-matrix) works but the dot density needs to drop ~30% on light, otherwise reads as noise.

### Provenance requirement

Any Atmospheric Protocol build that ships light + dark MUST declare in DESIGN.md provenance:

```yaml
provenance:
  light-mode-derivation: true
  divergences-from-library:
    - color-mode-axis (added light variant — beyond library default of dark-only)
    - light-glass-tokens (5 mandatory rules from liquid-glass.md § Light-mode adaptation)
    - atmosphere-dimming (opacity 0.55 in light; 1.0 in dark)
    - grain-blend-flip (overlay→multiply on light)
  trade-offs-accepted:
    - "Atmosphere intensity reduced in light mode to preserve text contrast — accepted because toggle UX requires both registers"
```

Without this declaration, the divergence audit in Phase 4 Step 4.5 fails — light-mode Atmospheric Protocol looks like generic SaaS chrome rather than a deliberate authored derivation.

### Interactive state coverage (mandatory companion step)

The token deltas above cover **surfaces** (atmosphere, glass cards, page backgrounds). They do NOT cover **interactive controls** (buttons, links, form inputs). The base Atmospheric Protocol CSS contains hardcoded values inside `.btn--primary` (`color: #000000`) that look correct in dark mode but render the button invisible in light mode. This is not a bug in the library — it's a structural reality of any single-theme style getting a derivation.

**Run `references/build-tactics.md` § Tactic 18 (Interactive state coverage in derived themes) for the full audit + override pattern.** At minimum, re-derive `.btn--primary` (default + hover + focus-visible), `.btn--secondary` (same), the theme toggle, and any nav-CTA pills. The reference build (`atmospheric-protocol-light-dark.html`) shows the canonical override block — copy its pattern, adapt selectors to your project.

---

## Tier Placement vs Technical Refined, Sanctuary Tech, Basalt Ecommerce

Atmospheric Protocol overlaps with three other dark-leaning libraries; choose based on these distinctions:

- **vs Technical Refined** — Technical Refined is monospace-led with sparse colour and a modular grid; it's a documentation/spec aesthetic. Atmospheric Protocol is serif-led with a load-bearing gradient atmosphere; it's a manifesto/protocol aesthetic. Technical Refined could ship in light mode; Atmospheric Protocol is dark-only.
- **vs Sanctuary Tech** — Sanctuary is muted, warm, and quiet — designed for crisis/legal/healthcare contexts where calm matters. Atmospheric Protocol is *atmospheric* but not calm — there's deliberate intensity in the gradient backdrop and italic typography. Sanctuary uses warm-tinted greys; Atmospheric uses near-black with cool undertones.
- **vs Basalt Ecommerce** — Basalt is dark-mode product/commerce with a stronger focus on imagery and product cards. Atmospheric Protocol has no commerce vocabulary — no price chips, no add-to-cart patterns, no product galleries. If the brief says "sell something," reach for Basalt; if it says "explain a framework," reach for Atmospheric.

If the brief mentions Stripe, Linear, Luma, Neuform, or Nexus — Atmospheric Protocol is the right pick. If it mentions documentation, API reference, or developer console — try Technical Refined first.
