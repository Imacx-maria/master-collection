# Layout Patterns

Composition decisions are not visual treatment — they are structural choices the agent must make explicitly. Tokens (colors, type, spacing) define how things look; layout patterns define how things are arranged.

Load this file in **Phase 3 (BUILD)** before generating markup, and consult during **Phase 4 (REVIEW)** for integrity checks.

---

## ⚠️ Bento is NOT the safe default

Bento is the **deliberate, opt-in** choice when:
1. The chosen style supports it (`playful-bento`, `spritify`, sometimes `creative-studio`), **AND**
2. The content has natural hierarchy — one item clearly anchors, others support.

**Both conditions must hold.** If either fails → bento is wrong, regardless of what would "look cool".

When in doubt: **uniform grid** (equal weight) or **list** (sequential). These are the safe defaults. Bento is the loud option that has to earn its place.

If your style is `editorial-portfolio`, `jocril-technical`, `basalt-ecommerce`, `memoir-blog`, `warm-serene-luxury`, `sanctuary-tech`, or `neo-brutalist` (when used reservedly) — **do not reach for bento as a fix-it tool**. The bento checks in this file apply *only when bento was correctly chosen*.

---

## The 4 Composition Patterns

Every section that holds multiple items uses one of these. Pick deliberately, never default.

### Pattern A — Bento Grid (mixed sizes, interlocked)

**What it is:** Cards of varying sizes (1×1, 2×1, 1×2, 2×2) packed into a master grid. No gaps in the layout — sizes vary, total area fills.

**When to use:**
- Style explicitly calls for it (`playful-bento`, often `spritify`, sometimes `creative-studio`)
- Content has natural hierarchy (one hero item + supporting items)
- 4–8 items where one or two deserve more visual weight
- Marketing or showcase contexts where rhythm matters

**When NOT to use:**
- Sequential / chronological lists (timelines, schedules) — equal weight per item
- Pure data tables
- More than ~10 items (gets chaotic)
- Style is restrained / editorial / sanctuary (wrong register)
- Style isn't `playful-bento` / `spritify` / `creative-studio` AND content has no hero item — **bento is not a generic fallback**
- You're reaching for bento to fix orphans in a uniform grid — **fix the grid, don't switch patterns**

**Implementation contract:** see `## Bento Grammar` below.

### Pattern B — Uniform Grid (equal sizes, flexible columns)

**What it is:** Same-size cards arranged in a regular grid. Column count fixed per breakpoint.

**When to use:**
- All items have equal weight (team members, schedule slots, equal-importance features)
- Content is browsable / scannable (no single hero)
- Predictable count (4 / 6 / 8 / 12 — multiples of breakpoint columns)

**When NOT to use:**
- Item count doesn't divide cleanly (5, 7 → órphans on last row)
- One item clearly deserves more weight (use Bento)
- Content is sequential and linear (use List)

**Critical rule — orphan prevention:**
If `items_count % columns != 0`, you have orphans. Fix with one of:
- Reduce `items` to a multiple of `columns` (cut weak items)
- Add items to fill last row
- Switch breakpoint columns (e.g., 5 items → 5-col grid not 4)
- Switch to Bento (give the orphan extra span to fill)

Never ship orphan rows in uniform grids. They look like a layout bug.

### Pattern C — List / Stack (vertical sequence)

List is **two distinct sub-patterns**. Pick the right one — they are not interchangeable.

#### C1 — Reading List (narrow column)

**What it is:** Items stacked vertically in a narrow reading-width column (max ~720px). Each item is text-heavy and gets read top-to-bottom.

**When to use:**
- Prose-heavy content: blog posts, FAQs, long testimonials, article lists
- Items where the body copy averages ≥80 characters per line at full width
- Reading-first contexts where eye fatigue at long line lengths is the real failure mode

**When NOT to use:**
- Items have a horizontal structure (label | content | meta) — use C2
- Items have little text (becomes a sparse skinny scroll inside an empty container)

#### C2 — Horizontal Row List (full container width)

**What it is:** Items stacked vertically but each row spans the **full container width**, with internal horizontal layout (e.g., `[time] [activity] [meta]`, `[icon] [title + body] [action]`, `[label] [value]`).

**When to use:**
- Sequential or comparable items with horizontal structure (schedules, timelines, line items, pricing rows, comparison tables, changelog entries, recent activity feeds)
- 4+ items where each row is short but the set is browsable
- Any list where shrinking width would leave a wide empty zone next to it

**When NOT to use:**
- Items are prose paragraphs (use C1)
- Items would look better grouped (use Grid)
- 10+ items with similar visual weight (consider 2-column row list to halve scroll)

**Width rule (universal):** A list's container width must match its **content shape**, not a fixed "reading width" default. If items are horizontal compositions, the list spans the same `max-width` as every other section in the page. A schedule rendered at 720px inside a 1280px container is a layout bug, not a stylistic choice.

