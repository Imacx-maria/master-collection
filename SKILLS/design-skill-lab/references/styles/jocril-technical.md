
# Jocril Frontend Design

This skill guides creation of frontend interfaces inspired by Jocril's design system - a refined, technical aesthetic that emphasizes clarity, precision, and thoughtful interaction design.

## Display Typography & Hero Patterns

Jocril is built on dramatic typographic scaling. The display tokens are not optional decoration — they are the system's core voice.

**`display-xl` (160px, Geist Sans 700)** — The product's defining moment. Landing page hero, version-launch page, the "what we do" statement. One per page maximum. Letter-spacing tight (-0.03em) for engineered crispness.

**`display-lg` (112px, Geist Sans 700)** — Major section anchors (Pricing, Features, Changelog headlines), secondary hero moments. Carries weight without claiming the page-defining slot.

**`headline-xl` (96px, Geist Sans 650)** — Product feature titles, pricing tier names, blog post titles. The workhorse for content with presence.

**`headline-lg` (70px)** — Sub-section titles, dashboard view headers, modal anchors.

**Hero patterns by page type:**

- **Landing page hero** — `display-xl` headline anchored left or asymmetric, mono `label-md` eyebrow above ("v1.0 RELEASED" or category tag), `body-md` description below. Use `5xl` (128px) vertical padding inside the hero. Teal accent only on the CTA button.
- **Pricing page** — `display-lg` page anchor ("Pricing"), then `headline-xl` per tier name. Cards use `card-default` with `xl` (32px) padding, `2xl` (48px) gap between tiers.
- **Feature deep-dive** — `display-lg` for the feature name, then `headline-lg` for sub-features. Code samples in mono inline with body.
- **Changelog / docs** — Skip display. `headline-xl` for entry titles, `headline-lg` for sub-versions. Mono badges for version numbers.

**Spacing for technical clarity:**

- Hero sections: `5xl` (128px) vertical padding to give the display type its room
- Section dividers: `4xl` (96px) between major sections — never less, breaks the calm
- Inside cards: `xl` (32px) padding for generous information-density
- Card grids (pricing, features): `2xl` (48px) gap minimum
- Inline metric strips: `lg` (24px) horizontal gap between metric clusters
- The signature dashed dividers should sit at `lg` margins from adjacent content

## Core Aesthetic Principles

**Typography-First Design**
- Geist Sans for primary UI (NOT Inter, Roboto, or system fonts)
- Geist Mono for labels, metadata, code references
- Aggressive size scaling: 70px → 160px for heroes, not timid 1.5x jumps
- Monospaced labels: uppercase, tight tracking (−0.0175rem)

