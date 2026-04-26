# Motion-Directed Spatial Portfolio

Cinematic, animation-led portfolio and case-study system for digital studios, creative technologists, product experience designers, Webflow interaction specialists, and spatial product showcases. Dark full-bleed atmosphere, oversized thin display typography, grayscale or low-saturation media, spatial object framing, scroll choreography, and project fragments that feel directed rather than merely laid out.

This is not a normal portfolio grid. It is a motion-directed website: each section behaves like a scene, each media asset has a camera relationship, and typography enters and leaves as part of the composition.

A working specimen lives at `_tests/design-skill-lab/oneshot/motion-directed-spatial-portfolio.html`. Treat it as the canonical reference build. Captured screenshots sit in `_tests/design-skill-lab/oneshot/_screenshots/`.

## Best for

- Webflow designers and interaction studios
- creative technologists
- 3D / product experience studios
- digital product portfolios
- premium agency portfolios
- industrial / product design case studies
- hardware and mobility product stories
- festival or event identity case studies
- immersive ecommerce campaign pages

**Avoid for:** hospitals, schools, legal/accounting, public information sites, docs, dashboards, accessibility-first informational pages, and any project where users must scan facts faster than they experience atmosphere.

## Required Resources

The skill expects these to be available. If something is missing, fall back gracefully (noted per item).

### Image generation

This style is media-driven, but the right way to fill the media slots depends on the runtime.

**Default — inline SVG illustrations (Claude Code, Cowork, any environment without an image-gen API):**

Build distinct SVG scenes inline for every media slot. The reference specimen at `_tests/design-skill-lab/oneshot/motion-directed-spatial-portfolio.html` is the canonical pattern:

- **Hero spatial object** — animated SVG (orb, concentric rings, frame markers, floating data chips). See the `<svg viewBox="0 0 600 600">` block in the hero of the reference build.
- **Tile media (3 SVGs)** — each project gets a distinct scene. Atlas: floating product OS interface mockup. Field: editorial type-and-horizon with sun glow. Halo: centered luxury capsule on concentric rings. See the `<svg viewBox="0 0 800 600">` blocks in the zigzag tile section.
- **Pinned panel media** — atmospheric stack (radial gradients + grid overlay + vignette + animated `::before` element per project).
- **Gallery cards** — gradient-and-shape blocks per card (animated radial center + numbered chip + meta tag).

Each project must have a *visually distinct* scene. Never ship plain gradient placeholders for tile media — they read as empty.

**When the runtime is Codex (or any agent with OpenAI image-model access):**

Generate real images via the OpenAI image model and save them to `assets/motion-directed-spatial-portfolio/` next to the HTML. Reference via `<img>` tags. Required slots and prompts:

- `hero-spatial.png` — "cinematic dark spatial scene, abstract orb or sculpture, deep purple and indigo atmosphere, soft volumetric light, 4:3"
- `tile-atlas.png` — "floating product OS interface mockup over purple and blue spatial atmosphere, depth grid lines, status chip overlay, dark cinematic, 4:3"
- `tile-field.png` — "editorial type-and-horizon scene, warm orange sun glow over low horizon, long sans-serif type fragments, dark sky, 4:3"
- `tile-halo.png` — "centered luxury product capsule on concentric teal rings, dark cradle, soft inner glow, spatial commerce mood, 4:3"
- `panel-atlas.png` / `panel-field.png` / `panel-halo.png` — full-bleed 16:9 cinematic versions of the same three projects
- `gallery-01.png` … `gallery-05.png` — moody 4:3 thumbnails (talk poster, award medallion, webinar still, article cover, conference photo)

After generating, count the files. Must be ≥12 before writing HTML. If any slot fails to generate, fall back to the inline SVG pattern for that slot only and note it in the final report.

**Do not use Pixa MCP.** It was tried earlier in development and the auth/registration friction made it unreliable. Stick with inline SVG (Claude/Cowork) or OpenAI image model (Codex).

### Animation libraries (CDN, always required)

```html
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@splidejs/splide@4.1.4/dist/js/splide.min.js"></script>
<link  href="https://cdn.jsdelivr.net/npm/@splidejs/splide@4.1.4/dist/css/splide-core.min.css" rel="stylesheet">
```

- **Lenis** — smooth scroll. Required.
- **GSAP + ScrollTrigger** — scroll-scrubbed parallax, pinning, text mask reveals. Required.
- **Splide** — draggable horizontal gallery for the "What's Hot" section. Required when that section is present.

### Fonts (Google Fonts, always required)

