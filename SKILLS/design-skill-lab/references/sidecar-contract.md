# Sidecar Generation Contract

`.design.md` is the **single source of truth**. Sidecars (`tokens.json`, `tailwind.config.js`) are derivatives — auto-generated, never hand-edited. If a sidecar drifts from its `.design.md`, regenerate; never reconcile by editing the sidecar.

This contract documents:
1. Which `.design.md` frontmatter sections feed which sidecar fields
2. The deterministic transform rules
3. Failure modes (skipped sections, malformed values)
4. The Phase 4.8 emission step

---

## Schema conventions (apply to every `.design.md`)

These conventions exist so the YAML parses consistently across tooling — Python (PyYAML), JS (`js-yaml`), Webflow's eventual ingestion layer, etc. Drift here breaks sidecars silently.

- **Timestamps and dates MUST be wrapped in single quotes.** Example: `interview-conducted-at: '2026-04-25T19:30:00'`. Without quotes, YAML parsers coerce the value to a native `datetime`/`date` object, which is not JSON-serializable and breaks the universal `tokens.json` export. Quoting forces string parsing — predictable across every parser.
- **Hex colours are bare strings, no quotes needed.** YAML treats `#FAFAF7` as a string already (the `#` starts a comment only at line start, and a value on the same line as a key is parsed as scalar).
- **Dimensions with units are bare strings.** `16px`, `1.5rem`, `clamp(72px, 9vw, 144px)` — all parse as strings without quotes. Bare numbers (`16`, no unit) are coerced to ints by YAML; the generator's `coerce_dimension()` handles that fallback, but prefer the explicit unit in source.
- **`fontFamily` values with spaces or commas MUST be quoted.** `fontFamily: 'EB Garamond'` not `fontFamily: EB Garamond` (YAML would parse the latter as a flow sequence under some configurations).

If a future schema field could ambiguously parse as a non-string scalar (number, bool, date, null), wrap it in single quotes. Defensive quoting is cheap; debugging a parser-coercion bug after a build ships is not.

---

## Source of truth: `.design.md` YAML frontmatter

