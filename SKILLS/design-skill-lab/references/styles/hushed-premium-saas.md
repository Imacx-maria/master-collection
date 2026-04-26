# Hushed Premium SaaS

The inverse of bold-display SaaS. Where most modern product pages reach for weight 700–900 to demand attention, Hushed Premium SaaS reaches for weight 200–300 — light, almost whisper-thin display typography that earns trust through quietness rather than volume. Inspired by ElevenLabs' approach to voice AI: the page reads as a premium audio brochure where lightness is confidence, not weakness.

## Best for

- Voice / audio AI products (ElevenLabs-class)
- Premium consumer tech (Apple-adjacent register)
- Refined SaaS launch pages and landing surfaces
- Boutique creator tools, premium productivity, design tools
- Audio / music / podcast platforms
- Dev-tool launches with a consumer-grade aesthetic
- Any product whose voice should be "calm authority" rather than "loud announcement"

**Avoid for:**
- Bold disruptive startups → use Bold Grid Manifesto (Neo-Brutalist)
- Kids / family products → use Spritify or Approachable Bento Trust
- Conservative legal / finance → use Institutional Serif Advisory or Quiet Editorial Authority
- Crisis / trauma-sensitive content → use Calm Secure Monospace
- Photography-driven hospitality → use Private Client Luxury

## The defining choice — light as the hero weight

Almost every other style in the library uses weight 400–900 for display. This style uses weight **200–300**. That single inversion is the brand. If a future revision asks "should we make the headlines bolder for more impact?" — the answer is no. The lightness IS the impact, in the same way that a whisper across a quiet room cuts through more than a shout.

## Display Typography & Hero Patterns

Three-family system with disciplined roles:

- **Display family — Waldenburg (proprietary) or Manrope (free proxy) at weight 200–300.** Whisper-thin, ethereal headlines. Negative letter-spacing −0.018em to −0.02em. Line-height tight (1.05–1.15) but not condensed — light weight at tight leading reads as poetic, not poster-like.
- **Body — Inter at weight 400 (regular) and 500 (medium).** Positive letter-spacing **+0.14px to +0.18px** at body sizes. This positive tracking is the signature reading texture. It contrasts deliberately with the display's negative tracking.
- **Bold accent — WaldenburgFH or Manrope at weight 700 uppercase, 14px, with 0.7px letter-spacing.** Reserved for the one place the type system raises its voice — typically a single CTA button or category label per page. Use sparingly; if you find yourself reaching for it in three places, demote at least two.
- **Mono — Geist Mono at relaxed line-height (1.85)** for code blocks, eyebrows, and technical metadata. Unhurried, never hurried.

**Hero patterns by page type:**

- **Product launch** — `display-xl` (96px Manrope 200) brand declaration in 1–2 lines, line-height 1.05. `body-lg` (20px Inter 400) subline below. Black pill primary + warm-stone secondary CTA. Stat ribbon with `display-lg` numbers (40–56px Manrope 200) on a 3-column grid above the fold.
- **Landing page** — Same pattern, optionally with a hero illustration / product screenshot below the actions. Section padding generous (clamp(80px, 13vw, 160px) top).
- **Pricing / plans** — Skip the largest display tier. `display-md` (48px Manrope 200) page anchor. Plans in 3-column white-card grid with multi-layer outline-ring shadow stack. One plan featured via warm-stone background tint, NOT via heavier border.
- **Documentation hub** — Skip display entirely. `headline-lg` (36px Manrope 300, slightly heavier) for entry titles. Body in Inter 16px with positive tracking — readable for long-form.

**Spacing for whisper rhythm:**

- Hero: `clamp(80px, 13vw, 160px)` top padding — the whitespace IS the volume
- Between sections: `clamp(64px, 9vw, 120px)` — generous; never less
- Inside cards: `xl` (32px) on bulk grid cards, `2xl` (48px) on featured / prominent cards
- Card grid gap: `lg` (24px) on bulk grids, `4xl` (80px) only when featuring 1–2 hero items
- Stat ribbons: `8xl` (64px) horizontal between stats — Apple-like generosity
- Section transitions never use hard rules. Whitespace + subtle background tint shift carry the chapter break.

## Core Aesthetic Principles

**Achromatic with warm undertones**
- The palette is intentionally without brand color
- Warmth lives in **surfaces** (`#F5F2EF` warm stone) and **shadows** (`rgba(78,50,23,0.04)`), never in hues
- A single muted accent is permitted only for sector-neutral trust signals (e.g., `#5C6E54` moss for B2B, declared as a divergence)
- Cool gray borders are forbidden — the warmth pervades borders, surfaces, AND shadows

**Multi-layer shadow stacks at sub-0.1 opacity**
- Every shadow operates at sub-0.1 opacity
- Combine THREE shadow layers on prominent surfaces (inset edge + outline ring + soft elevation)
- Surfaces seem to barely exist, floating just above the page
- Featured / hero CTAs use **warm-tinted shadows** (`rgba(78,50,23,0.04) 0 6px 16px`) — shadows have color, not just darkness

