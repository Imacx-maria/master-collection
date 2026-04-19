# AI.md — Master Collection AI Loader

Read this at the start of any AI session in this project.

This project has one shared AI brain at the parent root:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\AI_OS
```

Do not create separate `AI_OS/` folders inside `app/` or `site/`.

## Boot

1. Read `AI_OS/SESSION-PROMPTS/AI_SESSION_START.md`.
2. Read `AGENTS.md`.
3. Read `docs/DOCS_INDEX.md`.
4. Load the relevant child guidance:
   - `app/AGENTS.md` for the Webflow Designer Extension.
   - `site/AGENTS.md` for the website/platform.
5. Load the relevant plan from `docs/plans/`.

## Project Map

```text
MASTER-COLLECTION/
  app/   Master Collection Webflow Designer Extension
  site/  Master Collection website/platform
```

The app and site are siblings. Both are children of the Master Collection product. Neither owns the other.

## Source Of Truth

Project documentation lives at the parent root:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs
```

Child folders may have local `AGENTS.md`, `AI.md`, and `CLAUDE.md` files, but they should route to the parent docs instead of duplicating architecture decisions.

