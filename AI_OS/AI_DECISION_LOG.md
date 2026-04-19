
# AI Decision Log

The AI Decision Log records **important architectural and strategic decisions**
made during projects. Its purpose is to maintain continuity across sessions
and prevent re-solving the same problems repeatedly.

This document acts as the **memory layer of the AI Operating System**.

---

# How to Use This Log

Record decisions when:

• a system architecture is chosen
• a tool or model is selected
• a design pattern becomes standard
• a workflow is defined
• a major constraint or assumption is discovered

Each entry should capture **why the decision was made**, not only the decision itself.

---

# Entry Format

Date:

Project / Context:

Decision:

Reasoning:

Alternatives Considered:

Implications:

Next Review Date (optional):

---

# Example Entry

Date:
2026-03-09

Project / Context:
Flowbridge AI conversion pipeline

Decision:
Adopt structured JSON schema for intermediate site representation.

Reasoning:
Structured schema improves validation and enables automated checks before Webflow import.

Alternatives Considered:
- Direct HTML parsing
- CSS reconstruction

Implications:
Converter must always output schema-compliant JSON before import stage.

Next Review Date:
After 50 production imports.

---

---

Date:
2026-03-09

Project / Context:
AI Operating System — architecture

Decision:
AI_OS is copied per project, not shared from one central location.

Reasoning:
Different projects may need project-specific tweaks to skills, session prompts, or even model routing. A shared symlink approach would be simpler and always in sync, but would prevent any customization per project.

Alternatives Considered:
- One shared AI_OS folder referenced by all projects (rejected: no project-specific flexibility)
- Git submodule (rejected: overhead for a documentation system)

Implications:
- When the master AI_OS (Desktop/AI_OS) is updated, project copies must be manually synced
- Project-specific additions (extra session handoffs, custom skill tweaks) stay local
- Drift risk is accepted — periodic sync is the user's responsibility
- Core files (AI_OPERATING_SYSTEM.md, MODEL_SELECTION_GUIDE.md, CONTEXT_RULES.md) should stay identical across copies unless there's a deliberate reason to diverge

---

Date:
2026-03-09

Project / Context:
AI Operating System — documentation governance

Decision:
Adopt docs-strategy skill and documentation governance rules as part of the core AI_OS.

Reasoning:
Flowbridge demonstrated that without documentation governance, projects accumulate contradictory docs, random prompts, scattered plans, and dead files that actively mislead AI agents. Wrong documentation is worse than no documentation.

Alternatives Considered:
- Leave documentation ad hoc (rejected: proven failure in Flowbridge)
- Enforce via CLAUDE.md only (rejected: only covers Claude Code, not other tools)

Implications:
- All projects should follow docs-strategy placement and naming rules
- Breakthrough/discovery knowledge must be documented to prevent agents from reverting working implementations
- Regression prevention is now a first-class rule in both AI_OPERATING_SYSTEM.md and CONTEXT_RULES.md
- CLIs must place generated docs according to project structure, not randomly

---

Date:
2026-04-04

Project / Context:
AI Operating System — Codex adaptation

Decision:
Keep `my-precious` Claude-specific and add a separate `my-precious-codex` skill for OpenAI/Codex prompting.

Reasoning:
Claude-oriented prompt patterns in `my-precious` rely on Anthropic-specific assumptions such as XML-heavy structure, Claude model routing, and Claude Code execution patterns. Codex works better with concise layered `AGENTS.md` guidance, explicit step order, verification contracts, and OpenAI-specific reasoning-effort defaults. Splitting the skills preserves what already works in Claude while giving Codex first-class guidance.

Alternatives Considered:
- Rewrite `my-precious` into a fake multi-provider prompt skill (rejected: would blur real provider differences and weaken both workflows)
- Keep using the Claude-oriented skill for Codex (rejected: misleading defaults and stale OpenAI guidance)

Implications:
- Prompt-building is now provider-specific by default
- `AI_SESSION_START.md`, setup docs, and model guidance must route OpenAI/Codex users to the new skill
- Claude-specific skills remain valid and unchanged for Claude workflows

---

Date:
2026-04-05

