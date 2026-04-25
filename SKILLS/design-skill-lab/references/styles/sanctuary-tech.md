
# Sanctuary Tech Design System

A design system for contexts where users are stressed, vulnerable, or in crisis. The aesthetic communicates safety, restraint, and trustworthiness through deliberate visual choices.

## Display Typography & Hero Patterns

**Sanctuary deliberately has no `display-xl` or `display-lg` tokens.** This is not an oversight — large display type signals marketing energy ("LAUNCH! NEW! BIG!") which is exactly the wrong emotional register for crisis tools. A user in distress reading a 144px headline feels shouted at, not helped.

**`headline-lg` (40px, DM Mono 500)** — The largest headline this system permits. Use for page titles ("Get Help Now", "Crisis Resources"). Mono signals straightforward honesty, not corporate marketing. Letter-spacing tight (-0.01em) for legibility under stress.

**`headline-md` (24px, DM Mono 500)** — Section headers, panel titles, sub-page anchors. The workhorse for content hierarchy.

**`body-md` (15px, DM Mono 400)** — Body content. Slightly smaller than other systems (15px vs 16px) because mono fonts read denser; this preserves comfortable line length under stress. Line-height generous (1.7) for breathing room.

**`label-md` (12px, DM Mono 500)** — Metadata, timestamps, system labels. Same family throughout — no font-switching to signal "this is special".

**Hero patterns by page type — restrained by design:**

- **Crisis homepage** — `headline-lg` page title (e.g., "If you need help now, you're in the right place"). Single primary action below. No imagery, no animation, no visual flourish. `4xl` (120px) vertical padding for generous breathing — the whitespace IS the safety signal.
- **Resource page** — `headline-lg` for the resource name, `body-md` for what it does, contact action visible without scroll. Single column, max 60ch line length.
- **Help / FAQ** — `headline-md` per question, `body-md` answers. Dashed-panel components frame related content. `xl` (48px) between Q&A pairs.
- **Form pages (e.g., contact)** — `headline-lg` for the page intent ("How can we help?"), then form. Each field clearly labeled, generous touch targets.

**Spacing for safety:**

- All page sections: `4xl` (120px) vertical padding minimum — whitespace is a safety feature, not waste
- Between content blocks: `xl` (48px) for clear visual separation without crowding
- Inside cards/panels: `lg` (32px) padding — never less, the breathing space lets users feel calm
- Form fields: `md` (20px) between fields (not `sm`) — reduces submission stress
- Touch targets: minimum 44px (WCAG 2.2), padded with `pad-button` (16px) on buttons
- Page max-width: 720px for content (forces short line lengths, easier to read under stress)

**Why no display tokens here matters:**

If a brief asks for Sanctuary Tech but also wants "a bold hero with massive headline", that's a signal the brief is wrong for this style. Either downgrade to `headline-lg` (the system's max) or switch to a different style library — don't betray the trauma-informed contract by adding display tokens just for visual punch.

## Core Philosophy

**Restraint over persuasion.** This is NOT a marketing aesthetic. It doesn't try to sell, excite, or convert. It creates a calm space where users feel safe enough to complete difficult tasks.

**The design should feel like:**
- A quiet library, not a billboard
- A trusted professional, not a salesperson
- A deep breath, not a call to action

## When to Use This Skill

Use for:
- Crisis support tools (suicide prevention, abuse hotlines, victim services)
- Privacy/security tools (data removal, harassment protection)
- Healthcare interfaces (patient portals, mental health apps)
- Legal aid tools (rights information, complaint filing)
- Any context where users are anxious, scared, or vulnerable

Do NOT use for:
- Marketing sites optimized for conversion
- E-commerce or product showcases
- Entertainment or social apps
- Anything that needs to feel exciting or energetic

## Design DNA

| Element | Choice | Why |
|---------|--------|-----|
| Typography | Monospace primary | Feels technical, honest, no-nonsense |
| Borders | Dashed, never solid | Gentle, tentative, non-aggressive |
| Accent | Single muted color | Reduces visual stress |
| Whitespace | Generous (60%+ of viewport) | Breathing room, reduces overwhelm |
| Animation | Minimal, functional only | No distraction, no anxiety triggers |
| Imagery | Abstract or none | Avoids triggering content |

## Quick Start

### For HTML/CSS

1. Copy the base template from `assets/html-template.html`
2. The template includes CSS variables, font imports, and base styles
3. Reference `references/design-tokens.md` for the complete token system

### For React

