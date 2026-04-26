---
version: alpha
name: Motion-Directed Spatial Portfolio
description: "Animation-led dark portfolio and case-study style for creative technologists, Webflow specialists, spatial product studios, and premium digital portfolios. The page is designed as scroll keyframes — spatial hero object, oversized thin typography, grayscale media, sparse metadata, product/process fragments, and motion-directed transitions. Required libs: GSAP + ScrollTrigger + Lenis + Splide. Default media path is inline SVG illustrations; when the runtime is Codex, generate images via the OpenAI image model and save to assets/motion-directed-spatial-portfolio/. Reference specimen: _tests/design-skill-lab/oneshot/motion-directed-spatial-portfolio.html."
style-base: motion-directed-spatial-portfolio
style-tuning:
  axes:
    color-mode:
      value: dark
      rationale: The style depends on dark cinematic space; light mode removes the stage.
    fonts:
      value: mix
      rationale: Thin geometric sans display plus a small editorial serif counterpoint.
    layout:
      value: loose
      rationale: Composition is scene-directed, with intentional overlap, cropping, and spatial layers.
    content-width:
      value: full-bleed
      rationale: Media and spatial scenes use the viewport as canvas.
    corners:
      value: sharp
      rationale: Media and scenes should feel cinematic and architectural, not card-like.
    motion:
      value: high
      rationale: Scroll choreography is the style's core proof.
    color-loudness:
      value: monochrome
      rationale: Grayscale/dark palette with one project-specific shock accent.
    imagery:
      value: 3d
      rationale: Spatial object/media layers are load-bearing, even when built with CSS or photographic assets.
    page-load:
      value: subtle
      rationale: A short mask/fade reveal is acceptable; avoid long loaders unless the site is pure portfolio theatre.
colors:
  page-black: "#030303"
  stage-black: "#070707"
  charcoal: "#111111"
  graphite: "#1a1a1a"
  text-primary: "#f4f4f0"
  text-secondary: "#c9c7c1"
  text-muted: "#8a8882"
  text-ghost: "rgba(244,244,240,0.45)"
  hairline: "rgba(255,255,255,0.12)"
  hairline-faint: "rgba(255,255,255,0.06)"
  accent-acid: "#62ff6a"
  accent-warm: "#d7c0a2"
  overlay: "rgba(0,0,0,0.48)"
typography:
  display-xl:
    fontFamily: "Inter Tight, Satoshi, Neue Montreal, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(72px, 12vw, 168px)"
    fontWeight: 300
    lineHeight: 0.88
    letterSpacing: "-0.055em"
    textTransform: uppercase
  display-lg:
    fontFamily: "Inter Tight, Satoshi, Neue Montreal, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(56px, 9vw, 120px)"
    fontWeight: 300
    lineHeight: 0.9
    letterSpacing: "-0.045em"
    textTransform: uppercase
  headline-md:
    fontFamily: "Inter Tight, Satoshi, Neue Montreal, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(32px, 5vw, 64px)"
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  editorial:
    fontFamily: "Cormorant Garamond, Libre Baskerville, Georgia, serif"
    fontSize: "clamp(18px, 1.7vw, 24px)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body-sm:
    fontFamily: "Inter Tight, Helvetica Neue, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "-0.01em"
  label:
    fontFamily: "Inter Tight, Helvetica Neue, Arial, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.02em"
    textTransform: uppercase
  mono:
    fontFamily: "JetBrains Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "-0.01em"
rounded:
  sharp: 0px
  sm: 4px
  pill: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 72px
  scene: 100svh
  long-scene: 160svh
container:
  max-width: none
  caption-width: 36ch
  page-padding: "clamp(18px, 3vw, 48px)"
motion:
  fast: 180ms
  base: 420ms
  scene: 900ms
  scrub: "scroll-linked"
  ease-cinematic: "cubic-bezier(0.16, 1, 0.3, 1)"
  ease-mask: "cubic-bezier(0.77, 0, 0.175, 1)"
components:
  fixed-nav:
    backgroundColor: transparent
    textColor: "{colors.text-primary}"
    typography: "{typography.label}"
    position: fixed
  ghost-button:
    backgroundColor: transparent
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.hairline}"
    rounded: "{rounded.pill}"
    padding: "7px 12px"
  project-frame:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.hairline-faint}"
    rounded: "{rounded.sharp}"
    padding: 0px
  scene-caption:
    textColor: "{colors.text-secondary}"
    typography: "{typography.editorial}"
    maxWidth: "{container.caption-width}"
---

## Overview

Motion-Directed Spatial Portfolio is a dark cinematic design language for portfolios and case studies where motion is the proof of craft. It uses full-viewport scenes, object-like media layers, huge thin display typography, small metadata, and editorial captions. Pages are authored as scroll keyframes, not as a stack of cards.

## Required Patterns

Every build using this style should include:

- a spatial hero object or full-bleed product/media scene
- oversized thin display typography that overlaps or frames the object
- at least three scroll keyframes captured during QA
- a services/credits list rendered typographically, not as cards
- `prefers-reduced-motion` handling

## Reference Modes

Studio mode:

- portfolio hero
- floating screen/object
- project/media strips
- service credits
- contact/CTA close

Case-study mode:

- centered product/object hero
- sparse metadata
- archive/process fragments
- one project accent color
- repeated object/process motifs
