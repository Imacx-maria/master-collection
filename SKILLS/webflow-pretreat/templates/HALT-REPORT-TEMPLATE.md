# HALT-REPORT-TEMPLATE

Written as `output/{runner}_{slug}-file_output/HALT-REPORT.md` when any Structural Verification Gate row or Mandatory Output Manifest row FAILs. No ZIP is written. The extracted output folder is preserved as diagnostic evidence only.

```markdown
# HALT REPORT — {runner}_{slug}

**Date:** YYYY-MM-DD HH:MM
**Runner:** claude | codex
**Source ZIP:** {absolute path}
**Output mode declared:** local-preview | webflow-paste
**Triggering experiment:** EXP-NNN ({path to experiment file})

## Halt Cause

**Failed gate / row:** SV-N or L-N-check
**One-line failure:** {what was expected vs what was observed}
**Origin label:** S-origin | C-origin | W-origin | E-origin

## Evidence

### Captured output of the failing check
```
{paste actual command output verbatim — no paraphrase}
```

### Location in output
- File: `output/{runner}_{slug}-file_output/{path}`
- Line: N
- Context: {±5 lines around the failure site}

### Comparison to source
- Source reference: `{path in raw ZIP or extracted working folder}`
- Observed delta: {what changed between source and pretreat that caused the FAIL}

## Protected Set Impact

Any PASS → FAIL flips from the invoking experiment's Protected Set? List each:
| Anchor | Before | After | Commentary |
|---|---|---|---|
| `{anchor name}` | PASS | FAIL | {why this regressed} |

## What NOT to Do

- Do NOT hand-patch `output/{runner}_{slug}-file_output/`. That produces a Franken-artifact (CLAUDE.md rule 14).
- Do NOT delete the extracted folder — it is diagnostic evidence. It may be cleared before a clean re-run, but only when the fix is applied in the SKILL.
- Do NOT zip the output anyway "just to have something". The Mandatory Output Contract is binary: valid ZIP or HALT-REPORT.md, never both.

## Next Step Options

1. **Fix the skill:** update the rule in `references/lessons.md` (or the workflow in `SKILL.md`). Run `scripts/lesson_surface_lint.py`. Re-run the experiment.
2. **Narrow the experiment:** the hypothesis may have been too ambitious. Write a follow-up EXP with a narrower scope.
3. **Promote a new lesson:** if the failure mode is a new failure class the skill hasn't seen, this is the moment to promote it to an L-rule. Do the full three-surface update (lessons + gates + manifest) before the next run.
4. **Abort:** if the failure is E-origin (tooling), fix tooling and re-run the same experiment.
```
