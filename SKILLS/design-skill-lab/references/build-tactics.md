# Build Tactics

Tactical do/don't recipes for the **build moment** — decisions made *before* writing markup, not caught after. Tactics 1–13 come from Refactoring UI (Wathan & Schoger), Don't Make Me Think (Krug), and 100 Things Every Designer Needs to Know (Weinschenk). Tactics 14–17 are conditional gates covering recurring failure modes: dark-mode discipline, mobile nav implementation, component reusability, surface-context text scoping.

Tactics 1–13 always run. Tactics 14, 15, 16, and 17 are **conditional** — run only when their trigger axis or markup pattern is present.

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

This tactic exists because dark-mode builds reliably surface a recurring cluster of Critical issues — contrast, shadow→border substitution, focus visibility, featured-card distinction, and surface elevation. Each one is a recipe-level mistake, not a one-off bug.

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

**Hard-offset (brutalist) shadow on dark — the deliberate exception.** Some dark-mode styles intentionally break the "shadows are invisible on dark" rule by using a **hard, opaque, offset shadow** as graphic depth rather than realistic light. The Composio reference is canonical: dark cards (`#000`) on a Void Black page (`#0F0F0F`) carry a `box-shadow: rgba(0,0,0,0.15) 4px 4px 0px 0px` — a chunky offset block-shadow that reads as raw retro-computing depth, not as ambient light.

Recipe:

```css
/* Brutalist dark shadow — graphic, not lit */
.card--brutalist {
  background: #000;
  border: 1px solid rgba(255, 255, 255, 0.10);
  box-shadow: rgba(0, 0, 0, 0.15) 4px 4px 0 0;
}
```

Use only when:
- The style explicitly invites brutalist/retro-computing personality (Composio-class developer-tool sites, Bold Grid Manifesto on dark, technical-refined with intentional roughness).
- The shadow is **opaque and offset**, not soft and ambient — this is graphic depth, not realistic depth.
- It appears on **select** elements (hero cards, feature highlights), not every card. Floods the page if used as default elevation.

Don't combine with the hairline-border elevation system on the same card — pick one or the other. Mixing reads as confused.

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

Mobile nav is the most commonly skipped surface in build output — the desktop nav-list hides at the breakpoint and nothing replaces it. This tactic is the implementation contract — minimum viable mobile nav, no excuses.

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

## 17. Surface-context text scoping (conditional — runs when build mixes light/dark surfaces)

Mixed-surface layouts reliably ship invisible text because text colours inherit from the *page/section* context instead of being scoped to the *immediate surface*. The pattern is generic and recurs across libraries; this tactic is the build-time gate that catches it before delivery.

**When to run:** any build where the markup contains a surface-flip — a light section containing a dark card / panel / testimonial / quote / modal / callout, OR a dark section containing a light variant of the same. Trigger keywords in CSS: `.section--dark`, `.section--inverted`, `[data-theme="dark"]` scoped to a section, or any class that swaps the local background to the opposite of the page's `body`. If the build is single-mode and surfaces don't flip locally, skip.

The corollary trigger: **JS-driven reveal animations** (`.reveal { opacity: 0 }`, `.fade-in`, `[data-aos]`, etc.) without progressive-enhancement gating. These hide content until JS confirms — if JS fails, content stays invisible. See 17.4.

### 17.1 The contract

Every text element inside a flipped surface must declare its colour against its **local** surface, not inherit from the page.

- ❌ `.section--dark { color: var(--text-light); }` then a nested `.testimonial-card { background: white; }` with no colour reset → testimonial inherits light text on white = invisible.
- ✅ `.section--dark { color: var(--text-light); } .section--dark .testimonial-card { background: white; color: var(--text-dark); }` → reset.

The simplest implementation: every component that can sit on either light or dark surfaces (testimonial, card, quote, callout, panel) defines its own surface + colour pair as a unit. No exceptions.

### 17.2 The four common failure shapes

These are the patterns to scan for:

| Shape | Symptom | Fix |
|---|---|---|
| **Light card in dark section** | Card body text white-on-white; only avatar / icon visible | Component sets its own `color: var(--text-on-light-surface)` |
| **Dark card in light section** (testimonial-on-coloured) | Card body text dark-on-dark; only background visible | Component sets its own `color: var(--text-on-dark-surface)` |
| **Inherited via `color: inherit`** | Text "looks fine" in one section, breaks when component reused elsewhere | Replace `inherit` with explicit token from local surface |
| **JS-gated reveal without fallback** | Content invisible until scroll triggers `.visible`. If JS fails or runs late → permanent invisibility | See 17.4 progressive-enhancement gate |

### 17.3 Code patterns — token discipline for surface-aware components

The cleanest implementation uses **per-surface colour tokens** that are namespaced by the surface they belong to:

