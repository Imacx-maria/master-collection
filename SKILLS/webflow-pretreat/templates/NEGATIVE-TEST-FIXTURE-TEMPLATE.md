# Negative Test Fixture Template

**Pattern surfaced:** EXP-003 (L-7 universalization, 2026-04-25). Validated again in EXP-004 (mode-b probe universalization, same synthetic fixture reused). Promoted from ad-hoc technique to reusable template per Section D-B1 of POST-SHIP-RETROSPECTIVE-INPUT.md.

## Why this exists

When a rule is generalized from a specific case (e.g. "no global `.bg-whipe` collapse") to a universal form ("no global class-collapse on any source-DOM class"), you need three pieces of evidence to trust the generalization:

1. **Regression anchor:** the original specific case still PASSes (no false negative — universalization didn't lose precision).
2. **Class-name agnostic case:** a structurally-equivalent fixture with renamed class names also PASSes (proves universalization didn't accidentally hardcode the original names).
3. **Negative test:** intentionally violate the universalized rule on the new fixture; the gate must FAIL (proves the gate actually catches the violation, not just rubber-stamps).

Without all three, you're not validating universalization — you're hoping.

## When to instantiate this template

You're authoring an experiment that:
- Universalizes a previously fixture-specific rule (any rule that mentions specific class names, IDs, or fixture-derived constants in its body or its check command)
- Or introduces a new universal rule whose generalization claim needs proof

If the rule is born universal AND tested across ≥2 distinct scenarios in a single fixture, this template is overkill. Use it only when generalization is the explicit goal.

## Template

Copy the block below into your experiment's Before You Run declaration, then fill in the bracketed fields.

```markdown
### Negative test fixture set (per templates/NEGATIVE-TEST-FIXTURE-TEMPLATE.md)

**Rule under generalization:** [L-N — short name]
**Original specific case:** [the case the rule was first written for, e.g. ".bg-whipe global collapse on MNZ"]
**Universal claim:** [the structural pattern the universalized rule should catch, e.g. "no skill-injected global class collapse on any source-DOM class"]

**Three pieces of evidence required:**

1. **Regression anchor:**
   - Fixture: `[path/to/canonical-fixture.zip]`
   - Original symptom that should still be caught: `[describe]`
   - Expected verdict: PASS (rule fires correctly on canonical case)

2. **Class-name agnostic case:**
   - Synthetic fixture build script: `[path/to/build-synthetic.py]`
   - Construction method: `[e.g. "rename .bg-whipe → .page-curtain throughout HTML and CSS via deterministic regex"]`
   - Output fixture: `[path/to/synthetic.zip]`
   - Expected verdict: PASS (rule still fires after class rename — proves class-name independence)

3. **Negative test (intentional violation):**
   - Construction method: `[e.g. "after pretreatment, plant a global .{anyclass} { display: none } rule into fb-styles-site"]`
   - Where injected: `[output ZIP path or test-only copy]`
   - Expected verdict: FAIL (gate catches the planted violation)
   - **If this PASSes, DISCARD the universalization** — gate is rubber-stamping, not enforcing.
```

## Anti-patterns to avoid

**(a) Synthetic that's too synthetic.** If the synthetic fixture is hand-crafted from scratch with only the targeted scenario, it doesn't prove agnosticism — proves only "the rule works on a fixture I designed for it." Synthetic should be derived from a real fixture by mutating ONE dimension (typically class names). Everything else stays identical.

**(b) Negative test on a different gate.** The planted violation must specifically trigger the rule under test, not some adjacent gate. If you plant `.bg-whipe { display: none }` and the gate FAILs because `bg-whipe` is in a forbidden namespace (different rule), you proved nothing about overlay-scope universalization.

**(c) Skipping the negative test "because the rule clearly works".** This is the most common failure mode and the most expensive when wrong. EXP-003 caught the synthetic-PASS-but-negative-PASS case with this exact discipline; without it, the L-7 universal rule would have shipped with a probe that rubber-stamps.

**(d) Re-using the same synthetic across N experiments.** A synthetic built for L-7 universalization may not be suitable for testing L-31 transport, even if it's the same `.page-curtain` fixture. Each generalization needs its own three-piece set; sometimes the synthetic is shared, sometimes not.

## What to keep after the experiment

The synthetic fixture goes into `experiments/EXP-NNN-assets/` (not into `fixtures/` — that's the canonical training corpus, not synthetic artifacts). The build script for the synthetic stays alongside. If a future experiment needs the same synthetic, reference it; don't rebuild.

The negative test setup is usually transient — planted violation in a temp copy, verified, deleted. Document the construction method in the experiment log so it can be replayed.

## Reference precedents

- **EXP-003:** synthetic `.page-curtain` fixture from MNZ class-rename. Built script: `experiments/EXP-003-assets/build-synthetic-page-curtain-fixture.py`. Negative test: planted `.page-curtain { display: none !important }` post-pretreatment, gate FAILed correctly. Verdict: KEEP.
- **EXP-004:** reused EXP-003's synthetic for mode-b probe universalization. Three-piece set adapted to mode-b semantics.
