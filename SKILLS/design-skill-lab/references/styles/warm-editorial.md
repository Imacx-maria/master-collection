
# Warm Editorial

Literary-salon design system for AI products, technical writing surfaces, and thoughtful tools — characterised by parchment-toned canvas, single-weight serif headlines, terracotta brand accent, and exclusively warm-toned neutrals.

## Best for

- AI products and assistants (Claude-adjacent feel, but not Claude-specific)
- Developer tools that want warmth instead of clinical-tech
- Technical writing platforms, documentation, knowledge bases
- Magazine-style product pages (long-form scroll with chapter rhythm)
- Thoughtful B2B SaaS that wants to read literary rather than utilitarian
- Companion / agent / co-pilot products where trust and warmth matter

**Avoid for:** Loud marketing landings, kid products, dense dashboards, aggressive e-commerce, anything that needs a vibrant or saturated palette.

## Quick Start

1. Use Parchment (`#F5F4ED`) as the page background — never pure white
2. Set serif headlines at weight 500 only — no bold, no light, no italic
3. Reserve Terracotta (`#C96442`) for primary CTAs and the highest-signal brand moments
4. Use ring shadows (`0 0 0 1px #D1CFC5`) for interactive depth instead of drop shadows
5. Alternate light Parchment sections with Near Black (`#141413`) sections for chapter rhythm
6. Body line-height stays at 1.60 for essay-reading cadence

## Display Typography & Hero Patterns

Warm Editorial uses serif type as essay-page typesetting. Display sizes carry literary gravitas, not poster aggression.

**`display-xl` (64px, weight 500, line-height 1.10)** — The hero anchor. Maximum impact, book-title presence. One per page. Use centred or asymmetric within the hero container; never poster-shouting.

**`headline-xl` (52px, weight 500, line-height 1.20)** — Section openers. Marks chapter transitions; pairs naturally with the dark/light section alternation.

**`headline-lg` (36px, weight 500, line-height 1.30)** — Sub-section markers, secondary scene-setters.

**`headline-md` (32px, weight 500, line-height 1.10)** — Card titles, feature names, named moments inside sections.

**`headline-sm` (25px, weight 500, line-height 1.20)** — Smaller card titles, model names in comparison grids.

**Hero patterns by page type:**

- **AI product landing** — Centred or 60/40 asymmetric hero. `display-xl` headline + `body-lg` (20px Sans) supporting paragraph + Terracotta CTA + Warm Sand secondary CTA. Hero container at 32px radius optional. Generous 80–120px padding.
- **Technical product / tool** — Asymmetric hero with embedded screenshot or illustration on one side. Type sits in the gutter rather than competing with imagery.
- **Documentation / writing platform** — Reading-column hero (~720px max), `display-xl` headline, body-serif intro paragraph below. Closer to a book's title page than a product sheet.
- **Magazine-style scroll** — Hero immediately followed by a dark Near-Black section break, then back to light. Establish chapter rhythm in the first 1.5 viewports.

**Spacing for editorial composition:**

- Section vertical: 96–120px between major sections; 64px for sub-sections
- Hero padding: 80–120px top/bottom on desktop
- Card grid gaps: 24–32px
- Reading column max-width: 720px (long-form prose); 1200–1360px (full layouts)
- Body paragraph rhythm: line-height 1.60, paragraph margin 1em

## Content Slots

| Slot | Location | Content |
|------|----------|---------|
| `page-title` | `<title>` | Browser tab title |
| `nav-brand` | Nav | Brand wordmark (serif, 22–25px) |
| `nav-links` | Nav | Navigation items in Olive Gray (`#5E5D59`) |
| `nav-cta` | Nav | Terracotta or White Surface button |
| `hero-headline` | Hero | `display-xl` (64px) serif weight 500 |
| `hero-subhead` | Hero | `body-lg` (20px) sans, Olive Gray |
| `hero-cta-primary` | Hero | Terracotta button |
| `hero-cta-secondary` | Hero | Warm Sand button |
| `hero-illustration` | Hero | Optional organic illustration or product screenshot |
| `section-overline` | Section | Small uppercase label (10px, letter-spacing 0.5px) |
| `section-headline` | Section | `headline-xl` (52px) serif |
| `section-body` | Section | `body-md` or `body-serif` |
| `feature-card-title` | Feature | `headline-md` (32px) serif |
| `feature-card-body` | Feature | `body-md` sans |
| `model-card-name` | Model grid | `headline-sm` (25px) serif |
| `model-card-desc` | Model grid | `body-sm` Olive Gray |
| `dark-section-headline` | Dark band | `headline-xl` (52px) serif on Near Black, Ivory text |
| `dark-section-body` | Dark band | `body-md` sans, Warm Silver text |
| `code-block` | Inline | Anthropic Mono, 15px, line-height 1.60 |
| `footer-band` | Footer | Near Black background, Warm Silver text |

## Design Tokens Summary

**Colors:**
- Background: `#F5F4ED` (Parchment)
- Surface: `#FAF9F5` (Ivory)
- Surface-alt: `#E8E6DC` (Warm Sand)
- Surface-dark: `#30302E` / Page-dark: `#141413`
- Text: `#141413` (Near Black) / `#5E5D59` (Olive) / `#87867F` (Stone)
- Brand: `#C96442` (Terracotta) / `#D97757` (Coral)
- Borders: `#F0EEE6` (soft) / `#E8E6DC` (warm) / `#30302E` (dark)
- Ring shadows: `#D1CFC5` (warm) / `#C2C0B6` (deep)
- Focus: `#3898EC` (only cool colour, accessibility only)

