# Codex Prompt - Master Collection Site A-to-Z Implementation

**Windows path:** `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\AI_OS\SESSION-PROMPTS\SESSIONS\2026-04-19\002-master-collection-site-a-to-z-codex-prompt.md`

Target surface: Codex Desktop or Codex CLI.

Recommended main model: `gpt-5.3-codex`

Recommended main reasoning effort: `high`

Execution mode: autonomous bounded implementation with explicit checkpoints and commits.

Primary working directory:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site
```

Git repository root:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
```

---

## Role

You are Codex implementing the first real Master Collection website/platform inside `site/`.

The site is the storefront/account/package-access surface. It is not the Webflow Designer Extension.

Build the project as a real, runnable Next.js application, guided by the copied UI mockup and the parent project docs.

---

## Required Reading

Before editing, read:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\AI.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\AGENTS.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\CLAUDE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\DOCS_INDEX.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\ARCHITECTURE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\SETUP.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\PROJECT_CONTEXT.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\plans\002-master-collection-website-platform.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site\AGENTS.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site\AI.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site\CLAUDE.md
```

Read-only UI references:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site\_reference\master-collection-ui-mockup.html
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\package.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\components.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\src\index.css
```

Do not modify the Flow-Goodies reference project or the `app/` repo unless a docs file explicitly needs a parent-level update.

---

## Current Inputs

The mockup was copied from:

```text
C:\Users\maria\Downloads\Master Collection UI Mockup.html
```

to:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site\_reference\master-collection-ui-mockup.html
```

Treat the mockup as a visual/IA reference, not source code to extend directly.

The mockup implies a compact product-system shell:

- public catalog
- product detail and preview
- auth and checkout
- account and library
- mobile buyer flow
- shared components/states
- dark mode reference
- admin skeleton only, not admin functionality

Preserve the visual direction:

- sticky dark top bar and compact navigation/tabs
- neutral shadcn-like restraint
- small typography, tight spacing, thin borders
- monospace secondary labels/statuses where useful
- product grids and operational panels first, no hero-first marketing page
- light/dark mode, neutral palette, no decorative gradients/blobs

---

## Current Package/Docs Check

Package versions checked with `npm view` on 2026-04-19:

```text
next 16.2.4
react 19.2.5
react-dom 19.2.5
typescript 6.0.3
tailwindcss 4.2.2
@tailwindcss/postcss 4.2.2
@tailwindcss/vite 4.2.2
shadcn 4.3.0
@clerk/nextjs 7.2.3
stripe 22.0.2
@stripe/stripe-js 9.2.0
zod 4.3.6
lucide-react 1.8.0
next-themes 0.4.6
@radix-ui/react-slot 1.2.4
class-variance-authority 0.7.1
clsx 2.1.1
tailwind-merge 3.5.0
framer-motion 12.38.0
@tanstack/react-query 5.99.2
drizzle-orm 0.45.2
@neondatabase/serverless 1.1.0
```

Official-doc checks from 2026-04-19:

- Next.js App Router install docs: `https://nextjs.org/docs/app/getting-started/installation`
- Clerk Next.js quickstart: `https://clerk.com/docs/nextjs/getting-started/quickstart`
- Clerk middleware/proxy reference: `https://clerk.com/docs/reference/nextjs/clerk-middleware`
- Tailwind v4 + Next guide: `https://tailwindcss.com/docs/guides/nextjs`
- shadcn Tailwind v4 / React 19 notes: `https://ui.shadcn.com/docs/tailwind-v4`
- Stripe Checkout Sessions docs: `https://docs.stripe.com/payments/checkout-sessions`
- Stripe fulfillment docs: `https://docs.stripe.com/checkout/fulfillment`

Use latest stable packages at execution time, but do not silently violate project decisions. If the latest package behavior conflicts with this prompt, stop and explain the conflict.

Important current-stack implications:

