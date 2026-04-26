# Loader Patterns

Load in **Phase 3 Step 3.0.06** whenever `style-tuning.axes.page-load.value` is anything other than `none`. Skip entirely if `none` (no loader markup, no JS, no failure surface).

This file is the technical contract for **page loaders** — the animation that runs before / as the page first becomes visible. It is a **separate concern** from `motion-tactics.md`, which governs in-page motion (scroll reveals, hero entrances, hover states). A page can have `motion: low` and still have `page-load: branded-intro`, or `motion: high` with `page-load: none`. They are orthogonal axes.

The file exists because, before it was added, the skill was inventing loaders silently when `motion: high` was chosen — usually a generic spinner, occasionally a curtain wipe, with no failure-mode coverage (no max-timeout, no `prefers-reduced-motion` skip, no `.js-ready` gate). The two highest-severity loader bugs were "loader never resolves" and "page hidden behind loader breaks LCP".

See also: `motion-tactics.md` (in-page motion contract — loaders count toward the High-tier "3 motion moments" budget when justifying GSAP).

---

## The 4 primitives — what every loader reduces to

Strip every loader pattern down and you get four primitives. Knowing this is what lets the skill compose new patterns instead of memorising a fixed list.

| Primitive | Mechanism | Example patterns |
|---|---|---|
| **Rotation** | Continuous loop on a transform-rotate axis | Spinner, ring, arc, orbiting dots |
| **Translation** | Movement across X / Y / radial axis | Curtain wipe, sliding panels, progress bar fill, marquee |
| **Opacity / scale** | Fade or breathe via opacity/scale interpolation | Pulse, breathing logo, fade-in, scale-in |
| **Content-mimic** | Fake the final layout structure with placeholder blocks + shimmer | Skeleton screens, image-aware shimmer |

Everything else — timing, repetition, masking, easing — is composition on top of these four. A "logo reveal" is rotation + opacity + DrawSVG path translation. A "curtain wipe" is translation + clip-path mask. A "staggered dots" is opacity + scale + delay timing.

---

## Tier compatibility — what each `page-load` value commits to

### `page-load: none`
**No file load needed beyond this row.** No loader markup, no preloader CSS, no JS. The browser paints the page natively. This is the correct default for product surfaces where speed is the brand.

When user picks `none`, **do not generate a loader of any kind** — not even a 200ms fade-in. `none` means none.

### `page-load: subtle`
**Tier requirement:** any motion tier (`low`, `medium`, `high`) is fine.

Subtle loaders are CSS-only or near-CSS-only. They mask the FOUC gap and the asset-decode gap without announcing themselves. The user notices the page loaded smoothly; they never notice that there *was* a loader.

Patterns the skill picks from for `subtle`:
- **Body fade-in** (200-400ms opacity 0 → 1 on `<body>`, gated by `.js-ready` or `document.readyState === 'complete'`)
- **Hero image shimmer** (CSS gradient sweep on the hero `<img>` placeholder until `decode()` resolves)
- **Content fade with held layout** (skeleton structure with no shimmer, just empty boxes that resolve to content with a 300ms cross-fade)

### `page-load: functional`
**Tier requirement:** `motion: medium` or `high` recommended; `motion: low` triggers the soft warn (see Tier-coupling rule).

Functional loaders communicate "wait, content coming" when the wait is real and unpredictable. They appear after the initial paint when async data or heavy assets are loading. They are not a brand statement.

Patterns the skill picks from for `functional`:
- **Skeleton + shimmer** (preferred — fastest perceived performance; mimics final structure)
- **Spinner** (only when no structural prediction is possible — global app loading, modal data fetch)
- **Progress bar** (only when actual progress is measurable — file upload, multi-step async)

### `page-load: branded-intro`
**Tier requirement:** `motion: medium` or `high` recommended; `motion: low` triggers the soft warn.

Branded intros add 600-2000ms of loader theatre before content paints. They are a brand statement. The cost is real: every millisecond delays LCP. They are justified when the brand commits to motion as identity (creative studios, agency portfolios, neo-brutalist hero pages).

Patterns the skill picks from for `branded-intro`:
- **Curtain wipe** (full-screen solid colour translates off via clip-path or transform)
- **Logo reveal** (DrawSVG stroke-dashoffset on logo paths, then fade)
- **SplitText wordmark intro** (brand wordmark assembles character-by-character, then page reveals)
- **Mask reveal** (clip-path animation reveals content from a brand shape — circle, slash, diagonal)
- **Counter+wipe** (loading percentage counts up to 100, then curtain lifts — common in agency sites)

