---
version: alpha
name: Atmospheric Protocol
description: Editorial-meets-technical dark system — Instrument Serif display headlines (often paired with italic continuation), Inter for UI and data chrome, glass cards on near-black surface, and a load-bearing gradient atmosphere chosen from three named variants (Bloom, Flow, Particle).
colors:
  primary: "#FFFFFF"
  secondary: "#A1A1AA"
  tertiary: "#71717A"
  quaternary: "#52525B"
  background: "#030508"
  surface: "#080A10"
  surface-card: "#0A0D14"
  surface-glass: "rgba(3, 5, 8, 0.80)"
  surface-elevated: "#10131C"
  on-surface: "#FFFFFF"
  on-surface-muted: "#D4D4D8"
  border-hairline: "rgba(255, 255, 255, 0.05)"
  border-soft: "rgba(255, 255, 255, 0.08)"
  border-strong: "rgba(255, 255, 255, 0.12)"
  accent-bloom: "#6366F1"
  accent-flow: "#8F47AE"
  accent-particle: "#FFFFFF"
  accent-soft-bloom: "rgba(99, 102, 241, 0.20)"
  accent-soft-flow: "rgba(143, 71, 174, 0.20)"
  data-positive: "#10B981"
  data-warning: "#F59E0B"
  focus: "#3898EC"
typography:
  display-xl:
    fontFamily: "Instrument Serif, 'Source Serif 4', Georgia, serif"
    fontSize: 88px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -0.025em
  display-lg:
    fontFamily: "Instrument Serif, 'Source Serif 4', Georgia, serif"
    fontSize: 72px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: -0.025em
  display-italic:
    fontFamily: "Instrument Serif, 'Source Serif 4', Georgia, serif"
    fontSize: 88px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -0.025em
    fontStyle: italic
  headline-lg:
    fontFamily: "Instrument Serif, 'Source Serif 4', Georgia, serif"
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.10
    letterSpacing: -0.02em
  headline-md:
    fontFamily: "Instrument Serif, 'Source Serif 4', Georgia, serif"
    fontSize: 32px
    fontWeight: 400
    lineHeight: 1.20
    letterSpacing: -0.015em
  card-title:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.30
    letterSpacing: -0.005em
  body-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0
  body-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.625
    letterSpacing: 0
  label-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0
  overline:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.45
    letterSpacing: 0.10em
    textTransform: uppercase
  data:
    fontFamily: "JetBrains Mono, 'IBM Plex Mono', SFMono-Regular, Consolas, monospace"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0
rounded:
  sm: 6px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  pill: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
  5xl: 96px
  6xl: 128px
  pad-button: 6px
  pad-card: 32px
  pad-glass: 20px
container:
  max-width: 1280px
  padding-x: 32px
shadows:
  card-soft: "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
  card-bloom: "0 25px 50px -12px rgba(99, 102, 241, 0.20)"
  card-flow: "0 25px 50px -12px rgba(143, 71, 174, 0.18)"
  inset-highlight: "inset 0 1px 0 rgba(255, 255, 255, 0.05)"
  ring-hairline: "0 0 0 0.67px rgba(255, 255, 255, 0.05)"
motion:
  fast: 150ms
  base: 300ms
  reveal: 700ms
  ambient-slow: 8000ms
  ambient-flow: 20000ms
  ease-standard: "cubic-bezier(0.4, 0, 0.2, 1)"
  ease-signature: "cubic-bezier(0.2, 0.7, 0.2, 1)"
  ease-ambient: "cubic-bezier(0.4, 0, 0.6, 1)"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#000000"
    typography: "{typography.label-md}"
    rounded: "{rounded.pill}"
    padding: "{spacing.pad-button}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm}"
    border: "0.67px solid {colors.border-strong}"
  button-link:
    backgroundColor: "transparent"
    textColor: "{colors.tertiary}"
    typography: "{typography.label-md}"
    rounded: "0px"
    padding: "0px"
  nav-pill:
    backgroundColor: "{colors.surface-glass}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.pill}"
    padding: "{spacing.sm}"
    border: "0.67px solid {colors.border-soft}"
    blur: "12px"
  card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.2xl}"
    padding: "{spacing.pad-card}"
    shadow: "{shadows.card-soft}"   # MANDATORY — never omit; cards on bloom backdrop without shadow read as ghost outlines
  card-featured:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.2xl}"
    padding: "{spacing.pad-card}"
    shadow: "{shadows.card-bloom}"  # accent-tinted shadow for hero/featured cards (Bloom variant)
    note: "Use card-bloom shadow only on 1-2 hero/featured cards per page; standard cards stay on card-soft"
  card-glass:
    backgroundColor: "{colors.surface-glass}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.pad-glass}"
    border: "0.67px solid {colors.border-hairline}"
    blur: "12px"
    shadow: "{shadows.card-soft}"   # MANDATORY — even glass cards need a shadow anchor
  data-pill:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.data}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs}"
    border: "0.67px solid {colors.border-hairline}"
  overline-tag:
    backgroundColor: "{colors.surface-glass}"
    textColor: "{colors.on-surface}"
    typography: "{typography.overline}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs}"
    border: "0.67px solid {colors.border-soft}"
