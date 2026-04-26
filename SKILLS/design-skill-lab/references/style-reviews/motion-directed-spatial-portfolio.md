# Motion-Directed Spatial Portfolio — Style-Specific Review

Run this checklist in **Phase 4 Step 4.2** alongside the universal review. The library is animation-led — its failure modes cluster around **motion that fails the C.U.R.E. test** (generic fade-up on every block; loader theatre that hides content; "everything moves" with no direction).

These checks exist because the library only earns its place when motion is **directorial** — each transition expresses a specific intent. Generic Webflow-template motion ships flat and wastes the dark cinematic stage.

---

## 1. Stage — is the canvas dark and cinematic?

The library is dark-mode-native. Verify:

- Background sits at `#0a0a0a`–`#121212` (not pure black, not gray-900-from-Tailwind).
- Text is off-white `#f4f4f0`-ish (not pure white — pure white burns on dark backgrounds at large display sizes).
- Media (images, video stills) are **grayscale or near-grayscale** by default — full-colour appears only as a deliberate accent moment, not a default treatment.
- No bright surfaces inside the page (white cards on dark stage = wrong library; reach for Editorial Portfolio).

If background isn't truly dark or media isn't grayscale-by-default → wrong library. Reach for Editorial Portfolio (light) or Creative Studio (dark + colour).

## 2. Display typography — oversized, thin, architectural

The library's signature is **type as architecture** — Inter Tight thin/extralight at display sizes (`clamp(4rem, 12vw, 11rem)` range), used as composition element, not just headline. Verify:

- At least one display moment uses `font-weight: 200` or `300` at 8rem+ — **not** `font-bold` at 4rem (that's marketing serif, not spatial portfolio).
- Display headlines are **set tight** (`letter-spacing: -0.04em`, `line-height: 0.9–0.95`) — sprawl-y type breaks the architectural feel.
- Cormorant Garamond (or italic serif equivalent) used **sparingly** — italic serif as continuation/accent, not as primary display family.

If display typography reads like a normal marketing hero (semi-bold, generous tracking, line-height 1.2+), **refactor**. The point of the library is type-as-stage, not type-as-headline.

## 3. Motion — directed, not generic

This is the highest-risk failure mode. The craft guide is explicit: **"Do not add generic fade-up animation to every block."** Verify per-section:

- Each motion moment has a **stated intent** in the build comments — not just `data-aos="fade-up"` repeated 12 times.
- Motion uses **scroll keyframes** (page-scroll drives a timeline) where appropriate — not just IntersectionObserver fade-ins everywhere.
- Spatial hero object (the stage centerpiece — 3D, video, masked SVG, or animated image sequence) **moves with intent** (rotation, translation, scale tied to scroll progress), not a passive idle loop.
- No two adjacent sections use the same motion treatment (variety is the directorial gesture).

Mechanical check: search build for `fade-up` / `fade-in` repeated more than 3× — if so, **refactor**. Either remove the duplication or replace with directed transitions (Flip, parallax, stagger reveal, masked clip).

## 4. Loader theatre — only when the page IS the showcase

The craft guide forbids loader theatre **except for portfolio showcase sites**. The carve-out is narrow:

- If the brief is an actual portfolio (the page itself is the work shown), branded-intro loader is on-brand — verify it serves the showcase intent and isn't generic spinner-with-logo.
- If the brief is anything else (case study reading page, marketing page, agency landing), **page-load must be `subtle` or `none`**. Loader theatre on a non-showcase page hides content from users who came to read.

If `page-load: branded-intro` was set on a non-showcase page, **flag the tier-coupling conflict** and refactor to `subtle`.

## 5. Reading sections — content visible without animation

Long-form content (case study text, project descriptions, process documentation) must remain **readable if motion fails**. Verify:

- No `opacity: 0` on body-text containers without the `.js-ready` gate (build-tactics.md § 17.4).
- No animation delays > 600ms on sections that contain primary content — the user shouldn't be staring at a blank screen waiting for text to appear.
- `prefers-reduced-motion` fallback collapses scroll-keyframe animation to static state with all content visible. Test the toggle before delivery.

A page that hides its content behind motion is a failure mode this library specifically warns against.

## 6. Spatial hero — earns its weight?

The spatial hero (centerpiece visual that anchors the page) is the library's signature. Verify:

- Hero is **not** a stock 3D blob added because "the library does 3D." Apply C.U.R.E. — Context (does it relate to the work?), Usefulness (does it communicate?), Restraint (is it composed off-centre with breathing room?), Emotion (does it create the intended mood?).
- If `dimension: shader-accents` was set with this library, the WebGL hero must include all four failure-mode guards (webgl-3d-tactics.md § Pre-build checklist).
- If the hero is a video or image sequence, it is **muted by default** (auto-playing audio violates the cinematic restraint contract).

If the hero is generic ("rotating cube", "particle field with no theme"), the page reads as Webflow-template — **refactor or escalate to library switch**.

## 7. Accent — one shock colour, used once

The library specifies one project-specific shock accent (`accent-acid` `#62ff6a`, `accent-warm` `#d7c0a2`, or one custom colour per project). Verify:

- The accent appears in **at most 2 distinct visual moments** on the page (e.g., one display word + one CTA). More than that and the shock dilutes.
- Body text, secondary buttons, links in long-form content stay **off-white or muted grayscale** — never the accent.
- Dual-accent variants (project uses both `accent-acid` AND `accent-warm` simultaneously) are forbidden — pick one per project.

## 8. QA artifact — full-page screenshot is NOT enough

The craft guide explicitly warns: **"Do not make full-page screenshots your only QA artifact."** This style depends on motion that doesn't show in a screenshot. Verify the delivery includes:

- A short scroll-through video or GIF of the page in motion (or a clear note that motion-QA was done in browser).
- Reduced-motion screenshot showing the page is still legible without animation.
- Hero-state screenshot AND post-scroll-keyframe screenshot — to confirm the keyframed transition works.

If only a single full-page screenshot was produced, the QA pass is incomplete. The library's character lives in the transitions, not the static frames.
