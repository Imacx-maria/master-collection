# New Master Collection Extension — Detailed Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `writing-plans` or the local AI_OS execution workflow before implementation. Use `architect-advisor` for architecture decisions that change the split between marketplace, package backend, converter, and Webflow Designer Extension. Use `verification-orchestrator` before claiming completion.

**Goal:** Build a new Webflow Designer Extension named **Master Collection**, separate from the current Flow-Goodies extension, that lets a buyer enter a purchase/install code inside Webflow, fetch a prepared Master Collection package, run preflight checks, upload images/assets into the buyer's current Webflow site, guide manual font installation, optionally import CMS data, patch the XscpData payload for the current page/site, and paste/install the template or component with minimal user friction.

**Architecture:** Keep generation and installation separate. The skill/converter/build pipeline produces a portable package. The new Webflow extension is the target-aware installer. The marketplace/backend handles purchase codes, package access, package storage, and secrets. Webflow remains the only place where page/site context is known safely.

**Tech Stack:** Webflow Designer Extension API, Webflow Data API/Hybrid App path where available, TypeScript, React, Webpack or Vite after scaffold decision, Webflow clipboard XscpData, existing Flowbridge converter output, Cloudflare Worker + Backblaze B2 or equivalent package storage, Vitest/unit tests, browser/manual Designer verification.

**Status:** Planning artifact only. Do not implement from this file without first refreshing current repo state, because Webflow API capabilities and the local extension repos may have changed after 2026-04-19.

---

## 0. Executive Decision

Build a new extension, not a modification of the existing app.

Recommended new repo path:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

The existing Flow-Goodies app remains a reference implementation and fallback:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

The Flowbridge converter / package generator remains the generation-side source of truth:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude
```

The old converter and Cloudflare/B2 implementation remain reference material:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean
```

This plan intentionally avoids making the marketplace page or converter responsible for user-site installation. The installer extension runs inside the buyer's Webflow project, so it can obtain the current site ID and current page ID without asking the user to type them.

---

## 1. Product Flow We Are Building

### 1.1 Buyer Experience

1. Buyer purchases a template or component from the Flow Party marketplace.
2. Buyer receives an install code.
3. Buyer opens their target Webflow project.
4. Buyer opens the new Master Collection extension inside Webflow.
5. Buyer enters the install code.
6. Extension fetches package metadata and checks the current Webflow site/page.
7. Extension shows a preparation checklist:
   - package name/version
   - target site name
   - target page name
   - required fonts
   - missing fonts that must be installed manually
   - images/assets to upload
   - CMS collections/items to create or map
   - custom-code/runtime requirements, if any
   - interaction support notes, if any
8. If fonts are missing, the extension tells the user exactly which fonts to install before continuing.
9. User installs fonts manually in Webflow when required.
10. User returns to the extension and clicks a rescan button.
11. Extension uploads package images/assets into the current Webflow site.
12. Extension patches the XscpData payload with real Webflow asset IDs, current page ID, and any site-specific replacements.
13. Extension handles CMS data in the least confusing supported path:
    - automated import if app scopes/API capability are available
    - guided import/mapping if full automation is not available
14. Extension copies or injects the final XscpData into Webflow using the correct lane.
15. User pastes once, or clicks one install action if the payload is safe for direct Designer API insertion.
16. Extension runs post-install verification and shows any required manual follow-up.

### 1.2 Seller / Designer Experience

1. Designer builds in Webflow.
2. We export or capture source data.
3. Pre-treatment skill cleans and classifies the export.
4. Converter/package generator produces a marketplace-ready install package.
5. Package is uploaded to package storage.
6. Marketplace creates a product record and purchase/install code.
7. Buyer uses the new extension to install.

### 1.3 What This Solves

The converter cannot reliably upload images and CMS into the buyer's Webflow site unless it has buyer-specific token and site information. Asking users to paste tokens and site IDs into a marketplace page is friction-heavy and scary.

The extension runs inside Webflow, so it can:

```text
get current site -> upload assets to that site -> get current page -> patch XscpData -> install/paste
```

This also makes the font step clearer. Fonts are a Webflow project setup concern and often need manual installation. The extension can detect missing fonts before installation and guide the user while they are preparing to receive the template.

---

## 2. Current Evidence And Source References

### 2.1 Current Project State

Primary repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude
```

Important project files:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\CLAUDE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\src\lib\AGENTS.md
```

Key local facts:

- Current Flowbridge-claude phase is Lane B: Webflow export ZIP/pretreated HTML to Webflow clipboard XscpData.
- Minimal converter currently does not own native IX2/IX3 end-to-end conversion in the current contract.
- Old/proven modules exist in earlier converter work and can be pulled only when needed and understood.
- `payload.assets[]` must stay empty for native clipboard paste, because populated assets can crash the Webflow clipboard path.
- Image upload/relink can be handled outside `payload.assets[]` through a manifest/map.
- Pre-treatment skill is Claude prompt/workflow, not a TypeScript module.

### 2.2 Current Flow-Goodies App Reference

Reference app path:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

Important files:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\AGENTS.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\CLAUDE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\package.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\webflow.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\components\ImportPanel.tsx
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\utils\smartPaste.ts
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\utils\uploadAssets.ts
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\utils\bridgeReadiness.ts
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\docs\integration\flowbridge-flowgoodies-contract.md
```

Useful reference behavior:

- Uses Webflow Designer Extension API.
- Can get current site/page context.
- Has clipboard-paste helpers.
- Has page ID patching helpers.
- Has IX3 page ID patching helpers.
- Has image asset mapping concepts.
- Has font scan/reconnect helpers.
- Has readiness logic deciding whether a payload can be imported programmatically or must use clipboard paste.
- Has CMS static fill helpers.

Known drift/risk:

- Current contract mentions asset fallback upload paths that may not be wired into the current ImportPanel.
- Current app is multi-tool Flow-Goodies, not focused marketplace install UX.
- New extension should borrow proven ideas, not modify the old UX into a more complicated shape.

### 2.3 Old Converter / Worker Reference

Reference repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean
```

Important credential/config files:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\wrangler.toml
```

Important worker config facts:

```text
Cloudflare Worker name: flowbridge-assets
Worker main: workers/asset-proxy.js
Required Worker secrets: B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET, UPLOAD_API_KEY
```

Important rule:

Do not print, copy, commit, or paste secret values into docs, plans, prompts, chat, test logs, or markdown artifacts. Future agents should retrieve values from local ignored env files or provider dashboards only when actually executing deployment/backend work.

### 2.4 Official Webflow Capability References

Use current official Webflow docs before implementation. These were relevant as of this plan:

- Hybrid Apps overview: https://developers.webflow.com/apps/data/docs/hybrid-apps
- Designer `getSiteInfo()`: https://developers.webflow.com/designer/reference/get-site-info
- Designer `getCurrentPage()`: https://developers.webflow.com/designer/reference/get-current-page
- Data API asset upload/create asset: https://developers.webflow.com/data/reference/assets/assets/create
- Data API custom code registration: https://developers.webflow.com/data/reference/custom-code/custom-code/register-inline
- Data API custom code application/upsert: https://developers.webflow.com/data/reference/custom-code/custom-code-sites/upsert-custom-code

Agents must re-check official docs when implementing because app scopes and Designer/Data API capabilities change.

---

## 3. Core Architecture Decision

### 3.1 Recommended Split

Use four layers:

```text
1. Generation layer
   Pre-treatment skill + converter/package generator.

2. Package layer
   Immutable install package: XscpData + manifests + assets + CMS data + font requirements.

3. Marketplace/backend layer
   Purchase code redemption, package authorization, package retrieval, signed URLs, storage credentials.

