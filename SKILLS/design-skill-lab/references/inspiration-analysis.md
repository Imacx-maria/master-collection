# Inspiration Analysis

How to read an inspiration image, URL, or visual reference *without* copying it.

## Why This File Exists

When a user drops an image and says "make something like this", the failure mode is literal reproduction. The output becomes recognisable as "the inspiration with different content swapped in". This file is the mental discipline for extracting the *system* behind a reference instead of its surface.

## The Extraction Briefing

After examining the reference, produce a 5–8 line briefing. State it out loud to the user before proceeding. Format:

```
Direction (not target): <one-line mood statement>

Tokens to borrow:
- Colors: <2–3 dominant hex approximations, role-labeled>
- Typography: <category — not specific font names unless visually certain>
- Spacing density: <tight | medium | generous>
- Composition: <grid | asymmetry | poster | reading-column | layered>
- Motion vocabulary (if inferable): <mechanical | soft | none>

Tokens to avoid borrowing:
- <anything too specific to the original — hero layout, logo treatment, unique illustration, signature visual gimmick>

Mood keywords: <3–5 words>
```

The "tokens to avoid" line is the most important one. It is the explicit commitment to not copy specific visual moves.

## What to Extract vs What to Ignore

**Extract (the system):**
- Type hierarchy ratios (how much bigger is the hero vs body?)
- Color role distribution (60-30-10 split, monochrome + accent, etc.)
- Spacing rhythm (does the layout breathe or compress?)
- Structural logic (grid-driven, asymmetric, centered, full-bleed)
- Contrast strategy (high-contrast monochrome, low-contrast warm, dark + neon accent)
- Motion philosophy if visible (mechanical, soft, none)
- Restraint level (loud everywhere vs loud in one place)

**Ignore (the surface):**
- Specific hero composition
- Specific illustrations, photographs, or brand marks
- Specific copy tone or wording
- Signature UI gimmicks (the bespoke carousel, the one-off scroll effect)
- Exact hex values — approximate to the *role* they play

## Translating the Extraction Into a Library Choice

After the briefing, map to the library menu:

| Extracted quality | Likely library |
|---|---|
| Grid-visible, sharp edges, monochrome + accent, uppercase display | Neo-Brutalist |
| Compressed uppercase type, off-white, hover-reveal panels, image-led | Editorial Portfolio |
| Clean sans + mono, teal or vivid accent, dashed borders, technical calm | Jocril Technical |
| Serif display + neutral sans, split layouts, restrained product photography | Basalt E-Commerce |
| Sans body + serif italic accent, creamy neutral, reading-first card grids | Memoir Blog |
| Dark charcoal + bright coral/accent, rounded cards, full-color imagery | Creative Studio |
| Serif display + humanist sans, warm neutrals, numbered items, imagery-driven | Warm Serene Luxury |
| Bento grids, hierarchy-aware cards, saturated palette, energetic | Playful Bento |
| Geometric sans, switchable palettes, playful component shapes | Spritify |
| Monospace, dashed borders, muted tones, generous whitespace | Sanctuary Tech |
| None match cleanly | Custom / Freestyle |

If two libraries match partially, that's the signal to use the **dominant + secondary influence** pattern in Phase 2. Pick the one that covers the structural logic as dominant; the other contributes accents or type pairings.

## Divergence Prompts

Once a library is selected, use these prompts to ensure the project DESIGN.md actually diverges from the library default:

- *"If the library uses teal, what other accent carries the same mood but isn't teal?"*
- *"If the library pairs Geist Sans + Mono, what different pairing preserves the technical feel?"*
- *"If the library uses dashed borders, what other structural motif creates similar visual rhythm?"*
- *"If the inspiration has signature element X, how do we evoke the same *effect* without element X?"*

Any two divergence moves are enough to meet the 2-token rule. More is fine if they strengthen the brief.

## Fidelity Levels

Not every reference deserves the same treatment. There are 3 fidelity levels — defined in detail in `references/user-overrides.md` § Fidelity Scale:

- **Inspired (default)** — Extract systems, build original. Full 2-token rule applies. Output is "in the spirit of" the reference.
- **Adapted** — Borrow palette + type from the reference; layout and composition diverge. Output is "in the same family" but not the same site.
- **Faithful** — Close visual reproduction with minor differences. Divergence rule waived (documented). Reserved for clone-for-learning contexts.

Ask the user to choose if intent is unclear:
- *"How close to your reference should the result be? Inspired (extract systems), Adapted (borrow palette + type), or Faithful (close reproduction)?"*

Default to **Inspired** if not asked. Move on after one question.

**Never assume Faithful** is intended just because a reference was provided. The default position is always Inspired — the reference seeds, never dictates.

Even at Faithful, IP boundaries hold: no logo reproduction, no signature illustrations, no trademarked brand assets.

## Common Failure Modes

**Failure 1 — "Inspired by" becomes "same but different content."** The new output uses the reference's exact hero structure, navigation pattern, and visual motifs. Fix: diverge in at least composition *or* type pairing.

**Failure 2 — Extracting too many specific tokens.** The briefing lists 6 exact hex values, 3 specific fonts, and a hero layout diagram. Fix: stay at the category level. "A warm off-white around #F4F2F0-ish" not "#F4F3F0 exactly".

**Failure 3 — Ignoring the composition.** Only colors and fonts get extracted; the structural logic is missed. Fix: the composition line is non-optional. Every reference has one.

**Failure 4 — Mood keywords that are style-library names.** "Mood: brutalist, editorial, technical" is routing language, not mood. Fix: use experiential words — "confrontational, precise, archival, tense, calm, celebratory".

## Short Example

**User uploads a screenshot of a minimal Japanese fashion brand landing page.**

Briefing:
```
Direction (not target): Disciplined calm with one assertive moment.

Tokens to borrow:
- Colors: deep charcoal primary (#1A1A1Aish), warm off-white neutral (#F5F2EDish), single muted clay accent
- Typography: serif display + compressed geometric sans body
- Spacing density: generous, reading-column
- Composition: asymmetric with one large image anchor
- Motion vocabulary: soft fades only, no parallax

Tokens to avoid borrowing:
- The specific katakana typographic treatment
- The horizontal product carousel gimmick
- The model photography style

Mood keywords: composed, deliberate, quiet, warm, confident
```

Library choice: **Editorial Portfolio** as dominant (compressed type, off-white, asymmetric composition, image-led) with **Warm Serene Luxury** as secondary influence (the warmth, the clay accent, the generous spacing).

Divergences planned for the project DESIGN.md:
1. Swap the library's hover-reveal panels for a static asymmetric grid (composition)
2. Introduce a warm clay accent not present in either library default (color)
