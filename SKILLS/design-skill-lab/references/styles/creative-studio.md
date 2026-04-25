
# Creative Studio Warmth

Premium aesthetic for creative agencies and design studios. Dark, gallery-like backgrounds that make portfolio work pop, warmed by coral accents.

## Quick Start

1. Copy `assets/template.html` as starting point
2. Customize brand name, services, content
3. Replace placeholder images
4. Adjust sections based on context

## Display Typography & Hero Patterns

Creative Studio is portfolio-first. Type drama signals confidence and production value.

**`display-xl` (144px, Inter 700)** — The agency's name moment. Use on the home hero or the "we are X" intro band. One per page maximum.

**`display-lg` (112px, Inter 700)** — Big "what we do" statement headlines, project case study openers, "let's work together" CTAs. The workhorse for impact moments inside dark bands.

**`headline-xl` (96px)** — Service titles, project names in case studies, watermark-style background type.

**`headline-lg` (56px)** — Section headers inside content bands, sub-titles on case studies.

**Hero patterns by page type:**

- **Agency home hero** — Dark band, `display-xl` headline left or asymmetric, watermark text behind, primary CTA bottom. Use `4xl` (80px) vertical padding inside the band.
- **Case study opener** — Full-bleed coral or dark band with `display-lg` overlay on imagery. Use `pad-band` (48px) interior.
- **Process bands** — Each step uses `headline-lg` over the coral gradient backgrounds. The band padding (`pad-band` = 48px) is non-negotiable for rhythm.
- **About / team** — `display-xl` introduction over dark background, then `headline-lg` for individual team members.

**Spacing for the gallery feel:**

- Section bands (hero, services, stats): `5xl` (128px) or `4xl` (80px) vertical padding for the gallery breathing room
- Between sections: alternate dark/light bands with `4xl` minimum gap to prevent visual collision
- Card grids inside bands: `xl` (32px) gap minimum, `2xl` (48px) preferred for case studies
- Inside cards: `lg` (24px) — keep cards tight, let bands breathe

## Core Aesthetic

- **Dark foundation**: Charcoal hero (#2d2f2e) creates gallery feel
- **Warm coral accent**: #ff531f for CTAs, gradient scale for process bands
- **Full-color imagery**: Unlike brutalist grayscale, work is shown in full color
- **Generous rounding**: 24-48px radius on cards, full pill buttons
- **Sliding sections**: Light content overlaps dark with rounded top corners

## Section Selection

Choose sections based on client context:

| Section | Use When |
|---------|----------|
| Hero + Watermark | Always - establishes brand |
| Client Logo Bar | Has notable clients |
| Intro with Big Number | Emphasizing transformation (0→1) |
| Bento Grid | Multiple proof points to show |
| Services (dark) | Listing service offerings |
| FAQ | Common questions exist |
| Process Bands | Want to explain methodology |
| Stats Section | Have impressive metrics |

## Critical Implementation Rules

### Bento Grid Must Be Perfect Rectangle
```css
/* CORRECT - explicit areas */
grid-template-areas:
    "testimonial stat1     casestudy"
    "testimonial process   casestudy"
    "timeline    timeline  stat2";

/* WRONG - creates holes */
.card { grid-row: span 2; }
```

### Sliding Section Overlap
```css
.content-wrapper {
    margin-top: -80px;
    border-radius: 48px 48px 0 0;
    position: relative;
    z-index: 10;
}
```

### Pill Buttons
```css
.btn-primary {
    border-radius: 9999px; /* Full pill, always */
    background: #ff531f;
}
```

## JavaScript Interactions

The template includes working JS for:
- Navigation scroll effect (background on scroll)
- FAQ accordion (click to expand)
- Process band expansion (click to show steps)
- Smooth scroll for anchor links
- Scroll-triggered animations (IntersectionObserver)

## Design Tokens

See `references/design-tokens.md` for complete color, typography, and spacing values.

Key colors:
- Dark BG: `#2d2f2e`
- Light BG: `#f5f5f5`  
- Primary CTA: `#ff531f`
- Coral gradient: `#fff0eb → #ffc8b8 → #ff9d80 → #ff531f`

## Output Checklist

Every Creative Studio Warmth design should have:
- [ ] Dark charcoal hero with watermark
- [ ] Sliding light section (rounded top corners, negative margin)
- [ ] Coral accent (#ff531f) for CTAs
- [ ] Pill-shaped buttons
- [ ] Working JavaScript interactions
- [ ] Plus Jakarta Sans / Antonio typography
- [ ] Responsive breakpoints (1024px, 768px)

---

## Design Tokens (Complete Reference)

# Design Tokens

## Colors

### Dark Palette
```css
--dark-bg: #2d2f2e;           /* Hero, services, stats backgrounds */
--dark-secondary: #434645;     /* Watermark text, subtle elements */
--text-light: #ffffff;         /* White text on dark */
--text-muted-dark: #767f7a;    /* Muted text on dark backgrounds */
```

### Light Palette
```css
--light-bg: #f5f5f5;          /* Main content background */
--card-bg: #ffffff;            /* Cards, FAQ, footer */
--text-dark: #171717;          /* Primary text on light */
--text-muted: #afb6b4;         /* Secondary text, labels */
--border: #dddfde;             /* Borders, dividers */
```

### Coral Scale (Key Accent)
```css
--coral-lightest: #fff0eb;    /* Discovery band, subtle highlights */
--coral-light: #ffc8b8;       /* Concept band */
--coral-medium: #ff9d80;      /* Execution band */
--coral-strong: #ff531f;      /* Primary CTA, Launch band, links */
--coral-vivid: #ff825c;       /* Hover states */
```

## Typography

### Fonts
- **Display/Logo**: `Antonio` (700 weight, uppercase)
- **Body**: `Plus Jakarta Sans` (400, 500, 600, 700 weights)
- **Fallback**: `-apple-system, BlinkMacSystemFont, sans-serif`

### Scale
```css
/* Responsive clamp values */
--text-hero: clamp(2rem, 4vw, 3rem);
--text-section: clamp(3rem, 7vw, 5rem);
--text-giant: clamp(5rem, 10vw, 8rem);
--text-watermark: clamp(10rem, 22vw, 18rem);
```

## Border Radius
```css
--radius-sm: 24px;    /* Cards */
--radius-md: 32px;    /* Footer, hero image */
--radius-lg: 40px;    /* Large elements */
--radius-xl: 48px;    /* Content wrapper overlap */
--radius-pill: 9999px; /* Buttons, pills */
```

## Transitions
```css
/* Standard */
transition: all 0.3s ease;

/* Hero animations */
animation: slideFromLeft 1.4s cubic-bezier(1, -0.13, 0.18, 0.96);
animation: slideFromBottom 0.9s cubic-bezier(1, -0.13, 0.18, 0.96);
animation: fadeUp 0.6s cubic-bezier(0.93, 0.03, 0.56, 1);
```

## Breakpoints
- **Desktop**: 1200px+
- **Tablet**: 810px - 1199px
- **Mobile**: < 810px

## Templates

HTML starter templates: template.html 
Source: `/mnt/skills/user/creative-studio-warmth/assets/`
