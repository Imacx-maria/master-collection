# Technical Refined Review Checks

Load during Phase 4 when the chosen style is Technical Refined.

## Style-Specific Questions

1. **Is the teal accent focused or flooding?** Count teal usages — should be CTAs, active states, focus outlines only. If more than ~5% of the visible interface is teal, it's flooding.
2. **Is mono type used for metadata and labels specifically?** Geist Mono on labels, badges, code, timestamps, system language — not on body copy or headlines. Mis-assigning mono reads as amateur.
3. **Are heading jumps aggressive enough?** Heroes at 70–160px, not 48px. Timid scaling ("h1 is 1.5x h2") breaks the engineered feel.
4. **Do dashed borders appear as support motif, not dominant structure?** A few dashed dividers or card outlines are correct; dashed-everything makes the interface feel unfinished.
5. **Are focus outlines on-brand?** Teal accent outlines (not browser default blue). Remove → restyle, never just remove.
6. **Is depth created through tonal layers, not shadows?** Dark surface #141414 on #0A0A0A primary — subtle panel separation. Fluffy drop shadows are wrong.
7. **Does the interface still read cleanly if you mentally strip the teal?** If the answer is no, the teal is doing hierarchy work that type and spacing should be doing.
8. **Are pill buttons reserved for compact actions?** Full-radius (`9999px`) for buttons and badges only. Cards stay at 14px medium radius.

## Common Regressions

- Teal accent on backgrounds, not just foreground elements
- Mono type bleeding into body copy or large headlines
- Generic purple gradients or glassmorphism sneaking in (instant refactor)
- Too many border styles — pick dashed or solid, don't mix freely
- Hero typography too small — This style lives and dies by the scale jumps