```css
:root {
  /* Page-level defaults */
  --bg-page: #FFFFFF;
  --text-page: #1A1A1A;

  /* Per-surface tokens — declared once, used everywhere the surface appears */
  --surface-light: #FFFFFF;
  --text-on-surface-light: #1A1A1A;
  --text-muted-on-surface-light: #6B6B6B;

  --surface-dark: #1A1A1A;
  --text-on-surface-dark: #F5F5F5;
  --text-muted-on-surface-dark: #A0A0A0;
}

/* Component declares its surface + colour as a unit */
.testimonial-card {
  background: var(--surface-light);
  color: var(--text-on-surface-light);
}
.testimonial-card .role {
  color: var(--text-muted-on-surface-light);
}

/* Same component, dark variant */
.testimonial-card--dark {
  background: var(--surface-dark);
  color: var(--text-on-surface-dark);
}
.testimonial-card--dark .role {
  color: var(--text-muted-on-surface-dark);
}
```

The principle: **a component's text colour is determined by its own background, not by the section it sits in**. This pattern survives nesting, reordering, and theme switches.

### 17.4 Progressive-enhancement gate for reveal animations

If the build uses CSS-driven reveal animations (`opacity: 0` initial state, `opacity: 1` on `.visible` class added by JS), the initial hidden state must be **gated by a `.js-ready` class on the html/body element**. Without this gate, a JS failure leaves all `.reveal` content permanently invisible.

❌ **Broken pattern:**
```css
.reveal { opacity: 0; transform: translateY(20px); }
.reveal.visible { opacity: 1; transform: translateY(0); }
```
```js
// If this script fails, .reveal stays at opacity: 0 forever.
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

✅ **Progressive-enhancement pattern:**
```css
/* Reveal hidden state ONLY applies once JS confirms it can animate */
.js-ready .reveal { opacity: 0; transform: translateY(20px); }
.js-ready .reveal.visible { opacity: 1; transform: translateY(0); }
/* Without .js-ready, .reveal renders fully visible (graceful fallback) */
```
```js
(function() {
  // Mark JS as ready FIRST — enables the hidden state in CSS
  document.documentElement.classList.add('js-ready');

  // Defensive: if IntersectionObserver missing, show everything
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    return;
  }

  // Respect prefers-reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    return;
  }

  // Standard observer setup
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach(function(el) {
    observer.observe(el);
  });
})();
```

The `.js-ready` gate is the single most important line. Without it, every reveal-animated build is one JS error away from looking broken to the user.

### 17.5 Anti-patterns

- ❌ **Global `color: white` on a dark page body** without per-component overrides for nested light cards. Inheritance turns nested cards invisible.
- ❌ **`color: inherit`** on testimonial-name, card-title, quote-author. These elements are reused across surfaces; explicit tokens beat inheritance.
- ❌ **Reveal animations gated only by `prefers-reduced-motion`**. The reduced-motion fallback handles user preference, not JS failure. Use `.js-ready` for failure resilience.
- ❌ **Single `--text-default` variable used everywhere**. The variable name implies "use this for all text", which is exactly what creates the inheritance bug. Name tokens by surface (`--text-on-surface-light`), not by hierarchy (`--text-default`).
- ❌ **Single dark-mode override** like `[data-theme="dark"] { color: white }`. This works for top-level body text; it doesn't work for nested light cards intentionally placed on dark sections within dark mode (the inversion-of-inversion case).

### 17.6 Audit test (mental flip)

Before delivery, walk the build mentally. **Flip every surface**: every dark surface becomes light, every light surface becomes dark. Walk through every text element. If any text becomes invisible, illegible, or fails 4.5:1 contrast against its *new* surface — the colour was inherited instead of scoped. Refactor.

If the build has reveal animations, also: **disable JS** in the browser (DevTools → Sources → Disable JavaScript → reload). Every page section should be readable. If anything is invisible, the `.js-ready` gate is missing.

### 17.7 Checklist (run before delivery if Tactic 17 triggered)

- [ ] Every component that can appear on multiple surfaces declares its `background` AND `color` as a pair (no `color: inherit` on testimonial/card/quote/callout text)
- [ ] Per-surface colour tokens are namespaced (`--text-on-surface-dark`, not `--text-muted`)
- [ ] Mental flip test passes: flipping every surface mode exposes no invisible text
- [ ] If reveal animations are used: `.js-ready` gate present in CSS (`opacity: 0` only applies under `.js-ready`)
- [ ] If reveal animations are used: JS adds `.js-ready` to `document.documentElement` as the FIRST line of the IIFE
- [ ] If reveal animations are used: IntersectionObserver fallback present (if API missing → show everything)
- [ ] Disable-JS test passes: page renders fully readable without JS
- [ ] Disable-CSS test passes: page renders fully readable without CSS (semantic markup only — sanity check)

If any item fails, refactor before delivery. Surface-context bugs are among the most user-visible failure modes the skill can ship — text invisible on its own background.

---

## 18. Interactive state coverage in derived themes (conditional — runs whenever a build adds a non-default theme to a single-theme style)

This tactic exists because a real ship-defect happened: Atmospheric Protocol gained a light-mode derivation (`atmospheric-protocol-light-dark.html`), the surface tokens were carefully re-derived per `effects/liquid-glass.md` § 6.5, the page glass and atmosphere flipped correctly — but the primary CTA buttons rendered as `dark pill + dark text` (invisible) in light mode. Root cause: the dark CSS contained `color: #000000` hardcoded inside `.btn--primary`. The text-token followed the theme inversion (`var(--color-text-primary)` flipped from white → dark), but the hardcoded text colour did not. Result: a visually critical button that the user could not read.

