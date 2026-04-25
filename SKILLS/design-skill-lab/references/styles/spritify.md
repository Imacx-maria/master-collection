
# SPRITIFY Design System

A playful, family-friendly design system featuring bold typography, switchable color schemes, bento grid layouts, and cheerful UI components perfect for children's products and fun brands.

## Quick Start

Copy the template from `assets/template.html` as a starting point, then customize sections as needed.

## Composition Patterns — Bento or Uniform?

Spritify can use **either bento or uniform grid**. The choice is content-driven, not aesthetic-driven. See `references/layout-patterns.md` for the full decision tree.

**Use Bento (preferred for marketing-energy sections):**
- Feature highlights, "what we do", "who it's for"
- One item is the hero (visit page, sign up, play now)
- 4–6 items where hierarchy matters
- Spans: see `playful-bento.md` Bento Grammar — same vocabulary

**Use Uniform Grid (preferred for browse/scan sections):**
- Team members, equal-importance categories, schedule slots
- All items have equal weight
- Item count must be **divisible by column count** at every breakpoint (4 items → 4-col or 2-col; 6 items → 3-col or 2-col; 8 items → 4-col or 2-col)
- **Never `auto-fit minmax(...)` with arbitrary item counts** — produces orphans

**Use List / Stack:**
- Long-form content (testimonials, story pages)
- Sequential narrative (timeline of milestones)

**Failure mode that triggered this section being added:**
Defaulting to `auto-fit minmax(280px, 1fr)` for 6 cards. Result at 1200px viewport: 4-col grid with 2 cards alone in row 2. Visual misalignment with centred section header above. Always pick the column count deliberately.

## Display Typography & Hero Patterns

Spritify lives on bold, chunky typography that feels friendly rather than aggressive. League Spartan's heavy weights carry the playful identity.

**`display-xl` (112px, League Spartan 800)** — Hero moments where the brand voice needs maximum cheer. Use on home page heroes, "play now" intro pages, kids-app landing screens. One per page.

**`display-lg` (88px, League Spartan 800)** — Section openers ("Discover", "Features for Families"), secondary heroes inside sections, big "what's new" announcements. Carries cheerful weight without dominating.

**`headline-lg` (56px, League Spartan 700)** — Sub-section titles, card group headers, feature names. Heavy weight maintains the chunky feel.

**Hero patterns by page type:**

- **Home / kids landing** — `display-xl` headline (often switches color scheme on hover or scroll for variety), oversized illustration alongside, `button-accent` (pink) primary CTA. Use `4xl` (72px) vertical padding inside the hero.
- **Feature / category page** — `display-lg` page title, then accent-bordered cards (`accent-border-card`) for category tiles. Switch background color scheme between sections for visual variety.
- **Product / story page** — `display-lg` story title, generous illustration or photography, `body-md` description below. Hover micro-bounces on every interactive element.
- **About / family page** — `headline-lg` for "Made for families" type statements (skip display — keep grandma-friendly readability).

**Spacing for chunky tactility:**

- Hero sections: `4xl` (72px) or `5xl` (112px) vertical padding — generous and inviting
- Between sections: `4xl` (72px) for the cheerful breathing room
- Card grids: `xl` (32px) gap minimum — cards should feel like distinct toys, not crammed shelves
- Inside cards: `pad-card` (32px) — chunky padding maintains the tactile playfulness
- Button padding: `md` (16px) — combined with full-pill radius for the chunky-friendly look
- Color-scheme switches: change at `4xl` section boundaries, never mid-section

**Color-scheme + display interaction:**

When using switchable schemes (default → soft → bold), the display headline can shift color along with the background. This is part of the playful identity — but never switch within a single hero section. One scheme per top-level section.

## Design Tokens

See `references/design-tokens.md` for complete color schemes, typography, and spacing values.

### Color Schemes (Switchable)

Three schemes controlled via `data-scheme` attribute on `<html>`:

| Scheme | Primary | Secondary | Tertiary | Use Case |
|--------|---------|-----------|----------|----------|
| 1 | `#82eda6` (green) | `#ffff94` (yellow) | `#82eda6` | Default, energetic |
| 2 | `#f6bbfd` (pink) | `#f9f8f4` (off-white) | `#03594d` (dark) | Soft, friendly |
| 3 | `#82eda6` (green) | `#03594d` (dark) | `#f9f8f4` (off-white) | Bold, contrast |

### Typography

- **Headlines**: League Spartan 700/800, uppercase, tight tracking
- **Body**: Inter 400/500/700
- **Sizes**: clamp() for responsive scaling (48px → 110px for hero)

## Core Components

### Bento Grid

4-column grid with spanning options:

```css
.bento-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}
.bento-wide { grid-column: span 2; }
.bento-tall { grid-row: span 2; }
.bento-large { grid-column: span 2; grid-row: span 2; }
```

**Rule**: Bento grids must be balanced. Cards should span cells to create visual interest while maintaining alignment.

### Buttons

All buttons have:
- 2px solid border (`--green-dark`)
- 100px border-radius (pill shape)
- Box shadow offset (-4px 4px)
- Hover: translateY(-2px)

