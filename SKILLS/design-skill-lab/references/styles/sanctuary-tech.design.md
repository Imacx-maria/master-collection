---
version: alpha
name: Sanctuary Tech
description: Trauma-informed, low-stress aesthetic for crisis support, healthcare, legal aid, and privacy tools. Monospace type, dashed borders, muted tones, generous whitespace.
colors:
  primary: "#171717"
  secondary: "#525252"
  tertiary: "#16A34A"
  tertiary-dark: "#15803D"
  neutral: "#FAFAFA"
  surface: "#F5F5F5"
  border: "#D4D4D4"
  on-primary: "#FAFAFA"
  primary-dark: "#FAFAFA"
  secondary-dark: "#A3A3A3"
  tertiary-dark-mode: "#22C55E"
  neutral-dark: "#0A0A0A"
  surface-dark: "#171717"
  border-dark: "#404040"
typography:
  headline-lg:
    fontFamily: DM Mono
    fontSize: 40px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.01em
  headline-md:
    fontFamily: DM Mono
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.3
  body-md:
    fontFamily: DM Mono
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.7
  label-md:
    fontFamily: DM Mono
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 48px
  2xl: 64px
  3xl: 80px
  4xl: 120px
  5xl: 160px
  section: 80px
  pad-button: 16px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.pad-button}"
  button-primary-hover:
    backgroundColor: "{colors.tertiary-dark}"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
  dashed-panel:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
---

## Overview

Sanctuary Tech is trauma-informed design. The interface should feel honest, no-nonsense, and low-stress — no bright colors, no aggressive animations, no surprises. Monospace type signals technical honesty. Dashed borders feel structural without shouting. Suits crisis support, domestic abuse resources, healthcare for vulnerable populations, legal aid, privacy tools.

## Colors

Muted palette with one soft green accent. **Green chosen deliberately** — signals safety, "go", permission. Avoid red (danger), orange (warning), blue (corporate/cold) as primary accents for crisis tools.

**Light mode:**
- **Primary (#171717):** Headings
- **Secondary (#525252):** Body text
- **Tertiary (#16A34A):** Single green accent — safety signal
- **Tertiary-dark (#15803D):** Hover, active state
- **Neutral (#FAFAFA):** Main background
- **Surface (#F5F5F5):** Section backgrounds
- **Border (#D4D4D4):** Dashed borders — the signature structural motif

**Dark mode:**
- Primary-dark (#FAFAFA), secondary-dark (#A3A3A3), tertiary (#22C55E), neutral-dark (#0A0A0A), surface-dark (#171717), border-dark (#404040)

## Typography

DM Mono (or JetBrains Mono) throughout — body, headings, labels, everything. Monospace reads as "straightforward, honest, technical" rather than "marketed to you". Body at 15px/1.7 for comfortable reading under stress.

## Layout

Generous whitespace (80px+ section padding). Dashed borders to frame important content panels. One action per screen where possible — reduce cognitive load. No animations beyond subtle opacity or color transitions on interactive states.

## Shapes

Modest rounding (4px), mostly sharp. Cards use dashed 1px borders instead of fills or shadows.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Tertiary muted accent (`{colors.tertiary}`) on inverted text, sharp 4px radius, mono label typography. Calm and clearly clickable — never urgent or alarming.
- **`card-default`** — Surface panel with sharp corners and generous 32px padding. Content stays uncrowded; users in stress need breathing room.
- **`dashed-panel`** — Neutral background with dashed 1px border (not fill or shadow), sharp corners and 32px padding. Frames information without enclosing it heavily.

All components use generous internal padding (32px standard) to convey calm and respect for the user. Borders prefer dashed over solid; fills prefer transparent over saturated. Hover states are subtle tonal shifts, never colour jumps. Trauma-informed: never use red as the primary urgency color, never use motion to draw attention.

## Do's and Don'ts

- Do use green (#16A34A) as the single accent — it signals safety
- Do use dashed borders for panels and framed content
- Do reduce every screen to one or two clear actions
- Don't use red, orange, or blue as primary accents — wrong emotional signals for crisis
- Don't use animations that move fast or demand attention
- Don't use sans-serif — mono is the honesty signal
- Don't cram information — whitespace is a safety feature here
