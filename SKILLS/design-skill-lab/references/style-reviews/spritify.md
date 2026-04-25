# Spritify Review Checks

Load during Phase 4 when the chosen style is Spritify.

## Style-Specific Questions

1. **Is League Spartan used at heavy weights (700–800) for display?** Thin weights defeat the playful assertive feel. Check that headline weights aren't defaulting to 400.
2. **Is one of the three schemes clearly chosen and applied consistently within a view?** Mixing schemes inside a single page breaks the structure. Scheme switches happen between pages or sections, not within.
3. **Are components chunky and tactile?** Generous padding (16px+ on buttons), thick left-border accents on cards (6px). Thin, flat components feel wrong here.
4. **Are corners very rounded (16px minimum)?** Sharp corners are a total style break. 24px default, 40px for feature cards, full-pill for buttons.
5. **Do buttons use both dark-on-light AND accent (pink) variants?** The primary dark button + accent pink button is a pairing. Single-button-style pages feel undersigned.
6. **Is the typography chunky — heroes at 96–112px?** Small headlines break the playful energy. Scale aggressively.
7. **Is saturation embraced rather than feared?** The palette is saturated on purpose — #82EDA6 green, #F6BBFD pink, #FFFF94 yellow. Muting these defeats the style.
8. **Does the off-white (#F9F8F4) appear as the breathing space?** The neutral bridges the saturated blocks. Pure white instead breaks warmth.

## Layout Pattern Checks (NEW)

Spritify can use either bento OR uniform grid (see `references/layout-patterns.md`). The choice should be deliberate.

9. **Was the layout pattern chosen deliberately?** For sections with 4+ items, did the agent pick uniform grid (browse / equal weight) OR bento (marketing energy / hero + supporting)? Defaulting to `auto-fit minmax(...)` without thinking is a regression.
10. **No orphans in uniform grids.** If the section uses uniform grid, item count must be divisible by the column count at every breakpoint. 6 items in a 4-col grid = 4+2 orphans = visual bug. Switch to 3-col, 2-col, or refactor to bento.
11. **Bento sections use mixed spans.** If bento was chosen, at least 2 distinct span sizes must be used. All-`span 4` cards are a uniform grid in disguise.
12. **Section header alignment matches grid alignment.** Centred headers above left-aligned grids look broken (the os-traquinas v1 failure). Either centre the grid wrapper, or left-align the header.
13. **Sequential content uses uniform/list, not bento.** Schedules, timelines, ordered process steps — bento implies hierarchy that contradicts the sequence. Use uniform grid or vertical list.

## Common Regressions

- Using League Spartan 400 instead of 700+ (readable but not playful)
- Muting the palette because it "looks too much" — wrong instinct
- Sharp corners creeping in from default component libraries
- Mixing schemes within a single section (visual chaos)
- Small, thin buttons instead of chunky playful ones
- **`auto-fit minmax(280px, 1fr)` with 5/6/7 items** — produces orphan rows on most viewports. Use fixed columns or bento.
- **Centred section header above left-aligned grid** — visual misalignment. Force grid wrapper to centre, OR switch to fixed column count divisible by item count.
- **Calling something "bento" when all cards are the same size** — that's just a grid. Use real bento spans (see `layout-patterns.md`).
