# Master Collection MVP — Inside-Webflow App Plan

> **For agentic workers:** This replaces the first implementation target from `092-plan-new-master-collection-extension.md` with a smaller MVP. Keep the larger plan as future architecture context, but execute this file first unless Maria explicitly re-expands scope.

**Goal:** Build a new, small Webflow Designer Extension named **Master Collection** that runs inside Webflow and does only one job first: install a purchased package into the current Webflow site/page with minimal friction.

**MVP scope:** install code → fetch package → show font checklist → upload images/assets to current Webflow site → patch XscpData → copy/paste into current page.

**Not in MVP:** CMS automation, Hybrid App/OAuth, custom code installation, seller marketplace, payments, template generation UI, old Flow-Goodies utility tools.

---

## 1. Direct Answer

Yes. This is the app inside Webflow.

Technically, it is a **Webflow App with the Designer Extension capability**. It opens inside the Webflow Designer as an iframe/panel and can call the Designer API.

For the first version, do **not** build a full Hybrid App. Start with a Designer Extension only.

Why:

- Webflow docs say Designer Extensions run directly in Webflow's interface.
- The Designer API can read current site information.
- The Designer API can read the current page.
- The Designer API can upload assets into the site's Assets panel using `webflow.createAsset(file)`.
- This is enough for the first installation path.
- CMS automation can wait for version 2, where we may add the Data Client/Hybrid App capability.

Working product name:

```text
Master Collection
```

Recommended repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

UI requirement:

Use the same visual system as the current Flow-Goodies app: shadcn, bare neutral styling, light/dark mode only, no custom marketing look, no decorative theme.

Current reference app, read-only unless explicitly asked:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

---

## 2. Webflow Docs Check

Official docs checked on 2026-04-19:

- Designer Extensions: https://developers.webflow.com/designer/data/docs/designer-extensions
- Configuring Designer Extension: https://developers.webflow.com/apps/designer/guides/configuring-your-app
- Get site information: https://developers.webflow.com/designer/reference/get-site-info
- Get current page: https://developers.webflow.com/designer/reference/get-current-page
- Designer Asset APIs: https://developers.webflow.com/designer/reference/asset-overview
- Register an App: https://developers.webflow.com/apps/data/docs/register-an-app
- Hybrid Apps: https://developers.webflow.com/data/v2.0.0-beta/docs/hybrid-apps
- Data API Upload Asset: https://developers.webflow.com/data/reference/assets/assets/create
- Data API List Collections: https://developers.webflow.com/data/reference/cms/collections/list
- Data API Create CMS Items: https://developers.webflow.com/data/reference/cms/collection-items/staged-items/create-items
- Font variables: https://developers.webflow.com/designer/reference/create-font-family-variable

Key findings:

1. Designer Extensions run directly inside Webflow's interface and can interact with the Designer.
2. `webflow.json` should use `apiVersion: "2"`.
3. Webflow recommends using `webflow extension init` for new Designer Extensions.
4. `webflow.getSiteInfo()` returns `siteId`, `siteName`, workspace info, and domain info.
5. `webflow.getCurrentPage()` returns the page open in the Designer.
6. Designer Asset APIs support uploading assets to the current Webflow site through `webflow.createAsset(file)`.
7. Data Client/OAuth is only needed when we need server-side Webflow Data API operations such as CMS, advanced site data, custom code, or external-user OAuth.
8. Hybrid Apps combine Designer Extension and Data Client; useful later, not necessary for the first installer MVP.
9. Data API asset upload exists and requires `assets:write`, but the simpler MVP can avoid this path by using the Designer `createAsset` API.
10. Data API CMS operations exist and require CMS scopes, but CMS automation should be deferred.
11. The docs show font-family variables can be created by name, but that is not the same as installing custom font files. Missing font installation should stay manual in MVP.

---

## 3. MVP Product Flow

The first app should feel like this:

