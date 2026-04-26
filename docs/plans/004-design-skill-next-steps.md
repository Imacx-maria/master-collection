# Design Skill — Next Steps Plan

**Status:** ready to resume 2026-04-26 — Liquid Glass approved for now; refinements can continue in parallel.
**Skill:** `design-system-picker` at `~/.claude/skills/design-system-picker/`
**Owner:** Maria

## Why this plan exists

The skill is functional but not yet aligned with the Master Collection product reality. Right now it produces "any HTML/CSS that looks good in a browser." It needs to produce **HTML/CSS that round-trips through the Master Collection converter into Webflow without losing fidelity**, with a Finsweet-shaped class system and a deliverable style guide. This document is the punch list to get there.

The skill should remain usable as a standalone design tool, but its output contract must respect Flowbridge's rules. Current work is focused on Flowbridge **Lane B** (Webflow export / marketplace-style controlled assets), but the original Flowbridge architecture also has **Lane A** (arbitrary HTML/CSS import). Do not optimize the design skill in a way that makes Lane A harder later. Flowbridge's documented lessons and current converter constraints are the source of truth for Webflow-safe output.

---

## Workstream 1 — Webflow-validity output

**Goal:** every HTML/CSS the skill ships must be importable by the Master Collection converter (Flowbridge) into Webflow with zero loss.

### 1.1 Build the constraint reference

Create `~/.claude/skills/design-system-picker/references/webflow-validity.md`. Source it from:

- `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\LESSONS.md` — canonical Flowbridge lesson list and source of truth for what pre-treatment and the converter learned
- `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\architecture\2026-04-11-two-lane-objectives.md` — Lane A / Lane B ownership and future-compatibility boundaries
- `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\research\WEBFLOW-CSS-NATIVE-COVERAGE-MATRIX.md` — the authoritative "what survives the converter" table
- `docs/research/WEBFLOW-CSS-ROUTING-REFERENCE.md` — how CSS is routed into Webflow style panels
- `docs/research/IX3-CAPABILITIES-AND-LIMITS.md` — interaction-side limits
- `docs/research/FLOWKIT-V2-WEBFLOW-GUIDE.md` — the existing pattern reference
- `docs/CONDENSED-DOCTRINE.md` — the bottom-line doctrine
- `docs/rules/inviolables.md` — the hard rules

The reference must include, in priority order:

1. **Native-supported CSS properties** (the ones that round-trip cleanly). Treat as the default toolbox.
2. **Conditionally-supported properties** (work only with specific values or selectors). List the conditions.
3. **Unsupported properties** (must be avoided OR injected via embed/custom code with explicit cost). List the workaround per item.
4. **Selector limits** (e.g., descendant-only, no `:has()`, etc. — check the matrix).
5. **Layout primitives** Webflow understands (Flexbox + Grid as Webflow models them, not raw CSS).
6. **Asset rules** (image formats, SVG handling, fonts available natively vs. uploaded).
7. **Interaction primitives** (IX2 vs IX3 — what the skill is allowed to emit vs. what it must hand off).

### 1.2 Wire the constraint into Phase 3 BUILD

- Add Step **3.0.1 — Load `webflow-validity.md`** to the Phase 3 sequence in `SKILL.md`.
- Add a **build-time linter pass**: before writing the final HTML, every CSS property used must be checked against the matrix. If a property is in the unsupported list, either swap it for a native equivalent, or move it to a clearly-marked `<style data-webflow-embed>` block with a `// FALLBACK:` comment explaining why.
- Add Phase 4 check: a "Webflow round-trip audit" line in the review pass. The reviewer flags any unsupported property silently emitted in the main stylesheet.

### 1.3 Gotchas captured up front

Pull these into `webflow-validity.md` as call-outs based on Maria's repeated lessons:

- No `gap` on Webflow flex unless the doctrine has been updated (verify against the matrix).
- No CSS variables in places Webflow can't resolve them (typography font-family in particular — check matrix).
- No nested selectors deeper than Webflow allows.
- Anything from `inviolables.md` gets quoted verbatim.

---

## Workstream 2 — Finsweet client-first naming

**Goal:** the BUILD phase emits class names following Finsweet client-first conventions, not arbitrary semantic names.

### 2.1 Build the naming reference

Create `~/.claude/skills/design-system-picker/references/finsweet-client-first.md`. Cover:

