# webflow-pretreat — MEMORY index

Always loaded when the skill runs. Keep under 150 lines.

## What this skill does

Transforms a raw Webflow export ZIP into a pretreated ZIP whose HTML body has one wrapper child (`fb-page-wrapper`) and whose CSS/scripts/assets are restructured for the FlowBridge minimal converter.

## Current iteration

**Iteration 6 (shipped 2026-04-25, version: 6).** L-31 Mode-B Transport Protocol MATURE on scenario-diversity grounds (MNZ + synthetic page-curtain: 85 targets, multiple class-chain patterns, multiple triggering signature families, collision-handling via `data-flowbridge-ix-state` markers, class-name-agnosticism). L-30 stays YOUNG. Curated rule count is **28** (added L-32 `data-flowbridge-*` namespace convention, AUTHORING-PROCESS, in the 2026-04-25 P0 retrospective batch).

EXP-006 result: MNZ + synthetic both PASS all 16 contract checks at exit 0 with full 85/85 transport coverage. L-7 anti-broaden held (skill-injected=0); L-8 floor held (164/164); Protected Set 11/11 anchors held.

**Promotion 2026-04-25 (handoff 301):** `webflow-pretreat` is now the single active pre-treatment skill in Flowbridge-claude. Old `webflow-pre-treat-ai` + `webflow-pre-treat-codex` split archived under `_archive/2026-04-25-pre-treat-ai-codex-split/`. Mirror lives at `.claude/skills/webflow-pretreat/`.

Iteration log pre-2026-04-25 trim lives in `experiments/MEMORY-HISTORY.md`. Audit/promotion chain: 297 → 298 → 299 → 300 → 301 → 302.

## Lessons registry — snapshot

Full bodies in `references/lessons.md`. Compact status list:

**Curated (30 rules, inlined in references/lessons.md):** L-1, L-2, L-4, L-5, L-6, L-7, L-8, L-9, L-11, L-12, L-13, L-14, L-15, L-16, L-17, L-18, L-19, L-20, L-21, L-22, L-23, L-24, L-25, L-27, L-28, L-30, L-31, L-32, L-33, L-34

**Anti-lessons (MUST never re-broaden):**
- L-7 — overlay scoping (global `.bg-whipe` collapse is banned)
- L-8 — IX2 preservation (blanket strip is banned)
- L-25 — scoped fix discipline (re-broadening old wide rules is banned)
- L-34 — visible text/glyph mutation is banned (no thematic helpfulness, no SEO improvements, no emoji injection, no typo-fixing — content is read-only; see SKILL.md §Source Content Immutability)

**Informational:** L-14, L-20
**Verification meta-rule:** L-21
**Authoring-process:** L-32 (no manifest row; codifies `data-flowbridge-*` namespace convention)
**Excluded (appendix in lessons.md):** L-3 → L-16 (SUPERSEDED); L-10 → L-15 + L-15A (SUPERSEDED); L-26 (VERIFICATION-ONLY, converter-owned); L-29 (PASTE-SIDE, not pretreatment artifact-touching)

Maturity tags live on each L-rule body in `references/lessons.md`. Promote YOUNG → MATURE on scenario diversity (class chains, triggering signatures, parent contexts), not fixture count.

## Verification gate — compact index

Full bodies in `references/verification-gate.md`. SV-1..SV-19 cover pre-treatment artifact structure; SV-P1..SV-P6 cover paste-side when in scope.

## Known fixtures (stress tests)

| Slug | Source ZIP | Notable features |
|---|---|---|
| `mnz-creative` | `fixtures/mnz-creative-original.webflow.zip` | Six `.bg-whipe` overlays (L-7 anchor), IX2 transforms (L-8 anchor), 85 mode-b targets (L-31 anchor) |
| `srta-colombia` | `fixtures/srta-colombia-webflow.zip` | CMS template stubs (L-27), CMS anchor tagging (L-28). 0 mode-b targets — silent on L-31. |
| `bigbuns` | `fixtures/mc-001-bigbuns.webflow.zip` | GSAP scripts (L-9 + L-15 anchors), library CSS extraction (L-17). 0 mode-b targets — silent on L-31. |
| `synthetic-page-curtain` | `experiments/EXP-003-assets/synthetic-page-curtain.webflow.zip` | Class-rename of MNZ proving class-name-agnosticism for L-7 + L-31 |

