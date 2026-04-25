# Build Tactics

Tactical do/don't recipes for the **build moment** — decisions made *before* writing markup, not caught after. Tactics 1–13 come from Refactoring UI (Wathan & Schoger), Don't Make Me Think (Krug), and 100 Things Every Designer Needs to Know (Weinschenk). Tactics 14–16 are conditional gates added from verification-build evidence (kindertech, os-traquinas, ledger, mainframe): dark-mode discipline, mobile nav implementation, component reusability.

Tactics 1–13 always run. Tactics 14, 15, and 16 are **conditional** — run only when their trigger axis or markup pattern is present.

`base-principles.md` answers "is this right?" (audit lens). This file answers "what should I do *now*?" (build lens). Load both in Phase 3.

---

## 1. Hierarchy is built with weight + colour, not size alone

The default AI move is to scale fonts up to signal importance. Wrong tool, often.

- **To emphasise** → bump weight (500 → 700) and darken the colour. Size third.
- **To de-emphasise** → drop weight (500 → 400) and lighten the colour. Don't shrink text below 14px just to "make it secondary".
- **Emphasise by de-emphasising.** Make the surrounding content quieter so the primary stands out — instead of making the primary louder. This is usually the better move.

❌ Headline 64px bold black on body 16px regular black. Headline screams but body still competes.
✅ Headline 48px bold #0A0A0A on body 16px regular #545454. Same headline weight, but the body recedes — headline now reads as primary.

## 2. Design grayscale-first, add colour last

Forces hierarchy via spacing, contrast, weight, and size — not via the cheap shortcut of "make it the brand colour".

When generating the first pass of any section:
1. Lay out structure with neutral palette only (text + 1-2 greys + white/black surface)
2. Verify hierarchy works in this state (squint test passes)
3. Then add accent colour to **one** element per section — usually the primary action

If hierarchy doesn't hold in grayscale, colour won't save it. Refactor structure first.

## 3. 60-30-10 colour distribution

Default rule of thumb. Deviate only with reason.

- **60% dominant** — page background, section surfaces. Usually a neutral.
- **30% secondary** — cards, panels, inverted sections, supporting blocks.
- **10% accent** — CTAs, links, focus rings, highlights, key icons.

❌ Accent at 30%+ → accent loses meaning. Whole page reads "loud".
❌ 50/50 split between two colours → no hierarchy. Eye doesn't know where to land.
✅ Predominantly white surface, mid-grey panels for secondary content, single brand accent reserved for CTAs and active states.

If a style breaks this rule by design (`neo-brutalist` floods accent intentionally, `spritify` uses bold colour as primary surface), state it in DESIGN.md provenance — don't slip into 60-30-10 by accident.

## 4. One primary action per section

Every section has a hierarchy of actions. Pick one primary, demote the rest.

- **Primary** → solid filled button, accent colour, full weight.
- **Secondary** → outline / ghost button, neutral colour.
- **Tertiary** → text link with underline-on-hover, no button chrome.

❌ Hero with three identical buttons side by side → user can't tell which is the intended action.
✅ Hero with one solid CTA + one outline secondary + one text link "Or browse the docs". Eye lands on the CTA first.

If two actions genuinely deserve equal weight, you're probably hiding a bigger issue (the section is doing two jobs — split it). Resist the temptation to make both primary.

## 5. More space *between* groups than *within* them

Proximity = relationship. Uniform spacing destroys grouping.

- Inside a card, between label and value: tight (8-12px).
- Between two related cards: medium (16-24px).
- Between two distinct sections: large (64-96px).

❌ Form label 16px from field, field 16px from next label, next label 16px from its field → user can't tell which label belongs to which field. Reads as 6 floating items, not 3 pairs.
✅ Form label 8px from its field, field 24px from next label → 3 pairs visually grouped.

This applies to every layer: words within a phrase, items within a list, cards within a section, sections within a page. Spacing should always communicate "these belong together" or "these don't".

