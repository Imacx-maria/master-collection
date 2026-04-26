# Adaptive AI Console — Style-Specific Review

Run this checklist in **Phase 4 Step 4.2** alongside the universal review. Adaptive AI Console fails differently from other libraries: the failure mode is "Linear cosplay" (visual mimicry without the operational density that earned the look) or "AI slop dressed in dark mode" (indigo-violet sprinkled on generic SaaS chrome with no command palette, no rows, no provenance).

These checks exist because the library only earns its place when the page reads as a **product surface**, not a marketing landing pretending to be one.

---

## 1. Surface tier — is the canvas truly near-black?

The library specifies near-black surfaces (`#0d0e10` and friends), not "dark gray" and not pure `#000000`. Pure black reads cheap; mid-gray reads as Notion. Verify the surface tier:

- Background sits at `#0a0b0d` – `#10131a` range.
- Surface elevations step in 1–3% lightness increments — NOT 5–10% (Material Design uses big steps; Linear-class consoles use whisper-thin elevation).
- No `#1f2937` (Tailwind `gray-800`) or `#27272a` (Tailwind `zinc-800`) showing up — those are Tailwind defaults, not Linear values.

**Fail = refactor surfaces before delivery.** A non-near-black canvas breaks the entire optical contract.

## 2. Accent restraint — indigo-violet only on action, never decoration

The `#7170ff` accent is **interaction colour only**: primary buttons, focused inputs, active row state, command-palette current item, AI-composer send button. It must NOT appear on:

- Decorative gradient backgrounds (no "indigo blob behind hero")
- Borders (borders stay neutral hairline `#23252a`)
- Body text or headings
- Generic icons (icons stay neutral; only active-state icons take accent)
- Marketing hero "AI sparkle" decorations

Count accent occurrences per screen. **More than 3 distinct accent surfaces visible at once → too loud.** Linear's signature is one accent, applied with discipline.

## 3. Density — does the page feel operational?

The library is built for dense operational rows (issue lists, agent runs, action queues), not for marketing whitespace. Verify:

- At least one section uses `padding-y: 8–12px` per row (operational density), not `padding-y: 24–32px` (marketing card spacing).
- Row hover state shows accent border-left or background-tint at `accent-soft` — not just colour change.
- Dense sections have inline metadata (status pills, timestamps, mono badges) on the same row — not stacked vertically.

If every section uses generous marketing spacing → **wrong library**. Reach for Warm Editorial or Atmospheric Protocol instead.

## 4. Command palette — present and on-brand?

Command palette is a **signature pattern**, not optional decoration. If the build has no command palette UI:

- For product/dashboard surfaces: this is a **defect** — add one (overlay, `Cmd+K` trigger, keyboard hint visible somewhere).
- For pure marketing pages: acceptable to skip, but consider whether Adaptive AI Console was the right pick — Warm Editorial may serve the marketing side better.

When present, the palette must:
- Sit on `surface-elevated` with hairline border, NOT bento-styled rounded card.
- Show keyboard hints (`↵`, `↑↓`, `Esc`) in mono font.
- Use accent only for current-row highlight.

## 5. AI generated-action accountability

Any UI surface that displays a **generated** action (AI suggestion, agent step, drafted reply) must include accountability metadata. This is the library's ethical contract — if the AI did it, the user must be able to tell. Verify each AI-output surface has at least:

- A **trace marker** (`AI ·` prefix, sparkle icon, or "Generated" label)
- A **provenance source** (model name, timestamp, or "Drafted from {context}")
- A **reversibility affordance** (Edit / Discard / Regenerate visible at row level)

Missing any of these on a generated-action surface = **major defect**. Generated actions presented as if hand-typed is the failure mode this library exists to prevent.

## 6. Typography — Inter Variable + Berkeley Mono only

The pairing is non-negotiable for the library's identity:
- Display + body: Inter Variable (weights 400, 500, 600 — never `font-bold` 700 except for one-off display moments)
- Mono: Berkeley Mono (or fallback `JetBrains Mono`, `SF Mono`)

Check no Geist Sans, no Inter (non-variable), no SF Pro display-mode fonts crept in. **If Geist Sans is present, the build drifted to Technical Refined territory** — pick one library and commit.

## 7. Motion — micro, not theatrical

Motion budget for this library is **micro-interactions only**:
- Row hover: 80–120ms colour/border transition
- Command palette open: 150ms scale-from-95% + opacity
- AI composer state change: 200ms max
- NO scroll-triggered hero animations, NO parallax, NO loader theatre

If `motion: high` was set with this library, **flag the tier-coupling conflict** in delivery. Adaptive AI Console at `motion: high` reads as overproduced; Linear-class operational density depends on perceived snappiness, not animation flourish.

## 8. Bento — almost always wrong here

Bento grids belong to marketing showcase styles. Adaptive AI Console is operational — uniform grids and dense lists are the right patterns. If Phase 3 used bento for an operational section (issue list, agent run table, settings panel), **refactor to uniform grid or list** before delivery. Bento on a console reads as "marketing pretending to be a product."

Single-exception: a marketing-style "What you can build" section on a landing page can use bento — but flag it as a tonal pivot away from console identity.