**Typography:**
- Headline: Anthropic Serif (Georgia fallback), weight 500 only
- Body / UI: Anthropic Sans (Inter / system-ui fallback), weights 400–500
- Code: Anthropic Mono (SFMono / Consolas fallback), weight 400
- Body line-height: 1.60 (literary cadence)
- Headline line-height: 1.10–1.30 (tight but breathing)
- Label letter-spacing: 0.12–0.5px on ≤12px text

**Layout:**
- Container max-width: 1200–1360px
- Section vertical: 96–120px
- Hero padding: 80–120px

For complete values, see the YAML frontmatter in `warm-editorial.design.md`.

## Signature Patterns

### Single-Weight Serif Headlines
Every serif headline uses weight 500 — no bold, no light, no italic. This produces the "one author wrote every heading" voice that defines the style. If a heading needs more weight, use larger size or darker colour, never heavier serif weight.

### Ring-Based Depth
Interactive states use ring shadows (`0 0 0 1px <warm-grey>`) instead of drop shadows. The pattern creates a border-like halo that's softer than an actual border. When drop shadows do appear, they're whisper-soft (`0 4px 24px rgba(0,0,0,0.05)`).

```css
.button-secondary {
  box-shadow: 0 0 0 1px #D1CFC5;
}
.button-primary {
  box-shadow: 0 0 0 1px #C96442;
}
.card-featured {
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.05);
}
```

### Light/Dark Section Alternation
The page alternates between Parchment (`#F5F4ED`) and Near Black (`#141413`) sections, creating chapter-like rhythm. This is the primary depth mechanism — entire sections shift elevation by changing the ambient light level. Dark sections use Ivory (`#FAF9F5`) headlines and Warm Silver (`#B0AEA5`) body text.

```html
<section class="parchment-section">…</section>
<section class="dark-section">…</section>
<section class="parchment-section">…</section>
```

### Asymmetric Button Padding
Workhorse buttons use asymmetric padding (`0px 12px 0px 8px`) when paired with leading icons — this is the icon-first signature. Standalone buttons use balanced padding (`8px 16px`).

### Warm Border Discipline
Borders are cream-tinted (`#F0EEE6` for whisper, `#E8E6DC` for emphasised). Never use generic light grey (`#E5E7EB`) or cool grey-blue borders — they break the warm chromatic spell.

## Image Guidelines

- **Style:** Organic, hand-drawn-feeling vector illustrations preferred — Claude-adjacent personality. Terracotta + black + muted green is the natural illustration palette.
- **Avoid:** Geometric/tech-style icons, isometric 3D, gradient meshes, generic SaaS hero illustrations.
- **Product screenshots:** Embed in 16–32px radius containers. Dark UI screenshots provide good contrast against the Parchment canvas.
- **Photography (if used):** Warm-toned, natural light, editorial framing. Avoid cold colour-graded stock.

## Responsive Behavior

- **Desktop (>991px):** Full layout, multi-column where applicable, max display type at 64px
- **Tablet (768–991px):** 2-column grids stable, condensed nav, display drops to ~48px
- **Mobile (<768px):** Single column, hamburger nav, display drops to 36px → 28px on small mobile
- **Section padding:** Reduces from 120px → 80px → 56px proportionally
- **Reading columns:** Stay capped at ~720px on all breakpoints; collapse to full width at <767px

## Customization

The two divergence axes most commonly used:

1. **Brand colour shift** — Replace Terracotta with another warm chromatic anchor (burnt sienna, ochre, deep rust, dusty rose). Keep the warm-toned discipline; never substitute a cool colour.
2. **Typography pairing** — Anthropic Serif + Anthropic Sans is the canonical pair. Acceptable substitutions: Source Serif 4 + Inter, Tiempos + Söhne, Bookerly + IBM Plex Sans. Never use a geometric serif (Bodoni, Didot) — they break the literary-warmth mood.

Optional axes:

3. **Radius tightening** — Drop from 12/16/32 to 8/12/24 for a slightly more technical-leaning feel.
4. **Section alternation reduction** — Some builds skip the light/dark alternation entirely and stay on Parchment throughout. This is valid but loses the chapter rhythm.

## Tier Placement vs Memoir, Editorial Portfolio, Sanctuary Tech

Warm Editorial overlaps with three other libraries; choose based on these distinctions:

- **vs Memoir Blog** — Memoir is reading-first blog/newsletter; Warm Editorial is product-page literary. Memoir uses Manrope (sans-only headlines), Warm Editorial uses serif headlines. Memoir is narrow-width reading; Warm Editorial is full product layout.
- **vs Editorial Portfolio** — Editorial Portfolio is gallery-first, image-led, sharp corners, compressed uppercase Inter. Warm Editorial is type-first, soft corners, mixed serif/sans. Editorial Portfolio is for portfolios; Warm Editorial is for products.
- **vs Sanctuary Tech** — Sanctuary is monospace-led for crisis/legal/healthcare; Warm Editorial is serif-led for AI/technical products. Both share warmth, but Sanctuary is muted-quiet, Warm Editorial is muted-warm with one chromatic accent.