### Tier-coupling soft warn (mirrors `style-tuning.md`)

When `motion: low` AND `page-load: functional` or `branded-intro`:

1. Build the loader as specified — do not auto-demote.
2. Surface a one-line warning in delivery summary: `Note: motion: low + page-load: <value> is unusual. The page enters with a <pattern> animation, then sits nearly static.`
3. Record in `provenance.tuning-conflicts` with `acknowledged: false`, `resolution: build-as-specified`.
4. The conflict is non-blocking.

The combination is coherent in some designs (single-statement brutalist pages, anti-spectacle product launches with a one-time intro). Trust the user; flag the conflict; keep moving.

---

## Decision matrix — picking the pattern internally

The user picks the **role** (`subtle` / `functional` / `branded-intro`). The skill picks the **pattern** based on the chosen library, the `imagery` axis, and the `corners` axis. The user never sees the pattern selector.

### `subtle` → pattern map

| Library / context | Pattern |
|---|---|
| Editorial Portfolio, Memoir Blog | Body fade-in (250ms, `cubic-bezier(.2,.7,.2,1)`) |
| Basalt E-Commerce, Warm Serene Luxury, Warm Editorial | Hero image shimmer + body fade-in |
| Technical Refined, Sanctuary Tech (rare — usually `none`) | Body fade-in only, no shimmer |
| Imagery = `photographic` | Always include hero image shimmer |
| Imagery = `type-only` | Body fade-in only |

### `functional` → pattern map

| Context | Pattern |
|---|---|
| Page has predictable structure (cards, lists, feeds) | Skeleton + shimmer |
| Page is single-region async (modal, dashboard widget) | Spinner — match style: brutalist square, soft rounded ring, sharp arc |
| Page has measurable progress (upload, multi-step) | Progress bar — match corner style |
| Imagery = `photographic` + grid | Skeleton with image-shaped boxes + shimmer |
| Corners = `sharp` | Skeleton blocks with 0px radius; spinner = bare arc, no rounded caps |
| Corners = `rounded` | Skeleton blocks with 12-16px radius; spinner = soft ring with rounded line caps |

### `branded-intro` → pattern map

| Library | Pattern |
|---|---|
| Neo-Brutalist | Curtain wipe in accent colour (sharp clip-path, no easing curve — linear or `power1.in`) |
| Creative Studio | Counter+wipe (00 → 100% counter, then curtain lifts off-top) |
| Spritify | SplitText wordmark intro with bouncy CustomEase, vibrant accent |
| Playful Bento | Logo reveal via scale+bounce, then content stagger-in |
| Editorial Portfolio (rare for branded) | Mask reveal — diagonal slash exposes hero |
| Imagery = `type-only` | SplitText wordmark intro (brand carries the moment) |
| Imagery = `3d` | WebGL canvas runs first, then fades to content |
| Has SVG logo asset | DrawSVG logo reveal preferred |
| No SVG logo asset | Curtain wipe in accent colour |

If the user provided an inspiration URL/image (Phase 1 overrides), the skill biases pattern selection toward what the reference does. A reference site with a curtain loader → curtain wipe. A reference with a logo draw → DrawSVG reveal.

---

## Failure modes — the non-negotiable patterns

These are the four bugs that ship loaders into production-broken state. Every loader pattern below implements all four guards. **No exceptions.**

### Failure 1 — Loader never resolves

The loader hides content behind `opacity: 0` and waits for a JS event (`window.load`, async fetch, asset decode) to remove the hide. If the event never fires (CDN blocked, fetch rejects unhandled, decode fails on corrupt asset), the loader stays forever. User sees a spinning spinner or a static curtain and quits.

**Mandatory pattern: max-timeout safeguard.**

```js
// Every loader registers a hard timeout that resolves it no matter what.
const LOADER_MAX_MS = 4000; // longest acceptable wait — branded intros often shorter (1500-2500)

const resolveLoader = () => {
  document.documentElement.classList.add('loader-done');
  if (window.gsap) gsap.killTweensOf('.loader');
};

const safetyTimeout = setTimeout(resolveLoader, LOADER_MAX_MS);

// When the real ready event fires, clear the timeout and resolve normally.
window.addEventListener('load', () => {
  clearTimeout(safetyTimeout);
  resolveLoader();
});
```

