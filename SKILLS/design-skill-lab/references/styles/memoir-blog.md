
# Memoir Blog

Warm, content-focused blog design for writers, creators, and newsletter builders. The aesthetic is approachable yet refined — creamy backgrounds with tight typography create a reading-first experience.

## Quick Start

1. Copy `assets/template.html` (index) and `assets/post.html` (article) as starting points
2. Replace brand name, tagline, and blog content
3. Swap placeholder Unsplash images with your own
4. Adjust post categories and navigation links
5. Link blog cards in template.html to individual post pages

## Display Typography & Hero Patterns

Memoir is reading-first. Display type exists but used sparingly — drama lives in long-form prose, not in oversized headlines.

**`display-lg` (96px, Manrope 700)** — The one moment of typographic drama. Use only on the blog homepage masthead or for a featured post hero. Pair with the `accent-italic` (Source Serif 4) for the signature italic-serif-inside-sans pattern.

**`headline-xl` (64px, Manrope 700)** — Featured post titles, category page headers, "About" page anchor. Most blog "drama" lives here.

**`headline-md` (32px, Manrope 700)** — Article titles in card grids, sidebar headers, post sub-sections.

**`accent-italic` (18px, Source Serif 4 italic)** — Editorial accent for emphasis words inside body, pull-quotes, intro taglines. The italic-serif-inside-sans is the signature move — use it deliberately, not constantly.

**Hero patterns by page type:**

- **Blog homepage** — `display-lg` blog name (or `headline-xl` if more reserved), tagline below in `accent-italic`. Use `4xl` (80px) vertical padding. Featured post grid below.
- **Article page** — `headline-xl` post title, `accent-italic` subtitle/dek, author byline in `label-sm`. Hero image below or above. `5xl` (128px) top padding for breathing room.
- **Category / archive** — `headline-xl` category name, `body-md` description, then filter pills + blog card grid. `4xl` top padding.
- **About page** — `headline-xl` for "About", body Manrope with serif italic emphasis on key phrases.

**Spacing for reading rhythm:**

- Article body: `lg` (24px) between paragraphs, `2xl` (48px) before/after pull-quotes or images
- Section dividers: `4xl` (80px) for major page transitions, `2xl` between sub-sections inside articles
- Blog card grids: `xl` (32px) gap, `lg` inside individual cards (preserves reading density)
- Sidebar: `lg` between nav items, `xl` between sidebar sections
- Filter pill clusters: `sm` (8px) horizontal gap — pills should feel grouped, not separated

## Core Aesthetic

