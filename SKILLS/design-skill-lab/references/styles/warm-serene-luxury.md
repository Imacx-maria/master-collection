
# Warm Serene Luxury

Premium aesthetic for hospitality, lifestyle, and creative service brands. Warmth comes from carefully selected imagery rather than accent colors — the palette is intentionally minimal (#FAFAFA / #1A1A1A) so photography becomes the color story.

## Quick Start

1. Copy `assets/template.html` as starting point
2. Replace brand name, services, content
3. Swap placeholder images for warm, natural-light photography
4. Adjust sections based on context

## Display Typography & Hero Patterns

Luxury hospitality lives in restraint. Display type provides architectural elegance without competing with the photography.

**`display-xl` (144px, DM Serif Display)** — The brand's signature moment. Property name on home hero, "stay with us" anchors, the about-page declaration. Pair with photography that gives the type room — never crop tightly. One per page.

**`display-lg` (104px, DM Serif Display)** — Section openers ("Our Suites", "The Experience"), property collections, secondary heroes. Carries elegance without claiming the page-defining slot.

**`headline-lg` (56px)** — Sub-section titles, room/suite names within a list, editorial sub-anchors.

**`label-number` (11px, Onest)** — The signature numbered-item pattern (01, 02, 03) with wide tracking (0.14em) and uppercase. Use systematically for editorial sequencing — chapter markers, room counts, process steps.

**Hero patterns by page type:**

- **Property home** — `display-xl` brand/property name, full-bleed photography below or behind, `5xl` (144px) vertical padding for the architectural breathing room. No CTA shouting — a single quiet "Reserve" link in `label-number` style.
- **Suite / room detail** — `display-lg` suite name, large hero photography, then numbered item list (01 Bedroom, 02 Bathroom, 03 Terrace) using `numbered-item`. `4xl` (96px) padding throughout.
- **About / story** — `display-xl` declarative anchor ("A retreat for the senses"), then editorial body with images interspersed. Numbered chapters using `label-number`.
- **Reservations / contact** — Skip display. `headline-lg` for "Reserve" or "Inquire", calm form with generous spacing.

**Spacing for hospitality breathing:**

- Hero sections: `5xl` (144px) vertical padding — luxury demands physical room
- Between sections: `4xl` (96px) — never less, the calm rhythm depends on it
- Photography sections: pair `4xl` margins around full-bleed images for architectural pause
- Numbered item lists: `xl` (32px) between items, `lg` (24px) inside each item
- Inside cards: `pad-card` (32px) — generous, never tight
- Form fields: `lg` (24px) between fields for unhurried interaction
- The numbered-item pattern uses `zero` padding by design — relies on typography alone

**Photography is the focal element:**

If a hero section has display type AND photography, the photography always wins the hierarchy battle. Type is set quietly to the side or above, never overlapping the focal area. Use `5xl` margins around photography to let it breathe.

## Core Aesthetic

- **Near-white background**: #FAFAFA creates calm canvas
- **Typography contrast**: DM Serif Display (display) + Onest (body)
- **Numbered items**: (01), (02), (03) adds sophistication
- **Imagery-driven warmth**: Peachy, blush, terracotta tones in photos — not CSS
- **Generous whitespace**: 88px section gaps
- **Pill buttons**: Full border-radius CTAs

## Signature Patterns

| Pattern | Example | Usage |
|---------|---------|-------|
| Numbered items | `(01)` | Room cards, tabs, navigation |
| Section labels | Serif uppercase above headline | Every section header |
| Stats row | Large number + small label | Social proof, metrics |
| Spec grids | Value + label pairs | Room/product details |
| Link counts | `Features (16)` | Navigation sophistication |
| Tab selector | Room/Space picker in hero | Service selection |

## Section Selection

| Section | Use When |
|---------|----------|
| Hero + Tabs | Always — establishes brand + offerings |
| Room Preview Card | Highlighting primary offering |
| Info Cards Row | Hours, location, booking info |
| About + Stats | Building credibility |
| Full-Width Image | Breaking up text, showing space |
| Item Cards | Multiple rooms/services/products |
| CTA Banner | Driving conversions mid-page |
| Features Grid | Listing amenities/services |
| Gallery | Showcasing environment/work |
| Testimonials | Social proof |
| Contact | Always — clear next step |
| Footer | Always — navigation + info |

## Critical Rules

### Typography Hierarchy
```css
.display { /* Headlines */
  font-family: "DM Serif Display", serif;
  font-size: 96px;
  text-transform: uppercase;
  letter-spacing: -0.01em;
}

.section-label { /* Labels ABOVE headlines */
  font-family: "DM Serif Display", serif;
  font-size: 20px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

body { /* Everything else */
  font-family: "Onest", sans-serif;
  font-size: 18px;
}
```

### Numbered Pattern
```html
<span class="room-number">(01)</span>
<span class="tab-number">(02)</span>
<!-- Always parentheses, always zero-padded -->
```

### Pill Buttons
```css
.btn {
  border-radius: 9999px; /* Full pill, always */
  padding: 14px 28px;
}
```

## Micro-Interactions

The template includes JS for:
- Scroll-triggered fade-in animations
- Staggered children reveal (80ms delay)
- Counter animation for stats
- Image scale on hover (1.05×)
- Nav background solidifies on scroll
- Button lift + shadow on hover
- Contact card accent bar reveal
- Parallax on hero image
- `prefers-reduced-motion` respected

## Design Tokens

See `references/design-tokens.md` for complete values.

Key tokens:
- Light: `#FAFAFA`
- Dark: `#1A1A1A`
- Opacity variants: 75%, 65%, 40%, 10%, 5%, 3%
- Section padding: `88px`
- Grid gap: `40px`
- Container max: `1456px`

## Component Patterns

See `references/component-patterns.md` for HTML structures of all components.

## Output Checklist

Every Warm Serene Luxury design should have:
- [ ] #FAFAFA background with #1A1A1A text
- [ ] DM Serif Display for headlines/labels
- [ ] Onest for body text
- [ ] Numbered items pattern (01), (02)
- [ ] Section labels above headlines
- [ ] Pill-shaped buttons
- [ ] Stats row with large numbers
- [ ] Spec grids for details
- [ ] Warm imagery (not accent colors)
- [ ] 88px section gaps
- [ ] Working micro-interactions
- [ ] Responsive breakpoints (1199px, 767px)

---

## Design Tokens (Complete Reference)

# Design Tokens

## Colors

### Core
| Token | Value | Usage |
|-------|-------|-------|
| `--color-light` | `#FAFAFA` | Primary background |
| `--color-dark` | `#1A1A1A` | Primary text |

### Light Opacity Variants
| Token | Value |
|-------|-------|
| `--color-light-75` | `rgba(250, 250, 250, 0.75)` |
| `--color-light-10` | `rgba(250, 250, 250, 0.10)` |

### Dark Opacity Variants
| Token | Value | Usage |
|-------|-------|-------|
| `--color-dark-75` | `rgba(26, 26, 26, 0.75)` | Secondary text |
| `--color-dark-65` | `rgba(26, 26, 26, 0.65)` | Muted text |
| `--color-dark-40` | `rgba(26, 26, 26, 0.40)` | Placeholder, labels |
| `--color-dark-10` | `rgba(26, 26, 26, 0.10)` | Borders, dividers |
| `--color-dark-05` | `rgba(26, 26, 26, 0.05)` | Hover states |
| `--color-dark-03` | `rgba(26, 26, 26, 0.03)` | Card backgrounds |

## Typography

### Font Families
| Token | Value |
|-------|-------|
| `--font-display` | `"DM Serif Display", Georgia, serif` |
| `--font-body` | `"Onest", -apple-system, sans-serif` |

### Type Scale
| Style | Font | Size | Weight | Letter-spacing | Line-height | Transform |
|-------|------|------|--------|----------------|-------------|-----------|
| Display | DM Serif | 96px | 400 | -0.01em | 92% | uppercase |
| H1 | Onest | 80px | 300 | -0.03em | 92% | none |
| H2 | Onest | 36px | 400 | -0.02em | 108% | none |
| Section Label | DM Serif | 20px | 400 | +0.04em | 104% | uppercase |
| Body | Onest | 18px | 400 | -0.01em | 136% | none |
| Small | Onest | 14px | 400 | 0 | 136% | none |

### Responsive Typography
| Style | Desktop | Tablet | Mobile |
|-------|---------|--------|--------|
| Display | 96px | 72px | 48px |
| H1 | 80px | 56px | 36px |
| H2 | 36px | 28px | 24px |

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--section-padding` | `88px` | Section vertical padding |
| `--container-max` | `1456px` | Max content width |
| `--container-padding` | `24px` | Horizontal padding |
| `--grid-gap` | `40px` | Grid column gap |

## Layout

### Grid
```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 40px;
}
```

### Breakpoints
| Name | Value |
|------|-------|
| Desktop | `≥1200px` |
| Tablet | `768px – 1199px` |
| Mobile | `<768px` |

## Borders

| Token | Value |
|-------|-------|
| `--border-color` | `rgba(26, 26, 26, 0.10)` |
| `--radius-sm` | `8px` |
| `--radius-md` | `12px` |
| `--radius-lg` | `16px` |
| `--radius-full` | `9999px` |

## Transitions

| Token | Value | Usage |
|-------|-------|-------|
| `--transition` | `0.2s ease` | Standard |
| `--transition-slow` | `0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)` | Reveals |
| `--transition-smooth` | `0.6s cubic-bezier(0.16, 1, 0.3, 1)` | Page transitions |

## CSS Variables Block

```css
:root {
  --color-light: #FAFAFA;
  --color-dark: #1A1A1A;
  --color-light-75: rgba(250, 250, 250, 0.75);
  --color-light-10: rgba(250, 250, 250, 0.10);
  --color-dark-75: rgba(26, 26, 26, 0.75);
  --color-dark-65: rgba(26, 26, 26, 0.65);
  --color-dark-40: rgba(26, 26, 26, 0.40);
  --color-dark-10: rgba(26, 26, 26, 0.10);
  --color-dark-05: rgba(26, 26, 26, 0.05);
  --color-dark-03: rgba(26, 26, 26, 0.03);
  
  --font-display: "DM Serif Display", Georgia, serif;
  --font-body: "Onest", -apple-system, sans-serif;
  
  --section-padding: 88px;
  --container-max: 1456px;
  --container-padding: 24px;
  --grid-gap: 40px;
  
  --border-color: rgba(26, 26, 26, 0.10);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  
  --transition: 0.2s ease;
  --transition-slow: 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --transition-smooth: 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## Component Patterns

For complete component code snippets, read the original skill's component-patterns reference.
Source: `/mnt/skills/user/warm-serene-luxury/references/component-patterns.md`

## Templates

HTML starter templates: template.html 
Source: `/mnt/skills/user/warm-serene-luxury/assets/`
