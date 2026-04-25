# Blocker — cherry-pick recovery halted at Phase 0

**Date:** 2026-04-25
**Author:** Claude Code (Sonnet, executing on Legion)
**Source prompt:** `AI_OS/SESSION-PROMPTS/2026-04-25-cherry-pick-legitimate-codex-work.md`

## What I was trying to do

Phase 0 pre-flight of the cherry-pick recovery prompt. Working tree was required to be empty before any `git cherry-pick --no-commit` could run safely.

## Exact command and output

```
$ git status -s
?? AI_OS/SESSION-PROMPTS/2026-04-25-cherry-pick-legitimate-codex-work.md
?? SKILLS/design-skill-lab-research/
?? SKILLS/design-skill-lab/
?? _tests/
?? site/public/harness-one-page.html

$ git ls-files --others --exclude-standard | wc -l
57
```

## What was unexpected

The working tree is **not empty**. There are 57 untracked files spread across four directories plus the prompt file itself. The prompt's Phase 0 says "`git status -s` MUST be empty. If any check fails, HALT and report — do not proceed."

The most dangerous overlap:

- `SKILLS/design-skill-lab-research/` — already exists as an untracked tree in the working directory. This is **exactly** the recovery target of Phase 2 (cherry-picking `47e6847`). Running `git cherry-pick --no-commit 47e6847` against this state would either abort with `untracked working tree files would be overwritten by merge`, or silently merge the tree from the commit on top of the existing untracked content. Either outcome violates the prompt's "extract only the legitimate parts" guarantee — there's no clean baseline to extract against.

Other untracked content (not direct overlap with the recovery, but still violates Phase 0):

- `SKILLS/design-skill-lab/` — sibling design skill, different folder name, ~12 files visible
- `_tests/` — test harness output, ~18 files visible
- `site/public/harness-one-page.html` — single file
- `AI_OS/SESSION-PROMPTS/2026-04-25-cherry-pick-legitimate-codex-work.md` — the prompt itself (expected)

A sample of `SKILLS/design-skill-lab-research/` shows nested git repos (`repos/LibreUIUX-Claude-Code/`, `repos/claude-code-skill-factory/`, `repos/claude-skills/`) with `__pycache__/` artifacts and `.editorconfig` / `.vscode/settings.json` files. This looks like an in-progress local exploration that was never committed, not the contaminated Codex output.

## Three options for resolution

### Option A — Stash the untracked tree, run the cherry-pick, then re-apply

```powershell
git stash push --include-untracked -m "pre-cherry-pick stash 2026-04-25"
# run Phase 1 + Phase 2 of the prompt as-written
git stash pop
# inspect conflicts; re-apply selectively
```

**Pro:** preserves Maria's local work, gives clean baseline for cherry-pick.
**Con:** the stash pop will conflict on `SKILLS/design-skill-lab-research/` because Phase 2 will have committed content there. Resolution will be manual and tedious. Risk that Maria's local-only experimental version diverges from the cherry-picked version and the wrong one wins.

### Option B — Decide per directory before proceeding

For each untracked tree, ask:

1. `SKILLS/design-skill-lab-research/` — is the local untracked version Maria's authoritative work, or a leftover from a partial recovery? If authoritative → **commit it first**, then SKIP Phase 2. If leftover → delete (with explicit approval) and run Phase 2.
2. `SKILLS/design-skill-lab/` — separate skill, not in the recovery scope. Commit, gitignore, or delete (Maria decides).
3. `_tests/` — likely meant to be local-only test output. Add to `.gitignore` or commit (Maria decides).
4. `site/public/harness-one-page.html` — single artifact. Commit or delete (Maria decides).

**Pro:** zero loss of local work, every file gets a deliberate decision.
**Con:** requires Maria to triage each tree before the recovery can run.

### Option C — Abandon the original recovery plan for Phase 2

Phase 2 may already be moot. If the local `SKILLS/design-skill-lab-research/` is in fact Maria's authoritative version (or substantively equivalent to `47e6847`'s content), there is nothing to recover from `47e6847` for that path. Phase 1 (Chrome extension from `e2918ee`) is unaffected and can still proceed once the untracked tree is dealt with.

In this case the new sequence becomes:

1. Maria triages the four untracked trees (commit / gitignore / delete).
2. Run Phase 1 only (Chrome extension).
3. Diff `backup/pre-recovery-2026-04-25-codex-mess` vs `main` for `SKILLS/design-skill-lab-research/` to verify the local tree captures everything `47e6847` had. If yes → Phase 2 is dropped. If no → run a narrow Phase 2 with `--no-commit` on a clean tree.

**Pro:** acknowledges the actual state of the working tree instead of forcing it through the original protocol.
**Con:** changes the prompt's intent, requires architect sign-off.

## Status

**HALTED.** No git state mutated. No cherry-pick attempted. Working tree, index, and main HEAD are all unchanged from session start (HEAD = `b58321e`).

## Pre-flight verification (the parts that DID pass)

- `main` HEAD = `b58321e` ✅
- `backup/pre-recovery-2026-04-25-codex-mess` = `c60eddf77057db2bfe80eace0d7d1c4390ffbf1e` ✅
- `backup/pre-recovery-main-2026-04-25` exists ✅
- Only the working-tree-clean check failed.
