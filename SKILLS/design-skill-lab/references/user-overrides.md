# User Overrides

How to detect and handle user-provided design constraints — colors, fonts, image references, website URLs — without breaking the system's anti-template guarantees.

Load this file in **Phase 1 (ANALYSE)** when any of the override triggers below are detected.

---

## Why This File Exists

The 4-phase workflow has a non-negotiable rule: the project DESIGN.md must diverge from the library default in at least 2 tokens. This rule prevents the failure mode of "every output looks the same".

But users often provide concrete constraints — exact brand colors, a specific font, a website to match, a screenshot to follow. If the agent ignores these, the user is rightly frustrated. If the agent obeys them blindly, the output becomes templatey.

This file defines the protocol that resolves the tension.

---

## Detection Triggers

Run this check at the start of Phase 1, before selecting a style library.

### Trigger 1 — Explicit colors in prompt

Look for any of:
- Hex codes (`#2DD4CD`, `#000`)
- Named brand colors ("Stripe purple", "Linear teal")
- Color descriptions with role ("our primary is X, accent is Y")
- Attached color palette images (Coolors export, brand guideline screenshots)

### Trigger 2 — Explicit fonts in prompt

Look for any of:
- Font family names ("use Inter", "Geist Sans only")
- Font pairing requests ("serif headings + sans body")
- Custom font files attached (.woff2, .ttf, .otf)
- Brand guideline references that name fonts

### Trigger 3 — Image / screenshot reference

Look for any of:
- Uploaded image files (.png, .jpg, .webp)
- Pinterest board links
- Mood board attachments
- Screenshots of competitors or inspiration sites

### Trigger 4 — URL / website reference

Look for any of:
- Direct URLs to live sites
- "Like X website" without URL (treat as soft URL ref)
- Competitor names that imply a known visual identity ("like Linear", "like Stripe")
- Behance / Dribbble / Awwwards project links

If **none** of these triggers fire, proceed with the standard 4-phase workflow — no overrides apply.

If **any** trigger fires, follow the matching protocol below.

---

## Color Override Protocol

When user provides specific colors:

### Step C.1 — Acknowledge and capture
State explicitly which colors were captured and their assumed roles. If roles are ambiguous, ask one tight question:
- *"You provided #2DD4CD and #0A0A0A. Treat #2DD4CD as accent and #0A0A0A as primary text?"*

If user provides only 1-2 colors, derive the rest from the chosen library's palette logic (don't invent — extend systematically).

### Step C.2 — Apply colors verbatim in DESIGN.md
The user's colors go into the project DESIGN.md tokens exactly as given. No "approximation" or "shifted slightly for taste".

### Step C.3 — Mark colors as a divergence
The color override counts as **one** divergence from the library default. Note this explicitly in the DESIGN.md provenance section:
> *"Divergence 1 (color): User-provided palette overrides library default."*

