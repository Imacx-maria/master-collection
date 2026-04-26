# Atmospheric Protocol Review Checks

Load during Phase 4 when the chosen style is Atmospheric Protocol.

**Run `gradient-tactics.md` § Audit questions in addition** — the gradient backdrop is the load-bearing visual element of this style, so every audit must cover both the chrome (this file) and the atmosphere (gradient-tactics).

## Style-Specific Questions

1. **Is the variant declared and consistent?** The build should commit to Bloom, Flow, or Particle in DESIGN.md and use that variant's accent + backdrop + card-shadow recipe throughout. Mixed variants (indigo CTAs on a violet smoky backdrop, or particle field with chromatic shadows) break the atmospheric coherence. If the brief is unclear, default to **Bloom** — it's the most versatile.

2. **Does every headline use the italic-continuation pattern?** Hero headline must be two lines, second line italicised in the same Instrument Serif family. If the build has roman-only headlines, the typographic identity is missing — push back. Single-keyword italics inside a single-line headline are an acceptable relaxation; full-roman headlines are not.

3. **Is the page background `#030508` (or the chosen variant's near-black), not `#000000`?** Pure black is wrong — it reads as void and kills the gradient atmosphere because there's nothing to absorb the bloom/flow/particle colour. The faint blue undertone of `#030508` is what lets the atmosphere read as ambient light.

4. **Are all borders 0.67px white at 5–12% opacity, not 1px solid grey?** The hairline border is the chrome signature. 1px borders read as harsh; solid greys (`#27272A`, `#3F3F46`) break the translucency of the glass surfaces. Test by zooming to 200% — the hairline should still feel hair-thin.

5. **Does every card wear the gradient border shell?** Cards without the shell read as flat dark blocks (generic dark Tailwind dashboard). Audit every card on the page; the shell must be present on standard cards AND glass cards. If the build uses a `border: 1px solid rgba(...)` instead, that's wrong — replace with the wrapping shell.

5a. **🛑 CARDINAL — Does every card have a `box-shadow` applied?** This is the highest-frequency Atmospheric Protocol regression: the build defines `--shadow-card-soft` / `--shadow-card-bloom` tokens but forgets to apply them to `.gradient-shell` / `.card` / `.shell-content`. Without a shadow, the bloom backdrop bleeds past the card edges and reads as a "ghost outline" — the eye reconstructs an apparent second card offset from the actual card. **Mechanical check (run before delivery):**

```bash
grep -E "(\.gradient-shell|\.card|\.shell-content)\s*\{[^}]*\}" <build-file> | grep -v box-shadow
```

If this returns any class definition without `box-shadow`, the build will ship the ghost-outline bug. Add `box-shadow: var(--shadow-card-soft)` to standard card classes and `box-shadow: var(--shadow-card-bloom)` (or `card-flow`) to hero/featured-card variants. **Every card needs one.**

5b. **Is `max-width` set on the inner `shell-content` while the wrapper `gradient-shell` extends wider?** When the inner is narrower than the outer, the shell's gradient background gets exposed on the sides (visible misalignment). Constrain the wrapper, not the inner. Audit by inspecting any card where you applied `max-width`, `width`, or centering rules — confirm those rules sit on the `.gradient-shell`, not on `.shell-content` or its variants.

6. **Is monospace strictly limited to data?** Metric values, system labels, percentages, code references = mono. Body copy, headlines, button labels, nav links = NOT mono. The most common drift is using mono for buttons or labels because "it looks technical." Push back — mono creep dilutes the data signal.

7. **Is the overline pattern `● UPPERCASE LABEL` with the leading status dot?** Plain uppercase labels without the dot lose the protocol/infrastructure mood. The dot character (●, U+25CF) must match the text colour and sit at the same baseline.

8. **Is the nav a fixed centred glass pill, not a full-width bar?** Full-width navs are wrong for this style — they break the atmosphere by introducing a horizontal slab. The pill should float, blur the backdrop, and respond to content width.

9. **Is the atmosphere doing real work or just "a gradient"?** The backdrop should be one of three named variants with the matching recipe from `gradient-tactics.md`. A freelance interpretation (linear gradient with two stops, generic noise overlay, decorative SVG blob) is wrong even if it looks superficially similar. The recipe matters because animation cost, accessibility behaviour, and fallback strategy differ per recipe.

10. **For Particle variant: is there a CSS fallback on the canvas's parent?** WebGL failure (context loss, blocked, mobile GPU exhaustion) must leave a designed dark backdrop, not a flat `#030508` void. Test by disabling WebGL in DevTools.

11. **Is the page contrast preserved over the brightest gradient zone?** Bloom centres and flow midpoints reduce effective contrast on overlaid text. Test text contrast at the brightest atmospheric point, not the page average. Standard fix: drop the bloom opacity by 0.05 or push body text to pure white.

12. **Are accent-tinted shadows reserved for hero/featured cards only?** Every card on the page wearing a coloured shadow creates visual noise. Default to neutral `card-soft`; reserve `card-bloom` / `card-flow` for the 1–2 hero cards that anchor the page.

## Common Regressions

- Pure black `#000000` page background instead of the variant near-black — kills the atmosphere
- Solid grey borders (`border: 1px solid #27272A`) replacing the hairline pattern — chrome reads as harsh
- Cards missing the gradient border shell — flat blocks, generic dashboard look
- **Cards missing `box-shadow` — the highest-frequency regression.** Tokens are defined (`--shadow-card-soft`, `--shadow-card-bloom`) but never applied to the actual card classes. Result: bloom backdrop bleeds past card edges, the eye reads an apparent ghost outline, the page looks broken. Always grep for `box-shadow` before delivery and confirm every card class has one.
- **`max-width` on `.shell-content` (or `.testimonial-inner` / `.cta-inner` etc.) when the parent `.gradient-shell` is wider** — exposes the gradient-shell background on the sides, producing a visible misalignment that looks like a second card behind the first. Constrain the wrapper, not the inner.
- Mixing accent colours across a single page (indigo button on violet flow backdrop, etc.)
- Bold (700+) Instrument Serif headlines because "the design needed more impact" — weight 400 is the only weight
- Italic continuation dropped because "the second line looked weird" — that's the signature; restore it
- Mono leaking into body or button labels — dilutes the data signal
- Status dot (●) replaced by an SVG icon or removed entirely — both wrong; use the Unicode character
- Particle variant shipped without WebGL fallback — page goes blank if WebGL fails
- Animated atmosphere with no `prefers-reduced-motion` gate — fails accessibility audit
- Full-width navigation bar replacing the centred glass pill — breaks the atmosphere
- Coloured shadows on every card creating visual noise — limit to hero cards
- Bloom mesh with 5+ radial layers muddying into grey — drop to 3 maximum (see `gradient-tactics.md` § R1)
- Flow gradient size at default 100% so endpoints become visible during animation — must be `background-size: 400%` minimum
- Light-mode adaptation attempted — this style is dark-only by design; light-mode briefs should redirect to Warm Editorial or Technical Refined