- The folder/page/section/component/element naming hierarchy (e.g., `home-header_wrapper`, `home-header_title`).
- Utility class conventions (`u-text-h1`, `padding-section-large`, etc.).
- Spacing classes (`margin-bottom`, `margin-medium`, etc.) and how they pair with custom-property scales.
- Combo class rules and limits.
- The "global" vs. "page-specific" split.
- A worked example: a hero section in plain HTML/CSS, then the same hero in client-first.

Source: Finsweet's public client-first v2 docs (web search current canonical version before writing). Cross-check with anything in Flowbridge or Master Collection that already references Finsweet patterns.

### 2.2 Wire client-first into BUILD

- Phase 3 Step **3.0.2 — Load `finsweet-client-first.md`** after `webflow-validity.md`.
- Build-time rule: every emitted class name must match the client-first regex pattern documented in the reference. Naming violations are a Phase 4 Critical issue.
- Templates in `references/styles/<style>/assets/` must be re-audited (Workstream 8) to use client-first names. Until they are, the skill must rename on the fly during build.

---

## Workstream 3 — Style-guide output

**Goal:** every BUILD phase output ships with a complete style guide page, not just the design itself.

### 3.1 Define the style-guide template

A complete style guide includes:

- **Colors** — every token swatched with hex + variable name + usage note.
- **Typography** — every type scale entry rendered at real size with the font, line-height, weight, letter-spacing visible.
- **Spacing** — the scale rendered as visible bars or boxes with the variable name.
- **Radii / shape** — every radius variant rendered.
- **Shadows / elevation** — every shadow level rendered on a card.
- **Buttons** — primary/secondary/tertiary, all states (default/hover/active/disabled/loading).
- **Form fields** — input, textarea, select, checkbox, radio, all states.
- **Cards** — the project's canonical card variants.
- **Iconography** — icon sizes used and stroke conventions.
- **Motion** — list of named easings and durations with a demo of each.
- **Grid** — the column system rendered with overlay.
- **Breakpoints** — list with pixel values.

Build this as `references/style-guide-template.md` (a build-time scaffolding spec), plus an HTML scaffold at `references/style-guide-template.html` that the skill can fill in with the project's tokens.

### 3.2 Wire style-guide emission into BUILD

- Phase 3 always emits two files: the requested page **and** `style-guide.html`.
- Phase 4 review checks both. The style guide is a Critical-blocker if any token in the project DESIGN.md is not represented.

---

## Workstream 4 — Naming and trigger audit

**Goal:** the skill triggers reliably on the right requests and the style-library names match what users actually say.

### 4.1 Run the audit

Use `skill-creator` skill's analyze/optimize tools on `design-system-picker/SKILL.md`:

1. Test the description against a representative prompt set (Maria-style real briefs in EN and PT, vague prompts, style-name prompts, descriptor prompts like "agency site", "kids site", "calming UI").
2. Report which prompts mis-trigger or miss-trigger.
3. Suggest description rewording.

### 4.2 Audit per-style-library naming

For each library in `references/styles/`:

- Does the filename match what users call it? (`warm-serene-luxury` vs. how Maria actually phrases "luxury hotel" requests.)
- Does the library's `description` field surface the right trigger keywords?
- Is the style name discoverable from a plain-language brief, or does the skill have to be told the style by name?

Output: a list of rename + description-rewrite suggestions. Apply only after Maria approves.

### 4.3 Audit cross-references

- Every `references/<x>.md` referenced by `SKILL.md` must exist.
- Every file in `references/` must be referenced from `SKILL.md` or transitively, or be deleted/justified.

---

## Workstream 5 — Coherence and size audit

**Goal:** the skill's references are right-sized and internally consistent.

### 5.1 Use skill-creator to run a coherence pass

The skill-creator includes optimization tooling. Use it to:

- Check total token weight of `SKILL.md` + auto-loaded references. Flag if the auto-loaded budget is over the ceiling.
- Identify references that are **too long** (e.g., 900-line craft guides that should be split or trimmed) or **too short** to justify being a separate file.
- Identify duplicated content across libraries (e.g., the same anti-pattern listed in three style guides → move to `base-principles.md`).
- Identify under-used cross-references (a file referenced only once in deep prose that should be inlined).

### 5.2 Output

