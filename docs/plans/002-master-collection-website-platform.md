# Master Collection Website And Platform Plan

> **For agentic workers:** This is a planning artifact. Do not implement until Maria explicitly asks. Use this together with `093-plan-master-collection-mvp.md`, which covers the inside-Webflow Designer Extension. The website is the storefront/account/package vehicle; the Webflow app is the target-site installer.

**Goal:** Replace the old minimal converter playground with a real Master Collection website that showcases templates/components, handles accounts, checkout, purchased-product access, package preparation status, and install codes for the Master Collection Webflow app.

**Style:** Same visual baseline as the Master Collection app and current Flow-Goodies app: shadcn, bare neutral style, light/dark mode only, compact UI, no decorative marketing theme at this stage.

**MVP product idea:** Every template/component has a public web page that shows the item. If the user buys, they sign in, pay, and receive access in their account. The account page gives them an install code and package status. The user then opens the Master Collection app inside Webflow and pastes the code there.

---

## 1. Core Decision

The old minimal converter should stop being an end-user converter UI.

It becomes the foundation for:

```text
Master Collection website
public product previews
account/library access
package delivery
install-code issuance
```

The actual Webflow import remains inside:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

The website should not ask the buyer for:

- Webflow site ID
- Webflow page ID
- Webflow API token
- Webflow Designer state

Those belong inside the Webflow Designer Extension, because the app is running in the buyer's actual Webflow project.

---

## 2. High-Level Product Split

Use three connected surfaces:

```text
1. Master Collection Website
   Public catalog, previews, account, checkout, library, install codes.

2. Master Collection Package Backend
   Entitlements, package manifests, private assets, install-code resolution.

3. Master Collection Webflow App
   Runs inside Webflow and installs into the current site/page.
```

This keeps the user journey simple:

```text
Browse -> Buy -> Account Library -> Install Code -> Open Webflow App -> Paste Code -> Install
```

---

## 3. Recommended Stack

### Website

Recommended:

```text
Next.js App Router
TypeScript
shadcn/ui
Tailwind v4
Clerk
Stripe Checkout Sessions
Postgres database
Object storage for packages/assets
```

The exact host can be decided later. Vercel is a natural fit if using Next.js + Clerk + Stripe, but this plan does not require deployment yet.

### Authentication

Use Clerk.

Current official Clerk direction checked on 2026-04-19:

- Clerk supports Next.js App Router.
- Clerk uses `ClerkProvider`.
- Clerk uses `clerkMiddleware()`.
- Current docs mention `proxy.ts` for Next.js 16 and `middleware.ts` for Next.js <= 15.

Source:

```text
https://clerk.com/docs/nextjs/getting-started/quickstart
```

### Payments

Use Stripe first.

Current official Stripe direction checked on 2026-04-19:

- Use Checkout Sessions for most one-time purchases.
- Use webhooks for fulfillment.
- Do not rely only on the success redirect.
- Make fulfillment idempotent.

Sources:

```text
https://docs.stripe.com/payments/checkout-sessions
https://docs.stripe.com/checkout/fulfillment
```

### Second Payment Gateway

Do not implement a second gateway in MVP unless Maria chooses the provider.

Instead, design the database and code with a provider field:

```text
paymentProvider = "stripe" | "paypal" | "manual" | "other"
```

Stripe should ship first. A second gateway can plug into the same order and entitlement model later.

---

## 4. Naming

Public brand:

```text
Master Collection
```

Website working repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site
```

Webflow app repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

Package schema:

```text
master-collection-package@1
```

Webflow app package interface:

```ts
MasterCollectionPackage
```

Do not rename the parent project folder:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY
```

---

## 5. What The Website Must Do

The website owns:

- public catalog
- public product pages
- product previews
- authentication
- checkout entry
- payment fulfillment
- account dashboard
- purchase library
- package access
- install-code creation
- install-code status
- customer download/access history
- admin product/package management later

The website does not own:

- upload images into buyer's Webflow site
- determine buyer's current Webflow page
- paste XscpData into Webflow
- ask for Webflow token
- ask for Webflow site ID

---

## 6. User Journey

### 6.1 New Buyer

```text
Catalog page
Product page
Preview page
Buy button
Sign up/sign in with Clerk
Stripe Checkout
Checkout success page
Account library
Owned product page
Generate or reveal install code
Open Webflow
Open Master Collection app
Paste code
Install package
```

### 6.2 Returning Buyer

```text
Sign in
Account library
Choose purchased item
View package/version
Copy install code
Open Webflow app
Install
```

### 6.3 Admin/Seller Later

