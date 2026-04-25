# DOCS_INDEX — Master Collection

> Source of truth for Master Collection documentation.
> Before creating any new document, check this index first.

Last verified: 2026-04-25

## Living Documents (HOT — Always Current)

| Document | Path | Describes |
|----------|------|-----------|
| Architecture | `docs/ARCHITECTURE.md` | Current site/app/Chrome extension boundaries, package flow, and data flow |
| Setup | `docs/SETUP.md` | Current setup state, planned stacks, and credential rules |
| Project Context | `docs/PROJECT_CONTEXT.md` | Conversation-derived decisions and product vocabulary |
| Webflow App Research | `docs/WEBFLOW_APP_RESEARCH.md` | Official Webflow docs findings for Designer Extension capabilities and MVP boundaries |
| AI Session Entry | `AI.md` | Universal entry point for any AI session in this project |
| Agent Guidance | `AGENTS.md` | Operational guidance for Codex, Claude, and other coding agents |
| Claude Conventions | `CLAUDE.md` | Claude Code specific conventions for this project |

## Active Plans (Temporary)

| Document | Path | Purpose | Expected Completion |
|----------|------|---------|-------------------|
| Extension MVP | `docs/plans/001-master-collection-extension-mvp.md` | Build the first inside-Webflow app scope | After app MVP scaffold and verification |
| Website Platform | `docs/plans/002-master-collection-website-platform.md` | Build the site/account/checkout/package-access plan | After site skeleton, auth, checkout, and package API are implemented |
| App Build Plan | `docs/plans/003-master-collection-app-build-plan.md` | Detailed implementation plan for the first Webflow Designer Extension build | After app MVP scaffold and verification |
| Future Extension Plan | `docs/plans/000-master-collection-extension-future-plan.md` | Larger future plan including CMS/Hybrid/backend expansion | Archive or revise after MVP validates |

## Append-Only Documents

| Document | Path | Describes |
|----------|------|-----------|
| AI Decision Log | `AI_OS/AI_DECISION_LOG.md` | Stable architectural decisions and rationale |

## Child Project Routing

| Child | Path | Local Guidance |
|-------|------|----------------|
| Webflow app | `app/` | `app/AGENTS.md`, `app/AI.md`, `app/CLAUDE.md` |
| Website | `site/` | `site/AGENTS.md`, `site/AI.md`, `site/CLAUDE.md` |
| Chrome extension | `chrome-extension/` | `chrome-extension/AGENTS.md` |

## Archived (COLD)

Use `docs/_archive/` for completed plans, superseded investigations, and consumed handoffs.

## Rules

1. Do not duplicate architecture docs inside `app/`, `site/`, or `chrome-extension/`.
2. Keep child guidance short and route back to this parent docs folder.
3. Update this index when creating, archiving, or moving docs.
4. Move completed plans to `docs/_archive/` after they are consumed.