A spreadsheet-shaped report: `<file> | <lines> | <token est> | <auto-loaded?> | <recommendation>`.

---

## Workstream 6 — Hard-coded values audit

**Goal:** every value in every reference is either (a) intentionally hard-coded with a stated reason, or (b) a token reference.

Hard-coded **is okay** for:
- Typography ratios and floors from `typography-safety.md` (these are physics, not preferences).
- Spacing scale ratios.
- Easings and durations that are part of the named system.
- WCAG contrast minimums.

Hard-coded is **not okay** for:
- Colors written as hex inline when a variable exists.
- Font families written as strings inline when a variable exists.
- Magic pixel values that should reference the spacing scale.
- Values that vary per project being baked into a library default.

### 6.1 Method

Grep across `~/.claude/skills/design-system-picker/`:
- `#[0-9a-fA-F]{3,8}` for inline hex
- `font-family:\s*['"]` for inline font-family strings
- `\d+(px|rem|em)` outside known-token contexts
- `cubic-bezier` outside motion-token files

For each hit, decide: keep (and annotate) or replace with a variable.

### 6.2 Output

Patch list per file. Apply with Maria's review.

---

## Workstream 7 — Mandatory design-review activation

**Goal:** Phase 4 review **always** runs and **always** invokes `design-reviewer`, both in Cowork and Claude Code, with no silent skips.

### 7.1 Diagnose the current gap

Phase 4.3 already says "invoke design-reviewer." The failure mode is the orchestrator (Claude) skipping the call when a session feels "small enough." Check:

- Is `design-reviewer` accessible as a skill in both Cowork and Claude Code? (Already in the Cowork skill list as `design-reviewer`. Verify Claude Code parity.)
- What happens if `design-reviewer` itself is missing — does Phase 4 hard-fail or soft-skip?

### 7.2 Make it unskippable

- In `SKILL.md`, change Phase 4 language from "invoke" to **"Phase 4.3 is BLOCKING. The skill MUST call the design-reviewer skill before delivering. If design-reviewer is unavailable, halt and report — do not deliver."**
- Add a Phase 4.7 contract reminder (the existing self-correction loop memory is already aligned with this — keep it consistent).
- In the review-output format, require a literal line: `Design-reviewer invoked: yes / no` — if `no`, Phase 4 is incomplete.

### 7.3 Test

After change, run two end-to-end builds (one trivial landing page, one full e-commerce template). Confirm `design-reviewer` fires in both. Save a sample of each Phase 4 output in `references/style-reviews/` as a regression baseline.

---

## Workstream 8 — Step-by-step interview UI

**Goal:** the Phase 2.1 BLOCKING interview becomes a one-question-at-a-time guided flow instead of a wall of nine simultaneous questions.

### 8.1 Two implementation paths

**Path A — Cowork-native:** use `AskUserQuestion` (the multiple-choice tool already in Cowork) to ask one axis at a time. The skill orchestrates the loop:
- Ask axis 1 → wait for answer → ask axis 2 → … → ask axis 9 (or 10 if trauma-informed) → produce DESIGN.md.
- This is the lowest-friction path. Already supported by the platform. No new code.

**Path B — Claude Code interactive interface:** Claude Code does not have a native multiple-choice tool. Options:
- Open a local HTML form via a temporary file + browser launch, write answers to a file the skill reads back.
- Use Codex or a tiny CLI prompt loop. Not great UX.
- Fall back to a numbered-list one-at-a-time prompt in the chat ("answer 1, 2, 3, or 'you decide'").

### 8.2 Recommendation

Implement **Path A** in Cowork as the canonical path. In Claude Code, fall back to numbered-list one-at-a-time chat prompts (the existing flow, but enforced as one-question-per-turn instead of all nine at once). Document both modes in `SKILL.md` Phase 2.1.

### 8.3 Wire into the skill

- Add Phase 2.1 sub-steps:
  - **2.1.0 — Detect environment.** If Cowork → Path A. If Claude Code → Path B.
  - **2.1.1–2.1.9 — Ask one axis at a time.** Each step has a small set of plain-language options + the universal "you decide" escape.
  - **2.1.10 — Confirm summary.** Read all answers back, ask "go?" before proceeding.
- Update the per-axis source-field audit (existing Phase 4.0) so it sees one-axis-at-a-time provenance the same as the simultaneous version.

