---
version: alpha
name: Spritify
description: Playful, switchable-color-scheme aesthetic for kids products, family brands, and fun apps. League Spartan type, saturated palette, rounded component shapes.
colors:
  primary: "#03594D"
  secondary: "#555555"
  tertiary: "#82EDA6"
  accent-pink: "#F6BBFD"
  accent-yellow: "#FFFF94"
  accent-cyan: "#AEFBFF"
  neutral: "#F9F8F4"
  surface: "#FFFFFF"
  on-primary: "#F9F8F4"
typography:
  display-xl:
    fontFamily: League Spartan
    fontSize: 112px
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: -0.03em
  display-lg:
    fontFamily: League Spartan
    fontSize: 88px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: League Spartan
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: -0.02em
  body-md:
    fontFamily: League Spartan
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: League Spartan
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 16px
  md: 24px
  lg: 40px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 40px
  3xl: 56px
  4xl: 72px
  5xl: 112px
  section: 72px
  pad-card: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.primary}"
  button-accent:
    backgroundColor: "{colors.accent-pink}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.md}"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.pad-card}"
  accent-border-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
---

## Overview

Spritify is playful without being childish. Switchable color schemes let the same component system feel energetic (green + yellow), soft (pink + off-white), or bold (green + dark + off-white) depending on context. Suits kids products, family brands, educational tools, fun consumer apps.

## Colors

Three predefined schemes — each swaps `primary / secondary / tertiary` at the `:root` level while keeping component structure identical.

- **Primary (#03594D):** Deep forest green — default scheme main text
- **Tertiary (#82EDA6):** Light green — default scheme secondary surface
- **Accent-pink (#F6BBFD):** Pink accent — secondary scheme primary
- **Accent-yellow (#FFFF94):** Playful yellow — default scheme accent
- **Accent-cyan (#AEFBFF):** Cyan — variety option
- **Neutral (#F9F8F4):** Off-white — gentle background across all schemes
- **Surface (#FFFFFF):** White cards

### Scheme 1 — Default, energetic
`bg: #82EDA6 / accent: #FFFF94 / text: #03594D`

### Scheme 2 — Soft, friendly
`bg: #F6BBFD / accent: #F9F8F4 / text: #03594D`

### Scheme 3 — Bold, contrast
`bg: #82EDA6 / accent: #03594D / text: #F9F8F4`

## Typography

League Spartan throughout. Heavy weights (700–800) for display. Playful size scaling — heroes at 96–112px. Body stays comfortable at 17px.

## Layout

Generous spacing, lots of air, oversized components. Buttons feel chunky (16px padding, full pill). Cards have accent-color left borders (6px) for tactile feel.

## Shapes

Very rounded. 16px minimum card radius, 40px for large feature cards, full-pill buttons. Sharp corners break the Spritify feel.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, full pill radius, label-md typography. The default friendly action.
- **`button-accent`** — Saturated pink accent (`{colors.accent-pink}`) on primary text, full pill radius. Highlights playful or rewarding actions (subscribe, play, claim).
- **`card-default`** — Surface card with large radius (16px+) and 32px padding. Soft, approachable, never sharp.
- **`accent-border-card`** — Surface card with medium radius and 24px padding, intended to carry coloured borders or accents. For category tiles, feature highlights, kid-facing content blocks.

Components must read as friendly and tactile. All radii are generous; all interactions invite touch. Hover states should bounce slightly (overshoot easing), never just fade. Switchable colour schemes mean components must work across multiple palettes — design for the system, not a single palette.

## Do's and Don'ts

- Do use saturated colors together — fear of color is the wrong instinct here
- Do let components feel chunky and tactile — oversized padding, thick borders
- Do switch schemes across pages or sections for variety
- Don't use thin type weights — League Spartan shines at 700+
- Don't use sharp corners — rounds are non-negotiable
- Don't mix more than 2 schemes in a single view
