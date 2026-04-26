# Handoff — Loader Patterns + Axis 9 Page-Load

**Date:** 2026-04-26
**Session goal:** Add page-load as a first-class concern to the design-skill-lab. Stop the skill from silently inventing loaders.

---

## What changed

Four files in `SKILLS/design-skill-lab/`:

| File | Change |
|---|---|
| `references/style-tuning.md` | Added Axis 9 `page-load` (4 options + `you decide`). Tone renumbered to Axis 10. Per-library defaults table grew 8→9 columns. Library threshold updated ≥5/8 → ≥6/9. YAML manifesto schema includes `page-load` (with `value`, `source`, internal `pattern` field) and new `tuning-conflicts` block. Tier-coupling rule documented. Anti-patterns updated. |
| `references/loader-patterns.md` | **NEW.** ~840-line technical contract. The 4 primitives, decision matrix, 4 mandatory failure-mode patterns, 9 full recipes (body fade-in, hero shimmer, skeleton+shimmer, spinner, progress bar, curtain wipe, DrawSVG logo, SplitText wordmark, mask reveal), per-library default recipes, Webflow injection notes, pre-build checklist, Phase 4 audit questions. |
| `references/motion-tactics.md` | Cross-reference to `loader-patterns.md` at top. High-tier checklist updated: branded-intro loaders count toward "3 distinct motion moments" budget; loaders skip under reduced motion. |
| `SKILL.md` | Added Phase 3 Step 3.0.06 (load `loader-patterns.md` if `page-load !== 'none'`). Added row to Quick Reference table. Added file map entry. Tier-coupling rule + Sanctuary Tech sole auto-demote documented. |

Net new files: 1. Net edits: 3.

---

## Why

Before this session, the skill was inventing page loaders silently when `motion: high` was chosen — usually a generic spinner with zero failure-mode coverage. The two highest-severity loader bugs are:

1. **Loader never resolves** — `window.load` event never fires (CDN blocked, fetch unhandled), user trapped staring at a spinner.
2. **Page hidden behind loader breaks LCP** — the LCP element is gated by the loader (`display: none` on main) instead of overlaid (`position: fixed` with content painting normally underneath).

Neither was covered anywhere in the skill. Loaders were treated as a sub-case of `motion-tactics.md`, but they're a different animation class entirely — they fire before/during initial paint, not on scroll/hover, and they have unique failure modes (timeout safety, LCP regression, JS-disabled trap).

---

## Key design decisions (from this session — locked in by Maria)

| Decision | Resolution | Lives in |
|---|---|---|
| Question phrasing | Role-based: `none / subtle / functional / branded-intro` | style-tuning.md template + prose |
| Tier coupling on `motion: low` + non-subtle loader | **Soft warn-and-build**, never auto-demote | style-tuning.md § Tier-coupling rule + loader-patterns.md § Tier compatibility |
| Pattern picker (curtain vs DrawSVG vs skeleton vs ...) | Internal — skill maps role × library × imagery × corners → pattern. User never sees pattern selector. | loader-patterns.md § Decision matrix |
| Question position | Append at Axis 9; tone bumps to Axis 10 (still conditional on trauma-informed) | style-tuning.md interview template |
| Reference depth | Full — ~840 lines, all 9 recipes with HTML/CSS/JS, per-library defaults, Webflow specifics | loader-patterns.md |
| Sole auto-demote | trauma-informed mode + Sanctuary Tech library → page-load forced to `none` or `subtle`, regardless of user pick | loader-patterns.md § Per-library default recipes (Sanctuary Tech row) |

**Form convention (important for parser work):**
- **YAML value form**: hyphenated → `branded-intro`
- **Interview option label**: space form → `branded intro`
- Parser must accept both. Per-library defaults table uses YAML form.

---

## How to validate the changes

The skill has no automated tests for the interview flow. Manual verification:

1. **Run an interview build** with a brief that auto-detects to a library with a non-`none` default loader (e.g., "agency landing page" → Creative Studio → branded-intro).
2. **Verify the prompt sent to user** contains 9 questions (not 8), with Axis 9 being PAGE LOAD with the 4 options + you decide.
3. **Verify YAML frontmatter** of the resulting DESIGN.md includes:
   - `style-tuning.axes.page-load.value` set
   - `style-tuning.axes.page-load.source` set
   - `style-tuning.axes.page-load.pattern` recorded (the internal pick)
   - `provenance.library-derivation.method` says `9-axis match scoring`
4. **Verify the build output** for the loader pattern includes all four mandatory guards:
   - `.js-ready` gate in CSS (`.js-ready .loader { display: flex }`)
   - `setTimeout(resolveLoader, MAX_MS)` in the IIFE
   - `prefers-reduced-motion` check at the top of the IIFE (returns early)
   - `@media (prefers-reduced-motion: reduce)` CSS belt-and-braces
5. **Tier-coupling test**: brief that maps to `motion: low` with explicit `branded-intro` request → verify build proceeds, warning surfaces in delivery summary, `provenance.tuning-conflicts` populated.
6. **Trauma-informed test**: brief that fires Phase 1.0.5 trauma-informed mode + Sanctuary Tech library + user picks `branded-intro` → verify auto-demote to `subtle` (or `none`), logged in provenance.

If any verification fails, the gap is in the cross-reference chain. Most likely failure points:
- Phase 2.1 interview template not updated to 9 questions → grep style-tuning.md for the literal string `9 questions`
- Phase 3 Step 3.0.06 not loading loader-patterns.md → check SKILL.md line 113-117
- Pattern picker not running → check loader-patterns.md § Decision matrix is being read