4. Webflow installer extension layer
   Runs inside buyer's Webflow project and performs target-aware install.
```

### 3.2 What The Skill Should Own

The skill may own:

- visual source cleanup
- class/style normalization before converter
- asset inventory
- font inventory
- interaction classification
- CMS inventory
- metadata summaries
- warnings and unsupported-feature classification
- verifying that generated package matches source visually and structurally

The skill should not be trusted as the final writer of complex XscpData/IX3 JSON.

### 3.3 What The Converter / Package Generator Should Own

The deterministic generator should own:

- final XscpData shape
- Webflow node/style structure
- IX3 preservation from native IX3 where available
- IX2-to-IX3 conversion when revived from old modules
- asset references as portable manifest entries
- CMS manifest/data export
- font manifest
- runtime/custom-code manifest
- checksums and package schema version

### 3.4 What The New Extension Should Own

The new extension should own:

- purchase/install code entry
- package fetch
- Webflow site/page detection
- font preflight and manual install guidance
- target-site asset upload
- XscpData patching with real target asset IDs
- current page ID patching
- clipboard paste/import handoff
- CMS import or guided CMS mapping
- custom code/runtime setup when supported
- post-install verification

### 3.5 Why This Is Better Than Converter Uploads

The converter lives outside the buyer's target Webflow context. To upload assets/CMS from a web page, it would need the user to provide sensitive token/site details. That is more friction and worse trust.

The extension lives in the target Webflow project. It can make the experience feel native:

```text
"Enter code" -> "Install fonts if needed" -> "Prepare assets" -> "Paste/install"
```

This is the lowest-friction user path that still respects Webflow's constraints.

---

## 4. New Extension Scope

### 4.1 Name

Working name:

```text
Master Collection
```

Repository working name:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

Do not reuse the old `Flow-Goodies` app name unless Maria explicitly decides this becomes the production successor.

### 4.2 First Release Scope

The first credible release should install one purchased template/component package into the current Webflow page/site with:

- code redemption/fetch
- package manifest parsing
- current site/page detection
- missing-font checklist
- image upload to current Webflow site
- XscpData image ID/src patching
- page ID patching
- clipboard paste path
- post-paste checklist
- basic CMS data import plan or guided step, depending on confirmed Webflow capabilities

### 4.3 Explicit Non-Goals For First Release

Do not build these in the first implementation unless separately approved:

- full marketplace storefront UI
- seller dashboard
- payments
- license management beyond basic code validation
- fully automated CMS collection schema creation if Webflow API capabilities are not confirmed
- automated font installation if Webflow does not support it
- arbitrary HTML import tool UX
- broad Flow-Goodies utility tabs
- modifying the current Flow-Goodies app
- changing the current converter contract before package schema is agreed

---

## 5. Package Contract

### 5.1 Package File Concept

The package should be a portable install unit. It should not assume target site ID, target page ID, or target Webflow asset IDs.

Possible package root object:

```ts
export interface MasterCollectionPackage {
  schemaVersion: "master-collection-package@1";
  packageId: string;
  productId: string;
  productSlug: string;
  packageVersion: string;
  createdAt: string;
  source: PackageSourceInfo;
  install: InstallInstructions;
  xscp: XscpPackagePayload;
  assets: AssetManifestEntry[];
  fonts: FontManifestEntry[];
  cms: CmsManifest | null;
  interactions: InteractionManifest;
  customCode: CustomCodeManifest | null;
  verification: PackageVerificationSummary;
}
```

### 5.2 `source`

Track where the package came from.

```ts
export interface PackageSourceInfo {
  sourceKind: "webflow-export" | "component-capture" | "manual-package" | "unknown";
  sourceSiteName?: string;
  sourcePageName?: string;
  sourceExportHash?: string;
  sourceBuildTool?: "Flowbridge-claude" | "Flowbridge-rebuild-clean" | string;
  sourceBuildVersion?: string;
}
```

### 5.3 `install`

Tell the extension how to install.

```ts
export interface InstallInstructions {
  installKind: "page" | "section" | "component" | "symbol" | "mixed";
  preferredLane: "clipboard-xscp" | "designer-api-direct" | "hybrid";
  requiresCurrentPage: boolean;
  requiresAssetUpload: boolean;
  requiresCms: boolean;
  requiresFonts: boolean;
  requiresCustomCode: boolean;
  requiresInteractions: boolean;
  minimumWebflowApiVersion?: string;
}
```

### 5.4 `xscp`

Keep the actual clipboard payload portable.

```ts
export interface XscpPackagePayload {
  payload: unknown;
  payloadEncoding: "json";
  payloadHash: string;
  containsIx2: boolean;
  containsIx3: boolean;
  containsPageScopedInteractions: boolean;
  containsEmbeds: boolean;
  placeholderPageIds: string[];
  placeholderAssetIds: string[];
}
```

Rules:

- `payload.assets[]` must remain empty for clipboard paste packages.
- Assets belong in `assets[]` manifest, not `payload.assets[]`.
- Package may include placeholder image IDs, source URLs, or stable asset keys.
- Extension patches placeholders after upload.

### 5.5 `assets`

Manifest must be rich enough for upload, dedupe, patching, and verification.

```ts
export interface AssetManifestEntry {
  assetKey: string;
  kind: "image" | "video" | "lottie" | "document" | "font" | "other";
  role: "inline-img" | "background-image" | "css-url" | "embed" | "cms-field" | "runtime";
  fileName: string;
  originalUrl?: string;
  packageUrl: string;
  mimeType?: string;
  byteSize?: number;
  width?: number;
  height?: number;
  hash?: string;
  patchTargets: AssetPatchTarget[];
  uploadPolicy: "required" | "optional" | "external-ok" | "manual";
}
```

Patch target examples:

```ts
export interface AssetPatchTarget {
  targetKind:
    | "xscp-node-attr-src"
    | "xscp-node-img-id"
    | "xscp-style-background-image"
    | "xscp-ix3-media"
    | "cms-item-field"
    | "custom-code";
  selector?: string;
  nodeId?: string;
  styleId?: string;
  fieldSlug?: string;
  path?: string[];
}
```

### 5.6 `fonts`

Font requirements are first-class because Webflow font installation can be manual.

```ts
export interface FontManifestEntry {
  family: string;
  source: "google" | "adobe" | "custom" | "websafe" | "unknown";
  weights: number[];
  styles: Array<"normal" | "italic" | string>;
  required: boolean;
  usedBy: FontUsageEntry[];
  installHint?: string;
  fallbackFamily?: string;
}
```

The extension should detect missing fonts and show:

- exact family name
- weights/styles needed
- where it is used
- whether install is required or optional
- instructions to install it manually in Webflow
- rescan button

The extension should not silently continue when a required custom font is missing unless Maria explicitly chooses a soft-warning policy.

### 5.7 `cms`

CMS must be explicit and staged. It is a major confusion point.

```ts
export interface CmsManifest {
  schemaVersion: "flow-party-cms@1";
  collections: CmsCollectionManifest[];
  items: CmsItemManifest[];
  bindingStrategy: "auto-create" | "map-existing" | "static-fill" | "manual";
  requiresDataApi: boolean;
}
```

Collection manifest:

```ts
export interface CmsCollectionManifest {
  sourceCollectionId?: string;
  collectionKey: string;
  displayName: string;
  slug: string;
  fields: CmsFieldManifest[];
  expectedItemCount: number;
}
```

Field manifest:

```ts
export interface CmsFieldManifest {
  fieldKey: string;
  displayName: string;
  slug: string;
  type: string;
  required: boolean;
  relation?: {
    targetCollectionKey: string;
    relationKind: "single" | "multi";
  };
}
```

Important constraint:

Do not assume CMS bindings survive cross-site paste. Previous research found that Webflow strips or breaks some hard CMS bindings across sites. The safe path is to import data and guide mapping/rebinding, or convert certain content to static values when that is the correct product behavior.

### 5.8 `interactions`

Interactions need a manifest even if the XscpData already contains IX3.

```ts
export interface InteractionManifest {
  sourceFormat: "ix3" | "ix2-converted-to-ix3" | "ix2-preserved" | "custom-code" | "mixed" | "none";
  nativeWebflowSupported: boolean;
  pageScoped: boolean;
  requiresPageIdPatch: boolean;
  unsupportedBehaviors: UnsupportedInteractionEntry[];
}
```

Unsupported native cases may include:

- mouse move effects that are not representable in Webflow native IX3
- counters
- GSAP Flip
- pinning/ScrollTrigger behavior
- dynamic runtime values
- Lottie sync if not natively representable
- callbacks
- infinite marquee if no native equivalent

The package should tell the extension whether custom runtime code is required.

### 5.9 `customCode`

Custom code must be explicit, rare, and separately approved by package rules.

```ts
export interface CustomCodeManifest {
  required: boolean;
  scripts: CustomCodeScriptEntry[];
  installPolicy: "auto-if-scope-available" | "manual-copy" | "blocked";
}
```

Rules:

- Native IX2/IX3 should be preferred wherever possible.
- Custom code is acceptable only for verified native-impossible exceptions.
- Extension must tell the user what will be added and why.
- Auto custom-code insertion depends on current Webflow API/app scopes.

---

## 6. Backend And Credential Plan

### 6.1 Credential Policy

Agents must never paste secret values into:

- chat
- markdown plans
- repo docs
- committed files
- screenshots
- logs attached to docs
- prompt artifacts

Agents may name variable names and local file paths.

Agents may read `.env.example` files freely.

Agents may read `.env` or `.env.local` only when execution requires it, and they must not echo values.

### 6.2 Existing Credential Sources

Old converter local example:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.example
```