**Color Philosophy**
- **Teal accent system** (#2DD4CD, #16B7B2, #00DED7) - NOT purple gradients
- Dark/light theme support via CSS custom properties
- Neutral grays as foundation (--color-base-100 → --color-base-1000)
- High contrast for accessibility

**Structural Vocabulary**
- Dashed borders (`border: 1px dashed`) for cards and frames
- Accent dots (::before pseudo-elements) for section badges
- Design tokens for all spacing, radii, colors, transitions
- CSS custom properties (`--spacing`, `--radius-xs`, `--color-*`)

**Interaction Patterns**
- Focus outlines in accent colors (not browser default blue)
- 44px minimum touch targets on mobile
- Hover states that invert text/background
- GSAP for scroll-driven animations (not CSS keyframes for complex sequences)
- Transition disabling during theme switches to prevent flicker

## Implementation Guidelines

### Always Use Design Tokens

```css
:root {
  /* Spacing */
  --spacing: 0.25rem;
  
  /* Colors */
  --accent-100: #2DD4CD;
  --accent-200: #16B7B2;
  --accent-300: #00DED7;
  
  /* Radii */
  --radius-xs: 2px;
  --radius-sm: 4px;
  --radius-md: 8px;
  
  /* Transitions */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --default-transition-duration: 200ms;
}
```

### Typography Scale

```css
/* Hero headlines */
.heading-1 {
  font-family: var(--font-geist-sans);
  font-size: clamp(70px, 10vw, 160px);
  line-height: 1.05;
  font-weight: 600;
}

/* Monospaced labels */
.text-mono-xs {
  font-family: var(--font-geist-mono);
  font-size: 12px;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: -0.0175rem;
}
```

### Dark/Light Theme Pattern

```html
<!-- Theme toggle with localStorage persistence -->
<script>
  const theme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', theme);
</script>
```

```css
/* Theme-aware colors */
.card {
  background: var(--color-base-100);
  border: 1px dashed var(--color-base-300);
}

[data-theme="light"] .card {
  background: var(--color-light-base-primary);
  border-color: var(--color-light-base-tertiary);
}
```

### Component Patterns

**Badges with accent dots:**
```html
<div class="badge">
  <span data-slot="badge-icon" aria-hidden="true"></span>
  <span class="text-mono-xs">SECTION</span>
</div>
```

```css
[data-slot='badge-icon'] {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-100);
}
```

**Dashed border cards:**
```css
.card {
  border: 1px dashed var(--color-base-300);
  border-radius: var(--radius-md);
  padding: calc(var(--spacing) * 6);
  transition: border-color var(--default-transition-duration) var(--ease-out);
}

.card:hover {
  border-color: var(--accent-100);
}
```

**Buttons with invert hover:**
```css
.btn-cta {
  background: var(--accent-100);
  color: var(--color-dark-base-primary);
  border: 1px solid var(--accent-100);
}

.btn-cta:hover {
  background: transparent;
  color: var(--accent-100);
}
```

## Anti-Patterns to Avoid

❌ Generic system fonts (Inter, Roboto, Arial, -apple-system)
❌ Purple gradients on white backgrounds
❌ Solid borders instead of dashed
❌ Cookie-cutter rounded corners without token system
❌ Browser default focus outlines
❌ Generic blue (#007bff) colors
❌ Transitions during theme changes
❌ Small touch targets (<44px on mobile)

## Bundled Resources

### Typography Reference
See `references/typography.md` for:
- Geist font loading patterns with fallbacks
- Complete typography scale utilities
- Responsive text sizing strategies

### Color System
See `references/color-schemes.md` for:
- Full accent palette variations
- Dark/light theme color mappings
- Semantic color token usage

### Starter Templates
See `assets/templates/` for:
- `base.html` - Complete HTML boilerplate with design system
- `components.html` - Common component patterns
- React variants coming soon

### Font Files
Pre-loaded Geist fonts in `assets/fonts/`:
- `geist-sans.woff2`
- `geist-mono.woff2`

## Key Principles

1. **Token-first**: Every magic number becomes a custom property
2. **Theme-aware**: All colors reference CSS variables, not hardcoded values
3. **Accessible**: Focus states, tap targets, semantic HTML
4. **Performance-conscious**: GPU acceleration only when needed, GSAP for complex animations
5. **Distinctive**: Make choices that feel designed for the context, not generic

Remember: This aesthetic is refined and technical, not flashy. The goal is clarity, precision, and thoughtful interaction design - not to wow with complexity.

---

# Color System Reference

## Accent Palette (Teal System)

The Jocril design system uses a **teal/cyan accent palette** as the primary brand color - NOT purple gradients.

### Core Accent Colors

```css
:root {
  --accent-100: #2DD4CD; /* Primary teal - bright, vibrant */
  --accent-200: #16B7B2; /* Secondary teal - slightly darker */
  --accent-300: #00DED7; /* Tertiary teal - electric cyan */
}
```

**Usage patterns:**
- `--accent-100`: Primary CTAs, active states, focus rings
- `--accent-200`: Hover states, secondary buttons
- `--accent-300`: Accent dots, badges, highlights

### Example Applications

**Button hover inversion:**
```css
.btn-cta {
  background: var(--accent-100);
  color: var(--color-dark-base-primary);
  border: 1px solid var(--accent-100);
  transition: all 200ms cubic-bezier(0.22, 1, 0.36, 1);
}

.btn-cta:hover {
  background: transparent;
  color: var(--accent-100);
}
```

**Focus states:**
```css
.interactive:focus-visible {
  outline: 2px solid var(--accent-300);
  outline-offset: 2px;
}
```

**Badge accent dots:**
```css
[data-slot='badge-icon'] {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-100);
  box-shadow: 0 0 8px var(--accent-100);
}
```

## Dark Theme Base Colors

```css
:root {
  /* Base neutrals (dark → light) */
  --color-base-100: #0A0A0A;   /* Darkest background */
  --color-base-200: #141414;   /* Card backgrounds */
  --color-base-300: #1F1F1F;   /* Elevated surfaces */
  --color-base-400: #2A2A2A;   /* Borders, dividers */
  --color-base-500: #3F3F3F;   /* Subtle borders */
  --color-base-600: #555555;   /* Disabled states */
  --color-base-700: #7A7A7A;   /* Secondary text */
  --color-base-800: #A0A0A0;   /* Tertiary text */
  --color-base-900: #C5C5C5;   /* Primary text */
  --color-base-1000: #FAFAFA;  /* Brightest text */
  
  /* Semantic aliases */
  --color-background: var(--color-base-100);
  --color-foreground: var(--color-base-1000);
  --color-muted: var(--color-base-700);
  --color-border: var(--color-base-400);
}
```

**Usage:**
```css
body {
  background: var(--color-base-100);
  color: var(--color-base-1000);
}

.card {
  background: var(--color-base-200);
  border: 1px dashed var(--color-base-400);
}

.text-muted {
  color: var(--color-base-700);
}
```

## Light Theme Base Colors

```css
[data-theme="light"] {
  --color-light-base-primary: #FFFFFF;     /* Main background */
  --color-light-base-secondary: #F5F5F5;   /* Card backgrounds */
  --color-light-base-tertiary: #E0E0E0;    /* Borders */
  --color-light-base-quaternary: #CCCCCC;  /* Subtle borders */
  
  --color-light-text-primary: #0A0A0A;     /* Primary text */
  --color-light-text-secondary: #555555;   /* Secondary text */
  --color-light-text-tertiary: #7A7A7A;    /* Tertiary text */
  
  /* Override semantic aliases */
  --color-background: var(--color-light-base-primary);
  --color-foreground: var(--color-light-text-primary);
  --color-muted: var(--color-light-text-secondary);
  --color-border: var(--color-light-base-tertiary);
}
```

**Usage:**
```css
/* Write once, theme-aware automatically */
.card {
  background: var(--color-base-200);
  border: 1px dashed var(--color-base-400);
}

/* Light theme overrides */
[data-theme="light"] .card {
  background: var(--color-light-base-secondary);
  border-color: var(--color-light-base-tertiary);
}
```

## Theme Switching Implementation

### HTML Setup

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <script>
    // Apply theme before render to prevent flash
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
  </script>
</head>
```

### Theme Toggle Logic

```javascript
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  // Disable transitions during theme change
  html.classList.add('disable-transitions');
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  // Re-enable transitions after paint
  setTimeout(() => {
    html.classList.remove('disable-transitions');
  }, 0);
}
```

### Transition Disable Utility

```css
.disable-transitions,
.disable-transitions * {
  transition: none !important;
  animation: none !important;
}
```

## Semantic Color Usage

### Buttons

```css
/* Primary CTA - teal accent */
.btn-cta {
  background: var(--accent-100);
  color: var(--color-base-100);
}

/* Secondary - outline */
.btn-secondary {
  background: transparent;
  border: 1px solid var(--color-base-400);
  color: var(--color-base-1000);
}

/* Destructive - red accent */
.btn-destructive {
  background: #EF4444;
  color: white;
}
```

### Status Colors

```css
:root {
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: var(--accent-100);
}
```

### Borders & Dividers

**Dashed borders** are the primary pattern:
```css
.card {
  border: 1px dashed var(--color-base-400);
}

.card:hover {
  border-color: var(--accent-100);
}
```

**Solid borders** only for inputs:
```css
input {
  border: 1px solid var(--color-base-500);
}

input:focus {
  border-color: var(--accent-100);
}
```

## Gradient Usage (Minimal)

Avoid heavy gradients. When needed, use subtle ones:

```css
/* Subtle radial gradient for depth */
.hero-background {
  background: radial-gradient(
    circle at 50% 0%,
    rgba(45, 212, 205, 0.05) 0%,
    transparent 50%
  );
}

/* Progress fills */
.progress-bar {
  background: linear-gradient(
    90deg,
    var(--accent-200) 0%,
    var(--accent-100) 100%
  );
}
```

## Z-Index System

```css
:root {
  --z-below: -1;
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-maximum: 999;
}
```

## Anti-Patterns to Avoid

❌ Purple gradients (`linear-gradient(135deg, #667eea 0%, #764ba2 100%)`)
❌ Hardcoded color values (use tokens always)
❌ Blue focus outlines (browser default)
❌ Low contrast text (WCAG AA minimum: 4.5:1)
❌ Transitions during theme switching
❌ Solid backgrounds without considering theme
❌ Generic accent colors (#007bff, #6c757d)

## Accessibility Guidelines

- **Minimum contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: 2px solid, accent color, 2px offset
- **Touch targets**: 44x44px minimum on mobile
- **Theme preference**: Respect `prefers-color-scheme` media query

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--color-base-100);
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --color-background: var(--color-light-base-primary);
  }
}
```

## Color Token Quick Reference

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--accent-100` | #2DD4CD | #2DD4CD | Primary actions |
| `--accent-200` | #16B7B2 | #16B7B2 | Hover states |
| `--accent-300` | #00DED7 | #00DED7 | Highlights |
| `--color-background` | #0A0A0A | #FFFFFF | Body background |
| `--color-foreground` | #FAFAFA | #0A0A0A | Primary text |
| `--color-muted` | #7A7A7A | #555555 | Secondary text |
| `--color-border` | #2A2A2A | #E0E0E0 | Borders |