The `LOADER_MAX_MS` value depends on role:
- `subtle`: 800ms (the loader was meant to be invisible — never hold past one second)
- `functional` (skeleton): 6000ms (real content loads might take this long; below this is impatient)
- `functional` (spinner): 4000ms (longer than this, switch to skeleton or surface an error state)
- `branded-intro`: 2500ms (intro theatre should never exceed this on slow connections; skip the intro instead)

### Failure 2 — Loader breaks LCP

The Largest Contentful Paint metric measures when the largest in-viewport text/image element first paints. If that element is hidden behind a loader (opacity:0, display:none, behind a full-screen curtain `<div>`), LCP shifts to the loader element itself — usually a logo or empty container — and the metric gets worse, not better.

**Mandatory pattern: never gate the LCP element on the loader.**

- **Subtle** loaders apply opacity to `<body>` only briefly (200-400ms max). LCP element paints normally; the fade is visual polish.
- **Functional** loaders (skeleton) keep the same structural box dimensions as the final content — the skeleton box IS the LCP element until content fills it. Same paint timing.
- **Branded-intro** loaders use `position: fixed; z-index: 9999` over normally-painted content. The LCP element paints behind the loader at normal time; the loader covers it visually but doesn't delay paint. **Never use `display: none` on the main content during intro** — that pushes LCP to whenever the loader resolves.

```css
/* WRONG — LCP element is hidden */
.intro-active main { display: none; }

/* RIGHT — LCP element paints on time, loader sits on top */
.loader { position: fixed; inset: 0; z-index: 9999; }
.loader-done .loader { pointer-events: none; opacity: 0; transition: opacity 400ms; }
```

### Failure 3 — JS-disabled = page never appears

Same defect class as `motion-tactics.md` Tactic 17.4 (`.js-ready` gate). If the loader's "remove hide" logic is JS, and JS fails to load, the loader stays forever.

**Mandatory pattern: progressive enhancement gate.**

```css
/* Default state: NO loader visible. Page is fully readable. */
.loader { display: none; }

/* Once JS confirms it can run the loader, show it. */
.js-ready .loader { display: flex; opacity: 1; }

/* When loader resolves (real event OR safety timeout), fade out. */
.js-ready.loader-done .loader { opacity: 0; pointer-events: none; transition: opacity 400ms; }
```

```js
(function () {
  // STEP 1 — Mark JS as ready FIRST. Anything that throws above this line leaves loader hidden.
  document.documentElement.classList.add('js-ready');

  // STEP 2 — Register safety timeout immediately.
  const safetyTimeout = setTimeout(() => {
    document.documentElement.classList.add('loader-done');
  }, 4000);

  // STEP 3 — Real resolve event.
  window.addEventListener('load', () => {
    clearTimeout(safetyTimeout);
    document.documentElement.classList.add('loader-done');
  });
})();
```

This pattern means: JS loads → loader appears briefly → resolves on `window.load` or 4s timeout. JS fails → loader never appears, page is fully visible from the start. **Graceful degradation by default.**

### Failure 4 — `prefers-reduced-motion` ignored

A 2-second curtain wipe on a user with vestibular disorders is harmful. Loaders are some of the most motion-heavy moments on a page; ignoring the user's reduced-motion preference here is worse than ignoring it for hover transitions.

**Mandatory pattern: instant-resolve under reduced motion.**

```js
// At the top of the loader IIFE
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Skip the loader entirely. Add loader-done immediately.
  document.documentElement.classList.add('js-ready', 'loader-done');
  return;
}
```

```css
/* Belt-and-braces: even if JS forgets, the CSS skips the animation under reduced motion */
@media (prefers-reduced-motion: reduce) {
  .loader { display: none !important; }
  .loader * { animation: none !important; transition: none !important; }
}
```

Reduced-motion fallback is **not** "no page". Content must still appear — just without the loader theatre.

---

## Recipes

Each recipe below implements all four mandatory patterns. Copy the structure; swap tokens for the project DESIGN.md values.

### Recipe 1 — Body fade-in (subtle, CSS-only)

**Use for:** `subtle` role, any motion tier, any library. Lowest-cost loader. Masks FOUC without ceremony.