**Optional variant — 2-column row list:** for 7+ horizontal-row items, split into two parallel columns (e.g., morning | afternoon, features | benefits). Halves vertical scroll without breaking sequentiality. Use only when the items partition naturally; never just to "fill space".

#### Common to both C1 and C2

**When NOT to use list at all:**
- 6+ items where browsing matters more than reading order (use Grid or Bento)
- Items with little content AND no natural sequence (becomes sparse — use Grid)

### Pattern D — Hero + Supporting (asymmetric pair)

**What it is:** One large item + 2–4 smaller items beside or below.

**When to use:**
- One item is clearly the main attraction (featured project, hero product, lead testimonial)
- The supporting items add context without competing
- 3 to 5 items total

**When NOT to use:**
- All items have equal importance
- Supporting items have substantial content (they get crushed)

---

## Bento Grammar (the structural contract)

A bento is a **12-column grid** with rows of fixed height, where each card spans a specific number of columns and rows. The total area covered must equal the grid area — no gaps, no overflow.

### Standard span vocabulary (12-col grid)

| Span name  | Cols | Rows | Use for |
|------------|------|------|---------|
| Hero       | 6    | 2    | The page's anchor card. One per bento. |
| Wide       | 6    | 1    | Secondary hero, paired with another wide or with hero. |
| Tall       | 3    | 2    | Vertical accent — quote, single-stat, illustration column. |
| Square     | 3    | 1    | Standard small card. The workhorse. |
| Half       | 6    | 1    | Same as Wide; alias for clarity. |
| Full       | 12   | 1    | Closing statement — full-width band inside bento. |
| Quarter    | 3    | 1    | Same as Square; alias. |
| Two-thirds | 8    | 1    | Asymmetric anchor when hero is too much. |
| One-third  | 4    | 1    | Pairs with two-thirds (8 + 4 = 12). |

### Patterns by item count

The agent **must** pick one of these patterns for the given count, not invent.

**3 items:**
```
┌─────── 6×2 hero ───────┬── 6×1 wide ──┐
│                        ├──────────────┤
│                        │── 6×1 wide ──│
└────────────────────────┴──────────────┘
```
Or: hero (6×2) + two squares (3×2 each) on the right, stacked.