---

# Typography Reference

## Font Loading

### Geist Sans with Fallback Metrics

```css
@font-face {
  font-family: 'Geist';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('../fonts/geist-sans.woff2') format('woff2');
  unicode-range: U+00??, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, 
                 U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, 
                 U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}

@font-face {
  font-family: 'Geist Fallback';
  src: local('Arial');
  ascent-override: 95.94%;
  descent-override: 28.16%;
  line-gap-override: 0%;
  size-adjust: 104.76%;
}
```

**CSS Variable:**
```css
:root {
  --font-geist-sans: 'Geist', 'Geist Fallback';
}
```

### Geist Mono with Fallback Metrics

```css
@font-face {
  font-family: 'Geist Mono';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('../fonts/geist-mono.woff2') format('woff2');
  unicode-range: U+00??, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, 
                 U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, 
                 U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}

@font-face {
  font-family: 'Geist Mono Fallback';
  src: local('Arial');
  ascent-override: 74.67%;
  descent-override: 21.92%;
  line-gap-override: 0%;
  size-adjust: 134.59%;
}
```

**CSS Variable:**
```css
:root {
  --font-geist-mono: 'Geist Mono', 'Geist Mono Fallback';
}
```

## Typography Scale

### Monospaced Text Utilities

#### Extra Small (Labels)
```css
.text-mono-xs {
  font-family: var(--font-geist-mono);
  font-size: 12px;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: -0.0175rem;
  font-weight: 500;
}
```

