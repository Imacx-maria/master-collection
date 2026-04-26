# Liquid Glass

Load in **Phase 3** whenever `effects.liquid-glass === true` in the project's tuning manifesto, after the chosen style craft guide has been loaded and before BUILD begins. This file owns the *modifier*, not a 14th style — it is the topmost-chrome translucency layer that can be overlaid onto an existing style system. Without it, "Apple-style glass" gets interpreted as `backdrop-filter: blur(10px)` on whatever element happens to be selected, which ships as flat glassmorphism and fails the a11y guardrails on first scroll.

---

## 1. What this is

Liquid Glass is a **modifier**, not a style. It promotes the translucent-chrome pattern that `atmospheric-protocol` already ships (style #12) into a portable contract that other styles can opt into without forking. The default track is CSS-only (`backdrop-filter` + variant tokens + a11y media queries); the opt-in track is WebGL/SDF refraction, gated by `dimension: shader-accents`. The reason this is not style #14: glass surfaces already exist inside Atmospheric Protocol, so a parallel style would either duplicate that work or invalidate it. A modifier reuses the existing `surface-glass`, `pad-glass`, and `card-glass` tokens and adds the variant axis (regular / clear / prominent), the `prefers-reduced-transparency` fallback, and the optional refraction shader on top.

The modifier does **two things only**: it standardises the glass token vocabulary across styles, and it gates the WebGL refraction track behind explicit prerequisites. Everything else — animation, layout, typography — defers to the host style.

---

## 2. When to load

**Phase 1 — detection.** The user trigger lexicon: "glass", "liquid glass", "Apple-style", "frosted", "translucent nav", "iOS 26", "glassmorphism upgrade", "make the nav translucent", "blurred chrome over scrolling content". Any hit sets `effects.liquid-glass = true` in the tuning manifesto. The trigger is recorded in provenance with the matched phrase.

**Phase 2 — compatibility check.** Look up the chosen style in the matrix in §3. If the row is `Native` or `Conditional`, proceed. If the row is `Refused`, escalate to the override protocol in §9. If the row is `Hard refuse` (Sanctuary Tech), refuse outright and offer style switch.

**Phase 3 — load.** This file loads after the style craft guide and before any markup is generated. The CSS track is mandatory. The WebGL refraction track is only available when both `style-tuning.axes.dimension.value === 'shader-accents'` and `effects.liquid-glass === true` evaluate true; otherwise skip §7 entirely.

**Phase 4 — review.** The corresponding effects review file at `references/style-reviews/effects/liquid-glass.md` runs alongside the chosen style's review file. Two reviews, both must pass.

---

## 3. Compatibility matrix

| Style | Tier | Where glass goes | Where it doesn't | Why |
|-------|------|------------------|------------------|-----|
| Atmospheric Protocol | Native | Cards, nav, modals, overlays | Body prose | Already ships `surface-glass` + 12px blur — modifier promotes existing patterns to canonical |
| Adaptive AI Console | Native | Command palette, composer modal, toasts | Console rows, data cells | Console chrome is the natural home for floating translucent surfaces |
| Creative Studio | Native | Nav, lightbox, hero card overlays | Process band content | Editorial hero region tolerates floating glass; reading bands need solid surfaces |
| Technical Refined | Conditional | Dropdowns, command menus, tooltips, modals | Dashboard data cards | Data legibility is the brand promise — glass on metrics is forbidden |
| Warm Serene Luxury | Conditional | Booking widget, sticky bar, hero modals | Body content, gallery | Photography is the hero; glass over photos blurs the photo |
| Editorial Portfolio | Conditional | Image lightbox, filter chips | Reading column | Reading column contrast is non-negotiable |
| Motion-Directed Spatial Portfolio | Conditional | Floating spec cards, morphing nav | Case-study reading sections | Spatial chrome welcomes glass; case-study reading does not |
| Hushed Premium SaaS | Conditional | Sticky nav (current default uses backdrop-blur already), command palette, modal overlays, floating action sheet | Hero, manifesto warm-stone panel, testimonial card, primary cards in services/audience grids | The quietness depends on solid warm-stone surfaces and multi-layer sub-0.1 shadows. Glass on body cards collapses the shadow grammar; glass in hero competes with the whisper-display. Chrome layer is the only safe zone. |
| Neo-Brutalist | Refused | — | — | Brutalism rejects translucency by definition |
| Memoir Blog | Refused | — | — | Reading-first memoir tone is incompatible with chrome effects |
| Sanctuary Tech | **Hard refuse** | — | — | Trauma-informed contract prohibits visual complexity (no override path) |
| Basalt E-Commerce | Refused | — | — | Product imagery is the hero; glass blurs it |
| Spritify | Refused | — | — | Playful flat aesthetic rejects depth chrome |
| Playful Bento | Refused | — | — | Bento celebrates solid colour blocks, not translucency |
| Warm Editorial | Refused | — | — | Warm-paper editorial tone rejects cold glass chrome |

The 6 non-Sanctuary refused styles allow a single-element override (see §9). Sanctuary Tech does not.

---

## 4. Eligible vs forbidden elements

Glass is for **chrome and overlay layers**. Anything that holds primary content, primary conversion, or primary data is forbidden. Anything that floats above content or sits on the topmost z-tier is eligible.

### Eligible — chrome layer
- Navigation bars and pills (top nav, sidebar, breadcrumbs that float, mobile bottom tabs)
- Dropdowns, command palettes, autocomplete menus, context menus, tooltips
- Modal dialogs, sheets, drawer panels, half-sheets, overlay panels
- Toast notifications and transient floating messages
- Floating filters, segmented controls, sticky filter rails, chips

### Eligible — overlay layer
- Lightbox / image gallery chrome (close button, navigation arrows, caption bar)
- Hero image overlays when the hero is photography and a card floats over it
- Sticky controls (booking widget, video scrubber, floating action buttons)
- Scroll-triggered floating cards (hover-reveal overlays where the underlying card stays meaningful through the glass)

### Conditional
- **Secondary CTAs** — eligible if the button is not the primary conversion action. Apple specifically allows glass on buttons during interaction states.
- **Buttons** — eligible if not the hero conversion button. The primary conversion button on a landing page needs maximum contrast and brand presence; reserve glass for secondary controls.
- **Search bars** — eligible if floating in a hero region or sticky nav. Inline-in-form search bars stay solid.
- **Sidebar nav with content scroll behind it** — eligible. Sidebar nav adjacent to a static panel — solid is fine, glass is optional.

### Forbidden
- Body content / reading column / article text containers
- Hero typography backgrounds (display headlines need a solid surface)
- Primary conversion CTAs
- Full sections / page-level wrappers
- Data tables, dashboard cards holding metrics
- Form inputs (the input field itself; the dropdown menu opened from the input is eligible)
- Imagery containers (glass over images blurs the image)
- Anything inside Sanctuary Tech (hard refuse)

### Decision rule

Every glass element in generated markup must answer one of two labels in a comment:

```html
<!-- Liquid Glass: floating nav above scrolling content (chrome layer) -->
<nav class="lg-nav">…</nav>

<!-- Liquid Glass: command palette modal (overlay layer) -->
<div class="lg-modal" role="dialog">…</div>
```

If the comment cannot honestly say "chrome layer" or "overlay layer," the element is not eligible. Refactor to solid.

---

## 5. Variants

Three variants. Token shape:

```yaml
glass:
  blur-sm: 8px      # mobile floor
  blur-md: 12px     # default (matches atmospheric-protocol)
  blur-lg: 20px     # desktop hero
  blur-xl: 24px     # ceiling
  alpha-low: 0.65   # high-contrast surfaces
  alpha-med: 0.80   # default (= atmospheric-protocol surface-glass alpha)
  alpha-high: 0.90  # over variable / user-content background
  border-hairline: "1px solid rgba(255,255,255,0.18)"  # dark mode
  border-hairline-light: "1px solid rgba(0,0,0,0.10)"  # light mode
  shadow-anchor: "0 8px 32px 0 rgba(0,0,0,0.12)"      # mandatory floor
  fallback-bg: "{colors.surface-elev-2}"               # prefers-reduced-transparency

variants:
  regular:   { alpha: alpha-med,  blur: blur-md }   # default
  clear:     { alpha: alpha-low,  blur: blur-md }   # max transparency
  prominent: { alpha: alpha-high, blur: blur-lg }   # desktop hero
```

### Variant selection
- **regular** — default for nav, dropdowns, tooltips, toasts. Use when the background is a controlled gradient or atmospheric backdrop.
- **clear** — for surfaces that must show maximum content behind them (lightbox chrome, sticky video scrubber). Lower alpha trades contrast headroom for transparency.
- **prominent** — desktop hero modals, large overlay panels, surfaces over user-uploaded imagery. Higher alpha + larger blur compensates for unbounded background brightness.

### Token reconciliation note

`surface-glass: rgba(3,5,8,0.80)` from `atmospheric-protocol` corresponds to the `regular` variant's `alpha-med`. `pad-glass: 20px` from `atmospheric-protocol` is the spacing token. The `card-glass` component from `atmospheric-protocol` IS the glass card implementation; this modifier does not replace it. The new modifier adds the variants layer (regular / clear / prominent) and the `prefers-reduced-transparency` fallback on top. Do not invent parallel token names (`liquid-surface`, `glass-padding`, `lg-card`) — reuse the existing vocabulary.

---

## 6. CSS tracks — Tier 1 (basic frosted) + Tier 2 (Apple-ish pseudo-elements)

The CSS tracks are the default implementation paths. Every `effects.liquid-glass: true` build ships at least Tier 1; Tier 2 is the recommended upgrade for **premium surfaces** (hero modals, primary CTAs, signature glass nav pills, marquee cards). Tier 3 (SVG displacement) and Tier 4 (WebGL refraction) live in §6.7 and §7 respectively — those are gated tracks for refraction-driven moments.

**Decision rule per glass element:**
- Default: **Tier 1** — basic frosted, single-layer CSS, ships everywhere
- Element is the page's signature glass moment (hero card, nav pill carrying brand identity, primary CTA): **Tier 2** — adds pseudo-element edge lighting + inner reflection
- Element is a "wow" moment AND the brief explicitly references Apple Liquid Glass / iOS 26 / refraction: **Tier 3** (SVG displacement) — premium-only, gated
- Element is hero canvas with shader-accents budget already spent: **Tier 4** (WebGL) — opt-in, see §7

Mixing tiers is fine and expected — most builds are 80% Tier 1 + 20% Tier 2 + occasional Tier 3 for one signature element.

---

### Tier 1 — Basic frosted glass (single-layer CSS)

The mandatory floor for any `effects.liquid-glass: true` build. Every glass surface ships at least this.

```css
.liquid-glass {
  background: rgba(3, 5, 8, var(--glass-alpha-med));
  -webkit-backdrop-filter: blur(var(--glass-blur-md)) saturate(180%);
  backdrop-filter: blur(var(--glass-blur-md)) saturate(180%);
  border: var(--glass-border-hairline);
  box-shadow: var(--glass-shadow-anchor);  /* MANDATORY */
  border-radius: inherit;
}
```

The `box-shadow` floor is non-negotiable. Without a shadow anchor the glass surface reads as a transparency hole rather than a floating element — Apple's "floating appearance" and the existing `atmospheric-protocol` "MANDATORY shadow anchor" are the same instinct.

The `-webkit-backdrop-filter` prefix ships alongside the unprefixed property. Safari support depends on it.

The `saturate(180%)` is recommended even at Tier 1 — `blur` alone reads like fog; `blur + saturate` reads like glass (industry standard). On dark backgrounds the saturation boost is invisible but helpful for any colour-bearing pixel that bleeds through. On light backgrounds it's mandatory (see § 6.5).

**Brightness / contrast modulation (optional polish at Tier 1, mandatory at Tier 2):**

```css
.liquid-glass {
  /* light context: pull surfaces UP slightly */
  backdrop-filter: blur(18px) saturate(180%) brightness(1.05) contrast(105%);
}
```

`brightness(1.02–1.08)` lifts the glass surface above the backdrop without breaking contrast; `contrast(102–108%)` sharpens the colour bleed. Both are subtle — the difference is visible only when toggled on/off A/B.

### Optional gradient border shell

The optional gradient border shell (from `gradient-tactics.md` Recipe 6) replaces the single-value border on premium surfaces — the 1px `padding: 1px` shell technique applies here identically. Use it on hero modals, premium nav pills, and any glass surface where a hairline gradient frame ("highlights along glass edges") is part of the brief. Do not combine with a `border: 1px solid` on the inner — pick one or the other.

---

### Tier 2 — Apple-ish glass (CSS + pseudo-elements)

The recommended upgrade for signature glass moments. Adds edge lighting + inner reflection via `::before` and `::after`, producing the "skin" effect that distinguishes premium glass from basic frosted. Pure CSS — no SVG, no WebGL, no JS. Costs one extra paint per element.

#### When to escalate from Tier 1 to Tier 2

- The element carries brand identity (signature nav pill, hero card)
- The element sits over a busy / colourful backdrop (atmosphere, gradient mesh, image) — pseudo-element highlights READ here
- The brief uses words like "Apple-like", "premium", "polished", "iOS-style"
- The element is a primary CTA where one extra paint cycle is acceptable for visual quality

**Do NOT use Tier 2 for:**
- Body copy containers (forbidden across all tiers — see § 4)
- Dashboard data cells (forbidden across all tiers)
- Element budgets exceeded (Tier 2 counts double — 1 element = 1 backdrop-filter + 2 pseudo-element paints)

#### Mandatory base pattern

```css
.liquid-glass--tier2 {
  position: relative;
  overflow: hidden;
  isolation: isolate;  /* MANDATORY — prevents pseudo-elements from leaking blend modes */

  /* base layer: subtle gradient instead of flat tint */
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.35),
      rgba(255, 255, 255, 0.08)
    );

  -webkit-backdrop-filter: blur(22px) saturate(180%) brightness(1.05) contrast(105%);
  backdrop-filter: blur(22px) saturate(180%) brightness(1.05) contrast(105%);

  border: 1px solid rgba(255, 255, 255, 0.38);
  border-radius: inherit;

  /* MANDATORY shadow stack: drop + inner top highlight + inner bottom shade */
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.22),
    inset 0 1px 2px rgba(255, 255, 255, 0.75),
    inset 0 -8px 20px rgba(255, 255, 255, 0.08);
}

/* Edge lighting — top-left corner radial highlight (the "lit edge") */
.liquid-glass--tier2::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    radial-gradient(
      circle at 30% 15%,
      rgba(255, 255, 255, 0.75),
      transparent 28%
    ),
    linear-gradient(
      120deg,
      rgba(255, 255, 255, 0.28),
      transparent 40%,
      rgba(255, 255, 255, 0.12)
    );
  mix-blend-mode: screen;
  opacity: 0.65;
}

/* Inner reflection edge — softens the rim, prevents the edge looking "stamped" */
.liquid-glass--tier2::after {
  content: "";
  position: absolute;
  inset: 1px;  /* sits 1px inside the border so it reads as a separate inner ring */
  border-radius: inherit;
  pointer-events: none;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.25),
    inset 0 0 30px rgba(255, 255, 255, 0.12);
}
```

**Critical implementation rules for Tier 2:**

1. **`isolation: isolate` on the host is mandatory.** Without it, `mix-blend-mode: screen` on `::before` leaks to ancestor stacking contexts and produces unpredictable composites. This is the single most common Tier 2 bug.

2. **`overflow: hidden` is mandatory.** Without it, the pseudo-elements paint outside the rounded corners.

3. **`pointer-events: none` on both pseudo-elements** so they don't interfere with click / hover / focus on the host element.

4. **The host's `background` MUST be a gradient, not a flat rgba.** A flat tint inside Tier 2 fights the `::before` highlight — they look layered instead of fused. Subtle 135deg gradient (white→white at different alphas) is the canonical pattern.

5. **`::after` `inset: 1px`** (not `0`) — this places the inner ring just inside the host border, creating the "double-edge" reflection effect. Using `0` collapses the ring into the border and loses the depth.

#### Tier 2 + light-mode interaction

In light mode, the pseudo-element highlights still work, but the `mix-blend-mode: screen` on white-on-white reads weakly. Two adaptations:

- Drop `::before` opacity from `0.65` → `0.45` in light mode (white highlight on white-ish backdrop is too bright otherwise)
- Optionally swap `mix-blend-mode: screen` → `mix-blend-mode: soft-light` in light mode for a more subtle "lifted" feel

```css
:root[data-theme="light"] .liquid-glass--tier2::before {
  opacity: 0.45;
  mix-blend-mode: soft-light;
}
:root[data-theme="light"] .liquid-glass--tier2 {
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.55),
      rgba(255, 255, 255, 0.20)
    );
  border-color: rgba(20, 24, 31, 0.10);  /* dark hairline per § 6.5 Rule 2 */
  box-shadow:
    0 1px 2px rgba(20, 24, 31, 0.06),
    0 12px 32px rgba(20, 24, 31, 0.10),
    inset 0 1px 2px rgba(255, 255, 255, 0.85),
    inset 0 -8px 20px rgba(20, 24, 31, 0.04);
}
```

#### Tier 2 typography on glass

Same rules as Tier 1 (font-weight bump 400→500, optional text-shadow on small labels), but Tier 2 surfaces tolerate slightly heavier display weights because the edge lighting compensates for the additional visual mass.

#### Tier 2 anti-patterns

- **Multiple `::before` / `::after` layers stacked vertically** — the "more pseudo-elements = more glass" intuition is wrong. The edge-lighting + inner-reflection pair IS the recipe; adding more layers degrades performance and rarely improves the look.
- **`mix-blend-mode: multiply` on `::before` over a white surface** — produces near-black holes instead of highlights. `screen` (dark backdrop) or `soft-light` (light backdrop) only.
- **Animating the pseudo-element gradients** — same paint-cost penalty as animating `backdrop-filter`. Animate the host's `transform` / `opacity` only.

### prefers-reduced-transparency fallback

Non-optional. Users who set this preference have a strong reason (reduced visual noise, reading clarity).

```css
@media (prefers-reduced-transparency: reduce) {
  .liquid-glass {
    background: var(--glass-fallback-bg);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}
```

Mechanical check: `grep "prefers-reduced-transparency" <stylesheet>` must return ≥1 match per glass component.

### prefers-reduced-motion fallback

Required for any morphing or transition applied to glass elements (e.g., menu open/close, modal entry).

```css
@media (prefers-reduced-motion: reduce) {
  .liquid-glass,
  .liquid-glass * {
    transition: none !important;
    animation: none !important;
  }
}
```

### Anti-pattern: do not animate `backdrop-filter`

Animating `backdrop-filter` forces the browser to re-rasterize the blurred region every frame. The visual result is GPU-intensive jank. Animate `opacity` or `transform` instead. The morphing transition (e.g., dropdown reveal) animates the wrapper's opacity/transform; the blur itself is static.

Mechanical check: `grep "transition.*backdrop-filter\|@keyframes.*backdrop" <stylesheet>` must return zero matches.

### Typography on glass

Glass surfaces benefit from bumping text one font-weight tier (400 → 500, 500 → 600). The blur backdrop reduces apparent text contrast, and increased weight compensates without failing WCAG numeric tests. Apply at the component level, not globally:

```css
.liquid-glass { /* ... */ }
.liquid-glass > * { font-weight: 500; }  /* was 400 in body */
.liquid-glass strong, .liquid-glass h1, .liquid-glass h2 { font-weight: 600; }
```

For small labels (under 14px) on glass, an optional text-shadow improves edge definition without distorting the glyph:

```css
.liquid-glass .label-sm {
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.15);
}
```

### Element budget per viewport

Counted by visible-on-screen, not total in DOM. Sticky nav + modal open + tooltip = 3 already.

- **Mobile (≤768px):** ≤3 glass surfaces visible simultaneously.
- **Tablet (769–1199px):** ≤5.
- **Desktop (≥1200px):** ≤8.

### Hardware acceleration hint

Apply `transform: translateZ(0)` or `will-change: transform` to glass elements that animate position. Do not apply `will-change: backdrop-filter` — there is no win, and it pins GPU memory.

### Cross-references

- `gradient-tactics.md` § Recipe 6 — gradient border shell for glass cards.
- `references/styles/atmospheric-protocol.md` § Glass nav-pill — the canonical implementation pattern.

---

## 6.5 Light-mode adaptation — the 5 mandatory rules

The default CSS track in §6 is calibrated for **dark surfaces**. Light-mode glass is a different beast: the dark contract (translucent dark tint + faint white hairline + 16px blur) inverts to invisibility on light backgrounds. Every dark-mode token has a light-mode counterpart that is **not symmetrical** — light needs more opacity, more blur, more saturation, and a darker edge.

These 5 rules are mandatory whenever a glass surface ships in light mode. Skipping any one produces glass that "compiles but doesn't read":

### Rule 1 — Background tint MUST be opaque enough to read (≥ 0.55 alpha)

Dark glass works at `rgba(near-black, 0.04–0.10)` because the dark surface itself contributes the visual mass. Light glass at `rgba(white, 0.05)` is invisible — the light page bleeds through unchanged. Light-mode glass needs `rgba(255, 255, 255, 0.55–0.72)` minimum. Below 0.55, the surface boundary disappears and the build looks like a layout bug.

```css
/* Wrong — light glass at dark-mode opacity */
.card[data-theme="light"] { background: rgba(255, 255, 255, 0.08); }

/* Right — light glass at usable opacity */
.card[data-theme="light"] { background: rgba(255, 255, 255, 0.62); }
```

Acceptable range: 0.55 (subtle, requires busy backdrop) → 0.78 (near-opaque, safe on any backdrop). Above 0.78 the glass effect is no longer visible — just use a solid colour and skip `backdrop-filter`.

### Rule 2 — Hairline border MUST flip to dark (rgba(near-black, 0.08–0.14))

The dark-mode hairline is `rgba(255, 255, 255, 0.05)` — a faint white edge that catches light against a dark surface. Apply that hairline on a light page and **the edge disappears entirely** (white on light = invisible). Light-mode hairlines must be **dark**:

```css
/* Wrong — white hairline carried over to light mode */
.card[data-theme="light"] { border: 1px solid rgba(255, 255, 255, 0.05); }

/* Right — dark hairline, scaled for visibility on light */
.card[data-theme="light"] { border: 1px solid rgba(20, 24, 31, 0.10); }
```

Acceptable range: 0.08 (whisper) → 0.16 (assertive). Above 0.16 the edge stops reading as a hairline and starts reading as a structural border — a different visual register.

### Rule 3 — Blur radius MUST increase (28–40px on light, vs 16–24px on dark)

Backdrop-blur on dark works at 16px because dark surfaces accept low-information blur and still read as "atmospheric." On light, the same 16px produces a weak, wishy-washy effect — the eye reads it as "out of focus" rather than "frosted glass." Light needs a stronger blur to commit to the metaphor:

```css
/* Light-mode glass blur — stronger than dark */
.card[data-theme="light"] {
  backdrop-filter: blur(28px) saturate(1.55);
  -webkit-backdrop-filter: blur(28px) saturate(1.55);
}
```

Acceptable range: 24px (minimum for light-mode legibility) → 40px (marquee modal moments only — performance ceiling). Anything below 24px on light reads as "blurry photo," not "glass."

### Rule 4 — Saturate boost is MANDATORY on light (1.45–1.65); brightness + contrast are recommended polish

This is the rule most often skipped. Backdrop-blur on its own desaturates the underlying gradient — colour pulls *out* through the blur instead of *through* it. On dark, the desaturation is invisible (everything's near-black anyway). On light, desaturation makes the glass look **grey** instead of "frosted-with-colour-bleeding-through." Mandatory `saturate(1.45–1.65)` restores the colour pull:

```css
/* Wrong — light glass without saturation boost reads as grey film */
.card[data-theme="light"] { backdrop-filter: blur(28px); }

/* Better — saturate restores colour pull */
.card[data-theme="light"] { backdrop-filter: blur(28px) saturate(1.55); }

/* Best — saturate + brightness + contrast trio (industry standard) */
.card[data-theme="light"] {
  backdrop-filter: blur(28px) saturate(1.55) brightness(1.05) contrast(105%);
  -webkit-backdrop-filter: blur(28px) saturate(1.55) brightness(1.05) contrast(105%);
}
```

**`brightness(1.02–1.08)`** lifts the glass surface above the backdrop without breaking contrast. The glass appears to "float" with a subtle inner glow, instead of sitting flat against the page. Higher values (1.10+) start washing colours out — stay within 1.02–1.08.

**`contrast(102–108%)`** sharpens the colour bleed coming through the blur. On a dimmed atmosphere or pastel backdrop the difference is the line between "fogged window" and "frosted glass." Avoid above 110% — colour blocks start posterising.

Together the saturate + brightness + contrast trio is the industry-standard polish chain (`saturate(180%) brightness(1.05) contrast(105%)` is the canonical Apple-adjacent recipe). On dark mode, only `saturate()` is necessary; brightness and contrast are no-ops because dark glass has no colour to lift or sharpen. On light mode, the full trio is recommended for any premium surface (Tier 2+).

### Rule 5 — Backdrop MUST be busy (gradient / mesh / image — never flat white)

This rule is the single biggest cause of broken light-mode glass: the page underneath is `background: white` and the glass has nothing to refract. The result is a faintly-tinted rectangle that reads as a layout artefact, not as glass.

**Light-mode glass requires a visually-active background:**
- Gradient (single linear or radial counts; multi-stop mesh ideal)
- Photographic image
- Coloured atmosphere (Atmospheric Protocol's Bloom, Flow, Particle backdrops all qualify — see `gradient-tactics.md`)
- Pattern (subtle dot-grid, hairline mesh — anything that varies pixel-to-pixel)

If the brief or the chosen library does NOT support a busy backdrop, **light-mode glass cannot ship**. Either:
- Switch to a backdrop-supporting library (Atmospheric Protocol, Warm Editorial with gradient hero, Creative Studio with full-color media), OR
- Drop the glass treatment for the light variant — solid card with hairline border is correct here, not "glass that doesn't work"

### Quick reference — light vs dark token deltas

| Token | Dark default | Light derivation | Why |
|---|---|---|---|
| `background` alpha | 0.04–0.10 | **0.55–0.72** | Light glass evaporates below 0.55 |
| `border` colour | `rgba(255,255,255,0.05)` | **`rgba(20,24,31,0.10)`** | White hairline invisible on light |
| `backdrop-filter` blur | 16–24px | **28–40px** | Light needs stronger commitment |
| `backdrop-filter` saturate | n/a | **`saturate(1.55)`** | Restores colour pull lost to desaturation |
| Backdrop requirement | any | **busy (gradient/image/mesh)** | Glass on flat white = invisible |
| Text on glass | white / near-white | **`#14181F` (near-black)** | Contrast ratio inversion |
| `box-shadow` for lift | dark drop | **white inset top + dark drop** | Inset white edge gives "lifted glass" feel |

### Fallbacks (light-mode-specific)

The `prefers-reduced-transparency` block needs explicit light handling — the fallback surface should be **opaque white** (`#FFFFFF` or near-white), not the dark fallback:

```css
@media (prefers-reduced-transparency: reduce) {
  .card[data-theme="dark"] { background: var(--color-surface-card-dark); }
  .card[data-theme="light"] {
    background: #FFFFFF;       /* opaque, not translucent */
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    border-color: rgba(20, 24, 31, 0.12);
  }
}
```

### Compatibility matrix override for light-mode

The matrix in §3 is calibrated against dark-mode glass behaviour. When a style ships light-mode glass:

- **Native tier (Atmospheric Protocol, Adaptive AI Console, Creative Studio):** light-mode derivation is permitted but follows §6.5 rules. Document the divergence in DESIGN.md provenance.
- **Conditional tier:** the per-style scope constraints from §3 still apply — light-mode does NOT widen the eligible elements list. Light-mode dropdowns are still OK; light-mode glass dashboard cards are still forbidden.
- **Refused tier:** light-mode does NOT unlock the refusal. The single-element override path (§9) applies identically.
- **Sanctuary Tech — hard refuse stands** in light mode too. Light-mode glass on Sanctuary is doubly bad — the warm muted tones don't host glass at any opacity tier.

### Rule 6 — Interactive states must be re-derived per theme (companion rule)

The 5 rules above cover **glass surfaces**. They do NOT cover the **interactive controls sitting on those surfaces** — buttons, links, form inputs, toggles, chips, badges. A primary CTA whose dark-mode CSS contains `color: #000000` will ship invisibly broken in light mode (dark text on dark pill, because the button background follows `--color-text-primary` which inverts but the hardcoded text colour does not).

This is the single most common ship-defect when adding a light derivation to a dark style — the surfaces look right, the typography looks right, but a primary action is unreadable. **See `references/build-tactics.md` § Tactic 18 — Interactive state coverage in derived themes** for the full audit + override pattern. Mandatory whenever a build ships glass in both light and dark.

### Cross-references

- `references/styles/atmospheric-protocol.md` § Light-Mode Interpretation (Advanced Derivation) — the reference build.
- `_tests/design-skill-lab/oneshot/atmospheric-protocol-light-dark.html` — canonical implementation with toggle.
- `style-reviews/effects/liquid-glass.md` § Light-mode checks — the verification checklist.
- `references/build-tactics.md` § Tactic 18 — Interactive state coverage when deriving a new theme; required companion to this section.

---

## 6.7 SVG displacement track — Tier 3 (gated, premium-only)

The CSS tracks (Tier 1 + Tier 2) produce **frosted** glass — blur, saturate, edge lighting. They do NOT produce **refraction** — the optical effect of light bending through a prism. Refraction is what makes Apple's Liquid Glass feel like real glass instead of frosted plastic: pixels behind the surface appear shifted, often with subtle chromatic separation (red / green / blue channels offset by 1–2px).

Tier 3 introduces refraction via SVG filters — specifically `feDisplacementMap` driven by a noise or gradient source, optionally combined with `feColorMatrix` for chromatic aberration. It is significantly heavier than Tiers 1+2 (filter chain runs per-paint) and brittle on Safari, but it ships pure CSS+SVG with no JS or WebGL bundle. Use it sparingly — typically one element per page, the marquee glass moment.

### When to escalate from Tier 2 to Tier 3

- The brief explicitly references "Apple Liquid Glass," "iOS 26," "refraction," "prismatic edge," or "chromatic aberration"
- The element is the page's single signature glass moment (one hero CTA, one nav pill, one floating control) — never multiple Tier 3 elements per page
- The host style is in the Native or Conditional tier of the compatibility matrix (see § 3) AND the element is on the eligible list (see § 4)
- Performance budget allows: target devices include modern desktops; Safari ≥17 fallback acceptable

### Auto-refuse cases for Tier 3

- More than ONE Tier 3 element per page — escalate to user, propose Tier 2 for all-but-one
- Sanctuary Tech in trauma-informed mode — hard refuse identical to Tier 4 (cognitive load + thermal)
- Mobile-first build with no desktop tier — Tier 3 is too expensive on low-end mobile GPUs
- Element budget at Tier 1+2 already saturated — Tier 3 counts as 2 elements toward budget

### Mandatory base pattern

```html
<!-- Place this SVG once in the document, ideally near the closing </body> -->
<svg width="0" height="0" style="position: absolute" aria-hidden="true">
  <defs>
    <filter id="glass-refract" x="-20%" y="-20%" width="140%" height="140%">
      <!-- Noise source for displacement -->
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.018" numOctaves="2" seed="3" result="noise"/>
      <!-- Gentle blur on the noise so displacement feels organic, not pixelated -->
      <feGaussianBlur in="noise" stdDeviation="2" result="noise-blur"/>
      <!-- Displace SourceGraphic using the blurred noise as a map -->
      <feDisplacementMap in="SourceGraphic" in2="noise-blur" scale="8" xChannelSelector="R" yChannelSelector="G" result="displaced"/>
      <!-- Optional: chromatic aberration via channel offset -->
      <feColorMatrix in="displaced" type="matrix"
        values="1 0 0 0 0
                0 1 0 0 0
                0 0 1 0 0
                0 0 0 1 0"/>
    </filter>
  </defs>
</svg>
```

```css
.liquid-glass--tier3 {
  /* Inherits everything from Tier 2 (recommended host pattern) */
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.30), rgba(255, 255, 255, 0.06));
  -webkit-backdrop-filter: blur(20px) saturate(180%) brightness(1.05) contrast(105%);
  backdrop-filter: blur(20px) saturate(180%) brightness(1.05) contrast(105%);
  border: 1px solid rgba(255, 255, 255, 0.38);
  border-radius: inherit;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.22),
    inset 0 1px 2px rgba(255, 255, 255, 0.75),
    inset 0 -8px 20px rgba(255, 255, 255, 0.08);

  /* The Tier 3 escalation: SVG displacement filter on the host */
  filter: url(#glass-refract);
}

/* Pseudo-elements from Tier 2 still apply — edge lighting + inner reflection */
.liquid-glass--tier3::before { /* … same as Tier 2 ::before … */ }
.liquid-glass--tier3::after  { /* … same as Tier 2 ::after  … */ }
```

### Critical implementation rules for Tier 3

1. **The SVG `<filter>` must exist in the document.** A `filter: url(#glass-refract)` reference to a non-existent ID silently no-ops — Tier 3 degrades to Tier 2 without warning. Verify the SVG is present before delivery.

2. **`feTurbulence baseFrequency` controls the displacement texture's grain.** Lower values (0.005–0.015) = wavy, organic. Higher values (0.04–0.10) = tight, prismatic. Pick deliberately — wavy fits hero glass, tight fits chromatic-aberration moments.

3. **`feDisplacementMap scale` is the displacement strength.** 4–10 = subtle (real-glass-like). 12–20 = strong (psychedelic, only intentional). Above 20 = broken / unreadable text underneath.

4. **`filter` applies to the ELEMENT itself, not the backdrop behind it.** This is the fundamental SVG limitation: `feDisplacementMap` distorts the host's own pixels, not the page underneath. To distort the backdrop (true Apple-like refraction), you need either (a) a duplicated background snapshot, (b) WebGL, or (c) accept that Tier 3 distorts the glass surface markings (gradient, edge highlights) — which still reads as "glass" because the human eye associates surface distortion with refraction.

5. **Safari < 17 silently fails on `feDisplacementMap` chained with `feTurbulence`.** Tier 3 must include a Safari-version fallback that downgrades to Tier 2:
   ```css
   @supports not (filter: url(#test-id)) {
     .liquid-glass--tier3 { filter: none; }  /* falls back to Tier 2 base */
   }
   ```

6. **`prefers-reduced-motion` MUST disable the displacement filter.** Animated displacement (changing `feDisplacementMap scale` over time) is a vestibular trigger; static displacement is fine but must still be opt-out.
   ```css
   @media (prefers-reduced-motion: reduce) {
     .liquid-glass--tier3 { filter: none; }
   }
   ```

7. **Element budget for Tier 3:** ONE per page. Multiple Tier 3 elements compound the filter cost (each `feTurbulence` runs independently) and produce GPU thermal throttling on mid-range mobile within 30 seconds.

### Tier 3 + light-mode interaction

Refraction reads strongest over coloured / busy backdrops. On light mode with Atmospheric Protocol's dimmed atmosphere, Tier 3 still works but the chromatic effect is subtle. Adjust:
- `feDisplacementMap scale="6"` (down from 8) — light backdrops show displacement more sharply
- Consider raising `feTurbulence baseFrequency` slightly (0.015 → 0.020) for a tighter prismatic grain that catches the eye on lighter surfaces

### Tier 3 anti-patterns

- **Multiple Tier 3 elements per page** — 1 only. Two = forbidden. Three = budget catastrophe.
- **`filter: url(#glass-refract)` on body or full-screen overlays** — applies the filter chain to the entire viewport per paint. Performance disaster.
- **Animating `feDisplacementMap scale`** — looks dazzling for 2 seconds, jank for the next 30. Static only.
- **Tier 3 on text-bearing surfaces** — readable text + refraction = unreadable text. Tier 3 belongs on chrome (nav pills, controls, floating cards), never on prose.

### Tier 3 cross-references

- `gradient-tactics.md` § Recipe 6 — gradient border shell pairs with Tier 3 for premium edge frame.
- LogRocket "Liquid Glass with SVG filters" — external reference for `feDisplacementMap` chains.
- Apple's developer docs on Liquid Glass design (the Tier 3 spec is the closest CSS-only approximation).

---

## 7. WebGL / SDF refraction track — Tier 4 (gated, hero/experimental only)

### Gating rule

Both conditions must be true to load this track:

1. `style-tuning.axes.dimension.value === 'shader-accents'`
2. `effects.liquid-glass === true`

If either is false, skip this section entirely. The CSS track ships alone.

### Auto-refuse cases

- **Mobile-first projects.** Refuse with: "WebGL refraction track requires desktop-first layout or explicit mobile opt-in — current project is mobile-first, falling back to CSS track."
- **Sanctuary Tech.** Hard refuse, no override path.
- **`dimension: 3d-scene` already active.** Refuse with: "WebGL refraction inside an existing 3D scene is double-spend on the GPU; not coherent. Falling back to CSS track."

### The four mandatory failure-mode guards

These guards are defined in `references/webgl-3d-tactics.md` § The four mandatory failure-mode guards — cross-reference that file for the full code; do not re-implement here. The WebGL refraction track inherits them identically:

- [ ] **Guard 1 — WebGL feature detect.** With DOM fallback. If `hasWebGL()` returns false, the glass surface renders as the CSS track instead.
- [ ] **Guard 2 — Reduced motion.** Static frame on `prefers-reduced-motion: reduce`. The shader's RAF loop pauses; the last rendered frame stays. Listen for `change` event.
- [ ] **Guard 3 — DOM mirror for SEO / a11y AND legibility scrim.** The canvas is `aria-hidden="true"`; the real headline, body, and CTAs exist in DOM behind the refractive surface. If the canvas is fullscreen-fixed, ship the legibility scrim from `webgl-3d-tactics.md`.
- [ ] **Guard 4 — Load timeout.** 8 seconds. If the shader hasn't initialised in 8s, the CSS track renders instead.

### Minimal shader recipe — SDF + refraction

Following the SDF refraction pattern. The shader samples a DOM-captured background texture and offsets the sample coordinate proportional to the signed distance from the element edge.

```glsl
// SDF refraction — following Muggleee's pattern
// st = UV coords, sd = signed distance to element edge
vec2 offset = mix(vec2(0.0), normalize(st) / sd, length(st));
// Apply offset to sample the DOM-captured background texture
vec4 refractedColor = texture2D(uBackground, vUv + offset * uStrength);
```

Line-by-line:

- `normalize(st)` — unit vector from element centre to current pixel; the refraction direction (inward toward centre at edge, zero at centre).
- `1.0 / sd` — attenuation by signed distance; the offset grows as the pixel approaches the edge, simulating the wider refraction angle near a glass rim.
- `length(st)` — radial falloff from centre; the `mix()` blends from no-offset at centre to full-offset at edges.
- `uStrength` — uniform multiplier the build can tune per surface variant. Regular ≈ 0.02, clear ≈ 0.04, prominent ≈ 0.06 (relative to UV space, not pixels).

### DOM-sampling strategy

Use `html2canvas` or equivalent to capture a canvas snapshot of the page behind the glass element. The capture is a one-shot image (or refresh-on-scroll if the underlying content moves). Pass it as a sampler2D uniform.

**CORS warning.** CORS-tainted canvases (cross-origin images, iframes without CORS headers) will throw a security error and `getImageData()` / `texImage2D()` from the canvas will fail. Test with `crossOrigin: 'anonymous'` on all background assets. If a tainted-canvas error occurs, fall back to the CSS track and record the fall-back in provenance.

### Bundle weight ceiling

≤200 KB compressed (matches `webgl-3d-tactics.md` shader-accents tier). The shader, the DOM-capture library, and the uniforms manager combined. If the build exceeds 200 KB, drop the refraction track and ship CSS-only.

### What does NOT ship at this tier

- No fluid morphing between surfaces (a tooltip morphing into a menu via shader). That is `3d-scene` territory and out of scope.
- No physics-driven liquid motion. The shader is static-camera, scroll/hover-reactive at most.
- No multi-pass post-processing. One pass, one merged effect.

---

## 8. Tier-coupling

Glass interacts with the existing style-tuning axes as follows:

| Axis | Interaction with liquid-glass |
|------|------------------------------|
| `trauma-informed` | Hard-refuse — glass adds cognitive load and visual complexity incompatible with trauma-informed design principles. Mirrors the `webgl-3d` rule. |
| `motion: low` | Glass allowed; transitions must be CSS-only (no `backdrop-filter` transitions). Static glass only. |
| `motion: medium` | Glass allowed; morphing transitions permitted but not on `backdrop-filter`. Cap morph duration ≤300ms. |
| `motion: high` | Glass allowed; GSAP morphing on glass elements OK, but animate `transform` / `opacity`, NOT `backdrop-filter`. |
| `dimension: none` | CSS track only. |
| `dimension: shader-accents` | CSS track default; WebGL refraction track opt-in available. |
| `dimension: 3d-scene` | Auto-refuse WebGL refraction track — `3d-scene` owns the WebGL context. CSS track only. |
| `page-load: branded-intro` | Glass surfaces must be invisible during loader; fade-in after `.js-ready` class is set on body. Animate opacity, never `backdrop-filter`. |

---

## 9. Override protocol for refused styles

### Six non-Sanctuary refused styles

For Neo-Brutalist, Memoir Blog, Basalt E-Commerce, Spritify, Playful Bento, and Warm Editorial, a **single-element rule** applies. Up to ONE glass element is permitted per build, for isolated use cases (a floating tooltip, a video scrubber control, a single sticky CTA). The element must be true chrome — never structural, never primary-content-bearing.

If the user requests ≥2 glass elements on a refused style, escalate:

> "This style system uses [solid colour blocks / paper tones / brutalist surfaces] as its visual foundation, which is incompatible with repeated glass surfaces. Either switch to [nearest native style — typically Atmospheric Protocol or Adaptive AI Console] or limit glass to a single isolated element."

### Sanctuary Tech — hard refuse

No override path. If the user asks for glass inside Sanctuary Tech:

> "Liquid Glass is not available for this style. The trauma-informed design contract prohibits visual complexity and motion effects that increase cognitive load. Recommend staying with solid surfaces."

Record the refusal in provenance:

```yaml
provenance:
  effects:
    liquid-glass: false
    forced-override: true
    forced-override-reason: sanctuary-tech-trauma-informed
    user-requested: true
```

### Provenance template

Every build using the modifier records its decisions:

```yaml
provenance:
  effects:
    liquid-glass: true
    variant: regular              # regular | clear | prominent
    track: css                    # css | webgl-refraction
    override: single-element-rule # only present if refused-style override
    override-element: "floating video scrubber"
    override-rationale: "isolated chrome control, not structural glass"
    detection-trigger: "user said 'make the nav glass'"
```

When the WebGL track was attempted but fell back to CSS:

```yaml
provenance:
  effects:
    liquid-glass: true
    variant: prominent
    track: css
    track-fallback: true
    track-fallback-reason: "tainted-canvas error on hero background image"
```

---

## 10. Anti-patterns

❌ **Glass on body content / reading column.** Translucency under scrolling prose fails contrast at the worst scroll position (a bright background pixel behind dark text). Use solid surfaces for all body copy containers. Mechanical check: every `.liquid-glass` element must NOT contain a `<p>`, `<article>`, or `prose`-class child wider than 60ch.

❌ **Glass over animated or video backgrounds without a per-frame contrast guard.** A static contrast check does not cover the worst-case video frame; video can flash bright and drop text contrast to 1.4:1 in a single frame. Add a scrim (`background: linear-gradient(transparent, rgba(0,0,0,0.4))`) underneath the glass so the floor is always above 4.5:1, or lock the video brightness, or use a solid surface.

❌ **Animating `backdrop-filter`.** Every interpolation frame forces the browser to re-rasterize the blurred region. The visual result is GPU-intensive jank. Animate `opacity` or `transform` instead. Mechanical check: `grep "transition.*backdrop-filter\|@keyframes.*backdrop" <file>` must return zero matches.

❌ **Stacking ≥2 glass surfaces on a refused style.** Single-element rule means one. Two is a pattern; a pattern implies the style system has glass in it, which the refused tier explicitly rejects. Escalate to style switch.

❌ **Missing `prefers-reduced-transparency` fallback.** The `@media (prefers-reduced-transparency: reduce)` block with a solid `fallback-bg` is non-optional. Users who set this preference have a strong reason (reduced visual noise, reading clarity). Mechanical check: `grep "prefers-reduced-transparency" <stylesheet>` must return ≥1 match per glass component.

❌ **Glass on dashboard data cells.** Translucency makes numeric values ambiguous — the eye cannot distinguish whether the background texture is part of the metric or behind it. Data cells require opaque, high-contrast surfaces. Mechanical check: no `.liquid-glass` ancestor of `<td>`, `[role="cell"]`, or `data-metric`.

❌ **WebGL refraction without DOM mirror.** The canvas is `aria-hidden="true"` — screen readers and crawlers see nothing. The headline, body, and CTAs behind the glass MUST exist in DOM. Mechanical check: every canvas element with a glass shader must have a DOM sibling containing the real content; the canvas's accessible name is empty.

❌ **Opacity below alpha-low (0.65) on any glass surface holding interactive content.** At 0.5 or lower, the glass surface fails to read as a container — interactive elements appear to float without a parent. The `alpha-low` floor is the minimum for perceived containment. Tooltip-only chrome may go lower; anything containing a button, input, or link must respect the floor.

❌ **Glass over user-uploaded imagery without a fallback contrast overlay.** User content is unbounded — the next uploaded image may be pure white. Either ship a contrast overlay (`linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.5))`) under the glass, or use the `prominent` variant (alpha-high), or refuse glass on that surface.

❌ **Glass on a flat or near-solid background.** A glass surface needs visual complexity behind it to read as glass — over a flat backdrop, the blur reads as a darker rectangle, not a translucent material. Either ensure the backdrop has gradient/photographic/atmospheric variation (atmospheric-protocol's load-bearing atmosphere is the canonical pairing), or refuse glass on that surface and use a solid card. Mechanical check: visually inspect the area behind every `.liquid-glass` element — if it's a single flat colour or a 2-stop linear gradient, glass is wrong.

❌ **Inventing parallel token names.** `liquid-surface`, `glass-padding`, `lg-card`, `glass-blur-default` — every parallel name is a vocabulary fork that breaks cross-style consistency. Reuse `surface-glass`, `pad-glass`, `card-glass` from `atmospheric-protocol`; add only the variant layer (`alpha-low/med/high`, `blur-sm/md/lg/xl`, `regular/clear/prominent`).

---

## 11. Cross-references

- `references/styles/atmospheric-protocol.md` — `surface-glass`, `pad-glass`, `card-glass` tokens are the canonical source. The modifier reuses, not replaces, these. The "Glass nav-pill, fixed centred" signature pattern is the canonical implementation example.
- `references/styles/atmospheric-protocol.design.md` — exact YAML token values for `surface-glass: rgba(3,5,8,0.80)`, `pad-glass: 20px`, `card-glass.shadow: {shadows.card-soft}`.
- `references/gradient-tactics.md` § Recipe 6 — gradient border shell for premium glass surfaces (1px padding shell, inner radius = outer radius − padding).
- `references/webgl-3d-tactics.md` § The four mandatory failure-mode guards — WebGL refraction track inherits these identically. Do not re-implement.
- `references/webgl-3d-style-fit.md` — `dimension: shader-accents` tier definition; the prerequisite for the WebGL refraction track.
- `references/style-tuning.md` — `effects.liquid-glass` boolean is set by Phase 1 detection; axis 10 `dimension` determines which track is available.
- `references/style-reviews/effects/liquid-glass.md` — the Phase 4 review file for this modifier (loads alongside the chosen style's review).
- `SKILL.md` — Steps 1.5 (detection), 2.6 (compatibility check), 3.0.10 (load this file), 4.5b (load review file) reference this modifier.
