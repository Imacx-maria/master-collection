---
version: alpha
name: Editorial Portfolio
description: Warm, image-led, gallery-adjacent editorial system for portfolios, showcases, and cultural presentation surfaces.
colors:
  primary: "#1D1F1E"
  secondary: "#444745"
  tertiary: "#DBD5C9"
  neutral: "#F4F3F0"
  surface: "#F1EDE1"
  surface-dark: "#161616"
  on-primary: "#F4F3F0"
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 128px
    fontWeight: 400
    lineHeight: 0.9
    letterSpacing: -0.03em
  display-lg:
    fontFamily: Inter
    fontSize: 88px
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: -0.06em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 300
    lineHeight: 1.5
    letterSpacing: -0.02em
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.08em
rounded:
  sm: 0px
  md: 0px
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
  pad-button: 12px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  panel-overlay:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    padding: "{spacing.lg}"
  caption-strip:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-caps}"
    padding: "{spacing.pad-button}"
  footer-band:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.lg}"
---

## Overview

Editorial Portfolio is work-first. The interface should feel composed, calm, image-aware — like a gallery wall, fashion spread, or contemporary portfolio, not a generic product site. Contrast, proportion, and whitespace do the heavy lifting.

## Colors

Warm and restrained, anchored by deep ink text on a warm off-white field (#F4F3F0).

- **Primary (#1D1F1E):** Main text and structural anchors
- **Secondary (#444745):** Supporting text and quieter dividers
- **Tertiary (#DBD5C9):** Hover states, soft panel accents
- **Neutral (#F4F3F0):** White-smoke foundational background
- **Surface (#F1EDE1):** Cream accent surface, services sections
- **Surface-dark (#161616):** Footer, full-bleed dark blocks

## Typography

Inter at display sizes, weighted light (300–400), letter-spacing tightened hard (-0.03em to -0.06em). Compressed, uppercase-leaning, editorial. All type contributes to composition — no decorative flourishes.

## Layout

Generous whitespace, large directional type, asymmetry that still feels deliberate. Hero moments overlap imagery. Work listings use hover-reveal panels, image-and-caption pairings, and full-bleed moments.

## Shapes

Mostly sharp. Rectangles, lines, and image frames stay crisp. Zero-radius is the default.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text with sharp 4px radius and uppercase label-caps. Compact and restrained.
- **`panel-overlay`** — Off-white neutral panel that reveals on hover over imagery. Carries captions, project titles, metadata.
- **`caption-strip`** — Tertiary background with secondary text in label-caps. Used as image annotations and section dividers.
- **`footer-band`** — Dark surface band with inverted text. Closes the page with quiet weight.

Overlays and reveals are the interaction language. Cards and panels stay rectilinear. The image library does the heavy lifting; components stay deferential.

## Do's and Don'ts

- Do let imagery and proportion carry the drama
- Do use large type with discipline
- Do keep UI chrome minimal
- Don't over-round elements
- Don't turn the page into a component library showcase
- Don't use bright accent colors that break the editorial restraint