**Usage:** Section badges, category labels, timestamps

#### Small (Metadata)
```css
.text-mono-sm {
  font-family: var(--font-geist-mono);
  font-size: 14px;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: -0.0175rem;
  font-weight: 400;
}
```

**Usage:** Job listings, portfolio metadata

#### Medium (Responsive Body)
```css
.text-mono-md {
  font-family: var(--font-geist-mono);
  font-size: 16px;
  line-height: 1.2;
  font-weight: 400;
}

@media (min-width: 1024px) {
  .text-mono-md {
    font-size: 18px;
  }
}
```

**Usage:** Process descriptions, card details

#### Meta (Secondary Details)
```css
.text-mono-meta {
  font-family: var(--font-geist-mono);
  font-size: 14px;
  line-height: 1.2;
  font-weight: 400;
}

@media (min-width: 1024px) {
  .text-mono-meta {
    font-size: 16px;
  }
}
```

**Usage:** Supplementary information, footnotes

### Heading Scale

#### Heading 1 (Hero)
```css
.heading-1 {
  font-family: var(--font-geist-sans);
  font-size: 70px;
  line-height: 1.05;
  font-weight: 600;
  letter-spacing: -0.02em;
}

@media (min-width: 640px) {
  .heading-1 {
    font-size: 100px;
    line-height: 1.1;
  }
}

@media (min-width: 1024px) {
  .heading-1 {
    font-size: 130px;
  }
}

@media (min-width: 1280px) {
  .heading-1 {
    font-size: 160px;
  }
}
```

