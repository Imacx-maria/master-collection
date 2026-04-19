# Multi-Repo AI_OS Orchestration Prompt

> Paste into Codex when you want one orchestrator session to audit multiple repositories, then optionally run a second safe-sync pass only where risk is low.
> This prompt is Codex-first and is designed for unattended execution with a structured final report.
> Date: 2026-04-04

---

## Operator Checklist

Before using this prompt:

1. Fill in the target repository list.
2. Confirm the master `AI_OS` path.
3. Decide whether `.claude/` is in scope for these repositories.
4. Keep this run in **two phases**:
   - Phase 1 = `audit-only` across all repos
   - Phase 2 = `safe-sync` only for repos that are low-risk after Phase 1
5. Confirm there will be no commit or push.

Recommended default:

- `.claude/` sync in scope only for repos that actively use Claude Code
- if uncertain, audit first and defer `.claude/` edits to Phase 2

---

## Runtime Inputs

Fill these in before use:

- `MASTER_AI_OS = C:\Users\maria\Desktop\AI_OS`
- `MASTER_CLAUDE = C:\Users\maria\Desktop\.claude` or `not in scope`
- `TARGET_REPOS =`
  - `C:\path\to\repo-1`
  - `C:\path\to\repo-2`
  - `C:\path\to\repo-3`

---

## The Prompt (copy from here to the end of the file)

You are running a multi-repository AI_OS audit and selective safe-sync orchestration.

Master AI_OS:
`MASTER_AI_OS`

Master `.claude/`:
`MASTER_CLAUDE`

Target repositories:
`TARGET_REPOS`

Objective:
Audit the AI layer of all listed repositories first, then run a second safe-sync pass only for repositories where the drift is low-risk and the portable/project-specific boundary is clear.

Execution model:
- Use one main orchestrator lane.
- Use one worker lane per repository when parallel execution is available and useful.
- Main lane owns coordination, consistency, and final reporting.
- Each worker lane owns exactly one repository.
- No commits, no pushes, no destructive git commands.

Global rules:
1. Treat this as AI_OS adaptation, not replacement.
2. Start every repository with read-only discovery.
3. Preserve all project-specific files and knowledge.
4. Do not copy personal `~/.codex` behavior into repositories.
5. Sync only portable AI_OS material.
6. Do not sync personal-only skills by default, including:
   - personal-only skills such as `SKILLS/gws-manager/` or `SKILLS/user/`
   - mirrored global skills that already exist in Claude/Codex native skill systems
   - any skill tied to Maria-specific accounts, machine paths, or personal infrastructure
7. Do not rewrite project-specific `CLAUDE.md`, `AGENTS.md`, `AI.md`, `AI_DECISION_LOG.md`, dated session handoffs, repo-specific prompts, or custom skills unless the change is clearly safe and justified.
8. Do not do broad docs cleanup. Only inspect docs entry health where it affects the AI layer.
9. Verify before claiming completion.

## Preflight — Repository Boundary Check

Before Phase 1, run a boundary preflight for every target path.

For each repository path, determine:

1. Is this path actually a single repository root?
2. Is it instead:
   - a container folder with multiple nested repositories
   - a worktree with broken metadata in the current environment
   - a non-git root with a nested git repo inside it
   - a project root whose real sync target is a subdirectory
3. Does the path contain:
   - root `.git` or a valid worktree pointer
   - root `AI_OS/`
   - root `.claude/`
   - root `AGENTS.md` / `AI.md` / `CLAUDE.md`

If the path is not a clean single-repo target, do not proceed to normal audit classification.
Instead mark it immediately as one of:

- `wrong target path`
- `container folder, needs sub-repo paths`
- `broken worktree metadata`
- `nested repo boundary unclear`

Then report the reason and skip normal audit/safe-sync for that path.

## Phase 1 — Audit Only

For each repository:

1. Inspect, if present:
   - root `AGENTS.md`
   - root `AI.md`
   - root `CLAUDE.md`
   - `AI_OS/`
   - `.claude/`
   - AI-facing docs entry files such as `docs/DOCS_INDEX.md`, `README.md`, `AI.md`, or equivalent
2. Compare against:
   - `MASTER_AI_OS`
   - `MASTER_AI_OS\references\AI_OS_CURRENT_STANDARD.md`
3. Classify:
   - portable files that should be synced from master
   - project-specific files that must be preserved
   - stale or duplicated guidance
   - Codex parity gaps
   - optional `.claude/` drift if `.claude/` is in scope
4. Decide repository risk level:
   - `low-risk for safe-sync`
   - `needs manual review before sync`
   - `audit only, do not auto-sync`

Only run this phase normally for paths that passed the boundary preflight.
If a path failed preflight, report it as a boundary failure instead of forcing a normal audit result.

### Phase 1 per-repo output

Return for each repository:

1. Inventory summary
2. Drift summary
3. Portable vs preserved classification
4. Risk level
5. Recommended Phase 2 action
6. Boundary status

## Phase 2 — Selective Safe Sync

Only after finishing Phase 1 across all repositories:

1. Select only repositories classified as `low-risk for safe-sync`.
2. For those repositories only, apply a safe sync:
   - sync portable `AI_OS/` core files from master
   - sync portable `AI_OS/references/`, `AI_OS/templates/`, and `AI_OS/SKILLS/AGENTS.md`
   - preserve only project-specific local skill folders under `AI_OS/SKILLS/`
   - sync `AI_OS/SESSION-PROMPTS/AI_SESSION_START.md`
   - sync `AI_OS/SESSION-PROMPTS/SESSION_HANDOFF_TEMPLATE.md`
   - sync `.claude/` only if in scope and clearly safe
3. Preserve:
   - `AI_OS/AI_DECISION_LOG.md`
   - `AI_OS/SESSION-PROMPTS/SESSIONS/`
   - project-specific skills
   - project-specific references
   - project-specific prompts
   - root `AGENTS.md`, `AI.md`, and `CLAUDE.md` unless a change is clearly a safe portable sync
4. Skip Phase 2 for any repository that would require rewriting project-local behavior rather than syncing portable template material.

### Phase 2 per-repo output

For each repository that was safe-synced, return:

1. Changes made
2. Files intentionally preserved
3. Remaining issues
4. Verification performed

## Final Output Format

Return one consolidated report in this structure:

# Multi-Repo AI_OS Report

## Phase 1 — Audit Summary
- `[repo path]` — `[risk level]`
- `[repo path]` — `[risk level]`

## Phase 2 — Safe Sync Summary
- `[repo path]` — `[synced or skipped]`
- `[repo path]` — `[synced or skipped]`

## Repo Details

### `[repo path]`
1. Inventory summary
2. Drift summary
3. Portable vs preserved classification
4. Changes made or skipped
5. Remaining issues
6. Verification performed
7. Boundary status

## Shared Drift Patterns
- repeated issue 1
- repeated issue 2

## Repositories Requiring Manual Review
- `[repo path]` — `[reason]`

## Recommended Next Actions
1. `[next step]`
2. `[next step]`
3. `[next step]`

Verification requirements:
- confirm which repository paths passed preflight and which failed boundary checks
- confirm which repositories were inspected
- confirm which repositories were edited and which were audit-only
- if files were changed, verify the changed files exist and summarize the diffed result before claiming completion

Do not commit. Do not push.