The general lesson: **a style that ships with a single colour-mode default can hide hardcoded values inside interactive selectors that nobody notices, because the inversion only triggers when the new mode arrives.** When you add the new mode, you have to audit every interactive state in every interactive selector.

### 18.1 When this tactic fires

Run this checklist whenever any of the following are true:

- A library declared `color-mode: dark` (or `light`) ships a counterpart variant (light-on-dark or dark-on-light derivation).
- A theme-toggle or `prefers-color-scheme` switch is being added to a build that previously rendered in a single mode.
- A CSS-variable refactor introduces `[data-theme="..."]` selectors (or a parent class like `.theme-light`) for the first time.

If the build is single-mode by intent (e.g., Sanctuary Tech, Memoir Blog at default), this tactic does not apply.

### 18.2 The audit — find the hidden hardcoded values

Before claiming the new mode "works," grep the build CSS for every property in this list, in every interactive selector (`.btn*`, `.cta*`, `button`, `input`, `select`, `textarea`, `a:not(.card)`, `.toggle`, `.chip`, `.pill`, `.badge`, `.tag`, `.menu`, `.drawer`, `.dialog`, `.modal`, `.tab`, `nav-*`, `.link`):

| Property | Hardcoded value patterns to flag |
|---|---|
| `color` | `#000000`, `#000`, `black`, `#FFFFFF`, `#FFF`, `white`, any hex literal |
| `background` / `background-color` | hex literal, `black`, `white`, `rgb(0,0,0)`, `rgba(0,0,0,*)` (when not part of an intentional fixed-colour pattern like an accent) |
| `border-color` / `border` | hex literal, `black`, `white` |
| `box-shadow` | embedded hex (e.g. `0 0 24px #000`) |
| `outline-color` | hex literal |
| `fill` / `stroke` (on inline SVG) | hex literal |

Each hit is a candidate for theme inversion failure. Two outcomes per hit:

