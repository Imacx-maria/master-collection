# Motion Principles

Load in **Phase 3 Step 3.0.04** whenever `style-tuning.axes.motion.value` is `medium` or `high`. Skip if `low` (the principles still apply, but a `low` page has no motion budget worth auditing — the hover transition rule is in `base-principles.md` and is enough).

This file is the **design lens** for motion. It defines the vocabulary, timing thresholds, easing intent, and audit framework that govern *whether* and *why* motion belongs on a page. It does not specify build tooling — that's `motion-tactics.md` (CSS-only contract for `medium`, GSAP contract for `high`).

**Read this file BEFORE `motion-tactics.md`.** Tactics without principles produces "more CSS animations" interpreted as design — which is what the skill used to do. Principles first, then tactics.

**Sibling files:**
- `motion-tactics.md` — technical contract per tier (what runtime, what plugins, failure modes, performance budget)
- `loader-patterns.md` — page-load contract (what plays *before* the page becomes visible — orthogonal axis)
- `base-principles.md` Q9 — universal "does motion support the style" audit lens

---

## The taxonomy — animation vs micro-interaction vs functional motion

The skill currently uses "motion" as one bucket. That is the wrong granularity. Three distinct categories live inside it, each with a different job:

| Category | Primary objective | Trigger | Perceptual weight | Where the skill applies it |
|---|---|---|---|---|
| **Animation** | Storytelling, branding, hierarchy | System-initiated or page-load | High emotional weight; "captures" attention | Hero entrances, branded-intro loaders, scroll-driven sequences, illustration reveals |
| **Micro-interaction** | Functional feedback, confidence | User-initiated (click, hover, focus, tap) | Builds trust; feels responsive and "alive" | Button press states, form validation, toggle switches, copy-confirmed pulses |
| **Functional motion** | Guidance, orientation, spatial continuity | Navigation-driven (scroll, route change, layout reflow) | Maintains spatial awareness | Page transitions, accordion expand/collapse, FLIP layout interpolation, scroll snap |

**The guiding principle:** *animation is for show, micro-interaction is for flow, functional motion is for orientation.* If a piece of motion can't be assigned to one of the three, it does not belong on the page.

**Why this matters for the skill:** the audit lens differs per category. A hero entrance is judged on emotional fit and brand voice. A button micro-interaction is judged on responsiveness (≤100ms feedback, ≤200ms full state change). A page transition is judged on spatial coherence (the new view must arrive from the direction the link telegraphed).

When reviewing a build at Phase 4, classify every animated element into one of the three buckets first. Then apply the correct lens. A "scroll reveal that's beautiful but slow" is the right complaint for an *animation*; the same critique on a *micro-interaction* would be wrong because the bucket itself is wrong.

---

## The Four Pillars of micro-interactions (Dan Saffer)

Every micro-interaction has four parts. Naming them lets the skill audit each one independently instead of judging the whole as "feels fine".

### 1. Trigger
The spark that begins the interaction. **Manual triggers** are user-initiated (click, hover, focus, tap, swipe). **System triggers** are automatic (notification arriving, validation completing, error firing). Every interactive element must have an obvious trigger surface — if the user can't tell what initiates the motion, the motion has no audience.

**Audit:** is the trigger surface visible at rest? A button that only animates on hover but has no resting visual difference from plain text fails. The trigger must be discoverable before it's pulled.

### 2. Rules
The constraints that govern what happens after the trigger fires. Rules are the invisible logic — what state transitions, what data validates, what direction the panel slides. Rules are what make motion *predictable*. Predictability is what reduces cognitive load.

**Audit:** does the same trigger always produce the same motion? If a card hover sometimes lifts 4px and sometimes 8px depending on screen position, the rule is leaking. Pin it.

### 3. Feedback
The visual / auditory / haptic evidence that the rules are running. Feedback is the most user-facing pillar — it's what confirms the click registered. **Feedback must be brief and precise.** An overly elaborate response to a simple action feels sluggish and intrusive.

**Audit:** does feedback land within 100ms of the trigger? If not, the user re-clicks, doubling the action.