```html
<!-- No loader markup needed. The fade lives on <body> directly. -->
```

```css
/* Default: body is visible. Page works without JS. */
body { opacity: 1; }

/* JS confirms ready → switch to fade-in mode. */
.js-ready body { opacity: 0; transition: opacity 250ms cubic-bezier(.2,.7,.2,1); }
.js-ready.loader-done body { opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  .js-ready body { opacity: 1 !important; transition: none !important; }
}
```

```js
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-ready', 'loader-done');
    return;
  }
  document.documentElement.classList.add('js-ready');
  const safety = setTimeout(() => document.documentElement.classList.add('loader-done'), 800);
  // requestAnimationFrame waits for next paint — guarantees body is in opacity:0 state before transitioning
  requestAnimationFrame(() => requestAnimationFrame(() => {
    clearTimeout(safety);
    document.documentElement.classList.add('loader-done');
  }));
})();
```

### Recipe 2 — Hero image shimmer (subtle, CSS + decode())

**Use for:** `subtle` role, hero images that take >100ms to decode. Combines with Recipe 1.

```html
<div class="hero-image-frame">
  <img class="hero-image" src="hero.jpg" alt="..." />
</div>
```

```css
.hero-image-frame {
  position: relative;
  background: linear-gradient(90deg,
    var(--surface-2) 0%,
    var(--surface-3) 50%,
    var(--surface-2) 100%);
  background-size: 200% 100%;
  animation: shimmer 1.6s ease-in-out infinite;
}
.hero-image {
  opacity: 0;
  transition: opacity 400ms cubic-bezier(.2,.7,.2,1);
}
.hero-image.decoded {
  opacity: 1;
}
.hero-image.decoded ~ .hero-image-frame,
.hero-image-frame:has(.hero-image.decoded) {
  animation: none;
  background: transparent;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .hero-image-frame { animation: none; background: var(--surface-2); }
  .hero-image { opacity: 1 !important; transition: none !important; }
}
```

```js
document.querySelectorAll('.hero-image').forEach(img => {
  if (img.complete) {
    img.classList.add('decoded');
    return;
  }
  img.decode().then(() => img.classList.add('decoded')).catch(() => img.classList.add('decoded'));
  // Safety: if decode promise hangs, force-show after 3s
  setTimeout(() => img.classList.add('decoded'), 3000);
});
```

### Recipe 3 — Skeleton + shimmer (functional, CSS-only)

**Use for:** `functional` role with predictable structure. Fastest perceived performance; mimics final layout.

```html
<div class="skeleton-grid" aria-busy="true" aria-label="Loading content">
  <div class="skeleton-card"><div class="skeleton-img"></div><div class="skeleton-line w-80"></div><div class="skeleton-line w-60"></div></div>
  <div class="skeleton-card"><div class="skeleton-img"></div><div class="skeleton-line w-80"></div><div class="skeleton-line w-60"></div></div>
  <!-- repeat for grid count -->
</div>

<div class="real-grid" hidden>
  <!-- real content lives here, hidden until ready -->
</div>
```

```css
.skeleton-card {
  /* SAME box dimensions as the final card — keeps LCP stable */
  background: var(--surface-2);
  border-radius: var(--radius-card); /* matches token */
  padding: var(--space-card);
}
.skeleton-img,
.skeleton-line {
  background: linear-gradient(90deg,
    var(--surface-3) 0%,
    var(--surface-4) 50%,
    var(--surface-3) 100%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
  border-radius: var(--radius-line);
}
.skeleton-img { aspect-ratio: 16/9; }
.skeleton-line { height: 1em; margin-block: .5em; }
.skeleton-line.w-80 { width: 80%; }
.skeleton-line.w-60 { width: 60%; }

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-img, .skeleton-line { animation: none; background: var(--surface-3); }
}
```

```js
// Replace skeleton with real content when data is ready (or on max timeout)
function swapSkeleton() {
  document.querySelector('.skeleton-grid').remove();
  const real = document.querySelector('.real-grid');
  real.hidden = false;
}

const safety = setTimeout(swapSkeleton, 6000);

fetch('/api/content')
  .then(r => r.json())
  .then(data => {
    // populate .real-grid from data
    clearTimeout(safety);
    swapSkeleton();
  })
  .catch(() => { clearTimeout(safety); swapSkeleton(); /* show empty state */ });
```

### Recipe 4 — Spinner (functional, CSS-only)