### Step C.4 — Require an ORTHOGONAL second divergence
You still need one more divergence — but it **cannot** be in the color axis. Pick from:
- Typography pairing (swap one half of the library's default pairing)
- Spacing density (tighten or loosen the scale)
- Shape system (sharpen or soften radii)
- Component composition (e.g., panel-overlay → caption-strip pattern)

State the orthogonal divergence explicitly in the DESIGN.md provenance.

### Why orthogonal?
If both divergences were "I changed the colors", the output is structurally identical to the library default with paint swapped. That's still template copy by another name. Forcing an orthogonal second divergence guarantees the system fingerprint differs from the library default.

---

## Font Override Protocol

When user provides specific fonts:

### Step F.1 — Acknowledge and validate
- Confirm font availability (Google Fonts, Adobe Fonts, custom file)
- If user gives only one font, ask whether to keep the library's secondary font or pick a complement

### Step F.2 — Apply fonts in DESIGN.md typography tokens
Replace the library's `fontFamily` values with user-provided fonts. Adjust `fontWeight`, `letterSpacing`, and `lineHeight` to suit the new family — don't blindly carry over the library's tracking values, which may have been tuned for the old font.

### Step F.3 — Mark as divergence
Font override = **one** divergence. Same orthogonal-second-divergence rule applies (see Step C.4).

### Step F.4 — Compatibility check
Some library defaults assume specific font characteristics:
- Brutalist assumes condensed display fonts (Anton-style). Swapping in a humanist sans (Inter, Manrope) breaks the brutalist feel — flag this to the user.
- Sanctuary assumes monospace throughout. Swapping in a sans breaks the trauma-informed contract — refuse or escalate.
- Memoir relies on the italic-serif accent inside Manrope. If the user removes Source Serif italic, ask what should carry the editorial accent.

If the font change is incompatible with the chosen library's identity, switch libraries — don't force-fit.

---

## Image / Screenshot Reference Protocol

When user attaches an image as inspiration:

### Step I.1 — Run inspiration extraction
Load `references/inspiration-analysis.md` and run the briefing process. Extract direction (not target), tokens to borrow, tokens to avoid, mood keywords.

### Step I.2 — Determine fidelity intent
Ask the user one question (unless context makes it obvious):
- *"How close should the result be to your reference? Inspired (extract systems), Adapted (borrow palette + type, diverge in layout), or Faithful (close reproduction with minor differences)?"*

Default if not asked: **Inspired**.

### Step I.3 — Map to library + divergences
Use the inspiration-analysis library mapping to pick a starting library. Then derive divergences according to fidelity level (see Fidelity Scale section below).

### Step I.4 — If fidelity = Faithful
Document the waiver explicitly:
> *"Fidelity = Faithful. Divergence rule waived per user request — designed to closely follow attached reference."*

This is allowed but should be rare. Faithful mode produces designs vulnerable to looking like copies of the reference's brand.

---

## URL / Website Reference Protocol

When user provides a URL or names a known site:

### Step U.1 — Determine if you can fetch
- If a URL is provided AND web_fetch is available, fetch the homepage
- If web_fetch fails or is unavailable, treat as image reference only (ask user for screenshots)
- If user names a known site without URL ("like Linear"), proceed from training knowledge but state the assumption: *"Working from my understanding of Linear's current design — confirm if anything has changed recently?"*

### Step U.2 — Determine fidelity intent
Ask one question:
- *"How close to [site] should the result be? Inspired (their style of approach), Adapted (their palette + type, your layout), or Faithful (close visual match)?"*

Default if not asked: **Inspired**.

### Step U.3 — Apply fidelity level (see scale below)

### Step U.4 — Refuse outright clones of brand identities
Even at Faithful fidelity, do not reproduce trademarked logos, signature illustrations, or distinctive brand assets. The output should be visually similar in *system* (palette, type, layout patterns) but never *brand-identical*. Refuse and explain if the user explicitly asks for a logo clone.

---

## Fidelity Scale (3 levels)

Applies to image and URL references.

### Level 1 — Inspired (default)

**What it means:** The reference seeds inspiration but the output is original. The 2-token rule applies fully.

**What gets borrowed:**
- Mood, atmosphere, emotional register
- Compositional logic (grid vs asymmetry vs poster)
- Type hierarchy ratios (how much bigger is the hero vs body)
- Contrast strategy (high-contrast monochrome, warm low-contrast, etc.)

**What gets created fresh:**
- Specific colors (start from library palette, optionally shift accent)
- Specific fonts (start from library defaults, optionally swap)
- Specific component compositions
- Layout specifics (the reference's hero structure is *not* copied)

**Required divergences:** 2+ (full rule applies)

**Use when:** User says "I like the vibe of X", "make something with this kind of energy", or doesn't specify fidelity.

### Level 2 — Adapted

**What it means:** The reference's palette and type get adopted, but the layout, composition, and component patterns diverge. Output is recognisable as "in the same family" but not as "the same site with different content".

**What gets borrowed:**
- Color palette (extract 4-6 dominant colors with roles)
- Typography pairing (extract families, approximate weights)
- General density (tight vs spacious)

**What gets created fresh:**
- Layout structure (don't copy hero composition, navigation pattern, section order)
- Component compositions (use library defaults adapted to new colors/type)
- Distinctive visual moves (no copying signature gimmicks)

**Required divergences:** 1+ (the layout/composition divergence). Color and type are now anchored to the reference, so the orthogonal divergence must be in layout or component patterns.

**Use when:** User says "use these colors and fonts but make it your own layout", or attaches a brand guideline document.

### Level 3 — Faithful

**What it means:** Close visual reproduction with minor adjustments to avoid pure clone status. Layout, palette, type, and component patterns all closely follow the reference.

**What gets borrowed:**
- Color palette (verbatim if possible)
- Typography (verbatim families and weights)
- Layout structure (hero composition, navigation pattern, section order)
- Component compositions

**What gets fresh by necessity:**
- Copy and content (always different from reference)
- Imagery (different photos / illustrations to avoid IP infringement)
- Specific micro-interactions (the reference's bespoke gimmicks)

**Required divergences:** 0 (rule waived, but documented in delivery).

**Forbidden even at Faithful:**
- Trademarked logos
- Signature illustrations / brand illustrations
- Distinctive 3D / animation assets unique to the reference brand

**Use when:** User explicitly says "make it look exactly like X", or it's a known clone-for-learning context. Default to asking for confirmation: *"You want a close visual reproduction, not an inspired-by version?"*

---

## Combined Triggers — what if user provides multiple?

| Combination | How to handle |
|------------|---------------|
| Colors + Fonts | Both count as divergences. The 2-token rule is satisfied. Skip orthogonal-divergence requirement. |
| Colors + Image | Apply colors verbatim. Use image for layout / composition cues. Fidelity defaults to Inspired unless user says otherwise. |
| Image + URL of same site | Use both for cross-validation. Image gives visual specifics; URL gives full context. |
| URL + explicit colors | Use URL for layout/type/composition. Use explicit colors as override of URL's palette. State both clearly in provenance. |
| Image + "make it look like our brand" | Treat as Adapted fidelity by default — user wants brand alignment, not reproduction. Confirm. |

---

## Provenance Section in DESIGN.md

When overrides are applied, the project DESIGN.md must include a provenance section at the top of the markdown body, after the YAML frontmatter:

```markdown
## Provenance

- Library base: <library-name>
- Fidelity: <Inspired | Adapted | Faithful>
- User overrides:
  - Colors: <captured palette and source>
  - Fonts: <captured fonts and source>
  - Reference: <image filename or URL>
- Divergences from library default:
  - 1. <axis and brief description>
  - 2. <axis and brief description>
- Notes: <any waivers, compatibility flags, or trade-offs documented during ANALYSE>
```

This makes the design decisions auditable and helps future iterations understand why specific choices were made.

---

## Anti-patterns when handling overrides

- ❌ **Silently ignoring user-provided colors** because "they don't fit the style". If incompatible, escalate — don't override the user.
- ❌ **Asking 5 questions before starting.** One tight question per ambiguity, max two per session. If still unclear, default and document.
- ❌ **Copying the reference image's hero composition** at Inspired fidelity. That's the failure mode this whole protocol exists to prevent.
- ❌ **Refusing all overrides "because divergence rule"**. The rule exists to prevent template copy, not to ignore user constraints. Apply overrides + orthogonal divergence.
- ❌ **Letting Faithful fidelity reproduce trademarked logos or brand illustrations**. Even with the divergence rule waived, IP boundaries hold.
- ❌ **Skipping the provenance section.** Future iterations need to know why specific tokens diverged from the library default.

---

## Quick reference — decision tree

```
User input arrives.
│
├─ Contains explicit colors? ────────► Color Override Protocol
│
├─ Contains explicit fonts? ─────────► Font Override Protocol
│
├─ Contains image / screenshot? ─────► Image Reference Protocol
│                                       └─ Determine fidelity (Inspired/Adapted/Faithful)
│
├─ Contains URL / named site? ───────► URL Reference Protocol
│                                       └─ Determine fidelity (Inspired/Adapted/Faithful)
│
└─ None of the above? ───────────────► Standard 4-phase workflow, no overrides
```
