
# Editorial Portfolio

Warm minimalist design system characterized by compressed uppercase Inter typography, off-white backgrounds, and interactive hover-reveal portfolio panels.

## Quick Start

1. Copy `assets/template.html` to your working directory
2. Replace `<!-- SLOT: ... -->` placeholders with content
3. Add images (recommended: B&W or desaturated, high contrast)
4. Customize colors in `:root` CSS variables if needed

## Display Typography & Hero Patterns

Editorial portfolios use type as composition. Display sizes carry the weight of curated work.

**`display-xl` (128px, Inter 400)** — The portfolio holder's name moment, the about-page anchor, or the project series title. Compressed, light weight, hard letter-spacing (-0.03em). One per page.

**`display-lg` (88px, Inter 400)** — Project titles inside case studies, section openers ("Selected Work", "Recent"), the hover-reveal panel headlines. Use when the moment needs presence but isn't the page-defining statement.

**`headline-lg` (56px)** — Project names in grid views, sub-section titles, image captions that need weight.

**Hero patterns by page type:**

- **Portfolio home** — Asymmetric `display-xl` headline + portrait or featured project image. Use `5xl` (128px) top padding to give the type room. Tagline lines below in `body-md`.
- **Project case study** — Full-bleed image, then `display-lg` overlay or below image with `4xl` (80px) margin. Image library carries the visual weight.
- **About page** — `display-xl` introduction left, portrait right. `5xl` vertical padding throughout.
- **Index / archive** — `headline-lg` per project name, image grid with hover-reveal panels using `panel-overlay` component. No display type — let the image grid be the composition.

**Spacing for editorial composition:**

- Section openers: `5xl` (128px) top padding for major sections, `4xl` (80px) for sub-sections
- Image-led sections: `4xl` margin around full-bleed moments
- Project grid gaps: `xl` (32px) — never tighter, the breathing space is part of the editorial restraint
- Inside text columns: `lg` (24px) line-clusters, `xl` between paragraphs for long-form prose
- Hero asymmetry: leave 30-40% of the hero as negative space — that's not waste, that's composition

## Content Slots

| Slot | Location | Content |
|------|----------|---------|
| `page-title` | `<title>` | Browser tab title |
| `nav-name` | Nav | Name/brand in header |
| `hero-bg-image` | Hero | Full-bleed background image URL |
| `hero-portrait` | Hero | Portrait/featured image URL |
| `hero-title-line1` | Hero | Main headline (bold) |
| `hero-title-line2` | Hero | Subtitle line (thin weight) |
| `tagline-1`, `tagline-2` | Hero | Two descriptor lines |
| `about-headline` | About | Large section headline |
| `about-bio` | About | Biography paragraph |
| `motto-label` | About | Small label (e.g., "MOTTO") |
| `motto-text` | About | Tagline/motto text |
| `services-header-image` | Services | Header image URL |
| `services-title` | Services | Section headline |
| `service-cards` | Services | 3-column service cards |
| `work-section-title` | Work | Section title (e.g., "MY WORK") |
| `work-items` | Work | Work list items (see template) |
| `work-panels` | Work | Hover detail panels (see template) |
| `statement-bg-image` | Statement | Full-bleed background URL |
| `statement-text` | Statement | Artist statement text |
| `testimonials` | Testimonials | Quote blocks (see template) |
| `footer-headline` | Footer | Large footer text |
| `footer-cta` | Footer | Call-to-action text |
| `social-links` | Footer | Social media links |

## Design Tokens Summary

**Colors:**
- Background: `#f4f3f0` (warm off-white)
- Text: `#1d1f1e` (near-black)
- Accent: `#f1ede1` (cream hover state)
- Footer: `#161616` (dark)

**Typography:**
- Font: Inter (200, 300, 400 weights)
- Letter-spacing: `-0.03em` to `-0.06em` (compressed)
- Transform: `uppercase` on all text
- Hero: `11vw` fluid size

**Layout:**
- Container: `120em` max-width
- Section padding: `5rem` vertical
- Global padding: `3rem` → `2rem` → `1.5rem` responsive

For complete values, see `references/design-tokens.md`.

## Signature Patterns

### Hover-Reveal Work Panels
The work section uses `data-item` and `data-panel` attributes for hover interaction:
```html
<div class="work-line" data-item="1">...</div>
<div class="work-panel" data-panel="1">...</div>
```
JavaScript handles showing/hiding panels on hover.

### Mix-Blend Exclusion
Hero text uses `mix-blend-mode: exclusion` to remain visible over varying backgrounds.

