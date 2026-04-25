# Warm Editorial Review Checks

Load during Phase 4 when the chosen style is Warm Editorial.

## Style-Specific Questions

1. **Is the page background Parchment (#F5F4ED), not pure white?** Pure white breaks the entire chromatic spell. Ivory (#FAF9F5) is acceptable for cards and elevated surfaces, but the page foundation must be the warm parchment cream. This is the single most-violated rule of the style.

2. **Are all neutrals warm-toned?** Every grey must have a yellow-brown undertone (`#5E5D59`, `#87867F`, `#4D4C48`, `#3D3D3A`). If any grey reads cool/blue (e.g., Tailwind's slate-* or zinc-* defaults), refactor — it breaks the warmth instantly. Test: does the grey look right next to the Parchment background, or does it create a visual chill?

3. **Are serif headlines at weight 500 only?** No 600, 700, or italic. The single-weight discipline is the literary-voice signature. Bold serif breaks the "one author wrote every heading" cadence. If a heading needs more weight, use larger size or darker colour, never heavier serif.

4. **Is Terracotta (#C96442) reserved for primary CTAs and brand moments?** Multiple Terracotta blocks scattered across the page dilute the brand moment. The colour should function like a single highlight in an essay — used sparingly, with intent.

5. **Are interactive states using ring shadows, not drop shadows?** Buttons, cards, and hover states should use `0 0 0 1px <warm-grey>` patterns, not `box-shadow: 0 4px 6px rgba(0,0,0,0.1)`. Drop shadows feel SaaS-generic; ring shadows are the warm-editorial fingerprint.

6. **Is body text at line-height 1.60?** Tight body line-height (1.4–1.5) kills the literary cadence. The whole point of this style is essay-reading rhythm. Check every paragraph rule, not just the typography token.

7. **Does the page have light/dark section alternation, OR a deliberate reason to skip it?** Chapter rhythm is the structural signature. If the page is all Parchment with no Near Black sections, the rhythm is missing — but it's not always wrong (e.g., reading-column documentation pages). If skipped, the brief should justify it.

8. **Is the serif/sans split intact?** Headlines are serif; body, UI, and labels are sans; code is mono. Mixing sans into headlines breaks the typographic identity. Italicised serif body is acceptable for accent words; sans-serif headlines are not.

9. **Are corners comfortably rounded (8–12px standard, 16–32px for featured/hero)?** Sharp corners (<6px on cards/buttons) break the soft warmth. The radius discipline is part of the "approachable, thoughtful" mood.

## Common Regressions

- Using pure white (`#FFFFFF`) as the page background — Parchment or Ivory always
- Cool blue-grey neutrals leaking in from a default Tailwind/CSS framework palette
- Serif headlines drifting to weight 600 or 700 because "the design needed more impact"
- Terracotta used for multiple non-CTA elements (icons, dividers, badges) — dilutes the brand moment
- Generic Material/Bootstrap drop shadows replacing the ring-shadow pattern
- Body line-height at 1.4 because "1.6 looks too spaced" — the spacing IS the point
- Sans-serif headlines because the serif loaded too late or fell back to Times New Roman without a check
- Sharp corners on cards/buttons (`border-radius: 4px`) — too crisp for the literary mood
- Geometric/tech illustrations replacing the organic-illustration personality
- Cool focus colours other than the prescribed `#3898EC` accessibility blue
