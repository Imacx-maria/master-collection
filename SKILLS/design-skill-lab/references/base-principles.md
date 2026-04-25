# Base Frontend Principles

Universal rules that apply regardless of which style library is chosen. Load this alongside any style library, and always during Phase 3 (BUILD) and Phase 4 (REVIEW).

## Typography

- **Never** use generic system fonts (Arial, Helvetica) unless a style explicitly specifies them
- **Always** pair a display/headline font with a body font — one is never enough, three is a mess
- Use CSS `clamp()` for fluid type scaling: `font-size: clamp(2rem, 5vw + 1rem, 4rem)`
- Maintain consistent heading hierarchy (h1 > h2 > h3) — no skipping levels
- Body text minimum 16px on desktop, 14px absolute floor on mobile
- Line-height: 1.5–1.7 for body, 1.0–1.2 for display
- Letter-spacing: tighten display (-0.02em to -0.06em), widen labels/caps (+0.04em to +0.18em)

## Color & Theme

- Define all colors as CSS custom properties in `:root`
- Support dark/light themes when appropriate (not all styles need both — editorial, warm, memoir often don't)
- Ensure WCAG AA contrast minimums: 4.5:1 for body text, 3:1 for large text and UI components
- Use a dominant color + sharp accent approach, not evenly distributed palettes (60-30-10 is a good default)
- Never use an accent color as the dominant surface color
- Dark themes: avoid pure #000 backgrounds — use #0A0A0A to #141414 range for less eye strain

## Layout

- Use CSS Grid or Flexbox, never floats
- Define a max-width container (typically 1200–1440px for content, up to 1600px for image-led work)
- Consistent spacing scale based on multiples — most styles use 4/8/16/24/32/48/64/96/128
- Mobile-first responsive design — start narrow, expand up
- Test widths at 375px, 768px, 1024px, 1280px, 1440px minimum — mid-widths break more often than extremes
- Avoid centering everything; asymmetry and off-grid moments add character

## Interaction

- Meaningful hover states — not just color changes. Transforms, reveals, inversions, underline slides
- 44px minimum touch targets on mobile (WCAG 2.2)
- Transitions: 150–250ms for UI, 400–700ms for reveals and page transitions
- Cubic-bezier easing for personality: `cubic-bezier(0.4, 0, 0.2, 1)` standard, `cubic-bezier(0.68, -0.55, 0.265, 1.55)` for playful overshoot
- Prefer CSS transitions over JS animations for simple effects
- Respect `prefers-reduced-motion` — wrap animations in the media query

## Accessibility

- Semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<section>`, `<header>`, `<footer>`)
- Focus outlines that match the design system — never remove, always restyle
- Alt text on all images; decorative images get `alt=""`
- Label form inputs with `<label>` or `aria-label`
- Color is not the only means of conveying information — pair with text, icons, or position
- Reduced motion media query for users who prefer it
- Keyboard navigation works for every interactive element

## Code Quality

- Use design tokens for everything — no magic hex values, no magic pixel values, no inline styles
- CSS custom properties for colors, spacing, radii, transitions, shadows
- One CSS file per component when working in a framework; one file only when building HTML artifact
- Comment the *why*, not the *what* — `// primary accent` not `// #2DD4CD`

## Universal Anti-Patterns

Never ship with any of these:

- ❌ Generic AI slop — purple gradients on white, Inter everywhere, cookie-cutter rounded cards
- ❌ Decorative elements without purpose
- ❌ Inconsistent spacing or ad-hoc magic numbers
- ❌ Missing `:hover` / `:focus` states
- ❌ Layouts that break between 768px and 1024px
- ❌ Multiple conflicting font families (2 is a pair, 3+ is a mess)
- ❌ Pure #000 on pure #FFF (too harsh; use #0A0A0A on #FAFAFA or similar)
- ❌ Tiny body text (below 14px)
- ❌ Line length longer than 75ch or shorter than 45ch for body copy
- ❌ Disabled states that look enabled (or enabled states that look disabled)
- ❌ Icon-only buttons without accessible labels
- ❌ Carousels without keyboard controls
- ❌ Modals without escape-key close and focus trap

## Working with Templates

Several style libraries include HTML template files in their `assets/` directories. When a template exists:

1. Copy it as the starting point — don't build from scratch
2. Replace `<!-- SLOT: ... -->` placeholders with real content
3. **Apply the project-specific DESIGN.md tokens** — not the library defaults. This is where the divergence rule materialises.
4. Add/remove sections based on the specific project needs

Template locations are noted in each style's reference file.

## Universal Review Questions

Run these in Phase 4, regardless of style:

1. **First impression (5-second test).** Can a new user identify what this is and what to do within 5 seconds?
2. **Hierarchy.** Does the most important thing on the page look the most important?
3. **Alignment.** Do key edges, captions, and buttons share a deliberate grid?
4. **Typography.** Is there a clear scale? Are there more than 2 font families? Is body text ≥16px?
5. **Color.** Is there a clear 60-30-10 distribution? Does the accent do focused work?
6. **Contrast.** Does body text pass WCAG AA? Do UI components pass 3:1?
7. **Mid-width breakage.** Test at 900px and 1100px — the danger zones.
8. **Focus states.** Tab through the page. Is every focus state visible and on-brand?
9. **Motion.** Does it support the style, or distract from it? Does it respect reduced-motion?
10. **Reference fidelity.** If an inspiration was given, does the output borrow systems without copying surface?

### Layout Integrity (sub-checks for question 3 — Alignment)

Run these in addition to the alignment question above. They catch the most common composition failure modes. See `layout-patterns.md` for full detail.

11. **Alignment consistency.** Does each section's content (grid, list, cards) align with that section's header? If the header is centred, the items below should be centred too — not left-aligned items under a centred header.
12. **Orphan detection.** For every uniform grid: is `items_count % columns == 0` at every breakpoint? Lone cards on the last row are a layout bug. Fix in this priority: (a) cut/add items, (b) switch the breakpoint's column count, (c) — **only if the content already has natural hierarchy AND the chosen style supports bento** — refactor to bento. Never use bento as a generic orphan fix.
13. **Span hierarchy makes sense.** If a bento or hero+supporting layout is used, does the largest span hold the most important content? A "hero" card with a footnote inside it is wrong.
14. **Pattern fits content type.** Sequential / chronological content (timelines, schedules) uses uniform grid or list — never bento (varied sizes imply hierarchy that isn't there).
15. **Container width consistency.** Do all sections use the same `max-width` container? Switching between 1100px and 1400px between sections creates visual jitter.
16. **List width matches content shape.** If a section uses a vertical list (Pattern C), is the width correct for the content type? **Reading lists** (prose paragraphs, FAQs, articles) → narrow column ~720px. **Horizontal row lists** (schedules, line items, comparison rows, `[label] [value]` pairs) → full container width, same as every other section. A schedule rendered narrow inside a wide container is a layout bug — the empty space to the right reads as an unfinished section. See `layout-patterns.md` Pattern C1 vs C2.