**4 items:**
```
┌── 6×2 hero ──┬── 6×1 wide ──┐
│              ├──────────────┤
│              ├ 3×1 ┬ 3×1 ───┤
└──────────────┴─────┴────────┘
```
Or 2×2 quad of equal squares (then it's a uniform grid, not bento).

**5 items:**
```
┌── 6×2 hero ──┬── 6×1 wide ───────┐
│              ├───────────────────┤
│              ├ 3×1 ┬ 3×1 ────────┤
└──────────────┴─────┴─────────────┤
                 │── 12×1 full ────│   (closing)
```

**6 items (the os-traquinas Atividades case):**
```
┌── 6×2 hero ──┬── 6×1 wide ──────────┐
│              ├──────────────────────┤
│              ├ 3×1 ┬ 3×2 tall ──────┤
├──── 6×1 wide ┴─────┤                │
│                    │                │
└────────────────────┴────────────────┘
```
Total: 6+6+6+3+3+6 = 12+12+12 = 36 = 12 cols × 3 rows ✓

Or with closing full-wide:
```
6×2 hero + 6×1 wide + 6×1 wide + 3×1 + 3×2 tall + 12×1 full
```

**7+ items:** stop. 7+ in a single bento gets visually noisy. Either:
- Split into two bento sections
- Switch to uniform grid
- Drop weakest items

### Validation rules

Before shipping a bento, verify:

- **Sum of (cols × rows) per card == total grid area** (cols × max_row)
- **No gaps** (every cell of the grid is covered)
- **No more than one Hero (6×2) per bento** — multiple heroes = no hero
- **At least 2 different span sizes** — if all cards are 3×1, it's a uniform grid pretending to be bento

---

## Alignment Consistency Rules

These prevent the misalignment seen in the os-traquinas first version.

### Rule 1 — Section header alignment matches grid alignment

If `section-header { text-align: center }`, then the grid below must:
- Be **centred within the container** (not left-aligned), OR
- Span **full container width with content evenly distributed**

If the grid is uniform with `auto-fit minmax(...)` and the items don't fill the row, the result is left-aligned items under a centred header. Visual misalignment.

**Fix:** use **fixed columns** (`repeat(N, 1fr)`) with item count = N or 2N, OR centre the grid wrapper.

### Rule 2 — Container width consistency

Every section uses the same `max-width` container. If the hero is 1400px max-width, every section is 1400px max-width. Don't switch widths between sections — creates visual jitter on scroll.

### Rule 3 — Edge alignment across sections

When two adjacent sections have content that aligns to a vertical line (e.g., hero text starts at 80px from left, next section's first card also at 80px from left), they must use the **same horizontal padding**. Mixing `--sp-md` and `--sp-2xl` between sections breaks the rhythm.

### Rule 4 — Bento cells align to the master grid

Inside a bento, internal padding inside cards must come from the **same scale** the bento gutter uses. If bento gap is `var(--sp-lg)` (24px), card padding should be `var(--sp-lg)` or `var(--sp-xl)` — not random `var(--sp-pad-card)` if that's a different value.

---

## Decision Tree — what pattern for what content?

```
How many items?
│
├─ 1   → No pattern needed (single block)
├─ 2   → Hero + Supporting (asymmetric pair) OR side-by-side equal
├─ 3   → Bento (hero + two supporting) OR Uniform Grid 3-col
├─ 4   → Uniform Grid 4-col OR Bento (1 hero + 3 supporting)
├─ 5   → Bento (hero + wide + 3 squares) — uniform 5-col is fragile
├─ 6   → Bento (preferred for marketing)  OR  Uniform 3×2 (sequential)  OR  Uniform 2×3 (compact)
├─ 7   → Bento (split into 2 sections preferred)  OR  Uniform 7-col (rare)
├─ 8   → Uniform 4×2 OR Bento with closing full-wide
├─ 9   → Uniform 3×3 OR break into 3+6 bento
├─ 10  → Uniform 5×2 OR 2-col list
├─ 11+ → Stop. Split into two sections, or switch to list/timeline.
```

**Then ask: what's the content's emotional intent?**

| Intent | Pattern |
|--------|---------|
| Marketing energy / "look at this" | Bento |
| Browse / compare | Uniform Grid |
| Read prose top-to-bottom | List C1 (narrow column) |
| Sequence / schedule / line items | List C2 (full-width horizontal rows) |
| Highlight one thing | Hero + Supporting |

If style and intent disagree, intent wins. If sanctuary-tech style + marketing-energy intent → that's the wrong style for the brief. Escalate.

---

## Common Failure Modes

**Failure 1 — auto-fit grid with non-multiple item count.**
6 cards in `auto-fit minmax(280px, 1fr)` at 1200px viewport → 4 cols → 4+2 layout → 2 orphans on row 2. Visual mess. Fix: pick fixed columns, or switch to bento.

**Failure 2 — bento with all same size.**
Cards at `grid-column: span 4` for all 6 cards on a 12-col grid is just a 3-col uniform grid wearing a bento name. Fix: vary spans intentionally.

**Failure 3 — section header centred, grid left-aligned.**
Container is centred, grid is left-aligned inside container, items fill from left. The header floats above-centre while items pile bottom-left. Fix: align grid wrapper consistently with header (both centred or both left).

**Failure 4 — sequential content as bento.**
Schedule timeline as bento with mixed sizes implies hierarchy that isn't there. 8:00 isn't more important than 12:30. Fix: uniform grid or list for sequential content.

**Failure 5 — no closing or summary in long bento.**
Bento with 6+ cards and no full-wide closer feels like it ended mid-thought. Fix: add a 12×1 closing statement, or end with the natural-tallest card on the right.

**Failure 6 — horizontal-content list constrained to reading width.**
Schedule with `[time] [activity] [meta]` rows rendered at `max-width: 720px` while the page container is `1280px`. Result: list looks like an unfinished section with 40% empty space to its right, visually disconnected from the headers above and the sections below. Fix: list spans the same `max-width` as the rest of the page (Pattern C2). Reading width (~720px) only applies to prose paragraphs (Pattern C1).

**Failure 7 — list when grid was the right call.**
6+ short items with no sequential meaning rendered as a vertical list creates an unnecessarily tall section. If the items don't *need* to be read in order and have similar weight, use Uniform Grid. Use list only when sequence or reading is the point.

---

## Quick reference table

| Style library | Default pattern preference |
|---------------|---------------------------|
| `neo-brutalist` | Bento (asymmetric, grid-visible) |
| `editorial-portfolio` | Hero + Supporting (image-led asymmetric) |
| `jocril-technical` | Uniform Grid (technical clarity) |
| `basalt-ecommerce` | Uniform Grid (product-led, equal weight) |
| `memoir-blog` | List + Uniform Grid (reading-first) |
| `creative-studio` | Bento + Hero + Supporting (mixed) |
| `warm-serene-luxury` | Hero + Supporting (image-led) |
| `playful-bento` | **Bento — required, not optional** |
| `spritify` | Bento (preferred) or Uniform Grid (chunky) |
| `sanctuary-tech` | List or Single-column (low cognitive load) |

The "default" is the starting point. The brief and content can override — but the override must be deliberate and documented.
