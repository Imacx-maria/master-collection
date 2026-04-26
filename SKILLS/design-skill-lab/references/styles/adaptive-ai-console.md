# Adaptive AI Console

Dark-mode-native product system for AI agents, workflow automation, analytics copilots, command centers, and enterprise consoles. Inspired by Linear's engineered restraint: near-black surfaces, precise Inter typography, one indigo-violet accent, whisper borders, dense but calm UI, and interaction patterns that feel fast, searchable, and adaptive.

This style is not a brochure skin. It is for products where the interface itself is the value: task queues, prompt runs, workflow states, issue streams, model outputs, command palettes, audit trails, and generated recommendations.

## Best for

- AI agents and copilots
- Workflow automation products
- Analytics and insight consoles
- Enterprise SaaS dashboards
- Knowledge tools and internal operating systems
- Developer-facing productivity tools
- Support automation and triage tools
- Finance, security, and ops platforms that need a clean AI-native control surface

**Avoid for:** schools, hospitals, local service websites, luxury editorial brands, restaurants, warm community brands, classic brochure sites, and anything that needs emotional warmth more than operational clarity.

## Quick Start

1. Start with a near-black canvas: `#08090a`.
2. Use Inter Variable everywhere, with `font-feature-settings: "cv01", "ss03"` globally.
3. Use only three weights: `400` for reading, `510` for UI/emphasis, `590` for strong emphasis. Avoid `700`.
4. Use brand indigo/violet only for primary actions, selected states, active AI focus, and links.
5. Build depth through luminance steps and semi-transparent white borders, not heavy shadows.
6. Add product-native AI surfaces: command palette, prompt/input composer, generated recommendation cards, status streams, confidence/trace metadata, and adaptive next-action rows.
7. Keep motion functional: subtle reveal, hover, focus, and live-state transitions. No theatrical loader.

## Design Character

Adaptive AI Console is precise, quiet, dense, and dark. Content emerges from the background through calibrated luminance: page black, panel dark, elevated surfaces, translucent cards, and hairline borders. The page should feel engineered, not decorated.

The style works best when it shows product intelligence directly:

- command palette or search trigger
- structured prompts or task instructions
- generated recommendations
- workflow state rows
- logs, traces, and timestamps
- model/source confidence chips
- "next best action" modules

If the page is only a marketing headline and feature cards, use `technical-refined` or `atmospheric-protocol` instead.

## Design Tokens Summary

**Colors:**

- Page background: `#08090a`
- Deep background: `#010102`
- Panel background: `#0f1011`
- Elevated surface: `#191a1b`
- Hover surface: `#28282c`
- Primary text: `#f7f8f8`
- Secondary text: `#d0d6e0`
- Tertiary text: `#8a8f98`
- Quaternary text: `#62666d`
- Brand indigo: `#5e6ad2`
- Accent violet: `#7170ff`
- Accent hover: `#828fff`
- Success: `#27a644`
- Emerald: `#10b981`
- Border subtle: `rgba(255,255,255,0.05)`
- Border standard: `rgba(255,255,255,0.08)`
- Overlay: `rgba(0,0,0,0.85)`

**Typography:**

- Primary: Inter Variable, `font-feature-settings: "cv01", "ss03"`
- Mono: Berkeley Mono; fallback to `ui-monospace`, `SF Mono`, `Menlo`
- Display XL: 72px, weight 510, line-height 1, letter-spacing -1.584px
- Display: 48px, weight 510, line-height 1, letter-spacing -1.056px
- H1: 32px, weight 400, line-height 1.13, letter-spacing -0.704px
- H3/card title: 20px, weight 590, line-height 1.33, letter-spacing -0.24px
- Body large: 18px, weight 400, line-height 1.6
- Body: 16px, weight 400, line-height 1.5
- UI/body medium: 16px, weight 510, line-height 1.5
- Caption: 13px, weight 400/510, line-height 1.5
- Label: 12px, weight 510/590, line-height 1.4
- Mono body: 14px, weight 400, line-height 1.5

**Radius:**

- Micro: 2px
- Small controls: 4px
- Buttons/inputs: 6px
- Cards/dropdowns: 8px
- Panels/popovers: 12px
- Large panels: 22px
- Pills: 9999px
- Icon circles: 50%

**Depth:**

- Depth is mostly luminance: `rgba(255,255,255,0.02)` -> `0.04` -> `0.05`
- Borders are semi-transparent white, usually 5-8% opacity
- Use inset shadow for recessed panels
- Use multi-layer dark shadow only for dialogs, command palettes, and popovers