```text
Admin products
Create product
Upload prepared package/zip
Generate preview
Validate package
Publish product page
Monitor orders/install events
```

---

## 7. Page Plan - Public Website

### 7.1 `/`

Purpose:

Default entry point and catalog gateway.

MVP content:

- Master Collection name
- short explanation: templates and components for Webflow
- featured templates
- featured components
- sign in/account button
- theme toggle

Important:

- Do not make this a heavy marketing landing page first.
- The useful content should be the collection grid.

Primary actions:

- browse templates
- browse components
- sign in

### 7.2 `/templates`

Purpose:

Template catalog.

MVP content:

- grid/list of templates
- filters later: category, CMS, animations, free/paid
- price
- preview thumbnail
- "View" action

Data needed:

- product id
- slug
- title
- summary
- price
- status
- thumbnail
- tags

### 7.3 `/components`

Purpose:

Component catalog.

MVP content:

- grid/list of components
- price
- preview thumbnail
- category
- "View" action

Same model as templates, but product type is `component`.

### 7.4 `/templates/[slug]`

Purpose:

Public template product page.

MVP content:

- live preview/demo area or preview link
- title
- price
- short description
- included sections/pages
- required fonts
- CMS requirement flag
- interaction/custom-code warning if relevant
- screenshots or iframe preview
- buy button
- sign in/account button if already owned

Primary actions:

- preview
- buy
- open in account if owned

Important:

- This page is the new "vehicle" replacing the old converter playground for public viewing.
- It displays the template, but does not expose install package JSON to non-buyers.

### 7.5 `/components/[slug]`

Purpose:

Public component product page.

MVP content:

- component preview
- title
- price
- required fonts
- assets included
- Webflow compatibility notes
- buy button
- account link if owned

### 7.6 `/preview/[slug]`

Purpose:

Clean standalone product preview.

MVP content:

- full-page template/component preview
- minimal chrome
- back to product link
- theme control only if useful

Important:

- This can be generated from the same prepared source used for package generation.
- It should not show installer controls.
- It should not require auth for public previews unless the product is private.

### 7.7 `/pricing` or `/collection`

Purpose:

Optional later page for bundles or collection-level purchase.

MVP:

- skip unless selling bundles from day one.

---

## 8. Auth Pages

Use Clerk-hosted/drop-in components first.

### 8.1 `/sign-in`

Purpose:

User sign in.

MVP content:

- Clerk SignIn
- same Master Collection shell/header
- redirect back to intended product/account page

### 8.2 `/sign-up`

Purpose:

User registration.

MVP content:

- Clerk SignUp
- same Master Collection shell/header
- redirect to checkout or account after signup

### 8.3 Auth Route Protection

Public:

```text
/
/templates
/components
/templates/[slug]
/components/[slug]
/preview/[slug]
/sign-in
/sign-up
```

Protected:

```text
/account
/account/library
/account/library/[purchaseId]
/account/installations
/account/billing
/checkout/start
```

Admin protected:

```text
/admin
/admin/products
/admin/packages
/admin/orders
```

---

## 9. Checkout Pages And Flow

### 9.1 Recommended Checkout Rule

Require sign-in before checkout.

Reason:

- digital products need account access
- install codes must attach to a user
- avoids orphaned purchases
- makes account library reliable

Guest checkout can be added later if needed, but it adds support burden.

### 9.2 `/checkout/start`

Purpose:

Server-side endpoint/action that creates Stripe Checkout Session.

Inputs:

- product id
- product version id or current published version
- authenticated Clerk user id

Stripe metadata must include:

```text
userId
productId
productVersionId
orderId
```

Output:

- redirect to Stripe-hosted Checkout URL

### 9.3 Stripe Checkout Session

Use:

```text
mode = payment
Checkout Sessions API
Stripe-hosted Checkout first
```

Do not build a custom card form for MVP.

### 9.4 `/checkout/success`

Purpose:

Landing page after Stripe returns.

MVP content:

- payment received / preparing access
- link to account library
- if entitlement already exists, show purchased item
- if webhook is delayed, show "still preparing" state and poll/retry gently

Important:

- Success page is not the source of truth.
- Webhook fulfillment is source of truth.

### 9.5 `/checkout/cancel`

Purpose:

Return from canceled Checkout.

MVP content:

- "Checkout was canceled"
- return to product page
- try again

### 9.6 `/api/stripe/webhook`

Purpose:

Fulfill purchases reliably.

Events:

- `checkout.session.completed`
- `checkout.session.async_payment_succeeded`
- optionally `checkout.session.async_payment_failed`

Behavior:

- verify Stripe signature
- retrieve session/line items if needed
- idempotently mark order paid
- grant entitlement
- create license/install-code seed
- record fulfillment event

