# Master Collection Architecture

Last verified: 2026-04-25

## System Shape

Master Collection has one parent project and three child surfaces:

```text
MASTER-COLLECTION/
  site/              public/account website
  app/               Webflow Designer Extension
  chrome-extension/  Chrome extension companion
```

All children share one parent documentation layer:

```text
docs/
AI_OS/
```

## Product Boundary

The website is the storefront, account, and package-access surface.

The app is the inside-Webflow installer.

The Chrome extension is the browser companion for Webflow Designer utilities that are better handled by a browser extension than by the inside-Webflow app.

The website, app, and Chrome extension should not duplicate responsibilities.

## Website Responsibilities

The website owns:

- public catalog
- product pages
- template/component preview pages
- Clerk authentication
- Stripe Checkout
- account library
- purchase entitlements
- install-code creation
- package access endpoints
- install event history

The website should not ask a buyer for Webflow site ID, page ID, or API token.

## App Responsibilities

The Webflow app owns:

- running inside Webflow Designer
- detecting current Webflow site/page
- showing font preparation guidance
- uploading package images/assets to the current Webflow site
- patching XscpData with target page and asset IDs
- copying/pasting/installing into Webflow

## Chrome Extension Responsibilities

The Chrome extension owns:

- running as a Manifest V3 Chrome extension on Webflow Designer URLs
- Paste Guard browser interception
- interaction cleanup tooling
- a compact popup UI aligned with the Master Collection app visual baseline

The Chrome extension should not own checkout, account access, package APIs, or the inside-Webflow install flow.

## Package Flow

```text
Designer creates source in Webflow
Flowbridge/pre-treatment/package generator prepares MasterCollectionPackage
Master Collection site stores package and preview
Buyer purchases through site
Site grants entitlement and install code
Buyer opens Master Collection app inside Webflow
App redeems install code
App fetches package and assets
App uploads assets to buyer's Webflow site
App patches XscpData
Chrome extension can assist with browser-side paste safety when installed
Buyer installs/pastes into current Webflow page
```

## Current MVP Cut

App MVP:

- Designer Extension only
- install code or mock code
- package fetch/mock package
- current site/page detection
- font checklist
- image upload with Designer API
- XscpData patch
- clipboard paste

Site MVP:

- catalog
- preview pages
- Clerk auth
- Stripe one-time checkout
- account library
- install codes
- package API for the app

Chrome extension MVP:

- Manifest V3 copied into `chrome-extension/`
- Master Collection Companion branding
- compact neutral popup UI
- system light/dark detection with small override
- Paste Guard and interaction tooling preserved from the source extension

## Future Expansion

Future work may add:

- Hybrid App/Data API path
- CMS import and mapping
- custom-code installation
- admin product/package management
- second payment gateway
- bundle/full-collection purchase model

Do not pull future work into the MVP without explicit approval.