**Pill primary, warm-stone signature, asymmetric**
- Primary CTA = full pill (`9999px`), solid black or white-on-black, body-button typography
- Featured / hero secondary = the **warm-stone CTA** — translucent warm fill (`rgba(245,242,239,0.8)`), 30px radius (NOT full pill), **asymmetric padding** (`12px 20px 12px 14px`), warm-tinted shadow
- The asymmetric padding and 30px radius are the signature — recognizable as "the ElevenLabs button"
- Generic ghost / outline buttons are a fallback, not a default

**Generous radii everywhere**
- 16–24px on cards is the workhorse range
- 30px exclusively for the warm-stone CTA
- 9999px (pill) on all primary buttons, navigation pills, and tags
- Sharp corners (<8px) on cards or buttons break the ethereal quality

## Color Palette

| Token | Value | Usage |
|---|---|---|
| `--text-primary` | `#000000` | Headlines, display, primary CTA fills |
| `--text-secondary` | `#4E4E4E` | Body text, descriptions |
| `--text-tertiary` | `#777169` | Muted links, decorative underlines, fine print — warm gray, not cool |
| `--bg-page` | `#FFFFFF` | Primary background, card surfaces |
| `--bg-soft` | `#F5F5F5` | Subtle section differentiation |
| `--bg-warm` | `#F5F2EF` | Warm stone tint — the signature warm surface |
| `--bg-warm-trans` | `rgba(245,242,239,0.8)` | Featured CTA background |
| `--border-soft` | `#E5E5E5` | Explicit borders |
| `--border-faint` | `rgba(0,0,0,0.05)` | Ultra-subtle separators |

No brand color. No accent hue. If a divergence introduces a single sector-neutral tint (e.g., `#5C6E54` moss for B2B trust), declare it explicitly in provenance and use it surgically (eyebrow dot, micro-mark, hover state — never a fill).

## Shadow System

| Token | Value | Usage |
|---|---|---|
| `--shadow-inset-edge` | `rgba(0,0,0,0.075) 0 0 0 0.5px inset, #ffffff 0 0 0 0 inset` | Internal edge definition |
| `--shadow-outline` | `rgba(0,0,0,0.06) 0 0 0 1px, rgba(0,0,0,0.04) 0 1px 2px, rgba(0,0,0,0.04) 0 2px 4px` | Shadow-as-border for cards |
| `--shadow-card` | `rgba(0,0,0,0.4) 0 0 0 1px, rgba(0,0,0,0.04) 0 4px 4px` | Button elevation, prominent cards |
| `--shadow-warm-lift` | `rgba(78,50,23,0.04) 0 6px 16px` | Featured CTAs — warm-tinted |
| `--shadow-edge` | `rgba(0,0,0,0.08) 0 0 0 0.5px` | Subtle edge definition |

**The outline-ring shadow stack is the workhorse.** Three layers at sub-0.1 opacity is the default elevation for cards. Any shadow at >0.1 opacity breaks the ethereal quality immediately — it's an instant refactor.

**Reserve the full stack for hero/feature cards.** On bulk grids (e.g., 3+ matched cards), use the single outline-ring (`rgba(0,0,0,0.06) 0 0 0 1px` only) to keep paint cost manageable.

## Component Patterns

```css
/* Primary pill */
.btn-primary {
  background: var(--text-primary);
  color: var(--text-on-primary);
  border-radius: 9999px;
  padding: 0 18px;
  height: 44px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
}
.btn-primary:hover {
  transform: translateY(-1px);
  background: #1a1a1a;
}

/* Warm-stone signature CTA — asymmetric, 30px, warm shadow */
.btn-warm {
  background: rgba(245, 242, 239, 0.8);
  color: var(--text-primary);
  border-radius: 30px;
  padding: 12px 20px 12px 14px;
  box-shadow: rgba(78, 50, 23, 0.04) 0 6px 16px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
}
.btn-warm:hover {
  transform: translateY(-1px);
  background: var(--bg-warm);
  box-shadow: rgba(78, 50, 23, 0.06) 0 10px 24px;
}

/* Card — multi-layer shadow stack */
.card {
  background: var(--bg-page);
  border-radius: 20px;
  padding: 32px;
  box-shadow:
    rgba(0,0,0,0.06) 0 0 0 1px,
    rgba(0,0,0,0.04) 0 1px 2px,
    rgba(0,0,0,0.04) 0 2px 4px;
}

/* Hero card — heavier elevation */
.card-elevated {
  background: var(--bg-page);
  border-radius: 24px;
  padding: 48px;
  box-shadow:
    rgba(0,0,0,0.4)  0 0 0 1px,
    rgba(0,0,0,0.04) 0 4px 4px;
}

/* Whisper-weight display */
h1 {
  font-family: 'Manrope', 'Waldenburg Fallback', sans-serif;
  font-weight: 200;                /* the brand */
  font-size: clamp(48px, 7.4vw, 96px);
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

/* Body with positive tracking — the signature reading texture */
body {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.16px;
}
```