## 6. Ruthless words — kill happy talk

Krug's law: get rid of half the words on each page, then half of what's left.

Happy talk to delete on sight:
- "Welcome to our [thing]"
- "We are pleased to / proud to / excited to..."
- "At [Company], we believe..."
- "Our innovative platform empowers..."
- Generic "Learn more" / "Submit" / "Click here" CTAs (always replace with the specific outcome: "Start free trial", "Download the report", "Book a 15-min call")

Instructions are a failure signal — if you wrote a tooltip explaining how to use the form, the form isn't self-evident. Fix the form, then delete the tooltip.

Test: read the page out loud. Every sentence should pass "would a busy user actually need this?"

## 7. Self-evident button labels

Krug: self-evident > self-explanatory > requires explanation.

For every button/CTA, ask: **does this label tell the user exactly what happens after the click?**

❌ "Submit" → submit what?
❌ "Click here" → why?
❌ "Get started" → with what? doing what?
✅ "Create my account" — verb + outcome.
✅ "Book a 15-min demo" — verb + specifics.
✅ "Download PDF (2MB)" — verb + format + cost-of-action.

Action labels should survive being lifted out of context. If the label only makes sense next to its surrounding paragraph, it's failing the self-evident test.

## 8. Touch targets ≥ 44×44px, in the thumb zone

Mobile build constraint, not review check. Bake it in from the start.

- Every interactive element (button, link, icon button, form input, tab) → minimum 44×44px hit area on mobile (WCAG 2.2). Padding counts. Visual size can be smaller if hit area meets it.
- Spacing between adjacent touch targets → at least 8px.
- Primary CTAs on mobile-critical pages → place in the **thumb zone** (bottom third of the screen, centre or slight offset). Top-of-screen primary CTAs are a desktop convention; on mobile they require a stretch reach.

❌ 32px icon-button row with 4px between items → fat-finger hell, mis-tap rate spikes.
✅ 44px icon buttons with 12px gap, or 32px icons inside 44×44 hit areas with 8px between hit-area edges.

## 9. Form friction — every field costs

Each form field reduces conversion by 5-10% (industry rule of thumb). Aggressive defaults:

- Ask only for what you genuinely need *now*. Defer optional fields to onboarding/profile.
- Email is enough for most signup flows. Add password if needed. Phone is rarely justified upfront.
- No CAPTCHA unless you have evidence of bot abuse.
- Inline validation — show errors as the user types/leaves the field, not after submit.
- Required fields marked clearly (asterisk + colour, not colour alone).
- Input types match the data: `type="email"`, `type="tel"`, `type="number"`, `inputmode="..."` on mobile.
- Single column, top-aligned labels. Side-aligned labels are slower to scan.

❌ 11-field "Get Started" form asking for company size and job title before the user has even seen the product.
✅ 1-field "Enter your email" → product → onboarding wizard fills the rest progressively.

## 10. Shadows go down, not everywhere

Real light comes from above. Shadows offset vertically with minimal horizontal spread.

❌ `box-shadow: 0 0 20px rgba(0,0,0,0.1)` → reads as a glow, not depth.
✅ `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` → reads as elevated.

For realistic depth, combine two shadows (ambient + direct):

```css
box-shadow:
  0 1px 3px rgba(0,0,0,0.12),  /* direct, sharp */
  0 4px 12px rgba(0,0,0,0.08); /* ambient, soft */
```

Build a 3-5 level elevation scale and use it consistently:
- `--shadow-sm` — buttons, inputs (subtle lift on hover).
- `--shadow-md` — cards, panels, dropdowns.
- `--shadow-lg` — popovers, large cards.
- `--shadow-xl` — modals, dialogs.

For `neo-brutalist`-family styles: solid offset shadows (`4px 4px 0 #000`) are correct — those are graphic blocks, not realistic depth. Use the right shadow grammar for the style.

## 11. Don't put pure grey on coloured surfaces

