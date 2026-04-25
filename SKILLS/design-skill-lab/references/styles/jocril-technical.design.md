---
version: alpha
name: Jocril Technical
description: Refined, technical, modern interface language for developer tools, SaaS dashboards, and documentation-heavy product surfaces.
colors:
  primary: "#0A0A0A"
  secondary: "#555555"
  tertiary: "#2DD4CD"
  tertiary-deep: "#16B7B2"
  tertiary-vivid: "#00DED7"
  neutral: "#FAFAFA"
  surface: "#141414"
  surface-elevated: "#1F1F1F"
  on-primary: "#FAFAFA"
typography:
  display-xl:
    fontFamily: Geist Sans
    fontSize: 160px
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: -0.03em
  display-lg:
    fontFamily: Geist Sans
    fontSize: 112px
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: -0.025em
  headline-xl:
    fontFamily: Geist Sans
    fontSize: 96px
    fontWeight: 650
    lineHeight: 1.04
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Geist Sans
    fontSize: 70px
    fontWeight: 650
    lineHeight: 1.05
    letterSpacing: -0.02em
  body-md:
    fontFamily: Geist Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  label-md:
    fontFamily: Geist Mono
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: -0.0175em
rounded:
  sm: 8px
  md: 14px
  lg: 20px
  full: 9999px
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
  section: 48px
  gutter: 24px
  pad-button: 12px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.tertiary-deep}"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  badge-muted:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.sm}"
  page-shell:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
---

## Overview

Jocril Technical is a restrained, high-clarity system for serious digital products. It should feel precise, contemporary, quietly confident — not flashy. The interface should suggest competent engineering, strong information architecture, deliberate craft.

## Colors

Mostly neutral, with one vivid teal accent used surgically. Three teal variants give depth (#2DD4CD primary, #16B7B2 deep/hover, #00DED7 vivid for highlights).

- **Primary (#0A0A0A):** Dominant text and deepest grounding tone
- **Secondary (#555555):** Supporting metadata and quiet contrast
- **Tertiary (#2DD4CD):** Reserved teal accent for CTAs, active states, focus
- **Tertiary-deep (#16B7B2):** Hover state for teal elements
- **Tertiary-vivid (#00DED7):** Occasional highlight for maximum emphasis
- **Neutral (#FAFAFA):** High-clarity foreground on dark, bright foundation for light
- **Surface (#141414):** Primary dark card and panel surface

Do not let accent become the whole interface.

## Typography

Geist Sans for core hierarchy, Geist Mono for metadata, labels, system cues. Headings feel crisp and engineered. Aggressive size scaling — heroes at 70–160px, not timid 1.5x jumps. Mono labels uppercase with tight tracking (-0.0175rem).

## Layout

Strong structural spacing, disciplined containment. Generous margins, measured max widths, clear section boundaries. Dashed borders and dot accents as support motifs, not the main event.

## Elevation & Depth

Depth from tonal layers, subtle panel separation, occasional soft glow around accent states. No fluffy shadows or decorative blur stacks.

## Shapes

Rounded but controlled — medium radii for cards (14px), full radii only for pills and compact buttons.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Teal accent (`{colors.tertiary}`) on dark text, full pill radius, mono label typography. Reserved for primary CTAs only — one per screen.
- **`card-default`** — Dark surface (`{colors.surface}`) panel with medium radius (14px) and 24px padding. Stack on neutral background for tonal layering.
- **`badge-muted`** — Elevated surface tint with mono label typography, full pill radius. Use for metadata tags, status pills, version markers.
- **`page-shell`** — Bright neutral foundation (`{colors.neutral}`) with secondary text color and large radius. Wraps content sections.

All interactive components must define hover/focus states using the teal accent palette. Card and button components stay calm by default — depth comes from tonal layering, not shadows.

## Do's and Don'ts

- Do keep accents sparse and meaningful
- Do use mono for metadata, labels, system cues
- Do keep layouts calm and information-dense without cramping
- Don't turn every border, heading, and icon into an accent element
- Don't use generic glassmorphism or purple gradients
- Don't scale headings timidly — jumps should be dramatic
