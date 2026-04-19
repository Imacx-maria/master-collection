# Webflow App Research

Last verified: 2026-04-19

This note captures the official Webflow documentation findings that matter for the Master Collection Webflow app. It is intentionally scoped to the first installer MVP.

## Practical Conclusion

The first Master Collection app should be a Webflow App with the Designer Extension capability only.

That is enough for the MVP because the app runs inside the Webflow Designer, can use the client-side Designer APIs, and can call the Master Collection package backend for install-code and package data. A Data Client/OAuth Hybrid App should wait until we need server-side Webflow Data API operations such as CMS import, custom code management, or broader site-data automation.

## What A Designer Extension Is

Official docs describe Designer Extensions as single-page apps running in a secure iframe inside the Webflow Designer. They communicate with the Designer through client-side Designer APIs and can also integrate with backend services or third-party APIs.

Source:

- https://developers.webflow.com/apps/docs/designer-extensions

## Registration Model

When registering a Webflow App, Webflow separates two building blocks:

- Designer Extension: shows an overlay in the Designer and manipulates the Designer/site through Designer APIs.
- Data Client: reads and writes Webflow server data through the Data API with OAuth scopes.

Apps using both are Hybrid Apps. For the MVP installer, use Designer Extension first; add Data Client later only when the feature set requires OAuth scopes.

Sources:

- https://developers.webflow.com/apps/data/docs/register-an-app
- https://developers.webflow.com/data/reference/rest-introduction

## Development And Configuration

Webflow recommends starting Designer Extensions with the Webflow CLI:

```bash
webflow extension init <project-name>
```

The extension manifest is `webflow.json`. Important settings for this project:

- `apiVersion` should be set to `"2"`.
- `size` can be `default`, `comfortable`, or `large`.
- `publicDir` controls the built files served by the extension.
- `appIntents` and `appConnections` are available if the app later needs element connections.

Local extension serving uses:

```bash
webflow extension serve
```

The default local port is `1337`.

Sources:

- https://developers.webflow.com/apps/designer/guides/configuring-your-app
- https://developers.webflow.com/designer/reference/webflow-cli

## Designer API Capabilities Relevant To Master Collection

### Current Site And Page Context

The app can read metadata for the currently open Webflow site with `webflow.getSiteInfo()`, including `siteId`, `siteName`, workspace fields, and domains. It can read the current Designer page with `webflow.getCurrentPage()`.

This supports the product boundary already chosen: the website should not ask buyers for Webflow site IDs or page IDs. The app can discover that context inside Webflow.

Sources:

- https://developers.webflow.com/designer/reference/get-site-info
- https://developers.webflow.com/designer/reference/get-current-page

### Elements

Designer APIs can create, select, manipulate, style, and arrange elements on the canvas. The docs specifically cover selected elements, all elements, programmatic selection, insertion before/after, prepend/append, and bulk creation with `elementBuilder()`.

This is relevant for any future path where Master Collection inserts native element structures directly rather than relying only on clipboard/XscpData handoff.

Sources:

- https://developers.webflow.com/designer/reference/elements-overview
- https://developers.webflow.com/designer/reference/creating-retrieving-elements

### Styles And Classes

The Designer API can create styles, set CSS properties, and apply styles to elements. Webflow styles correspond to Designer classes.

This matters for future native installation paths and for validating whether a package requires class creation versus XscpData paste.

Sources:

- https://developers.webflow.com/designer/reference/styles-overview
- https://developers.webflow.com/designer/reference/style-properties

### Assets

Designer Asset APIs can upload new assets, retrieve existing assets and metadata, update names/alt text, organize folders, and get hosted asset URLs.

This is directly useful for the MVP installer: package image assets can be fetched by the extension and uploaded into the buyer's current Webflow site before patching package data.

Source:

- https://developers.webflow.com/designer/reference/asset-overview

### Pages And Folders

Designer Page APIs provide access to page information and can update page metadata such as name, slug, title, SEO, and Open Graph data. Folder APIs can create and nest folders, but moving pages/folders changes URLs and must be handled carefully.

This is not needed for the first installer MVP except for reading target page context.

Source:

- https://developers.webflow.com/designer/reference/pages-overview

### Components

Designer APIs can register component definitions from an existing root element or create blank component definitions. However, Webflow currently documents that API creation and management of Component Properties is not yet supported.

This means component-property-heavy package automation should be treated as a later research area, not an MVP assumption.

Source:

- https://developers.webflow.com/designer/reference/components-overview

### User Capabilities And App Modes

`webflow.canForAppMode()` can check whether the current user/app mode has the needed Designer abilities. The app should use this before actions that require Designer access and show clear guidance when the user is in a mode that cannot perform the install step.

Source:

- https://developers.webflow.com/designer/reference/get-users-designer-capabilities

## Data API And Hybrid App Boundary

The Data API is a REST API for Webflow server resources. It is the right path for CMS items, forms, localization, custom code, webhooks, and server-side site management. A broad public app should use OAuth through a Data Client instead of asking buyers for site tokens.

For Master Collection:

- MVP: Designer Extension plus Master Collection backend.
- Later Hybrid App: add Data Client/OAuth when CMS import, custom code, or server-side Webflow site automation becomes part of the product.
- Avoid: asking website buyers to paste Webflow site tokens or site IDs into the Master Collection website.

Sources:

- https://developers.webflow.com/data/reference/rest-introduction
- https://developers.webflow.com/apps/data/docs/register-an-app
- https://developers.webflow.com/data/v1.0.0/docs/get-a-site-token

## MVP Implications

1. Keep the app scoped to install-code redemption, package fetch, font checklist, asset upload, XscpData patching, and clipboard/install handoff.
2. Use Designer APIs for current site/page context and asset uploads.
3. Do not add OAuth/Data Client until a real feature requires Webflow Data API scopes.
4. Do not assume custom fonts can be installed automatically in MVP. Keep missing font installation as user-guided preparation unless a later docs check proves a complete supported path.
5. Check Designer capabilities at app launch and before install actions.
6. Build with Webflow CLI conventions so local testing works through the Webflow Designer.
