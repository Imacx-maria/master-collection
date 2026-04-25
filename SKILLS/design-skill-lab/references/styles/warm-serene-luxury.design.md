---
version: alpha
name: Warm Serene Luxury
description: Hospitality and wellness aesthetic driven by photography, not accent colors. Minimal near-white palette lets imagery become the color story.
colors:
  primary: "#1A1A1A"
  secondary: "rgba(26, 26, 26, 0.75)"
  tertiary: "rgba(26, 26, 26, 0.40)"
  neutral: "#FAFAFA"
  surface: "rgba(250, 250, 250, 0.75)"
  surface-muted: "rgba(250, 250, 250, 0.10)"
  on-primary: "#FAFAFA"
  border-soft: "rgba(26, 26, 26, 0.10)"
  hover-state: "rgba(26, 26, 26, 0.05)"
typography:
  display-xl:
    fontFamily: DM Serif Display
    fontSize: 144px
    fontWeight: 400
    lineHeight: 0.96
    letterSpacing: -0.02em
  display-lg:
    fontFamily: DM Serif Display
    fontSize: 104px
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: DM Serif Display
    fontSize: 56px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -0.01em
  body-md:
    fontFamily: Onest
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-number:
    fontFamily: Onest
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.14em
rounded:
  sm: 0px
  md: 4px
  lg: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 96px
  5xl: 144px
  section: 96px
  pad-card: 32px
  zero: 0
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-number}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  card-default:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.pad-card}"
  numbered-item:
    backgroundColor: "transparent"
    textColor: "{colors.secondary}"
    typography: "{typography.label-number}"
    padding: "{spacing.zero}"
---

## Overview

Warm Serene Luxury is photography-driven restraint. The palette is intentionally minimal (#FAFAFA near-white + #1A1A1A near-black) so imagery becomes the color story. Suits boutique hotels, wellness, spas, interior design.

## Colors

No accent colors by design — warmth comes from imagery and imperfectly-white neutral. All secondary tones are rgba variants of the primary #1A1A1A for tonal depth.

- **Primary (#1A1A1A):** All headlines and body text
- **Secondary (rgba(26,26,26,0.75)):** Secondary text, subtitles
- **Tertiary (rgba(26,26,26,0.40)):** Placeholders, labels
- **Neutral (#FAFAFA):** Primary background — the only background color
- **Border-soft (rgba(26,26,26,0.10)):** Hairline dividers
- **Hover-state (rgba(26,26,26,0.05)):** Subtle hover backgrounds

## Typography

DM Serif Display for all headlines — dramatic, elegant, architectural. Onest for body and UI. Numbered items (01, 02, 03) with wide-tracked uppercase labels are a signature pattern.

## Layout

Photography-dominant. Generous section padding (96px+). Numbered sections establish rhythm. Room preview cards, property highlights, and imagery pairings carry the composition.

## Shapes

Mostly sharp. Subtle 4–8px radius on cards, zero on buttons.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, sharp small radius, label-number typography. Quiet confidence — never demands attention from the photography.
- **`card-default`** — Warm neutral surface with medium radius (8px) and 32px padding. Frames imagery and editorial copy without competing.
- **`numbered-item`** — Transparent background with secondary text in the distinctive label-number typography (e.g., "01", "02"). Used as section markers and editorial sequencing.

Photography is the primary visual element; components stay deferential. Hover states use subtle tonal warmth shifts. Numbered items carry the editorial rhythm — count sequences, not just lists. Generous internal padding throughout reinforces the hospitality feel.

## Do's and Don'ts

- Do let photography carry all the color
- Do use numbered items (01, 02, 03) with wide-tracked labels
- Do keep the palette to #FAFAFA + #1A1A1A + rgba variants only
- Don't introduce accent colors — ever
- Don't round elements aggressively — the elegance is in the restraint
- Don't compress vertical rhythm — luxury needs space