- **Inter Tight** weights `200, 300, 400, 500` — display + UI
- **Fraunces** weights `200, 300, 400` (italic enabled) — editorial body and italic accents
- **JetBrains Mono** weight `400` — metadata, captions, status chips

### Safety net JS (always required)

The script must include:

1. An inline `<head>` script that adds `has-curtain` class only when motion is allowed (so file:// double-click never traps the user behind a curtain)
2. A `safeBoot()` wrapper around the main motion init — catches any thrown error and forces a static-render fallback
3. A 4-second watchdog timer that force-removes the curtain if it's still up
4. A `?static` query parameter that disables animations and shows everything statically (for screenshot tools)
5. The motion script wrapped in an IIFE so its locals (especially short variable names) don't collide with minified library globals

These are non-negotiable. The build has been broken twice by missing them.

## Quick Start

1. Build a dark full-bleed page, not a white portfolio shell.
2. Use oversized thin geometric sans display type as the main architectural material.
3. Use one contrasting editorial serif for italic accents inside headlines and for body copy. Never use serif italic *inside* a headline as decoration without intent.
4. Treat hero media as a spatial object: generated illustration, SVG scene, vehicle, product, sculpture, screen, or object-in-environment.
5. Use scroll milestones, not a static section stack.
6. Capture 5+ viewport keyframes while designing; full-page screenshots are not enough.
7. Use motion only when it changes spatial understanding: reveal, mask, scale, parallax, pin, scrub, rotate, or move a camera-like layer.
8. Build distinct inline SVG illustrations for every media slot (default). When the runtime is Codex, generate real images via the OpenAI image model and save to `assets/motion-directed-spatial-portfolio/`. Never ship plain gradient placeholders for tile media.

## Design Character

Motion-Directed Spatial Portfolio feels like a monochrome product film crossed with a portfolio. It has the restraint of minimalism but the composition is not static. Huge text, object photography or illustration, 3D-like product framing, and negative space are choreographed across scroll.

The page should feel:

- cinematic
- spatial
- premium
- quiet but not static
- motion-authored
- case-study capable
- slightly strange in a controlled way

If it feels like a normal agency homepage with fade-ins, it failed.

## Design Tokens Summary

**Colors:**

- Page black: `#050505`
- Stage black: `#0a0a0a`
- Charcoal: `#111111`
- Soft graphite: `#1a1a1a`
- Primary text: `#f4f4f0`
- Secondary text: `#c9c7c1`
- Muted text: `#8a8882`
- Ghost text: `rgba(244,244,240,0.45)`
- Hairline: `rgba(255,255,255,0.14)`
- Hairline faint: `rgba(255,255,255,0.06)`
- Accent acid: `#62ff6a`
- Accent warm: `#d7c0a2`
- Overlay: `rgba(0,0,0,0.48)`

Accent usage should be rare. Most pages are black, white, grayscale, and one shock accent used in a case-study panel or project-specific highlight. Per-tile atmospheric color (purple/orange/teal in the reference build) gives each project a separate scene identity.

**Typography:**

- Display: Inter Tight, weight 200, line-height 0.86, letter-spacing -0.045em, uppercase
- Italic accent: Fraunces, weight 300 italic, lowercase, embedded inside Inter Tight headlines for one word at a time
- Body / editorial: Fraunces, weight 300, line-height 1.18-1.30
- UI labels: Inter Tight 500, 12px, letter-spacing 0.04em, uppercase
- Metadata: JetBrains Mono, 11px, letter-spacing 0.06em, uppercase

When mixing fonts inside a headline, account for per-font baseline differences. Serif italic sits visually higher than uppercase sans of the same `font-size` — give the italic word slightly less letter-spacing and the same line-height as the surrounding sans.

**Layout:**

- Full-bleed page
- Fixed top nav with minimal labels (brand left, CTA + time + hamburger right)
- Hero height: `100svh`
- Pinned panel sections: `100svh` each
- Scene sections (zigzag tiles, gallery, manifesto, contact): variable height, never less than 80svh for breathable presence
- Project zigzag tiles: same image size on every tile, alternating image-left/image-right rhythm
- Container max width applies only to captions/metadata, not the main composition

**Motion:**

- Hero title masks reveal line-by-line (clip-path / translateY 110% → 0) on a stagger
- Spatial object drifts/rotates/scales subtly on scroll
- Foreground/background layers move at different rates
- Project media pins briefly while next panel rises over it
- Section titles can clip/reveal by line
- Cursor/hover affects media (scale 1.04 inside overflow-hidden frames), but should not become a gimmick

## Required Page Structure

The reference specimen demonstrates the canonical section order. Every build using this style should include these sections, in this order:

1. **Curtain + nav** — page-load curtain (with count-up), fixed nav (brand · start a project · time · hamburger)
2. **Hero** — multi-line architectural headline + spatial object/illustration + editorial caption + meta footer row
3. **Ticker / marquee** — slowly scrolling discipline list as a thin breakout band
4. **Zigzag tile section** — three project tiles, same image size, alternating image-left → image-right → image-left, each with copy column (label, headline with italic accent, body paragraph, metadata grid)
5. **Pinned full-bleed panels** — three project scenes (one per zigzag project), each pinned full-viewport with cinematic atmospheric media, project name + tagline, body description, discipline tag pills, bottom label row with project + discipline + view-case link
6. **What's Hot draggable gallery** — Splide-driven horizontal carousel, 3-5 cards bleeding off both edges, each with media + numbered chip + meta tag + serif caption below
7. **Manifesto** — single right-aligned massive thin sans claim with one italic accent word, "Find out more" link
8. **Contact / closing** — `[Final frame ...]` head row, big claim with italic accent, bordered Contact CTA, four-column meta footer (Email, Studio, Now Booking, Stay in Touch with social links)
9. **Flip menu** (overlay, triggered by hamburger) — full-page rotateX flip-in, four nav links with mono numbers, aside with serif body copy + reach-the-studio block, footer with location + social links

Sections that are not in this list usually mean the page has slipped into generic-agency territory. If you cut a section, document why.

## Signature Patterns

### Spatial hero object

The hero centers on an object or object-like media layer. It should be an inline SVG scene (default) or a Codex-generated image — never a plain gradient. The object must feel physically staged, not pasted in a card.

Use:

- dark vignette
- object layer above background
- multi-line headline crossing or wrapping around the object
- small metadata at the top or edges
- one editorial serif paragraph as caption

### Multi-line headline with italic accent cycler

Headlines are not just readable headings. They define the page structure.

```html
<h1 class="hero__display">
  <span class="hero__display-line"><span>Digital</span></span>
  <span class="hero__display-line indent"><span>product</span></span>
  <span class="hero__display-line">
    <span class="hero__display-cycler">
      <span class="hero__display-cycler-track" data-cycler>
        <span>experiences</span>
        <span>encounters</span>
        <span>moments</span>
        <span>frames</span>
      </span>
    </span>
  </span>
  <span class="hero__display-line indent"><span>that matter.</span></span>
</h1>
```

ONE line of the headline cycles a Fraunces italic word every ~2.8 seconds. The rest stays static. The cycling word is rendered in serif italic lowercase to contrast the surrounding uppercase sans. Per-font line-height adjustments are critical — see the design tokens above.

### Zigzag tile section (NOT the same as pinned panels)

Three tiles in a 2-column grid, image and copy swapping sides on each:

- Tile 1: image **left**, copy right
- Tile 2: image **right**, copy left (`tile--right` modifier)
- Tile 3: image **left**, copy right

All three tile media slots must have the **same aspect ratio and visual weight** to create a clean diagonal rhythm. The media is a richer SVG illustration (or generated image) per project — Atlas gets a UI screen mockup, Field gets editorial type-and-horizon, Halo gets a centered product on rings. Never a flat gradient.

### Pinned full-bleed panels (separate from zigzag)

Each project also gets a full-viewport pinned scene. GSAP ScrollTrigger pins each panel briefly so the next one rises over it. Inside the pinned scene:

- atmospheric full-bleed media (matching the tile's color identity but more cinematic)
- top label strip: `[Featured · 01 / 03]` and `Pinned scene · {discipline}`
- bottom-area content grid: project name + tagline (with italic accent), body paragraph, discipline tag pills, bottom label row (project, discipline, view case)

### Draggable gallery (Splide)

Splide config:

```js
new Splide("#hot-carousel", {
  type: "slide",
  autoWidth: true,
  gap: 20,
  drag: "free",
  snap: true,
  arrows: false,
  pagination: false,
  flickPower: 600,
  easing: "cubic-bezier(0.16, 1, 0.3, 1)",
  speed: 800,
}).mount();
```

Cards bleed off both edges (left/right padding only on the track, not on the slides). Each card: media block (4:3) + numbered chip + meta tag + serif caption *below* the media (not overlaid — captions overlaid on bleeding cards always clip).

### Full-page flip menu

Triggered by the nav hamburger. Full-viewport overlay that flips in via `rotateX(-92deg → 0)` over ~720ms with cubic-bezier mask easing. Hamburger morphs into X (two `transform: rotate(45deg / -45deg)`). Body scroll locks via `is-menu-open` class on `<html>`. Lenis smooth-scroll pauses while open.

Menu structure:

- header strip: brand · index · scene/reel count
- main grid: numbered nav links (WORK, STUDIO, PROCESS, CONTACT — each [01]–[04]) staggered in from below + aside with serif body copy + reach-the-studio block
- footer: location coordinates + social links

Hover state on a nav link: morphs from Inter Tight uppercase to Fraunces serif italic lowercase, gap widens. Small luxury detail.

ESC and any nav-link click close the menu.

### Case-study archive mode (variant)

For project pages, switch from studio hero to object archive:

- centered product hero
- sparse metadata
- process cards or image fragments
- industrial/product textures
- occasional high-saturation project color
- repeated motif blocks

## Components

### Fixed minimal nav

- Position: fixed top
- Background: transparent
- `mix-blend-mode: difference` so it reads on dark and light backgrounds
- Layout: brand left, start-a-project middle, time + hamburger right
- Hamburger morphs to X when menu open

### Ghost button / pill

- Transparent
- 1px hairline border (`rgba(255,255,255,0.14)`)
- Small uppercase label (11px, letter-spacing 0.06em)
- 9999px pill or 4px rectangle depending on context
- Hover: invert (background → bone, text → page) or slight glow

### Project frame (zigzag tile)

- Same aspect ratio across all tiles in the section
- 1px hairline-faint border
- Inner SVG art absolute-positioned to fill
- Number chip top-left, project title bottom-left, tag chip bottom-right
- Hover: inner art scales 1.04 inside `overflow: hidden`

### Pinned scene

- Full-viewport
- Atmospheric media stack: base gradient + grid overlay + vignette
- Distinctive animated element per project (orb, horizon shift, concentric rings)
- Content grid bottom-positioned, never floating mid-screen

### Scene caption

- Fraunces serif, weight 300
- 18-24px
- Max width 32-38ch
- Used as a quiet counterpoint to giant display type

## Motion Rules

Do:

- Use scroll progress as a timeline.
- Use transform and opacity as the main animation tools.
- Pin sparingly; one or two pinned sections is fine, the reference uses three.
- Use `prefers-reduced-motion` to reduce movement to fades and static placement.
- Use `?static` query param for screenshot tools.
- Keep text readable at each scroll keyframe.
- Capture keyframe screenshots during review.
- Wrap motion init in `safeBoot()` with a watchdog timer.
- Wrap your main script in an IIFE.

Don't:

- Do not add generic fade-up animation to every block.
- Do not animate everything at once.
- Do not use loader theatre unless the site is a portfolio showcase.
- Do not hide content behind long animation delays.
- Do not make full-page screenshots your only QA artifact.
- Do not let the curtain stay up if scripts fail.
- Do not declare short variable names like `n` in global scope (collides with minified libraries).

## Analysis Method For References

For any new reference in this style:

1. Capture hero after the loader clears.
2. Capture 3-5 viewport screenshots at scroll milestones.
3. Record motion grammar:
   - loader type
   - pinned sections
   - parallax layers
   - scale/opacity reveals
   - typography splitting/masking
   - media transitions
   - cursor or hover behavior
   - menu open animation
4. Inspect the live site's `window` object for the libs in use (look for `gsap`, `Lenis`, `Splide`, `ScrollTrigger`, `window.matchMedia` queries).
5. Create a static contact sheet from keyframes.
6. Write the style spec from the keyframes plus motion grammar.

## Tier Placement

- Choose **Motion-Directed Spatial Portfolio** when motion and spatial media are the core brand proof.
- Choose **Spatial Product Showcase** for product/object/3D sites that need less portfolio theatre.
- Choose **Cinematic Mono Brutal** for black-and-white agency sites driven by type/video, not spatial product scenes.
- Choose **Creative Studio Heavy** for colorful/agency motion systems with branded intros and broad service storytelling.
- Choose **Atmospheric Protocol** for editorial intelligence/protocol pages with ambient gradients rather than physical/spatial media.

## Reference Build

The working specimen is `_tests/design-skill-lab/oneshot/motion-directed-spatial-portfolio.html`. It is the source of truth for this style. When in doubt about layout, copy structure, motion timing, or component anatomy, read the specimen — it implements every pattern in this spec. The accompanying `motion-directed-spatial-portfolio.design.md` carries the YAML token block for design-system tooling.
