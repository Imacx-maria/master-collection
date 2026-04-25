
# Neo-Brutalist Style Skill

Apply consistent Neo-Brutalist design patterns across all visual outputs including HTML pages, React components, and presentations.

## Display Typography & Hero Patterns

Brutalism is graphic confrontation. Display type is non-negotiable — small headlines kill the style.

**`display-xl` (160px, Anton 400)** — The brutal opening statement. Hero pages, manifesto pages, "WE ARE [X]" anchors. UPPERCASE always, tight letter-spacing (-0.02em), line-height crushed (0.92). One per page.

**`display-lg` (120px, Anton 400)** — Major section anchors, project openers, feature statements. Still aggressively large.

**`headline-lg` (64px, Anton 400)** — Sub-section titles, card headers, list anchors. The "small" headline option — and it's still 64px because brutalism has no room for timid type.

**Hero patterns by page type:**

- **Landing page hero** — Full-bleed `display-xl` headline, often clipped at the edge or mis-aligned with the grid for graphic tension. Mono `label-md` eyebrow above ("MANIFESTO" / "READ THIS"). Grid background visible behind. `5xl` (160px) vertical padding for full physical presence.
- **Project / showcase page** — `display-lg` project title, often stacked across multiple lines for graphic weight. Hard-shadow offsets on accompanying buttons. `4xl` (96px) vertical padding.
- **Manifesto / about** — `display-xl` for the opening declaration, then mono body text with wide tracking. The contrast between display drama and mono utility is the point.
- **Index / archive** — Each entry uses `headline-lg` aggressively (one per row). Grid background structures the layout.

**Spacing for graphic structure:**

- Hero sections: `5xl` (160px) vertical padding — brutalism needs physical room
- Section dividers: `4xl` (96px) between major sections, with hard-shadow offset elements as accent if needed
- Inside cards: `lg` (24px) — keep cards tight and rectangular, the grid does the breathing
- Card grids: `grid` (60px) gap matches the background grid — always align to 60px increments
- Hard-shadow offsets: typically `8px 8px 0 var(--color-primary)` — tied to spacing scale via `xs` (4px) or `sm` (8px) increments

## Core Design Principles

1. **Sharp, Bold Typography**: Anton for display (headlines), Roboto Mono for body/metadata
2. **High Contrast**: Strong black/white or dark/light contrast with minimal gray tones
3. **Zero Border Radius**: All elements have sharp, 90-degree corners
4. **Grayscale Images**: Images default to grayscale with color on hover
5. **Grid Backgrounds**: 60px or 40px grid patterns at low opacity
6. **Thick Borders**: 1-2px borders on cards and containers
7. **Uppercase Everything**: All text in uppercase with wide letter-spacing
8. **Minimal Animation**: Subtle, purposeful transitions (0.3s - 1s)

## When to Use This Skill

Use this skill whenever:
- Creating a landing page, website, or web application
- Building React components for a Neo-Brutalist project
- Designing presentations with brutalist aesthetics
- The user asks for "brutalist", "neo-brutalist", "minimalist", or "high-contrast" styles
- Creating visual content that should have bold, modern, edgy design

## Quick Start

### For HTML Websites

1. Copy the base HTML template from `assets/html-template.html`
2. The template includes:
   - CSS variables for light/dark mode theming
   - Tailwind CSS configuration
   - Font imports (Anton, Roboto Mono)
   - Global grid background
   - Scrollbar styling

### For React Components

1. Use component templates in `assets/`:
   - `react-component-card.tsx` - Card component
   - `react-component-button.tsx` - Button component
2. Apply Tailwind classes following the patterns
3. Reference `assets/tailwind-config.js` for theme configuration

### For Presentations (PowerPoint)

When creating slides:
1. Use **Anton** for slide titles (80pt - 120pt)
2. Use **Roboto Mono** for body text (14pt - 18pt)
3. Apply color scheme:
   - Dark background: #181818
   - Text: #DDDDDD
   - Accent: #5F5F5F
4. Add grid patterns as background (60px squares)
5. Use grayscale images with high contrast
6. Sharp corners on all shapes (no rounded corners)

## Design Tokens Reference

For detailed color values, typography scales, and spacing guidelines, see `references/design-tokens.md`.

Key tokens:
- **Light Mode**: #FFFFFF bg, #181818 text, #888888 accent
- **Dark Mode**: #181818 bg, #DDDDDD text, #5F5F5F accent
- **Display Font**: Anton (uppercase, tight tracking)
- **Mono Font**: Roboto Mono (uppercase, wide tracking)
- **Grid**: 60px x 60px (main), 40px x 40px (detail)

## Component Patterns

For ready-to-use component code snippets, see `references/component-patterns.md`.

Common patterns include:
- Cards with hover shadow effects
- Buttons with slide-up background fill
- Full-screen modals with curtain transitions
- Hero headers with layered images
- Form inputs with bottom borders
- Grid background overlays

## Implementation Workflow

1. **Start with structure**: Use HTML template or React component templates
2. **Apply typography**: Anton for headlines, Roboto Mono for everything else
3. **Set up theming**: Use CSS variables for colors to support light/dark mode
4. **Add grid background**: Fixed position grid at low opacity
5. **Style components**: Sharp corners, thick borders, high contrast
6. **Image treatment**: Grayscale default, color on hover
7. **Add interactions**: Subtle hover effects (transform, shadow, color changes)