**Use for:** `functional` role when no structural prediction is possible. Use sparingly — skeleton beats spinner for perceived performance.

Style variants by `corners` token:
- `sharp`: bare SVG arc, no rounded caps
- `soft`: ring with `stroke-linecap: round`, slight gradient
- `rounded`: thicker ring, softer colour, `stroke-linecap: round`

```html
<div class="spinner" role="status" aria-label="Loading">
  <svg viewBox="0 0 50 50">
    <circle cx="25" cy="25" r="20" fill="none" stroke-width="4"></circle>
  </svg>
</div>
```

```css
.spinner {
  width: 48px; height: 48px;
  animation: spin 1s linear infinite;
}
.spinner svg { width: 100%; height: 100%; }
.spinner circle {
  stroke: var(--accent);
  stroke-dasharray: 90 150;
  stroke-dashoffset: 0;
  /* Sharp variant: stroke-linecap: butt; */
  /* Soft / rounded variants: */
  stroke-linecap: round;
  animation: spin-dash 1.4s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes spin-dash {
  0% { stroke-dasharray: 1 150; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 90 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90 150; stroke-dashoffset: -125; }
}

@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; }
  .spinner circle { animation: none; stroke-dasharray: 90 150; }
}
```

### Recipe 5 — Progress bar (functional, GSAP-driven)

**Use for:** `functional` role when actual progress is measurable. Drive `.progress` value from real load events, not fake timer.

```html
<div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
  <div class="progress-bar"></div>
</div>
```

```css
.progress {
  width: 100%;
  height: 4px;
  background: var(--surface-2);
  border-radius: var(--radius-line);
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  width: 0%;
  background: var(--accent);
  border-radius: inherit;
  transform-origin: left center;
}
```

```js
const bar = document.querySelector('.progress-bar');
const progressEl = document.querySelector('.progress');

function setProgress(pct) {
  pct = Math.max(0, Math.min(100, pct));
  if (window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.to(bar, { width: pct + '%', duration: 0.4, ease: 'power2.out' });
  } else {
    bar.style.width = pct + '%';
  }
  progressEl.setAttribute('aria-valuenow', pct);
  if (pct >= 100) document.documentElement.classList.add('loader-done');
}

// Drive from real progress source (XHR onprogress, asset count, fetch readers)
// Example: track image load count
const imgs = document.images;
let loaded = 0;
Array.from(imgs).forEach(img => {
  if (img.complete) loaded++;
  else img.addEventListener('load', () => setProgress((++loaded / imgs.length) * 100));
  img.addEventListener('error', () => setProgress((++loaded / imgs.length) * 100));
});
setProgress((loaded / imgs.length) * 100);

// Safety: force-complete after 6s
setTimeout(() => setProgress(100), 6000);
```

### Recipe 6 — Curtain wipe (branded-intro, GSAP)

**Use for:** `branded-intro` for Neo-Brutalist, Editorial Portfolio (rare), any library where a single solid-colour panel is the brand statement.

```html
<div class="curtain" aria-hidden="true">
  <div class="curtain-panel curtain-panel-1"></div>
  <div class="curtain-panel curtain-panel-2"></div>
</div>
```

```css
.curtain {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  pointer-events: none;
}
.curtain-panel {
  flex: 1;
  background: var(--accent);
}
/* Two-panel split-curtain: top half lifts up, bottom half drops down */
.curtain-panel-1 { /* top — animates translateY(-100%) */ }
.curtain-panel-2 { /* bottom — animates translateY(100%) */ }

/* Initial state ONLY when JS confirms ready */
.js-ready .curtain { display: flex; }

@media (prefers-reduced-motion: reduce) {
  .curtain { display: none !important; }
}
```

```js
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-ready', 'loader-done');
    return;
  }
  document.documentElement.classList.add('js-ready');

  const safety = setTimeout(runCurtain, 2500);

  function runCurtain() {
    clearTimeout(safety);
    if (!window.gsap) {
      document.querySelector('.curtain').style.display = 'none';
      document.documentElement.classList.add('loader-done');
      return;
    }
    const tl = gsap.timeline({
      onComplete: () => {
        document.querySelector('.curtain').remove();
        document.documentElement.classList.add('loader-done');
      }
    });
    tl.to('.curtain-panel-1', { yPercent: -100, duration: 0.9, ease: 'power3.inOut' }, 0.3)
      .to('.curtain-panel-2', { yPercent: 100, duration: 0.9, ease: 'power3.inOut' }, 0.3);
  }

  if (document.readyState === 'complete') runCurtain();
  else window.addEventListener('load', runCurtain);
})();
```