Old converter local ignored values:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
```

Old worker config:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\wrangler.toml
```

Known variable names from `.env.example`:

```text
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
B2_ENDPOINT
CDN_BASE_URL
UPLOAD_API_KEY
WF_API_TOKEN
```

Known Cloudflare Worker:

```text
flowbridge-assets
```

Known Worker secret names:

```text
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
UPLOAD_API_KEY
```

### 6.3 Recommended New Backend Env Layout

If creating a new package backend repo, use:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker
```

Create:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker\wrangler.toml
```

Do not commit `.env.local`.

Suggested variable names:

```text
FLOW_PARTY_PACKAGE_BUCKET
FLOW_PARTY_PACKAGE_BASE_URL
FLOW_PARTY_UPLOAD_API_KEY
FLOW_PARTY_SIGNING_SECRET
FLOW_PARTY_LICENSE_SECRET
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
B2_ENDPOINT
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
WEBFLOW_CLIENT_ID
WEBFLOW_CLIENT_SECRET
WEBFLOW_REDIRECT_URI
```

Use clearer `FLOW_PARTY_*` names for new work, but document any temporary mapping to the old `flowbridge-assets` Worker.

### 6.4 New Extension Env Layout

New extension repo should have:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\webflow.json
```

Suggested extension variables:

```text
VITE_MASTER_COLLECTION_API_BASE_URL
VITE_MASTER_COLLECTION_PACKAGE_BASE_URL
VITE_MASTER_COLLECTION_ENV
VITE_MASTER_COLLECTION_DEBUG
```

If using Webpack instead of Vite, use equivalent `process.env` or define-plugin naming. Do not decide bundler only because of variable names.

### 6.5 Credential Retrieval Instructions For Future Agents

When an agent executes backend or extension setup:

1. Read this plan.
2. Read the new repo `AGENTS.md` if it exists.
3. Inspect `.env.example` files first.
4. Inspect local ignored `.env.local` files only if actual command execution needs values.
5. For existing B2/Worker credentials, check:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
```

6. For Cloudflare Worker secrets, use provider dashboard or Wrangler secret tooling for the Worker named:

```text
flowbridge-assets
```

7. For Webflow extension client ID, inspect the relevant `webflow.json`.
8. For Webflow OAuth/Data API credentials, retrieve from the Webflow Developer/App dashboard, not from chat.
9. If credentials are missing, stop and ask Maria for access or approval to create new credentials.

### 6.6 Backend API Shape

Minimum backend endpoints:

```http
POST /api/install-codes/resolve
GET  /api/packages/{packageId}/manifest
GET  /api/packages/{packageId}/package
GET  /api/packages/{packageId}/assets/{assetKey}
POST /api/install-events
```

`POST /api/install-codes/resolve` request:

```json
{
  "code": "BUYER-INSTALL-CODE",
  "webflowSiteId": "optional-current-site-id",
  "webflowPageId": "optional-current-page-id",
  "extensionVersion": "0.1.0"
}
```

Response:

```json
{
  "ok": true,
  "packageId": "pkg_...",
  "productName": "Template Name",
  "packageVersion": "1.0.0",
  "manifestUrl": "https://...",
  "expiresAt": "2026-04-19T12:00:00Z"
}
```

`GET /api/packages/{packageId}/package` returns the full `MasterCollectionPackage`, or a signed URL to it.

Asset URLs should be short-lived or access-controlled if products are paid.

### 6.7 Backend Storage Shape

Recommended storage key layout:

```text
packages/
  {packageId}/
    manifest.json
    package.json
    xscp.json
    assets/
      {assetKey}-{filename}
    cms/
      collections.json
      items.json
    verification/
      source-screenshot.png
      package-report.json
```

Avoid a flat bucket where filenames collide.

### 6.8 Marketplace Relationship

The marketplace does not need the buyer's Webflow token/site ID for installation.

Marketplace should own:

- purchase
- product metadata
- package listing
- install code issuance
- account/library history

Extension should own:

- current target Webflow site/page
- asset upload
- page ID patch
- install

Backend bridges the two:

- validate code
- serve package
- track install events
- keep package assets private enough for paid products

---

## 7. Extension UX Plan

### 7.1 Main States

The extension should be a focused installer with these states:

```text
1. Welcome / Code Entry
2. Package Loading
3. Site Context Check
4. Preflight Checklist
5. Font Preparation
6. Asset Upload
7. CMS Preparation
8. Install/Paste
9. Post-Install Verification
10. Done / Follow-Up
```

Do not add unrelated Flow-Goodies utility tabs.

### 7.2 Welcome / Code Entry

User-facing behavior:

- Ask for install code.
- Explain that installation happens inside the current Webflow project.
- Do not ask for Webflow token unless the selected architecture absolutely requires a temporary fallback.
- Offer "Paste code" input and "Continue".

Technical behavior:

- Validate non-empty code.
- Call backend resolve endpoint.
- Store minimal session state.
- Do not permanently store install code unless license UX needs it.

### 7.3 Package Loading

Behavior:

- Fetch manifest.
- Fetch package.
- Validate schema version.
- Validate package hash if present.
- Show clear error if code is invalid, expired, or package cannot be fetched.

Implementation:

- Use strict TypeScript validators or a runtime schema library.
- Keep package parse errors human-readable.
- Log technical details behind debug flag only.

### 7.4 Site Context Check

Behavior:

- Detect current Webflow site ID.
- Detect current page ID.
- Show target site/page before install.
- Warn if no page is selected/open.

Implementation:

- Use `webflow.getSiteInfo()`.
- Use `webflow.getCurrentPage()`.
- Store:

```ts
interface TargetWebflowContext {
  siteId: string;
  siteName?: string;
  pageId: string;
  pageName?: string;
}
```

### 7.5 Preflight Checklist

Show a preparation checklist before any irreversible or noisy operation.

Checklist rows:

- Target Webflow site
- Target Webflow page
- Package version
- Required fonts
- Missing fonts
- Assets to upload
- CMS data
- Interactions
- Custom code
- Paste lane

Each row should have:

- status: ready / needs action / warning / blocked
- short explanation
- action button if applicable

### 7.6 Font Preparation UX

This is a key product win.

Behavior:

- Extension scans fonts currently available in site/project if the API supports it.
- Extension compares available fonts against package `fonts[]`.
- Missing required fonts block install until user confirms or rescans clean.
- Missing optional fonts warn but do not block.
- For custom fonts, tell user manual install is required.
- For Google fonts, tell user exact family/weights/styles.

Suggested user-facing copy style:

```text
Install these fonts before importing:
Inter — 400, 500, 700
Editorial New — 400, italic

After installing them in Webflow, return here and click Rescan fonts.
```

Do not over-explain the technology.

Technical implementation:

- Reuse ideas from current Flow-Goodies font scanning helpers.
- Define a stable `FontPreflightResult`.
- Keep comparison case-insensitive for family names.
- Preserve exact display names from package for UX.
- Provide an override only if Maria approves it.

### 7.7 Asset Upload UX

Behavior:

- Show number and size of assets.
- Upload into the buyer's current Webflow site.
- Show progress.
- Dedupe where safe.
- Patch package XscpData only after upload succeeds.
- Retry failed assets.
- Let user continue only when required assets are uploaded or explicitly marked external/manual.

Technical requirements:

- Prefer Webflow Designer Extension asset creation if available and suitable.
- If Hybrid/Data API asset upload is needed, use the backend/OAuth path.
- Never use `payload.assets[]` for clipboard paste packages.
- Store uploaded mapping:

```ts
interface UploadedAssetMapEntry {
  assetKey: string;
  webflowAssetId: string;
  hostedUrl?: string;
  originalPackageUrl: string;
  fileName: string;
}
```

Patch targets:

- inline image `src`
- inline image `data.img.id`
- background image CSS URLs
- style background refs
- CMS image fields
- custom code URLs if package policy allows

### 7.8 CMS Preparation UX

CMS should be a separate step, but not a confusing separate product.

Behavior:

- If package has no CMS, mark CMS as "Not needed".
- If package has CMS, show collection names and item counts.
- Decide whether the current app can:
  - create collections
  - map to existing collections
  - import items
  - only guide the user
- Present the least confusing path.

Possible modes:

```text
Auto import:
  Extension/backend can create/populate CMS safely.

Map existing:
  User maps package collections/fields to existing site CMS.

Static fill:
  CMS content becomes static content inside the installed section/page.

Manual:
  Extension gives a checklist/export file.
```

First release recommendation:

- Implement manifest parsing and UX.
- Implement static/no-CMS path first.
- Implement CMS item import only after API capability and scopes are verified.
- Do not promise full automated cross-site CMS binding until proven in Webflow.

### 7.9 Install / Paste UX

Most full-fidelity packages should use clipboard XscpData paste.

Behavior:

- Prepare final patched XscpData.
- Copy using the proven Webflow clipboard approach.
- Tell user where to paste.
- Keep one final action:

```text
Copy and paste into Webflow
```

or, if direct API insertion is safe:

```text
Install on current page
```

Rules:

- If payload contains IX3, IX2, embeds, CMS manifests, or custom code, prefer clipboard path unless proven direct Designer API insertion supports it.
- Use direct programmatic import only for safe payloads.
- Keep the user flow simple even if implementation has lanes.

### 7.10 Post-Install Verification UX

After paste/install:

- Confirm whether assets were uploaded.
- Confirm final XscpData was copied.
- Offer post-paste checks:
  - missing images
  - fonts still missing
  - CMS follow-up
  - custom code follow-up
  - interactions warning if applicable

If APIs allow inspecting selected/current elements after paste, add lightweight verification. If not, use a guided checklist.

---

## 8. Extension Technical Plan

### 8.1 Scaffold Decision

Start from the current Flow-Goodies extension only as a reference, not by editing it.

Options:

1. Copy minimal scaffold from Flow-Goodies:
   - faster
   - already known to work with Webflow extension build
   - may carry old app complexity if not pruned

2. Create clean scaffold:
   - cleaner architecture
   - requires verifying Webflow extension setup from scratch

Recommendation:

Use a clean scaffold but copy only necessary build patterns from Flow-Goodies if Webflow extension setup is finicky.

### 8.2 Proposed File Structure

```text
app/
  AGENTS.md
  CLAUDE.md
  README.md
  package.json
  tsconfig.json
  webpack.config.js or vite.config.ts
  webflow.json
  .env.example
  .gitignore
  public/
  src/
    index.tsx
    app/
      App.tsx
      appState.ts
      routes.ts
    components/
      Button.tsx
      Checklist.tsx
      ProgressBar.tsx
      Notice.tsx
    features/
      package/
        packageTypes.ts
        packageSchema.ts
        packageClient.ts
        packageStore.ts
      install/
        installMachine.ts
        installSteps.ts
        installSession.ts
      webflow/
        currentContext.ts
        designerApi.ts
        dataApi.ts
      fonts/
        fontTypes.ts
        fontScanner.ts
        fontDiff.ts
        FontPreflightPanel.tsx
      assets/
        assetTypes.ts
        assetFetcher.ts
        assetUploader.ts
        assetPatcher.ts
        AssetUploadPanel.tsx
      cms/
        cmsTypes.ts
        cmsPlanner.ts
        cmsInstaller.ts
        CmsPreparationPanel.tsx
      paste/
        xscpPatcher.ts
        clipboard.ts
        pasteLane.ts
      verification/
        installVerifier.ts
        verificationTypes.ts
      telemetry/
        installEvents.ts
      errors/
        userErrors.ts
        technicalErrors.ts
    styles/
      app.css
  tests/
    packageSchema.test.ts
    fontDiff.test.ts
    assetPatcher.test.ts
    xscpPatcher.test.ts
    installMachine.test.ts
```

### 8.3 App State

Use an explicit state machine or reducer. Avoid scattered booleans.

```ts
type InstallStep =
  | "code-entry"
  | "loading-package"
  | "site-context"
  | "preflight"
  | "fonts"
  | "assets"
  | "cms"
  | "install"
  | "verification"
  | "done"
  | "error";
```

Core session:

```ts
interface InstallSession {
  code?: string;
  package?: MasterCollectionPackage;
  target?: TargetWebflowContext;
  fontResult?: FontPreflightResult;
  assetResult?: AssetInstallResult;
  cmsPlan?: CmsInstallPlan;
  patchedPayload?: unknown;
  errors: InstallUserError[];
}
```

### 8.4 Package Client

Responsibilities:

- resolve install code
- fetch manifest
- fetch package
- validate schema
- fetch package asset bytes/URLs
- report install events

Do not bake local development URLs into components. Use config module.

### 8.5 Webflow Adapter

Create a thin adapter around Webflow globals so tests can mock it.

```ts
interface WebflowDesignerAdapter {
  getSiteInfo(): Promise<{ siteId: string; siteName?: string }>;
  getCurrentPage(): Promise<{ id: string; name?: string }>;
  createAsset?(file: File): Promise<{ id: string; url?: string }>;
}
```

If using Data API/OAuth:

```ts
interface WebflowDataAdapter {
  uploadAsset(siteId: string, file: File): Promise<WebflowAssetResult>;
  listCollections(siteId: string): Promise<WebflowCollection[]>;
  createCollection?(siteId: string, input: CmsCollectionInput): Promise<WebflowCollection>;
  createCollectionItem?(collectionId: string, input: CmsItemInput): Promise<WebflowCmsItem>;
}
```

Keep Designer and Data adapters separate.

### 8.6 Font Scanner

Responsibilities:

- retrieve available fonts through Webflow API if available
- fallback to variable/font helper patterns from Flow-Goodies if needed
- compare with package manifest
- return actionable missing list

```ts
interface FontPreflightResult {
  availableFamilies: string[];
  required: FontRequirementStatus[];
  optional: FontRequirementStatus[];
  missingRequired: FontManifestEntry[];
  missingOptional: FontManifestEntry[];
  canContinue: boolean;
}
```

### 8.7 Asset Installer

Responsibilities:

- read `assets[]`
- fetch asset bytes from package URLs
- convert to `File`
- upload to Webflow site
- collect Webflow IDs/URLs
- retry failed uploads
- patch XscpData

Pseudo-flow:

```ts
async function installAssets(pkg, webflow, onProgress) {
  const requiredAssets = pkg.assets.filter(asset => asset.uploadPolicy === "required");
  const uploaded = [];

  for (const asset of requiredAssets) {
    const file = await fetchPackageAssetAsFile(asset);
    const result = await webflow.createAsset(file);
    uploaded.push(mapUploadResult(asset, result));
    onProgress(uploaded.length, requiredAssets.length);
  }

  return buildAssetInstallResult(uploaded);
}
```

### 8.8 Xscp Patcher

Responsibilities:

- clone package XscpData safely
- patch current page IDs
- patch IX3 page-scoped IDs
- patch image asset IDs
- patch image URLs
- patch background URLs
- preserve existing Webflow-compatible structure
- keep `payload.assets[]` empty for clipboard lane

Potential helper signatures:

```ts
function patchXscpForTarget(
  payload: unknown,
  target: TargetWebflowContext,
  assets: AssetInstallResult,
): unknown;

function assertClipboardSafePayload(payload: unknown): ClipboardPayloadReport;
```

### 8.9 Clipboard Helper

Use the proven Webflow clipboard copy path from Flow-Goodies as reference.

Important:

- `navigator.clipboard.writeText()` may not behave like Webflow's expected paste event.
- Existing helper uses `document.execCommand("copy")` with a copy event.
- Re-test inside Webflow Designer.

### 8.10 CMS Installer

First version should be conservative.

Responsibilities:

- parse package CMS manifest
- show plan
- determine supported install mode
- if no CMS, skip
- if static fill, patch static content before paste
- if Data API can import items, import items with progress
- if collection binding cannot be guaranteed, guide mapping

Do not hide CMS complexity behind a false "done" state.

### 8.11 Error Model

Use user-facing errors that explain next action.

Examples:

```ts
type InstallUserErrorCode =
  | "INVALID_CODE"
  | "PACKAGE_FETCH_FAILED"
  | "UNSUPPORTED_PACKAGE_VERSION"
  | "NO_CURRENT_PAGE"
  | "MISSING_REQUIRED_FONTS"
  | "ASSET_UPLOAD_FAILED"
  | "CMS_REQUIRES_MANUAL_MAPPING"
  | "CLIPBOARD_COPY_FAILED"
  | "WEBFLOW_API_SCOPE_MISSING";
```

Each error should have:

- short title
- plain explanation
- next action
- technical details hidden behind debug mode

---

## 9. Backend Technical Plan

### 9.1 Decide Reuse vs New Worker

Options:

1. Reuse `flowbridge-assets`
   - faster
   - existing B2 secrets already configured
   - risk: name and endpoint are converter/playground oriented

2. Create new `master-collection-packages` Worker
   - cleaner product boundary
   - separate auth, logs, storage prefixes
   - requires provisioning

Recommendation:

Create a new Worker for package delivery when moving beyond prototype. Reuse old worker only as a temporary proof of concept.

### 9.2 Worker Responsibilities

- validate install code
- return package manifest
- return package file or signed package URL
- return asset files or signed asset URLs
- record install events
- enforce package access
- optionally proxy Webflow Data API if OAuth/Hybrid App architecture requires backend participation

### 9.3 Worker Non-Responsibilities

- do not convert Webflow export ZIPs
- do not patch target page IDs
- do not upload directly into user's Webflow site unless using an OAuth-backed Webflow Data API route
- do not store user Webflow tokens in logs

### 9.4 Install Code Data Model

Minimum:

```ts
interface InstallCodeRecord {
  codeHash: string;
  productId: string;
  packageId: string;
  buyerId?: string;
  status: "active" | "used" | "revoked" | "expired";
  maxInstalls?: number;
  installCount: number;
  createdAt: string;
  expiresAt?: string;
}
```

For prototype, records can be static JSON or a simple KV store. For production, use a real database.

### 9.5 Package Manifest Data Model

Minimum:

```ts
interface PackageRecord {
  packageId: string;
  productId: string;
  version: string;
  storageKey: string;
  manifestKey: string;
  status: "draft" | "active" | "archived";
  createdAt: string;
}
```

### 9.6 Install Event Data Model

```ts
interface InstallEvent {
  packageId: string;
  productId: string;
  eventType:
    | "code_resolved"
    | "preflight_started"
    | "fonts_missing"
    | "assets_uploaded"
    | "cms_started"
    | "payload_copied"
    | "install_completed"
    | "install_failed";
  webflowSiteId?: string;
  webflowPageId?: string;
  extensionVersion: string;
  createdAt: string;
  errorCode?: string;
}
```

Do not send package source code, secret tokens, or full user site content as telemetry.

---

## 10. Converter / Package Generator Plan

### 10.1 Relationship To Flowbridge-claude

Flowbridge-claude should eventually output package-ready artifacts, but not as the first blocker for the extension scaffold.

