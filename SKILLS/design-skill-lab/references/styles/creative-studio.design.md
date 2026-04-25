---
version: alpha
name: Creative Studio
description: Dark, gallery-like aesthetic for creative agencies and design studios. Charcoal foundation with warm coral accent for CTAs and process bands.
colors:
  primary: "#171717"
  secondary: "#434645"
  tertiary: "#FF531F"
  tertiary-light-1: "#FFF0EB"
  tertiary-light-2: "#FFC8B8"
  tertiary-mid: "#FF9D80"
  neutral: "#F5F5F5"
  surface: "#FFFFFF"
  surface-dark: "#2D2F2E"
  on-primary: "#FFFFFF"
  muted-dark: "#767F7A"
  muted-light: "#AFB6B4"
  border: "#DDDFDE"
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 144px
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: -0.04em
  display-lg:
    fontFamily: Inter
    fontSize: 112px
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: -0.035em
  headline-xl:
    fontFamily: Inter
    fontSize: 96px
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0.08em
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 80px
  5xl: 128px
  section: 80px
  pad-button: 14px
  pad-band: 48px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.tertiary-mid}"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  hero-band:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.section}"
  process-band-1:
    backgroundColor: "{colors.tertiary-light-1}"
    textColor: "{colors.primary}"
    padding: "{spacing.pad-band}"
  process-band-2:
    backgroundColor: "{colors.tertiary-light-2}"
    textColor: "{colors.primary}"
    padding: "{spacing.pad-band}"
  process-band-3:
    backgroundColor: "{colors.tertiary-mid}"
    textColor: "{colors.primary}"
    padding: "{spacing.pad-band}"
  process-band-4:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.pad-band}"
---

## Overview

Creative Studio is premium agency aesthetic — dark, gallery-like backgrounds that make portfolio work pop, warmed by coral accents. Suits design studios, branding agencies, creative services.

## Colors

Dark charcoal foundation (#2D2F2E) for hero, services, stats — creates the gallery feel. Light content areas (#F5F5F5) let imagery dominate. Coral gradient scale (#FFF0EB → #FFC8B8 → #FF9D80 → #FF531F) powers process bands and accent moments.

- **Primary (#171717):** Primary text on light
- **Secondary (#434645):** Watermark text, subtle dark-bg elements
- **Tertiary (#FF531F):** Coral accent — CTAs, final process band
- **Neutral (#F5F5F5):** Main content background
- **Surface-dark (#2D2F2E):** Hero, services, stats backgrounds
- **Muted-dark (#767F7A):** Muted text on dark backgrounds
- **Muted-light (#AFB6B4):** Secondary text, labels on light
- **Border (#DDDFDE):** Dividers, card outlines

## Typography

Inter throughout, weighted bold (700) for headlines. Aggressive scaling — hero at 96px on desktop. Labels uppercase with generous tracking.

## Layout

Dark hero, light content bands, coral-gradient process sections. Full-color imagery is the point — no desaturation, no monochrome treatments. Cards rounded generously (16px) for warmth against the dark frame.

## Shapes

Generously rounded. Cards at 16px, buttons full-pill. Dark sections can use 24px for statement blocks.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Coral accent (`{colors.tertiary}`) on inverted text, full pill radius, uppercase label-caps typography. The single saturated moment per band.
- **`card-default`** — Dark surface card with medium radius (16px) and 24px padding. Houses agency case studies and team bios.
- **`hero-band`** — Full-bleed dark surface with 80px vertical padding. Statement opener — one per page.
- **`process-band-1` through `process-band-4`** — Tonal progression of coral accent (light → mid → vivid) for sequential process steps. 48px padding across the band. Demonstrates narrative through color shift.

Bands and cards are the structural language. Borders are subtle; depth comes from color shifts and generous padding, not shadows.

## Do's and Don'ts

- Do use the coral gradient scale for process/timeline sections
- Do alternate dark and light bands for visual rhythm
- Do show portfolio work in full color, large, unapologetic
- Don't desaturate or tint portfolio imagery
- Don't let coral dominate — it's an accent, not a surface
- Don't use sharp corners — warmth comes from curves
