# Editorial Portfolio Review Checks

Load during Phase 4 when the chosen style is Editorial Portfolio.

## Style-Specific Questions

1. **Does imagery carry the composition?** If removing every image leaves the page still feeling "finished", the images aren't doing their job. They should feel load-bearing, not decorative.
2. **Is the display type compressed and tight?** Letter-spacing at -0.03em to -0.06em for headlines, weight at 400 (light), sizes at 56px+. Default Inter letter-spacing is wrong.
3. **Is the palette restrained?** Off-white (#F4F3F0), near-black (#1D1F1E), one warm cream (#DBD5C9). No accent colors, no gradients.
4. **Are hover-reveal panels or similar editorial transitions used?** The signature is motion that reveals — captions sliding over images, panels exposing credits. Static hovers feel undersigned.
5. **Is asymmetry deliberate or just messy?** Asymmetric hero moments should follow an internal logic (image-left + text-right-offset, full-bleed + caption-band). Random offsets feel amateur.
6. **Does the footer band (#161616) anchor the page?** Dark footer is the editorial closer — provides weight against the warm neutral above.
7. **Are corners sharp?** Zero radius on everything except maybe tiny badges. Rounded cards break the gallery feel.
8. **Is line length controlled for body copy?** 45–65ch max. Full-width body text breaks the editorial rhythm.

## Common Regressions

- Default Inter letter-spacing instead of tightened display settings
- Introducing accent colors to "liven things up" — defeats the point
- Using rounded cards imported from component libraries
- Centering everything — editorial wants asymmetry
- Body font weight at 400 instead of 300 (the lightness is a feature)
