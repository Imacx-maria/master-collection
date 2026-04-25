# Master Collection

Master Collection is the parent workspace for three connected product surfaces:

- `site/` - the website/platform for catalog, previews, auth, checkout, account library, install codes, and package access.
- `app/` - the Webflow Designer Extension that runs inside Webflow and installs purchased packages into the buyer's current site/page.
- `chrome-extension/` - the Chrome extension companion for Webflow Designer browser-side utilities.

## Git Layout

This parent repository maps to:

```text
https://github.com/Imacx-maria/master-collection.git
```

It owns the shared documentation, AI_OS, and the `site/` application. The local `app/` folder is intentionally ignored here because it is an independent repository:

```text
https://github.com/Imacx-maria/master-collection-app.git
```

For Vercel, connect the `master-collection` repository and set the project root directory to `site/` after the site runtime is scaffolded.

## Start Here

Read these files before implementation:

```text
AI.md
AGENTS.md
docs/DOCS_INDEX.md
docs/ARCHITECTURE.md
```

Then read the child guidance for the folder you are touching. The `site/` and `chrome-extension/` guidance are tracked in this repository; the `app/` guidance is tracked in the separate app repository and appears locally when that repo is checked out at `app/`.

```text
app/AGENTS.md
site/AGENTS.md
chrome-extension/AGENTS.md
```