### Sticky Footer
Footer uses negative margin + spacer technique to create reveal-on-scroll effect.

For component code, see `references/component-patterns.md`.

## Image Guidelines

- **Style:** Black & white or desaturated, high contrast
- **Hero background:** Landscape orientation, can be busy (text uses blend mode)
- **Portrait:** Tall aspect ratio (template uses 120% padding-top)
- **Work panels:** Square or portrait crops, 13rem display height

## Responsive Behavior

- **Desktop (>991px):** Full layout, side-by-side work list + panels
- **Tablet (≤991px):** Centered text, stacked hero elements
- **Mobile (≤479px):** Single column, panels below list, touch-tap interaction

## Customization

Edit CSS variables in `:root`:
```css
:root {
  --white-smoke: #f4f3f0;    /* Change background */
  --primary-text: #1d1f1e;    /* Change text color */
  --accent-hover: #f1ede1;    /* Change hover state */
  --footer-bg: #161616;       /* Change footer */
}
```

Typography weight can be adjusted but maintain the compressed letter-spacing for aesthetic consistency.

---

## Design Tokens (Complete Reference)

# Editorial Portfolio Design Tokens

Extracted from Pierre template. All values are exact.

## Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--white-smoke` | `#f4f3f0` | Primary background |
| `--primary-text` | `#1d1f1e` | Headlines, body text |
| `--secondary-text` | `#444745` | Subtitles, metadata |
| `--accent-hover` | `#DBD5C9` | Hover states, services section bg |
| `--footer-bg` | `#161616` | Footer background |

## Typography

### Font Stack
```css
font-family: Inter, sans-serif;
```
Load from Google Fonts: `Inter:200,300,regular`

### Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| Hero Display | `11vw` | 400 | 0.9 | `-0.03em` |
| H1 | `5.5rem` | 400 | 95% | `-0.06em` |
| H3 | `3.5rem` | 400 | 110% | `-0.06em` |
| H3 (light) | `3rem` | 400 | 120% | `-0.03em` |
| H4 | `32px` | 400 | 120% | `-0.03em` |
| Subtitle | `3.7rem` | 200 | 110% | `-0.06em` |
| Body | `1rem` | 300 | 150% | `-0.06em` |
| Small | `1rem` | 300 | 150% | `0.02em` |
| Logo | `25px` | 400 | - | - |

### Text Transform
All text: `text-transform: uppercase`

### Thin Variant
```css
.is-thin {
  font-weight: 200;
  line-height: 0.93;
}
```

## Spacing

### Section Padding
```css
padding-top: 5rem;
padding-bottom: 5rem;
```

### Global Padding (horizontal)
| Breakpoint | Value |
|------------|-------|
| Desktop | `3rem` |
| Tablet (≤767px) | `2rem` |
| Mobile (≤479px) | `1.5rem` |

### Container
```css
max-width: 120em;
```

### Component Gaps
- Section gap: `5rem`
- Content gap: `1.5rem`
- Work list gap: `10rem` (between columns)
- Work line height: `2.5rem`

## Responsive Breakpoints

```css
/* Tablet */
@media screen and (max-width: 991px) { }

/* Small Tablet */
@media screen and (max-width: 767px) { }

/* Mobile */
@media screen and (max-width: 479px) { }
```

### Typography Scale by Breakpoint

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| H1 | `5.5rem` | `4rem` | `1.9rem` |
| H3 | `3.5rem` | `2rem` | `1.7rem` |
| Hero | `11vw` | `7.1em` | `3.9em` |
| Subtitle | `3.7rem` | `2rem` | `1.8rem` |

## Special Effects

### Mix Blend Mode
Hero text and nav logo use exclusion blend:
```css
mix-blend-mode: exclusion;
```

### Nav Scroll State
```css
.logo.scroll {
  color: var(--white-smoke);
  mix-blend-mode: normal;
}
```

### Image Treatment
Hero portrait uses aspect ratio padding:
```css
padding-top: 120%; /* Creates tall portrait aspect */
```

### Border Style
Work lines use thin bottom borders:
```css
border-bottom: 1px solid #000;
```

## Animation Timing

### Hover Reveal Panels
```css
transition: opacity 0.5s ease;
```

### Smooth Scroll (Lenis)
```javascript
duration: 1.5,
easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t))
```

---

## Component Patterns

For complete component code snippets, read the original skill's component-patterns reference.
Source: `/mnt/skills/user/editorial-portfolio/references/component-patterns.md`

## Templates

HTML starter templates: template.html 
Source: `/mnt/skills/user/editorial-portfolio/assets/`
