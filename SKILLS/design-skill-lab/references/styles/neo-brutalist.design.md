---
version: alpha
name: Neo-Brutalist
description: Hard-edged, high-contrast, grid-driven system for bold landing pages, edgy brands, and poster-like tech showcases.
colors:
  primary: "#181818"
  secondary: "#888888"
  tertiary: "#DDDDDD"
  neutral: "#EAEAEA"
  surface: "#FFFFFF"
  surface-dark: "#2A2A2A"
  on-primary: "#DDDDDD"
typography:
  display-xl:
    fontFamily: Anton
    fontSize: 160px
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: -0.02em
  display-lg:
    fontFamily: Anton
    fontSize: 120px
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Anton
    fontSize: 64px
    fontWeight: 400
    lineHeight: 0.98
  body-md:
    fontFamily: Roboto Mono
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0.08em
  label-md:
    fontFamily: Roboto Mono
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.2em
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
  4xl: 96px
  5xl: 160px
  grid: 60px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.on-primary}"
    textColor: "{colors.primary}"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
  meta-chip:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
---

## Overview

Neo-Brutalist is unapologetic, graphic, and structural. The interface should read as a designed object with visible grids, hard edges, and obvious decisions — not a polished corporate kit. Dark mode flips primary/neutral; light mode stays paper-like.

## Colors

Mostly monochrome, with grayscale depth. Use dark surfaces for hero/statement blocks and light surfaces for content breathing room.

- **Primary (#181818):** Dominant text, borders, graphic weight
- **Secondary (#888888):** Quiet utility tone, grid support, inactive metadata
- **Tertiary (#DDDDDD):** Dark-mode primary text
- **Neutral (#EAEAEA):** Paper-like page background in light mode
- **Surface (#FFFFFF):** Card fields in light mode
- **Surface-dark (#2A2A2A):** Card fields in dark mode

No bright accents. If the brief needs a punch, a sparing orange/red hit (#FF5C39-ish) works — but never as dominant color.

## Typography

Display is Anton-style — compressed, dramatic, uppercase-leaning. Body and labels are mono (Roboto Mono), with wide tracking for system feel.

## Layout

Grids visible, alignments hard, spacing disciplined. Headlines sized at 6xl–8xl. Hover states use translate + hard shadow offsets (8px 8px 0 var(--color-primary)) to simulate physical displacement.

## Shapes

Zero radius everywhere. Square corners, square buttons, square cards.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, zero radius, mono label-md typography. Brutally rectangular — never softened.
- **`card-default`** — Hard-bordered surface card with zero radius and 24px padding. Stack on the grid background like construction blocks.
- **`meta-chip`** — Inverted primary background with secondary text in mono label-md, zero radius. Tags, status markers, version numbers — never decorative.

All components stay aggressively rectangular. Borders are visible and structural. Hover states invert (background ↔ text), they don't soften. Grid backgrounds stay visible behind components — depth is structural, not atmospheric.

## Do's and Don'ts

- Do keep shapes sharp and corners at 0
- Do let the grid show when it strengthens composition
- Do keep interactions mechanical — translate offsets, hard shadows, instant state changes
- Don't soften the interface with rounded UI or gradients
- Don't add more than one accent color
- Don't let hover animations become "smooth" or "elegant"