1. Apply the design tokens via CSS variables or Tailwind config
2. Use component patterns from `references/component-patterns.md`
3. Follow the interaction guidelines (no aggressive animations)

## Typography

**Primary (body, UI):** DM Mono or JetBrains Mono
- Clean, readable monospace
- Use for body text, labels, buttons, navigation

**Secondary (headlines only):** Inter or system sans-serif
- Soft, humanist sans-serif
- Use ONLY for h1/h2 headlines
- Provides warmth without losing technical feel

**Type Scale:**
```
--text-xs: 0.75rem    /* 12px - labels, metadata */
--text-sm: 0.875rem   /* 14px - secondary text */
--text-base: 1rem     /* 16px - body */
--text-lg: 1.125rem   /* 18px - lead text */
--text-xl: 1.25rem    /* 20px - h3 */
--text-2xl: 1.5rem    /* 24px - h2 */
--text-3xl: 2rem      /* 32px - h1 */
--text-hero: clamp(2.5rem, 5vw, 3.5rem) /* hero */
```

**Line Heights:**
- Headlines: 1.1-1.25
- Body: 1.6-1.7 (generous for readability)
- Monospace body: 1.7-1.8 (needs more leading)

## Color System

**Light Mode (default):**
```css
--bg-primary: #fafafa      /* main background */
--bg-alt: #f5f5f5          /* section backgrounds */
--text-primary: #171717    /* headings */
--text-secondary: #525252  /* body text */
--text-tertiary: #a3a3a3   /* metadata, hints */
--border: #d4d4d4          /* dashed borders */
--accent: #16a34a          /* single accent (green = safety) */
--accent-dark: #15803d     /* accent hover/active */
```

**Dark Mode:**
```css
--bg-primary: #0a0a0a
--bg-alt: #171717
--text-primary: #fafafa
--text-secondary: #a3a3a3
--text-tertiary: #525252
--border: #404040
--accent: #22c55e
--accent-dark: #16a34a
```

**Why green?** Green signals safety, "go", permission. Avoid red (danger), orange (warning), or blue (corporate/cold) as primary accents for crisis tools.

## Signature Elements

### Dashed Borders

The defining visual element. Use everywhere instead of solid borders:

```css
border: 1px dashed var(--border);
```

Why dashed?
- Feels tentative, gentle, non-aggressive
- Creates separation without harsh lines
- Suggests "here's a boundary, but it's soft"

### Cards

```css
.card {
    background: var(--bg-primary);
    border: 1px dashed var(--border);
    border-radius: 4px;  /* subtle, not rounded */
    padding: 1.5rem;
}

.card:hover {
    border-color: var(--accent);
}

.card:focus-within {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
```

### Buttons

```css
.btn-primary {
    font-family: var(--font-mono);
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.875rem 1.5rem;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background 0.2s ease;
}

.btn-primary:hover {
    background: var(--accent-dark);
}

.btn-secondary {
    font-family: var(--font-mono);
    background: transparent;
    color: var(--text-primary);
    border: 1px dashed var(--border);
    border-radius: 4px;
    padding: 0.875rem 1.5rem;
}

.btn-secondary:hover {
    border-color: var(--accent);
    color: var(--accent);
}
```

### Quick Exit Button

**Required for crisis tools.** Always include a quick exit in top-left:

```html
<a href="https://google.com" class="quick-exit">
    ✕ Quick Exit
</a>
```

```css
.quick-exit {
    position: fixed;
    top: 1rem;
    left: 1rem;
    background: #dc2626;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    text-decoration: none;
    z-index: 9999;
}
```

## Layout Principles

### Whitespace

Use generous whitespace. When in doubt, add more:

```css
.section {
    padding: 5rem 0;  /* vertical breathing room */
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.content-narrow {
    max-width: 65ch;  /* optimal reading width */
}
```

### Text Alignment

- **Left-align all body text** (3+ lines)
- **Center only:** short headlines, taglines, hero text
- **Never center:** paragraphs, card content, lists

### Breakout Sections

For emphasis, break out of the container grid:

```css
.breakout {
    background: var(--bg-alt);
    padding: 3rem;
    margin: 0 2rem;  /* inset from edges */
    border-radius: 4px;
}
```

## Interaction Design

### Hover States

Subtle, functional, not playful:

```css
/* Good: color change */
.link:hover { color: var(--accent); }

/* Good: border emphasis */
.card:hover { border-color: var(--accent); }

/* Bad: bouncy animations */
.card:hover { transform: scale(1.05); } /* NO */

/* Bad: attention-grabbing effects */
.btn:hover { animation: pulse 0.5s infinite; } /* NO */
```