---

## Memory updates (Maria's auto-memory)

Three memory files updated:

- **NEW**: `design_skill_lab_loader_patterns.md` — full contract summary, hyphen-vs-space form note, four failure-mode patterns, soft-warn rule, sole auto-demote.
- **REWRITTEN**: `design_skill_lab_style_tuning.md` — was 4 rounds stale (still talked about 11 axes, Phase 2.2.5, separate corner axes). Now reflects 9 axes at Phase 2.1, ≥6/9 threshold.
- **UPDATED**: `design_skill_lab_blocking_interview.md` — Round 9 entry added, "8 plain-language questions" → "9 (10 if trauma-informed)".
- **UPDATED**: `MEMORY.md` index — three rows fixed/added.

---

## Git status — handoff to user

Per `~/.claude/CLAUDE.md`: "No autonomous git operations. Enforced via `.claude/settings.json` deny list." Maria runs git commands manually.

**Suggested commit:**

```bash
cd C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION

git add SKILLS/design-skill-lab/SKILL.md \
        SKILLS/design-skill-lab/references/style-tuning.md \
        SKILLS/design-skill-lab/references/motion-tactics.md \
        SKILLS/design-skill-lab/references/loader-patterns.md \
        SKILLS/design-skill-lab/HANDOFF_2026-04-26_loader-patterns.md

git commit -m "design-skill-lab: add page-load axis (9) + loader-patterns reference

- Add Axis 9 'page-load' (none/subtle/functional/branded-intro) to style-tuning
  interview. Tone renumbered to Axis 10. Library mapping threshold updated
  from 5/8 to 6/9.
- New references/loader-patterns.md: 4 primitives, decision matrix, 9 recipes
  (body fade-in, hero shimmer, skeleton+shimmer, spinner, progress bar,
  curtain wipe, DrawSVG logo, SplitText wordmark, mask reveal), 4 mandatory
  failure-mode patterns (max-timeout, LCP-safe overlay, .js-ready gate,
  prefers-reduced-motion skip), per-library defaults, Webflow notes.
- Phase 3 Step 3.0.06 added to SKILL.md: load loader-patterns.md if
  page-load != 'none'.
- motion-tactics.md cross-references loader-patterns.md; branded-intro
  loaders count toward GSAP-justification budget at high tier.
- Tier-coupling rule (motion: low + non-subtle loader = soft warn-and-build,
  never auto-demote). Sole auto-demote: trauma-informed + Sanctuary Tech
  forces page-load to none/subtle.

Closes the silent-loader-invention gap that had no failure-mode coverage."
```

**Files-changed summary** (no git operations run by Claude):

```
SKILLS/design-skill-lab/SKILL.md                                    | edited (+18 lines)
SKILLS/design-skill-lab/references/style-tuning.md                  | edited (+~80 lines)
SKILLS/design-skill-lab/references/motion-tactics.md                | edited (+3 lines)
SKILLS/design-skill-lab/references/loader-patterns.md               | new (~840 lines)
SKILLS/design-skill-lab/HANDOFF_2026-04-26_loader-patterns.md       | new (this file)
```

---

## Open questions / future work

1. **Should the auto-demote rule extend beyond Sanctuary Tech?** Currently the only auto-demote is trauma-informed + Sanctuary Tech. If trauma-informed mode is active with another library (Memoir, Warm Editorial), should branded-intro also be force-demoted? Not covered yet. Maria's call.
2. **Counter+wipe variant in Recipe 6 is described but not coded.** The Creative Studio default is "counter+wipe" but the recipe shows the basic curtain wipe with the counter mentioned in the Variants paragraph. If a build hits this default, the agent has to compose the counter from `gsap.to({val: 0}, {val: 100, snap: 'val', onUpdate: ...})` — that pattern is documented but not in a complete code block. Could be expanded.
3. **No automated test for the interview flow.** Phase 4.0 audits provenance after the fact; there's no pre-flight check that the interview actually included Axis 9 in the message sent. A test build with `page-load: <missing>` would catch this — worth adding to a future verification round.
4. **Sidecar generator (`generate-sidecars.py`) does not yet read `page-load`.** If the sidecar contract translates DESIGN.md → tokens.json/tailwind.config.js, page-load is a behavioural axis (not a token) so it likely doesn't apply. Worth confirming when sidecar work resumes.

---

## State of the skill at end of session

- **Phases**: 1 (ANALYSE) → 2 (TRANSLATE: 9-axis interview → library mapping → DESIGN.md derivation) → 3 (BUILD: loads motion-tactics + loader-patterns + build-tactics + layout-patterns conditionally) → 4 (REVIEW: lint + style-specific + universal + layout integrity + divergence audit + delivery)
- **Style libraries**: 12 (Neo-Brutalist, Editorial Portfolio, Technical Refined, Basalt E-Commerce, Memoir Blog, Creative Studio, Warm Serene Luxury, Playful Bento, Spritify, Sanctuary Tech, Warm Editorial, Custom/Freestyle)
- **Reference files**: 10 (`base-principles`, `build-tactics`, `inspiration-analysis`, `user-overrides`, `style-tuning`, `layout-patterns`, `motion-tactics`, `loader-patterns` ← NEW, `typography-safety`, `sidecar-contract`)
- **Per-library default tables**: 9-axis profile in `style-tuning.md` + page-load recipe map in `loader-patterns.md` — must stay in sync if libraries are added/removed.