New fixtures continue the loop under the same Before You Run protocol.

## Experiments ledger — pointer

Active experiment files live in `experiments/EXP-*.md`. One-line summary format in each file's header. The detailed iteration narrative — including pre-2026-04-25 results — lives in `experiments/MEMORY-HISTORY.md`. Most recent: EXP-006 (KEEP) closed F-1 + F-2 follow-ups from EXP-005.

## Paths

The skill is **host-project-agnostic**. Paths below describe the current training environment, not skill requirements.

- **Training ground (current):** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\AI_OS\SKILLS\webflow-pretreat\`
- **Mirror (loader-discoverable):** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\.claude\skills\webflow-pretreat\`
- **Ship target (distribution):** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\SKILLS\webflow-pretreat\`
- **Training host:** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\` — where fixtures, output/, and experiments/ live during training
- **Fixtures corpus (training only):** `Flowbridge-claude\fixtures\*.webflow.zip`

## Training vs Ship — what travels

When copying the skill to MASTER-COLLECTION (or any new host), only these folders ship:

- `SKILL.md`
- `references/` (all 5 files)
- `scripts/` (all 5 files)
- `templates/` (all 4 files)
- A trimmed `MEMORY.md`

These STAY in the training host (Flowbridge-claude) and are NOT shipped:

- `evals/` — training-time test prompts against the local fixture corpus
- `experiments/` — training-time experiment ledger including `MEMORY-HISTORY.md`

A new host running the skill needs zero files from Flowbridge-claude. Scripts read from `SKILL_DIR/references/lessons.md` (auto-contained), never from any `docs/` folder outside the skill.

## Runner constraints

These are environment-specific facts about WHERE this skill can and cannot run. Surface BEFORE picking a runner for an experiment.

**Cowork PowerShell 60s timeout (D1).** The Cowork desktop session's `mcp__Windows-MCP__PowerShell` tool has a 60s per-call cap. Full pretreatment of a real Webflow export (99KB+ HTML, 160KB+ source CSS, AI-driven reasoning across N transformations) cannot complete within 60s. Use **Claude Code on the Legion** OR **Codex CLI** as runner for full pretreatment. Cowork is appropriate for control-plane checks (lesson_surface_lint, probe self-test, small file edits, quick PowerShell <30s queries) but NOT for full-fixture transformation runs.

**Scheduled-vs-turn-by-turn boundary (D2).** Experiments require human-in-loop (architect verdict on KEEP/DISCARD/PARTIAL). Auxiliary monitoring (lint runs, regression-anchor diff, fixture auto-scan, MASTER-COLLECTION sync drift check) can be scheduled. Scheduling an EXP-NNN drafting task or "run experiment X next week" is an anti-pattern — the verdict requires human authority.

**Cross-link:** `docs/LOOP.md` §5 Periodic Sweeps for related ritual work.

## Open skill debt (scoped, waiting for dedicated experiments)

- **Verification-gate.md L729-730 doc drift:** prose still names MNZ class chains as scope-defining for the mode-B rows. Reframe as illustrative when next L-31 touch lands. Non-blocking.
- **`summarize_static_visible_class_state_safety` consumes legacy `INITIAL_STATE_TARGETS`:** if a non-MNZ fixture regresses on that probe row in a future experiment, migrate it onto the dynamic catalog too.
- **Stale prose breadcrumbs in references/:** `references/lessons.md`, `references/decision-patterns.md`, `references/verification-gate.md`, `references/webflow-constraints.md`, and `scripts/paste_contract_probe.py` carry `docs/LESSONS.md` / `webflow-pre-treat-ai` mentions in PROSE (not code paths). Historical breadcrumbs, not runtime dependencies. Cosmetic batch-rewrite candidate.

## Fast rules (repeated from SKILL.md for reflex recall)

- Input is exactly one raw `.zip`. Never start from a pretreated folder.
- Output is a ZIP OR a HALT-REPORT. Never both, never neither.
- Every run declares all 7 Before You Run fields and a Protected Set if fixture-affecting.
- Every failure mode promotes to an L-rule with origin label (S/C/W/E).
- The `lesson_surface_lint.py` check MUST pass before the next experiment starts.
- Anti-lessons are anti-lessons forever. Re-broadening re-ships the regression.