**Usage:** Landing page heroes, primary headlines

**Responsive behavior:**
- Mobile: 70px
- Tablet: 100px
- Desktop: 130px
- Large: 160px

#### Heading 2 (Section Titles)
```css
.heading-2 {
  font-family: var(--font-geist-sans);
  font-size: 30px;
  line-height: 1;
  font-weight: 600;
  letter-spacing: -0.01em;
}

@media (min-width: 640px) {
  .heading-2 {
    font-size: 36px;
  }
}

@media (min-width: 1024px) {
  .heading-2 {
    font-size: 48px;
  }
}
```

**Usage:** Section headings, page titles

## Typography Pairing Guidelines

### Display + Monospace
Primary pattern: Geist Sans for headlines, Geist Mono for supporting text

```html
<div class="hero">
  <h1 class="heading-1">Manufacturing</h1>
  <p class="text-mono-md">PRECISION LASER CUTTING & CNC MILLING</p>
</div>
```

### High Contrast Weights
Use aggressive weight jumps (100-200 vs 800-900) not subtle differences (400 vs 600)

```css
.section-label {
  font-weight: 200; /* Light */
}

.section-title {
  font-weight: 800; /* Heavy */
}
```

### Size Extremes
Prefer 3x+ size jumps between hierarchical levels

```css
/* Hero: 160px */
.heading-1 { font-size: 160px; }

/* Meta: 14px (11.4x smaller) */
.text-mono-xs { font-size: 14px; }
```

## Loading Strategy

1. **Preload critical fonts** in HTML head:
```html
<link rel="preload" href="/fonts/geist-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/geist-mono.woff2" as="font" type="font/woff2" crossorigin>
```

2. **Define @font-face** with font-display: swap
3. **Provide fallback metrics** to prevent layout shift
4. **Use CSS variables** for consistent font-family references

## Accessibility Considerations

- Minimum 14px for body text
- Line height ≥1.2 for readability
- Letter spacing adjustments for uppercase text
- No orphaned text in headlines (use `&nbsp;` or CSS)
- Semantic HTML heading hierarchy

## Common Mistakes to Avoid

❌ Using variable fonts without specifying weights
❌ Missing fallback font metrics (causes layout shift)
❌ Not preloading critical fonts
❌ Using generic font-family names (Arial, sans-serif)
❌ Timid size scaling (1.5x jumps instead of 3x+)
❌ Lowercase labels without sufficient tracking adjustments

## Templates

HTML starter templates: base.html 
Source: `/mnt/skills/user/jocril-frontend-design/assets/`
