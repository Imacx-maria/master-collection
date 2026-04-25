# Typography Safety

How to pick line-height correctly — without over-tightening tiny text or over-loosening big type. The model is **deviation from a baseline anchor**, modulated by tier and content shape, not a flat minimum floor across all sizes.

Load this file in **Phase 3 (BUILD)** when defining type tokens, and consult during **Phase 4 (REVIEW)** as part of the typography integrity audit.

---

## 🧠 The baseline anchor

**120%–145% of font size** is the safe, proven default. That's the anchor. Everything below is conscious deviation; everything above is conscious deviation. Both are legitimate — but only at the right tier.

```
1.2 ─────────────── 1.45
        anchor zone
```

Default to **1.4 for body**, **1.1 for headings**, **1.0 for hero**. Tweak from there visually, not mathematically.

---

## 📏 The four tiers

Pick line-height by **what role the text is playing**, not by font size alone. A 14px label and a 14px body paragraph live at different line-heights even at the same size, because their job is different.

### Tier 1 — Body / reading text (paragraphs, articles, dashboards)

**Range: `1.3` – `1.5`** (sweet spot ~1.4)

Why:
- Too tight → eye loses the line on long passages
- Too loose → reading flow breaks, vertical rhythm collapses

This is the only tier where line-height is **structurally required** to be in range. Body below `1.3` reads as cramped tech UI. Body above `1.5` reads as a Word doc.

### Tier 2 — Medium / UI (subtitles, h3, h4, dense card content, labels)

**Range: `1.1` – `1.3`**

Why:
- Compactness with hierarchy intact
- Still readable for short multi-line spans
- Tighter than body because lines are shorter and content is scanned, not read

### Tier 3 — Headlines / display (h1, h2, hero text, big branding)

**Range: `0.9` – `1.2`**

Yes, this includes values **below 1.0**.

Why:
- Big text already has visual separation from sheer size
- Tight spacing = stronger visual impact, more poster-like
- Loose headlines (>1.2) read as amateur instantly

This is where the previous typography-safety doc was wrong. A condensed display headline at `1.08` because "fonts have descenders" actively destroys the impact. The right answer is to evaluate the **content shape** (1-2 lines vs 3+) and adjust within range, not blanket-ban tight values.

### Tier 4 — Minimal text (slogans, button labels, single-line hero)

**Range: `0.85` – `1.1`** (often **optical**, not mathematical)

Why:
- These are designed as shapes, not paragraphs
- Optical balance > readability rules
- One short line has no "next line" to collide with

Don't compute these from a table. Set, look, adjust by eye.

---

## ⚡ Quick cheat sheet

| Tier | Line-height | Default |
|------|-------------|---------|
| Body / reading | 1.3 – 1.5 | **1.4** |
| Medium / UI | 1.1 – 1.3 | **1.2** |
| Headlines / display | 0.9 – 1.2 | **1.0** |
| Minimal (1-line) | 0.85 – 1.1 | **1.0** |

Start there. Tweak visually.

---

## ⚠️ Modifiers — the rules designers actually live by

Pick a value from the tier's range, then move within the range based on these:

### Modifier 1 — Line length controls spacing

- **Long lines** (60+ chars) → push **toward upper end** of range
- **Short lines** (under 40 chars) → push **toward lower end** of range

Long lines need more leading because the eye has further to travel back to the next line's start. Short lines don't have this problem; tighter leading reads as more deliberate.

If you ignore this, your design feels "off" even if the numbers are technically "correct".

### Modifier 2 — Font character (heavy / large x-height / condensed)

**Increase line-height (+0.05 to +0.10)** when the font is:
- Heavy or bold weight (700+)
- Large x-height (the lowercase letters take more vertical room)
- Condensed (Anton, Druk, League Spartan)

**Decrease line-height (-0.05)** when the font is:
- Light weight (300 or below)
- Airy or wide
- Low x-height (lots of internal padding inside the em)

### Modifier 3 — Line count (the optical permission)

- **1 line** — almost any value works; pick optically. Default to 1.0.
- **2 lines** — stay in tier range, tweak by eye
- **3+ lines** — push toward upper end of tier range; descenders and accents become visible failure risks

This is why a hero in 1 line can be `0.9` and look great, while the same font same size at 3 lines needs `1.05+`.

### Modifier 4 — Language (diacritic load)

For body text in any language: no adjustment needed (1.3-1.5 has the headroom).

For **display in non-English with stacked diacritics** (pt, fr, es, de, vi, cs, pl, hu) **and** 3+ lines **and** condensed font: add `+0.05` to your tier value.