```text
Open Webflow project
Open Master Collection
Paste install code
Installer fetches package
Installer shows target site/page
Installer shows required fonts
User installs missing fonts manually if needed
Installer uploads package images into current Webflow site
Installer patches XscpData with current page + uploaded assets
Installer copies final payload
User pastes into Webflow
Done
```

The user should not need to:

- type a Webflow site ID
- paste a Webflow API token into the marketplace
- understand package storage
- understand XscpData
- manually upload images
- touch the old converter playground

---

## 4. MVP Architecture

Use only three pieces first:

```text
1. Package generator
   Produces a simple install package.

2. Package backend
   Resolves install code and serves package/assets.

3. Webflow Designer Extension
   Runs inside Webflow and installs the package.
```

Do not build CMS/backend OAuth in MVP.

### 4.0 UI And Styling Baseline

The new folder should copy the styling approach from Flow-Goodies, not invent a new interface.

Reference files:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\components.json
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\index.css
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\src\components\App.tsx
```

Required shadcn config baseline:

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

Required CSS baseline:

- Tailwind v4.
- `@import "tailwindcss";`
- `@import "tw-animate-css";`
- `@import "shadcn/tailwind.css";`
- neutral light/dark CSS variables from Flow-Goodies.
- `--radius: 0;`
- `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- no additional color palette.
- no decorative gradients.
- no custom branded skin beyond the Flow-Goodies neutral theme.

Required UI behavior:

- one small header
- product name + version
- small outline light/dark toggle
- app root toggles `.dark` on `document.documentElement`
- localStorage theme key for the new app, for example `master-collection-theme`
- same compact spacing density as Flow-Goodies
- shadcn primitives only where useful
- plain step panels, not a marketing page

Recommended initial shadcn components:

```text
button
card
label
switch
```

Add more components only when the MVP needs them.

### 4.1 Package Generator

Source:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude
```

MVP output:

```json
{
  "schemaVersion": "master-collection-package@1",
  "packageId": "pkg_demo_001",
  "name": "Demo Component",
  "xscpData": {},
  "fonts": [],
  "assets": []
}
```

### 4.2 Package Backend

For MVP, the backend can be extremely simple:

- install code maps to a package JSON
- package JSON has asset URLs
- assets are hosted where extension can fetch them with CORS

Existing credentials/reference:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\wrangler.toml
```

Known worker reference:

```text
flowbridge-assets
```

Known secret names only:

```text
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
UPLOAD_API_KEY
```

Do not expose secret values in docs, chat, commits, or logs.

### 4.3 Webflow Designer Extension

New repo:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app
```

App capability:

```text
Designer Extension only
```

Not Hybrid yet.

Required Designer API calls:

```ts
webflow.getSiteInfo()
webflow.getCurrentPage()
webflow.createAsset(file)
```

Clipboard paste:

Use the existing Flow-Goodies copy/paste strategy as reference.

---

## 5. Simple Package Contract

Keep the first package contract tiny.

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
  code: "CMS_NOT_SUPPORTED" | "CUSTOM_CODE_NOT_SUPPORTED" | "INTERACTIONS_LIMITED" | "FONT_MANUAL_INSTALL";
  message: string;
}
```

Rules:

- `xscpData.payload.assets` stays empty for clipboard paste.
- Package assets live in `assets[]`, not Webflow clipboard `payload.assets[]`.
- CMS packages can be detected but should block or warn in MVP.
- Custom-code packages can be detected but should block or warn in MVP.

---

## 6. Simple Extension Screens

### Screen 1 — Enter Code

Fields:

- install code input
- continue button

Behavior:

- call package backend
- show loading/error
- load package into state

### Screen 2 — Target Check

Show:

- current Webflow site name
- current page name

Behavior:

- use `webflow.getSiteInfo()`
- use `webflow.getCurrentPage()`
- block if current page cannot be detected

### Screen 3 — Font Checklist

Show:

- required fonts
- weights/styles
- "Install these in Webflow before importing"
- "I installed them / continue" button

MVP policy:

- Do not try to auto-install fonts.
- Do not promise perfect font detection.
- Use package manifest as the source of truth.
- If we can cheaply scan existing font variables, add "detected" later.

