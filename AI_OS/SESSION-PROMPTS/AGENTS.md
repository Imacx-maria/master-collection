# SESSION-PROMPTS/AGENTS.md

## Package Identity

`SESSION-PROMPTS/` holds reusable session templates, Codex runbooks, plus dated session artifacts.
This folder is where continuity survives tool switches, long debugging efforts, and major milestone handoffs.

## Setup & Run

```bash
find SESSION-PROMPTS -maxdepth 2 -type f | sort
find SESSION-PROMPTS/SESSIONS -maxdepth 2 -type f | sort
rg -n "Codex|Claude|handoff|session" SESSION-PROMPTS
```

## Patterns & Conventions

- Keep stable reusable cross-tool prompts at the top level: `AI_SESSION_START.md`, `SESSION_HANDOFF_TEMPLATE.md`, and evergreen setup prompts like `per-project-full-setup-prompt.md`.
- Keep Codex-first reusable execution prompts under `SESSION-PROMPTS/CODEX-RUNBOOKS/`.
- Store historical session output under `SESSION-PROMPTS/SESSIONS/YYYY-MM-DD/`.
- Dated files do not belong at the top level. If a filename starts with a date, it should normally live under `SESSIONS/YYYY-MM-DD/` unless it is an intentional versioned standard artifact.
- Use dated filenames for handoffs: `YYYY-MM-DD_HH-MM_topic_handoff.md`.
- Cross-tool files must say so explicitly. `AI_SESSION_START.md` is universal; `per-project-full-setup-prompt.md` is Codex-first but intentionally portable to other agents with light wording changes.
- Preserve the distinction between reusable template and historical artifact. Do not turn a dated session note into the canonical template.
- When a task is spread across tools or Codex sub-agents, capture the durable conclusion in a handoff rather than assuming the thread history is enough.

## Portable vs Personal

- Keep evergreen, project-portable prompts in this package.
- Keep personal or project-specific execution prompts out of the master top level unless they are deliberate examples or references.
- Historical one-off prompts may stay in the master repo as examples, but they belong under `SESSIONS/` so they do not get mistaken for current templates.

## Touch Points / Key Files

- Universal boot file: `SESSION-PROMPTS/AI_SESSION_START.md`
- Milestone handoff template: `SESSION-PROMPTS/SESSION_HANDOFF_TEMPLATE.md`
- Reusable repo-sync prompt: `SESSION-PROMPTS/per-project-full-setup-prompt.md`
- Reusable Codex runbooks: `SESSION-PROMPTS/CODEX-RUNBOOKS/`
- Multi-repo orchestration prompt: `SESSION-PROMPTS/multi-repo-ai-os-orchestration.md`
- Historical architecture handoff: `SESSION-PROMPTS/SESSIONS/2026-03-09/2026-03-09_ai-os-architecture-handoff.md`
- Historical planning artifact: `SESSION-PROMPTS/SESSIONS/2026-03-28/2026-03-28_ai-os-claude-folder-restructure-plan.md`

## JIT Index Hints

```bash
find SESSION-PROMPTS/SESSIONS -maxdepth 2 -type f | sort
rg -n "^## " SESSION-PROMPTS/AI_SESSION_START.md SESSION-PROMPTS/SESSION_HANDOFF_TEMPLATE.md
find SESSION-PROMPTS/CODEX-RUNBOOKS -maxdepth 2 -type f | sort
rg -n "Claude|Codex|continue|handoff|runbook" SESSION-PROMPTS
```

## Common Gotchas & Breakthrough Knowledge

- Historical files may use older conventions or even lack a `.md` suffix, such as `SESSION-PROMPTS/SESSIONS/2026-03-10/Audit Report Ix2 Vs Ix3`. Preserve them as evidence unless the user explicitly wants cleanup.
- Do not rewrite old handoffs to match current thinking. Add a new dated handoff when the understanding changes.
- If a file assumes a specific tool, say so in the file body instead of relying on the filename alone.

## Regression Prevention

- Do not delete or relocate dated session artifacts casually.
- Keep the handoff template aligned with the current AI_OS rules around verification, handoff timing, and cross-tool continuity.
- If you change where new handoffs or reusable runbooks should live, update the boot docs and setup docs in the same edit.

## Pre-PR Checks

```bash
find SESSION-PROMPTS -maxdepth 3 -type f | sort
rg -n "SESSIONS/YYYY-MM-DD|CODEX-RUNBOOKS|handoff|AI Session Start" SESSION-PROMPTS
```