**Variants:**
- Single panel sliding off-top: drop `.curtain-panel-2`, animate single panel `yPercent: -100`
- Diagonal wipe: replace transform with `clip-path: polygon(...)` interpolation
- Counter+wipe: prepend a `<div class="curtain-counter">00</div>` that increments via `gsap.to({val: 0}, {val: 100, duration: 1.4, snap: 'val', onUpdate: ...})` before the wipe runs

### Recipe 7 — Logo reveal with DrawSVG (branded-intro, Club GSAP)

**Use for:** `branded-intro` when project has an SVG logo. The most "designed" loader — strokes draw themselves, then fade to content.

Requires Club GSAP (`DrawSVGPlugin`). Verify license before using outside Webflow.

```html
<div class="logo-loader" aria-hidden="true">
  <svg viewBox="0 0 200 60" class="logo-svg">
    <path class="logo-path" d="M10,30 L40,10 L70,30 L40,50 Z" fill="none" stroke="var(--accent)" stroke-width="2" />
    <!-- additional paths -->
  </svg>
</div>
```

```css
.logo-loader {
  position: fixed; inset: 0; z-index: 9999;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg);
}
.logo-svg { width: 200px; height: auto; }
.js-ready .logo-loader { display: flex; }
@media (prefers-reduced-motion: reduce) {
  .logo-loader { display: none !important; }
}
```

```js
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-ready', 'loader-done');
    return;
  }
  document.documentElement.classList.add('js-ready');
  const safety = setTimeout(resolve, 2500);

  function resolve() {
    clearTimeout(safety);
    if (!window.gsap || !window.DrawSVGPlugin) {
      document.querySelector('.logo-loader').style.display = 'none';
      document.documentElement.classList.add('loader-done');
      return;
    }
    gsap.registerPlugin(DrawSVGPlugin);
    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to('.logo-loader', {
          opacity: 0, duration: 0.5, ease: 'power2.out',
          onComplete: () => {
            document.querySelector('.logo-loader').remove();
            document.documentElement.classList.add('loader-done');
          }
        });
      }
    });
    tl.from('.logo-path', { drawSVG: '0%', duration: 1.2, stagger: 0.1, ease: 'power2.inOut' });
  }

  if (document.readyState === 'complete') resolve();
  else window.addEventListener('load', resolve);
})();
```

### Recipe 8 — SplitText wordmark intro (branded-intro, Club GSAP)

**Use for:** `branded-intro` when imagery is `type-only` or the brand wordmark IS the identity. Characters or words assemble in.

Requires Club GSAP (`SplitText`).

```html
<div class="wordmark-loader" aria-hidden="true">
  <h1 class="wordmark">YOUR BRAND</h1>
</div>
```

```css
.wordmark-loader {
  position: fixed; inset: 0; z-index: 9999;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg);
}
.wordmark {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 6rem);
  letter-spacing: -0.02em;
  margin: 0;
}
.js-ready .wordmark-loader { display: flex; }
.js-ready .wordmark .char { opacity: 0; display: inline-block; }
@media (prefers-reduced-motion: reduce) {
  .wordmark-loader { display: none !important; }
}
```

```js
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-ready', 'loader-done');
    return;
  }
  document.documentElement.classList.add('js-ready');
  const safety = setTimeout(resolve, 2500);

  function resolve() {
    clearTimeout(safety);
    if (!window.gsap || !window.SplitText) {
      document.querySelector('.wordmark-loader').style.display = 'none';
      document.documentElement.classList.add('loader-done');
      return;
    }
    gsap.registerPlugin(SplitText);
    const split = new SplitText('.wordmark', { type: 'chars', charsClass: 'char' });
    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to('.wordmark-loader', {
          opacity: 0, duration: 0.5, delay: 0.4, ease: 'power2.out',
          onComplete: () => {
            split.revert();
            document.querySelector('.wordmark-loader').remove();
            document.documentElement.classList.add('loader-done');
          }
        });
      }
    });
    tl.to(split.chars, {
      opacity: 1,
      yPercent: 0,
      duration: 0.6,
      stagger: 0.04,
      ease: 'power3.out'
    }).from(split.chars, { yPercent: 80 }, 0);
  }

  if (document.readyState === 'complete') resolve();
  else window.addEventListener('load', resolve);
})();
```

