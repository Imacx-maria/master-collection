# Neo-Brutalist Review Checks

Load during Phase 4 when the chosen style is Neo-Brutalist.

## Style-Specific Questions

1. **Are corners actually 0?** Check every button, card, input, modal. Any radius > 2px is a regression.
2. **Is the grid visible when it strengthens composition?** Hero, section dividers, and card alignments should reveal the grid — not hide it.
3. **Do hover states use physical displacement?** Translate + hard shadow (e.g. `translate(-4px, -4px)` + `8px 8px 0 var(--color-primary)`), not soft fades or color swaps.
4. **Is there at most one accent color?** Neo-Brutalist breaks if accents multiply. Count them.
5. **Is the type mono + compressed sans paired correctly?** Display in Anton (or equivalent compressed), body and labels in Roboto Mono with wide tracking (0.08em+).
6. **Is there anything "soft" in the interface?** Gradients, blur, elegant animations, gentle curves — all break the style. Refactor or remove.
7. **Does the dark mode flip primary/neutral cleanly?** #181818 ↔ #DDDDDD swap, not a tinted midtone.
8. **Are uppercase labels tracked wide enough?** 0.18em–0.2em for small labels. Defaults feel wrong.

## Common Regressions

- Rounded buttons creeping in from default component libraries — always audit third-party imports
- "Smooth" cubic-bezier easing instead of linear or step
- Drop shadows instead of offset hard shadows
- Body text in sans-serif instead of mono (the mono body is a signature move)
