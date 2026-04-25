# Warm Serene Luxury Review Checks

Load during Phase 4 when the chosen style is Warm Serene Luxury.

## Style-Specific Questions

1. **Are there any accent colors?** If yes, remove. The palette is strictly #FAFAFA + #1A1A1A + rgba variants. Accent colors break the photography-carries-color principle.
2. **Does imagery carry the color story?** If the images are cropped out, the page should feel colorless. If it still looks colorful, a color has snuck in somewhere.
3. **Are numbered items (01, 02, 03) used with wide-tracked labels?** Signature pattern for sections and steps. Wide tracking (0.14em) and small size (11px).
4. **Is DM Serif Display used for all headlines?** Sans-serif headlines break the elegance completely. Onest is body-only.
5. **Is section padding at 96px+?** Luxury needs space. Compressed sections destroy the brief instantly.
6. **Is secondary text using rgba variants of primary, not separate gray tones?** `rgba(26,26,26,0.75)` — not `#444745` or some other sibling gray. The rgba approach keeps the tonal family unified.
7. **Are corners subtle (0–8px)?** Aggressive rounding breaks the elegance. Sharp or nearly-sharp.
8. **Does the interface feel photograph-first, UI-second?** If chrome, cards, or navigation dominate the viewport vs imagery, refactor. The hotel/spa/interior brief requires imagery primacy.

## Common Regressions

- Adding a subtle accent color "for interest" — immediately breaks the brief
- Sans-serif headlines (Inter, Onest) instead of DM Serif Display
- Using mid-gray (#888888) instead of rgba variants for secondary text
- Compressed section padding to "fit more" — luxury is spacious or it isn't luxury
- Rounded cards or pill buttons from SaaS component libraries
