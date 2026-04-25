
# Playful Bento Design System

A structure-first design system featuring bold typography, vibrant color palette, and hierarchy-aware bento grids. Domain-flexible — adapts to any product while maintaining visual discipline.

## Philosophy

This system prioritizes:
1. **Hierarchy over decoration** — Not all cards are equal. Anchor > Outputs > Stats > Tagline.
2. **Structure over content** — Fill slots, don't write prose.
3. **Domain neutrality** — Base template is emoji-free, placeholder-driven.
4. **Intentional asymmetry** — Cards of different importance look different.

## Quick Start

Copy `assets/template.html` as starting point. The template is domain-neutral with placeholder content.

## Bento Grammar (the structural contract)

Bento is **not** a visual treatment — it's a composition system. See `references/layout-patterns.md` for the full grammar. Summary for this style:

**The grid:** 12 columns on desktop, fixed-row-height (`grid-auto-rows: 200px` or similar), gap = `var(--gutter)` = 16px.

**The span vocabulary you must use:**

| Card role     | Span (cols × rows) | Notes |
|---------------|--------------------|-------|
| Hero          | 6 × 2              | One per bento. Holds the page anchor. |
| Wide          | 6 × 1              | Pairs with hero or another wide. |
| Tall          | 3 × 2              | Vertical accent — single stat or quote. |
| Square        | 3 × 1              | Workhorse small card. |
| Full          | 12 × 1             | Closing or opening band inside bento. |
| Two-thirds    | 8 × 1              | Asymmetric anchor (alt to hero). |
| One-third     | 4 × 1              | Pairs with two-thirds (8 + 4 = 12). |

