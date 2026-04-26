# Base Frontend Principles

Universal rules that apply regardless of which style library is chosen. Load this alongside any style library, and always during Phase 3 (BUILD) and Phase 4 (REVIEW).

## Typography

- **Never** use generic system fonts (Arial, Helvetica) unless a style explicitly specifies them
- **Always** pair a display/headline font with a body font — one is never enough, three is a mess
- Use CSS `clamp()` for fluid type scaling: `font-size: clamp(2rem, 5vw + 1rem, 4rem)`
- Maintain consistent heading hierarchy (h1 > h2 > h3) — no skipping levels
- Body text minimum 16px on desktop, 14px absolute floor on mobile
- Line-height: 1.5–1.7 for body, 1.0–1.2 for display
- Letter-spacing: tighten **non-condensed** display (-0.02em to -0.06em), widen labels/caps (+0.04em to +0.18em). For **condensed/heavy** display (Anton, Bebas, Druk, Inter Black, etc.) use the tier-based scale in `typography-safety.md` (hero >60px = 0 minimum; section 32-60px = 0.01em; card title <32px = 0.02em). Compressing condensed type below these floors causes letter collisions — see Q19.

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
- **Never use bare element selectors for structural CSS** (`position`, `z-index`, `display: fixed/absolute`, layout-defining width/height). HTML semantic elements like `<nav>`, `<section>`, `<header>`, `<footer>`, `<aside>` are commonly reused multiple times per page (a top nav + footer nav columns + sidebar nav). A rule like `nav { position: fixed; top: 0 }` will pin EVERY nav on the page to the top-left, including the ones inside the footer. **Always scope structural rules with an ID or class** (`#site-nav { position: fixed }` or `.site-nav { ... }`). Reserve bare element selectors for typography defaults (`h1, h2, h3 { font-family }`), reset (`* { box-sizing }`), or behavioural defaults (`a { color: inherit }`) — never for layout positioning. This is the creative-studio failure mode: footer's `<nav class="ft-col">` rendered fixed at top:0 left:0 because the global `nav { position: fixed }` rule was greedy.

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
- ❌ Bare element selectors for structural CSS (`nav { position: fixed }`, `section { display: grid }`, `aside { width: 300px }`). Always scope with ID or class — bare selectors hit every instance of the element on the page, including nested ones in unexpected places (footer navs, sidebar asides, etc.)

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

### Surface-Context Discipline (sub-checks for question 6 — Contrast)

These catch a class of failure where text becomes invisible because its colour was inherited from the *parent section's* surface context instead of being scoped to the *immediate surface* it sits on. This is the bug behind testimonial cards going white-on-white when nested in dark sections, and partner labels going dark-on-dark in dark cards.

17. **Surface-scoped text colour.** Every text colour is bound to the *immediate surface* it sits on, not inherited from the section/page context. When a light card is nested inside a dark section (or a dark card inside a light section), the card resets its text colours to its own surface context — never inherits.

    **Audit test:** mentally flip every surface (every dark surface becomes light, every light surface becomes dark). Walk through every text element. If any text becomes invisible, illegible, or fails 4.5:1 contrast against its *new* surface, the colour was inherited instead of scoped — refactor.

    **Practical rule:** text inside a `.card` / `.testimonial` / `.callout` / `.panel` reads its colour from the card's local context (`--text-on-card-surface`), not from the body's `--text-default`. Always namespace text-colour vars by surface, or always re-declare them inside the local component.

    **Common failures this catches:**
    - Testimonial card with light bg nested in dark section → name goes white-on-white
    - Partner card with dark bg in light grid → role label goes dark-on-dark
    - Tab panel with inverted bg vs page → secondary text inherits page-default colour
    - Modal/dialog opens over dark page but uses light surface → headline inherits the page's white-text rule

### Type-System Discipline (sub-checks for question 4 — Typography)

Run these in addition to the typography question above. They catch failures specific to mixed-font pairings and condensed/heavy display type.