### Focus States

**Always visible.** Users in crisis may rely on keyboard navigation:

```css
:focus {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

:focus:not(:focus-visible) {
    outline: none;
}

:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
```

### Transitions

Keep them short and functional:

```css
transition: color 0.2s ease;
transition: border-color 0.2s ease;
transition: background 0.2s ease;
```

No transitions longer than 0.3s. No bounces, springs, or elastic effects.

## Content Guidelines

### Language

- Use "survivor" not "victim"
- Use "you" not "users" or "individuals"
- Avoid clinical or legal jargon
- Be direct but warm

### Consent

Always explain what happens before asking for action:

```
✓ "We'll generate a letter you can review before sending"
✗ "Submit your complaint"
```

### Progress Indication

Show where users are in multi-step processes:

```
Step 2 of 4 • Takes about 5 minutes
```

## Accessibility Requirements

These are non-negotiable for crisis tools:

- [ ] Color contrast: 4.5:1 minimum (WCAG AA)
- [ ] Focus indicators: Always visible
- [ ] Keyboard navigation: Full support
- [ ] Screen reader: Proper headings, labels, ARIA
- [ ] Reduced motion: Respect `prefers-reduced-motion`
- [ ] Touch targets: 44x44px minimum
- [ ] Zoom: Allow up to 200% without breaking

## Crisis Resources Section

For tools serving users in distress, include crisis resources prominently:

```html
<section class="crisis-section">
    <h2>Need immediate support?</h2>
    <p>If you're in crisis, these resources can help.</p>
    <div class="crisis-cards">
        <div class="crisis-card">
            <h3>National Hotline</h3>
            <a href="tel:1-800-XXX-XXXX">1-800-XXX-XXXX</a>
            <p>Available 24/7</p>
        </div>
        <div class="crisis-card">
            <h3>Crisis Text Line</h3>
            <p>Text HOME to 741741</p>
        </div>
    </div>
</section>
```

Style with warm background (not alarming):

```css
.crisis-section {
    background: #fef2f2;  /* soft pink, not aggressive red */
    border: 1px dashed #fca5a5;
    padding: 2.5rem;
    border-radius: 4px;
}
```

## Reference Files

- `references/design-tokens.md` - Complete token system (colors, spacing, typography)
- `references/component-patterns.md` - Ready-to-use component code
- `assets/html-template.html` - Base HTML template with all styles

## Output Quality Checklist

Every Sanctuary Tech design should have:

- [ ] DM Mono or similar monospace as primary font
- [ ] Dashed borders (never solid for decorative borders)
- [ ] Single muted accent color
- [ ] Generous whitespace (sections: 5rem+ padding)
- [ ] Left-aligned body text
- [ ] Visible focus states
- [ ] Quick exit button (for crisis tools)
- [ ] Crisis resources section (for crisis tools)
- [ ] No aggressive animations or attention-grabbers
- [ ] 4.5:1 color contrast minimum
- [ ] Content warnings where appropriate

---

## Design Tokens (Complete Reference)

# Sanctuary Tech Design Tokens

Complete token system for Sanctuary Tech interfaces.

## Colors

### Light Mode (Default)

```css
:root {
    /* Backgrounds */
    --bg-primary: #fafafa;
    --bg-alt: #f5f5f5;
    --bg-elevated: #ffffff;
    
    /* Text */
    --text-primary: #171717;
    --text-secondary: #525252;
    --text-tertiary: #a3a3a3;
    --text-inverse: #fafafa;
    
    /* Borders */
    --border: #d4d4d4;
    --border-light: #e5e5e5;
    --border-focus: #16a34a;
    
    /* Accent (Safety Green) */
    --accent: #16a34a;
    --accent-dark: #15803d;
    --accent-light: #22c55e;
    --accent-subtle: #dcfce7;
    
    /* Semantic */
    --warning-bg: #fef2f2;
    --warning-border: #fca5a5;
    --warning-text: #991b1b;
    --info-bg: #eff6ff;
    --info-border: #93c5fd;
    --info-text: #1e40af;
}
```

### Dark Mode

```css
[data-theme="dark"], .dark {
    --bg-primary: #0a0a0a;
    --bg-alt: #171717;
    --bg-elevated: #262626;
    
    --text-primary: #fafafa;
    --text-secondary: #a3a3a3;
    --text-tertiary: #525252;
    --text-inverse: #171717;
    
    --border: #404040;
    --border-light: #262626;
    --border-focus: #22c55e;
    
    --accent: #22c55e;
    --accent-dark: #16a34a;
    --accent-light: #4ade80;
    --accent-subtle: #14532d;
    
    --warning-bg: #450a0a;
    --warning-border: #7f1d1d;
    --warning-text: #fca5a5;
    --info-bg: #1e3a5f;
    --info-border: #1e40af;
    --info-text: #93c5fd;
}
```

