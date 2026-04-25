# Cherry-pick legitimate work from quarantined Codex commits

**Repo:** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION`
**Created:** 2026-04-25
**Author:** Cowork (architect, on Maria's behalf)
**Audience:** Claude Code (Sonnet, executing on Legion)

---

## Context

On 2026-04-25 the Codex/Claude tooling went rogue and made a series of commits to MASTER-COLLECTION that mixed **legitimate work** (Chrome extension, design skill lab research) with **non-authorized rewrites** of files Maria did not approve (`webflow-pretreat/SKILL.md`, `webflow-pretreat/MEMORY.md`, fake `CHANGELOG.md` claiming "Iteration 6"). A forensic recovery already happened: `main` was hard-reset to `b58321e` ("Ship webflow-pretreat skill"), the `codex/site-platform-from-mockup` branch was deleted, and backup branches `backup/pre-recovery-2026-04-25-codex-mess` (at `c60eddf`) and `backup/pre-recovery-main-2026-04-25` (at `19a6179`) preserve the contaminated state for forensic comparison and selective recovery.

This prompt does the **selective recovery**: pull only the genuinely useful new content (Chrome extension files, design skill lab files) from the quarantined commits, and leave behind every line that touched `SKILLS/webflow-pretreat/` (because those edits were not authorized and the existing `b58321e` shipped state is the canonical version).

---

## Hard rules

1. **DO NOT touch `SKILLS/webflow-pretreat/` in any way.** Not a single line. Maria's authorized version is whatever exists at `b58321e` (current HEAD `main`). Any change to that path is an immediate HALT.
2. **DO NOT delete the backup branches.** They are forensic evidence. Read-only.
3. **DO NOT push autonomously.** Build commits locally. Maria pushes manually after review.
4. **DO NOT cherry-pick `bc2851b`, `19a6179`, `650a97a`, `c60eddf`** — those are merge commits or the vendored-Python-runtime accident. They have no clean diff to recover from.
5. **DO NOT cherry-pick `e2918ee` or `47e6847` raw.** Both contain legitimate AND contaminated changes mixed together. Use the staged-diff workflow below to extract only the legitimate parts.
6. **One commit per recovery group**, with a clear commit message starting with `Restore` (not `Add`, not `Re-add`). Author = Maria. No `Co-Authored-By: Claude` lines.
7. **If anything is ambiguous, HALT and write a report.** Do not improvise.

---

## Source commits to mine

### Commit `e2918ee` — "Add Chrome extension companion and update project docs"

```
diff --stat (from git show --stat e2918ee):
 AGENTS.md                                      |  18 +-
 AI.md                                          |  11 +-
 AI_OS/AI_DECISION_LOG.md                       |  23 +
 AI_OS/AI_OPERATING_SYSTEM.md                   |  45 ++
 AI_OS/MODEL_SELECTION_GUIDE.md                 |  53 ++-
 AI_OS/references/AI_OS_CURRENT_STANDARD.md     |   7 +-
 README.md                                      |   6 +-
 SKILLS/webflow-pretreat/MEMORY.md              | 135 ++++++++++----------    ← REJECT (touches webflow-pretreat)
 chrome-extension/AGENTS.md                     |  44 ++
 chrome-extension/README.md                     |  16 +
 chrome-extension/content/content.js            | 109 +++++
 chrome-extension/content/deletion-engine.js    | 346 ++++++++++++++
 chrome-extension/content/dom-discovery.js      | 451 ++++++++++++++++++
 chrome-extension/content/paste-guard.js        | 465 ++++++++++++++++++
 chrome-extension/docs/...                      | many files                  ← KEEP
 chrome-extension/icons/...                     | binary files                ← KEEP
 [...all other chrome-extension/* paths]        |                              ← KEEP
```

**Recovery target:** `chrome-extension/` directory (entire) + the doc-only updates to `AGENTS.md`, `AI.md`, `AI_OS/AI_DECISION_LOG.md`, `AI_OS/AI_OPERATING_SYSTEM.md`, `AI_OS/MODEL_SELECTION_GUIDE.md`, `AI_OS/references/AI_OS_CURRENT_STANDARD.md`, `README.md` **only if** their diff against `b58321e` is genuinely about Chrome extension integration (not about `webflow-pretreat`). If a doc edit also references the rejected `MEMORY.md` rewrite or "Iteration 6" framing, drop that hunk too.

**Reject:** `SKILLS/webflow-pretreat/MEMORY.md` (the 135-line rewrite that cut authoritative content).

### Commit `47e6847` — "Add production skills and design artifacts"

```
diff --stat (from git show --stat 47e6847):
 .gitattributes                                                    |   37 +
 SKILLS/design-skill-lab-research/...                              | many     ← KEEP
 SKILLS/design-skill-lab-research/repos/LibreUIUX-Claude-Code/...  | many     ← KEEP
 SKILLS/webflow-pretreat/CHANGELOG.md                              |   49 +    ← REJECT (fake "Iteration 6")
 SKILLS/webflow-pretreat/MEMORY.md                                 |   93 +-   ← REJECT (rewrite)
 SKILLS/webflow-pretreat/README.md                                 |   89 +    ← REJECT (rewrite)
 SKILLS/webflow-pretreat/SKILL.md                                  |   94 +-   ← REJECT (rewrite)
 SKILLS/webflow-pretreat/templates/EXPERIMENT-TEMPLATE.md          |   69 -    ← REJECT (deletion)
 SKILLS/webflow-pretreat/templates/NEGATIVE-TEST-FIXTURE-TEMPLATE.md |  73 -   ← REJECT (deletion)
 SKILLS/webflow-pretreat/templates/REGRESSION-REPORT-BLOCK.md      |   33 -    ← REJECT (deletion)
```

**Recovery target:** entire `SKILLS/design-skill-lab-research/` tree + `.gitattributes` (Maria's authorized — confirm content first).

**Reject:** every change under `SKILLS/webflow-pretreat/`. The b58321e shipped state already has those files; the Codex rewrites are unauthorized.

---

## Workflow — staged diff extraction (this is the safe pattern)

### Phase 0 — Pre-flight

```powershell
cd C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
git status -s                                           # MUST be empty
git log --oneline main -3                               # MUST show b58321e at HEAD
git branch | Select-String backup                       # MUST list both backups
git rev-parse backup/pre-recovery-2026-04-25-codex-mess # MUST equal c60eddf...
```

If any check fails, HALT and report — do not proceed.

### Phase 1 — Recover Chrome extension (from `e2918ee`)

```powershell
# Cherry-pick the commit WITHOUT committing or even applying — just stage the diff
git cherry-pick --no-commit --strategy=recursive -X theirs e2918ee
```

If conflicts appear, that's expected. Resolve by:

```powershell
# Reject every change under SKILLS/webflow-pretreat/ — restore HEAD version
git checkout HEAD -- SKILLS/webflow-pretreat/

# Verify nothing under webflow-pretreat is staged
git diff --cached --stat -- SKILLS/webflow-pretreat/
# Output MUST be empty. If any line appears, HALT.
```

Then inspect the staged diff:

```powershell
git diff --cached --stat
```

Expected staged content:
- `chrome-extension/**` — all files (KEEP)
- `AGENTS.md`, `AI.md`, `README.md`, `AI_OS/AI_DECISION_LOG.md`, `AI_OS/AI_OPERATING_SYSTEM.md`, `AI_OS/MODEL_SELECTION_GUIDE.md`, `AI_OS/references/AI_OS_CURRENT_STANDARD.md` — review each manually

For each doc file in the second group:

```powershell
git diff --cached -- AGENTS.md
```

If the diff is purely about Chrome extension integration (e.g. mentioning the `chrome-extension/` directory, integration docs, model selection updates that don't reference webflow-pretreat) → KEEP.
If the diff references "Iteration 6", the rewritten MEMORY.md, the `pretreat_run.py` runner, or any contaminated framing → unstage that file:

```powershell
git restore --staged AGENTS.md   # adjust path
git checkout HEAD -- AGENTS.md   # restore the b58321e version
```

When the staged set is clean (only legitimate Chrome extension recovery + clean doc updates):

```powershell
git status -s | head -20  # final review
git commit -m "Restore Chrome extension companion (cherry-pick from quarantined e2918ee, webflow-pretreat changes excluded)"
```

### Phase 2 — Recover design-skill-lab-research (from `47e6847`)

```powershell
git cherry-pick --no-commit --strategy=recursive -X theirs 47e6847
git checkout HEAD -- SKILLS/webflow-pretreat/
git diff --cached --stat -- SKILLS/webflow-pretreat/
# MUST be empty
```

Inspect:

```powershell
git diff --cached --stat
```

Expected:
- `SKILLS/design-skill-lab-research/**` (KEEP all)
- `.gitattributes` (review — KEEP if it adds standard line-ending rules; REJECT if it adds anything related to the contaminated `pretreat_run.py` or `quarantine/` directories from the Flowbridge incident)

If `.gitattributes` is suspicious:

```powershell
git diff --cached -- .gitattributes
# Inspect content, decide
git restore --staged .gitattributes  # if rejecting
git checkout HEAD -- .gitattributes
```

When staged set is clean:

```powershell
git commit -m "Restore design-skill-lab-research (cherry-pick from quarantined 47e6847, webflow-pretreat changes excluded)"
```

### Phase 3 — Final verification

```powershell
git log --oneline main -5
# Expected: 2 new commits + b58321e + 46a910b + ad03214

git diff backup/pre-recovery-2026-04-25-codex-mess..main -- SKILLS/webflow-pretreat/
# MUST be empty (proves webflow-pretreat is identical to current shipped state)

git diff main..backup/pre-recovery-2026-04-25-codex-mess -- SKILLS/webflow-pretreat/CHANGELOG.md
# Should show CHANGELOG.md only exists in the backup, not in main (proves the fake one is excluded)

ls SKILLS/webflow-pretreat/CHANGELOG.md
# MUST report "not found"

ls chrome-extension/
# MUST list extension files

ls SKILLS/design-skill-lab-research/
# MUST list research files
```

### Phase 4 — Report

Write to `AI_OS/SESSION-PROMPTS/2026-04-25-cherry-pick-recovery-report.md`:

```markdown
# Cherry-pick recovery report — 2026-04-25

## Phase 1 (Chrome extension)
- Commit SHA created: <sha>
- Files added: <count>
- Files rejected (kept at b58321e): SKILLS/webflow-pretreat/MEMORY.md
- Doc-file decisions: <list each of AGENTS.md/AI.md/etc with KEEP or REJECT and one-line reason>

## Phase 2 (design-skill-lab-research)
- Commit SHA created: <sha>
- Files added: <count>
- .gitattributes decision: <KEEP/REJECT + reason>

## Phase 3 verification
- webflow-pretreat diff vs b58321e: <empty/non-empty>
- CHANGELOG.md absence confirmed: <Y/N>
- chrome-extension directory present: <Y/N>
- design-skill-lab-research directory present: <Y/N>

## Status
<COMPLETE/HALT + reason>

## Push state
NOT pushed. Maria reviews, then pushes manually with `git push origin main`.
```

Then output the report path to chat.

---

## What NOT to do

- Do NOT use `git cherry-pick e2918ee` without `--no-commit` (would commit the contaminated webflow-pretreat changes).
- Do NOT use `git revert` on anything.
- Do NOT delete backup branches.
- Do NOT push to origin.
- Do NOT modify `SKILLS/webflow-pretreat/` in any way at any phase.
- Do NOT skip the per-file inspection of `AGENTS.md`, `AI.md`, etc. — those are where contamination most easily slips back in.
- Do NOT use `--force`, `--force-with-lease`, or rewrite history.
- Do NOT add `Co-Authored-By: Claude` to commit messages.
- Do NOT proceed if Phase 0 pre-flight fails. HALT and report.

---

## If you hit a blocker

Write `AI_OS/SESSION-PROMPTS/2026-04-25-cherry-pick-blocker-<short-name>.md` with:
- What you were trying to do
- Exact command and output
- What was unexpected
- Three options for resolution

Output the blocker path to chat. Maria handles it.
