# AGENTS.md

## Project Snapshot

This repository is the master `AI_OS` template that gets copied into other projects.
It is documentation-first: mostly Markdown guidance, reusable skills, session templates, and sync scripts.
Primary stack: Markdown, shell, batch, and repo-structure conventions rather than an app runtime.
Use the nearest `AGENTS.md` for local rules in `SESSION-PROMPTS/`, `references/`, `templates/`, and `SKILLS/` only when a project keeps local skills.

For Codex and other repo-native coding agents, this file is the primary operational entry point.
Keep Claude-specific behavior in `CLAUDE.md` snippets and `.claude/` tooling; keep cross-tool rules here and in `AI.md`.

## Root Setup Commands

```bash
git status --short
find . -maxdepth 2 -type f | sort
rg -n "^# " AI_OPERATING_SYSTEM.md CONTEXT_RULES.md MODEL_SELECTION_GUIDE.md NEW_PROJECT_SETUP.md
find SKILLS -maxdepth 2 -type f | sort
find SESSION-PROMPTS/SESSIONS -maxdepth 2 -type f | sort
```

## Universal Conventions

- Keep tool-neutral operating rules in `AI_OPERATING_SYSTEM.md`, `CONTEXT_RULES.md`, root `AGENTS.md`, and `templates/AI.md`.
- Keep Claude-only material clearly scoped to `templates/CLAUDE_MD_SNIPPET.md`, `.claude/` references, or Claude-specific reference files.
- When adding Codex guidance, make it additive. Do not weaken or replace Claude-specific setup that still serves Claude Code/Cloud.
- Prefer boring names and stable locations over clever docs. Update the existing source of truth instead of creating a parallel file.
- Use real file paths and real search commands. This repo exists to steer future agents precisely.

## Security & Secrets

- Never commit tokens, live credentials, or personal override files copied from a real project.
- Treat `references/GOOGLE_ACCOUNTS_MAP.md` and similar operational docs as sensitive internal context; do not paste them into random summaries.
- In downstream projects, `CLAUDE.local.md` and similar local overrides stay gitignored and tool-specific.

## Regression Prevention

Before modifying any documentation or template:
1. Identify which workflow currently depends on it: Claude setup, Codex navigation, session handoff, or skill loading.
2. Check neighboring files so the same rule is not contradicted elsewhere.
3. Preserve provider-specific behavior that is intentionally scoped, even when adding multi-tool support.
4. If you change a template, verify the corresponding setup doc still points to the right file and path.
5. If impact is unclear, stop and ask.

Breaking an existing workflow is worse than leaving a gap explicitly documented.

If this repo documents capabilities that contradict vendor defaults or generic AI assumptions, trust the local docs and working workflow. Do not "correct" them from memory.

## Git Safety

Destructive git operations still require explicit user permission.

- Never run without asking: `git checkout -- <path>`, `git pull`, `git merge`, `git rebase`, `git reset --hard`, `git stash drop`, `git clean -f`, `git push --force`.
- Always allowed: `git status`, `git diff`, `git log`, `git show`, `git reflog`, `git add`, `git commit`.
- Before any risky git command: inspect `git status`, report what will change, and wait for approval.
- Panic rule: stop on unexpected repo state. Do not stack more git commands to "repair" it.

## Branch Workflow & Session Handoff

- Work on a feature or fix branch, not `main`.
- Use `SESSION-PROMPTS/SESSION_HANDOFF_TEMPLATE.md` for substantial template or workflow changes that should survive tool switches.
- Store dated handoffs in `SESSION-PROMPTS/SESSIONS/YYYY-MM-DD/`.
- If you add or move canonical guidance files, update the docs that route agents there: usually `NEW_PROJECT_SETUP.md`, `DOCS_INDEX_TEMPLATE.md`, `templates/AI.md`, or this file.
- Codex sub-agents / chat agents are execution helpers, not durable memory. Persist important findings in repo docs or dated handoffs.

## JIT Index

### Canonical Root Files

- `AI_OPERATING_SYSTEM.md` — universal operating rules across tools
- `CONTEXT_RULES.md` — conflict handling, tool boundaries, regression discipline
- `MODEL_SELECTION_GUIDE.md` — provider/model routing guidance
- `NEW_PROJECT_SETUP.md` — how this template is installed into a new project
- `DOCS_INDEX_TEMPLATE.md` — baseline docs index structure for downstream projects

### Directory Map

- `SKILLS/` — local/project-specific skill overrides only → see `SKILLS/AGENTS.md`
- `SESSION-PROMPTS/` — boot prompts, handoff template, dated session artifacts → see `SESSION-PROMPTS/AGENTS.md`
- `references/` — load-on-demand references and provider-specific notes → see `references/AGENTS.md`
- `templates/` — starter files copied into project roots → see `templates/AGENTS.md`

### Quick Find Commands

```bash
rg -n "Codex|Claude|Gemini|OpenAI" AI_OPERATING_SYSTEM.md CONTEXT_RULES.md MODEL_SELECTION_GUIDE.md templates SESSION-PROMPTS references
rg -n "AGENTS.md|AI.md|CLAUDE.md" NEW_PROJECT_SETUP.md DOCS_INDEX_TEMPLATE.md templates SESSION-PROMPTS
find SKILLS -maxdepth 2 -type f | sort
find SESSION-PROMPTS/SESSIONS -maxdepth 2 -type f | sort
```

## Breakthrough Knowledge

- AI_OS intentionally separates cross-tool rules from tool-native configuration.
- `CLAUDE.md` and `.claude/` remain Claude-specific. Root `AGENTS.md` and `AI.md` carry repo-level guidance that Codex and other agents can read.
- Prompt-building lives in the tool-native global skill systems: Claude uses Claude-native skills/commands, and Codex uses `~/.codex/skills`.
- Some docs are intentionally provider-specific, such as `templates/CLAUDE_MD_SNIPPET.md` and `references/CLAUDE-CODE-INSTRUCTION-FOLLOWING.md`. Do not flatten them into generic docs unless the behavior is actually cross-tool.

## Definition of Done

- Paths, filenames, and commands are real.
- Codex-facing docs and Claude-facing docs do not contradict each other.
- New guidance is placed in the narrowest correct home.
- If a change alters workflow across sessions or tools, the handoff/setup docs are updated in the same pass.
