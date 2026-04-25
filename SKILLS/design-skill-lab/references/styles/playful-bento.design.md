---
version: alpha
name: Playful Bento
description: Energetic marketing and product aesthetic built around bento grids, hierarchy-aware cards, and vibrant but disciplined color usage.
colors:
  primary: "#0F0F0F"
  secondary: "#525252"
  tertiary: "#F59E0B"
  accent-alt: "#8B5CF6"
  neutral: "#FAFAFA"
  surface: "#FFFFFF"
  surface-tint-1: "#FEF3C7"
  surface-tint-2: "#DBEAFE"
  surface-tint-3: "#D1FAE5"
  surface-tint-4: "#FCE7F3"
  on-primary: "#FAFAFA"
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 128px
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: -0.05em
  display-lg:
    fontFamily: Inter
    fontSize: 96px
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: -0.04em
  headline-xl:
    fontFamily: Inter
    fontSize: 80px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.02em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 12px
  md: 20px
  lg: 32px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 40px
  3xl: 64px
  4xl: 96px
  5xl: 128px
  section: 64px
  gutter: 16px
  pad-button: 14px
  pad-cell-sm: 20px
  pad-cell-accent: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  bento-cell-large:
    backgroundColor: "{colors.surface-tint-1}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
  bento-cell-medium:
    backgroundColor: "{colors.surface-tint-2}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  bento-cell-small:
    backgroundColor: "{colors.surface-tint-3}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.pad-cell-sm}"
  bento-cell-accent:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.pad-cell-accent}"
---

## Overview

Playful Bento is energetic without being chaotic. The bento grid gives visual rhythm and hierarchy — one large feature cell surrounded by medium and small supporting cells, each with its own tint. Suits marketing sites, creative tools, energetic brands for adult audiences.

## Colors

Muted tints (not saturated brights) for bento cells — they sit next to each other without fighting. The tertiary amber and violet accent-alt appear sparingly on statement cells or CTAs.

- **Primary (#0F0F0F):** All text, high-contrast
- **Secondary (#525252):** Metadata, muted labels
- **Tertiary (#F59E0B):** Amber accent for statement cells
- **Accent-alt (#8B5CF6):** Violet — for variety when amber is overused
- **Neutral (#FAFAFA):** Page background
- **Surface (#FFFFFF):** Plain cells
- **Surface-tint-1..4:** Cream / blue / mint / pink tinted cell backgrounds

## Typography

Inter 800 for display drama. Inter 400 for body. Tight letter-spacing on headlines (-0.04em) for the compressed, assertive feel bento grids need.

## Layout

Bento grid is the main structural device. Cells at different sizes — one hero cell (2x2 or 2x1), several medium cells, small cells for metadata or tags. Generous radii (20–32px) soften the grid.

## Shapes

Generously rounded. 20px is the default cell radius, 32px for hero cells. Buttons full-pill.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, full pill radius, label-md typography. Energetic but disciplined — never multi-coloured.
- **`bento-cell-large`** — Surface tint 1 (lightest) with large radius (20px) and 40px padding. Hero of the bento grid — one per layout.
- **`bento-cell-medium`** — Surface tint 2 with medium radius and 24px padding. The workhorse cell — multiple per layout.
- **`bento-cell-small`** — Surface tint 3 (deepest) with medium radius and 20px padding. Compact metric or stat cells.
- **`bento-cell-accent`** — Tertiary saturated colour with large radius and 32px padding. The single attention-grabbing moment per grid.

Bento cells form interlocking grids of varying sizes. Tonal hierarchy (tint-1 → tint-2 → tint-3) creates visual rhythm without saturation overload. The accent cell carries all the colour weight.

## Do's and Don'ts

- Do use tints, not saturated brights — cells must coexist
- Do vary cell sizes for hierarchy — never a uniform grid
- Do use one strong accent cell per grid, not every cell
- Don't use more than 4 surface tints — gets cluttered
- Don't use sharp corners — bento is inherently soft
- Don't make every cell the same size — that's just a grid, not bento
