# Master Collection App Build Plan

Last verified: 2026-04-19

## Status

Planning artifact only. Do not treat this file as implementation evidence.

This plan recovers the detailed build path for the Master Collection Webflow Designer Extension in:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

It expands the active MVP plan without changing the product boundary.

## Source Of Truth

Read these before implementing:

- `AI.md`
- `AGENTS.md`
- `docs/DOCS_INDEX.md`
- `docs/ARCHITECTURE.md`
- `docs/WEBFLOW_APP_RESEARCH.md`
- `docs/plans/001-master-collection-extension-mvp.md`
- `app/AGENTS.md`
- `app/README.md`

Important local rules:

- Keep shared documentation in the parent `docs/` folder.
- Keep one project AI_OS at the parent root.
- Do not create `app/AI_OS/`.
- The app and site are siblings.
- The app installs inside Webflow.
- The site owns catalog, auth, checkout, account library, entitlements, install-code creation, and package access.

## Goal

Build the first Master Collection app as a Webflow Designer Extension that installs a purchased package into the buyer's current Webflow site/page.

MVP flow:

```text
Open Webflow project
Open Master Collection app inside Designer
Paste install code
Resolve package or use DEMO mock
Show current site/page
Show font checklist
Upload package assets into the current Webflow site
Patch XscpData with current page and uploaded asset references
Copy Webflow clipboard payload
User pastes into the current Webflow page
Show completion notes
```

## Non-Goals

Do not include these in the first app build:

- Hybrid App / Data Client / OAuth
- CMS import or CMS binding
- custom-code installation
- seller marketplace tools
- checkout, account, or entitlement creation
- package generator UI
- old Flow-Goodies utility tools
- asking buyers for Webflow site IDs, page IDs, or API tokens

If a package requires CMS or custom code, the MVP should block or show a clear unsupported warning.

## Webflow App Boundary

The first app is a Webflow App with the Designer Extension capability only.

Use Designer APIs for:

```ts
webflow.getSiteInfo()
webflow.getCurrentPage()
webflow.createAsset(file)
webflow.canForAppMode(...)
```

Use the Master Collection package backend for install-code and package data. The app may use `DEMO` as a local mock package mode before the backend is ready.

Do not add Data API/OAuth until a real feature requires server-side Webflow operations such as CMS import, custom code, webhooks, or broader site-data automation.

## App Folder Scaffold

Target folder:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

The folder already contains lightweight routing docs. Keep them unless a local app-specific implementation detail genuinely needs a new local doc.

Expected scaffold after implementation:

```text
app/
  AGENTS.md
  AI.md
  CLAUDE.md
  README.md
  .env.example
  .gitignore
  components.json
  index.html
  package.json
  postcss.config.*
  tsconfig.json
  tsconfig.node.json
  vite.config.ts
  webflow.json
  src/
    main.tsx
    index.css
    App.tsx
    components/
      ui/
      AppHeader.tsx
      InstallCodeStep.tsx
      TargetCheckStep.tsx
      FontChecklistStep.tsx
      AssetUploadStep.tsx
      ClipboardStep.tsx
      DoneStep.tsx
    lib/
      clipboard/
      package/
      webflow/
      xscp/
    mocks/
      demoPackage.ts
    test/
```

Keep the exact tree flexible if the Webflow CLI template creates a slightly different Vite layout. Preserve the boundaries and responsibilities.

## Stack

Use the smallest app stack that matches the MVP and local UI baseline:

- Webflow CLI Designer Extension project
- `webflow.json` with `apiVersion: "2"`
- Vite
- React
- TypeScript
- Tailwind v4
- shadcn/ui
- `radix-lyra`
- neutral light/dark CSS variables
- lucide icons
- compact Flow-Goodies-style UI
- runtime package validation
- unit tests for package validation and XscpData patching

Use the Webflow CLI when possible:

```bash
webflow extension init
webflow extension serve
```

The Webflow local extension serve default is port `1337`.

Use normal app scripts once scaffolded:

```bash
npm run dev
npm run build
npm run test
npm run lint
```

Add only scripts that actually exist and pass.

## UI Baseline

Follow the shared baseline in `AGENTS.md` and the MVP plan:

- shadcn/ui
- `radix-lyra`
- Tailwind v4 CSS variables
- neutral light/dark mode
- lucide icons
- compact Flow-Goodies-style UI
- no marketing page
- no decorative branded theme
- no extra color palette
- no gradients or ornamental backgrounds

Reference styling source, read-only unless Maria explicitly asks otherwise:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

Required shadcn baseline:

```json
{
  "style": "radix-lyra",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

CSS baseline:

- `@import "tailwindcss";`
- `@import "tw-animate-css";`
- `@import "shadcn/tailwind.css";`
- neutral light/dark variables from Flow-Goodies
- `--radius: 0;`
- `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

Initial UI components:

- small header
- product name and version
- outline light/dark toggle
- install code input
- compact step panels
- clear loading/error states

Use `master-collection-theme` as the localStorage key for theme mode.

## Package Schema

Keep the first package contract tiny and explicit:

```ts
export interface MasterCollectionPackage {
  schemaVersion: "master-collection-package@1";
  packageId: string;
  productId?: string;
  name: string;
  version: string;
  xscpData: unknown;
  fonts: SimpleFontRequirement[];
  assets: SimpleAssetRequirement[];
  warnings?: SimplePackageWarning[];
}
```

Fonts:

```ts
export interface SimpleFontRequirement {
  family: string;
  weights?: Array<string | number>;
  styles?: string[];
  required: boolean;
  installNote?: string;
}
```

Assets:

```ts
export interface SimpleAssetRequirement {
  key: string;
  fileName: string;
  url: string;
  mimeType?: string;
  required: boolean;
  patchTargets: SimpleAssetPatchTarget[];
}
```

Patch targets:

```ts
export interface SimpleAssetPatchTarget {
  kind: "image-src" | "image-asset-id" | "background-url";
  path: Array<string | number>;
}
```

Warnings:

```ts
export interface SimplePackageWarning {
  code:
    | "CMS_NOT_SUPPORTED"
    | "CUSTOM_CODE_NOT_SUPPORTED"
    | "INTERACTIONS_LIMITED"
    | "FONT_MANUAL_INSTALL";
  message: string;
}
```

Rules:

- `xscpData.payload.assets` stays empty for clipboard paste.
- Package assets live in `assets[]`, not Webflow clipboard `payload.assets[]`.
- Runtime validation must reject invalid package data before install steps run.
- CMS packages should block or warn in the MVP.
- Custom-code packages should block in the MVP.

Use TypeScript types plus a runtime validator. A small schema library such as `zod` is acceptable if no existing app validation pattern exists after scaffold.

## DEMO Package

Add a development-only mock package resolved by install code:

```text
DEMO
```

The DEMO package should include:

- `schemaVersion: "master-collection-package@1"`
- stable demo `packageId`
- name and version
- one simple `xscpData` payload
- one required font
- one image asset
- at least one image patch target
- at least one warning if a manual step is being demonstrated

DEMO exists to let the app validate the full inside-Webflow flow before the package backend is ready.

Do not treat DEMO as a replacement for the backend contract.

## Webflow Adapter

Create a thin adapter around Designer APIs so UI state and tests do not depend directly on the global `webflow` object.

Adapter responsibilities:

- detect whether the Designer API is available
- check required capabilities with `webflow.canForAppMode(...)` where practical
- call `webflow.getSiteInfo()`
- call `webflow.getCurrentPage()`
- upload files with `webflow.createAsset(file)`
- normalize Webflow API errors into readable app errors

Suggested shape:

```ts
export interface WebflowTargetContext {
  siteId: string;
  siteName: string;
  pageId?: string;
  pageName?: string;
}

export interface UploadedWebflowAsset {
  packageAssetKey: string;
  fileName: string;
  assetId?: string;
  url?: string;
}
```

Do not ask the user to enter a site ID or page ID. If current site/page cannot be detected, block the install step with a clear message.

## Font Checklist

Fonts are manual in the MVP.

Requirements:

- Render package fonts from the package manifest.
- Show family, weights, styles, and required/optional status.
- Show a clear manual-install instruction.
- Require user confirmation before continuing when required fonts exist.
- Do not promise perfect font detection.
- Do not auto-install custom font files.

Later research may add better detection, but this plan does not depend on it.

## Asset Upload

Asset upload happens inside Webflow using the Designer API:

1. Read package `assets[]`.
2. Fetch each asset URL.
3. Convert each response into a `Blob`.
4. Create a `File` with the package file name and MIME type.
5. Call `webflow.createAsset(file)`.
6. Store the returned Webflow asset ID and/or hosted URL.
7. Show upload progress and retry failed uploads.
8. Pass uploaded asset data into XscpData patching.

Rules:

- Do not request Webflow API tokens.
- Asset URLs must be fetchable by the extension with CORS.
- Required asset failures block paste.
- Optional asset failures show a warning and allow the user to decide if the UI supports it.

## XscpData Patching

Patch a cloned copy of the package `xscpData`.

Required behavior:

- patch current page placeholders using the current Designer page context
- patch `image-src` targets with uploaded asset URLs
- patch `image-asset-id` targets with uploaded asset IDs when available
- patch `background-url` targets with uploaded asset URLs
- preserve unrelated XscpData
- enforce empty `payload.assets[]`
- fail loudly on missing required patch targets

The path patcher should be tested without Webflow.

Test cases:

- patches image `src`
- patches image asset ID
- patches background URL
- rejects invalid paths for required assets
- keeps `payload.assets[]` empty
- leaves unrelated payload fields unchanged

## Clipboard Helper

Use the proven Flow-Goodies Webflow clipboard strategy as the reference.

Requirements:

- copy the final patched XscpData payload
- show clear paste instructions
- handle copy failure
- do not expose raw XscpData unless needed for debugging
- keep the helper minimal and app-owned after porting

The user-facing step should say what to do in Webflow, not explain the internal payload format.

## Screens And State

Use a simple step flow:

1. Enter Code
2. Target Check
3. Font Checklist
4. Prepare Images
5. Paste Into Webflow
6. Done

State should track:

- install code
- package load status
- validated package
- current site/page context
- font confirmation
- asset upload status by package asset key
- uploaded Webflow asset mapping
- patched XscpData
- clipboard copy status
- final warnings

Avoid a large state-management library unless the scaffold or implementation proves it is necessary.

## Backend Boundary

The real package fetch can wait until the shell and DEMO flow work.

Expected future endpoint:

```text
POST /api/install-code/resolve
```

Environment variable:

```text
VITE_MASTER_COLLECTION_API_BASE_URL
```

Backend/package worker secret names only:

```text
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
UPLOAD_API_KEY
```

Do not print secret values. Do not commit `.env.local`.

## Implementation Sequence

### Phase 1 - Designer Extension Shell

Goal: app opens inside Webflow and builds.

Tasks:

- scaffold the Webflow Designer Extension in `app/`
- preserve existing child routing docs
- configure `webflow.json` with `apiVersion: "2"`
- set up Vite, React, TypeScript, Tailwind v4, shadcn, lucide
- apply the Flow-Goodies neutral light/dark baseline
- add `.env.example`
- add install code screen
- add theme toggle
- add build/dev/test scripts that actually work

Verification:

- `npm run build`
- app renders locally
- if possible, `webflow extension serve` opens in Webflow Designer

### Phase 2 - Package Contract And DEMO

Goal: app can load a valid mock package.

Tasks:

- add package types
- add runtime validation
- add `DEMO` mock package
- load `DEMO` from the install code screen
- render package name/version
- reject invalid package shape

Verification:

- unit test validates DEMO
- unit test rejects invalid package
- UI displays DEMO package metadata

### Phase 3 - Current Site/Page Detection

Goal: app knows where the user is installing.

Tasks:

- add Webflow adapter
- detect Designer API availability
- call `getSiteInfo`
- call `getCurrentPage`
- display site/page names
- block if current page cannot be detected

Verification:

- adapter tests for fallback/error normalization
- manual Webflow test shows correct site/page when available

### Phase 4 - Font Checklist

Goal: user sees font requirements before install.

Tasks:

- render package fonts
- show required vs optional
- show weights/styles
- show manual install note
- require confirmation for required fonts

Verification:

- required font blocks until confirmation
- optional font does not block
- DEMO font appears correctly

### Phase 5 - Asset Upload

Goal: package assets upload into the buyer's current Webflow site.

Tasks:

- fetch asset URLs
- convert responses to `File`
- call `webflow.createAsset(file)`
- track upload status
- support retry on failed upload
- store uploaded ID/URL mapping

Verification:

- upload adapter can be mocked in tests
- manual Webflow test uploads one DEMO image into Assets
- no Webflow token is requested

### Phase 6 - XscpData Patch

Goal: final payload points to current page and uploaded assets.

Tasks:

- clone package XscpData
- patch page placeholders
- patch asset targets
- enforce empty `payload.assets[]`
- report missing required patch targets

Verification:

- unit tests cover patch targets
- manual payload inspection shows uploaded asset references

### Phase 7 - Clipboard Paste

Goal: user can paste final package into Webflow.

Tasks:

- port minimal clipboard helper from Flow-Goodies
- copy final patched XscpData
- show paste instructions
- show success/failure state

Verification:

- manual paste works in Webflow Designer
- pasted component includes uploaded image
- user did not type site ID or Webflow token

### Phase 8 - Real Package Fetch

Goal: install code resolves through the package backend.

Tasks:

- add API client using `VITE_MASTER_COLLECTION_API_BASE_URL`
- define request/response contract for `POST /api/install-code/resolve`
- keep `DEMO` mock mode for development
- handle invalid code and expired code errors
- verify package JSON before using it

Verification:

- valid test code resolves
- invalid code shows readable error
- package asset URL fetch succeeds from extension

## Verification Plan

Use the lightest credible verification for each phase, then run the full available app verification before handoff.

Minimum final verification for implementation:

- `npm run build`
- `npm run test` if tests are configured
- `npm run lint` if lint is configured
- manual or browser check that the app UI renders
- Webflow Designer manual check when Webflow access is available

Manual Webflow verification checklist:

- app opens inside Designer
- current site is detected
- current page is detected
- DEMO package loads
- required font checklist blocks until confirmed
- one image uploads to Webflow Assets
- final XscpData is copied
- paste into Designer works
- pasted element references uploaded asset
- no buyer Webflow token/site ID/page ID is requested

If Webflow Designer verification is not available, report the result as partial verification and say exactly which manual checks remain.

## Completion Criteria

The app MVP is complete only when:

- the Designer Extension shell exists and builds
- `DEMO` package validates and loads
- current site/page detection is implemented
- font checklist is implemented
- asset upload path is implemented
- XscpData patching is implemented and tested
- clipboard helper is implemented
- the UI supports the full install flow
- verification evidence is recorded

Docs-only, setup-only, or scaffold-only work does not count as app MVP completion.