- Use Next.js App Router, TypeScript, React 19, Tailwind v4.
- Next.js 16 uses `proxy.ts` for Clerk route protection. Use `middleware.ts` only if you intentionally downgrade to Next <= 15, which is not expected.
- Use Stripe Checkout Sessions for one-time purchase flow. Fulfillment must be webhook/idempotency-first; redirect success is not the source of truth.
- Use `npm` for the website. Keep `bun` confined to the separate `app/` Webflow extension.

---

## Real User Goal

Build the first Master Collection website/platform in:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site
```

The site must support the intended buyer journey:

```text
Browse catalog -> view product -> preview -> sign in -> checkout -> account library -> install code -> Webflow app redeems code
```

The first screen should be useful product/catalog UI, not a marketing landing page.

---

## First Behavior-Changing Step

The first behavior-changing step is creating a runnable Next.js App Router site shell in `site/` that renders the Master Collection public catalog/dashboard shell using the mockup direction.

Name setup-only work as setup-only. Do not end the run with only setup/config/docs unless a real blocker prevents behavior-changing progress.

---

## Git Safety And Commit Plan

Start with:

```bash
git status --short --branch
```

Plain-language state expected at prompt creation:

- parent repo is on `main`
- `docs/DOCS_INDEX.md` and `docs/plans/003-master-collection-app-build-plan.md` may already be dirty from earlier work
- `site/_reference/master-collection-ui-mockup.html` is intentionally present as this task's reference artifact
- `app/` is a separate repo and ignored by parent

Do not revert unrelated changes. Do not stage or commit unrelated dirty docs unless your changes genuinely require them.

Create a working branch from the parent repo unless already on a suitable feature branch:

```bash
git switch -c codex/site-platform-from-mockup
```

If the branch already exists, switch to it after confirming it will not discard work.

Commit in small coherent checkpoints. Suggested commit rhythm:

1. `site: scaffold next app shell`
   - Next.js app builds.
   - npm scripts exist.
   - baseline lint/build passes or blocker documented.
2. `site: add master collection design shell`
   - mockup-inspired shell, theme, navigation, responsive layout.
   - public catalog routes render.
3. `site: add product previews and fixture data`
   - product model, seed products, template/component pages, preview pages.
4. `site: add auth and account skeleton`
   - Clerk provider/proxy/env placeholders, sign-in/sign-up, protected account shell.
5. `site: add checkout and install-code flow skeleton`
   - Stripe session route, webhook skeleton, idempotent fulfillment boundary, install-code model/API.
6. `site: verify and document commands`
   - final verification, docs updates only for durable commands/facts.

Before each commit:

- run the strongest relevant check for that slice;
- stage only files belonging to that slice;
- do not commit secrets or `.env.local`;
- include the copied mockup reference in the first site commit unless Maria has already committed it.

Do not push unless Maria explicitly asks.

---

## Orchestration

Use a main-agent-plus-subagents pattern. Do not spawn a swarm for theater; use bounded lanes with non-overlapping write scopes.

Main agent:

- model: `gpt-5.3-codex`
- effort: `high`
- owns critical path, file integration, final quality bar, final verification, and commits.

Recommended side lanes:

1. Explorer lane - `gpt-5.4-mini`
   - Read docs, mockup, app/reference stack.
   - Return page/surface inventory and constraints.
   - Read-only.
2. Scaffold worker - `gpt-5.3-codex`
   - Own only scaffold/config/design-system files under `site/`: `package.json`, lockfile, `next.config.*`, `tsconfig.json`, `postcss.config.*`, `components.json`, `src/app/layout.tsx`, `src/app/globals.css`, base UI utilities.
   - Do not touch business routes.
3. UI/product worker - `gpt-5.3-codex`
   - Own only public routes, product fixtures, shared site shell/cards/previews.
   - Avoid auth/checkout APIs.
4. Auth/commerce worker - `gpt-5.3-codex`
   - Own only Clerk/Stripe/account/API boundary files after scaffold exists.
   - No UI redesign.
5. Verification lane - `gpt-5.4-mini`
   - Run build/lint/test/browser checks in parallel when main work continues.
   - Report concrete failures, not opinions.

Delegation rules:

- Keep the main agent on the immediate blocking step.
- Delegate only concrete side tasks with non-overlapping file ownership.
- Tell workers they are not alone in the codebase and must not revert others' edits.
- Do not wait on subagents unless the next main-path action is blocked.
- The main agent remains responsible for integration and final verification.
- If subagent edits conflict, stop and merge intentionally; do not blindly overwrite.

---

## Scope

Implement the first website MVP shell and core platform skeleton:

- Next.js App Router site in `site/`
- TypeScript
- npm package manager
- Tailwind v4
- shadcn/ui using the existing `radix-lyra` neutral baseline where supported
- light/dark mode with CSS variables
- lucide icons
- compact Flow-Goodies/Master Collection visual baseline
- public catalog and product routes
- preview route
- product fixture data
- Clerk auth scaffold
- protected account shell
- Stripe Checkout Sessions scaffold
- webhook fulfillment boundary designed for idempotency
- account library/install-code UI skeleton
- package access API skeleton for the Webflow app
- tests for pure product/install-code/fulfillment helpers where practical
- repo-standard build/lint/test verification
- browser smoke verification over the running dev server

Keep `site/_reference/master-collection-ui-mockup.html` as an input artifact. Do not transform it into the app source.

---

## Out Of Scope

Do not implement:

- Webflow Designer Extension logic inside `site/`
- asking buyers for Webflow site IDs, page IDs, API tokens, or Webflow Designer state
- XscpData patching in the website
- asset upload into a buyer's Webflow site
- CMS import
- real package generator UI
- admin product management beyond a clearly marked skeleton/reference route if needed
- second payment provider
- marketplace seller tools
- deployment
- real database provisioning unless credentials and provider are already available
- child `site/AI_OS`
- duplicate architecture docs inside `site/`
- edits to `app/` except read-only inspection

If a task would require credentials or a live service, implement the safe boundary, `.env.example`, and mocked/dev behavior, then mark the live integration as blocked/pending credentials. Do not fake production verification.

---

## Scaffold Rules

The `site/` folder is not empty. It already contains local routing guidance and the copied mockup reference.

Preferred scaffold path:

1. Try to scaffold Next.js into `site/` without deleting existing files.
2. If `create-next-app` refuses because the directory is non-empty, create a temporary sibling scaffold, then move generated app files into `site/` while preserving:
   - `site/AGENTS.md`
   - `site/AI.md`
   - `site/CLAUDE.md`
   - `site/_reference/master-collection-ui-mockup.html`
3. Delete the temporary scaffold after files are moved and verified.

Suggested command shape:

```bash
npx create-next-app@latest site-next-temp --ts --eslint --app --src-dir --tailwind --import-alias "@/*" --use-npm
```

Then move the generated files into `site/` carefully.

After scaffold, expected commands in `site/package.json`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix",
    "typecheck": "tsc --noEmit",
    "test": "vitest run"
  }
}
```

