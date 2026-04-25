# Regression Report Block

Every session result file MUST include this block at the end when the experiment was fixture-affecting. It compares the Protected Set before and after the change.

```markdown
## Regression Report

### Protected Set — Before
| Anchor | Status Before | Evidence path |
|---|---|---|
| `L-N-check` manifest row | PASS / FAIL / WARN / N-A | `output/{runner}_{slug}-file_output/pretreat-manifest.json` |
| `SV-N` verification gate | PASS / FAIL / WARN | `references/verification-gate.md` row |
| Paste parity anchor: `{name}` | PASS / FAIL | `{fixture}-paste-parity.md` line N |

### Protected Set — After
| Anchor | Status After | Evidence path | Delta |
|---|---|---|---|
| `L-N-check` | PASS / FAIL / WARN / N-A | same path as Before | same / flip |

### Verdict
- All anchors held? YES → KEEP is available.
- Any anchor flipped PASS → FAIL? YES → REGRESSION — discard the change or narrow it.
- Any anchor flipped FAIL → PASS (unexpected)? Investigate. If tied to the experiment hypothesis, record as positive side effect. If unrelated, flag as E-origin environmental change.

### If a new L-rule was promoted
- L-N — {one-line body}
- Origin: S | C | W | E
- Fixture where it surfaced: {slug}
- Verification gate: SV-X
- Manifest row: L-N-check
- Anti-re-broaden guardrail (if anti-lesson): {what must never be re-expanded}
- `scripts/lesson_surface_lint.py` verdict: PASS (lessons ↔ gates ↔ manifest in sync) | FAIL (drift — STOP before next run)
```
