# Playful Bento Review Checks

Load during Phase 4 when the chosen style is Playful Bento.

## Style-Specific Questions

1. **Does the bento grid have clear hierarchy?** One hero cell (2x2 or 2x1), several medium cells, small cells for metadata. Uniform grids are not bento — they're just grids.
2. **Are cell backgrounds tinted, not saturated?** Muted tints (cream, light blue, mint, pink) coexist well. Saturated brights fight each other. If adjacent cells clash, tone them down.
3. **Is there one accent cell per grid, not every cell?** Amber or violet on one statement cell. If every cell is a different bright, the grid loses focus.
4. **Are cell radii generous (20–32px)?** Sharp corners break bento instantly. The soft grid is the whole aesthetic.
5. **Is Inter weight 800 used for display drama?** 700 feels corporate, 800+ feels assertive. Bento needs the latter.
6. **Do cells use different sizes for visual rhythm?** 2x2 + 2x1 + 1x1 + 1x1 is a good pattern. Check spans — `grid-column: span 2 / span 2` on the hero cell.
7. **Are buttons full-pill rounded?** `border-radius: 9999px`. Square buttons in a bento grid feel out of place.
8. **Is there enough gutter between cells?** 16px is the starting point. Cells touching directly compress the energy.

## Bento Structural Checks (NEW — non-negotiable)

These were added after a real-world failure where the agent shipped a uniform 4-col grid disguised as "bento". See `references/layout-patterns.md` for the full grammar.

9. **Real bento or uniform grid in disguise?** Pick a card at random. Does it have a different `grid-column: span` value than its neighbours? If all cards span the same number of columns, it's a uniform grid pretending to be bento. Refactor with mixed spans.
10. **Span coverage adds up.** Calculate `Σ (cols × rows)` across all cards. It must equal `12 × max_row_used`. Anything else means there are visual gaps in the layout.
11. **At most one Hero (6×2) per bento section.** Multiple hero cells = no hero. Demote one or split into two bento sections.
12. **At least 2 distinct span sizes used.** A bento with 4 cards all at `span 6` is a 2-col uniform grid. Use the span vocabulary in `layout-patterns.md`.
13. **Pattern matches item count.** Reference the count→pattern table in `layout-patterns.md`. 6 cards has a documented pattern (hero + wide + wide + small + tall + closing). Don't invent a 7th pattern.
14. **No orphan rows in mobile fallback.** When bento collapses to single column on mobile, every card stacks full-width — that's fine. But if you fall back to a 2-col uniform grid on tablet and have an odd item count, you get orphans. Either stack full-width, or pick item count divisible by 2.

## Common Regressions

- Uniform grid (all cells same size) — it's just a grid, not bento
- More than 4 tints used, making the page feel cluttered
- Sharp corners on cells from default grid libraries
- Saturated cells adjacent to each other creating visual noise
- Content overflowing cells because the hierarchy wasn't planned — cells should be sized to their content weight
- **Auto-fit minmax() with non-multiple item count** — produces orphan rows. Use fixed columns or bento spans.
- **Hero card with footnote-importance content** — the largest cell must hold the most important content. If the hero is "Mini-Cozinha" but the actual page anchor is "Expressão Plástica", swap them.