### Recipe 9 — Mask reveal (branded-intro, GSAP + clip-path)

**Use for:** `branded-intro` when the brand has a signature shape (slash, circle, hex). Content paints behind a mask that animates out.

No Club GSAP needed — pure GSAP core.

```html
<!-- The whole page lives inside .masked-content. The mask animates its clip-path. -->
<div class="masked-content">
  <!-- existing page markup -->
</div>
```

```css
.js-ready .masked-content {
  clip-path: polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%);
}
.js-ready.loader-done .masked-content {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}
@media (prefers-reduced-motion: reduce) {
  .masked-content { clip-path: none !important; }
}
```

```js
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-ready', 'loader-done');
    return;
  }
  document.documentElement.classList.add('js-ready');
  const safety = setTimeout(resolve, 2500);

  function resolve() {
    clearTimeout(safety);
    if (!window.gsap) {
      document.documentElement.classList.add('loader-done');
      return;
    }
    gsap.to('.masked-content', {
      clipPath: 'polygon(0 0, 100% 0, 100% 100%, 0 100%)',
      duration: 1.2,
      ease: 'power3.inOut',
      onComplete: () => document.documentElement.classList.add('loader-done')
    });
  }

  if (document.readyState === 'complete') resolve();
  else window.addEventListener('load', resolve);
})();
```

**Variants by shape:**
- Diagonal slash: `clip-path: polygon(0 0, 50% 0, 0 100%)` → full polygon
- Circle reveal: `clip-path: circle(0% at center)` → `circle(150% at center)`
- Vertical wipe: `clip-path: inset(50% 0 50% 0)` → `inset(0 0 0 0)`

---

## Per-library default recipes

When `page-load` is set (not `none`), these are the default pattern picks per library before user overrides. The skill records the pick in `style-tuning.axes.page-load.pattern`.

| Library | Default role | Default pattern |
|---|---|---|
| **Neo-Brutalist** | branded-intro | Curtain wipe (Recipe 6) — single solid panel in accent, sharp `power1.in` ease |
| **Editorial Portfolio** | subtle | Body fade-in (Recipe 1) + hero image shimmer (Recipe 2) |
| **Technical Refined** | none | (no loader) |
| **Basalt E-Commerce** | subtle | Body fade-in + hero image shimmer (product images decode) |
| **Memoir Blog** | none | (no loader — reading-first, speed matters) |
| **Creative Studio** | branded-intro | Counter+wipe (Recipe 6 variant) — counter to 100, then split-curtain lift |
| **Warm Serene Luxury** | subtle | Body fade-in + hero image shimmer with warm `--surface` tones |
| **Playful Bento** | branded-intro | Logo reveal (Recipe 7) with bouncy CustomEase, OR scale-in if no SVG logo |
| **Spritify** | branded-intro | SplitText wordmark intro (Recipe 8) — vibrant accent, kid-friendly bounce |
| **Sanctuary Tech** | none | (no loader — anti-spectacle by design; trauma-informed contexts must NOT have surprise motion) |
| **Warm Editorial** | subtle | Body fade-in (Recipe 1) only — minimal ceremony, parchment background |
| **Custom / Freestyle** | derived from user answers | Pattern picked from decision matrix above |

**Sanctuary Tech is locked.** Even if user picks `branded-intro` while in trauma-informed mode, demote to `subtle` (Recipe 1 only) and document in provenance. Surprise full-screen motion can be re-traumatising. This is the only auto-demote in the file; rationale is `trauma-informed.md`.

---

## Webflow-specific notes

When deploying to Webflow:

- **Inject the loader markup** in Page Settings → Custom Code → "Inside `<head>` tag" for the CSS and the `<div class="loader">` placeholder, OR in the page's first Embed block in Designer. The loader must paint before the Webflow page renders to mask the FOUC.
- **Inject the loader JS** in Page Settings → Custom Code → "Before `</body>` tag", AFTER the GSAP CDN scripts loaded site-wide in Project Settings → Custom Code → Footer. The order matters — `window.gsap` must exist when the loader IIFE runs.
- **Club GSAP plugins** (DrawSVG, SplitText) are **bundled with Webflow paid plans**. The site you ship from Webflow has access; ports off-Webflow need a separate Club GSAP membership.
- **Webflow IX2 page-load animations** can coexist with custom GSAP loaders, but should not target the same elements. Pick one orchestration layer per element. Generally: IX2 for hover/scroll micro-interactions, custom GSAP for the loader and signature moments.
- **For Flow-Goodies / Flowbridge integrations** GSAP is already loaded site-wide — check `window.gsap` and `window.DrawSVGPlugin` / `window.SplitText` before initialising. Don't re-import.
- **`prefers-reduced-motion`** must be tested in the Webflow Designer preview AND in the published site. Designer may not honour the OS-level setting; published site does.

---

## Pre-build checklist

Before marking a build with a loader complete, verify:

- [ ] `style-tuning.axes.page-load.value` is recorded in DESIGN.md frontmatter
- [ ] `style-tuning.axes.page-load.pattern` is recorded (the internal pick, e.g., `curtain-wipe`, `skeleton-shimmer`)
- [ ] If `value: none` → NO loader markup or JS shipped
- [ ] If `value: subtle` → loader resolves within 800ms max
- [ ] If `value: functional` → loader resolves within 4-6s max (skeleton 6s, spinner 4s)
- [ ] If `value: branded-intro` → loader resolves within 2.5s max
- [ ] **`.js-ready` gate present**: loader is hidden by default in CSS, only shown after JS confirms ready
- [ ] **Safety timeout present**: `setTimeout(resolveLoader, MAX_MS)` registered at IIFE start
- [ ] **`prefers-reduced-motion` check at IIFE top**: if reduced, loader skipped entirely (`loader-done` class added immediately)
- [ ] **CSS belt-and-braces**: `@media (prefers-reduced-motion: reduce)` disables loader animations even if JS forgets
- [ ] **LCP element NOT gated by loader**: main content paints normally; loader sits on top via `position: fixed`. Verify with Lighthouse — LCP should not regress vs `page-load: none`
- [ ] **Disable-JS test passes**: page renders fully readable in DevTools with JS disabled. No loader hangs. No invisible content.
- [ ] **GSAP-failure test passes**: temporarily block `cdn.jsdelivr.net` in DevTools → reload. Loader either skips gracefully OR uses non-GSAP fallback. Page never hangs.
- [ ] **Tier-coupling conflict logged**: if `motion: low` + `functional`/`branded-intro`, `provenance.tuning-conflicts` contains the entry, delivery summary includes the warning line
- [ ] **Sanctuary Tech / trauma-informed**: if active, page-load is `none` or `subtle` only — never `functional` or `branded-intro`, regardless of user pick (auto-demote, log in provenance)
- [ ] **Webflow deployment** (if applicable): Club GSAP plugins listed in delivery summary with license note; loader CSS in `<head>`; loader JS Before `</body>`; tested in published site, not just Designer preview

---

## Audit questions (Phase 4 loader lens)

When `page-load != none`, run these alongside the motion lens (`motion-tactics.md` § Audit questions):

1. **Does the loader resolve in every failure scenario?** Manually test: JS disabled, GSAP CDN blocked, network throttled to 3G, reduced-motion enabled. The loader must resolve (or skip) in all four.
2. **Does the loader serve the brand?** A spinner is functional, not branded. A curtain wipe with no easing curve and a default colour is generic. If removing the loader doesn't change the brand impression, demote to `subtle` or `none`.
3. **Is the loader's timing under control?** Branded intros longer than 2.5s frustrate even patient users. Test with `LOADER_MAX_MS` halved — does the build still feel right?
4. **Does the loader regress LCP?** Run Lighthouse before and after adding the loader. If LCP shifts by >200ms, the LCP element is gated by the loader — refactor (use `position: fixed` overlay, not `display: none` on main).
5. **Is the loader role consistent with motion tier?** If `motion: low` + `branded-intro`, has the warning been surfaced? Has the conflict been logged?
6. **Does the skeleton match the final layout?** Skeleton boxes that don't match real content dimensions cause layout shift when content arrives — that's worse than no skeleton. Measure CLS before and after.
7. **Is `prefers-reduced-motion` actually honoured?** Toggle the setting in DevTools → Rendering → Emulate CSS prefers-reduced-motion. The loader must skip entirely — not "play faster", not "play once". Skip.