Project / Context:
AI Operating System — prompt and plan persistence for Codex sessions

Decision:
When a Codex session produces a substantial prompt, execution plan, or handoff, store it as a file by default and return the Windows absolute path to the user.

Reasoning:
Large prompts and plans are brittle when copy-pasted through chat. Maria uses multiple chats and needs durable path-based reuse instead of relying on long inline responses. A saved artifact in AI_OS is a more reliable memory surface than thread history alone.

Alternatives Considered:
- Keep returning long prompts inline only (rejected: fragile and hard to reuse across chats)
- Store prompts only in dated session handoffs (rejected: good for history, bad for reusable execution artifacts)
- Store prompts only in project repos (rejected: not every prompt belongs to one repo, and cross-session reuse becomes harder)

Implications:
- Reusable prompts should usually live in `AI_OS/SESSION-PROMPTS/CODEX-RUNBOOKS/`
- Active plans should usually live in `docs/plans/` when the repo has project docs, otherwise under `AI_OS/SESSION-PROMPTS/SESSIONS/YYYY-MM-DD/`
- Handoffs should usually live in `docs/handoffs/` when that repo uses them, otherwise under `AI_OS/SESSION-PROMPTS/SESSIONS/YYYY-MM-DD/`
- Responses should include clickable Windows absolute paths whenever a substantial prompt, plan, or handoff is saved
- Chat should not be treated as the only storage layer for durable execution artifacts

---

Date:
2026-04-05

Project / Context:
Agent Skills architecture — boundary cleanup across Codex global, Windows AI_OS, and repo-local scaffolds

Decision:
Treat bootstrap order and conflict resolution as separate concepts, keep Maria-only always-on behavior in global Codex config, keep portable continuity in AI_OS, and keep skills limited to workflow core plus optional references.

Reasoning:
The previous setup mixed three different concerns: personal defaults, portable cross-project scaffolding, and reusable skill logic. That produced duplicated git policy inside skills, project-specific examples inside the master AI_OS, and ambiguity about whether higher-level files were discovery order or authority order. Separating these concerns reduces drift, lowers skill load cost, and makes progressive disclosure real instead of nominal.

Alternatives Considered:
- Keep the old overlap and rely on "nearest file wins" behavior (rejected: too much duplicated policy and hidden contradiction risk)
- Push most policy down into skills (rejected: skills become mini knowledge bases and stop being load-efficient)
- Move more personal behavior into the copied AI_OS (rejected: weakens portability and makes repo templates too opinionated)

Implications:
- Codex global remains the home for Maria-only defaults such as plain-language git workflow guidance
- AI_OS master must avoid project-specific build commands and repo-specific path examples
- Repo-local docs should record architecture and migration state rather than copying full skills
- Priority skills should expose optional support files explicitly and remain usable without loading them all

---

Date:
2026-04-05

Project / Context:
AI Operating System — Windows-first path rendering for Maria

Decision:
When returning reusable paths, prompt files, plans, or saved documents to Maria, use the Windows absolute path as the primary user-facing path. WSL paths are secondary and should only be included when technically useful.

Reasoning:
Maria operates on a Windows machine and often needs to reuse paths across chats. Returning `/mnt/c/...` by default forces unnecessary path translation and repeatedly creates friction. The storage location can remain on the Windows filesystem while user-facing reuse should stay Windows-native.

Alternatives Considered:
- Keep returning WSL paths by default because the agent is executing in WSL (rejected: convenient for the agent, annoying for the user)
- Return only WSL paths and expect manual conversion (rejected: recurrent friction and error-prone reuse)
- Return both forms equally every time (rejected: adds noise when one primary path is clearly better for the user)

Implications:
- Windows absolute path is now the default in user-facing answers
- WSL path may still appear in tooling, shell commands, or technical notes when execution requires it
- Saved prompt/runbook responses should be copy-paste-ready for opening in other chats without path conversion

---

Date:
2026-04-05

Project / Context:
Codex prompt and plan generation workflow

Decision:
For substantial prompt or execution-plan requests in Codex, always route through `my-precious` or `my-precious-codex`. If the current project has `AI_OS/`, save the artifact to the project-local documented AI_OS location and return the Windows absolute path.