Pure grey (#888, #666) on a coloured background looks dead — grey has no saturation, fights the surface hue.

- On a blue card → use a desaturated blue for secondary text, not grey.
- On a warm-toned section → warm-tinted neutral, not pure grey.
- Mix 10-20% of the surface hue into the text colour.

Quick HSL recipe: same hue as background, drop saturation to 10-20%, adjust lightness for contrast.

❌ `color: #6B7280` on `background: #1E40AF` (blue card) → grey looks dirty against the blue.
✅ `color: #93C5FD` (light blue) on `background: #1E40AF` → harmonised, contrast preserved.

White-on-coloured works the same way: rather than `rgba(255,255,255,0.7)` everywhere, hand-pick a tinted neutral that reads white but harmonises.

## 12. Faces look toward the CTA

If the design uses imagery with people, the eyes/face direction in those images matter — the user follows the gaze (Weinschenk, dedicated face-processing region in the brain).

- Faces looking *away* from the CTA → user follows gaze off-screen, attention leaks.
- Faces looking *at* or *toward* the CTA → reinforces the visual flow.
- Headshot facing camera in a hero → neutral, doesn't direct attention either way.

This applies to illustrations and photos alike. When picking/cropping imagery, check eye direction relative to the rest of the composition.

## 13. Fewer borders, more shadows + spacing

Borders make designs feel busy. Most can be replaced.

- Card separation → background colour shift OR shadow OR extra spacing — not borders by default.
- Input field borders → keep them (forms need clear hit boundaries) but use 1px in a neutral colour.
- Section dividers → whitespace + colour shift > horizontal rule lines.

When borders *are* the right call (technical-refined dashed borders, neo-brutalist solid frames), they're a deliberate style signature — not a default fallback. Match the style's grammar.

❌ Every card has a 1px grey border + a shadow + a coloured top accent → triple-decorated, noisy.
✅ Card uses shadow alone for elevation. Border reserved for active/focus states.

## 14. Dark-mode discipline (conditional — runs when `color-mode = both` OR `color-mode = dark`)

Dark mode is not "invert the colours and ship". Light-mode tokens, recipes, and instincts produce broken dark-mode UIs. This tactic is the **build-time** gate — issues caught here never reach Phase 4.7's self-correction loop.

**When to run:** check `style-tuning.axes.color-mode.value`. If `light`, skip this tactic entirely. If `dark` or `both`, run the full checklist before generating any markup that targets the dark palette. For `both`, the rule is independent verification per palette — both passes must hold.

This tactic exists because verification build kindertech-v2 surfaced 5 of 6 Critical issues in the dark variant: contrast, shadow→border substitution, focus visibility, featured-card distinction, and surface elevation. Each one of those is a recipe-level mistake, not a one-off bug.

### 14.1 Surfaces — never pure black, never pure white

Pure `#000` page backgrounds make every surface above them look like a panel floating in vacuum. Real OLED apps tune the dark base to allow elevation hierarchy.

- **Page background** → `#0A0A0A` to `#141414` range. Pick one, document it.
- **Card / panel surface** → one tier brighter than page (e.g., page `#0F0F0E` → card `#1A1A19`).
- **Quiet panel / muted section** → another tier brighter still (e.g., `#222221`).
- **Text primary** → `#E0E0E0` to `#F0F0F0`. Pure `#FFFFFF` on `#000` causes halation (smearing/glow on OLED).
- **Text secondary** → 60-70% lightness of primary, same hue family as the surface.

Build a 3-tier surface scale (`bg-page < surface-card < surface-quiet`) so dark elevations read by **lightness shift**, not by shadow.

❌ `--bg-dark: #000000; --card-dark: #111111;` → 1-step delta, surfaces blend.
✅ `--bg-page-dark: #0F0F0E; --surface-card-dark: #1A1A19; --surface-quiet-dark: #222221;` → 3-tier scale, hierarchy reads.

### 14.2 Shadows don't work on dark — substitute with borders

Box-shadows assume the surface is lighter than the shadow colour. On dark backgrounds, a `rgba(0,0,0,0.1)` shadow is invisible (and going darker than `#0A0A0A` is impossible).

Replacement recipe:

```css
/* Light mode card elevation */
--shadow-md: 0 2px 4px rgba(0,0,0,0.08), 0 6px 14px rgba(0,0,0,0.06);

/* Dark mode equivalent — use a hairline border */
--shadow-md-dark: 0 0 0 1px rgba(255,255,255,0.06);
```

Tiered:
- `--dark-elev-1` → `0 0 0 1px rgba(255,255,255,0.04)` (subtle lift, e.g., inputs)
- `--dark-elev-2` → `0 0 0 1px rgba(255,255,255,0.08)` (cards)
- `--dark-elev-3` → `0 0 0 1px rgba(255,255,255,0.12)` (popovers, modals)

For dramatic elevation on dark (modals over a backdrop), pair the hairline border with a dark scrim (`background: rgba(0,0,0,0.6)` on the backdrop) — the depth comes from the scrim, not the shadow.

❌ Same `box-shadow` token in both modes → invisible in dark.
✅ Mode-conditional shadow: light uses vertical-offset shadow, dark uses hairline border + optional inner glow.

### 14.3 Accents — desaturate, never invert

Light-mode accents at full saturation glow harshly on dark backgrounds. The eye reads them as alarming.

- Drop saturation 10-20% from the light-mode value.
- Brighten lightness 5-15% to keep contrast above 4.5:1 against dark text overlays.
- Test the accent against both `surface-card-dark` and `bg-page-dark` — the lower-contrast pairing is the one that fails.

Quick HSL recipe:
```
Light accent:  hsl(15, 100%, 56%)   /* #FF531F coral */
Dark accent:   hsl(15, 90%, 62%)    /* #FF6B3D — desaturated, brightened */
```

Verify with WCAG: dark accent on `bg-page-dark` ≥ 4.5:1 for text use, ≥ 3:1 for large text or non-text UI.

### 14.4 Focus rings — must survive both modes

Light-mode focus rings (`outline: 2px solid #2563EB`) often disappear on dark surfaces or clash with dark accents.

Recipe:
- Dedicated `--focus-ring-dark` token, distinct from light-mode value.
- Use a **brightness-shifted** version of the accent OR a neutral high-contrast value (e.g., `#F0F0F0` outline + 2px offset).
- Always pair `outline` with `outline-offset: 2px` — gives breathing room on busy surfaces.
- 2px minimum thickness in dark mode (1px disappears against textured surfaces).

❌ `:focus { outline: 2px solid var(--accent); }` reused across modes → fails when dark accent ≈ surface card lightness.
✅ Mode-conditional: `[data-theme="dark"] :focus { outline: 2px solid var(--focus-ring-dark); outline-offset: 2px; }`

### 14.5 Featured / emphasised cards must distinguish in dark

Light mode often signals "this is the featured plan" by background tint (`background: #FFF8F0`) or border (`border: 2px solid coral`). Both fail in dark mode without explicit handling:
- Tinted bg → looks identical to surface-card on dark unless the tint is deliberately re-tuned for dark.
- Coloured border → loud and aggressive on dark surfaces, breaks the muted dark grammar.

Recipe for featured-card distinction in dark:
1. **Brighter surface tier** — feature uses `surface-quiet-dark` while neighbours use `surface-card-dark`. Single lightness step is enough.
2. **Accent inner-glow** — `box-shadow: inset 0 0 0 1px var(--accent-mid-dark)` adds an internal accent line without a heavy border.
3. **Top-edge accent** — `border-top: 2px solid var(--accent-dark)` keeps coloured emphasis but only on one edge.

Pick one. Stacking all three is decoration, not hierarchy.

### 14.6 Image and SVG handling

- Photographic imagery → check it doesn't carry a bright sky/white-background that becomes a glaring rectangle on dark page. Pre-darken in CSS via `filter: brightness(0.9) contrast(1.05)` for cross-mode photos, or ship a dark-tuned variant.
- SVG icons that use `currentColor` → free dark-mode handling, prefer this approach.
- SVGs with hardcoded fills → audit each one; provide a dark variant or mark as "light-only".
- Logos → if the logo has a dark-mode variant, use it. If not, document the regression.

### 14.7 Checklist (run before generating dark-mode markup)

If `color-mode = dark` or `color-mode = both`, every item below must be resolved before writing any dark-targeting CSS:

- [ ] Page bg ≠ pure `#000` (range `#0A0A0A`–`#141414`)
- [ ] Text primary ≠ pure `#FFF` (range `#E0E0E0`–`#F0F0F0`)
- [ ] 3-tier dark surface scale defined (`bg-page` < `surface-card` < `surface-quiet`)
- [ ] Shadow tokens have a dark-mode equivalent (border-based, not shadow-based)
- [ ] Accent dark variant defined: saturation −10–20%, lightness +5–15%
- [ ] Accent dark variant verified ≥4.5:1 against dark-text use, ≥3:1 against UI-overlay use
- [ ] Focus ring has dedicated dark token, ≥2px, with offset
- [ ] Featured-card distinction recipe chosen (surface tier OR inner glow OR top accent — not all three)
- [ ] Photographic imagery audited for dark-mode glare; SVG fills audited for hardcoded colours
- [ ] If `color-mode = both`: light palette and dark palette pass independently — no shared tokens that fail in one mode

If any item is unresolved, fix in tokens before generating markup. This is what stops the same 5/6 Criticals showing up in the next build.

## 15. Mobile nav implementation (conditional — runs when `nav` element exists in build)

Every verification build so far shipped without a working mobile nav. The desktop nav-list hides at the breakpoint, and nothing replaces it. This tactic is the implementation contract — minimum viable mobile nav, no excuses.

**When to run:** any build that has a `<nav>` with multiple links and a breakpoint-based hide rule for the nav-list. If the nav has only one link or is always visible, skip.

### 15.1 The contract

Mobile nav must include all of:

1. **Hamburger trigger** — `<button>` with `aria-expanded`, `aria-controls`, accessible label (`aria-label="Open menu"` / `"Close menu"`). Visible only at breakpoint.
2. **Drawer / overlay** — full-height (or full-screen) panel containing the nav links. Slides or fades in.
3. **Open / close mechanics**:
   - Click hamburger → open
   - Click X (or hamburger again) → close
   - Click outside the drawer (on backdrop) → close
   - Press `Escape` → close
4. **Focus management**:
   - When opened, focus moves to first interactive element inside the drawer (or to close button)
   - When closed, focus returns to the hamburger trigger
   - Focus is trapped inside the drawer while open — `Tab` cycles within drawer, doesn't escape to the page below
5. **Body scroll lock** — when drawer is open, the page beneath doesn't scroll. Apply `overflow: hidden` on `<body>` while open.
6. **Reduced motion** — if `prefers-reduced-motion: reduce`, drawer fades in/out (no slide), or instant.

### 15.2 Markup pattern

```html
<nav class="site-nav">
  <a href="/" class="logo">Brand</a>

  <!-- Desktop nav-list (hidden on mobile via CSS) -->
  <ul class="nav-list" data-desktop>
    <li><a href="#features">Features</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#about">About</a></li>
  </ul>

  <!-- Hamburger (hidden on desktop via CSS) -->
  <button
    class="nav-toggle"
    aria-expanded="false"
    aria-controls="mobile-drawer"
    aria-label="Open menu"
    data-nav-toggle
  >
    <span class="nav-toggle-bar" aria-hidden="true"></span>
    <span class="nav-toggle-bar" aria-hidden="true"></span>
    <span class="nav-toggle-bar" aria-hidden="true"></span>
  </button>

  <!-- Drawer + backdrop -->
  <div class="nav-backdrop" data-nav-backdrop hidden></div>
  <aside id="mobile-drawer" class="nav-drawer" data-nav-drawer hidden aria-label="Site navigation">
    <button class="nav-close" aria-label="Close menu" data-nav-close>×</button>
    <ul class="nav-drawer-list">
      <li><a href="#features">Features</a></li>
      <li><a href="#pricing">Pricing</a></li>
      <li><a href="#about">About</a></li>
    </ul>
  </aside>
</nav>
```

### 15.3 CSS contract

```css
/* Default — mobile-first */
.nav-list[data-desktop] { display: none; }
.nav-toggle { display: inline-flex; }

@media (min-width: 768px) {
  .nav-list[data-desktop] { display: flex; }
  .nav-toggle { display: none; }
  .nav-drawer, .nav-backdrop { display: none !important; }
}

.nav-drawer[hidden] { display: none; }
.nav-drawer {
  position: fixed; inset: 0 0 0 auto;
  width: min(320px, 85vw);
  background: var(--surface-card);
  z-index: 100;
  transform: translateX(100%);
  transition: transform 250ms var(--ease-standard);
}
.nav-drawer[data-open="true"] { transform: translateX(0); }

.nav-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 99;
  opacity: 0; transition: opacity 250ms;
}
.nav-backdrop[data-open="true"] { opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  .nav-drawer, .nav-backdrop { transition: none; }
}
```

### 15.4 JavaScript contract (vanilla, no framework dependencies)

```js
(function () {
  const toggle = document.querySelector('[data-nav-toggle]');
  const close = document.querySelector('[data-nav-close]');
  const drawer = document.querySelector('[data-nav-drawer]');
  const backdrop = document.querySelector('[data-nav-backdrop]');
  if (!toggle || !drawer) return;

  let lastFocused = null;
  const focusableSel = 'a[href], button, [tabindex]:not([tabindex="-1"])';

  function open() {
    lastFocused = document.activeElement;
    drawer.hidden = false; backdrop.hidden = false;
    requestAnimationFrame(() => {
      drawer.dataset.open = 'true'; backdrop.dataset.open = 'true';
    });
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    document.body.style.overflow = 'hidden';
    const first = drawer.querySelector(focusableSel);
    (first || drawer).focus();
    document.addEventListener('keydown', onKey);
    backdrop.addEventListener('click', closeDrawer);
  }

  function closeDrawer() {
    drawer.dataset.open = 'false'; backdrop.dataset.open = 'false';
    setTimeout(() => { drawer.hidden = true; backdrop.hidden = true; }, 250);
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKey);
    backdrop.removeEventListener('click', closeDrawer);
    if (lastFocused) lastFocused.focus();
  }

  function onKey(e) {
    if (e.key === 'Escape') return closeDrawer();
    if (e.key !== 'Tab') return;
    // focus trap
    const focusables = Array.from(drawer.querySelectorAll(focusableSel))
      .filter(el => !el.hasAttribute('disabled'));
    if (focusables.length === 0) return;
    const first = focusables[0], last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  toggle.addEventListener('click', () => {
    toggle.getAttribute('aria-expanded') === 'true' ? closeDrawer() : open();
  });
  if (close) close.addEventListener('click', closeDrawer);
})();
```

### 15.5 Checklist

If the build has a `<nav>` element with breakpoint-based hide:

- [ ] Hamburger button exists, has `aria-expanded`, `aria-controls`, accessible label
- [ ] Drawer markup exists with `aria-label` and starts `hidden`
- [ ] Backdrop element exists for click-outside-to-close
- [ ] Click on hamburger toggles open/close
- [ ] Click on backdrop closes
- [ ] `Escape` closes
- [ ] Focus moves into drawer on open, returns to trigger on close
- [ ] `Tab` is trapped within drawer while open
- [ ] `<body>` `overflow: hidden` while drawer is open
- [ ] `prefers-reduced-motion` respected (no slide)
- [ ] Drawer hidden completely on desktop breakpoint (`display: none !important`)

If any item missing, the nav is broken on mobile. This is not a "polish for v2" item — keyboard users and screen-reader users genuinely cannot navigate without it.

## 16. Component reusability discipline (conditional — runs when 3+ instances of the same pattern appear)

Three is the threshold. One instance is a one-off; two is a coincidence; **three is a pattern that needs a component definition**. Without this discipline, builds end up with seven slightly-different "card" styles that each carry their own padding, radius, shadow — and every change costs N edits instead of one.

**When to run:** scan the build *before* generating the third instance of any of: card, button, list-item, input, badge, tag, callout, testimonial, feature-block, pricing-tier, section-header. If the third one is about to appear, define a component instead of duplicating.

This tactic exists because verification-build evidence (multiple `os-traquinas`, `mainframe`, `ledger` builds) showed the same pattern: cards rendered as 4-7 sibling div blocks each with their own bespoke styling. The result: visual drift, inconsistent radii, inconsistent padding, broken hierarchy across what should look like a uniform set.

### 16.1 The "if you can't reuse it" test

Before shipping any pattern that appears 3+ times, answer:

- **Can I describe it in a single class + variants?** (`.card`, `.card--featured`, `.card--quiet`)
- **Do all instances share the same padding, radius, shadow, and internal spacing tokens?** Token values come from the system, never hand-typed.
- **If I had to add a 5th instance, would I copy-paste a div block, or would I just write `<div class="card">`?**

If the answer to (3) is "copy-paste a div block", it's not a component — it's seven ad-hoc styles wearing matching paint.

### 16.2 Variant naming convention

Every reusable component gets explicit variants. Naming uses a `block__element--modifier` style or Tailwind data-attribute style — pick one and stick to it for the whole build.

Required variants by component type:

| Component | Default | Variants |
|---|---|---|
| **Button** | `.btn` (primary) | `.btn--secondary` (outline/ghost), `.btn--tertiary` (text), `.btn:disabled` |
| **Card** | `.card` (default) | `.card--featured` (hero / recommended), `.card--quiet` (de-emphasised) |
| **Input** | `.input` (default) | `.input--invalid` (error), `.input:disabled` |
| **Badge / Tag** | `.badge` | `.badge--neutral`, `.badge--success`, `.badge--warning`, `.badge--error` |
| **List item** | `.list-item` | `.list-item--active`, `.list-item--header` |
| **Section** | `.section` | `.section--inverted` (dark band), `.section--quiet` (muted bg) |

If a variant is needed once, document it; if it's needed three times, add it to the table for that build.

### 16.3 Tokens-first composition

Every visual property of a component must come from a design token, not a hand-typed value. The component's CSS reads like a recipe of tokens:

```css
.card {
  padding: var(--space-pad-card);          /* spacing scale */
  border-radius: var(--radius-md);         /* radius scale */
  background: var(--surface-card);         /* color tier */
  box-shadow: var(--shadow-md);            /* elevation scale */
  font-size: var(--font-body);             /* type scale */
}
.card--featured {
  background: var(--surface-quiet);        /* tier shift, not new colour */
  box-shadow: var(--shadow-lg);            /* elevation shift, not custom */
}
```

If a component uses `padding: 27px` or `box-shadow: 0 5px 11px rgba(0,0,0,0.13)` (custom values), it has broken the system. Refactor: the value either belongs in the token scale (add it once, use everywhere) or it's wrong (snap to the nearest scale value).

### 16.4 Variant-by-state matrix

Components that combine variants × states get a small matrix. Don't ship one without the other.

For a button: `(primary | secondary | tertiary) × (default | hover | active | focus | disabled)` = 15 cells. All 15 must have defined styling — not necessarily distinct, but explicitly considered. Tactic / Tactic 14 already covers `:focus` for dark mode; this tactic covers the matrix completeness.

A common failure: `.btn--secondary:disabled` falling back to `.btn:disabled` styles, which were designed for the primary variant and look wrong on the outline button. Audit each cell.

### 16.5 Anti-pattern — "almost-reusable" components

Watch for components where the public API is a `class="card"` but every instance overrides 3+ properties inline:

```html
<!-- ❌ this isn't reusable, the overrides are doing all the work -->
<div class="card" style="padding: 24px; background: #f5f5f5; border-radius: 12px;">
<div class="card" style="padding: 32px; background: #ffffff; border-radius: 16px;">
<div class="card" style="padding: 16px; background: #fafaf7; border-radius: 8px;">
```

If three instances of the same class need three sets of inline overrides, the variants don't exist yet. Define `.card--sm`, `.card--md`, `.card--lg` (or whatever the difference actually is) and remove the inline styles. Inline overrides are a debt signal.

### 16.6 Checklist

If the build has 3+ instances of any component type, every item below must be true before delivery:

- [ ] Component is defined as a single class + named variants (no inline style overrides for variant differences)
- [ ] Every variant uses tokens from the system — no magic padding/radius/shadow values
- [ ] All required variants for the component type are defined (see 16.2 table)
- [ ] All states (default/hover/active/focus/disabled) are styled per variant where applicable
- [ ] Featured / emphasised / quiet variants distinguish via tier shift on tokens (surface tier, elevation tier), not bespoke colours
- [ ] Renaming the chosen base library (e.g., switching `creative-studio` for `technical-refined` in DESIGN.md) wouldn't require touching component CSS — only the tokens

If any item fails, refactor. Component discipline failures are the difference between "this build is a system" and "this build is a collage".

---

## Trauma-informed mode (cross-reference)

When Phase 1 detects sensitive content (health, abuse, crisis, legal aid, addiction, mental health, grief, financial distress), the build mode shifts. Load `~/.claude/skills/design-reviewer/references/trauma-informed.md` from the design-reviewer skill before Phase 2 — it covers SAMHSA principles, copy guidelines, sensitive imagery, and red flags.

Key build-time shifts under trauma-informed mode:
- Avoid harsh reds, alarming yellow/black combinations, clinical white
- Prefer muted warm tones, soft greens/blues
- No autoplay, no sudden animations, no urgency tactics
- Always-visible exit/skip options
- Strength-based, empowering language ("You have the right to..." not "Victims can...")
- Crisis resources visible but not alarming
- Never require retelling the trauma
- No dark patterns of any kind

If trauma-informed mode is active, state this in the delivery summary.

---

## Pre-build checklist

Before generating any markup, run through these:

- [ ] Hierarchy designed with weight + colour, not size alone (Tactic 1)
- [ ] First pass thought through in grayscale (Tactic 2)
- [ ] Accent colour reserved for ~10% of surface area (Tactic 3)
- [ ] One primary action identified per section (Tactic 4)
- [ ] Spacing scale: more between groups than within (Tactic 5)
- [ ] Copy passes ruthless words test — no happy talk, specific CTA labels (Tactics 6-7)
- [ ] Mobile touch targets ≥ 44×44 with adequate spacing (Tactic 8)
- [ ] Forms minimised to essential fields (Tactic 9)
- [ ] Shadow grammar matches the style (vertical offset OR style-specific solid) (Tactic 10)
- [ ] No pure grey on coloured surfaces (Tactic 11)
- [ ] Imagery face direction reinforces flow (if applicable) (Tactic 12)
- [ ] Borders earn their place (Tactic 13)
- [ ] If `color-mode = both` or `dark` → Tactic 14 dark-mode checklist passed (Tactic 14.7)
- [ ] If `<nav>` with breakpoint hide → Tactic 15 mobile nav contract included (Tactic 15.5)
- [ ] If 3+ instances of any component pattern → Tactic 16 component reusability contract met (Tactic 16.6)
- [ ] If sensitive content → trauma-informed reference loaded (cross-reference section)

These are gates, not suggestions. Skipping them means catching the same issues in Phase 4.3 / 4.7 — wastes the self-correction loop on stuff that should never have shipped.