### 8.4 Risk

`AskUserQuestion` returns one answer at a time but the skill needs to chain nine of them. Verify: can a skill loop on `AskUserQuestion` calls within a single turn? If not, the skill emits one question, ends its turn, and resumes when the user answers. The skill must store interview state somewhere (the conversation itself is fine; explicit echo of "axis 3 of 9 — you've picked X for axis 1, Y for axis 2" keeps state recoverable).

---

## Workstream 9 — Re-run existing demos through the new skill

**Goal:** every demo built before the recent fixes (typography-safety, build-tactics, style-tuning, BLOCKING interview, loader-patterns, Liquid Glass research) gets brought up to current standards. **Fix in place — do not rebuild.**

### 9.1 Inventory the demos

Find every demo file the skill produced. Likely locations:
- `~/.claude/skills/design-system-picker/references/style-reviews/<style>.md` (these are review records, not demos — but reference demo paths).
- The Master Collection workspace for any HTML demos (`MASTER-COLLECTION/site/`, `MASTER-COLLECTION/app/` — ignore node_modules).
- The session outputs folder for older artifacts.
- The kindertech.html v1 referenced in the BLOCKING-interview memory — find it and treat as Demo Zero.

Build the inventory as a table: `<demo file> | <style library> | <date built> | <which fixes predate it>`.

### 9.2 Per-demo audit checklist

For each demo, run it through the **current** skill rules:

- Phase 4 design-reviewer pass.
- `webflow-validity.md` lint.
- `finsweet-client-first.md` naming check.
- `typography-safety.md` tier+modifier audit.
- `build-tactics.md` 13-tactic check.
- `loader-patterns.md` axis-9 alignment.
- Hard-coded-values grep (Workstream 6).
- Style-guide-companion presence (Workstream 3).

Output per demo: a Critical/High/Medium/Low issue list.

### 9.3 Fix in place

- Open the existing file. Apply the fixes. **Do not regenerate from scratch** — preserve the original design intent and any Maria-validated decisions.
- Each demo gets a small footer comment block: `<!-- Re-audited <date> against design-skill-lab v<n>. Issues fixed: ... -->`.
- Add the re-audited demo back to its `references/style-reviews/<style>.md` as the new baseline.

### 9.4 Order

Audit first, fix in batches:
1. The Liquid Glass demos (most recent — should be cleanest).
2. The trauma-informed / Sanctuary Tech demos (highest stakes).
3. The remaining nine library demos.

---

## Sequencing

The workstreams are not all independent. Suggested order:

1. **Workstream 1 (Webflow validity)** — foundational. Everything downstream depends on it.
2. **Workstream 2 (Finsweet)** — also foundational, parallel to 1.
3. **Workstream 3 (style guide)** — depends on 1+2 being in place so the style guide reflects valid output.
4. **Workstream 7 (review activation)** — parallel; small change but high leverage. Do early.
5. **Workstream 8 (interview UI)** — parallel; UX improvement, no dependency.
6. **Workstream 4 (naming audit)** + **Workstream 5 (coherence audit)** + **Workstream 6 (hard-coded audit)** — run together as one structural sweep once 1+2+3 are landed.
7. **Workstream 9 (re-run demos)** — last. Demos can only be properly re-audited once the rules they're being checked against are stable.

## Resolved start inputs

Resolved on 2026-04-26 before starting Workstream 1:

- **Flowbridge source of truth:** the design skill is standalone, but its Webflow-safe output must follow Flowbridge's source-of-truth rules. Use `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\LESSONS.md` as the canonical lesson/rule source, `WEBFLOW-CSS-NATIVE-COVERAGE-MATRIX.md` as the operational CSS/converter source for the current minimal converter, and `2026-04-11-two-lane-objectives.md` to preserve the Lane B now / Lane A later boundary. Use `WEBFLOW-CSS-ROUTING-REFERENCE.md`, `docs/breakthroughs/`, and `CONDENSED-DOCTRINE.md` as evidence/expansion references, not automatic overrides of the current matrix.
- **Finsweet client-first:** default to Client-First v2.
- **Style guide format:** HTML output is enough for now. No `.docx`/PDF deliverable unless requested later.
- **Liquid Glass:** approved for now. It still needs refinements, but it does not block this plan.