## Layout

- **Container width:** 1200–1240px max with generous gutters (clamp(20px, 4vw, 48px))
- **Hero:** centered or asymmetric — both work. Asymmetric reads more refined; centered reads more neutral. Choose based on brand voice.
- **Section padding:** `clamp(64px, 9vw, 120px)` vertical on every section. Hero gets `clamp(80px, 13vw, 160px)` top.
- **Card grids:** 3-column on desktop with `lg` (24px) gap; collapse to 2 / 1 column at standard breakpoints.
- **Featured surfaces (manifesto, testimonial, CTA):** wrap in a warm-stone `bg-warm` panel with 24px radius for chapter punctuation. Use sparingly — once or twice per page.

## Anti-Patterns to Avoid

- ❌ Bold (700+) Waldenburg/Manrope for body or section headings — only for the specific uppercase bold CTA
- ❌ Heavy shadows (>0.1 opacity) — the ethereal quality requires whisper-level depth
- ❌ Brand colors or accent hues — the system is achromatic with warm undertones
- ❌ Cool gray borders — the warm tint pervades borders, surfaces, and shadows
- ❌ Negative letter-spacing on body text — Inter uses positive tracking here (+0.14px to +0.18px)
- ❌ Opaque, heavy buttons — the warm translucent stone treatment is the signature
- ❌ Sharp corners (<8px) on cards — the generous radius is structural
- ❌ Symmetrical padding on the warm-stone CTA — `12px 20px 12px 14px` asymmetric is the brand
- ❌ Pure black `#000` background page — this is a light-mode style; dark-mode adaptation is out of scope unless explicitly briefed
- ❌ Saturated backgrounds — the page stays white/off-white; the warm stone is the only "color"

## Known Tensions

- **Light weight + accessibility.** Manrope/Waldenburg 200 at body sizes can fail WCAG AAA. Hold the line at display only — body must use Inter weight 400+. If a hero subtitle is under 24px, switch to Inter, not Manrope. Run contrast spot-checks at the smallest display size used.
- **Shadow stacking + paint performance.** Three-layer shadows on every card hit paint performance on lower-end devices. Reserve the full stack for hero/feature cards; use the single outline-ring on bulk grids.
- **Warm shadows + dark mode.** This style is designed for light surfaces. Dark-mode adaptation needs to invert the warmth (warm-tinted glow instead of warm-tinted shadow) and is not part of this preset. If a brief asks for dark mode + this style, escalate — it's a different style at that point.

## Output Checklist

Every Hushed Premium SaaS design should have:

- [ ] White or off-white page background (`#FFFFFF` / `#F5F5F5`)
- [ ] Display typography at weight 200–300 (Manrope or Waldenburg)
- [ ] Inter body at weight 400 with positive letter-spacing (+0.14 to +0.18px)
- [ ] Multi-layer shadow stacks at sub-0.1 opacity on cards (3 layers on hero, 1 layer on bulk)
- [ ] Warm-stone surface (`#F5F2EF`) on at least one featured panel (manifesto, testimonial, hero secondary)
- [ ] At least one warm-stone CTA with asymmetric padding (`12px 20px 12px 14px`) and 30px radius
- [ ] Pill (9999px) on primary buttons
- [ ] Generous section padding (`clamp(64px, 9vw, 120px)` vertical minimum)
- [ ] Card radius ≥16px (cards), ≥20px on prominent cards
- [ ] No brand color, no accent hue (single sector-neutral tint allowed if declared as divergence)
- [ ] Warm-tinted shadow (`rgba(78,50,23,0.04)`) on the featured CTA
- [ ] `prefers-reduced-motion` respected (no transform / opacity / animation)
- [ ] Mobile nav contract (Tactic 15) — hamburger with `aria-expanded`, Escape-to-close, focus trap
- [ ] `.js-ready` gate on reveal animations (Tactic 17)
- [ ] WCAG AA contrast verified for body text (4.5:1 minimum)
- [ ] If introducing a single sector-neutral accent, document it in provenance as a declared divergence

## Reference Implementation

A one-shot demo for Verum & Co. (B2B advisory firm brief) lives at:

```
_tests/design-skill-lab/oneshot/hushed-premium-saas.html
```

It diverges from this style's defaults in:
1. Display family Manrope 200 (proxy declared for Waldenburg)
2. Section padding tightened (96px → 80px) for denser B2B editorial pace
3. Single moss accent (`#5C6E54`) introduced for sector-neutral trust

Use it as scaffolding for new builds, but apply per-project DESIGN.md tokens — never the demo's tokens verbatim.
