---
version: alpha
name: Basalt E-Commerce
description: Luxury grayscale e-commerce system for beauty, skincare, fashion, and lifestyle shops. Serif display + neutral sans, floating product imagery, split-layout pages.
colors:
  primary: "#000000"
  secondary: "#1E1E1F"
  tertiary: "#BFBFBF"
  neutral: "#F5F5F5"
  surface: "#FFFFFF"
  surface-alt: "#E4E4E4"
  on-primary: "#FFFFFF"
typography:
  display-xl:
    fontFamily: EB Garamond
    fontSize: 120px
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: -0.02em
  display-lg:
    fontFamily: EB Garamond
    fontSize: 88px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: -0.02em
  display-italic:
    fontFamily: EB Garamond
    fontSize: 120px
    fontWeight: 400
    fontStyle: italic
    lineHeight: 0.95
  headline-lg:
    fontFamily: EB Garamond
    fontSize: 56px
    fontWeight: 400
    lineHeight: 1.05
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.55
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.12em
rounded:
  sm: 0px
  md: 4px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 96px
  5xl: 128px
  section: 96px
  pad-card: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  product-card:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.pad-card}"
  price-label:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
    padding: "{spacing.sm}"
---

## Overview

Basalt E-Commerce is pared-back luxury. The interface should feel editorial and considered — products as objects to contemplate, not items to cart-and-go. Grayscale palette forces the product photography to carry the color story.

## Colors

Pure grayscale, no accents. Black (#000) for primary text, deep charcoal (#1E1E1F) for secondary, light gray (#E4E4E4) as the product-card surface where items float with soft shadows.

- **Primary (#000000):** Headlines, body, primary text
- **Secondary (#1E1E1F):** Deep charcoal for dividers and secondary UI
- **Tertiary (#BFBFBF):** Muted gray for metadata
- **Neutral (#F5F5F5):** Off-white page background
- **Surface (#FFFFFF):** Pure white cards, modals
- **Surface-alt (#E4E4E4):** Gray product-card background — the floating-product treatment

## Typography

EB Garamond Regular for all display (never bold). Italic accent on first word of headlines for editorial drama. Inter for body and UI chrome. Strong contrast between serif drama and sans utility.

## Layout

Split-layout pages (50/50 content + image), floating product photography on gray cards, generous vertical rhythm. Section padding at 96px+ for luxury breathing room.

## Shapes

Sharp corners dominate. Product cards can have minimal 4px radius. No pill buttons, no rounded cards.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid primary on inverted text, sharp 4px radius, uppercase label-caps typography. Restraint over flourish — never pill-shaped.
- **`product-card`** — Off-white surface (`{colors.surface-alt}`) with sharp corners and generous 32px padding. Lets product photography breathe.
- **`price-label`** — Pure surface with primary text in label-caps. Compact, utilitarian, never decorative.

All components stay crisp and rectilinear. Shadows are absent or whisper-soft. Hierarchy comes from spacing and typography, not depth.

## Do's and Don'ts

- Do use EB Garamond Regular only — never bold, italic for accent only
- Do float product imagery on gray cards with soft shadows
- Do split layouts 50/50 with strong asymmetry within each half
- Don't introduce any accent color
- Don't round buttons or cards heavily
- Don't use sans-serif for headlines — the serif is the point