This is the narrow case where accents on uppercase headlines (`Ã`, `Ó`, `Ñ`) collide with line above. It's real, but it's the **convergence** of conditions, not any single one.

---

## 🧩 The pro heuristic (start here, then tune)

```
body          → 1.4
heading (h2-h4) → 1.1 to 1.2
hero (h1)       → 1.0
button / label  → 1.0
```

Then check the build with:
- The longest realistic copy in each tier (not lorem)
- The actual language (with accents if applicable)
- The actual font, not a system fallback

Adjust visually. There is no single perfect value.

---

## 🚫 When tight is correct (don't "fix" these)

These are not bugs:

- **Hero in 1-2 lines, condensed display, English copy, no descenders** → `0.9-1.0` is correct. Tightening makes the headline a solid visual block. Loosening makes it look like a default Word headline.
- **Display caps** (Anton, Druk) in a brand mark → `0.85-0.95` is often the right answer optically. Math-derived 1.08 will feel limp.
- **Pull-quote hero in serif italic** → `1.0` for a 2-line quote. The italic cant gives perceived breathing room.
- **Button label** → `1.0` is universal. Don't touch.

If the design-reviewer flags these as failures, override the audit with documented reason in provenance: *"Hero is 1-line controlled copy; tight leading is intentional impact choice (typography-safety.md tier 4 / minimal)."*

---

## ⚠️ When tight is wrong (real failure modes)

These ARE bugs:

### Failure T1 — Body below tier 1 floor
Body copy at `line-height: 1.2`. Reads as cramped, breaks scanning. Fix: bring to 1.4.

### Failure T2 — Headline crammed when modifiers converge
Headline at `line-height: 0.85` AND condensed font AND 3+ lines AND non-English with accents. Lines collide; descenders clip. Fix: stay in tier 3 range but push to upper end (1.05-1.10) for this specific combination.

### Failure T3 — Compounding compression
`line-height: 0.9` AND `letter-spacing: -0.05em` AND `word-spacing: 0`. Three tight axes. Fix: loosen one, usually the line-height.

### Failure T4 — Mono headline at headline line-height
DM Mono / Geist Mono at headline size with `line-height: 0.95`. Mono glyphs don't have the optical metrics for tight leading at scale. Fix: mono headlines need 1.10-1.20 even when display-equivalent sans is at 1.0.

### Failure T5 — Display caps without tracking
Uppercase display with `letter-spacing: 0` and tight line-height. Letters read as a wall. Fix: add `+0.02em` to `+0.04em` tracking; tight line-height is fine.

### Failure T6 — Body too small AND too tight
14px body with line-height 1.3 = 18.2px line distance. Cramped. Fix: either size up to 16px+, or push line-height to 1.5.

---

## 🧠 The brutal truth

If your typography looks bad, it's almost never the font. It's:
- Wrong line-height for the **tier** (using body values on hero, or hero values on body)
- Wrong **line length** modifier (long lines with tight leading, short lines with loose)
- Inconsistent **rhythm** (every section using a different scale)

Typography safety isn't a floor. It's **choosing the right tier and tuning within its range**.

---

## Audit checklist (Phase 4)

For every type token in the build:

- [ ] Which **tier** does this token serve? (body / medium / hero / minimal)
- [ ] Is its line-height **inside the tier's range**?
- [ ] Has the **line length modifier** been applied? (long → upper, short → lower)
- [ ] Has the **font character modifier** been applied? (heavy/condensed → +; light → −)
- [ ] If display + 3+ lines + non-English + condensed → has language modifier been applied?
- [ ] Body never below 1.3
- [ ] Hero loose ( >1.2 ) flagged — usually a bug
- [ ] No compounding compression (1 tight axis max on the same token)

If a token is **deliberately outside** its tier range (e.g., hero at 0.85 for impact), document the reason in DESIGN.md provenance. Outside-range without rationale = refactor.

---

## Pre-build checklist (run before writing display CSS)

For each display/headline token, answer:

1. What **tier** is this token? (body / medium / hero / minimal)
2. How many **lines** will the typical copy span? (1 / 2 / 3+)
3. Is the font **condensed, heavy, or large-x-height**?
4. What **language(s)** will the copy be in?
5. What's a sensible **starting value** from the tier range, with modifiers applied?

Set that as the line-height. Then check the actual rendered build with realistic copy.

Don't start from a flat minimum; start from the tier's anchor and deviate with reason.
