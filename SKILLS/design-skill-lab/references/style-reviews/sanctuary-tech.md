# Sanctuary Tech Review Checks

Load during Phase 4 when the chosen style is Sanctuary Tech.

**Critical note:** this style is used for crisis, healthcare, and trauma-informed contexts. Review failures here have real human consequences — users may be in acute distress. Err toward caution.

## Style-Specific Questions

1. **Is the only accent color green (#16A34A)?** If red, orange, or blue has appeared anywhere as primary accent, refactor immediately. Wrong emotional signals for crisis contexts.
2. **Is monospace type used throughout?** Body, headings, labels, everything. Sans-serif or serif breaks the honesty signal. DM Mono or JetBrains Mono only.
3. **Do dashed borders frame important panels?** The structural motif. 1px dashed border (#D4D4D4 light / #404040 dark) for content panels, resource lists, alert boxes.
4. **Is section padding generous (80px+)?** Whitespace is a safety feature — reduces cognitive load. Compressed sections raise stress.
5. **Is body text at 15px/1.7 for comfortable reading?** Users under stress read slower. Tight line-height or small body text actively hurts.
6. **Are animations absent or extremely subtle?** Opacity fades and color transitions only. No slide-ins, no bounces, no parallax. Motion signals urgency — wrong signal here.
7. **Does each screen have one clear primary action?** Multiple competing CTAs overwhelm distressed users. Secondary actions should be visually quieter.
8. **Are contrast ratios well above WCAG AA?** Aim for AAA (7:1 body) where possible. Distressed users may be reading in poor conditions or through tears.

## Trauma-Informed Checks

9. **Does language avoid triggering phrases?** No "emergency" red text, no countdown timers, no "urgent action required" banners. Calm, factual language.
10. **Is there a clear exit or escape?** A visible "leave site quickly" option or clear navigation out. Users may be in unsafe physical environments.
11. **Is content progressive, not overwhelming?** Show one thing at a time. Expandable sections for more detail, not walls of text.

## Common Regressions

- Using red accent for CTAs because "it's urgent" — exactly the wrong instinct
- Switching to sans-serif because "mono looks too technical" — mono is the honesty signal
- Shadow-based cards instead of dashed borders
- Compressing sections to "show more" — violates the whitespace-as-safety principle
- Adding animations for "polish" — raises anxiety in distressed users
- Multiple primary CTAs competing for attention