## Typography

### Font Families

```css
:root {
    --font-mono: 'DM Mono', 'JetBrains Mono', 'Fira Code', monospace;
    --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}
```

### Font Imports

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale

```css
:root {
    --text-xs: 0.75rem;      /* 12px */
    --text-sm: 0.875rem;     /* 14px */
    --text-base: 1rem;       /* 16px */
    --text-lg: 1.125rem;     /* 18px */
    --text-xl: 1.25rem;      /* 20px */
    --text-2xl: 1.5rem;      /* 24px */
    --text-3xl: 2rem;        /* 32px */
    --text-4xl: 2.5rem;      /* 40px */
    --text-hero: clamp(2.5rem, 5vw, 3.5rem);
}
```

### Line Heights

```css
:root {
    --leading-none: 1;
    --leading-tight: 1.1;
    --leading-snug: 1.25;
    --leading-normal: 1.5;
    --leading-relaxed: 1.6;
    --leading-loose: 1.7;
    --leading-mono: 1.8;     /* extra space for monospace */
}
```

### Font Weights

```css
:root {
    --font-normal: 400;
    --font-medium: 500;
    --font-semibold: 600;
    --font-bold: 700;
}
```

### Letter Spacing

```css
:root {
    --tracking-tighter: -0.03em;
    --tracking-tight: -0.02em;
    --tracking-normal: 0;
    --tracking-wide: 0.02em;
}
```

## Spacing Scale

Based on 4px grid:

```css
:root {
    --space-0: 0;
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.25rem;   /* 20px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */
    --space-20: 5rem;     /* 80px */
    --space-24: 6rem;     /* 96px */
}
```

## Layout

```css
:root {
    /* Container widths */
    --container-sm: 640px;
    --container-md: 768px;
    --container-lg: 1024px;
    --container-xl: 1200px;
    
    /* Content widths */
    --content-narrow: 65ch;
    --content-wide: 80ch;
    
    /* Border radius */
    --radius-sm: 2px;
    --radius-md: 4px;
    --radius-lg: 8px;
    --radius-full: 9999px;
}
```

## Shadows

Minimal, functional shadows only:

```css
:root {
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    
    /* Focus ring */
    --ring-width: 2px;
    --ring-offset: 2px;
    --ring-color: var(--accent);
}
```

## Transitions

```css
:root {
    --transition-fast: 150ms ease;
    --transition-base: 200ms ease;
    --transition-slow: 300ms ease;
}
```

## Z-Index Scale

```css
:root {
    --z-dropdown: 100;
    --z-sticky: 200;
    --z-modal-backdrop: 400;
    --z-modal: 500;
    --z-toast: 600;
    --z-quick-exit: 9999;
}
```

## Breakpoints

```css
/* Mobile first breakpoints */
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
```

```css
/* Usage */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

## Complete CSS Variables Block

Copy this into your stylesheet:

```css
:root {
    /* Colors - Light Mode */
    --bg-primary: #fafafa;
    --bg-alt: #f5f5f5;
    --bg-elevated: #ffffff;
    --text-primary: #171717;
    --text-secondary: #525252;
    --text-tertiary: #a3a3a3;
    --text-inverse: #fafafa;
    --border: #d4d4d4;
    --border-light: #e5e5e5;
    --accent: #16a34a;
    --accent-dark: #15803d;
    --accent-light: #22c55e;
    --accent-subtle: #dcfce7;
    --warning-bg: #fef2f2;
    --warning-border: #fca5a5;
    
    /* Typography */
    --font-mono: 'DM Mono', 'JetBrains Mono', monospace;
    --font-sans: 'Inter', system-ui, sans-serif;
    
    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    --space-3xl: 4rem;
    --space-4xl: 5rem;
    
    /* Layout */
    --container-max: 1200px;
    --content-max: 65ch;
    --radius: 4px;
    
    /* Transitions */
    --transition: 200ms ease;
}
```

---

## Component Patterns

For complete component code snippets, read the original skill's component-patterns reference.
Source: `/mnt/skills/user/sanctuary-tech/references/component-patterns.md`

## Templates

HTML starter templates: html-template.html 
Source: `/mnt/skills/user/sanctuary-tech/assets/`