Important:

- Must be safe if called multiple times.
- Must not grant duplicate entitlements incorrectly.

---

## 10. Account Pages

### 10.1 `/account`

Purpose:

User home/dashboard.

MVP content:

- user identity
- purchased item count
- recent purchases
- install status summary
- link to library
- billing link

Primary actions:

- view library
- continue installation

### 10.2 `/account/library`

Purpose:

Purchased templates/components.

MVP content:

- list/grid of owned products
- product type
- version
- purchase date
- install status
- "Open" action

Each card/item should show:

- title
- thumbnail
- product type
- current package version
- status: ready / preparing / needs update / archived

### 10.3 `/account/library/[purchaseId]`

Purpose:

Owned product access page. This is the first part of the operation after purchase.

MVP content:

- product title
- package/version status
- install code
- required fonts
- package requirements
- "Open Master Collection app in Webflow" instruction
- copy install code button
- preview link
- support/troubleshooting notes

Install code section:

- reveal or generate install code
- copy button
- expiration/reuse policy
- last used timestamp if available

Package status section:

```text
Ready
Preparing
Failed validation
Archived
Update available
```

Requirements section:

- fonts
- images/assets
- CMS required or not
- custom code required or not
- Webflow plan notes if relevant

Do not show raw XscpData by default.

### 10.4 `/account/installations`

Purpose:

History of install sessions.

MVP content:

- install code
- product
- created date
- last redeemed date
- target site name/id if the Webflow app reports it
- status

This is optional for MVP but useful once the extension sends install events.

### 10.5 `/account/billing`

Purpose:

Payment/order access.

MVP content:

- orders
- receipts/invoices link from Stripe if available
- payment status

For MVP, this can be simple and read-only.

---

## 11. Check-In / Check-Out Concept

Interpret "checkout" as payment checkout and "check-in" as installation session preparation.

### 11.1 Checkout

Checkout means:

```text
User pays for the product.
Stripe confirms payment.
Website grants entitlement.
```

### 11.2 Check-In

Check-in means:

```text
User opens an owned product.
Website creates or activates an install session.
Website gives an install code.
Webflow app redeems that code.
```

### 11.3 Check-Out / Completion

Completion means:

```text
Webflow app reports package prepared/copied/installed.
Website marks install session complete or partially complete.
```

Install session statuses:

```text
created
code_issued
redeemed_in_app
assets_uploaded
payload_copied
installed
failed
expired
```

---

## 12. Package And Converter Vehicle

### 12.1 What Replaces The Minimal Converter UI

The old converter playground becomes two things:

```text
1. Product preview page
2. Package preparation pipeline
```

Public visitors see the preview, not the conversion controls.

Authenticated buyers see package/install access, not converter internals.

### 12.2 Source Artifacts

For each product/version, store:

```text
source zip or prepared source
converted preview page
MasterCollectionPackage JSON
asset files
font manifest
CMS manifest if any
validation report
screenshots
```

The buyer does not need to see the raw zip.

### 12.3 Package Flow

```text
Designer creates template/component in Webflow
Source export/pre-treatment happens
Package generator builds MasterCollectionPackage
Website stores package privately
Public preview page is generated
Product page is published
Buyer purchases
Account page grants install code
Webflow app redeems code and installs
```

### 12.4 Package Access

Package JSON and private assets should be available only when:

- user owns entitlement, or
- install code is valid, or
- admin preview is being used

Public preview assets can be separate from private install package assets.

---

## 13. Data Model

### 13.1 Users

Stored through Clerk plus local mirror.

```ts
type User = {
  id: string;
  clerkUserId: string;
  email: string;
  name?: string;
  createdAt: string;
};
```

### 13.2 Products

```ts
type Product = {
  id: string;
  slug: string;
  type: "template" | "component";
  title: string;
  summary: string;
  description?: string;
  status: "draft" | "published" | "archived";
  currentVersionId?: string;
  priceCents: number;
  currency: string;
  stripePriceId?: string;
  createdAt: string;
  updatedAt: string;
};
```

### 13.3 Product Versions / Packages

```ts
type ProductVersion = {
  id: string;
  productId: string;
  version: string;
  packageId: string;
  packageSchemaVersion: "master-collection-package@1";
  previewUrl?: string;
  packageStorageKey: string;
  validationStatus: "pending" | "passed" | "failed";
  status: "draft" | "published" | "archived";
  createdAt: string;
};
```

### 13.4 Orders