**Patterns by item count (pick one, don't invent):**

- **3 items** — `[hero 6×2] [wide 6×1] [wide 6×1]`
- **4 items** — `[hero 6×2] [wide 6×1] [3×1] [3×1]`
- **5 items** — `[hero 6×2] [wide 6×1] [3×1] [3×1] [12×1 full closer]`
- **6 items** — `[hero 6×2] [wide 6×1] [3×1] [tall 3×2] [wide 6×1] [12×1 full closer]`
- **7+ items** — split into two bento sections; don't cram

**Validation rules (run before declaring done):**

1. **Sum spans correctly** — `Σ (cols × rows) == 12 × max_row`. If your numbers don't add to a multiple of 12, you have visual gaps.
2. **One Hero max** — multiple 6×2 cells = no hero, just two fighting cards.
3. **At least 2 distinct span sizes** — all-`span 4` or all-`span 6` is a uniform grid, not bento.
4. **Largest span = most important content** — hero card holds the page anchor, not a footnote.
5. **Mobile fallback collapses to single column** — never to 2-col uniform grid (creates orphans).

**Anti-pattern — uniform grid in disguise:**
```
6 cards, each at "grid-column: span 4" on a 12-col grid
```
That's a 3-col uniform grid. If you want bento, vary the spans intentionally per the table above.

## Display Typography & Hero Patterns

Bento grids need display drama in the anchor cell to establish hierarchy. Without it, every cell reads equal — and the bento becomes just a grid.

**`display-xl` (128px, Inter 800)** — The anchor cell's hero text or the page-level masthead. Inter 800 with tight tracking (-0.05em) for compressed energy. One per page.

**`display-lg` (96px, Inter 800)** — Secondary anchor cells, section openers ("Our Process", "Features"), or the home page hero if the bento is below the fold. Aggressive but contained.

**`headline-xl` (80px, Inter 800)** — Medium bento cell headlines, feature anchors, statement moments inside cards.

**`headline-lg` (48px)** — Standard bento cell titles, section sub-headers.

**Hero patterns by page type:**

- **Marketing landing** — Hero band ABOVE the bento grid, with `display-xl` headline + body description + primary CTA. Below: bento grid with one cell using `headline-xl` as the in-grid anchor. `4xl` (96px) hero padding.
- **Bento-only home** — Skip the hero band. The largest bento cell IS the hero, using `display-lg` headline directly inside it. Grid takes full viewport. `2xl` (40px) gutter between cells.
- **Product / feature page** — `display-lg` page anchor at top, then mid-page bento for proof points (3-4 cells), then full-width content sections.
- **Pricing / comparison** — `headline-xl` for tier names inside cards. Skip display — pricing comparisons need clarity, not drama.

**Spacing for bento rhythm:**

- Hero band (when present): `4xl` (96px) vertical padding
- Bento section: `4xl` top/bottom padding from page edges or surrounding sections
- Bento gutter (between cells): `gutter` (16px) — never wider, breaks the bento feel
- Cell padding: `xl` (32px) for large/medium cells, `pad-cell-sm` (20px) for small cells, `pad-cell-accent` (32px) for accent cells
- Between bento section and next content: `5xl` (128px) for clear separation
- Card grids inside content (not bento): `2xl` (40px) gap

## Core Rules

### Bento Hierarchy (Non-Negotiable)

Cards have visual weight. Never make all cards equal.

| Card Type | Role | Visual Treatment |
|-----------|------|------------------|
| **Anchor** | Core concept | Largest (2×2), dark bg, big title |
| **Environment** | Output as PLACE | Tall, edge-to-edge visual, minimal caption |
| **Object** | Output as IDENTITY | Wide, horizontal, trading-card framing |
| **Stat** | Utility metric | Small, single-purpose, number-forward |
| **Tagline** | Positioning | Full-width, poster-like, minimal padding |

See `references/bento-hierarchy.md` for detailed card specifications.

### Content Slots

Claude fills structured slots, not prose. Each slot has constraints.

| Slot | Max Length | Rules |
|------|------------|-------|
| Anchor headline | 6 words | Concept-level, no metaphors |
| Anchor body | 1 sentence | Clarifies the concept |
| Output name | 2-3 words | Artifact name, not feature |
| Output description | 1 sentence | What it IS, not what it DOES |
| Stat value | Number or short | No fake metrics unless told |
| Stat label | 2 words max | No fluff |
| Tagline | "Not X. Y." | Declarative principle |

See `references/content-slots.md` for slot map and examples.

### Visual Placeholders (No Emojis by Default)

Base template uses abstract placeholders:
- Empty frames with aspect-ratio
- Grid textures
- Abstract shapes (blocks, bars)
- Numbers and labels only

Emojis allowed ONLY when:
- Tone = `playful` AND domain supports it
- User explicitly requests them
- Used in demo/preview contexts

### Tone Parameter

Accept tone input. Adjust copy style accordingly:

| Tone | Characteristics |
|------|-----------------|
| `neutral` (default) | Confident, minimal, no jokes |
| `bold` | Declarative, punchy, short |
| `friendly` | Warm, approachable, second-person |
| `playful` | Emojis allowed, casual, fun |
| `premium` | Refined, sparse, understated |

## Design Tokens

See `references/design-tokens.md` for complete specifications.

### Color Palette

The system uses a vibrant, consistent color palette organized into three categories:

**Primary Colors:**
- **Primary Green**: `#82eda6` - Main brand color, CTAs, backgrounds
- **Dark Green**: `#03594d` - Text, borders, shadows

**Accent Colors:**
- **Pink**: `#f6bbfd` - Accent buttons, highlights
- **Rose**: `#fccddc` - Card backgrounds
- **Hot Pink**: `#fc5681` - Bold accents
- **Orange**: `#fdc068` - Warm accents
- **Bright Orange**: `#ff9124` - High-energy CTAs
- **Cyan**: `#aefbff` - Fresh accents
- **Blue**: `#589af0` - Links, interactive elements
- **Purple**: `#c88cfd` - Accent highlights
- **Yellow**: `#ffff94` - High-visibility CTAs
- **Lime**: `#d8e268` - Bright accents

**Neutral Colors:**
- **Off-white**: `#f9f8f4` - Page backgrounds
- **Sage**: `#89a9a1` - Muted accents

### Typography

- **Headlines**: Fredoka 500/600/700 (Google Fonts), uppercase
- **Body**: Inter 400/500/600 (Google Fonts)
- **Letter-spacing**: Add 0.5px (0.04-0.08em) to ALL uppercase text

### Key Measurements

- Border width: 1px solid
- Border radius: 20px cards, 60px feature cards, 100px buttons
- Shadows: -3px 3px offset default (brutalist style)
- Grid gap: 16px
- Card padding: 28px standard, 32px anchor

## Constraints (What Claude Must NOT Do)

1. Never make all cards equal importance
2. Never use emojis in base template (neutral tone)
3. Never invent fake metrics unless instructed
4. Never use metaphors by default
5. Never flatten hierarchy
6. Never center all content vertically
7. Never rely on headings alone to explain purpose
8. Never write prose where slots expect structured input

## Responsive Behavior

- Desktop (≥1440px): 4-column grid
- Tablet (810px-1439px): 2-column, anchor spans full
- Mobile (<810px): 1-column, stacked

## Implementation Checklist

1. Copy `assets/template.html`
2. Load fonts: Fredoka (400, 500, 600, 700) + Inter (400, 500, 600) from Google Fonts
3. Fill content slots per `references/content-slots.md`
4. Verify hierarchy: anchor dominates, outputs differ, stats are small
5. Add letter-spacing (0.5px) to ALL uppercase text
6. Use 1px borders throughout
7. Apply correct shadow values (-3px 3px default)

---

## Design Tokens (Complete Reference)

# Design Tokens Reference

## Color Palette

### Primary Colors

```css
/* Primary Green - Main brand color, used for backgrounds and CTAs */
--color-primary: #82eda6;
--green-light: #82eda6; /* Alias */

/* Primary Dark Green - Text color, borders, shadows */
--color-text-primary: #03594d;
--green-dark: #03594d; /* Alias */
```

### Accent Colors

```css
/* Pink - Accent color for buttons, highlights */
--color-pink: #f6bbfd;
--pink: #f6bbfd; /* Alias */

/* Rose Pink - Cards, section backgrounds */
--color-rose: #fccddc;
--rose: #fccddc; /* Alias */

/* Hot Pink - Highlights, accents */
--color-hot-pink: #fc5681;
--hot-pink: #fc5681; /* Alias */

/* Orange - Buttons, interactive elements */
--color-orange: #fdc068;
--orange: #fdc068; /* Alias */

/* Bright Orange - CTAs, highlights */
--color-orange-bright: #ff9124;
--orange-bright: #ff9124; /* Alias */

/* Cyan - Section backgrounds, accents */
--color-cyan: #aefbff;
--cyan: #aefbff; /* Alias */

/* Blue - Links, interactive elements */
--color-blue: #589af0;
--blue: #589af0; /* Alias */

/* Purple - Accent highlights */
--color-purple: #c88cfd;
--purple: #c88cfd; /* Alias */

/* Yellow - Buttons, highlights */
--color-yellow: #ffff94;
--yellow: #ffff94; /* Alias */

/* Lime Green - Accents */
--color-lime: #d8e268;
--lime: #d8e268; /* Alias */
```

### Neutral Colors

```css
/* Off White - Page backgrounds */
--color-background: #f9f8f4;
--off-white: #f9f8f4; /* Alias */

/* Sage Green - Muted accents */
--color-sage: #89a9a1;
--sage: #89a9a1; /* Alias */

/* Dark Green Transparent - Overlays */
--color-overlay: rgba(2, 89, 77, 0.2);
--border-soft: rgba(3, 89, 77, 0.2); /* Alias */
```

## Typography

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

### Font Families

```css
/* Headlines */
font-family: 'Fredoka', sans-serif;
font-weight: 600;
text-transform: uppercase;

/* Body */
font-family: 'Inter', sans-serif;
font-weight: 400;
```

### Font Scale (Consolidated)

Only these sizes. No 11px, 13px, 15px, 17px.

| Token | Size | Use |
|-------|------|-----|
| `--text-xs` | 12px | Tags, labels, captions |
| `--text-sm` | 14px | Body text, buttons |
| `--text-base` | 16px | Primary body, inputs |
| `--text-lg` | 20px | Subheadings |
| `--text-xl` | 28px | Bento titles |
| `--text-2xl` | 48px | Anchor title |
| `--text-hero` | clamp(48px, 10vw, 110px) | Hero H1 |
| `--text-section` | clamp(36px, 7vw, 72px) | Section H2 |

### Letter Spacing (Required for Uppercase)

ALL uppercase text needs letter-spacing:

| Element | Spacing |
|---------|---------|
| Buttons | 0.04em |
| Tags/Labels | 0.06–0.08em |
| Headlines | -0.02em to 0.03em |
| Stat labels | 0.05–0.06em |

```css
.btn { letter-spacing: 0.04em; }
.bento-tag { letter-spacing: 0.08em; }
.bento-title { letter-spacing: 0.03em; }
```

## Spacing

### Section Padding

```css
/* Desktop */
.section { padding: 80px 24px; }

/* Tablet */
@media (min-width: 810px) and (max-width: 1439.98px) {
    .section { padding: 60px 20px; }
}

/* Mobile */
@media (max-width: 809.98px) {
    .section { padding: 48px 16px; }
}
```

### Grid Gap

```css
.bento-grid { gap: 16px; }
.card-grid { gap: 20px; }
```

### Card Padding

| Card Type | Padding |
|-----------|---------|
| Standard bento | 28px |
| Anchor | 32px |
| Stat cards | 20px |
| Object (no padding) | 0 |
| Environment (no padding) | 0 |

## Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 100px (pill) |
| Cards | 20px |
| Feature Cards | 60px |
| Hero visual | 60px (top corners) |
| Inputs | 12px |
| Small elements | 10px |
| Large elements | 40px |
| Portrait frames | 8px |

## Shadows

### Brutalist Offset Shadows

```css
/* Small (default) */
box-shadow: -3px 3px 0px 0px var(--green-dark);

/* Medium */
box-shadow: -4px 4px 0px 0px var(--green-dark);

/* Large */
box-shadow: -5px 6px 0px 0px var(--green-dark);

/* Hover state */
box-shadow: -5px 5px 0px 0px var(--green-dark);
```

### Layered Shadow (Premium Effect)

```css
box-shadow:
    -0.3px 0.36px 0px 0px rgba(4, 88, 78, 0.06),
    -1.14px 1.37px 0px 0px rgba(4, 88, 78, 0.23),
    -5px 6px 0px 0px rgb(4, 88, 78);
```

### Soft Shadows

```css
/* Card hover */
box-shadow: 0 12px 32px rgba(3, 89, 77, 0.12);

/* Sticky CTA */
box-shadow: 0 -4px 20px rgba(3, 89, 77, 0.12);
```

## Transitions

```css
/* Standard interactions */
transition: transform 0.2s, box-shadow 0.2s;

/* Background */
transition: background 0.4s ease;

/* Drawer slide */
transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);

/* FAQ accordion */
transition: max-height 0.3s ease;

/* FAQ icon */
transition: transform 0.25s ease;
```

## Z-Index Scale

| Element | Z-Index |
|---------|---------|
| Navigation | 100 |
| Sticky CTA | 90 |
| Drawer overlay | 200 |
| Drawer panel | 201 |

## Breakpoints

```css
/* Tablet */
@media (min-width: 810px) and (max-width: 1439.98px) {
    /* 2-column bento, adjusted nav, hero */
}

/* Mobile */
@media (max-width: 809.98px) {
    /* 1-column, stacked */
}

/* Desktop */
@media (min-width: 1440px) {
    /* Full layout */
}
```

## Component Patterns

### Button Base

```css
.btn {
    border: 1px solid var(--green-dark);
    padding: 14px 28px;
    border-radius: 100px;
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: -3px 3px 0px 0px var(--green-dark);
}

.btn:hover {
    transform: translate(2px, -2px);
    box-shadow: -5px 5px 0px 0px var(--green-dark);
}
```

### Card Base

```css
.bento-card {
    background: var(--off-white);
    border: 1px solid var(--green-dark);
    border-radius: 20px;
    padding: 28px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: -4px 4px 0px 0px var(--green-dark);
}

.bento-card:hover {
    transform: translate(2px, -2px);
    box-shadow: -6px 6px 0px 0px var(--green-dark);
}
```

### Dark Card Variant

```css
.bento-card.dark {
    background: var(--green-dark);
    color: var(--off-white);
}
```

---

# Bento Hierarchy Reference

## Visual Weight Scale

Cards are NOT equal. This is the hierarchy:

```
ANCHOR (weight: 5)
    ↓
ENVIRONMENT / OBJECT (weight: 3)
    ↓
STATS (weight: 1)
    ↓
TAGLINE (weight: 2, but positioned last)
```

## Card Specifications

### Anchor Card

**Role**: The core concept. This is what the product IS.

**Grid Position**: Top-left, spans 2 columns × 2 rows

**Visual Rules**:
- Dark background (`--green-dark`)
- Light text (`--off-white`)
- Title: 48px, uppercase, Fredoka 600
- Body: 16px, single sentence, 0.7 opacity
- Logo/visual: Centered, 140px, abstract shape
- Padding: 32px

**Must Feel**: Dominant, foundational, unmissable

```css
.bento-anchor {
    grid-column: 1 / 3;
    grid-row: 1 / 3;
    padding: 32px;
    background: var(--green-dark);
    color: var(--off-white);
}
```

### Environment Card (Output as PLACE)

**Role**: One of two outputs. Represents a context/world/scene.

**Grid Position**: Right side, spans 2 columns × 2 rows (parallel to anchor)

**Visual Rules**:
- NO padding — edge-to-edge visual
- Abstract layered environment (terrain shapes)
- Focal point placeholder (abstract figure)
- Caption bar at bottom: "Output A" + tag
- Minimal text — caption level only

**Must Feel**: Like a window into a world. Immersive. Not a feature card.

```css
.bento-environment {
    grid-column: 3 / 5;
    grid-row: 1 / 3;
    padding: 0;
    overflow: hidden;
    min-height: 340px;
}
```

**Internal Structure**:
```
┌─────────────────────────┐
│                         │
│   [abstract layers]     │
│                         │
│      [focal point]      │
│                         │
├─────────────────────────┤
│ Output A      [tag]     │  ← caption bar
└─────────────────────────┘
```

### Object Card (Output as IDENTITY)

**Role**: One of two outputs. Represents an owned artifact/collectible.

**Grid Position**: Full-width, below stats row

**Visual Rules**:
- Horizontal trading-card layout
- Three-column internal structure: portrait | info | stats
- Strong internal framing with borders
- Portrait zone: accent background
- Stats zone: data visualization (bars)

**Must Feel**: Like something you OWN. A collectible. Framed.

```css
.bento-object {
    grid-column: 1 / -1;
    padding: 0;
    overflow: hidden;
}

.object-card {
    display: grid;
    grid-template-columns: 140px 1fr 180px;
    min-height: 160px;
}
```

**Internal Structure**:
```
┌──────────┬─────────────┬──────────┐
│          │             │ ATTR ▓▓▓ │
│ [portrait]│ Output B    │ ATTR ▓▓  │
│          │ Subtype     │ ATTR ▓▓▓▓│
│          │ #000001     │ ATTR ▓▓▓ │
└──────────┴─────────────┴──────────┘
```

### Stat Cards

**Role**: Utility metrics. Quick facts.

**Grid Position**: Row 3, one cell each

**Visual Rules**:
- Single purpose — one number, one label
- Number: 42px, Fredoka 600
- Label: 12px, uppercase, 0.6 opacity
- Centered content
- Optional accent background (yellow, off-white)

**Must Feel**: Glanceable. Data-forward. No prose.

```css
.bento-stat-1, .bento-stat-2, .bento-stat-3 {
    padding: 20px;
    justify-content: center;
    text-align: center;
}
```

### Preview Card

**Role**: Abstract visual placeholder for grid/options.

**Grid Position**: Row 3, rightmost cell

**Visual Rules**:
- 2×2 grid of abstract cells
- Varying opacity (0.15–0.3)
- No content — pure placeholder

### Tagline Card

**Role**: Positioning statement. Philosophy.

**Grid Position**: Full-width, bottom row

**Visual Rules**:
- Dark background
- Centered text
- Title: clamp(32px, 5vw, 52px), uppercase
- Optional tag above ("Principle")
- Minimal padding — poster-like

**Must Feel**: Declarative. Confident. Final word.

```css
.bento-tagline {
    grid-column: 1 / -1;
    padding: 32px 40px;
    text-align: center;
    background: var(--green-dark);
}
```

## Grid Template

```
┌─────────────────┬─────────────────┐
│                 │                 │
│  ANCHOR (2×2)   │  ENVIRONMENT    │
│                 │  (2×2)          │
│                 │                 │
├────┬────┬────┬──┴─────────────────┤
│stat│stat│stat│ preview           │
├────┴────┴────┴────────────────────┤
│  OBJECT (full width)              │
├───────────────────────────────────┤
│  TAGLINE (full width)             │
└───────────────────────────────────┘
```

## Relationship Rules

### Environment vs Object

These cards MUST differ:

| Aspect | Environment | Object |
|--------|-------------|--------|
| Orientation | Vertical (tall) | Horizontal (wide) |
| Borders | None (edge-to-edge) | Strong internal framing |
| Content | Visual-dominant | Data-structured |
| Feel | Immersive (you're IN it) | Owned (you HAVE it) |

### Hierarchy Enforcement

At a glance, without reading:
- Anchor must dominate
- Environment and Object must be visually distinct types
- Stats must be small and subordinate
- Tagline must feel like a conclusion

**If all cards look equally important, the hierarchy failed.**

---

# Content Slots Reference

Claude fills structured slots, not prose. This document defines each slot.

## Slot Map

### Hero Section

| Slot | Input Required | Output | Constraints |
|------|----------------|--------|-------------|
| `hero.tagline` | Product description | ≤10 words | Positioning hook |
| `hero.headline` | Value proposition | ≤8 words | Value-forward, not clever |
| `hero.subheadline` | Use case | 1 sentence | Clarifies who/what |

**Example**:
```
Input: "AI tool that turns selfies into pixel art game characters"
Output:
  tagline: "You don't just become a character. You spawn into a world."
  headline: "Turn Photos Into Pixel Art"
  subheadline: "Upload a selfie. Get two game-ready artworks in 30 seconds."
```

### What You Get Section (Primary Bento)

#### Slot A: Anchor Card

| Field | Constraint | Example |
|-------|------------|---------|
| `anchor.tag` | 2 words | "The Concept" |
| `anchor.headline` | ≤6 words, no metaphors | "Two Outputs. One System." |
| `anchor.body` | 1 sentence | "One input. Two artifacts." |

**Rules**:
- Must communicate the CORE idea
- No feature lists
- No adjective stacks

#### Slot B: Environment Card

| Field | Constraint | Example |
|-------|------------|---------|
| `environment.label` | "Output A" or similar | "Output A" |
| `environment.tag` | 1 word | "Environment" |

**Rules**:
- Text is caption-level only
- Visual does the talking
- No descriptions of what it DOES

#### Slot C: Object Card

| Field | Constraint | Example |
|-------|------------|---------|
| `object.name` | 2-3 words | "Output B" |
| `object.class` | 2 words | "Identity Component" |
| `object.id` | Format: #XXXXXX | "#000001" |
| `object.stats` | 3-4 attributes | ATTR: 75, ATTR: 90, etc. |

**Rules**:
- Feels like a collectible
- Data-structured, not prose
- Stats are abstract unless domain-specific

#### Slot D: Stat Cards (×3)

| Field | Constraint | Example |
|-------|------------|---------|
| `stat.value` | Number or "—" | "6", "30s", "—" |
| `stat.label` | ≤2 words | "Outputs", "Metric" |

**Rules**:
- No fake metrics unless instructed
- Zero fluff
- Placeholder "—" if unknown

#### Slot E: Preview Card

No content. Abstract 2×2 grid placeholder.

#### Slot F: Tagline Card

| Field | Constraint | Example |
|-------|------------|---------|
| `tagline.tag` | 1 word | "Principle" |
| `tagline.statement` | "Not X. Y." structure | "Not Realism. Style." |

**Rules**:
- Declarative, not descriptive
- Sounds like a principle
- No adjective stacks

### How It Works Section

#### Step Cards

| Field | Constraint | Example |
|-------|------------|---------|
| `step.number` | "01", "02", "03" | "01" |
| `step.label` | ≤3 words | "Upload Photo" |
| `step.body` | 1 sentence | "Drop a file. We handle the rest." |

### FAQ Section

| Field | Constraint | Example |
|-------|------------|---------|
| `faq.question` | Natural question | "How long does it take?" |
| `faq.answer` | 2-3 sentences max | Concise answer |

## Tone Adjustments

### Neutral (Default)
```
headline: "Transform Your Input"
body: "One submission. Two outputs."
tagline: "Not X. Y."
```

### Bold
```
headline: "Your Input. Transformed."
body: "Submit once. Get two."
tagline: "X is dead. Y wins."
```

### Friendly
```
headline: "Turn Your Input Into Something New"
body: "Just upload once — you'll get two outputs back."
tagline: "We believe in Y, not X."
```

### Playful
```
headline: "Your Input → Pure Magic ✨"
body: "Drop it in, get two goodies out!"
tagline: "Forget X. We're all about Y 🎮"
```

### Premium
```
headline: "Refined Output"
body: "One input. Two artifacts."
tagline: "Not X. Y."
```

## Anti-Patterns

### Don't Write Prose
❌ "Our innovative platform leverages cutting-edge AI technology to transform your ordinary photos into extraordinary pixel art masterpieces that capture the essence of classic gaming aesthetics."

✅ "Upload a photo. Get pixel art."

### Don't Stack Adjectives
❌ "Amazing, beautiful, stunning, incredible outputs"

✅ "Two outputs"

### Don't Use Metaphors (Unless Playful Tone)
❌ "Unlock the power of your imagination"

✅ "Create two artworks"

### Don't Flatten Hierarchy
❌ All slots get 2-3 sentences

✅ Anchor: 1 sentence. Stats: 2 words. Tagline: 4 words.

---

## Additional References (Load on Demand)

For detailed component code: read `references/styles/playful-bento-components.md`
For animation patterns: read `references/styles/playful-bento-animations.md`

## Templates

HTML starter templates: cta-section.html template.html stats-section.html nav.html cards.html hero-section.html about-section.html 
Source: `/mnt/skills/user/playful-bento/assets/`
