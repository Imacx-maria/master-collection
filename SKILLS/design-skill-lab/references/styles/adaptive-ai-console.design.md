---
version: alpha
name: Adaptive AI Console
description: "Dark-mode-native AI/product console style inspired by Linear's engineered restraint — near-black surfaces, Inter Variable precision, indigo-violet interaction accent, dense operational rows, command palette, AI composer, and accountable generated-action surfaces."
style-base: adaptive-ai-console
style-tuning:
  axes:
    color-mode:
      value: dark
      rationale: Dark is the native medium; light mode would require a separate product-console interpretation.
    fonts:
      value: sans
      rationale: Inter Variable is the whole typographic identity; mono is supporting chrome only.
    layout:
      value: grid-based
      rationale: Product-console surfaces need predictable columns, rows, panels, and inspector rails.
    content-width:
      value: standard
      rationale: Marketing pages use a 1200px cap; app shells can go full workspace but still use disciplined panels.
    corners:
      value: soft
      rationale: 6-12px functional radius; precise, not playful.
    motion:
      value: low
      rationale: Motion is functional and stateful, not theatrical.
    color-loudness:
      value: monochrome
      rationale: Achromatic dark UI with one indigo-violet action/active accent.
    imagery:
      value: abstract
      rationale: Product chrome, console fragments, command palette, and AI streams replace photography.
    page-load:
      value: functional
      rationale: AI/product interfaces may need skeletons, streaming states, and loading affordances rather than a branded intro.
colors:
  marketing-black: "#08090a"
  deep-black: "#010102"
  panel-dark: "#0f1011"
  surface-elevated: "#191a1b"
  surface-hover: "#28282c"
  text-primary: "#f7f8f8"
  text-secondary: "#d0d6e0"
  text-tertiary: "#8a8f98"
  text-quaternary: "#62666d"
  brand-indigo: "#5e6ad2"
  accent-violet: "#7170ff"
  accent-hover: "#828fff"
  security-lavender: "#7a7fad"
  success: "#27a644"
  emerald: "#10b981"
  border-primary: "#23252a"
  border-secondary: "#34343a"
  border-tertiary: "#3e3e44"
  border-subtle: "rgba(255,255,255,0.05)"
  border-standard: "rgba(255,255,255,0.08)"
  surface-ghost: "rgba(255,255,255,0.02)"
  surface-subtle: "rgba(255,255,255,0.04)"
  surface-standard: "rgba(255,255,255,0.05)"
  overlay: "rgba(0,0,0,0.85)"
typography:
  display-xl:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 72px
    fontWeight: 510
    lineHeight: 1.0
    letterSpacing: -1.584px
    fontFeatureSettings: '"cv01", "ss03"'
  display-lg:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 64px
    fontWeight: 510
    lineHeight: 1.0
    letterSpacing: -1.408px
    fontFeatureSettings: '"cv01", "ss03"'
  display:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 48px
    fontWeight: 510
    lineHeight: 1.0
    letterSpacing: -1.056px
    fontFeatureSettings: '"cv01", "ss03"'
  heading-1:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 32px
    fontWeight: 400
    lineHeight: 1.13
    letterSpacing: -0.704px
    fontFeatureSettings: '"cv01", "ss03"'
  heading-3:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 590
    lineHeight: 1.33
    letterSpacing: -0.24px
    fontFeatureSettings: '"cv01", "ss03"'
  body-lg:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: -0.165px
    fontFeatureSettings: '"cv01", "ss03"'
  body:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
    fontFeatureSettings: '"cv01", "ss03"'
  body-medium:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 510
    lineHeight: 1.5
    letterSpacing: 0
    fontFeatureSettings: '"cv01", "ss03"'
  caption:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 13px
    fontWeight: 510
    lineHeight: 1.5
    letterSpacing: -0.13px
    fontFeatureSettings: '"cv01", "ss03"'
  label:
    fontFamily: "Inter Variable, SF Pro Display, -apple-system, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 510
    lineHeight: 1.4
    letterSpacing: 0
    fontFeatureSettings: '"cv01", "ss03"'
  mono-body:
    fontFamily: "Berkeley Mono, ui-monospace, SF Mono, Menlo, monospace"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
rounded:
  micro: 2px
  sm: 4px
  md: 6px
  card: 8px
  panel: 12px
  large-panel: 22px
  pill: 9999px
spacing:
  px: 1px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  section: 80px
container:
  marketing-max-width: 1200px
  app-shell: full
  padding-x: 32px
shadows:
  micro: "rgba(0,0,0,0.03) 0px 1.2px 0px 0px"
  inset-panel: "rgba(0,0,0,0.2) 0px 0px 12px 0px inset"
  ring: "rgba(0,0,0,0.2) 0px 0px 0px 1px"
  elevated: "rgba(0,0,0,0.4) 0px 2px 4px"
  focus: "rgba(0,0,0,0.1) 0px 4px 12px"
motion:
  fast: 120ms
  base: 180ms
  reveal: 300ms
  stream: 600ms
  ease-standard: "cubic-bezier(0.4, 0, 0.2, 1)"
components:
  button-primary:
    backgroundColor: "{colors.brand-indigo}"
    textColor: "#ffffff"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    hoverBackground: "{colors.accent-hover}"
  button-ghost:
    backgroundColor: "{colors.surface-ghost}"
    textColor: "#e2e4e7"
    border: "1px solid {colors.border-standard}"
    rounded: "{rounded.md}"
    padding: "8px 14px"
  card:
    backgroundColor: "{colors.surface-ghost}"
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.border-standard}"
    rounded: "{rounded.card}"
    padding: "{spacing.xl}"
  panel:
    backgroundColor: "{colors.panel-dark}"
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.border-subtle}"
    rounded: "{rounded.panel}"
    padding: "{spacing.xl}"
  command-palette:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.border-standard}"
    rounded: "{rounded.panel}"
    shadow: "{shadows.elevated}"
  ai-composer:
    backgroundColor: "{colors.surface-ghost}"
    textColor: "{colors.text-secondary}"
    border: "1px solid {colors.border-standard}"
    rounded: "{rounded.card}"
    padding: "12px 14px"
  status-chip:
    backgroundColor: "transparent"
    textColor: "{colors.text-secondary}"
    border: "1px solid {colors.border-primary}"
    rounded: "{rounded.pill}"
    typography: "{typography.label}"
---

## Overview

Adaptive AI Console is the Linear-inspired operating surface for AI-native products. It is dark, exacting, quiet, and interaction-led. The defining feature is not a hero illustration or decorative gradient; it is product intelligence made visible through command palettes, AI composers, generated next-action rows, issue streams, trace metadata, confidence chips, and dense operational panels.

Use this style when the product must feel like a reliable AI workspace: fast, searchable, accountable, and calm under load.

## Differentiators

Compared with **Technical Refined**, Adaptive AI Console is less documentation/spec and more live operating system.

Compared with **Atmospheric Protocol**, it is less cinematic and more utilitarian; atmosphere gives way to product chrome.

Compared with **Sanctuary Tech**, it is denser and more productivity-oriented; not trauma-informed, not care-first.

## Required AI-Native Patterns

Every build using this style should include at least two of:

- command palette or `Cmd+K` search
- AI input composer
- generated next-action rows
- issue/task stream
- trace/provenance metadata
- confidence/source chips
- skeleton or streaming generated-content state

If none of those patterns are present, use another dark technical style instead.