```ts
type Order = {
  id: string;
  userId: string;
  provider: "stripe" | "manual" | "other";
  providerSessionId?: string;
  providerPaymentId?: string;
  status: "pending" | "paid" | "failed" | "refunded";
  amountCents: number;
  currency: string;
  createdAt: string;
  paidAt?: string;
};
```

### 13.5 Entitlements

Entitlement means the user owns access.

```ts
type Entitlement = {
  id: string;
  userId: string;
  productId: string;
  orderId: string;
  status: "active" | "revoked" | "refunded";
  createdAt: string;
};
```

### 13.6 Install Codes

```ts
type InstallCode = {
  id: string;
  codeHash: string;
  entitlementId: string;
  productVersionId: string;
  status: "active" | "used" | "expired" | "revoked";
  maxUses: number;
  useCount: number;
  expiresAt?: string;
  createdAt: string;
};
```

Store hashes, not plain codes, if possible.

### 13.7 Install Sessions

```ts
type InstallSession = {
  id: string;
  installCodeId: string;
  userId: string;
  productId: string;
  productVersionId: string;
  webflowSiteId?: string;
  webflowSiteName?: string;
  webflowPageId?: string;
  status:
    | "created"
    | "redeemed_in_app"
    | "assets_uploaded"
    | "payload_copied"
    | "installed"
    | "failed";
  createdAt: string;
  updatedAt: string;
};
```

### 13.8 Package Assets

```ts
type PackageAsset = {
  id: string;
  productVersionId: string;
  assetKey: string;
  storageKey: string;
  fileName: string;
  mimeType: string;
  sizeBytes?: number;
  hash?: string;
};
```

---

## 14. API Route Plan

### Public/Product API

```text
GET /api/products
GET /api/products/[slug]
```

Optional if using server components directly.

### Checkout API

```text
POST /api/checkout/start
POST /api/stripe/webhook
```

### Account API

```text
GET /api/account/library
GET /api/account/library/[purchaseId]
POST /api/account/install-codes
```

### Extension API

Used by the Master Collection Webflow app.

```text
POST /api/install-code/resolve
GET /api/packages/[packageId]
GET /api/packages/[packageId]/assets/[assetKey]
POST /api/install-events
```

The extension should call these with install code and app metadata. It should not need a buyer Webflow token.

### Admin API Later

```text
POST /api/admin/products
POST /api/admin/packages
POST /api/admin/packages/[id]/validate
POST /api/admin/products/[id]/publish
```

---

## 15. Admin Pages Later

Not MVP, but the architecture should leave room.

### 15.1 `/admin`

Purpose:

Admin overview.

Content:

- products count
- packages needing validation
- recent orders
- failed installs

### 15.2 `/admin/products`

Purpose:

Manage templates/components.

Content:

- product table
- status
- current version
- sales count
- edit action

### 15.3 `/admin/products/new`

Purpose:

Create product shell.

Fields:

- title
- slug
- product type
- price
- summary
- tags

### 15.4 `/admin/products/[id]`

Purpose:

Edit product and versions.

Content:

- product metadata
- preview
- versions
- package validation state
- publish/archive controls

### 15.5 `/admin/packages/[id]`

Purpose:

Package processing/validation.

Content:

- source artifact
- generated preview
- package manifest
- font list
- asset list
- CMS manifest
- validation report

---

## 16. UI Requirements

Use same baseline as Flow-Goodies and Master Collection app:

```text
shadcn
radix-lyra
neutral palette
Tailwind v4
CSS variables
light/dark mode only
lucide icons
compact spacing
no decorative marketing theme
```