If create-next-app chooses slightly different scripts, keep the standard equivalents and make sure `docs/SETUP.md` / `AGENTS.md` are updated only if durable commands change.

---

## Package Guidance

Use latest stable versions at execution time unless they conflict with docs or each other.

Minimum intended dependencies:

```text
next
react
react-dom
@clerk/nextjs
stripe
@stripe/stripe-js
zod
lucide-react
next-themes
class-variance-authority
clsx
tailwind-merge
@radix-ui/react-slot
```

Minimum intended dev dependencies:

```text
typescript
tailwindcss
@tailwindcss/postcss
shadcn
tw-animate-css
vitest
@testing-library/react
@testing-library/jest-dom
jsdom
eslint
```

Do not install database packages unless you are actually implementing a DB-backed phase. If you reach database work and no provider is configured, prefer a repository/storage interface with in-memory fixtures for local dev and a clearly documented future adapter.

If you do install DB tooling later, prefer one modern Postgres path, not several. Recommended default when Vercel/Neon is chosen: Drizzle ORM + Neon serverless Postgres. Do not assume credentials exist.

---

## UI / IA Requirements

Build the first screen as a useful catalog/product workspace, not a hero page.

Required public routes:

```text
/
/templates
/components
/templates/[slug]
/components/[slug]
/preview/[slug]
```