18. **Mixed-font pairing weight contrast.** When two type styles pair on the same line, headline, or paragraph (e.g., serif heavy + sans for an inline accent, or sans + italic serif for emphasis), **at least ONE part must be ≤400 (light/regular)**.

    - **Heavy + Heavy = forbidden** (the two styles compete; reads as accidental, not designed)
    - **Heavy + Light = ideal** (clearest weight contrast; the light part lets the heavy part dominate intentionally)
    - **Light + Light = acceptable** (low-key, restrained; works for editorial/literary contexts)
    - **Sans regular (400) inside serif heavy headline = OK** as long as the sans is not also heavy

    **Audit test:** for every headline or paragraph that mixes fonts, check the computed weight of each segment. If both segments are ≥500, refactor — usually the secondary font drops to 300 (Light) or stays at 400 (Regular).

    **Why this matters:** weight contrast is what makes a serif/sans pairing read as one composed phrase rather than two competing words. Without it, the eye doesn't know which to read first.

19. **Tier-based letter-spacing for condensed/heavy display.** Condensed grotesks (Anton, Bebas Neue, Druk Condensed, Acumin Condensed Heavy, etc.) and heavy weights (700+) of any sans collide at small sizes — bowls of B/O/R/D touch and the text reads as a black slab. Letter-spacing must scale **inversely** with size:

    - **Hero display (>60px)** → `letter-spacing: 0` is fine (sometimes even -0.01em for editorial impact)
    - **Section heading (32–60px)** → `letter-spacing: 0.01em` minimum
    - **Card title / subhead (<32px)** → `letter-spacing: 0.02em` minimum
    - **Uppercase label (≤14px)** → `letter-spacing: 0.04–0.12em` (existing rule, unchanged)

    See `typography-safety.md` § "Tier-based letter-spacing for condensed/heavy display" for the full contract and convergent-failure cases (uppercase + condensed + heavy + small-size = compounded compression).

    **Audit test:** for every condensed or heavy headline below 60px, measure (visually or in DevTools) whether B/O/R/D bowls touch. If yes, increase letter-spacing to the next tier and re-check.

### Layout-Width Discipline (sub-checks for question 7 — Mid-width breakage)

These catch failures specific to multi-column grids where text content is squeezed at intermediate widths. Run at 900px, 1100px, and 1280px viewports — the danger zones for column collapse.

20. **Column min-width on multi-col grids with text content.** Every grid column that holds text (lists, paragraphs, KPI labels, form fields) must have an explicit `minmax(<floor>, 1fr)` rather than bare `1fr`. Bare `1fr` allows the column to shrink below readable threshold when the sibling column claims more intrinsic space, causing **word-per-word breakdown** (each word renders on its own line because the column is narrower than the longest word).

    **Audit test:** at 900px and 1100px viewports, scan every multi-column section. If any text item breaks word-per-word, the column has insufficient floor. Fix: add `minmax(<content-floor>, 1fr)` per the recipes in `layout-patterns.md` § Failure 8.

    **Common offenders:**
    - Tab content with `[copy] [list]` 2-col layout — list column collapses
    - Service card grid where one card has long title — others squeeze
    - Form layouts with `[label] [input]` 2-col — label column collapses on long labels
    - Side-by-side comparison sections (before/after, light/dark, before-fix/after-fix)

21. **Stat / KPI / feature block baseline alignment.** When a row of cells contains `[number/figure] [description]` and the description copy varies in line count across cells (one cell has 1-line description, others have 2-line), the cells will misalign vertically — the 1-line cell's content sits higher than its siblings, breaking the visual baseline.

    **Audit test:** for every row of stats / KPIs / feature cards, count the lines in each cell's description. If line count varies, verify the cells use either grid-template-rows shared across the parent, or `min-height` on the description element, or `align-items: end` on the description (per `layout-patterns.md` § Failure 9). If none of these are present and line count varies → refactor.

    **Visual symptom:** one stat in a 4-stat row "floats" — its number aligns with neighbours but its description ends earlier, leaving visual whitespace below it that reads as broken.
