# Master Collection

Master Collection is the parent workspace for two connected product surfaces:

- `site/` - the website/platform for catalog, previews, auth, checkout, account library, install codes, and package access.
- `app/` - the Webflow Designer Extension that runs inside Webflow and installs purchased packages into the buyer's current site/page.

## Git Layout

This parent repository maps to:

```text
https://github.com/Imacx-maria/master-collection.git
```

It owns the shared documentation, AI_OS, and the `site/` application. The `app/` folder is intentionally ignored here because it is an independent repository:

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

Then read the child guidance for the folder you are touching:

```text
app/AGENTS.md
site/AGENTS.md
```
