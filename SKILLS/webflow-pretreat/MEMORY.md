# webflow-pretreat — MEMORY index

Always loaded when the skill runs. Keep under 150 lines.

## What this skill does

Transforms a raw Webflow export ZIP into a pretreated ZIP whose HTML body has one wrapper child (`fb-page-wrapper`) and whose CSS/scripts/assets are restructured for the FlowBridge minimal converter.

## Current iteration

**Iteration 2 (2026-04-24):** Self-contained. All scripts copied verbatim from their canonical origins (hash-verified MATCH). References `verification-gate.md`, `decision-patterns.md`, `webflow-constraints.md`, `mechanical-consultation.md` copied verbatim. `lessons.md` curated to 26 rules (30 minus L-3, L-10, L-26, L-29) with an Excluded Rules appendix.

**Iteration 3 (2026-04-24, validated by EXP-002):** Architect landed 4 targeted fixes — (1) SKILL.md L-16 row rewritten to require the outer dep-gate wrapper always when Webflow globals / source-DOM selectors are detected (contradiction A resolved); (2) SKILL.md L-1.6 row rewritten to exclude `@media`-trapped selectors from the carrier count (contradiction B resolved); (3) `paste_contract_probe.py` `site_css_carried_check` patched with `strip_media_blocks` + `exclude_media`; (4) `host_topology_check` patched to per-file equality (`count >= 1 AND custom == media`). `lesson_surface_lint.py` PASS. EXP-002 validated all 4 fixes flipped their probe rows FAIL → PASS while holding the 7-anchor Protected Set. Remaining skill gap: mode-B transport protocol (documented in `experiments/EXP-DRAFT-mode-b-transport.md`).

**Iteration 3 continued (2026-04-24, validated by EXP-003):** L-7 universalized. Dropped the fixture-specific `L7_PURE_OVERLAY_CLASSES` whitelist (MNZ-spelling) in favor of runtime enumeration of source-DOM classes. New probe helpers `enumerate_source_dom_classes`, `parse_simple_class_chain_selector`, `collect_class_collapse_rules_from_css`. `overlay_neutralization_scope_check` now intersects output findings with source-DOM classes and subtracts source-preserved collapse rules (source-authored `.hide-all { display: none }` utility classes are legit per L-1, not L-7 violations). Validated on MNZ (regression anchor held) + synthetic `.page-curtain` fixture + planted-collapse negative test. Protected Set 9/9 held. `lesson_surface_lint.py` PASS. L-7 debt struck from backlog.

