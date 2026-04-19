# Master Collection Setup

Last verified: 2026-04-19

## Current State

This repository now contains shared documentation plus the first runnable website/platform scaffold.

Maria created:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site
```

The shared AI_OS and project docs were initialized at the parent root.

## GitHub Repositories

Maria created two GitHub repositories:

```text
https://github.com/Imacx-maria/master-collection.git
https://github.com/Imacx-maria/master-collection-app.git
```

Use this local mapping:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
  -> https://github.com/Imacx-maria/master-collection.git

C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
  -> https://github.com/Imacx-maria/master-collection-app.git
```

The parent repository owns shared docs, `AI_OS/`, and the future `site/` runtime. The `app/` folder is ignored by the parent repository because it is its own Git repository.

For Vercel, connect `Imacx-maria/master-collection` and set the Vercel Root Directory to:

```text
site
```

Do not connect the Webflow app to Vercel unless a future architecture decision creates a separate hosted backend or public app surface for it.

Current Vercel status checked on 2026-04-19:

- Vercel CLI is installed.
- `vercel whoami` reports that the configured token is not valid.
- No Vercel project has been linked for this repo yet.

When the site runtime exists, log in again with Vercel CLI and link only the website/platform project.

## AI_OS

Project AI_OS path:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\AI_OS
```

Source template:

```text
C:\Users\maria\Desktop\AI_OS
```

This project intentionally has one AI_OS at the parent root. Do not add child AI_OS copies inside `app/` or `site/`.

During setup, the master AI_OS was copied without:

- `.git/`
- `templates/`
- personal-only `SKILLS/gws-manager/`
- personal-only `SKILLS/user/`
- `references/GOOGLE_ACCOUNTS_MAP.md`
- old master session files

## Planned App Stack

Path:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

Planned:

- Webflow Designer Extension
- TypeScript
- React
- shadcn/ui
- Tailwind v4
- Flow-Goodies neutral light/dark styling baseline

No runtime has been initialized yet.

## Site Stack

Path:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site
```

Initialized:

- Next.js App Router
- TypeScript
- shadcn/ui
- Tailwind v4
- Clerk
- Stripe Checkout Sessions
- fixture-backed product/account/package data
- install-code and package API skeletons

Planned later:

- Postgres database
- package storage

Current commands:

```bash
cd site
npm run dev
npm run build
npm run test
npm run lint
npm run typecheck
```

Do not use bun for the website. Keep bun confined to the separate `app/` Webflow extension.

## Credentials

Do not print or commit secrets.

Future `.env.example` files should document variable names only.

Future `.env.local` files should be ignored by git.

Reference credential locations from older Flowbridge work may be used only as pointers for future setup, not copied into docs:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\wrangler.toml
```

## First Implementation Order

1. Scaffold `app/` from `docs/plans/001-master-collection-extension-mvp.md`.
2. Scaffold `site/` from `docs/plans/002-master-collection-website-platform.md`.
3. Only after both shells exist, connect package/code APIs.

Maria may choose to start with site first if the public catalog/account workflow becomes the current priority.
