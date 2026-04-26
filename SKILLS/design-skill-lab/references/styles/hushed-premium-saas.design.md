---
version: alpha
name: Hushed Premium SaaS
description: Whisper-weight display typography on warm-white canvas with sub-0.1 opacity multi-layer shadows. Premium consumer-tech and refined SaaS register — quiet confidence over loud announcement.
colors:
  primary: "#000000"
  secondary: "#4E4E4E"
  tertiary: "#777169"
  neutral: "#FFFFFF"
  surface: "#F5F5F5"
  surface-warm: "#F5F2EF"
  surface-warm-translucent: "rgba(245, 242, 239, 0.8)"
  border-soft: "#E5E5E5"
  border-faint: "rgba(0, 0, 0, 0.05)"
  on-primary: "#FFFFFF"
  ring-focus: "rgba(147, 197, 253, 0.5)"
typography:
  display-xl:
    fontFamily: Waldenburg
    fontSize: 96px
    fontWeight: 300
    lineHeight: 1.05
    letterSpacing: -0.02em
  display-lg:
    fontFamily: Waldenburg
    fontSize: 72px
    fontWeight: 300
    lineHeight: 1.08
    letterSpacing: -0.02em
  display-md:
    fontFamily: Waldenburg
    fontSize: 48px
    fontWeight: 300
    lineHeight: 1.08
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Waldenburg
    fontSize: 36px
    fontWeight: 300
    lineHeight: 1.17
  headline-md:
    fontFamily: Waldenburg
    fontSize: 32px
    fontWeight: 300
    lineHeight: 1.13
  body-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0.18px
  body-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0.18px
  body-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0.16px
  body-medium:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0.16px
  ui-nav:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.15px
  button-default:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.47
  button-bold:
    fontFamily: Waldenburg
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: 0.7px
    textTransform: uppercase
  caption:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: 0.14px
  code-md:
    fontFamily: Geist Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.85
  micro:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
rounded:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 20px
  xl: 24px
  warm: 30px
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
  section: 96px
  pad-card: 24px
  pad-button-pill: "0px 14px"
  pad-button-warm: "12px 20px 12px 14px"
shadows:
  inset-edge: "rgba(0,0,0,0.075) 0px 0px 0px 0.5px inset, #ffffff 0px 0px 0px 0px inset"
  outline-ring: "rgba(0,0,0,0.06) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 1px 2px, rgba(0,0,0,0.04) 0px 2px 4px"
  card: "rgba(0,0,0,0.4) 0px 0px 1px, rgba(0,0,0,0.04) 0px 4px 4px"
  warm-lift: "rgba(78,50,23,0.04) 0px 6px 16px"
  edge-subtle: "rgba(0,0,0,0.08) 0px 0px 0px 0.5px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-default}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button-pill}"
  button-secondary-white:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    typography: "{typography.button-default}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button-pill}"
    boxShadow: "{shadows.card}"
  button-warm-stone:
    backgroundColor: "{colors.surface-warm-translucent}"
    textColor: "{colors.primary}"
    typography: "{typography.button-default}"
    rounded: "{rounded.warm}"
    padding: "{spacing.pad-button-warm}"
    boxShadow: "{shadows.warm-lift}"
  button-uppercase-bold:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-bold}"
    rounded: "{rounded.full}"
    padding: "{spacing.pad-button-pill}"
  card-default:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.pad-card}"
    boxShadow: "{shadows.outline-ring}"
  card-elevated:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.lg}"
    boxShadow: "{shadows.card}"
  page-shell:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    padding: "{spacing.xl}"
---

## Overview

Hushed Premium SaaS is the inverse of bold-display systems. Where most modern SaaS reaches for weight 700-900 to demand attention, this style reaches for weight 300 — light, almost whisper-thin display typography that creates intrigue through restraint. Inspired by ElevenLabs' approach to voice AI: the design feels like a premium audio brochure where lightness reads as confidence, not weakness.

Suits premium consumer tech, voice/audio AI, refined SaaS launch pages, boutique creator tools, and any product that earns trust through quietness rather than volume. Sits between Warm Serene Luxury (photography-led hospitality) and Rounded Energetic SaaS (chunky friendly product) — a premium SaaS register that is neither hospitality nor energetic.

## Colors

Achromatic palette with warm undertones. The page is white, but the warmth comes from warm-stone surfaces (`#F5F2EF` at 80% opacity) and warm-tinted shadows (`rgba(78, 50, 23, 0.04)`) — never from accent hues.