### Screen 4 — Prepare Images

Show:

- asset count
- upload progress
- retry failed uploads

Behavior:

- fetch each package asset URL
- make a `File`
- call `webflow.createAsset(file)`
- collect returned asset IDs/URLs
- patch XscpData

### Screen 5 — Paste Into Webflow

Show:

- "Copy for Webflow"
- short paste instruction

Behavior:

- patch page IDs using current page
- patch assets using uploaded Webflow asset IDs/URLs
- copy final XscpData using proven Webflow clipboard strategy
- user pastes into Designer

### Screen 6 — Done

Show:

- images uploaded
- payload copied
- remaining manual notes

---

## 7. Implementation Phases

## Phase 1 — New Designer Extension Shell

Goal:

New app opens inside Webflow.

Tasks:

- [ ] Create `C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app`.
- [ ] Initialize with Webflow CLI if possible: `webflow extension init`.
- [ ] Use `apiVersion: "2"` in `webflow.json`.
- [ ] Add React/TypeScript if CLI template supports it.
- [ ] Add shadcn using the same Flow-Goodies baseline: `radix-lyra`, neutral, CSS variables, Tailwind v4, lucide icons.
- [ ] Copy/adapt the Flow-Goodies `src/index.css` token structure.
- [ ] Implement light/dark mode only.
- [ ] Match Flow-Goodies compact header and theme toggle style.
- [ ] Add local `AGENTS.md`.
- [ ] Add `.env.example`.
- [ ] Add "Enter install code" screen.
- [ ] Build extension.
- [ ] Serve extension locally in Webflow.

Verification:

- [ ] App opens in Webflow Designer.
- [ ] Code input renders.
- [ ] `npm run build` passes.

## Phase 2 — Mock Package

Goal:

App can load a fake package without backend.

Tasks:

- [ ] Add `MasterCollectionPackage` types.
- [ ] Add runtime validation.
- [ ] Add mock package with one image and one font.
- [ ] Code `DEMO` loads mock package.
- [ ] Render package name/version.

Verification:

- [ ] Unit test validates mock package.
- [ ] Invalid package is rejected.
- [ ] UI displays mock package.

## Phase 3 — Current Site/Page Detection

Goal:

App knows where the user is installing.

Tasks:

- [ ] Add Webflow adapter.
- [ ] Call `webflow.getSiteInfo()`.
- [ ] Call `webflow.getCurrentPage()`.
- [ ] Display site/page names.
- [ ] Store `siteId` and page reference/ID.

Verification:

- [ ] Manual Webflow test shows correct site.
- [ ] Manual Webflow test shows correct page.
- [ ] Missing page/API error shows readable error.

## Phase 4 — Font Checklist

Goal:

User sees fonts before install.

Tasks:

- [ ] Render package fonts.
- [ ] Mark required vs optional.
- [ ] Show weights/styles.
- [ ] Add "I installed these fonts" button.
- [ ] Add warning that custom fonts must be installed manually in Webflow.

Verification:

- [ ] Mock package font appears.
- [ ] Required font blocks until user confirms.
- [ ] Optional font does not block.

## Phase 5 — Asset Upload

Goal:

Images are uploaded into the buyer's current Webflow site from inside Webflow.

Tasks:

- [ ] Fetch package asset URL.
- [ ] Convert response to Blob/File.
- [ ] Call `webflow.createAsset(file)`.
- [ ] Capture Webflow asset result.
- [ ] Show upload progress.
- [ ] Retry failures.

Verification:

- [ ] One test image uploads into Webflow Assets panel.
- [ ] Upload error is readable.
- [ ] No Webflow token is requested.

## Phase 6 — Patch XscpData

Goal:

Final payload points to current page and newly uploaded assets.

Tasks:

- [ ] Clone XscpData.
- [ ] Patch current page ID placeholders.
- [ ] Patch image `src` targets.
- [ ] Patch image asset ID targets.
- [ ] Patch background URL targets if present.
- [ ] Enforce empty `payload.assets[]`.