## Signature Patterns

### Command palette as a first-class surface

Every Adaptive AI Console page should have a visible command/search affordance. It can be a `Cmd+K` trigger in nav, a central input composer, or a floating command panel.

Use:

- `#191a1b` panel
- `1px solid rgba(255,255,255,0.08)` border
- 12px radius
- 16px Inter input text
- 13px result labels, weight 510
- 12px metadata in quaternary text

### AI input composer

The input composer is the product's "mouth." It should be more important than a generic CTA.

Use:

- `rgba(255,255,255,0.02)` background
- 1px standard border
- 6-8px radius
- icon-aware padding
- attached action button in brand indigo
- optional model/source chips beneath

### Adaptive next-action row

Show generated recommendations as compact rows, not generic cards.

Each row should include:

- status dot or icon
- action label
- short reason
- confidence/source metadata
- primary affordance on the right

### Issue/task stream

Use Linear-like list rows for dense operational content:

- 44-52px row height
- subtle hover surface
- small status indicator
- title in 15-16px Inter 510
- metadata in 13px tertiary/quaternary text
- sparse accent only on selected/active state

### Trace / provenance metadata

AI surfaces must show why something appeared:

- `source`
- `confidence`
- `model/run`
- `updated`
- `owner`
- `status`

Use mono for run IDs and code-like labels only.

## Components

### Primary button

- Background: `#5e6ad2`
- Hover: `#828fff`
- Text: white
- Radius: 6px
- Padding: 8px 16px
- Font: Inter 14-16px, weight 510

### Ghost button

- Background: `rgba(255,255,255,0.02)`
- Text: `#e2e4e7`
- Border: `1px solid rgba(255,255,255,0.08)`
- Radius: 6px
- Hover: `rgba(255,255,255,0.05)`

### Card

- Background: `rgba(255,255,255,0.02)` to `rgba(255,255,255,0.05)`
- Border: `1px solid rgba(255,255,255,0.08)`
- Radius: 8px standard, 12px featured
- Hover: slight background opacity increase

### Panel

- Background: `#0f1011` or `#191a1b`
- Border: `1px solid rgba(255,255,255,0.05)`
- Radius: 12px
- Use for console panes, sidebars, and AI workspaces

### Badge / chip

- Background: transparent or `rgba(255,255,255,0.05)`
- Border: `1px solid #23252a`
- Radius: 9999px
- Font: 12px Inter 510
- Use for status, source, model, filter, and confidence chips

## Layout

- Container max: 1200px for marketing, full app shell for product surfaces
- Marketing hero: centered or slightly left-biased, with product console preview below
- Product shell: sidebar + main panel + optional inspector/assistant rail
- Feature sections: 2-3 columns, but include real product chrome or interaction fragments
- Section spacing: 80px desktop, 48px mobile
- Rows and panels should feel denser than marketing cards but never cramped

## Motion

Motion is functional:

- hover background opacity changes
- focus ring transitions
- row selection transitions
- subtle loading shimmer for generated content
- streaming text or progress states where content is genuinely generated

Avoid:

- branded intro loaders
- parallax spectacle
- large animated gradients
- exaggerated easing

## Do's and Don'ts

Do:

- Use `font-feature-settings: "cv01", "ss03"` globally on Inter.
- Use weight 510 as the default emphasis/UI weight.
- Use negative letter spacing on display sizes.
- Use near-black surfaces and white-opacity borders.
- Use indigo/violet sparingly and only for interaction or active intelligence.
- Show product-native AI affordances: composer, command palette, generated actions, traces.
- Use source/confidence/run metadata so AI output feels accountable.

Don't:

- Do not use pure white as the default text color; prefer `#f7f8f8`.
- Do not use weight 700.
- Do not make it a generic dark SaaS marketing page.
- Do not use decorative purple gradients.
- Do not use solid colored cards.
- Do not overuse the accent.
- Do not hide AI provenance behind vague sparkle language.
- Do not use heavy shadows for ordinary cards.

## Tier Placement

- Choose **Adaptive AI Console** when the interface is the product and AI behavior must be visible.
- Choose **Technical Refined** when the page is technical but not AI-native.
- Choose **Atmospheric Protocol** when the page is a cinematic/editorial intelligence brand, not an operational console.
- Choose **Sanctuary Tech** when calm, safety, privacy, or crisis sensitivity matters more than productivity density.