Sidecars are generated from the YAML frontmatter block at the top of any `.design.md` file. The frontmatter is delimited by `---` lines. The expected sections (all optional — generator emits only what's present):

| `.design.md` section | Shape | Emits to |
|---|---|---|
| `colors:` (single-mode) | flat key → hex string | `tokens.json` color tier + `tailwind.config.js` colors |
| `colors.light:` / `colors.dark:` (dual-mode) | nested by mode | `tokens.json` per-mode + `tailwind.config.js` colors with dark variant prefix |
| `typography:` | role → `{fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, textTransform}` | `tokens.json` typography + `tailwind.config.js` `fontSize` (with line-height) + `fontFamily` |
| `rounded:` | tier → px or rem string | `tokens.json` borderRadius + `tailwind.config.js` `borderRadius` |
| `spacing:` | tier → px string | `tokens.json` spacing + `tailwind.config.js` `spacing` |
| `container:` | `{max-width, padding-x}` | `tokens.json` container + `tailwind.config.js` `container` config |
| `motion:` | `{fast, base, reveal, ease-*}` | `tokens.json` motion + `tailwind.config.js` `transitionDuration` + `transitionTimingFunction` |
| `shadows:` | tier → CSS box-shadow string | `tokens.json` shadow + `tailwind.config.js` `boxShadow` |

Sections not listed above are passed through to `tokens.json` under `extras` and ignored by `tailwind.config.js`. New sections can be added without breaking the generator.

---

## Output 1: `tokens.json` (W3C Design Tokens-aligned)

`tokens.json` is the universal, framework-agnostic export. Structure follows the W3C Design Tokens Community Group draft format: each token is `{ "$value": ..., "$type": "color|dimension|fontFamily|..." }`.

Schema:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "color": {
    "light": {
      "bg-page":     { "$value": "#FAFAF7", "$type": "color" },
      "surface-card": { "$value": "#FFFFFF", "$type": "color" },
      ...
    },
    "dark": {
      "bg-page":     { "$value": "#0F0F0E", "$type": "color" },
      ...
    }
  },
  "typography": {
    "display-xl": {
      "fontFamily":    { "$value": "Fraunces",        "$type": "fontFamily" },
      "fontSize":      { "$value": "clamp(72px, 9vw, 144px)", "$type": "dimension" },
      "fontWeight":    { "$value": 600,               "$type": "fontWeight" },
      "lineHeight":    { "$value": 0.95,              "$type": "number" },
      "letterSpacing": { "$value": "-0.03em",         "$type": "dimension" }
    },
    ...
  },
  "borderRadius": {
    "sm": { "$value": "6px",  "$type": "dimension" },
    ...
  },
  "spacing": {
    "xs": { "$value": "4px", "$type": "dimension" },
    ...
  },
  "shadow": {
    "sm": { "$value": "...", "$type": "shadow" },
    ...
  },
  "motion": {
    "fast":          { "$value": "150ms", "$type": "duration" },
    "ease-standard": { "$value": "cubic-bezier(0.4, 0, 0.2, 1)", "$type": "cubicBezier" }
  },
  "container": {
    "max-width":  { "$value": "1440px", "$type": "dimension" },
    "padding-x":  { "$value": "32px",   "$type": "dimension" }
  },
  "extras": { ...passthrough... }
}
```

For single-mode colours (no `light:` / `dark:` sub-blocks), the generator emits `color.default.*` instead of `color.light.*` to avoid implying mode context that doesn't exist.

---

## Output 2: `tailwind.config.js`

Tailwind 3.4+ compatible config, ES module syntax. Emits a `theme.extend` block — the project keeps Tailwind defaults and adds the design-system tokens on top. Use `theme.extend` (not `theme:`) so utilities like `text-sm` keep working.

Template:

```js
/** @type {import('tailwindcss').Config} */
/* AUTO-GENERATED from <relative-path-to-design.md> on <ISO-timestamp>. Do not edit. */
export default {
  content: ['./**/*.{html,js,jsx,ts,tsx}'],
  darkMode: 'class', // or 'media' if .design.md uses prefers-color-scheme only
  theme: {
    extend: {
      colors: {
        // Single-mode: flat keys
        // Dual-mode: light values at root + .dark{} variant via CSS variables
        'bg-page':      'var(--color-bg-page)',
        'surface-card': 'var(--color-surface-card)',
        accent:         'var(--color-accent)',
        ...
      },
      fontFamily: {
        display: ['Fraunces', 'serif'],
        body:    ['Inter', 'sans-serif']
      },
      fontSize: {
        // [size, { lineHeight, letterSpacing, fontWeight }]
        'display-xl': ['clamp(72px, 9vw, 144px)', {
          lineHeight: '0.95',
          letterSpacing: '-0.03em',
          fontWeight: '600'
        }],
        ...
      },
      borderRadius: {
        sm: '6px', md: '10px', lg: '14px', pill: '9999px'
      },
      spacing: {
        xs: '4px', sm: '8px', md: '16px', ...
      },
      boxShadow: {
        sm: '...', md: '...', lg: '...'
      },
      transitionDuration: {
        fast: '150ms', base: '300ms', reveal: '700ms'
      },
      transitionTimingFunction: {
        standard:   'cubic-bezier(0.4, 0, 0.2, 1)',
        'out-expo': 'cubic-bezier(0.16, 1, 0.3, 1)',
        bounce:     'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
      },
      container: {
        center: true,
        padding: '32px',
        screens: { '2xl': '1440px' }
      }
    }
  }
};
```

**Dual-mode strategy:** Tailwind config references CSS custom properties (`var(--color-bg-page)`). The generator emits a companion `tokens.css` block (separate file or appended to existing CSS) defining `:root { --color-*: <light value>; }` and `.dark { --color-*: <dark value>; }`. This keeps Tailwind's `dark:` variants working with CSS-level mode switching.

**Single-mode strategy:** values are inlined directly as hex strings. No CSS variables needed.

---

## Failure modes & how the generator handles them

| Issue | Behaviour |
|---|---|
| `.design.md` has no `---` frontmatter block | Hard error: emit nothing, log to stderr. |
| Frontmatter is malformed YAML | Hard error: emit nothing, log line number. |
| `colors:` missing entirely | Skip color section in both sidecars; warn but don't fail. |
| `colors:` has both flat keys and `light:` / `dark:` sub-blocks | Hard error: ambiguous mode, ask user to pick. |
| Typography token missing `fontFamily` or `fontSize` | Skip that token in `tailwind.config.fontSize`; include partial in `tokens.json`. |
| Hex values in unusual format (`rgb()`, `hsl()`) | Pass through verbatim — W3C tokens spec accepts these. Tailwind accepts them too. |
| Spacing/radius values without units (`16` instead of `16px`) | Coerce to `px`, log warning. |
| Unknown section under frontmatter | Pass through to `tokens.json.extras`, ignore for Tailwind. |

---

## Phase 4.8 emission step

After all Phase 4 audits pass, the skill emits sidecars next to the build artifact, in whichever directory the build was placed:

```
<build-output-dir>/
├── <name>.html
├── <name>.design.md             ← source
├── <name>.tokens.json           ← generated
└── <name>.tailwind.config.js    ← generated
```

Naming rule: sidecars share the basename of the `.design.md`, with their own extension. This keeps multiple builds in the same directory unambiguous.

**Where build artifacts live (NEVER write to project root by default):**
- Production deliverables → wherever the host project organises its outputs (`site/`, `app/`, `dist/`, etc.).
- Skill verification / failure evidence builds → `_tests/<skill-name>/` at the repo root, not in the project root itself.
- One-off explorations → ask the user where to put them; never default to the repo root.

The default for `python3 generate-sidecars.py <path>` is to emit sidecars next to the source. If the source lives in a tests folder, sidecars also live there. Don't override `--out-dir` to push them somewhere else without a reason.

The generator script lives at `references/scripts/generate-sidecars.py` and is invoked via:

```bash
python3 references/scripts/generate-sidecars.py <path-to-design.md>
```

If `python3` isn't available, the agent can read the script and apply its logic manually — but the script is preferred (deterministic, fewer transcription errors).

---

## When NOT to generate sidecars

- The build is a one-off explanation or demo, not a project the user will iterate on.
- The `.design.md` is intentionally exploratory and lacks a stable token system yet.
- The user explicitly says "skip sidecars" — log it in the delivery summary.

For any production-bound build (anything Maria might fork, deploy, or hand off to Webflow/Flowbridge), sidecars are required.
