# Memoir Blog Review Checks

Load during Phase 4 when the chosen style is Memoir Blog.

## Style-Specific Questions

1. **Is Source Serif 4 italic used for accent words/phrases inside Manrope body?** The italic-serif-inside-sans is the signature move. Without it, the style degrades to "generic blog".
2. **Is the background creamy (#F4F2F0), not pure white?** Pure white breaks the warmth. Article cards can be white, but the page foundation stays warm.
3. **Do blog cards feel tidy and consistent?** 24px padding, 8px radius, subtle shadow or no shadow. Inconsistent card treatments break the archive rhythm.
4. **Is body line-height at 1.65 for reading comfort?** Tight line-height (1.3–1.4) is for display, not long-form body. Check every article-body rule.
5. **Do filter pills distinguish active from inactive clearly?** Active = white fill + dark text; Inactive = cream fill (#EDEAE7) + muted text. No border-only states.
6. **Are sidebar inactive items at ~0.48 opacity?** Muted but readable — signals "clickable but not current". Fully opaque sidebar breaks hierarchy.
7. **Do listing view and post view feel like one system?** Same type scale, same colors, same spacing rhythm. If a reader can't tell they're on the same site, refactor.
8. **Is body text at 16px minimum with comfortable measure (45–75ch)?** Reading-first is the whole brief — nothing matters if reading is uncomfortable.

## Common Regressions

- Dropping the Source Serif italic accent — it seems "extra" but it's the signature
- Pure white background instead of creamy neutral
- Card designs pulled from SaaS dashboards (wrong proportions for reading)
- Body text below 16px to "fit more above the fold" — defeats the brief
- Saturated accent colors creeping in — memoir is calm, not vibrant