Current root:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude
```

Future outputs:

```text
dist/packages/{packageId}/package.json
dist/packages/{packageId}/xscp.json
dist/packages/{packageId}/assets/*
dist/packages/{packageId}/cms/*
dist/packages/{packageId}/verification/*
```

### 10.2 Minimal Package Generator Work

Add or plan a packaging command later:

```text
bun run build:package
```

This command should:

1. run/accept pretreated source
2. produce XscpData
3. extract asset manifest
4. extract font manifest
5. extract CMS manifest if any
6. classify interactions
7. write package JSON
8. write checksums
9. validate schema

### 10.3 IX2/IX3 Future Work

Do not ask the skill to hand-write final IX3 JSON.

Recommended future flow:

```text
native IX3 in source -> preserve/extract deterministically
IX2 without IX3 -> convert through deterministic ix2-to-ix3 module
native-impossible behavior -> manifest + custom code exception
```

The old converter has relevant modules in:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\src\lib
```

Flowbridge-claude has docs pointing to these modules. Pull only what is needed and verify with fixtures/paste tests.

### 10.4 Package Validation

Package generator must fail if:

- package schema is invalid
- required asset file is missing
- required font family has no manifest entry
- package XscpData cannot be parsed
- package expects target page ID but has no placeholder markers or patchable IX entries
- `payload.assets[]` is non-empty for clipboard lane

---

## 11. Implementation Phases

## Phase 0 — Refresh Evidence And Confirm Naming

Goal: start from current truth.

Tasks:

- [ ] Read `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md`.
- [ ] Read `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\CLAUDE.md`.
- [ ] Read this plan.
- [ ] Read `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\AGENTS.md`.
- [ ] Read `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\CLAUDE.md`.
- [ ] Inspect current Webflow docs for Designer API and Hybrid/Data API changes.
- [ ] Confirm final new repo name with Maria only if naming matters before scaffold.
- [ ] Confirm whether prototype should reuse `flowbridge-assets` or create a new package worker.

Verification:

- [ ] Produce a short evidence note listing current API capabilities and any docs changes.

## Phase 1 — Create New Extension Skeleton

Goal: new app opens in Webflow and shows a code-entry screen.

Files to create:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\AGENTS.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\CLAUDE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\README.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\package.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\tsconfig.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\webflow.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\.gitignore
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\src\index.tsx
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app\src\app\App.tsx
```

Tasks:

- [ ] Create repo directory.
- [ ] Add local instructions explaining this is a new installer, not old Flow-Goodies.
- [ ] Add package scripts: `dev`, `build`, `test`, `lint`.
- [ ] Add minimal React app.
- [ ] Add minimal Webflow extension config.
- [ ] Add `.env.example` with non-secret variable names.
- [ ] Add `.gitignore` that excludes `.env`, `.env.local`, build output, and node modules.
- [ ] Run install.
- [ ] Run build.
- [ ] Load extension in Webflow dev flow.

Verification:

- [ ] `npm run build` passes.
- [ ] Extension opens in Webflow.
- [ ] Code-entry screen renders.

## Phase 2 — Package Schema And Mock Package

Goal: extension can parse a local/mock package before backend exists.

Files:

```text
src\features\package\packageTypes.ts
src\features\package\packageSchema.ts
src\features\package\packageClient.ts
src\features\package\__fixtures__\mockPackage.ts
tests\packageSchema.test.ts
```

Tasks:

- [ ] Define `MasterCollectionPackage`.
- [ ] Define asset/font/CMS/interactions/custom code manifest types.
- [ ] Add runtime validation.
- [ ] Add a local mock package fixture.
- [ ] Add package parse test.
- [ ] Add invalid schema test.
- [ ] Add package hash/checksum placeholder if not implementing full checksum yet.

Verification:

- [ ] Tests pass for valid mock package.
- [ ] Tests reject invalid package.
- [ ] UI can display mock package name/version from code-entry flow.

## Phase 3 — Current Webflow Context Adapter

Goal: extension knows where it is installing.

Files:

```text
src\features\webflow\designerApi.ts
src\features\webflow\currentContext.ts
tests\currentContext.test.ts
```

Tasks:

- [ ] Wrap `webflow.getSiteInfo()`.
- [ ] Wrap `webflow.getCurrentPage()`.
- [ ] Normalize target context.
- [ ] Handle missing page.
- [ ] Handle API errors.
- [ ] Show site/page in UI.

Verification:

- [ ] Mock tests pass.
- [ ] Manual Webflow test shows correct site ID/name.
- [ ] Manual Webflow test shows correct current page ID/name.

## Phase 4 — Preflight Checklist

Goal: user sees exactly what will happen before assets/CMS/paste.

Files:

```text
src\features\install\installMachine.ts
src\features\install\installSteps.ts
src\components\Checklist.tsx
src\features\install\PreflightPanel.tsx
```

Tasks:

- [ ] Implement install step model.
- [ ] Build checklist statuses from package + target.
- [ ] Show required fonts count.
- [ ] Show missing fonts placeholder until scanner exists.
- [ ] Show assets count.
- [ ] Show CMS count.
- [ ] Show interactions status.
- [ ] Show custom-code status.

Verification:

- [ ] UI shows correct mock package checklist.
- [ ] Unit test checklist builder for no-assets/no-CMS package.
- [ ] Unit test checklist builder for assets/CMS/fonts package.

## Phase 5 — Font Preflight

Goal: extension tells user which fonts must be installed manually before receiving template.

Files:

```text
src\features\fonts\fontTypes.ts
src\features\fonts\fontScanner.ts
src\features\fonts\fontDiff.ts
src\features\fonts\FontPreflightPanel.tsx
tests\fontDiff.test.ts
```

Tasks:

- [ ] Inspect current Flow-Goodies font helpers.
- [ ] Decide scanner strategy using current Webflow API.
- [ ] Implement `diffFonts(packageFonts, availableFonts)`.
- [ ] Implement missing required/optional logic.
- [ ] Implement UI panel listing exact missing families/weights/styles.
- [ ] Add "Rescan fonts" action.
- [ ] Add "Continue with warning" only if Maria approves soft policy.

Verification:

- [ ] Unit tests for exact match.
- [ ] Unit tests for case-insensitive family match.
- [ ] Unit tests for missing weight/style.
- [ ] Manual Webflow test with one missing font.
- [ ] Manual Webflow test after installing font and rescanning.

## Phase 6 — Asset Fetch, Upload, And Patch

Goal: package images upload into the buyer's current Webflow site, then XscpData is patched.

Files:

```text
src\features\assets\assetTypes.ts
src\features\assets\assetFetcher.ts
src\features\assets\assetUploader.ts
src\features\assets\assetPatcher.ts
src\features\assets\AssetUploadPanel.tsx
tests\assetPatcher.test.ts
```

Tasks:

- [ ] Define `AssetInstallResult`.
- [ ] Fetch asset from package URL.
- [ ] Convert response to `File`.
- [ ] Upload using Designer API or confirmed Data API path.
- [ ] Capture Webflow asset ID and hosted URL.
- [ ] Add upload progress.
- [ ] Add retry for failed asset.
- [ ] Patch inline image `src`.
- [ ] Patch inline image IDs.
- [ ] Patch background image URLs.
- [ ] Preserve `payload.assets[] = []` for clipboard lane.
- [ ] Fail clearly if a required asset cannot be uploaded.

Verification:

- [ ] Unit test patching inline image.
- [ ] Unit test patching background image.
- [ ] Unit test that `payload.assets[]` remains empty.
- [ ] Manual Webflow test uploads at least one image.
- [ ] Manual paste test shows image from buyer's Webflow assets.

## Phase 7 — Page ID And IX3 Patch

Goal: interactions/page-scoped data point to the current target page.

Files:

```text
src\features\paste\xscpPatcher.ts
tests\xscpPatcher.test.ts
```

Tasks:

- [ ] Inspect current Flow-Goodies `patchPageStartIds`.
- [ ] Inspect current Flow-Goodies `patchIX3PageIds`.
- [ ] Port only necessary logic.
- [ ] Add tests for page start/page-scoped IX data.
- [ ] Ensure XscpData clone does not mutate original package.
- [ ] Ensure unsupported/unknown IX data is preserved.

Verification:

- [ ] Unit tests pass.
- [ ] Fixture package with IX3 patches to current page ID.
- [ ] Clipboard paste still succeeds.

## Phase 8 — Clipboard Install Lane

Goal: one reliable paste action for full-fidelity packages.

Files:

```text
src\features\paste\clipboard.ts
src\features\paste\pasteLane.ts
src\features\install\InstallPanel.tsx
tests\pasteLane.test.ts
```

Tasks:

- [ ] Port proven copy-event helper from Flow-Goodies.
- [ ] Detect package lane.
- [ ] Block direct import for packages with interactions/embeds/CMS/custom-code unless proven safe.
- [ ] Copy patched payload.
- [ ] Show paste instruction.
- [ ] Add error if clipboard copy fails.

Verification:

- [ ] Unit test lane decision.
- [ ] Manual Webflow test: copied payload pastes.
- [ ] Manual Webflow test: IX3 package uses clipboard lane.

## Phase 9 — CMS Preparation

Goal: handle CMS without confusing buyer.

Files:

```text
src\features\cms\cmsTypes.ts
src\features\cms\cmsPlanner.ts
src\features\cms\cmsInstaller.ts
src\features\cms\CmsPreparationPanel.tsx
tests\cmsPlanner.test.ts
```

Tasks:

- [ ] Parse CMS manifest.
- [ ] Display collections/items/fields.
- [ ] Decide install mode:
  - no CMS
  - static fill
  - map existing
  - auto import
  - manual
- [ ] Implement no-CMS path.
- [ ] Implement static-fill path if package supports it.
- [ ] Prototype Data API import only after scope/capability verification.
- [ ] Add mapping UX plan before building mapping UI.

Verification:

- [ ] Unit test no-CMS package.
- [ ] Unit test static-fill package.
- [ ] Manual test package with CMS shows correct plan.
- [ ] Do not claim automatic CMS binding until verified in real Webflow.

## Phase 10 — Backend Prototype

Goal: install code fetches package from a controlled endpoint.

Recommended repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker
```

Files:

```text
AGENTS.md
CLAUDE.md
README.md
package.json
wrangler.toml
.env.example
src\index.ts
src\installCodes.ts
src\packages.ts
src\storage.ts
tests\*.test.ts
```

Tasks:

- [ ] Create backend repo or worker folder.
- [ ] Create `.env.example`.
- [ ] Add no-secret credential map.
- [ ] Implement `POST /api/install-codes/resolve`.
- [ ] Implement package manifest route.
- [ ] Implement package file route.
- [ ] Implement asset route or signed URL redirect.
- [ ] Add CORS for extension origin.
- [ ] Add install event route.
- [ ] Add basic rate limiting if feasible.
- [ ] Add local mock package storage.
- [ ] Deploy to staging Worker.

Verification:

- [ ] Local tests pass.
- [ ] Staging endpoint resolves a test code.
- [ ] Extension fetches package from staging endpoint.
- [ ] Secret values are not committed.

## Phase 11 — Package Generator Prototype

Goal: create one real install package from current converter output.

Files in Flowbridge-claude may include:

```text
src\lib\package\
src\lib\package\types.ts
src\lib\package\build-package.ts
src\lib\package\validate-package.ts
tests\package\*.test.ts
```

Tasks:

- [ ] Define package schema shared or mirrored with extension.
- [ ] Convert minimal converter output into package shape.
- [ ] Add asset manifest from source/pretreated HTML.
- [ ] Add font manifest.
- [ ] Add placeholder CMS manifest if no CMS.
- [ ] Add interaction manifest.
- [ ] Validate package.
- [ ] Write package output folder.
- [ ] Upload package to package backend manually or via script.

Verification:

- [ ] Package validates.
- [ ] Extension loads package.
- [ ] Asset upload and paste works with generated package.

## Phase 12 — End-To-End Prototype

Goal: buyer-like flow works in a test Webflow site.

Test setup:

- one simple package
- one required image
- one required Google/custom font
- no CMS initially
- IX3 if available after current package supports it, otherwise static first

Steps:

- [ ] Generate package.
- [ ] Upload package to staging backend.
- [ ] Create test install code.
- [ ] Open buyer test Webflow site.
- [ ] Open extension.
- [ ] Enter code.
- [ ] Confirm site/page detection.
- [ ] Confirm missing font detection.
- [ ] Install font manually.
- [ ] Rescan.
- [ ] Upload asset.
- [ ] Copy/install XscpData.
- [ ] Paste.
- [ ] Inspect result visually.
- [ ] Publish test page if needed.
- [ ] Confirm image URL resolves from buyer Webflow assets.

Verification:

- [ ] User did not type site ID.
- [ ] User did not paste Webflow token into marketplace page.
- [ ] User had a clear font preparation step.
- [ ] Required assets uploaded to target site.
- [ ] Pasted result appears on correct current page.

---

## 12. Detailed Task Checklist By Workstream

### 12.1 Workstream A — Product Contract

- [ ] Decide package schema version name.
- [ ] Decide install package file name.
- [ ] Decide whether package includes full XscpData inline or separate `xscp.json`.
- [ ] Decide asset URL signing policy.
- [ ] Decide code redemption validity rules.
- [ ] Decide whether one code can install multiple times.
- [ ] Decide how buyer accesses reinstall history.
- [ ] Decide font blocking policy.
- [ ] Decide CMS first-release policy.
- [ ] Decide custom-code install policy.

### 12.2 Workstream B — Extension Shell

- [ ] New repo created.
- [ ] Local docs created.
- [ ] Webflow extension config created.
- [ ] Build works.
- [ ] Webflow dev load works.
- [ ] App state model exists.
- [ ] Error model exists.
- [ ] Debug logging toggle exists.

### 12.3 Workstream C — Package Fetch

- [ ] Code entry form.
- [ ] Resolve endpoint client.
- [ ] Package fetch client.
- [ ] Runtime validation.
- [ ] Invalid code error.
- [ ] Expired code error.
- [ ] Network error.
- [ ] Unsupported package version error.

### 12.4 Workstream D — Site Context

- [ ] Current site ID fetch.
- [ ] Current site name display.
- [ ] Current page ID fetch.
- [ ] Current page name display.
- [ ] Missing page handling.
- [ ] Page change handling, if Webflow supports events.

### 12.5 Workstream E — Fonts

- [ ] Package fonts parsed.
- [ ] Webflow fonts scanned.
- [ ] Required fonts diffed.
- [ ] Optional fonts diffed.
- [ ] Weights/styles displayed.
- [ ] Manual install copy written.
- [ ] Rescan action.
- [ ] Blocking policy implemented.

### 12.6 Workstream F — Assets

- [ ] Package assets parsed.
- [ ] Asset fetch works.
- [ ] File conversion works.
- [ ] Upload works.
- [ ] Progress works.
- [ ] Retry works.
- [ ] Required/optional policy works.
- [ ] Upload result map created.
- [ ] Image patch works.
- [ ] Background patch works.
- [ ] Empty `payload.assets[]` enforced.

### 12.7 Workstream G — CMS

- [ ] CMS manifest parsed.
- [ ] No-CMS flow complete.
- [ ] CMS summary UI complete.
- [ ] Static-fill strategy implemented if package supports it.
- [ ] Auto-import feasibility tested.
- [ ] Mapping UX designed before full build.
- [ ] CMS import errors are user-readable.

### 12.8 Workstream H — Interactions / IX

- [ ] Interaction manifest parsed.
- [ ] Page ID patching works.
- [ ] IX3 page-scoped references patched.
- [ ] IX2/IX3 preservation tested with fixtures when available.
- [ ] Unsupported interaction warnings shown.
- [ ] Custom runtime requirements shown.

### 12.9 Workstream I — Paste / Install

- [ ] Lane decision function.
- [ ] Clipboard helper.
- [ ] Direct Designer API insertion only for safe payloads.
- [ ] Copy success UI.
- [ ] Paste instructions.
- [ ] Clipboard failure recovery.
- [ ] Post-paste checklist.

### 12.10 Workstream J — Backend

- [ ] Worker/repo decision.
- [ ] Env examples.
- [ ] Secret retrieval documented.
- [ ] Code resolve endpoint.
- [ ] Package endpoint.
- [ ] Asset endpoint.
- [ ] Install events.
- [ ] CORS.
- [ ] Staging deploy.
- [ ] Test code.

### 12.11 Workstream K — Verification

- [ ] Unit tests.
- [ ] Extension build.
- [ ] Backend tests.
- [ ] Staging package fetch.
- [ ] Webflow manual install test.
- [ ] Visual check against source.
- [ ] Asset URL check.
- [ ] Font warning check.
- [ ] CMS check when implemented.

---

## 13. Sub-Agent / Execution Lane Recommendation

Use one main lane plus up to three bounded side lanes when executing this plan.

### 13.1 Main Lane

Recommended model:

```text
gpt-5.3-codex or gpt-5.4
```

Responsibilities:

- own architecture decisions
- create extension scaffold
- integrate package/client/site/font/asset/paste flows
- keep scope tight
- run final verification
- write handoff

### 13.2 Explorer Lane: Current Flow-Goodies Reference

Recommended model:

```text
gpt-5.4-mini
```

Responsibilities:

- inspect current Flow-Goodies helper functions
- list reusable code paths
- identify stale/drifted contract areas
- do not edit files

Output:

- short report with file paths and recommended port candidates

### 13.3 Backend Lane

Recommended model:

```text
gpt-5.3-codex
```

Responsibilities:

- create or prototype package worker
- define env examples
- implement code/package endpoints
- use existing credentials safely
- do not expose secrets

Write scope:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\package-worker
```

### 13.4 Package Schema Lane

Recommended model:

```text
gpt-5.3-codex
```

Responsibilities:

- define package schema in Flowbridge-claude or shared package
- build mock/generated package
- validate package

Write scope:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude
```

### 13.5 Verification Lane

Recommended model:

```text
gpt-5.4-mini or gpt-5.3-codex
```

Responsibilities:

- verify extension build
- verify backend route
- verify package schema
- run manual Webflow checklist if browser/Webflow access is available
- produce evidence, not claims

---

## 14. Risk Register

### Risk 1 — Webflow API Cannot Fully Automate CMS Binding

Impact:

- buyer may still need guided CMS mapping

Mitigation:

- keep CMS as separate preparation step
- support static-fill packages
- only claim auto CMS after verified

### Risk 2 — Fonts Cannot Be Installed Programmatically

Impact:

- manual user action required

Mitigation:

- make missing-font preflight clear and early
- show exact family/weights/styles
- rescan after manual install

### Risk 3 — Clipboard Payload Breaks If `payload.assets[]` Is Populated

Impact:

- Webflow paste may crash/fail

Mitigation:

- keep `payload.assets[]` empty
- use separate asset manifest
- patch image references after upload

### Risk 4 — Direct Designer API Insertion Loses Fidelity

Impact:

- interactions/embeds/CMS may not survive

Mitigation:

- default full-fidelity packages to clipboard lane
- direct insertion only for safe packages

### Risk 5 — Package Assets Are Publicly Guessable

Impact:

- paid templates can leak

Mitigation:

- signed URLs or code-gated routes
- package-level access checks
- avoid permanent public package JSON when product is paid

### Risk 6 — Secret Leakage

Impact:

- account compromise

Mitigation:

- use `.env.example` for names only
- ignored `.env.local` for local values
- Cloudflare/Webflow dashboard for secrets
- never paste values into docs/chat/logs

### Risk 7 — IX2/IX3 Conversion Becomes Too Coupled To Skill

Impact:

- fragile packages and hard-to-debug interactions

Mitigation:

- deterministic converter owns final IX JSON
- skill only classifies/prepares/verifies
- old converter modules pulled deliberately and tested

### Risk 8 — User Still Feels Too Many Steps

Impact:

- product feels hard despite technical correctness

Mitigation:

- present one install journey with staged checklist
- hide implementation lanes
- keep user actions to:
  1. enter code
  2. install missing fonts if needed
  3. paste/install

---

## 15. Acceptance Criteria

### 15.1 Prototype Acceptance

The prototype is acceptable when:

- [ ] New extension exists in its own repo.
- [ ] Buyer can enter a test code.
- [ ] Extension fetches a mock/staging package.
- [ ] Extension detects current Webflow site/page.
- [ ] Extension identifies missing fonts from package manifest.
- [ ] Extension uploads at least one image into the target site.
- [ ] Extension patches XscpData with uploaded asset info.
- [ ] Extension patches current page ID.
- [ ] Extension copies final payload to clipboard.
- [ ] User can paste into Webflow.
- [ ] Pasted element/page visually includes uploaded target-site image.
- [ ] No Webflow token is typed into the marketplace page.
- [ ] No secret values are committed or written to docs.

### 15.2 First Release Acceptance

The first real release is acceptable when:

- [ ] Package backend validates install codes.
- [ ] Package storage is access-controlled enough for paid products.
- [ ] Extension error states are user-readable.
- [ ] Font preflight works with real packages.
- [ ] Asset upload works for all package image roles used by release templates.
- [ ] CMS behavior is honest and verified.
- [ ] IX3/page-scoped payloads install correctly for supported packages.
- [ ] Unsupported interactions are flagged before install.
- [ ] Post-install checklist catches the known manual tasks.
- [ ] Documentation tells future agents exactly where credentials live without exposing values.

---

## 16. Commands To Expect

Current Flowbridge-claude:

```bash
bun run test
bun run typecheck
bun run build:playground
```

Current Flow-Goodies reference:

```bash
npm run dev
npm run build
npm run test
npm run lint
```

New extension expected:

```bash
npm install
npm run dev
npm run build
npm run test
npm run lint
```

New backend expected:

```bash
npm install
npm run test
npm run dev
npm run deploy:staging
```

Do not run deployment commands without confirming credentials/environment.

---

## 17. Documentation To Create During Implementation

New extension docs:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\INSTALLER_ARCHITECTURE.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\PACKAGE_CONTRACT.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\CREDENTIALS_AND_ENV.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\WEBFLOW_CAPABILITIES.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\VERIFICATION.md
```

Backend docs:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\PACKAGE_API_CONTRACT.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\CREDENTIALS_AND_ENV.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\PACKAGE_STORAGE.md
```

Flowbridge-claude docs to update when package generation begins:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\architecture\PACKAGE-CONTRACT.md
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md
```

Avoid creating one-off markdown files in repo roots.

---

## 18. Immediate Next Prompt For An Executor

Use this only after Maria approves moving from plan to implementation.

```text
You are working on the Master Collection installer project.

Read:
1. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md
2. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\CLAUDE.md
3. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\plans\000-master-collection-extension-future-plan.md
4. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\AGENTS.md
5. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\CLAUDE.md

Goal for this first implementation pass:
Create a new repo at C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app. Do not modify the old Flow-Goodies app. Build a minimal Webflow Designer Extension shell that opens in Webflow, accepts a mock install code, loads a mock MasterCollectionPackage, detects current Webflow site/page through the Designer API, and renders the preflight checklist with package fonts/assets/CMS/interactions summary.

Credential rule:
Do not read or print secret values. Use .env.example for variable names. If backend credentials become necessary later, retrieve names/paths from the plan and ask before reading ignored .env.local values.

Scope for this pass:
- New extension scaffold
- package schema/types
- mock package
- current site/page adapter
- preflight checklist UI
- basic tests
- build verification

Out of scope:
- real backend
- real package purchase codes
- real asset upload
- CMS import
- modifying Flowbridge converter
- modifying old Flow-Goodies

Before editing, state exact files you will create. Then implement. Verify with build/tests and report evidence.
```

---

## 19. Final Recommendation

Yes, the new extension should be on the plan.

The right product architecture is:

```text
Marketplace sells and authorizes.
Package backend serves controlled install packages.
Flowbridge skill/converter generates portable packages.
New Webflow extension installs into the buyer's current site.
```

This gives the least-friction buyer experience because the user does not need to provide a Webflow site ID and should not need to place a Webflow token into the marketplace page. It also gives a natural place to prepare the user for manual font installation before import, which is exactly the kind of step that feels acceptable when it is shown inside Webflow as part of a clear install checklist.