## Color Mode Toggle

Always provide a theme toggle when implementing:

```jsx
const [theme, setTheme] = useState('dark');

useEffect(() => {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}, [theme]);
```

## Best Practices

- **Keep it minimal**: Less is more - avoid clutter
- **Emphasize hierarchy**: Use size and weight for visual hierarchy
- **Consistent spacing**: Use 4px, 8px, 16px, 24px, 32px, 60px multiples
- **High contrast text**: Always ensure text is readable (WCAG AA minimum)
- **Purposeful animation**: Only animate on user interaction (hover, click)
- **Grid alignment**: Align elements to the grid when possible
- **Sharp transitions**: Use cubic-bezier for snappy, mechanical feel

## Common Tailwind Class Combinations

```jsx
// Card
"bg-background-light border border-primary shadow-lg hover:translate-x-[-4px] hover:translate-y-[-4px] hover:shadow-[8px_8px_0_var(--color-primary)]"

// Button
"font-mono text-sm uppercase tracking-[0.2em] border border-primary px-8 py-4 hover:bg-primary hover:text-background-dark transition-colors duration-300"

// Headline
"font-display text-6xl md:text-8xl uppercase leading-[0.95] text-primary"

// Metadata
"font-mono text-xs uppercase tracking-widest text-accent"

// Image
"grayscale contrast-125 group-hover:grayscale-0 group-hover:contrast-100 transition-all duration-700"
```

## Responsive Design

- **Mobile**: Single column, larger touch targets, simplified layouts
- **Tablet**: 2-column grids, moderate spacing
- **Desktop**: 3-column grids, full visual effects, larger typography

Always test at breakpoints: 640px (sm), 768px (md), 1024px (lg), 1728px (max-width)

## Output Quality Standards

Every Neo-Brutalist design should have:
- [ ] Sharp corners on all elements
- [ ] Anton font for display text
- [ ] Roboto Mono font for body/labels
- [ ] All text in uppercase
- [ ] High contrast (4.5:1 minimum ratio)
- [ ] Grid background pattern
- [ ] Grayscale images by default
- [ ] 1-2px borders on containers
- [ ] Theme toggle (for web)
- [ ] Consistent spacing system

---

## Design Tokens (Complete Reference)

# Neo-Brutalist Design Tokens

## Color Palette

### Light Mode
```css
--color-primary: #181818      /* Main text and borders */
--color-bg-light: #FFFFFF     /* Card backgrounds */
--color-bg-dark: #EAEAEA      /* Page background */
--color-accent: #888888       /* Secondary text and subtle elements */
```

### Dark Mode
```css
--color-primary: #DDDDDD      /* Main text and borders */
--color-bg-light: #2A2A2A     /* Card backgrounds */
--color-bg-dark: #181818      /* Page background */
--color-accent: #5F5F5F       /* Secondary text and subtle elements */
```

## Typography

### Display Font
- **Family**: Anton
- **Usage**: Large headlines, hero text, titles
- **Style**: Uppercase, tight letter-spacing (-0.02em)
- **Sizes**: 60px - 180px (responsive)

### Monospace Font
- **Family**: Roboto Mono
- **Weights**: 400 (regular), 700 (bold)
- **Usage**: Body text, labels, metadata, buttons
- **Style**: Uppercase, wide letter-spacing (0.15em - 0.2em)
- **Sizes**: 10px - 16px

## Spacing & Layout

### Grid System
- **Pattern**: 60px x 60px grid (main sections)
- **Pattern**: 40px x 40px grid (detail sections)
- **Opacity**: 0.15 for main, 0.03 for subtle
- **Color**: Uses accent color variable

### Max Width
- **Container**: 1728px
- **Content**: Center-aligned with padding

## Border & Shape

### Borders
- **Width**: 1px (subtle), 2px (prominent)
- **Color**: Primary or accent
- **Radius**: 0px (sharp corners always)

### Shadows
- **Card Hover**: 8px 8px 0 var(--color-primary)
- **Offset**: -4px, -4px on hover

## Image Treatment

### Default State
```css
filter: grayscale(100%) contrast(125%)
```

### Hover State
```css
filter: grayscale(0%) contrast(100%)
transform: scale(1.05)
```

### Transition
```css
transition: filter 0.7s ease, transform 0.7s ease
```

## Effects

### Backdrop Blur
```css
backdrop-filter: blur(12px)
background: var(--color-bg-dark)
opacity: 0.8 - 0.95
```

### Mix Blend Mode
- Use `mix-blend-difference` for text overlays
- Use `mix-blend-screen` for image overlays (optional, mobile)

### Transitions
- **Colors**: 0.3s - 0.5s ease
- **Transforms**: 0.7s - 1s ease
- **Theme Toggle**: 0.5s ease

## Aspect Ratios

- **Portrait Cards**: 3:4 or 4:5
- **Landscape Cards**: 16:9 (video)
- **Square**: 1:1 (minimal usage)

---

## Component Patterns

For complete component code snippets, read the original skill's component-patterns reference.
Source: `/mnt/skills/user/neo-brutalist-style/references/component-patterns.md`

## Templates

HTML starter templates: html-template.html 
Source: `/mnt/skills/user/neo-brutalist-style/assets/`
