# AGENTS.md — Master Collection

## Project

Master Collection is a two-surface product:

- `site/` — public website, product previews, auth, checkout, account library, install codes, package access.
- `app/` — Webflow Designer Extension that runs inside Webflow and installs a purchased package into the current site/page.

Both folders are children of the Master Collection parent project. Do not treat the site as a child of the app or the app as a child of the site.

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

The website must not ask buyers for Webflow site IDs, page IDs, or API tokens.

## UI Baseline

Both `site/` and `app/` should use the same simple visual baseline:

- shadcn/ui
- `radix-lyra`
- neutral light/dark mode
- Tailwind v4 CSS variables
- lucide icons
- compact Flow-Goodies-style UI
- no decorative marketing theme at this stage

Reference styling source:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

## Commands

The website runtime has been initialized in `site/` with npm:

```bash
# site/
npm run dev
npm run build
npm run test
npm run lint
npm run typecheck
```

The Webflow extension runtime is separate under `app/`:

```bash

# app/
npm run dev
npm run build
npm run test
npm run lint
```

## Secrets

Do not print or commit secret values.

Use `.env.example` for variable names. Use ignored `.env.local` files only when execution requires real credentials.

Existing reference credential paths from the old Flowbridge work are documented in the imported plans. Treat them as reference locations, not as values to copy into chat or docs.
