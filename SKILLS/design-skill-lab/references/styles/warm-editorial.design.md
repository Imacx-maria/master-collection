---
version: alpha
name: Warm Editorial
description: Literary-salon system for AI products, technical writing, and thoughtful tools — parchment canvas, serif headlines at single weight, terracotta brand accent, ring-based depth, exclusively warm-toned neutrals.
colors:
  primary: "#141413"
  secondary: "#5E5D59"
  tertiary: "#87867F"
  neutral: "#F5F4ED"
  surface: "#FAF9F5"
  surface-alt: "#E8E6DC"
  surface-dark: "#30302E"
  brand: "#C96442"
  brand-soft: "#D97757"
  on-primary: "#FAF9F5"
  on-dark: "#B0AEA5"
  border-soft: "#F0EEE6"
  border-warm: "#E8E6DC"
  border-dark: "#30302E"
  ring-warm: "#D1CFC5"
  ring-deep: "#C2C0B6"
  focus: "#3898EC"
  error: "#B53333"
typography:
  display-xl:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 64px
    fontWeight: 500
    lineHeight: 1.10
    letterSpacing: 0
  headline-xl:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 52px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0
  headline-lg:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 36px
    fontWeight: 500
    lineHeight: 1.30
    letterSpacing: 0
  headline-md:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 32px
    fontWeight: 500
    lineHeight: 1.10
    letterSpacing: 0
  headline-sm:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 25px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0
  feature-title:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 21px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0
  body-serif:
    fontFamily: "Anthropic Serif, Georgia, serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-lg:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-md:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-sm:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  caption:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: 0
  label:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: 0.12px
  overline:
    fontFamily: "Anthropic Sans, Inter, system-ui, sans-serif"
    fontSize: 10px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0.5px
    textTransform: uppercase
  code:
    fontFamily: "Anthropic Mono, SFMono-Regular, Consolas, monospace"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: -0.32px
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  2xl: 24px
  3xl: 32px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 80px
  5xl: 120px
  section: 96px
  pad-button: 12px
shadows:
  ring-warm: "0 0 0 1px #D1CFC5"
  ring-deep: "0 0 0 1px #C2C0B6"
  whisper: "0 4px 24px rgba(0, 0, 0, 0.05)"
  ring-soft: "0 0 0 1px rgba(201, 197, 184, 0.7)"
  soft: "0 18px 60px rgba(20, 20, 19, 0.08)"
components:
  button-primary:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.pad-button}"
    shadow: "{shadows.ring-warm}"
  button-primary-hover:
    backgroundColor: "{colors.brand-soft}"
  button-secondary:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.pad-button}"
    shadow: "{shadows.ring-warm}"
  button-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.pad-button}"
    shadow: "{shadows.ring-deep}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
    shadow: "{shadows.whisper}"
    border: "1px solid {colors.border-soft}"
  card-featured:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.2xl}"
    shadow: "{shadows.whisper}"
    border: "1px solid {colors.border-warm}"
  hero-container:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.3xl}"
    padding: "{spacing.4xl}"
  dark-section:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.section}"
    border: "1px solid {colors.border-dark}"
  caption-label:
    backgroundColor: "transparent"
    textColor: "{colors.tertiary}"
    typography: "{typography.overline}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
    border: "1px solid {colors.border-warm}"
---

## Overview

Warm Editorial is a literary-salon system for AI products, thoughtful tools, and technical writing surfaces. The page reads like a well-paced essay rather than a product sheet — parchment canvas, serif headlines at a single medium weight, generous body line-height, and a single chromatic brand moment in terracotta. Where most technical sites lean cold and futuristic, this one radiates human warmth without sacrificing rigour.

The signature move is the chromatic discipline: every neutral has a yellow-brown undertone. There are no cool blue-grays anywhere. Borders are cream-tinted, shadows are warm transparent blacks, and even the darkest dark surfaces carry a barely perceptible olive warmth. Combined with serif/sans pairing and ring-based depth, this produces a "thoughtful companion" mood rather than "powerful tool."

## Colors

Exclusively warm-toned. The palette is gradient-free; depth comes from light/dark section alternation and warm ring shadows.