---

## Overview

Atmospheric Protocol is the visual language of the cognitive-tooling and protocol-infrastructure surface — Neuform, Nexus, Stripe-adjacent infrastructure landing pages, AI editorial product pages with technical chrome. The page reads simultaneously as a literary editorial (serif display typography with frequent italic continuations) and as a piece of technical infrastructure (data pills, monospace metrics, glass cards with hairline gradient borders, an atmospheric backdrop that breathes).

The signature move is the **gradient backdrop as load-bearing element**, not decoration. The page is built atop one of three named atmospheres — Bloom (radial colour glows), Flow (smoky linear shift), or Particle (WebGL dot-matrix breathing) — and the rest of the system (chrome, type, components) is calibrated to sit *quietly* on top. Restraint above; atmosphere below. If both layers shout, the style breaks.

## Colors

Dark mode only. The palette is intentionally narrow: near-black canvas, three steps of glass surface, white-and-three-greys text, one accent (varies per variant), and tightly controlled hairline borders.

- **Primary (#FFFFFF):** Text on dark surfaces; primary button background.
- **Secondary (#A1A1AA):** Body copy on dark; muted UI text.
- **Tertiary (#71717A):** Supporting copy, captions, link rest state.
- **Quaternary (#52525B):** Footnotes, disabled states, lowest-contrast metadata.
- **Background (#030508):** Page canvas. Near-black with a faint blue undertone (vs. pure `#000` which reads as void).
- **Surface (#080A10):** Subtle elevation above the canvas — section backings, full-bleed bands.
- **Surface-card (#0A0D14):** Standard opaque card background. The "solid" card recipe.
- **Surface-glass (rgba(3,5,8,0.80)):** Translucent card requiring `backdrop-filter: blur(12px)`. The atmospheric backdrop bleeds through; the card reads as ice.
- **Surface-elevated (#10131C):** Inputs, data pills, the slightly brighter chrome that sits inside cards.
- **Border-hairline (rgba(255,255,255,0.05)) / Border-soft (0.08) / Border-strong (0.12):** Three tiers of white-at-low-opacity borders. Always 0.67px (the "Webflow hairline" — sharper than 1px, scales correctly on Retina).
- **Accent-bloom (#6366F1):** Indigo. The Bloom variant accent — appears in radial blooms behind cards, in CTA hover halos, in data-positive states.
- **Accent-flow (#8F47AE):** Violet. The Flow variant accent — runs through the smoky linear gradient and tints the gradient border shells.
- **Accent-particle (#FFFFFF):** Particle variant deliberately uses no chromatic accent — the particle field is monochromatic white, the page reads as pure data.
- **Focus (#3898EC):** Accessibility blue for input focus rings (the only cool colour reserved purely for a11y).

The accent choice is **per-variant, not per-page**. A Bloom-variant build uses indigo throughout. A Flow-variant build uses violet throughout. Mixing accents across a single page breaks the atmospheric coherence — the gradient and the chrome must agree.

## Typography

Instrument Serif (Source Serif 4 fallback) carries every display moment — at weight 400 only. The single-weight discipline matches Warm Editorial's logic but the cadence here is colder, more declarative. The signature **italic continuation** move appears constantly: a roman headline followed by an italic variant of the same family on the next line ("Better questions. *Better answers.*" / "Capital orchestration *redefined.*" / "Cognitive Calibration *Protocol.*"). The italic is not decoration — it's how the headline finishes its thought.

Inter handles UI, body, labels, and card titles at three weights (400 / 500). Body line-height is moderate (1.55–1.60) — tighter than Warm Editorial's literary 1.60, looser than dashboard-tight 1.40. The page should read like a research paper, not a magazine and not a Bloomberg terminal.

JetBrains Mono (or IBM Plex Mono) is reserved for **data**: metric values, percentages, code references, system labels in the chrome of cards ("NEXUS_VM V3.0" / "POLICY_V2"). Never used for body or display.

Tiny labels (12px) carry deliberate `letter-spacing: 0.10em` and uppercase transformation when they function as overline tags ("● CORE CAPABILITIES" / "● THE FUNDAMENTAL AXIOM"). The leading dot character (●) before the overline is part of the signature — it reads as a status LED, reinforcing the protocol/infrastructure mood.

## Layout

Bounded grid composition. Container caps at 1280px with 32px page padding. Sections breathe at 96–128px vertical spacing on desktop. The hero pattern is consistent across the style: small overline pill, centred display headline (often two-line with italic continuation), supporting `body-lg` paragraph at ~60ch max width, then a 3-column glass-card grid below. After the grid, a wide editorial quote in `headline-lg` serif (often italicised mid-sentence) sets up the next section.

The 3-card grid is the load-bearing structural pattern. Each card is identical in width, varies in internal content (one shows a data console, one shows an interactive widget, one shows a metrics pill). The variation in content with consistency in card dimension is the rhythm.

## Shapes

Two distinct radius families coexist:

- **Soft and large** for cards and hero panels (`{rounded.2xl}` = 32px standard; the source DESIGN files used 31px and 23px — the system rounds to 24/32 for cleaner Tailwind mapping).
- **Tight and pill** for chrome (`{rounded.pill}` for nav, primary buttons, overline tags; `{rounded.md}` = 12px for secondary buttons; `{rounded.sm}` = 6px for data pills inside cards).

Iconography is **linear** weight (Solar / Lucide / Phosphor light), stroke 1.5px. No filled icons except for the leading status-LED dot in overlines. Geometric icons (squares, circles, octagons used as logos) are acceptable as glyphs; never use illustrative or 3D icons.

## Depth

Depth is communicated through three layered mechanisms, used together:

1. **Glass surfaces** — `backdrop-filter: blur(12px–24px)` on translucent cards, letting the atmospheric backdrop bleed through. The blur is what makes the card read as ice rather than just a darker rectangle.
2. **Hairline gradient border shell** — every card on the page wears a 1px gradient border that fades from `rgba(255,255,255,0.10)` at the top to transparent at the bottom (or accent-tinted for Bloom/Flow variants). This is the premium-feel signature; remove it and the cards read as flat blocks. Recipe in `gradient-tactics.md` § Recipe 6.
3. **Coloured shadow tied to accent** — Bloom variant uses `shadow: 0 25px 50px -12px rgba(99,102,241,0.20)` on featured cards, replacing the default black shadow. The shadow tints the substrate and visually links the card to the gradient backdrop above.

Drop shadows below `card-soft` are the standard; the bloom-tinted shadow is reserved for hero or featured cards. Never both on adjacent cards (creates noisy hierarchy).

## Atmosphere variants

This is the style's defining axis. Pick one variant per build; document the choice in the brief.

### Bloom (radial glow blooms)

- **Source:** Nexus screenshot — multiple soft indigo/violet planet-glow ellipses scattered behind cards.
- **Recipe:** `gradient-tactics.md` § Recipe 1 (layered radial mesh, dark-mode pattern). 3 blooms, indigo + violet stops, 0.12–0.18 opacity each.
- **Use when:** the page feels capital-infrastructure / financial / orchestration / "operating at scale." The blooms read as scattered light sources, suggesting depth and presence.
- **Accent token:** `accent-bloom` (#6366F1). All buttons, links, focus moments, data-positive states use indigo.
- **Card shadow:** `card-bloom` (indigo-tinted) on hero cards, `card-soft` (neutral black) on standard cards.

### Flow (smoky linear shift)

- **Source:** Neuform "Cognitive Calibration" screenshot — wavy smoky gradient flowing diagonally across the page, animated slowly.
- **Recipe:** `gradient-tactics.md` § Recipe 2 (smoky linear flow, 400% size, 20s ease-in-out shift). Pair with Recipe 3 (SVG `feTurbulence` grain overlay, opacity 0.3, static seed).
- **Use when:** the page feels cognitive / philosophical / editorial / "rewriting your thinking." The flow + grain reads as ambient consciousness, suggesting introspection.
- **Accent token:** `accent-flow` (#8F47AE). Violet runs through gradient stops and accent moments alike.
- **Card shadow:** `card-flow` (violet-tinted) on hero cards.

### Particle (WebGL dot-matrix breathing)

- **Source:** DESIGN_2 spec — full-bleed WebGL canvas, 800–3000 dots in a grid or Poisson distribution, breathing pulse motion, optional pointer-reactive drift.
- **Recipe:** `gradient-tactics.md` § Recipe 5 (particle field, breathing pulse shader). Pair with a flat `#030508` page background (no radial blooms — the particles ARE the atmosphere).
- **Use when:** the page feels protocol / data / quiet-technical / "system signal." The particles read as dataflow without representing anything specific.
- **Accent token:** `accent-particle` (#FFFFFF). The page is monochromatic; chromatic accent is intentionally absent.
- **Card shadow:** `card-soft` only (no chromatic shadows — the particle field provides all the atmospheric colour).
- **Mandatory fallback:** CSS gradient background on the canvas's parent element so WebGL failure leaves a designed page, not nothing. See `gradient-tactics.md` § Recipe 5 pre-build checklist.

## Components

- **`button-primary`** — White pill on dark, black text, full radius. The single high-contrast moment per section. Used for hero CTAs ("Acquire Book," "Initialize," "Secure the Manual").
- **`button-secondary`** — Transparent with hairline border, muted text, 12px radius. The workhorse — most chrome buttons sit at this weight.
- **`button-link`** — Plain text in tertiary grey, no chrome, hover lifts to white. Nav items use this.
- **`nav-pill`** — Glass capsule (blur 12px, hairline border) housing nav links + a primary CTA. Floats fixed at the top, centred. Width responds to content.
- **`card`** — Standard opaque card (`#0A0D14`, 32px radius, 32px padding, `card-soft` shadow). The 3-card grid uses this.
- **`card-glass`** — Translucent card (`rgba(3,5,8,0.80)`, 16px radius, 20px padding, hairline border, `backdrop-filter: blur(12px)`). Used inside other cards (e.g. the "PROCESSING SPEED" widget inside the Velocity Extraction card).
- **`data-pill`** — Tiny chrome chip housing a metric or system label ("NEXUS_VM V3.0," "0.02ms," "$124,500.00"). Monospace text, hairline border, slightly elevated background.
- **`overline-tag`** — Glass pill housing the section overline ("● CORE CAPABILITIES"). The leading status dot is character-level (●), not an SVG.

The gradient border shell is a wrapper pattern, not a component — wrap any card in `.gradient-shell` (recipe in `gradient-tactics.md` § Recipe 6) to get the premium hairline frame.

## Do's and Don'ts

- **Do apply `--shadow-card-soft` (or `--shadow-card-bloom` for hero/featured cards) to every card on the page.** Cards without shadow read as "ghost outlines" against the bloom backdrop — the bloom shows past the card edges and the eye reconstructs an apparent second card. The shadow anchors the card visually. **This is non-negotiable.**
- Do build on top of one of the three atmospheres — Bloom, Flow, or Particle — and pick it before writing markup
- Do use Instrument Serif at weight 400 only, with italic continuation as the headline-completion move
- Do reserve monospace (JetBrains Mono) strictly for data, metrics, system labels — never for body
- Do wear hairline borders at 0.67px (not 1px) and white at 5–12% opacity (not solid grey)
- Do use the gradient border shell on every card on the page — it's the premium-feel signature
- Do match the accent colour to the variant: Bloom = indigo, Flow = violet, Particle = monochrome white
- Do use the `●` status-dot character before overlines as a signature glyph
- Don't mix two atmospheres on one page — pick one
- Don't use bold (700+) on serif headlines — 400 is the only weight, italic is the only variation
- Don't use saturated chromatic colour outside the chosen accent — the palette is monochromatic-with-one-hue
- Don't use heavy drop shadows or coloured ambient lighting beyond the bloom-tinted card shadow recipe
- Don't introduce a light mode for this style — the entire system is dark-mode-native; light mode requires Warm Editorial or another style entirely
- Don't load the WebGL particle field without a CSS gradient fallback on the parent element
- Don't animate more than 2 things at once on the page (the atmosphere is the primary motion budget; layered card animations compound and feel nervous)
- Don't drop the gradient border shell to "save effort" — it's the difference between this style and a generic dark Tailwind dashboard
- **Don't set `max-width` on a card's inner content surface (`shell-content` / `testimonial-inner` / etc.) when its `gradient-shell` wrapper extends wider.** The shell background gets exposed on the sides where the inner doesn't cover, producing a visible misalignment. Apply `max-width` to the wrapper, not the inner.
- **Don't ship cards without a shadow.** Defining shadow tokens in CSS but not applying them to `.gradient-shell` / `.card` / `.shell-content` is the most common Atmospheric Protocol regression. Mechanical check: grep your build for `box-shadow` — every card class should have one.