- **Intentional fixed colour** (e.g., a brand pill that's always coral on every theme) — leave it but document in DESIGN.md provenance under `theme-locked-colours`.
- **Inversion-breaking** (the property pairs with a token that DOES invert) — must be overridden in the new theme.

### 18.3 The five interactive states that must be re-audited per new theme

For every interactive selector that the audit flags, re-derive **all five states** in the new theme:

1. **Default / resting state** — base colour, background, border on the unhovered, unfocused element.
2. **`:hover`** — colour shift, background lift, border highlight. Often inverts the resting state (transparent ↔ filled). Always check that the inverted state still has contrast against the new theme's surface.
3. **`:focus-visible`** — outline / ring colour and width. The default browser ring is `Highlight` (system colour) which usually works, but custom rings with hardcoded `outline-color: #...` will break.
4. **`:active`** — pressed / down state. Often a `transform: translateY(1px)` only (theme-safe) but sometimes adds a background tint that needs theme awareness.
5. **`:disabled`** / `[aria-disabled="true"]` — usually a desaturated muted state. Hardcoded `color: #ccc` breaks on light backgrounds (becomes invisible). Use a token-derived muted colour.

Plus two state-adjacent considerations:

- **Placeholder text** in inputs (`::placeholder`) — usually a fixed grey that fails contrast on the inverted theme. Override per theme.
- **Selection** (`::selection`) — the highlight colour for selected text. If hardcoded, looks wrong in the new theme.

### 18.4 The override pattern — explicit, not relying on cascade

**Wrong** — assume the cascade will catch it because the variable inverts:

```css
/* Original, single-mode build */
.btn--primary {
  background: var(--color-text-primary);
  color: #000000;          /* ← hardcoded, will not invert */
}
```

This ships broken in the new theme. The text-primary token flipped, the colour did not.

**Right** — explicit per-theme override:

```css
/* Original — kept as-is, defines the dark-mode (default) behaviour */
.btn--primary {
  background: var(--color-text-primary);
  color: #000000;
}

/* New theme — explicit override for the hardcoded value */
:root[data-theme="light"] .btn--primary {
  color: #FFFFFF;          /* ← inverted intentionally */
}
:root[data-theme="light"] .btn--primary:hover { /* ... */ }
:root[data-theme="light"] .btn--primary:focus-visible { /* ... */ }
:root[data-theme="light"] .btn--primary:disabled { /* ... */ }
```

Three rules of the override pattern:

- **Override at the same specificity tier or higher** than the original. `:root[data-theme="light"] .btn--primary` (specificity 0,2,1) beats `.btn--primary` (0,1,0).
- **Override every state, not just default.** Even if `:hover` uses tokens that invert correctly, declare the override anyway — it makes the per-theme intent explicit and survives future refactors.
- **Document the inversion in DESIGN.md provenance** under `theme-derivation.interactive-overrides` so a future audit knows why the duplicate rules exist.

### 18.5 The cross-state contrast spot-check

For every primary interactive in the build (CTAs, primary buttons, form submits), compute the contrast ratio of `color` against `background-color` in BOTH themes, in BOTH `:default` and `:hover`. Acceptable: ≥ 4.5:1 (WCAG AA for normal text), ≥ 3:1 for large text (≥18px or ≥14px bold).

A 50ms manual test in DevTools beats catching it in user testing. Toggle the theme; for each visible button, inspect → "Contrast ratio" indicator. Any AA failure is a delivery blocker.

### 18.6 Reduced-transparency + theme-derivation interaction

The `prefers-reduced-transparency` fallback block (mandatory whenever `backdrop-filter` is in use — see `effects/liquid-glass.md`) MUST handle each theme separately:

```css
@media (prefers-reduced-transparency: reduce) {
  /* Default fallback — covers the original mode */
  .glass-surface { background: var(--color-surface-card); backdrop-filter: none; }

  /* Per-theme fallback — covers the derived mode separately */
  :root[data-theme="light"] .glass-surface {
    background: #FFFFFF;
    backdrop-filter: none;
    border-color: rgba(20, 24, 31, 0.12);
  }
}
```

If the media query block does NOT differentiate per theme, the derived mode inherits the wrong fallback (e.g., dark surface colour on light page) and the reduced-transparency a11y path renders as broken. This is the most common silent regression at this stage — it only surfaces when a tester explicitly enables `prefers-reduced-transparency` in OS settings.

### 18.7 Pre-delivery checklist

- [ ] Grep for every `color`, `background*`, `border-color`, `box-shadow`, `outline*`, `fill`, `stroke` declaration with a hardcoded hex / `black` / `white` value inside an interactive selector — documented or overridden, never silently shipped
- [ ] Every flagged hit is either listed in `theme-locked-colours` provenance OR has a per-theme override block
- [ ] Each interactive selector's five states (default, hover, focus-visible, active, disabled) verified in BOTH themes
- [ ] `::placeholder` and `::selection` colours verified in BOTH themes if used
- [ ] Contrast spot-check: every primary CTA + form submit ≥ 4.5:1 in both themes, both default and hover
- [ ] `prefers-reduced-transparency` media query has a separate block per theme
- [ ] Toggle test: load page in default theme → toggle → visually scan each button and link in viewport → no invisible text, no missing borders
- [ ] DESIGN.md provenance declares `theme-derivation.interactive-overrides: true` and lists which selectors required overrides

If any item fails, refactor before delivery. Interactive-state inversion bugs are visible to every user the moment the new theme renders — they are not edge cases.

### 18.8 Cross-references

- `effects/liquid-glass.md` § 6.5 — Light-mode glass adaptation, the 5 mandatory rules; this tactic is the build-side companion (those rules cover surfaces; this tactic covers interactives ON those surfaces).
- `references/styles/atmospheric-protocol.md` § Light-Mode Interpretation (Advanced Derivation) — the canonical case study; the bug that motivated this tactic.
- `style-reviews/effects/liquid-glass.md` § Light-mode glass — the 5-rule check + interactive state coverage — the verification pass.
- Tactic 14 (dark-mode discipline) — pair this tactic when adding a light derivation to a dark default; pair Tactic 14 when adding a dark derivation to a light default.

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
- [ ] If build mixes light/dark surfaces (`.section--dark` containing light cards or vice versa) OR uses reveal animations → Tactic 17 surface-context checklist passed (Tactic 17.7)
- [ ] If build adds a non-default theme (light derivation of a dark style, or vice versa) OR introduces theme-toggle → Tactic 18 interactive-state coverage checklist passed (Tactic 18.7)
- [ ] If sensitive content → trauma-informed reference loaded (cross-reference section)

These are gates, not suggestions. Skipping them means catching the same issues in Phase 4.3 / 4.7 — wastes the self-correction loop on stuff that should never have shipped.
