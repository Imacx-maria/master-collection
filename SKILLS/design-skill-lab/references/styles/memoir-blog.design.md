---
version: alpha
name: Memoir Blog
description: Reading-first blog and newsletter system with creamy neutrals, Manrope + Source Serif 4 italic pairing, and tidy blog card grids.
colors:
  primary: "#000000"
  secondary: "#755F59"
  tertiary: "#EDEAE7"
  neutral: "#F4F2F0"
  surface: "#FFFFFF"
  on-primary: "#FFFFFF"
  muted: "rgba(0, 0, 0, 0.48)"
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 96px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: -0.06em
  headline-xl:
    fontFamily: Manrope
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.06em
  headline-md:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.03em
  accent-italic:
    fontFamily: Source Serif 4
    fontSize: 18px
    fontWeight: 400
    fontStyle: italic
    lineHeight: 1.5
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.65
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0.06em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
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
  section: 48px
  pad-button: 12px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  blog-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  filter-pill-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: "{spacing.sm}"
  filter-pill-inactive:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: "{spacing.sm}"
---

## Overview

Memoir is a reading-first blog and newsletter system. It should feel welcoming, structured, literate — built for browsing, reading, returning. Creamy foundation with white article cards for reading surfaces.

## Colors

Creamy and warm, white where reading happens.

- **Primary (#000000):** Main text, strong contrast anchors
- **Secondary (#755F59):** Warmer supporting text, muted browns
- **Tertiary (#EDEAE7):** Inactive pills, soft section changes, cream accents
- **Neutral (#F4F2F0):** Main page foundation — creamy canvas
- **Surface (#FFFFFF):** Blog cards, article reading surfaces
- **Muted (rgba(0,0,0,0.48)):** Inactive sidebar text

## Typography

Manrope for all core UI and headlines. Source Serif 4 italic for emphasis words and editorial accents — this italic-serif-inside-sans pattern is the signature move. Body at 16px/1.65 for comfortable reading.

## Layout

Blog card grids for archives, sidebar navigation with muted inactive states, tag filter pills (active white / inactive cream). Long-form pages breathe; listing and post views must feel like one system.

## Shapes

Modest rounding. Cards 8px, pills fully rounded, sharp corners only where appropriate.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, full pill radius, label-sm typography. Reading-friendly and unobtrusive.
- **`blog-card`** — Cream surface with 8px radius and 24px padding. Stacked vertically in reading-first card grids.
- **`filter-pill-active`** — Surface tint with primary text in label-sm, full pill. Marks the currently-selected category filter.
- **`filter-pill-inactive`** — Tertiary tint with secondary text. Unselected filter siblings.

Pills cluster horizontally above content lists. Cards stack with generous gaps for reading rhythm. The serif italic accent (in typography) is the only "decoration" — components themselves stay quiet.

## Do's and Don'ts

- Do use italic serif for emphasis inside Manrope body
- Do keep blog cards tidy — 24px padding, 8px radius, soft depth
- Do use warm secondary browns (#755F59) for metadata
- Don't let decorative accents crowd the content
- Don't make listing and post views feel unrelated
- Don't sacrifice line length or contrast for atmosphere