- **Creamy background**: #F4F2F0 — warm canvas for reading
- **Typography contrast**: Manrope (headers) + Source Serif 4 italic (accents)
- **Tight letter-spacing**: -0.06em on headlines for modern density
- **White blog cards**: #FFFFFF with soft 8px border-radius
- **Metadata pattern**: Category • Read time (e.g., "Business • 5 min")
- **Arrow CTAs**: 24px arrow-up-right icons in cream pills
- **Black sidebar text**: #000000 with opacity 0.6 for inactive items
- **Tag filter pills**: Active = white, Inactive = cream (#EDEAE7)

## Signature Patterns

| Pattern | Example | Usage |
|---------|---------|-------|
| Hero headline | Mixed serif italic | "Ideas for the *modern* creator" |
| Blog card | Image + title + arrow + meta | Post listings |
| Email form | Input + Subscribe button | Hero + sidebar |
| Category bullet | "Business • 5 min" | Every blog card |
| Arrow icon | 45° arrow in pill | Post links, CTAs |
| Pinned post | Sidebar card with "Pinned" label | Highlight best content |
| Tag filters | Pill buttons (All, Writing, etc.) | Above blog grid |
| Search bar | Icon + input in white pill | Filter posts |
| Sidebar footer | "© 2025 Name. Created by X." | Attribution + year |

## Typography Hierarchy

```css
h1 { /* Hero headline */
  font-family: "Manrope", sans-serif;
  font-weight: 500;
  font-size: 64px;
  letter-spacing: -0.06em;
  line-height: 110%;
}

.italic-accent { /* Emphasis words */
  font-family: "Source Serif 4", serif;
  font-style: italic;
  letter-spacing: -0.07em;
}

body { /* Body + UI text */
  font-family: "Manrope", sans-serif;
  font-weight: 400;
  font-size: 14px;
  line-height: 150%;
}

.card-title { /* Blog card headlines */
  font-family: "Manrope", sans-serif;
  font-weight: 500;
  font-size: 16px;
  letter-spacing: -0.02em;
  line-height: 130%;
}

.metadata { /* Category, read time */
  font-family: "Manrope", sans-serif;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.48);
}
```

## Blog Card Structure

```html
<a href="#" class="blog-card">
  <div class="card-image">
    <img src="..." alt="...">
  </div>
  <div class="card-content">
    <div class="card-header">
      <h3 class="card-title">Post Title Here</h3>
      <div class="arrow-icon">
        <!-- Arrow SVG -->
      </div>
    </div>
    <div class="card-meta">
      <span class="category">Business</span>
      <span class="separator">•</span>
      <span class="read-time">5 min</span>
    </div>
  </div>
</a>
```

## Blog Post Structure

```html
<!-- Post Navigation -->
<nav class="post-nav">
  <a href="template.html" class="post-nav-back">Back</a>
  <div class="post-meta">
    <span class="category">Business</span> • <span>2 min read</span>
  </div>
  <a href="#" class="post-nav-next">→</a>
</nav>

<!-- Post Header -->
<header class="post-header">
  <h1 class="post-title">Article Title</h1>
  <p class="post-excerpt">Article excerpt/summary...</p>
</header>

<!-- Featured Image -->
<div class="post-image">
  <img src="..." alt="...">
</div>

<!-- Post Content -->
<article class="post-content">
  <h2>Section Heading</h2>
  <p>Paragraph content...</p>
</article>
```

## Section Selection

| Section | Use When |
|---------|----------|
| Hero + Subscribe | Always — establishes brand + captures emails |
| Tag Filters + Search | Always — above blog grid for navigation |
| Blog Grid (3-col) | Main content listing |
| Sidebar Nav | Desktop — icon navigation with black text |
| Sidebar Pinned Post | Feature best/evergreen content |
| Sidebar Subscribe | "Stay in the loop" + email form |
| Sidebar Footer | Year + creator attribution |
| Mobile Menu | Tablet/mobile — slide-out navigation |
| Footer CTA | Additional subscribe opportunity |

## Layout Specs

- **Container max-width**: 900px (content area)
- **Sidebar width**: 200px (fixed, desktop only)
- **Blog grid**: 3 columns at 16px gap
- **Card image ratio**: 4:3
- **Card border-radius**: 8px outer, 4px for image
- **Section padding**: 48px vertical

## Responsive Breakpoints

```css
/* Desktop: min-width 1200px */
/* Tablet: 810px - 1199px */
/* Mobile: max-width 809px */
```

- Desktop: Sidebar visible, 3-column grid
- Tablet: Sidebar hidden, 2-column grid
- Mobile: Full-width cards, hamburger menu

## Micro-Interactions

Include JS for:
- Card hover: Image scale (1.02×) + lift shadow
- Arrow icon: Rotate 45° on card hover
- Form submit: Button pulse animation
- Scroll reveal: Fade-up on blog cards (staggered 100ms)
- Mobile menu: Slide-in from left
- `prefers-reduced-motion` respected

## Accessibility

Built-in accessibility features:
- Skip link ("Skip to content") for keyboard users
- Focus-visible states on all interactive elements
- WCAG AA compliant contrast (4.5:1 minimum)
- Visually-hidden labels on search inputs
- Semantic HTML structure (nav, main, article, header)
- `loading="lazy"` on below-fold images
- `prefers-reduced-motion` respected

## Design Tokens

See `references/design-tokens.md` for complete values.

Key tokens:
- Background: `#F4F2F0`
- Card: `#FFFFFF`
- Text: `#000000`
- Text muted: `rgba(0, 0, 0, 0.48)`
- Border: `rgba(0, 0, 0, 0.12)`
- Accent bg: `#EDEAE7`
- Card radius: `8px`
- Button radius: `12px`

## Output Checklist

Every Memoir Blog design should have:
- [ ] #F4F2F0 creamy background
- [ ] Manrope for headlines and UI
- [ ] Source Serif 4 italic for emphasis
- [ ] -0.06em letter-spacing on headlines
- [ ] 3-column blog card grid
- [ ] Arrow-up-right icons in cards
- [ ] Category • Read time metadata
- [ ] Email subscribe form (hero + sidebar)
- [ ] White cards with 8px radius
- [ ] Sidebar with black text (opacity 0.6 inactive)
- [ ] Author profile (avatar + name + role) at top
- [ ] Nav item counts (Letters 6) and external arrows
- [ ] Pinned post card in sidebar
- [ ] "Stay in the loop" subscribe section
- [ ] Footer with year + creator credit
- [ ] Tag filter pills above grid
- [ ] Search bar with icon
- [ ] Blog post template with Back/Next navigation
- [ ] Post header: title + excerpt + featured image
- [ ] Post content: h2 headings + paragraphs (max-width: 65ch)
- [ ] Responsive at 1200px, 810px breakpoints
- [ ] Working hover states and transitions
- [ ] Skip link for keyboard navigation
- [ ] Focus-visible states on interactive elements
- [ ] WCAG AA contrast (text-muted: rgba(0,0,0,0.64))
- [ ] Accessible labels on form inputs
- [ ] loading="lazy" on below-fold images

---

## Design Tokens (Complete Reference)

# Memoir Blog Design Tokens

## Colors

### Core Palette
```css
:root {
  /* Backgrounds */
  --bg-primary: #F4F2F0;       /* Main page background */
  --bg-card: #FFFFFF;          /* Blog card background */
  --bg-accent: #EDEAE7;        /* Section accents, pills */
  --bg-nav: #EDEAE7;           /* Sidebar/nav background */
  
  /* Text */
  --text-primary: #000000;
  --text-muted: rgba(0, 0, 0, 0.64);   /* WCAG AA compliant on cream */
  --text-light: rgba(0, 0, 0, 0.24);
  
  /* Interactive */
  --btn-bg: #000000;
  --btn-text: #FFFFFF;
  --btn-hover: #1A1A1A;
  
  /* Borders */
  --border-subtle: rgba(0, 0, 0, 0.06);
  --border-default: rgba(0, 0, 0, 0.12);
  
  /* Warm Grays (from original) */
  --warm-100: #F4F2F0;
  --warm-200: #EDEAE7;
  --warm-300: #DAD3CE;
  --warm-400: #C3B8AE;
  --warm-500: #AA988D;
  --warm-600: #998276;
  --warm-700: #8C746A;
  --warm-800: #755F59;
}
```

## Typography

### Font Families
```css
:root {
  --font-display: "Manrope", sans-serif;
  --font-body: "Manrope", sans-serif;
  --font-accent: "Source Serif 4", serif;
}
```

### Font Sizes
```css
:root {
  /* Headlines */
  --text-hero: 64px;       /* Hero headline */
  --text-h1: 48px;         /* Section headlines */
  --text-h2: 32px;         /* Sub-headlines */
  --text-h3: 24px;         /* Card titles (large) */
  
  /* Body */
  --text-lg: 18px;         /* Large body */
  --text-base: 16px;       /* Default body */
  --text-sm: 14px;         /* Small text */
  --text-xs: 12px;         /* Metadata, captions */
  
  /* Responsive overrides */
  --text-hero-tablet: 56px;
  --text-hero-mobile: 40px;
}
```

### Letter Spacing
```css
:root {
  --tracking-tight: -0.06em;    /* Headlines */
  --tracking-tighter: -0.07em;  /* Italic accents */
  --tracking-normal: -0.02em;   /* Card titles */
  --tracking-wide: 0.04em;      /* Labels, buttons */
}
```

### Line Heights
```css
:root {
  --leading-tight: 110%;     /* Headlines */
  --leading-snug: 130%;      /* Card titles */
  --leading-normal: 150%;    /* Body text */
  --leading-relaxed: 170%;   /* Long-form content */
}
```

## Spacing

### Base Scale
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
}
```

### Layout
```css
:root {
  --container-max: 900px;
  --sidebar-width: 200px;
  --section-padding: 48px;
  --grid-gap: 16px;
  --card-padding: 12px;
}
```

## Border Radius

```css
:root {
  --radius-sm: 4px;       /* Image corners, small pills */
  --radius-md: 8px;       /* Cards, inputs */
  --radius-lg: 12px;      /* Buttons, large elements */
  --radius-xl: 16px;      /* Modal, overlay */
  --radius-full: 9999px;  /* Pills, avatars */
}
```

## Shadows

```css
:root {
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-card-hover: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-dropdown: 0 8px 24px rgba(0, 0, 0, 0.12);
  --shadow-modal: 0 16px 48px rgba(0, 0, 0, 0.16);
}
```

## Transitions

```css
:root {
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --transition-spring: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Z-Index

```css
:root {
  --z-base: 1;
  --z-card: 10;
  --z-sticky: 100;
  --z-nav: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;
}
```

## Breakpoints

```css
/* Use in media queries */
--breakpoint-sm: 640px;
--breakpoint-md: 810px;
--breakpoint-lg: 1200px;

/* Recommended patterns */
@media (max-width: 809px) { /* Mobile */ }
@media (min-width: 810px) and (max-width: 1199px) { /* Tablet */ }
@media (min-width: 1200px) { /* Desktop */ }
```

## Icons

Arrow-up-right SVG (24×24):
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M7 7h10v10"/>
  <path d="M7 17 17 7"/>
</svg>
```

Common icons: Home, User, FileText, BookOpen, Mail, Link, Menu, X

## Templates

HTML starter templates: post.html template.html 
Source: `/mnt/skills/user/memoir-blog/assets/`