**Iteration 6 SHIPPED (2026-04-25, prompt 295).** Cross-fixture validation as designed (BigBuns + Srta Colombia) revealed both fixtures detect 0 mode-b targets — vacuous-hold, not transport-confirmed. Architect reframe applied 2026-04-25: maturity = scenario diversity, not fixture count. L-31 promoted YOUNG → MATURE on existing scenario coverage (MNZ + synthetic page-curtain: 85 targets, multiple class-chain patterns, multiple triggering signature families, collision-handling via F-1 markers, class-name-agnosticism). L-30 stays YOUNG (Mode B exercised once; scenario-diversity story not yet equivalent). Iteration 6 shipped to `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\SKILLS\webflow-pretreat\` (`SKILL.md + references/ + scripts/ + templates/ + trimmed MEMORY.md`; `evals/` + `experiments/` stayed in training host). Ship-copy lint PASS + probe self-test PASS confirmed post-copy. POST-SHIP-RETROSPECTIVE-INPUT.md trigger checklist all 6 boxes flipped. See `experiments/EXP-DRAFT-295-vacuous-cross-fixture-finding.md` for the full vacuous-cross-fixture finding + reframe rationale. **Iteration 6 validated by EXP-006:** F-1 + F-2 bundled fix landed. **F-1 (skill emission collision marker, S-origin):** L-31 collision-handling addendum appended to `references/lessons.md` body (no rewrite); SKILL.md workflow Step 7a extended to detect collision groups (same class chain + ≥2 distinct `required` tuples) and emit `data-flowbridge-ix-state="ix-state-{N}"` markers + marker-keyed runtime-gated CSS rules instead of class-chain rules for those groups. Global sequential marker numbering per output file. Idempotent per L-6. MNZ collision: 26 `.arrow-ab` elements → ix-state-1 (×25 left-arrows, translate3d(-100%,0,0)) + ix-state-2 (×1 right-arrow, translate3d(100%,0,0)). **F-2 (probe runtime-gate awareness, C-origin):** new `_RUNTIME_GATE_PREFIX_RE` + `strip_runtime_gate_prefix(selector) -> (stripped, was_gated)` helper added to `paste_contract_probe.py`; recognizes `html:not(.w-mod-ix2)`, `html:not(.w-mod-ix3)`, `html.w-mod-js:not(.w-mod-ix2)`, `html.w-mod-js:not(.w-mod-ix3)`, and bare `:not(.w-mod-ix2|3)` prefixes. Applied to BOTH `summarize_static_visible_class_state_safety` (line 760+) AND `collect_ix_state_css_rules` (line 1183+) — the second consumer was caught + fixed in second pass after first F-2 attempt left `mode-b-static-visible-ix-state-safety` newly failing on the 26 markers. Both safety paths now share identical runtime-gate semantics. **Result:** MNZ `mode-b-initial-state-transport` PASS at 85/85 transported (was 60/85 in EXP-005). Class-state-safety PASS, 0 hazards (was FAIL, 5 in EXP-005). IX-state-safety PASS, 26 markers / 0 hidden / 0 unsafe. L-7 anti-broaden HELD (skill-injected=0). L-8 floor HELD (164/164). Synthetic mirrors MNZ — same 16 contract checks PASS, exit 0. Probe self-test PASS. lesson_surface_lint PASS. Curated rule count stays 27 (L-31 grew via addendum; no new L-rule). Iteration 6 ready to ship to MASTER-COLLECTION.

**Iteration 5 (2026-04-25, validated by EXP-005):** L-31 — Mode-B Transport Protocol authored across all four skill surfaces. New `lessons.md` L-31 body (ARTIFACT-TOUCHING, Maturity: YOUNG) emits runtime-gated `html:not(.w-mod-ix2) <target.selector> { <decls>; }` CSS rules into `fb-styles-site` (or library host when `component_fallback_host` annotated) for every target detected by the post-EXP-004 universal `detect_mode_b_targets`. New `SKILL.md` Mandatory Output Manifest L-31 row + step 6 amendment + new step 7a (probe-as-detector + emission). New `verification-gate.md` SV-19 body + Gate Report Template row. L-30 retroactively tagged Maturity: YOUNG (introduced 2026-04-24, MNZ-only). Curated rule count bumped 26 → 27. Mode-B IX2 transport protocol gap struck from "Known skill debt." Architect-approved runtime-gating choice (a) `html:not(.w-mod-ix2)` adopted; mechanical L-7 escape verified by reading `parse_simple_class_chain_selector` (rejects `:`, ` `, `(` so L-31 rules never enter L-7 candidate set); cascade-safety verified by reading `selector_specificity` (L-31 rule scores `(0, K+2, 1)` vs source `.X.Y` scoring `(0, K, 0)`, so `transport_property_is_cascade_safe` returns True). No probe modifications.

**Iteration 3 continued (2026-04-25, validated by EXP-004):** Mode-B target detection universalized. Replaced the hardcoded MNZ-derived `INITIAL_STATE_TARGETS` catalog as the mode-B transport authority with `detect_mode_b_targets(html)` — scans source HTML for elements with hidden-on-load inline styles (display:none, visibility:hidden, opacity:0, off-screen translate, zero-scale transform, fully-clipped clip-path, zero-collapse sizing) gated by (IX-shaped OR data-w-id). `build_manifest` threads source's detected catalog into output's transport scan so contract-check IDs align. `mode_b_d007_anchor_check` now looks up dynamic targets by class chain. The `INITIAL_STATE_TARGETS` constant is preserved-but-narrowed as legacy spec for the out-of-scope `summarize_static_visible_class_state_safety` check. MNZ now detects 94 dynamic targets (vs 8 hardcoded baseline) — all 5+ prompt-required class chains FOUND. Synthetic `.page-curtain` detects 94 (renamed `bg-whipe`→`page-curtain` proves class-agnostic). `mode-b-initial-state-transport` FAIL count rose from 7 (baseline) to 84 missing — broader detection coverage; not masking. Protected Set 7/7 measurable anchors held; the 3 anchors not in this probe (L-27 stub, L-11/L-12 wrapper, L-18 asset preservation) are unchanged-by-construction since pretreatment skill was not modified. Probe self-test + lesson-surface lint PASS.

**Next iteration (5):** EXP-005 — author L-31 (Mode-B Transport Protocol) per `experiments/EXP-DRAFT-mode-b-transport.md` Option 2, pointing it at the probe's now-universal `detect_mode_b_targets` catalog. Generalising the d007 anchor check from MNZ-specific class chains to "any `menu-bar-*` shell + its hidden-on-load children" lands alongside L-31 (overlapping logic). Then EXP-006/007 cross-fixture validation on Srta + BigBuns.

## Lessons registry — snapshot

Full bodies in `references/lessons.md`. Compact status list:

**Curated (28 rules, inlined in references/lessons.md):** L-1, L-2, L-4, L-5, L-6, L-7, L-8, L-9, L-11, L-12, L-13, L-14, L-15, L-16, L-17, L-18, L-19, L-20, L-21, L-22, L-23, L-24, L-25, L-27, L-28, L-30, L-31, L-32

L-32 added 2026-04-25 (P0 retrospective batch): `data-flowbridge-*` namespace convention (AUTHORING-PROCESS). Codifies an existing pattern; not artifact-touching, no manifest row.

**Anti-lessons (MUST never re-broaden):**
- L-7 — overlay scoping (global `.bg-whipe` collapse is banned)
- L-8 — IX2 preservation (blanket strip is banned)
- L-25 — scoped fix discipline (re-broadening old wide rules is banned)

**Informational:** L-14, L-20
**Verification meta-rule:** L-21
**Excluded (appendix in lessons.md):** L-3 → L-16 (SUPERSEDED); L-10 → L-15 + L-15A (SUPERSEDED); L-26 (VERIFICATION-ONLY, converter-owned); L-29 (PASTE-SIDE, not pretreatment artifact-touching)

## Verification gate — compact index

Full bodies in `references/verification-gate.md`. SV-1..SV-18 cover pre-treatment artifact structure; SV-P1..SV-P6 cover paste-side when in scope.

## Known fixtures (stress tests)

| Slug | Source ZIP | Notable features |
|---|---|---|
| `mnz-creative` | `fixtures/mnz-creative-original.webflow.zip` | Six `.bg-whipe` overlays (L-7 anchor), IX2 transforms (L-8 anchor), complex CSS |
| `srta-colombia` | `fixtures/srta-colombia-webflow.zip` | CMS template stubs (L-27), CMS anchor tagging (L-28) |
| `bigbuns` | `fixtures/mc-001-bigbuns.webflow.zip` | GSAP scripts (L-9 + L-15 anchors), library CSS extraction (L-17) |

New fixtures added later continue the loop under the same Before You Run protocol.

## Experiments ledger — index

Append one line per EXP-NNN as experiments are run. Format: `EXP-NNN ({fixture}, {runner}): {outcome} — {one-line takeaway}`

EXP-001 (mnz-creative, claude): HALT S-origin+E-origin — 2 skill contradictions (SKILL.md manifest vs L-16; L-1.6 vs L-2) + 2 skill gaps (mode-B transport protocol; D-007 overlay transport) + 1 probe bug (host-topology multi-page false FAIL). Anti-lesson anchors L-7/L-8/L-30 PASS. SUPERSEDED by EXP-002.
EXP-002 (mnz-creative, claude): PARTIAL KEEP — iteration-3 validation. 4 architect fixes landed (L-16 rewrite, L-1.6 rewrite, probe @media exclusion, probe per-file host-topology). All 4 flipped FAIL → PASS. Protected Set 7/7 held. Remaining 2 FAILs (`mode-b-initial-state-transport`, `mode-b-d007-anchor-safety`) captured as L-rule candidate in `EXP-DRAFT-mode-b-transport.md`. Output ZIP: `output/claude_mnz-creative-file_output.zip`.
EXP-003 (mnz-creative + synthetic `.page-curtain`, claude): KEEP — L-7 universalized. Dropped `L7_PURE_OVERLAY_CLASSES` whitelist; rewrote rule body + SKILL manifest row + probe `overlay_neutralization_scope_check`. Probe now enumerates source-DOM classes at runtime and subtracts source-preserved collapse rules (e.g. designer-authored `.hide-all { display: none }` utilities are exempt). Triple validation: MNZ PASS (skill-injected=0, source-preserved=6), synthetic `.page-curtain` PASS (class-name-agnostic proven), negative test with planted `.page-curtain { display: none !important }` FAIL (exactly 2 flagged). Protected Set 9/9 held. `lesson_surface_lint`: PASS.
EXP-DRAFT-295 (bigbuns + srta-colombia raw fixture probe-only, claude): HALT-WITH-REFRAME — both fixtures detect 0 mode-b targets via `paste_contract_probe.detect_mode_b_targets`. Cross-fixture validation as designed cannot deliver L-31 maturity (vacuous-hold, not transport-confirmed). Architect directive 2026-04-25: maturity = scenario diversity, not fixture count. L-31 promoted YOUNG → MATURE on existing scenario coverage (MNZ + synthetic). L-30 stays YOUNG. Iteration 6 ships to MASTER-COLLECTION (SKILL.md + references/ + scripts/ + templates/ + trimmed MEMORY.md). lesson_surface_lint PASS post-edit. POST-SHIP-RETROSPECTIVE-INPUT.md item E4 already carries the maturity-convention refinement text. Output: no transform run; deliverables are the L-31 maturity edit + MEMORY.md debt-entry rewrite + ship copy + draft `experiments/EXP-DRAFT-295-vacuous-cross-fixture-finding.md`.
EXP-006 (mnz-creative + synthetic `.page-curtain`, claude): KEEP — bundled F-1 (skill collision-marker emission, S-origin) + F-2 (probe runtime-gate awareness, C-origin). L-31 collision-handling addendum appended (no body rewrite). SKILL.md Step 7a extended for collision-mode emission (group by class-chain; bucket with ≥2 distinct required tuples emits per-element `data-flowbridge-ix-state="ix-state-{N}"` markers + marker-keyed runtime-gated CSS rules instead of class-chain rules; idempotent per L-6). Probe gained `_RUNTIME_GATE_PREFIX_RE` + `strip_runtime_gate_prefix(selector) -> (stripped, was_gated)` helper, applied to BOTH `summarize_static_visible_class_state_safety` AND `collect_ix_state_css_rules` (second consumer caught in second pass after first F-2 attempt left ix-state-safety newly failing on markers). MNZ result: `mode-b-initial-state-transport` PASS at 85/85 (was 60/85 in EXP-005); class-state-safety PASS at 0 hazards (was 5); ix-state-safety PASS at 26 markers / 0 hidden / 0 unsafe; L-7 anti-broaden held (skill-injected=0); L-8 floor held (164/164). Synthetic mirrors MNZ — exit 0 on both with `--fail-on-contract`. Probe self-test PASS. Lint PASS. 11/11 Protected Set anchors held; L-31 anchor strengthened from 60/85 to 85/85. Phase 1 instrumentation FRESH (timing log + profile JSON + reference-load report all this-run, none carried). Curated rule count stays 27. **Iteration 6 shippable.** Outputs: `output/claude_mnz-creative-file_output.zip` (8,174,200 bytes, 102 members) + `output/claude_synthetic-page-curtain-file_output.zip` (8,176,360 bytes, 102 members).
EXP-005 (mnz-creative + synthetic `.page-curtain`, claude): PARTIAL — L-31 (Mode-B Transport Protocol) authored across all four skill surfaces (lessons + manifest row + SV-19 + workflow step 7a + MEMORY ledger). Runtime-gated `html:not(.w-mod-ix2) <target.selector>` CSS rules emitted in `fb-styles-site` (and `fb-styles-splide` for slider2 component-root) for every target detected by post-EXP-004 `detect_mode_b_targets`. MNZ transport coverage: 60/85 (`converted-to-css/embed`) + 1/85 (`component-root-fallback`) — a +59 jump from EXP-004 baseline of 1 transported. `mode-b-d007-anchor-safety` flipped FAIL→PASS. `webflow-paste-overlay-neutralization-scope` STAYS PASS with `skill-injected=0` (L-7 anti-broaden held). `mode-b-inline-ix-preserved` STAYS PASS with 164/164 (L-8 floor held). Synthetic `.page-curtain` mirrors MNZ structurally — class-name-agnosticism proven at the emission level. Architect-approved gate (a) chosen — flagged upfront per G4. L-7 escape + cascade-safety + transport-match mechanically verified by reading `parse_simple_class_chain_selector` (rejects `:`/` `/`(`) + `selector_specificity` (`(0, K+2, 1)` > `(0, K, 0)`) + `css_selector_matches` (endswith). Maturity tag YOUNG on L-31; L-30 retroactively tagged YOUNG. No probe modifications. Curated count 26 → 27. Two narrow follow-ups for EXP-006: (F-1, S-origin) `.arrow-ab` cascade-risk on 25 targets where two `required` sets collide on one selector — needs per-element `data-flowbridge-ix-state` marker fallback in step 7a; (F-2, C-origin) `mode-b-static-visible-class-state-safety` flagged 5 content-bearing-root hazards because the probe row does not recognize the runtime-gate prefix as discharging the safety check — needs a one-helper probe update. Protected Set 10/10 hold. Lesson-surface lint PASS. Output: `output/claude_mnz-creative-file_output.zip` (8,174,354 bytes, 102 members) + `output/claude_synthetic-page-curtain-file_output.zip` (8,175,795 bytes, 101 members).
EXP-004 (mnz-creative + synthetic `.page-curtain`, claude): KEEP — mode-B target detection universalized. Replaced hardcoded `INITIAL_STATE_TARGETS` (as mode-B authority) with `detect_mode_b_targets(html)` structural detector + canonical `mode_b_required_fragments` + class-chain-keyed `mode_b_d007_anchor_check`. MNZ: 94 dynamic targets (vs 8 hardcoded baseline) including all 5+ prompt-required class chains; 24 unique class chains. Synthetic: 94 detected, `page-curtain`/14 matches MNZ `bg-whipe`/14 — class-agnostic proven. `mode-b-initial-state-transport` FAIL: 84 missing (vs EXP-002 baseline 7) — broader coverage, not masking. Protected Set 7/7 measurable anchors PASS; 3 unmeasurable anchors unchanged-by-construction. Probe self-test + lesson-surface lint PASS. Skill-prompt deviations logged: (1) `INITIAL_STATE_TARGETS` retained as legacy spec for out-of-scope `summarize_static_visible_class_state_safety`; (2) §Detection #1 relaxed from strict `data-w-id` to `(IX-shaped OR data-w-id)` per primary-source evidence (MNZ ratio 164:35 IX-vs-data-w-id makes strict criterion unsatisfiable). Unblocks EXP-005 (L-31 authoring against now-universal probe).

## New L-rule candidates this cycle

- **L-31 — Mode-B IX2 transport protocol (READY for EXP-005 authoring):** probe's `detect_mode_b_targets` catalog is now class-name-agnostic; L-31 author step can point at it directly per `experiments/EXP-DRAFT-mode-b-transport.md` Option 2.
- **D-007 generalization (deferred to EXP-005):** widen d007 anchor check from MNZ-specific class chains to "any `menu-bar-*` shell + its hidden-on-load children co-transport". Overlaps with L-31 emission logic; lands together.

## Known skill debt (scoped, waiting for dedicated experiments)

- ~~**L-7 fixture-specificity debt**~~ — **RESOLVED in EXP-003 (2026-04-24).** L-7 is now universal: probe enumerates source-DOM classes at runtime and flags any skill-injected global class-based collapse CSS on any of them, while subtracting source-preserved legit collapse utilities. Validated on MNZ (regression anchor held) + synthetic `.page-curtain` fixture (class-name-agnostic) + negative test (planted collapse caught). No longer blocks ship.
- ~~**Mode-B target detection fixture-specificity debt**~~ — **RESOLVED in EXP-004 (2026-04-25).** Probe detects mode-B targets structurally per source HTML inline-style hidden-on-load fingerprints + IX-shape/data-w-id gate. The 8-entry hardcoded MNZ catalog is no longer the authority for mode-B transport (kept as legacy spec for one out-of-scope check only). Unblocks L-31 authoring.
- ~~**Mode-B IX2 transport protocol gap (L-31 emission)**~~ — **RESOLVED in EXP-006 (2026-04-25).** F-1 collision-marker emission + F-2 probe runtime-gate awareness landed as a bundled fix. MNZ + synthetic both PASS all 16 contract checks at exit 0 with full 85/85 transport coverage. L-31 collision-handling addendum + SKILL.md Step 7a extension + probe `strip_runtime_gate_prefix` helper applied to both safety paths.
- **Maturity convention refined 2026-04-25** (prompt 295 finding): scenario-diversity, not fixture-count. Cross-fixture validation on BigBuns + Srta Colombia (planned as L-31 maturity gate) revealed both fixtures detect 0 mode-b targets — vacuous-hold, not transport-confirmed. Reframe applied: L-31 promoted to MATURE based on existing scenario coverage already validated on MNZ + synthetic (85 targets, multiple class-chain patterns, multiple triggering signature families, collision-handling, class-name-agnosticism). Searching for a 3rd organic fixture purely to satisfy "tested in N fixtures" is fixture-bending; stress-tests are not curriculum. See `experiments/EXP-DRAFT-295-vacuous-cross-fixture-finding.md` and `experiments/POST-SHIP-RETROSPECTIVE-INPUT.md` item E4 refinement.
- **`data-flowbridge-ix-state="ix-state-{N}"` namespace** (added by EXP-006 F-1) — collision-mode marker attribute emitted by SKILL.md Step 7a when L-31 detects same-class-chain targets with multiple distinct required tuples. Lives in the existing `data-flowbridge-*` attribute family per skill-authoring convention. Recognized by `ix_state_markers_in_selector` in the probe.
- **Verification-gate.md L729-730 doc drift:** prose still names MNZ class chains as scope-defining for the mode-B rows. Reframe as illustrative after EXP-005 lands L-31. Non-blocking.
- **`summarize_static_visible_class_state_safety` still consumes legacy `INITIAL_STATE_TARGETS`:** if a non-MNZ fixture regresses on that probe row in a future experiment, migrate it onto the dynamic catalog too. Out of EXP-004 scope.

## Paths

The skill is **host-project-agnostic**. Paths below describe the current training environment, not skill requirements.

- **Training ground (current):** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\AI_OS\SKILLS\webflow-pretreat\`
- **Ship target (planned):** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\SKILLS\webflow-pretreat\`
- **Training host:** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\` — where fixtures, output/, and experiments/ live during training
- **Fixtures corpus (training only, stays in lab):** `Flowbridge-claude\fixtures\*.webflow.zip`

## Training vs Ship — what travels

When copying the skill to MASTER-COLLECTION (or any new host), only these folders ship:

- `SKILL.md`
- `references/` (all 5 files)
- `scripts/` (all 4 files)
- `templates/`

These folders STAY in the training host (Flowbridge-claude) and are NOT needed for the skill to run:

- `evals/` — training-time test prompts against the Flowbridge-claude fixture corpus. A new host runs evals against its own fixtures, if any.
- `experiments/` — training-time experiment ledger (EXP-001, EXP-002, ...). Lives where training happens.
- `MEMORY.md` — **partial exception:** the ship copy gets a trimmed MEMORY.md that drops training-specific experiment indices and fixture snapshots. The Fast Rules and Paths sections ship.

A new host running the skill needs zero files from Flowbridge-claude. Fixtures are the host's own. Output lands in the host's own `output/` folder. Scripts read from `SKILL_DIR/references/lessons.md` (auto-contained), never from any `docs/` folder outside the skill.

### Known stale prose references (cosmetic, non-blocking)

After the portability pass, a few files still mention `docs/LESSONS.md` inside PROSE (not code paths):

- `references/lessons.md` lines 410, 545, 587, 589, 618, 645, 681, 708, 753, 801, 866, 872, 880 — historical "Sync surface" lines carried over from canonical lesson bodies. They name the old `docs/LESSONS.md` and `AI_OS/SKILLS/webflow-pre-treat-ai/...` paths as provenance. These are historical breadcrumbs, not runtime dependencies.
- `references/decision-patterns.md` lines 175, 185 — text references to `docs/LESSONS.md`.
- `references/verification-gate.md` lines 169, 365, 367, 371, 640 — text references to `docs/LESSONS.md` in SV-7 extension docs.
- `references/webflow-constraints.md` lines 62, 207 — text references to `docs/LESSONS.md`.
- `scripts/paste_contract_probe.py` lines 450, 497 — comment lines mention `docs/LESSONS.md L-27 algorithm` (the algorithm itself is embedded in the script, the comment is just provenance).

These do NOT block the skill from running on any host — the Python scripts and the runtime lint read from `SKILL_DIR/references/lessons.md` exclusively after the iteration 2 portability pass. The prose mentions are cosmetic and can be rewritten in a batch pass before shipping to MASTER-COLLECTION.

## Runner constraints (added 2026-04-25, P0 retrospective batch)

These are environment-specific facts about WHERE this skill can and cannot run. Surface BEFORE picking a runner for an experiment.

### Cowork PowerShell 60s timeout (D1)

**Hard constraint:** the Cowork desktop session's `mcp__Windows-MCP__PowerShell` tool has a 60-second per-call timeout. Subprocess calls that exceed this limit time out, return no output, and cannot be resumed.

**Implication for this skill:** full pretreatment of a real Webflow export (99KB+ HTML files, 160KB+ source CSS, IX2 inline styles requiring AI-driven reasoning across N transformations) cannot complete within 60 seconds. EXP-001 stage 3 confirmed this empirically: Cowork subagent halted on the largest reasoning step.

**Required action:** when running the pretreat workflow, use **Claude Code on the Legion** OR **Codex CLI** as the runner. Both have shell access without 60s caps. Cowork is appropriate for: control-plane checks (lesson_surface_lint, probe self-test), small file edits, and quick PowerShell queries that finish in <30s. NOT appropriate for: full-fixture pretreatment runs.

**Workaround when full Legion access unavailable:** redirect long PowerShell output to file via `Start-Process ... -RedirectStandardOutput ...` and read with `Get-Content` after — sidesteps the timeout for output-bound calls but does not help for compute-bound work.

### Scheduled-vs-turn-by-turn boundary (D2)

**Rule:** experiments require human-in-loop (architect verdict on KEEP/DISCARD/PARTIAL). Auxiliary monitoring tasks do not.

**Scheduled is appropriate for:**
- Daily lint runs (`lesson_surface_lint.py` against the skill)
- Post-EXP regression monitor (Protected Set diff against baseline; alert if anchor flipped)
- Fixture auto-scan (when new `.webflow.zip` lands in fixtures/, run L-27 classification + shape report)
- MASTER-COLLECTION sync drift check (compare ship copy vs training copy; alert if files diverged silently)

**Turn-by-turn is required for:**
- Experiment runs (any EXP-NNN)
- Architect verdict decisions (PASS / FAIL / PARTIAL / KEEP / DISCARD)
- New L-rule promotion decisions
- Skill contradiction resolution
- Any work where keep/discard requires human judgment

**Anti-pattern:** scheduling an EXP-NNN drafting task or a "run experiment X next week" agent. The verdict on the experiment cannot be issued by the scheduled task itself; the human is the verdict authority. Scheduling experiments is a thin disguise over autonomous-loop ambitions that the loop discipline rejects.

**Cross-link:** see `docs/LOOP.md` §5 Periodic Sweeps for related ritual work that benefits from periodic execution but doesn't itself produce verdicts.

### Bash availability instability (D3)

The Cowork session's `mcp__workspace__bash` tool is intermittently unavailable. When down, fallback procedure:

1. Use `mcp__Windows-MCP__PowerShell` with output redirected to file (`-RedirectStandardOutput`)
2. Read via `Get-Content` to inspect
3. Apply 60s timeout discipline (D1) — chunk long-running operations

When bash is up, prefer it for: `find`, `grep -r`, file copies (`cp`, `rsync`), `unzip`/`zip`. PowerShell handles the same operations with different syntax.

---

## Fast rules (repeated from SKILL.md for reflex recall)

- Input is exactly one raw `.zip`. Never start from a pretreated folder.
- Output is a ZIP OR a HALT-REPORT. Never both, never neither.
- Every run declares all 7 Before You Run fields and a Protected Set if fixture-affecting.
- Every failure mode promotes to an L-rule with origin label (S/C/W/E).
- The `lesson_surface_lint.py` check MUST pass before the next experiment starts.
- Anti-lessons are anti-lessons forever. Re-broadening re-ships the regression.