Reference:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\components.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\index.css
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\components\App.tsx
```

Website layout should be simple:

- top nav
- theme toggle
- account button
- product grids
- product detail pages
- account pages
- plain tables/checklists

No custom visual design needed yet.

---

## 17. MVP Build Order

### Phase 1 - Website Skeleton

Tasks:

- [ ] Create `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site`.
- [ ] Set up Next.js App Router.
- [ ] Add TypeScript.
- [ ] Add shadcn using same neutral baseline.
- [ ] Add light/dark mode.
- [ ] Create public layout.
- [ ] Create placeholder pages:
  - `/`
  - `/templates`
  - `/components`
  - `/templates/[slug]`
  - `/components/[slug]`
  - `/preview/[slug]`

Verification:

- [ ] Build passes.
- [ ] Light/dark toggle works.
- [ ] Pages route correctly.

### Phase 2 - Product Data And Preview

Tasks:

- [ ] Define product model.
- [ ] Add fixture products.
- [ ] Render catalog grids.
- [ ] Render product pages.
- [ ] Render preview page from fixture.
- [ ] Add required fonts/assets/CMS notes on product page.

Verification:

- [ ] Template and component pages show fixture products.
- [ ] Product detail page links to preview.

### Phase 3 - Clerk Auth

Tasks:

- [ ] Add Clerk.
- [ ] Add sign-in/sign-up pages.
- [ ] Protect account routes.
- [ ] Add account shell.
- [ ] Add user button/account nav.

Verification:

- [ ] Public pages remain public.
- [ ] Account pages require sign-in.
- [ ] Signed-in user can reach `/account`.

### Phase 4 - Stripe Checkout

Tasks:

- [ ] Add Stripe SDK.
- [ ] Create checkout start route.
- [ ] Create orders table/model.
- [ ] Create Stripe Checkout Session.
- [ ] Add success/cancel pages.
- [ ] Add webhook route.
- [ ] Fulfill order idempotently.
- [ ] Grant entitlement.

Verification:

- [ ] Test purchase creates Stripe session.
- [ ] Webhook marks order paid.
- [ ] Entitlement appears in account library.

### Phase 5 - Account Library

Tasks:

- [ ] Create `/account/library`.
- [ ] Create `/account/library/[purchaseId]`.
- [ ] Show purchased products.
- [ ] Show package status.
- [ ] Generate/reveal install code.
- [ ] Copy install code.

Verification:

- [ ] Paid user sees owned product.
- [ ] Non-owner cannot access product package page.
- [ ] Install code is generated for owned product.

### Phase 6 - Extension Package API

Tasks:

- [ ] Add `POST /api/install-code/resolve`.
- [ ] Add `GET /api/packages/[packageId]`.
- [ ] Add asset access route.
- [ ] Add install event route.
- [ ] Return `MasterCollectionPackage`.
- [ ] Enforce entitlement/install-code access.

Verification:

- [ ] Master Collection extension can resolve code.
- [ ] Package JSON is returned only for valid code.
- [ ] Package assets are fetchable by the extension.

### Phase 7 - Real Package Pipeline

Tasks:

- [ ] Connect package generator output to product version.
- [ ] Store package JSON and assets.
- [ ] Generate public preview page.
- [ ] Validate package before publishing.
- [ ] Show validation status in admin or temporary internal page.

Verification:

- [ ] Real prepared package appears in account library.
- [ ] Extension can install it in Webflow.

---

## 18. MVP Cut Line

MVP includes:

- public product pages
- preview pages
- Clerk auth
- Stripe one-time payment
- account library
- install code
- package API for extension
- basic package storage

MVP excludes:

- CMS automation
- seller dashboard
- marketplace payouts
- subscriptions
- bundles
- coupons
- refunds UI
- second payment gateway
- Webflow token entry
- custom code install

---

## 19. Open Decisions

Maria should decide later:

1. Second payment gateway:
   - PayPal?
   - Paddle?
   - Lemon Squeezy?
   - manual invoices?

2. Database:
   - Supabase Postgres?
   - Neon?
   - Vercel Postgres/Marketplace?

3. Hosting:
   - Vercel?
   - Cloudflare?

4. Package storage:
   - reuse current B2/Cloudflare worker?
   - create Master Collection package worker?

5. Purchase model:
   - individual products only?
   - bundles?
   - full collection membership?

6. Install-code policy:
   - one code per purchase?
   - reusable codes?
   - expiring codes?
   - per-site install limits?

Recommended defaults:

- Stripe first.
- Sign-in required before checkout.
- Postgres database.
- Reuse existing B2/Cloudflare only for prototype.
- Create Master Collection package worker for production.
- One install code per purchase, reusable during MVP, with logged install events.

---

## 20. First Executor Prompt

Use this only when Maria asks to implement the website skeleton.

```text
Build the Master Collection website skeleton. This is not the Webflow extension.

Read:
1. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md
2. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\CLAUDE.md
3. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\plans\002-master-collection-website-platform.md
4. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\plans\001-master-collection-extension-mvp.md

Create:
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\site

Goal for first pass:
- Next.js App Router skeleton
- TypeScript
- shadcn using the same Flow-Goodies neutral light/dark baseline
- public pages:
  - /
  - /templates
  - /components
  - /templates/[slug]
  - /components/[slug]
  - /preview/[slug]
- fixture product data
- no Clerk yet
- no Stripe yet
- no backend yet
- no custom design beyond the bare shared style

Before editing, state exact files you will create.
Verify with build and local dev server browser check if feasible.
```

---

## 21. Recommendation

Build the Master Collection website first as a clean storefront/account shell, not as a converter UI.

The old converter was useful as a playground, but the buyer-facing site should be:

```text
catalog
product preview
checkout
account library
install code
package access
```

Then the Master Collection Webflow app remains the place where installation actually happens.