Verification:

- [ ] Unit test patches image src.
- [ ] Unit test patches asset ID.
- [ ] Unit test keeps `payload.assets[]` empty.
- [ ] Manual payload inspection shows target asset URL/ID.

## Phase 7 — Clipboard Paste

Goal:

User can paste final package into Webflow.

Tasks:

- [ ] Port/copy minimal proven clipboard helper from Flow-Goodies.
- [ ] Copy final XscpData.
- [ ] Show paste instructions.
- [ ] Handle copy failure.

Verification:

- [ ] Manual paste works in Webflow Designer.
- [ ] Pasted component includes uploaded image.
- [ ] User did not type site ID or Webflow token.

## Phase 8 — Replace Mock Backend With Real Package Fetch

Goal:

Install code fetches package from backend.

Tasks:

- [ ] Define simple endpoint: `POST /api/install-code/resolve`.
- [ ] Return package URL or package JSON.
- [ ] Serve assets with CORS.
- [ ] Wire extension to real endpoint.
- [ ] Keep `DEMO` mock mode for development.

Verification:

- [ ] Test code resolves.
- [ ] Package loads.
- [ ] Asset URL fetch succeeds from extension.

---

## 8. What We Deliberately Postpone

### CMS

Postpone CMS automation.

Reason:

- It likely requires Data Client/OAuth scopes.
- Cross-site CMS binding has known risk.
- MVP can still be valuable without CMS.

MVP behavior:

- If package includes CMS, show:

```text
This package needs CMS data. CMS install is coming next, so this package cannot be installed by the simple installer yet.
```

### Custom Code

Postpone custom code installation.

Reason:

- Needs stronger permissions and review.
- For Webflow-native components, should not be common.

MVP behavior:

- Block packages requiring custom code.

### Hybrid App

Postpone Hybrid App.

Reason:

- Designer Extension alone is enough for current site/page + asset upload + paste.
- Hybrid/OAuth increases complexity and user trust burden.

When to add Hybrid:

- CMS import
- custom code registration
- advanced package licensing tied to Webflow accounts
- server-side Webflow Data API operations

---

## 9. Credential Rules For MVP

The extension should not need buyer Webflow tokens.

The extension may need:

```text
VITE_MASTER_COLLECTION_API_BASE_URL
```

Backend/package worker may need:

```text
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET
UPLOAD_API_KEY
```

Existing reference paths:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.example
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\.env.local
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-rebuild-clean\wrangler.toml
```

Do not print secret values.

Do not commit `.env.local`.

Do not ask Maria for a Webflow site ID in the app. The app should get it from `webflow.getSiteInfo()`.

---

## 10. First Executor Prompt

Use this prompt when Maria approves implementation:

```text
Build the simple Master Collection MVP as a new Webflow Designer Extension.

Read:
1. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\docs\STATE.md
2. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flowbridge-claude\CLAUDE.md
3. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\docs\plans\001-master-collection-extension-mvp.md
4. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\AGENTS.md
5. C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update\CLAUDE.md

Create:
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\app

Do not modify:
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update

First implementation scope:
- Webflow Designer Extension shell
- apiVersion 2 webflow.json
- shadcn UI using the same Flow-Goodies `radix-lyra` neutral light/dark style
- no custom marketing theme
- install code screen
- mock package loaded by code DEMO
- package schema/types
- current site/page detection using Designer API
- font checklist from package manifest
- no CMS
- no custom code
- no Hybrid App/OAuth
- no real backend yet

Before editing, state exact files you will create.
Verify with build/test and, if possible, opening in Webflow Designer.
```

---

## 11. Recommendation

Rewrite the first build around this simpler app.

The bigger plan is still useful, but it is too broad for the first step. The right first product is:

```text
Designer Extension inside Webflow
Install code
Package fetch
Font checklist
Designer API asset upload
XscpData patch
Clipboard paste
```

This proves the most important idea: the user installs from inside their own Webflow project, without entering site IDs or Webflow tokens into the marketplace page.