### 4. Loops & Modes
The meta-rules. **Loops** govern repetition and duration (a progress bar runs until upload completes; a spinner runs until response arrives). **Modes** are temporary states that change the interface's function (long-press reveals contextual menu; drag mode disables scroll). Loops and modes are how micro-interactions "remember" what's happening.

**Audit:** does the loop have an exit condition? A spinner with no max-timeout is a failure mode. A mode with no exit affordance is a trap.

**Application rule:** every micro-interaction the skill ships must have all four pillars accounted for, even if some are trivial (a button hover has Trigger=hover, Rules=none, Feedback=color shift + 1px lift, Loop=none, Mode=none — three of four are trivial, but they're documented).

---

## Temporal design — the duration table

The single most common motion failure is bad timing. Too fast = users miss the transition (perceived as flicker). Too slow = users perceive the interface as lagging.

This table is **canonical for the skill**. Pull from it; do not invent durations.

| Interaction type | Duration (ms) | Functional goal | Example |
|---|---|---|---|
| **Button feedback** | 80–100 | Immediate confirmation of "pressed" state | `:active` color/shadow shift |
| **Hover state** | 150–250 | Quick but noticeable affordance change | Card lift, link underline grow |
| **Micro-interaction** | 150–200 | Status change with light delight | Toggle switch, form validation tick |
| **Standard UI transition** | 200–300 | Natural movement for small UI elements | Dropdown open, tooltip appear |
| **Modal entrance** | 300–400 | Gentle entrance for content shift | Dialog scale-in, sheet slide-up |
| **Contextual page slide** | 300–500 | Maintains orientation during full-screen shift | Route transition, drawer open |
| **Hero scroll reveal** | 600–900 | Editorial pacing, deliberate weight | Headline fade-up, illustration scale |
| **Success / celebration** | 600–1000 | Intentional slow to emphasise achievement | Confirmation checkmark, completion burst |
| **Ambient loop** | 3000–10000 | Background presence, never demands attention | Float, pulse, gradient shift |

### The two thresholds you cannot ignore

**100ms — the perception of immediacy.** Below 100ms, feedback feels instantaneous. Above 100ms, the user perceives a delay. For micro-interactions specifically, the *first frame* of feedback must paint within this budget — even if the full animation is longer. Use `transition-delay: 0` and a snappy first frame.

**The 20% rule (Weber-Fechner).** Humans don't perceive duration differences below ~20%. A change from 200ms to 220ms is invisible; 200ms to 250ms is the minimum *audible* shift. Tune in 50ms increments, not 10ms.

### When to stretch above the table

- **Brand commitment to slow craft.** Editorial / luxury / hospitality sites can intentionally push to 1200–1500ms for hero moments. Document this as a brand decision, not "more is better".
- **Inertia continuing user motion.** A swipe carries momentum. A dismiss-on-drag should fade out over the time it takes the gesture to complete its arc — not a fixed 300ms.
- **Pause between staged elements.** A timeline of 4 staggered headlines at 150ms stagger × 800ms each is a 1.5s entrance. That's correct for a hero. It's wrong for a tooltip.

### When to compress below the table

- **High-frequency repeats.** If the user fires the same micro-interaction 10× in a row (typing in a chat, sending reactions), every animation should be on the *floor* of its range or below. 150ms hover that fires 30×/minute = 4.5s of animation per minute. Cut to 80ms.
- **Forms with immediate validation.** Field validation lights green in 100ms, not 200ms. Anything slower reads as the field "thinking", which makes the user re-read what they typed.

---

## Easing — intent before curve

Every easing curve has an *intent*. Picking by feel produces inconsistency; picking by intent produces a system.

### The three intent categories

**Ease-out (deceleration) — for elements ENTERING the screen.**
The element starts fast and slows down. The fast start makes the interface feel responsive; the slow finish lets the eye settle on the destination. **Default for 80% of UI motion.**

Recommended curves:
- `cubic-bezier(0.2, 0.7, 0.2, 1)` — the skill's signature ease-out (already used in motion-tactics.md)
- `cubic-bezier(0.33, 1, 0.68, 1)` — Material Design `easeOutCubic`
- `cubic-bezier(0, 0, 0.2, 1)` — Material Design `easeOutQuart` (snappier)

**Ease-in (acceleration) — for elements LEAVING the screen permanently.**
The element starts slow and speeds up, suggesting it's gaining velocity to depart. Use sparingly — ease-in feels heavy and slow at the start, which is wrong for most cases. **Only when the element won't return** (closing modal, dismissing notification, deleting an item).

Recommended curves:
- `cubic-bezier(0.4, 0, 1, 1)` — `easeInQuad`
- `cubic-bezier(0.55, 0.085, 0.68, 0.53)` — `easeInCubic`

**Ease-in-out (acceleration + deceleration) — for elements MOVING WITHIN the screen.**
The element accelerates and decelerates symmetrically. Used when the element doesn't enter or leave, just moves to a new position (accordion expand, layout reflow, drawer slide between two anchored states).

Recommended curves:
- `cubic-bezier(0.4, 0, 0.2, 1)` — Material's standard "emphasized" easing
- `cubic-bezier(0.65, 0, 0.35, 1)` — `easeInOutCubic` (gentle)
- `cubic-bezier(0.83, 0, 0.17, 1)` — `easeInOutQuint` (dramatic)

### Linear is wrong for UI

Linear motion (constant speed) appears robotic to the human eye. Reserve it for two cases only:
- **Continuous loops** that don't have a "start" or "end" — spinners, marquees, loading bars without progress
- **Scrub-driven scroll animations** — when scroll position drives the animation timeline, easing on each frame compounds and feels wrong; let the user's scroll velocity provide the curve

For everything else: never `linear`.

### Signature easing per project

Generic eases (`power2`, `easeOutCubic`, `ease`) feel default. A **project signature ease** — one custom cubic-bezier or `CustomEase` curve used across all hero / brand moments — is the difference between "animated" and "designed". Establish it once in DESIGN.md, reuse everywhere.

```css
/* DESIGN.md example */
--ease-signature: cubic-bezier(0.16, 1, 0.3, 1);  /* "verum-out" — fast start, very slow finish */
--ease-fast: cubic-bezier(0.4, 0, 0.2, 1);         /* standard ease for UI */
--ease-slow: cubic-bezier(0.65, 0, 0.35, 1);       /* in-out for layout reflow */
```

### Forbidden — mixing 4+ easing curves on one page

Picking `power2` for hero, `expo.out` for cards, `elastic` for buttons, and `bounce` for icons reads as un-designed. The skill picks **1–2 curves + 1 signature** per project and sticks with them.

---

## Spring physics vs fixed timing

Modern design systems (Material 3, iOS, React Spring) have moved toward spring-based motion. Instead of specifying duration + curve, the designer specifies physical attributes:

| Property | What it controls | Higher = | Lower = |
|---|---|---|---|
| **Stiffness (tension)** | How quickly motion starts | Faster, more force | Slower, gentler |
| **Damping (friction)** | How quickly motion stops | Less bouncing, settles fast | More oscillation, "wobbly" |
| **Mass** | Perceived weight | Sluggish, takes longer | Light, quick to move |

**Why spring sometimes beats fixed timing:** spring physics responds to user velocity. If a user swipes a card fast, a spring system carries that momentum into the animation. A fixed `300ms ease-out` ignores the user's physical input and feels disconnected.

### When to reach for spring

- **Drag-and-release interactions.** Throwable cards, swipe-to-dismiss, pull-to-refresh — the release should carry the user's velocity, not snap to a default duration.
- **Bouncy / playful brand voice.** Spritify, Playful Bento, kid-facing products. A spring with low damping (0.6–0.7) gives the bounce that fixed cubic-bezier can only fake clumsily.
- **Layout reflows after drag.** When a user reorders a list, the surrounding items should spring into their new positions, not slide on a fixed timer.

### When to stay with fixed timing

- **UI state transitions that must feel uniform.** Every dropdown opens identically. Every modal slides up identically. Spring's velocity-responsiveness is a *bug* here — consistency wins.
- **Brand voices that read "considered" not "playful".** Editorial, Memoir, Sanctuary Tech, Warm Editorial. Fixed cubic-bezier with restrained durations.
- **Performance-critical paths.** Spring solvers compute every frame; fixed easings are pre-computed curves. On a low-end device, spring on 50 simultaneous elements is jank — fixed easing is not.

### Signature spring per project (when used)

```js
// Spritify-style bouncy spring
const playfulSpring = { stiffness: 280, damping: 18, mass: 1 };

// Creative Studio-style snappy spring
const studioSpring = { stiffness: 400, damping: 30, mass: 0.8 };

// Warm Editorial-style gentle spring (rarely springy at all)
const editorialSpring = { stiffness: 180, damping: 28, mass: 1.2 };
```

---

## Friction model — for scroll and gestures

Scrolling and gestural interfaces are governed by friction, not by deceleration. **Constant deceleration** (a quadratic function of time) feels mechanical. **Friction** (a power function where time is the exponent) feels physical.

The friction coefficient typically lives between `0.0001` and `0.01` for web applications. Different surfaces want different coefficients:

| Context | Friction | Why |
|---|---|---|
| **Long list flick** (Contacts-style) | Low (`~0.0005`) | User wants to fling through hundreds of items quickly |
| **Reading content** (article, blog) | High (`~0.005`) | Preserve reading focus; over-scroll feels disrespectful |
| **Map / canvas pan** | Medium (`~0.001`) | Balance between exploration and precision |
| **Photo gallery** | Low–medium (`~0.0008`) | Fast browsing with controlled stops |

The skill rarely overrides native scroll friction — but when it does (with libraries like Lenis, ScrollSmoother), the coefficient is a design decision, not a default. Document the choice in DESIGN.md if non-default.

---

## C.U.R.E. — the audit framework

Use this in Phase 4 motion review. Every motion moment in the build is judged against four questions:

### **C — Context**
*What is the user doing right now?* Motion that fits a marketing landing page disrupts a SaaS dashboard. A full-screen reveal during a data-entry task is a disruption, no matter how beautiful.

**Failure signals:**
- Animations that interrupt task flow
- Motion that hides controls the user is reaching for
- Loaders on pages where the user is mid-action

### **U — Usefulness**
*Does the motion clarify a relationship or indicate status?* If the animation is purely decorative, it should be the first thing cut. The bar is high: motion must do work.

**Useful motion examples:**
- Accordion expand → "this content was always here, just hidden" (preserves mental map)
- FLIP transition during sort → "items reordered, here's where they went"
- Skeleton screen → "structure is loading, here's what to expect"

**Decorative motion examples (cut on sight):**
- Background gradient that shifts colour every 8 seconds with no semantic meaning
- Hero illustration that rotates 360° on page load with no narrative reason
- Card hover that animates 4 properties at different durations for "richness"

### **R — Restraint**
*How many things move?* Performance is improved by limiting moving parts. Overloading a page with motion overwhelms neurodivergent users and produces "motion noise" — where everything competes for attention and nothing wins.

**Hard rule:** at most **one signature motion moment per page**. A page with 12 equal-weight animations has no hierarchy.

**Restraint test:** disable all motion on the page mentally. Which animation would you reinstate first? That's the signature. The rest are candidates for cutting.

### **E — Emotion**
*Does the motion convey the right brand voice?* Motion is one of the most direct ways a product expresses personality. A finance app that uses bouncy springs feels unserious. A kids' product with stiff fixed easings feels cold.

**Brand voice → motion personality map:**
- **Playful, energetic** → high stiffness + low damping springs, bouncy curves, overshoot
- **Considered, editorial** → fixed timing, ease-out, longer durations (700–900ms)
- **Technical, clinical** → fast fixed timing (150–250ms), `power2.out`, no overshoot
- **Warm, hospitable** → medium springs with high damping (no bounce), gentle in-out
- **Bold, brutalist** → minimal motion overall; when present, sharp + fast (100–200ms)

C.U.R.E. is run **per motion moment**, not per page. A single page can have a C-failure on one element and a clean run on the rest.

---

## Performance — what's safe to animate

Browsers process layout in three stages: **Layout → Paint → Composite**. Animating properties that force Layout or Paint recalculation = jank. Animating properties handled in Composite = smooth.

### The GPU-only rule

Animate **only** these properties for 60fps performance:

- `transform` (translate, scale, rotate, skew)
- `opacity`
- `filter` (with caveats — heavy on low-end GPUs)
- `clip-path` (modern browsers)

**Forbidden in animations** (force Layout / Paint recalculation):
- ❌ `width`, `height` — use `transform: scale()` or `clip-path`
- ❌ `top`, `left`, `right`, `bottom` — use `transform: translate()`
- ❌ `margin`, `padding` — restructure with flex/grid + transform
- ❌ `border-width` — animate `box-shadow` or pseudo-elements instead
- ❌ `font-size` — animate `transform: scale()` on a wrapper

**Composite-stage hint:**
```css
.animated-element {
  will-change: transform, opacity;
}
```

Use `will-change` sparingly — it consumes GPU memory. Add it before the animation starts, remove it after.

### LCP and motion

Hero entrances must not block Largest Contentful Paint. The headline must paint visibly within the LCP budget (<2.5s on 3G). If GSAP is hiding the headline at `opacity: 0` before reveal, the headline isn't in the LCP — that's a regression.

**Fix:** use `.js-ready` gate (motion-tactics.md § Required pattern). The CSS hiding only applies *after* JS confirms it can run the animation.

---

## Accessibility — the non-negotiables

Approximately **15% of users** experience some form of vestibular (inner ear) or photosensitivity disorder. Motion accessibility is a health requirement, not a polish item.

### WCAG criteria the skill enforces

| Criterion | Level | What it requires |
|---|---|---|
| **2.2.2 Pause, Stop, Hide** | A | Any moving / blinking content that auto-starts and runs >5 seconds must have a pause/stop control |
| **2.3.1 Three Flashes** | A | No content flashes more than 3 times per second (seizure risk) |
| **2.3.3 Animation from Interactions** | AAA | Users can disable non-essential animations triggered by their own actions (e.g., parallax) |

### `prefers-reduced-motion` — what "reduced" actually means

The reduced-motion fallback is **not** "no animation". Content must still appear. Replace 600ms reveals with 0ms reveals (instant), not "never reveal".

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

For JS-driven animations (GSAP), branch at the top:

```js
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Apply final state immediately
  gsap.set(targets, { opacity: 1, y: 0, clearProps: "all" });
  return;
}
```

### The 5-second rule (WCAG 2.2.2)

Any continuous motion that auto-starts and lasts >5 seconds **must** be pausable. This rules out:
- ❌ Auto-playing video without pause control
- ❌ Auto-rotating carousel without pause-on-hover or explicit pause button
- ❌ Background gradient animations that never stop with no escape

If the motion is decorative (ambient float, breathing logo) and loops indefinitely, it must either:
1. Be subtle enough that it's not "moving content" in a WCAG sense (a 3% scale pulse over 8s likely qualifies — judgment call)
2. Have a documented pause affordance

When in doubt, gate ambient loops behind `prefers-reduced-motion` and ship a pause toggle for non-decorative auto-play.

### The three-flash rule (WCAG 2.3.1)

No motion may flash more than 3 times per second (red flashes are most dangerous). This is rarely a concern in modern UI but applies to:
- Strobe-effect loaders
- Aggressive error pulses (a 200ms red flash repeated 5×/sec on a wrong-password shake)
- Decorative "glitch" effects on hero text

If a motion flashes faster than 3Hz, slow it down or replace with a non-flashing pattern.

---

## Pattern catalog — common micro-interactions worth knowing

These are reference patterns for the skill to reach for when designing per-element motion. Each is described by its job, not its visual treatment.

### Feedback patterns

**Button ripple / bubble.** Visual wave originating from the click point. Confirms exactly where the user touched. Strong on mobile (touch target verification). Mild on desktop (cursor already shows position).

**Shake-for-error.** Horizontal shake (3–5px translation, 4–6 cycles, ~400ms total) on a form field or login form when validation fails. References the physical "no" head shake; communicates rejection without reading copy.

**Pulse confirmation.** Brief scale-up (1.0 → 1.08 → 1.0 over 200ms) on an icon or button after a successful action. "Heart" icon liked, "saved" icon confirmed.

**Celebratory burst.** Confetti, particle spray, animated mascot crossing the screen. Reserved for milestones (task complete, payment confirmed, achievement unlocked). Asana's "celebratory creatures" are the canonical example. Use ≤1×/session — overuse breaks the dopamine loop.

### Navigation patterns

**Pull-to-refresh.** Vertical drag past a threshold triggers reload. Originated in Tweetie 2009. Works because: (1) the threshold logic is forgiving; (2) the spinner appears as immediate feedback; (3) the gesture is reversible if released early.

**Swipe-to-reveal.** Horizontal swipe on a list item reveals hidden actions (delete, archive, flag). Reduces on-screen clutter for secondary actions. Works on mobile lists; weak on desktop without a clear affordance.

**Accordion expand.** Clicking a row expands it inline to reveal more content. Motion confirms "this content was always here, hidden" — preserves the user's mental map. Animate `max-height` (with care — Layout cost) or use a scaleY transform on the inner.

**Page slide transition.** Route change slides the new view in from the direction of the link (right link → enters from right). Maintains spatial coherence. Requires View Transitions API or framework router cooperation.

### Status patterns

**Skeleton screen.** Gray boxes that mimic the shape of the final content while loading. Reduces perceived wait time vs spinner because users see the layout coming. Use when wait is ≥500ms and structure is predictable.

**Typing indicator.** Pulsing dots in a chat interface while the other party types. Real-time status; reduces silence anxiety. Three dots, staggered opacity loop, ~1.4s cycle.

**Progressive auto-fill.** Suggestions appear inline as the user types. Reduces data-entry friction by predicting intent. Animate the suggestion list with a fast (150–200ms) slide-in.

**Progress bar with backward texture.** A progress bar where the internal pattern flows opposite to the fill direction. Tricks perception into reading the wait as faster (research-backed: up to 11% perceived reduction). Use for any wait >2s.

### Orientation patterns

**FLIP layout transition.** When DOM mutates (sort, filter, expand), capture the start state, apply the new layout, animate the delta. Buttery layout interpolation. GSAP Flip plugin is the standard.

**Parallax depth.** Background, midground, foreground scroll at different rates. Communicates depth, not "we have animations". **Desktop-only** — mobile parallax is jank.

**Pinned scroll sequence.** A section pins while a sequence plays out as the user scrolls. Used for product reveals, before/after comparisons, multi-step explainers. Budget: at most one per page.

---

## Apple HIG vs Material Design — when each philosophy applies

Two dominant design philosophies, two different approaches to motion. The skill picks per project.

| Philosophy | Core metaphor | Motion priority | Depth indicator | When to lean this way |
|---|---|---|---|---|
| **Material Design** | Paper + ink, rationalised space | Expressive, physics-based | Shadows + Z-axis elevation | Android products, productivity apps, expressive brands, builds where motion *is* the brand |
| **Apple HIG** | Natural interaction, deference | Subtle, brief, cancelable | Blur + translucency | iOS products, premium tech, restraint-first brands, builds where motion serves content |

### Apple HIG's four motion rules (worth internalising)

1. **Brevity.** Motion should be quick. If a view slides down from the top, it dismisses sliding up — never broken.
2. **Cancelability.** Users must never wait for an animation to finish before they can act. Tap mid-animation = animation ends instantly, action proceeds.
3. **Spatial coherence.** Reverse the direction on dismissal. The mental map must hold.
4. **Translucency over shadows.** Depth via blur, not via z-elevation drop shadows.

### Material Design's two motion schemes

**Standard.** Functional, minimal. Used for productivity contexts and apps where motion shouldn't distract.

**Expressive.** Springs that overshoot their final value to add a subtle bounce. Used for brands and contexts where motion is part of personality.

The skill picks Standard by default. Expressive is opted into via `motion: high` + a brand voice that warrants it (Spritify, Playful Bento, Creative Studio).

---

## Audit checklist — Phase 4 motion lens

Run when `motion != low`. Builds on the existing audit in `motion-tactics.md` § Audit questions; this list adds the principle-level checks.

- [ ] **Taxonomy** — every motion moment classified as animation, micro-interaction, or functional motion. Lens applied per category.
- [ ] **Four pillars (per micro-interaction)** — Trigger discoverable; Rules consistent; Feedback ≤100ms first frame; Loops/Modes have exit conditions.
- [ ] **Duration** — every animation duration sourced from the canonical table OR justified as a brand-driven exception in DESIGN.md.
- [ ] **Easing intent** — entering elements use ease-out; leaving permanent uses ease-in; in-bounds movement uses ease-in-out. ≤2 generic curves + 1 signature curve total per project.
- [ ] **GPU-only** — every animation touches only `transform` / `opacity` (or `filter` / `clip-path` with awareness). No `width`, `height`, `top`, `left`, `margin` animations.
- [ ] **C.U.R.E.** — each motion moment passes Context / Usefulness / Restraint / Emotion. Decorative-only motion cut.
- [ ] **One signature** — the page has exactly one signature motion moment, not 12 competing ones.
- [ ] **5-second rule** — any auto-running motion >5s has a pause affordance OR is gated behind `prefers-reduced-motion`.
- [ ] **3-flash rule** — no motion flashes more than 3×/second.
- [ ] **Reduced motion** — `prefers-reduced-motion: reduce` skips animation, content still appears.
- [ ] **LCP** — hero content paints within LCP budget, even if GSAP fails or hasn't run yet (`.js-ready` gate present).
- [ ] **Mobile** — parallax and pinned sequences are gated behind `(min-width: 768px)` OR simplified on mobile.
- [ ] **CSS-vs-GSAP transform handoff (high tier only)** — no `.js-ready` CSS rule sets `transform:` on a GSAP-tweened element. CSS owns opacity for the pre-JS hide; GSAP owns transform fully. Mixing them stacks two `translate()` calls in the inline style and leaves the element permanently masked. (Full pattern: `motion-tactics.md` § CSS-vs-GSAP transform handoff.)

---

## Anti-patterns

- ❌ **Motion-as-decoration.** Animations with no Context / Usefulness justification. Cut on sight.
- ❌ **Mixing 4+ easing curves.** Reads as un-designed. Pick 1–2 + 1 signature.
- ❌ **Linear easing on UI.** Robotic. Reserved for continuous loops and scrub-driven scroll only.
- ❌ **Animating Layout properties.** `width`/`height`/`top`/`left` = jank. Transform + opacity only.
- ❌ **Hero hidden behind animation that depends on JS.** No `.js-ready` gate = invisible content if JS fails. See motion-tactics.md § Required pattern.
- ❌ **CSS transform as pre-seed for GSAP-tweened elements.** `transform: translateY(110%)` in CSS + `gsap.to({yPercent: 0})` produces stacked translates in the inline style, leaving the element permanently masked. Split responsibility: CSS handles opacity for the `.js-ready` pre-JS hide; GSAP fully owns transform. See motion-tactics.md § CSS-vs-GSAP transform handoff.
- ❌ **Auto-running motion >5s without pause control.** WCAG 2.2.2 violation.
- ❌ **Same fixed duration for every animation.** A 300ms button hover and a 300ms hero reveal feel wrong because the *content scale* differs. Match duration to content scale per the table.
- ❌ **Spring physics on UI state transitions that need to feel uniform.** Spring's velocity-responsiveness is a bug here. Fixed timing wins.
- ❌ **Easing by feel instead of by intent.** Pick by category (ease-out for enter, ease-in for leave permanent, ease-in-out for in-bounds), not by aesthetic preference.
- ❌ **More than one signature motion per page.** No hierarchy = no impact.

---

## Quick reference

| Question | Answer |
|---|---|
| What's the difference between animation and micro-interaction? | Animation = show, branding, narrative. Micro-interaction = flow, functional feedback, user-triggered. |
| Default easing for entering elements? | Ease-out (`cubic-bezier(0.2, 0.7, 0.2, 1)` is the skill's signature). |
| How long should a button press feel? | 80–100ms first frame, full state change in ≤200ms. |
| When is spring better than fixed timing? | Drag-and-release, playful brand, layout reflows after user input. |
| What's the only safe property pair for animation? | `transform` + `opacity`. Add `filter` / `clip-path` cautiously. |
| What's the maximum auto-running motion duration without a pause control? | 5 seconds (WCAG 2.2.2). |
| How many signature motion moments per page? | One. |
| What does "reduced motion" mean? | Content still appears, but instantly (0.01ms transitions). Never "never reveal". |
| When do I cut decorative motion? | Always. If C.U.R.E. fails on Usefulness, it's gone. |
