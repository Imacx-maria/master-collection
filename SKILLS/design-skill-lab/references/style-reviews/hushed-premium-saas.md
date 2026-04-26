# Hushed Premium SaaS Review Checks

Load during Phase 4 when the chosen style is Hushed Premium SaaS.

## Style-Specific Questions

1. **Is the display weight 200–300?** If any display headline is at weight 400+, refactor. The whisper-thin lightness IS the brand. Bold display breaks the entire identity in one stroke. The single permitted exception is the uppercase bold CTA pattern (Manrope/Waldenburg 700, ≤14px, with 0.7px tracking) — and only if it appears at most once on the page.
2. **Are shadows at sub-0.1 opacity, multi-layer?** Any single shadow at >0.1 opacity is wrong. Cards on the page should use the 3-layer outline-ring stack (`rgba(0,0,0,0.06) 0 0 0 1px, rgba(0,0,0,0.04) 0 1px 2px, rgba(0,0,0,0.04) 0 2px 4px`) on hero/feature cards, and the single outline-ring on bulk grids. If you see `rgba(0,0,0,0.15)` or heavier, the ethereal quality is broken.
3. **Is there a warm-stone surface (`#F5F2EF`) on at least one panel?** Manifesto, testimonial, hero secondary CTA — at least one of these must use the warm-stone surface. Without it, the page reads as cold tech minimalism, not premium consumer SaaS.
4. **Is the warm-stone CTA present and asymmetric?** The signature CTA uses `rgba(245,242,239,0.8)` background, **30px** radius (NOT full pill), **asymmetric padding** (`12px 20px 12px 14px`), and warm-tinted shadow (`rgba(78,50,23,0.04) 0 6px 16px`). If the page has no warm-stone CTA, the brand register is missing. If it's present but symmetric or full-pill, refactor to the asymmetric 30px form.
5. **Is body text using positive letter-spacing (+0.14 to +0.18px)?** Inter at body sizes must use positive tracking. This is the airy reading texture that contrasts with the tight display. If body uses `letter-spacing: 0` or negative, the rhythm fails — the page reads as generic SaaS.
6. **Does the palette stay achromatic with warm undertones only?** No brand color, no accent hue. Warmth lives in surfaces and shadows, never in hues. A single sector-neutral tint (e.g., `#5C6E54` moss for B2B trust) is permitted ONLY if declared as a divergence in provenance and used surgically (eyebrow dot, micro-mark, hover) — never as a fill.
7. **Are primary buttons full pill (9999px)?** Pill on primary is non-negotiable. Sharp-cornered or rounded-rect primary buttons break the register. The 30px radius is reserved for the warm-stone CTA — don't apply 30px to the black primary.
8. **Is section padding generous (clamp(64px, 9vw, 120px) minimum)?** Apple-like generosity is the rhythm. Compressed sections compromise the premium feel. Hero gets even more (`clamp(80px, 13vw, 160px)` top). If section padding is below 64px on any major section, it reads as a regular SaaS landing, not premium.
9. **Are card radii ≥16px (cards) and ≥20px (prominent cards)?** Sharp corners (<8px) on cards break the ethereal quality. The generous radius is structural. If you see `border-radius: 4px` or `8px` on a content card, refactor to 16–24px.
10. **Does it pass the "whisper test"?** Mute the page and squint. Does the hero feel like it's whispering authority, or shouting? If it shouts (heavy weight, saturated colors, hard shadows, dense layout), the register is wrong — the ENTIRE point of this style is that lightness is the impact.

## Common Regressions

- Display weight crept up to 400+ "for readability" — instant identity loss. Hold the line at 200–300.
- Shadow stack collapsed to a single heavy shadow "to make cards pop" — refactor back to 3 layers at sub-0.1.
- Brand color introduced "for visual interest" — kills the entire achromatic discipline. The warmth is the only "color" decision.
- Warm-stone CTA replaced with a generic ghost button — loses the signature. The asymmetric 30px warm-stone is the brand mark.
- Body text using `letter-spacing: 0` or negative — destroys the airy reading texture. Inter at body sizes is +0.14 to +0.18px, always.
- Section padding compressed to fit more content above the fold — destroys the rhythm. Content density is wrong here; the whitespace IS the volume.
- Cool gray borders introduced — the warmth must pervade. Use warm-tinted borders (`rgba(0,0,0,0.05)` reads warm enough; `#E5E5E5` is acceptable; `#9CA3AF` cool gray is forbidden).
- Sharp-cornered cards (<8px radius) — breaks the generous-radius vocabulary. Refactor to 16+.
- Hero in 3+ lines at weight 200 — light weight + long lines reads as anemic. Tighten copy to 1–2 lines, OR push weight to 300 and accept the slight density shift.

## When the design-reviewer flags low contrast

Manrope/Waldenburg 200 at smaller display sizes (<32px) often fails WCAG AAA contrast. This is a real failure, not a stylistic license. The fix is **always** to switch the smaller size to Inter weight 400+ — never to bump Manrope/Waldenburg to weight 500+. If a hero subtitle is under 24px, it must be Inter, not Manrope.

If the audit flags the hero headline (>48px) at weight 200 as low contrast, that's typically a backdrop-contrast issue, not a typography issue. Verify against the actual surface — if the hero sits on white (`#FFFFFF`) and uses `--text-primary: #000`, contrast is 21:1 even at weight 200. If it's failing, something else is wrong (probably a backdrop or overlay).