Variants:
- `.btn-primary`: Dark bg, light text, light shadow
- `.btn-secondary`: Light bg, dark text, dark shadow  
- `.btn-ghost`: Transparent bg, dark border/text, dark shadow
- `.btn-accent`: Pink bg, dark text

### Cards

Standard card pattern:
```css
.card {
    background: var(--off-white);
    border: 2px solid var(--green-dark);
    border-radius: 24px;
    padding: 28px;
}
```

### Contact Drawer

Slide-in drawer from right with:
- Overlay (50% opacity dark)
- Header section (off-white, rounded bottom)
- Body section (cyan background)
- Form with underline inputs
- Close on Escape key

### FAQ Accordion

- Container with accent color left border (6px)
- Single-open behavior
- Plus icon rotates to X when active
- Smooth max-height transition

## Logo

SVG ghost/sprite shape — use inline with `fill="var(--green-dark)"`:

```html
<svg viewBox="0 0 256 256" fill="none">
    <path d="M 128.945 0 C 199.203 0.508 256 57.617 256 127.994..." fill="currentColor"/>
</svg>
```

Full path in `assets/logo.svg`.

## Responsive Breakpoints

- Desktop: 4-column bento, full layouts
- Tablet (900px): 2-column bento
- Mobile (600px): 1-column, stacked layouts

## Implementation Checklist

1. Load Google Fonts: League Spartan (700, 800) + Inter (400, 500, 700)
2. Set CSS variables for color scheme
3. Add `data-scheme="1"` to `<html>` for scheme switching
4. Use bento grid for content sections
5. Apply consistent border-radius (24px cards, 100px buttons)
6. Add hover states with translateY and shadow changes

---

## Design Tokens (Complete Reference)

# SPRITIFY Design Tokens

## Color Palette

### Core Colors

```css
--green-light: #82eda6;
--green-dark: #03594d;
--yellow: #ffff94;
--pink: #f6bbfd;
--off-white: #f9f8f4;
--cyan: #aefbff;
--border-soft: rgba(3, 89, 77, 0.2);
```

### Scheme Variables

```css
/* Scheme 1: Green + Yellow (Default) */
[data-scheme="1"] {
    --bg-primary: #82eda6;
    --bg-secondary: #ffff94;
    --bg-tertiary: #82eda6;
    --accent: #ffff94;
}

/* Scheme 2: Pink + Off-white + Dark */
[data-scheme="2"] {
    --bg-primary: #f6bbfd;
    --bg-secondary: #f9f8f4;
    --bg-tertiary: #03594d;
    --accent: #f6bbfd;
}

/* Scheme 3: Green + Dark + Off-white */
[data-scheme="3"] {
    --bg-primary: #82eda6;
    --bg-secondary: #03594d;
    --bg-tertiary: #f9f8f4;
    --accent: #82eda6;
}
```

## Typography

### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=League+Spartan:wght@700;800&display=swap" rel="stylesheet">
```

### Font Families

```css
/* Headlines */
font-family: 'League Spartan', sans-serif;
font-weight: 800;
text-transform: uppercase;
letter-spacing: -0.02em;

/* Body */
font-family: 'Inter', sans-serif;
font-weight: 400;
```

### Font Sizes

| Element | Size | Line Height |
|---------|------|-------------|
| Hero H1 | clamp(48px, 10vw, 110px) | 0.9 |
| Section H2 | clamp(36px, 7vw, 72px) | 0.95 |
| Bento Title | 28px (42px for large) | 1 |
| Body | 14-15px | 1.5-1.6 |
| Tag/Label | 11-14px | 1 |

## Spacing

### Section Padding

```css
/* Desktop */
padding: 80px 24px;

/* Mobile */
padding: 60px 16px;
```

### Grid Gap

```css
gap: 16px; /* Bento grid */
gap: 20px; /* Card grids */
```

### Card Padding

```css
padding: 28px; /* Standard bento card */
padding: 20px; /* Style cards */
```

## Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 100px |
| Cards | 24px |
| Hero visual | 60px (top) |
| Input fields | 12px |
| Small elements | 12px |

## Shadows

### Button Shadows

```css
/* Normal */
box-shadow: -4px 4px 0 var(--green-light); /* Primary */
box-shadow: -4px 4px 0 var(--green-dark);  /* Secondary/Ghost */

/* Hover */
box-shadow: -6px 6px 0 rgba(3, 89, 77, 0.4);
```

### Card Shadows

```css
/* Hover state */
box-shadow: 0 12px 32px rgba(3, 89, 77, 0.12);
```

## Transitions

```css
/* Standard */
transition: transform 0.3s, box-shadow 0.3s;

/* Background color (scheme switch) */
transition: background 0.4s ease;

/* Drawer */
transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
```

## Z-Index Scale

| Element | Z-Index |
|---------|---------|
| Navigation | 100 |
| Sticky CTA | 90 |
| Drawer overlay | 200 |
| Drawer | 201 |

## Breakpoints

```css
/* Tablet */
@media (max-width: 900px) { }

/* Mobile */
@media (max-width: 768px) { }

/* Small mobile */
@media (max-width: 600px) { }
```

## Templates

HTML starter templates: template.html 
Source: `/mnt/skills/user/spritify-design/assets/`