Required auth/account/checkout skeleton routes:

```text
/sign-in
/sign-up
/checkout/success
/checkout/cancel
/account
/account/library
/account/library/[purchaseId]
/account/installations
/account/billing
```

Optional/admin skeleton only:

```text
/admin
```

Only add `/admin` if it is clearly marked as future/internal and does not expand into real admin CRUD.

Mockup-inspired layout:

- sticky top shell
- compact nav tabs or route-aware segmented nav
- neutral cards/tables/panels
- product preview thumbnails
- install-code panel
- status badges
- dark-mode variant
- mobile buyer-flow layout

Design constraints:

- no decorative marketing theme
- no gradient blobs or ornamental backgrounds
- no purple/purple-blue dominant theme
- no beige/brown/orange theme
- no cards inside cards
- buttons/cards radius 8px or less
- no viewport-scaled font sizing
- text must fit on mobile and desktop
- layout must remain stable when data/status changes
- include visual preview surfaces for products, using local placeholder/mockup imagery or generated preview panels until real product screenshots exist

---

## Domain Model

Start with fixture data, then structure it so real storage can replace it.

Core types:

```ts
type ProductType = "template" | "component";
type ProductStatus = "draft" | "published" | "archived";

type Product = {
  id: string;
  slug: string;
  type: ProductType;
  title: string;
  summary: string;
  description?: string;
  status: ProductStatus;
  currentVersionId?: string;
  priceCents: number;
  currency: string;
  stripePriceId?: string;
  tags: string[];
  thumbnail?: string;
};

type ProductVersion = {
  id: string;
  productId: string;
  version: string;
  packageId: string;
  packageSchemaVersion: "master-collection-package@1";
  previewUrl?: string;
  packageStorageKey?: string;
  validationStatus: "pending" | "passed" | "failed";
  status: ProductStatus;
};

type Order = {
  id: string;
  userId: string;
  provider: "stripe" | "manual" | "other";
  providerSessionId?: string;
  providerPaymentId?: string;
  status: "pending" | "paid" | "failed" | "refunded";
  amountCents: number;
  currency: string;
};

type Entitlement = {
  id: string;
  userId: string;
  productId: string;
  orderId: string;
  status: "active" | "revoked" | "refunded";
};

type InstallCode = {
  id: string;
  codeHash: string;
  entitlementId: string;
  productVersionId: string;
  status: "active" | "used" | "expired" | "revoked";
  maxUses: number;
  useCount: number;
  expiresAt?: string;
};
```

Store hashes, not plain codes, in persistent models. In local mock/dev UI, it is acceptable to display a mock plain code, but keep the production boundary hash-first.

---

## API Route Skeleton

Create route handlers only as far as they can be safely implemented without secrets.

Public/product:

```text
GET /api/products
GET /api/products/[slug]
```

Checkout:

```text
POST /api/checkout/start
POST /api/stripe/webhook
```

Account:

```text
GET /api/account/library
GET /api/account/library/[purchaseId]
POST /api/account/install-codes
```

Extension API:

```text
POST /api/install-code/resolve
GET /api/packages/[packageId]
GET /api/packages/[packageId]/assets/[assetKey]
POST /api/install-events
```

Rules:

- Route handlers must return typed JSON.
- Use Zod for request/response validation where useful.
- Stripe webhook must verify signature when env exists; otherwise return clear local-dev blocked behavior.
- Fulfillment helper must be idempotent by design and unit-tested as a pure function.
- Package access must be entitlement/install-code gated by interface, even if local fixture implementation is mocked.

---

## Auth Rules

Use Clerk.

For Next.js 16, use `proxy.ts` with `clerkMiddleware()`.

Public routes:

```text
/
/templates
/components
/templates/[slug]
/components/[slug]
/preview/[slug]
/sign-in
/sign-up
/checkout/success
/checkout/cancel
```

Protected routes:

```text
/account(.*)
/checkout/start
/api/account(.*)
```

Do not hard-fail local development when Clerk env vars are missing. Provide clear placeholder UI or blocked messages, but keep the app buildable.

Create `.env.example` with variable names only:

```text
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/account
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/account
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

Do not create or commit `.env.local`.

---

## Checkout Rules

Use Stripe Checkout Sessions for one-time purchases.

Require sign-in before checkout.

Checkout session metadata must include:

```text
userId
productId
productVersionId
orderId
```

Webhook fulfillment is the source of truth.

The success page may call/read fulfillment status, but it must not be the only fulfillment mechanism.

Implement idempotency surfaces:

- one order per provider session or explicit pending order
- fulfillment helper checks whether entitlement already exists
- repeated webhook calls do not duplicate entitlements/install codes

---

## Execution Plan

### Phase 0 - Preflight

- Read required docs.
- Inspect git status.
- Confirm current branch / create feature branch.
- Inspect `site/` contents and preserve routing docs/reference mockup.
- Re-check current npm package versions if you need to install packages.
- Define first behavior-changing file set before editing.

Checkpoint: no commit unless only branch creation happened.

### Phase 1 - Scaffold

- Create Next.js App Router project inside `site/`.
- Use npm.
- Add/verify TypeScript, ESLint, Tailwind v4, App Router, `src/` layout, `@/*` alias.
- Add Vitest/test setup if create-next-app did not include tests.
- Add `.env.example`.
- Preserve `site/AGENTS.md`, `site/AI.md`, `site/CLAUDE.md`, `site/_reference/...`.
- Run build/lint/typecheck as available.

Commit if passing or if blocker is understood and documented.

### Phase 2 - Design System And Shell

- Add shadcn config/components using radix-lyra neutral baseline.
- Port neutral CSS variable baseline from Flow-Goodies/app reference as appropriate.
- Add theme provider/toggle with localStorage or `next-themes`.
- Build top shell/nav matching mockup direction.
- Build responsive layout and dark mode.
- Add reusable components: product card, status badge, price label, install-code panel, preview frame, empty state, loading/skeleton.

Commit after build/lint/browser smoke.

### Phase 3 - Public Product Surfaces

- Add fixture product data and typed helpers.
- Implement `/`, `/templates`, `/components`.
- Implement `/templates/[slug]`, `/components/[slug]`.
- Implement `/preview/[slug]`.
- Include product preview visual surfaces.
- Product pages show price, required fonts, package status, CMS/custom-code warnings, preview link, buy/account action.

Commit after tests/build/browser smoke.

### Phase 4 - Auth And Account Shell

- Add Clerk provider.
- Add `proxy.ts` protection for protected routes.
- Add `/sign-in`, `/sign-up`.
- Add `/account`, `/account/library`, `/account/library/[purchaseId]`, `/account/installations`, `/account/billing`.
- Use mock account/library data when Clerk env is missing.
- Do not require real Clerk secrets to build.

Commit after build/lint and route smoke.

### Phase 5 - Checkout And Fulfillment Skeleton

- Add Stripe client/server helpers.
- Add `POST /api/checkout/start`.
- Add `POST /api/stripe/webhook`.
- Add idempotent fulfillment pure helper and tests.
- Add `/checkout/success`, `/checkout/cancel`.
- Use clear blocked response when Stripe env is missing.
- Do not grant duplicate entitlements in helper tests.

Commit after tests/build.

### Phase 6 - Install Code And Package API Skeleton

- Add install-code creation/generation/hash helper.
- Add install-code resolve API for the Webflow app.
- Add package API skeleton with entitlement/install-code checks at the interface boundary.
- Add install event route.
- Add tests for install-code validation and package access guard.

Commit after tests/build.

### Phase 7 - Verification And Docs

- Run final verification.
- Update parent docs only if durable commands or facts changed:
  - `docs/SETUP.md`
  - `AGENTS.md`
  - `site/AGENTS.md`
  - `docs/DOCS_INDEX.md` only if adding/moving docs
- Do not create duplicate docs under `site/`.
- Final commit only if coherent and verified.

---

## Verification

Use exactly one final verification label:

- `repo-standard verified` - repo-standard checks ran successfully.
- `partial verification` - only targeted/ad hoc/fallback checks ran.
- `unverified` - intended verification did not run successfully.

Required checks by the end:

```bash
npm run typecheck
npm run lint
npm run test
npm run build
```

If one script does not exist, either add it as part of scaffold or explicitly explain why it is not present.

Browser verification:

- Start dev server in `site/`.
- Use browser automation/Playwright/agent-browser if available.
- Check desktop and mobile widths.
- Visit:
  - `/`
  - `/templates`
  - `/components`
  - one product detail route
  - one preview route
  - `/account`
  - `/checkout/success`
- Confirm no critical console errors.
- Confirm light/dark toggle works.
- Confirm text does not overflow at mobile width.
- Confirm product cards and install-code panels are layout-stable.

Do not claim Webflow app integration or live Stripe/Clerk fulfillment unless actually verified with credentials.

---

## Coding Discipline

- Surface material assumptions before editing.
- Ask if ambiguity would materially change the outcome; otherwise choose the smallest reversible path and state it.
- Prefer the smallest direct implementation. Do not add speculative features, abstractions, options, or framework changes.
- Keep edits surgical: touch only files needed for this request, match local style, and avoid drive-by cleanup or formatting.
- Clean up only unused code introduced or orphaned by your own change.
- Define concrete success criteria before claiming completion, then verify with the lightest credible repo-standard check.
- Preserve existing user changes.
- Never run destructive git commands without explicit approval.
- Never print or commit secrets.

---

## What Does Not Count As Success

The session is not successful if it only:

- creates planning docs
- adds configuration with no running UI
- creates a generic landing page instead of the useful catalog/account shell
- copies the mockup HTML as the runtime app instead of implementing the site
- implements catalog pages with no product data model
- implements checkout UI without a server-side Stripe boundary
- implements account pages without an install-code/package-access boundary
- claims Clerk/Stripe production readiness without credentials and live verification
- modifies `app/` responsibilities into the site
- asks buyers for Webflow site/page/API-token details

---

## Stop Conditions

Stop and report instead of improvising if:

- package latest versions create incompatible install/build failures after two focused attempts;
- Clerk/Stripe live behavior is required but credentials are missing;
- create-next-app or shadcn CLI wants to overwrite existing guidance/reference files;
- a requested site behavior belongs to the Webflow app boundary;
- the same build/test issue fails after two fix attempts;
- git state is too mixed to stage only your own coherent changes.

When stopped, report:

- exact blocker
- files changed so far
- verification run
- safest next option

---

## Required Final Report

Include:

1. Final outcome classification, exactly one:
   - `setup-only`
   - `guardrail-only`
   - `behavior-changing`
   - `blocked`
2. Verification label, exactly one:
   - `repo-standard verified`
   - `partial verification`
   - `unverified`
3. Branch name.
4. Commit hashes created, with one-line purpose for each.
5. Files/folders changed.
6. Commands run and pass/fail result.
7. Browser verification summary.
8. Any credentials/live-service blockers.
9. What Maria should do next in plain language.

Always include full Windows paths for created files or important artifacts.