Reasoning:
Ad hoc inline prompt drafting is too easy to do inconsistently. It leads to prompts that are not persisted, are returned only in chat, or are saved in the wrong place. Codifying `my-precious` as the mandatory routing layer for substantial prompt and plan work makes the behavior explicit and reusable. Requiring project-local AI_OS persistence prevents prompt loss and keeps execution artifacts where future sessions can actually find them.

Alternatives Considered:
- Keep prompt generation as an ordinary chat behavior with no mandatory skill routing (rejected: too inconsistent)
- Save prompts only in chat unless the user explicitly asks for a file (rejected: too fragile)
- Save prompts in global AI_OS instead of the project-local AI_OS when a project already has AI_OS (rejected: weakens project continuity and discoverability)

Implications:
- Codex global guidance should route substantial prompt and plan requests through `my-precious` / `my-precious-codex`
- `my-precious` skills should require persistence when project-local AI_OS exists
- User-facing responses should return the Windows absolute path to the saved artifact, not just inline prompt text

---

Date:
2026-04-19

Project / Context:
Master Collection — project structure

Decision:
Use one parent project with two sibling child folders: `app/` for the Webflow Designer Extension and `site/` for the website/platform.

Reasoning:
The app and site are tightly connected by install codes and package access, but neither owns the other. Treating them as siblings under one Master Collection parent prevents duplicated architecture docs and makes the product boundary clear.

Alternatives Considered:
- Put the site under the app (rejected: the site owns checkout/account/package access and should not be subordinate to the installer)
- Put the app under the site (rejected: the app is a Webflow Designer Extension with a separate runtime and packaging flow)
- Create two unrelated repos (rejected: too easy for docs and contracts to drift)

Implications:
- Shared documentation lives at the parent root under `docs/`.
- Shared AI_OS lives at the parent root under `AI_OS/`.
- Child folders keep only lightweight routing files unless implementation-specific docs become necessary.

---

Date:
2026-04-19

Project / Context:
Master Collection — product boundary

Decision:
The website sells and serves package access; the Webflow app installs packages inside the buyer's current Webflow project.

Reasoning:
The buyer's Webflow site/page context only exists safely inside Webflow. The website should avoid asking for Webflow site IDs, page IDs, or API tokens. The app can read current site/page and upload assets using Webflow Designer APIs.

Alternatives Considered:
- Make the website perform conversion/upload directly (rejected: creates token/site friction and trust problems)
- Keep the old converter playground as the main buyer surface (rejected: too mechanical and not product-shaped)

Implications:
- The site owns catalog, auth, checkout, account library, install codes, package access, and previews.
- The app owns current site/page detection, asset upload into Webflow, XscpData patching, and paste/install handoff.
- Package contracts must be shared between the two surfaces.

---

Date:
2026-04-19

Project / Context:
Master Collection — AI_OS placement

Decision:
Copy and adapt the master `C:\Users\maria\Desktop\AI_OS` into the Master Collection parent root only. Do not create child AI_OS copies in `app/` or `site/`.

Reasoning:
One parent AI_OS keeps the project memory coherent while allowing child folders to have concise local guidance. Copying AI_OS into both children would immediately create drift and duplicate decisions.

Alternatives Considered:
- AI_OS only inside `site/` (rejected: app work would be second-class)
- AI_OS only inside `app/` (rejected: site/platform work would be second-class)
- AI_OS duplicated in both children (rejected: guaranteed drift)

Implications:
- Agents should start at parent `AI.md` and route into the relevant child.
- Parent `docs/DOCS_INDEX.md` is the authoritative docs map.
- Child `AGENTS.md`, `AI.md`, and `CLAUDE.md` files are routing files, not architecture sources of truth.

---

# Guidelines

Good entries should:

• explain reasoning clearly
• include rejected alternatives
• describe consequences

Avoid:

• vague decisions
• undocumented assumptions
• missing context

---

# Purpose

Over time this file becomes:

• a project memory
• an architectural history
• a source of future design guidance

This helps both humans and AI agents maintain **consistent decision-making across sessions**.
