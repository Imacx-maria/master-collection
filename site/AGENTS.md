# AGENTS.md — Master Collection Site

## Scope

This folder is the Master Collection website/platform.

It is a child of:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
```

The site is not the Webflow installer. It showcases, sells, authenticates, grants access, and serves install codes/packages.

## Start Here

1. Read `../AI.md`.
2. Read `../AGENTS.md`.
3. Read `../docs/ARCHITECTURE.md`.
4. Read `../docs/plans/002-master-collection-website-platform.md`.

## Documentation

Do not duplicate parent docs here.

If a doc is about shared product architecture, package flow, auth/payment/account, or site/app boundary, write it under:

```text
..\docs
```

Only create local docs here for site-specific implementation details after the site is scaffolded.

## MVP Boundary

First site MVP:

- public catalog
- template/component pages
- preview pages
- Clerk auth
- Stripe Checkout Sessions
- account library
- install code
- package API for the Webflow app

Do not implement Webflow token/site/page entry on the website.

## UI

Use the same shadcn/Flow-Goodies neutral light baseline documented in `../AGENTS.md`. Keep dark mode disabled until Maria explicitly asks to re-enable it.

## Commands

Use Bun in this folder:

```bash
bun run dev
bun run build
bun run test
bun run lint
bun run typecheck
```
