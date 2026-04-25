# AGENTS.md — Master Collection

## Project

Master Collection is a three-surface product:

- `site/` — public website, product previews, auth, checkout, account library, install codes, package access.
- `app/` — Webflow Designer Extension that runs inside Webflow and installs a purchased package into the current site/page.
- `chrome-extension/` — Chrome extension companion for browser-side Webflow Designer utilities such as Paste Guard.

All child folders belong to the Master Collection parent project. Do not treat one child surface as the owner of another.

## Start Here

Before code or docs work:

1. Read `AI.md`.
2. Read `docs/DOCS_INDEX.md`.
3. Read `docs/ARCHITECTURE.md`.
4. Read the nearest child `AGENTS.md` for the files you will touch.

## Documentation Rule

There is one authoritative documentation folder:

```text
docs/
```

There is one project AI_OS:

```text
AI_OS/
```

Do not create duplicate AI_OS folders or parallel architecture docs inside `app/` or `site/`. Child docs should be short routing files unless a child-specific implementation detail truly belongs there.

## Current Plans

- `docs/plans/001-master-collection-extension-mvp.md` — first Webflow app MVP.
- `docs/plans/002-master-collection-website-platform.md` — website/platform plan.
- `docs/plans/000-master-collection-extension-future-plan.md` — broader future extension architecture.

Execute the MVP plans before expanding into the future plan.

## Product Boundaries

The website owns:

- catalog
- product pages and previews
- Clerk auth
- Stripe checkout
- account/library
- install codes
- package access

The Webflow app owns:

- current Webflow site/page detection
- font checklist inside Webflow
- asset upload into the buyer's Webflow site
- XscpData patching
- clipboard paste/install handoff

The Chrome extension owns:

- browser-side companion controls for Webflow Designer
- Paste Guard
- interaction cleanup tooling
- lightweight UI aligned with the app visual baseline

The website must not ask buyers for Webflow site IDs, page IDs, or API tokens.

## UI Baseline

All UI surfaces should use the same simple visual baseline:

- shadcn/ui
- `radix-lyra`
- neutral light mode for now; dark mode is reference-only until explicitly re-enabled
- Tailwind v4 CSS variables
- lucide icons
- compact Flow-Goodies-style UI
- no decorative marketing theme at this stage

For the Chrome extension popup, use neutral CSS variables directly and default to system light/dark detection with a small override control.

Reference styling source:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

## Commands

The website runtime has been initialized in `site/` with Bun:

```bash
# site/
bun run dev
bun run build
bun run test
bun run lint
bun run typecheck
```

The Webflow extension runtime is separate under `app/` and also uses Bun:

```bash

# app/
bun run dev
bun run build
bun run test
bun run lint
```

The Chrome extension under `chrome-extension/` is a Manifest V3 extension copied from the prior companion extension. It has no package runtime yet; validate it by checking `manifest.json` and loading the folder as an unpacked extension in Chrome.

## Secrets

Do not print or commit secret values.

Use `.env.example` for variable names. Use ignored `.env.local` files only when execution requires real credentials.

Existing reference credential paths from the old Flowbridge work are documented in the imported plans. Treat them as reference locations, not as values to copy into chat or docs.