- **Primary (#000000):** Headlines, display type, primary CTA fills
- **Secondary (#4E4E4E):** Body text, descriptions
- **Tertiary (#777169):** Muted links, decorative underlines, fine print — warm gray, not cool
- **Neutral (#FFFFFF):** Primary background, card surfaces, button fills
- **Surface (#F5F5F5):** Subtle section differentiation
- **Surface-warm (#F5F2EF):** Warm stone tint — the signature warm surface
- **Surface-warm-translucent (rgba(245,242,239,0.8)):** Featured CTA background
- **Border-soft (#E5E5E5):** Explicit borders
- **Border-faint (rgba(0,0,0,0.05)):** Ultra-subtle separators

No brand color. The palette is intentionally achromatic. Warmth is the only "color" decision, and it lives in surfaces and shadows rather than in hues.

## Typography

Three-family system with disciplined roles:

- **Waldenburg weight 300 (Light)** for ALL display headings. This is the defining choice. The lightness is non-negotiable — bold Waldenburg breaks the entire identity. Letters feel like sound waves rendered in type: thin, precise, surprisingly impactful at scale.
- **Inter weight 400-500** for body and UI, with **positive letter-spacing (+0.14px to +0.18px)** that creates an airy reading rhythm. This contrasts deliberately with the tight display tracking (-0.02em).
- **Waldenburg weight 700 uppercase (WaldenburgFH)** appears only in specific bold CTA labels with 0.7px letter-spacing — the one place the type system raises its voice. Use sparingly.
- **Geist Mono** at relaxed line-height (1.85) for code blocks. Unhurried, never hurried.

Display sizes scale from 48px (card heading) to 96px (hero) — generous but not aggressive. The lightness compensates for the size; together they read as confident rather than shouting.

## Layout

Apple-like generosity: 96px+ vertical section padding creates a premium, unhurried pace. Each section is an exhibit. The whitespace isn't cold because the warm-stone surfaces and warm-tinted shadows give empty space a tactile quality.

Single-column hero, expanding to 2-3 column feature grids. Full-width gradient or warm-surface sections alternate with white content sections. Centered content with generous max-width — never edge-to-edge unless the content is a full-bleed product showcase.

## Elevation & Depth

The most refined shadow system in the library. Every shadow operates at sub-0.1 opacity, and many include both outward cast AND inward inset components. The signature is **shadow stacking**:

- **Inset edges** (`0 0 0 0.5px inset`) define internal borders so subtle they're felt rather than seen
- **Outline rings** (`0 0 0 1px` at 6% black) act as shadow-as-border for cards
- **Soft elevations** (`0 4px 4px` at 4% black) provide gentle lift
- **Warm-tinted shadows** (`rgba(78,50,23,0.04) 0 6px 16px`) on featured CTAs — shadows have color, not just darkness

Combine all of these on prominent elements (inset + outline + elevation). Surfaces seem to barely exist, floating just above the page with the lightest possible touch.

## Shapes

Generous radii throughout. **Pills (9999px) for primary buttons** — non-negotiable, no sharp-cornered buttons. **30px for warm-stone CTAs** — slightly less round than full pill, creates the asymmetric tactile signature. **16-24px for cards** — comfortable, never sharp. Sharp corners (<8px) on cards break the ethereal quality.

## Components

Component tokens are defined in the YAML front matter. Key patterns:

- **`button-primary`** — Solid black on white text, full pill, default body button typography. The standard CTA.
- **`button-secondary-white`** — White fill on primary text, full pill, with the card-shadow stack (`rgba(0,0,0,0.4) 0px 0px 1px, rgba(0,0,0,0.04) 0px 4px 4px`). Used as the secondary action next to primary.
- **`button-warm-stone`** — The signature button. Translucent warm-stone fill (`rgba(245,242,239,0.8)`), 30px radius (not full pill), asymmetric padding (`12px 20px 12px 14px`), warm-tinted shadow (`rgba(78,50,23,0.04) 0px 6px 16px`). Used for hero/featured actions where tactile quality matters.
- **`button-uppercase-bold`** — Reserved for specific brand-loud moments. WaldenburgFH 14px weight 700 uppercase with 0.7px tracking. The one place type gets loud.
- **`card-default`** — White surface with 20px radius and the multi-layer outline-ring shadow stack (3 layers at sub-0.1 opacity). Reads as a surface that barely exists.
- **`card-elevated`** — White surface with 24px radius and the card shadow (1px outline + 4px lift). For prominent feature cards.

All components defer to typography. The shadow system carries depth; nothing relies on heavy fills, saturated borders, or aggressive contrast. Hover states are subtle tonal shifts (background opacity nudges, slight shadow growth), never colour jumps.

## Do's and Don'ts

- Do use Waldenburg weight 300 for ALL display headings — the lightness IS the brand
- Do stack shadows in 3 layers (inset + outline + elevation) at sub-0.1 opacity for prominent surfaces
- Do use warm-tinted shadows (`rgba(78,50,23,0.04)`) on featured CTAs
- Do apply positive letter-spacing (+0.14 to +0.18px) on Inter body text
- Do use 9999px pill for primary buttons; 30px for the warm-stone signature CTA
- Do let whitespace be the loudest element — 96px+ section padding is the rhythm
- Don't use bold (700+) Waldenburg for body or section headings — only for the specific uppercase bold CTA
- Don't use heavy shadows (>0.1 opacity) — the ethereal quality requires whisper-level depth
- Don't introduce brand colors or accent hues — the system is achromatic with warm undertones
- Don't use cool gray borders — the warm-tint pervades borders, surfaces, and shadows
- Don't apply negative letter-spacing to body text — Inter uses positive tracking here
- Don't make buttons opaque and heavy — the warm translucent stone treatment is the signature
- Don't use sharp corners (<8px) on cards — the generous radius is structural

## Sector Fit

**Best for:** Premium consumer tech, voice/audio AI products, refined SaaS launch pages, creator tools with a premium register, boutique productivity, design tools, audio/music platforms, Apple-adjacent product categories.

**Avoid for:** Bold disruptive startups (use Bold Grid Manifesto), kids/family products (use Rounded Energetic SaaS or Spritify), conservative legal/finance (use Institutional Serif Advisory or Quiet Editorial Authority), crisis support / trauma-sensitive content (use Calm Secure Monospace), photography-driven hospitality (use Private Client Luxury).

## Known Tensions

- **Light weight + accessibility:** Waldenburg 300 at body sizes can fail WCAG AAA. Hold the line at display only — body must use Inter weight 400+. If a hero subtitle is under 24px, switch to Inter, not Waldenburg.
- **Shadow stacking + performance:** Three-layer shadows on every card can hit paint performance on lower-end devices. Reserve the full stack for hero/feature cards; use the single outline-ring on bulk grids.
- **Warm shadows + dark mode:** This style is designed for light surfaces. A dark-mode adaptation would need to invert the warmth (warm-tinted glow instead of warm-tinted shadow) and is not part of this preset.
