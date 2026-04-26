# AGENTS.md - Master Collection Chrome Extension

## Scope

This folder is the Master Collection Chrome extension companion for Webflow Designer.

It is a child of:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION
```

The Chrome extension is not the website and is not the Webflow Designer Extension app. It provides browser-side companion utilities for Webflow Designer, including Paste Guard and interaction tooling.

## Start Here

1. Read `../AI.md`.
2. Read `../AGENTS.md`.
3. Read `../docs/ARCHITECTURE.md`.

## UI

Use the same simple neutral baseline as the Master Collection app:

- compact layout
- neutral light/dark variables
- no decorative marketing theme
- no purple/blue branded palette
- detect system light/dark by default
- allow only a small theme override control when useful

## Extension Rules

- Keep Manifest V3.
- User/tester installation instructions live in `docs/INSTALL.md`.
- Official Chrome Web Store publishing requirements live in `docs/CHROME-WEB-STORE-PUBLISHING.md`.
- Do not modify the original source extension at:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\webflow-ix-cleaner
```

- Work in this copied folder only.
- Keep content-script behavior scoped to Webflow Designer URLs.