- **Primary (#141413):** Anthropic Near Black — primary text on light surfaces, page background on dark sections. Warm, almost olive-tinted.
- **Secondary (#5E5D59):** Olive Gray — secondary body text and quieter copy.
- **Tertiary (#87867F):** Stone Gray — tertiary text, footnotes, metadata.
- **Neutral (#F5F4ED):** Parchment — primary page background. The emotional foundation; the warm cream IS the personality.
- **Surface (#FAF9F5):** Ivory — cards and elevated containers on Parchment. Subtle layering.
- **Surface-alt (#E8E6DC):** Warm Sand — secondary button backgrounds and prominent interactive surfaces.
- **Surface-dark (#30302E):** Dark Surface — dark-theme containers and elevated dark elements; warm charcoal.
- **Brand (#C96442):** Terracotta — the only chromatic colour. Reserved for primary CTAs and the highest-signal brand moments.
- **Brand-soft (#D97757):** Coral — lighter variant for hover states, links on dark surfaces, secondary emphasis.
- **Border-soft (#F0EEE6):** Standard light border — barely visible warm cream.
- **Border-warm (#E8E6DC):** Prominent borders, section dividers.
- **Ring-warm (#D1CFC5) / Ring-deep (#C2C0B6):** Ring-shadow colours for interactive states.
- **Focus (#3898EC):** The only cool colour in the entire system; reserved for input focus rings purely for accessibility.

## Typography

Anthropic Serif (Georgia fallback) at weight 500 carries every headline — no bold, no light, no italic. The single-weight discipline is intentional: it produces a consistent "voice" across all heading sizes, as if one author wrote everything. Anthropic Sans (Inter fallback) handles UI, body, and labels with quiet efficiency. Anthropic Mono (system mono fallback) is reserved strictly for code.

Body line-height is generous (1.60) — significantly more than typical product sites. This produces an essay-reading cadence, not a dashboard-scanning one. Headlines run tight (1.10–1.30) but never claustrophobic; serif letterforms need breathing room sans-serifs don't. Tiny labels (≤12px) carry deliberate letter-spacing (0.12px–0.5px) to remain readable.

## Layout

Magazine-like pacing. Sections breathe at 96–120px vertical spacing on desktop, alternating between light Parchment environments and Near Black dark sections like chapters in a book. Container caps at ~1200–1360px. Hero moments use editorial layouts (asymmetric or centred-with-discipline) rather than poster aggression. Multi-column grids appear for model/feature comparison; otherwise single-column reading rhythm dominates.

## Shapes

Comfortably to generously rounded. 8px on standard buttons and cards, 12px on primary buttons and inputs, 16px on featured containers, 32px on hero containers and embedded media. Sharp corners are wrong — softness is core to the identity. The radius scale itself is one of the divergence axes: tightening to 8/12 vs default 12/16 is a legitimate brand-tightening move.

## Depth

Depth comes from **warm-toned ring shadows**, not drop shadows. The signature `0 0 0 1px` ring pattern using `#D1CFC5` or `#C2C0B6` creates a border-like halo that's softer than an actual border — a shadow pretending to be a border. When drop shadows do appear, they're whisper-soft (`rgba(0,0,0,0.05) 0 4px 24px`) — barely visible lifts that suggest floating rather than casting. The most dramatic depth effect is light/dark section alternation (Parchment ↔ Near Black), which shifts the entire ambient light level.

## Components

Component tokens are defined in YAML frontmatter. Key patterns:

- **`button-primary`** — Terracotta on Ivory text, 8–12px radius, ring-warm shadow. The only chromatic button; reserved for primary CTAs.
- **`button-secondary`** — Warm Sand on Charcoal text, 8px radius, ring-warm shadow. Workhorse button — warm, unassuming, clearly interactive.
- **`button-dark`** — Dark Surface on Ivory text, 8px radius, ring-deep shadow. Inverted variant for dark-on-light emphasis.
- **`card`** — Ivory on Parchment, 12px radius, whisper shadow + soft border. Standard content card.
- **`card-featured`** — Larger 16px radius, whisper shadow, warm border. Used for model comparison and feature highlights.
- **`hero-container`** — 32px radius on Parchment. Carries display typography and hero illustrations.
- **`dark-section`** — Near Black full-bleed environment with Ivory text and Warm Silver body. The chapter-break moment.
- **`input`** — Surface bg, 12px radius, warm border. Focus state uses Focus blue ring (the only cool moment).

The dark/light alternation is a layout primitive, not a component — sections opt into the dark environment by wrapping in `dark-section`.

## Do's and Don'ts

- Do use Parchment (#F5F4ED) as the primary light background — the warm cream IS the personality
- Do use serif at weight 500 for every headline — single-weight is intentional
- Do reserve Terracotta (#C96442) for primary CTAs and brand moments only
- Do keep all neutrals warm-toned — every grey has a yellow-brown undertone
- Do use ring shadows (0 0 0 1px) for interactive states instead of drop shadows
- Do alternate between light and dark sections to create chapter rhythm
- Do use generous body line-height (1.60) for essay-reading cadence
- Don't use cool blue-greys anywhere — the palette is exclusively warm
- Don't use bold (700+) on serif headlines — 500 is the ceiling
- Don't introduce saturated colours beyond Terracotta
- Don't use sharp corners (<6px radius) — softness is core to the identity
- Don't apply heavy drop shadows — depth comes from rings and section contrast
- Don't use pure white as a page background — Parchment or Ivory always
- Don't reduce body line-height below 1.40 — kills the literary cadence
- Don't mix sans-serif into headlines — the serif/sans split is the typographic identity
