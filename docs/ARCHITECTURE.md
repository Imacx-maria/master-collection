# Master Collection Architecture

Last verified: 2026-04-19

## System Shape

Master Collection has one parent project and two child surfaces:

```text
MASTER-COLLECTION/
  site/  public/account website
  app/   Webflow Designer Extension
```

Both children share one parent documentation layer:

```text
docs/
AI_OS/
```

## Product Boundary

The website is the storefront, account, and package-access surface.

The app is the inside-Webflow installer.

The website and app communicate through install codes and package APIs. They should not duplicate responsibilities.

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

## Future Expansion

Future work may add:

- Hybrid App/Data API path
- CMS import and mapping
- custom-code installation
- admin product/package management
- second payment gateway
- bundle/full-collection purchase model

Do not pull future work into the MVP without explicit approval.

