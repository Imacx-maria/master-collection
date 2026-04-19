# Master Collection Project Context

Last verified: 2026-04-19

## Origin

This project grew out of the Flowbridge converter work.

The old minimal converter/playground is no longer the intended user-facing product. It becomes part of the Master Collection package/preview pipeline.

## Stable Decisions

1. The product name is **Master Collection**.
2. The parent project folder is:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
```

3. The app and site are sibling child projects:

```text
app/
site/
```

4. Documentation and AI_OS live only at the parent root.
5. The app is a Webflow Designer Extension for inside-Webflow installation.
6. The site is the online platform for catalog, previews, auth, checkout, account library, package access, and install codes.
7. Both app and site should use the same simple shadcn/Flow-Goodies visual baseline.

## Relevant Imported Plans

```text
docs/plans/000-master-collection-extension-future-plan.md
docs/plans/001-master-collection-extension-mvp.md
docs/plans/002-master-collection-website-platform.md
```

## Current Product Flow

```text
User browses Master Collection site
User views a template/component page
User signs in with Clerk
User buys through Stripe
Site grants account/library access
Site provides install code
User opens Webflow project
User opens Master Collection app
User pastes install code
App fetches package
App uploads assets and patches XscpData
User installs/pastes into Webflow
```

## UI Baseline

Reference app:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\Flow-Goodies-extension-fg-api-update
```

Use:

- shadcn/ui
- `radix-lyra`
- neutral light/dark mode
- Tailwind v4
- CSS variables
- lucide icons
- compact spacing

No extra marketing design at this planning stage.

