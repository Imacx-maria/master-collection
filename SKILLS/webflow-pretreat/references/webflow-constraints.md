# Webflow Platform Constraints

What Webflow paste, Designer, and the minimal converter require from the pre-treated HTML. Load this file when reasoning about HEAD migration, embed routing, style/script extraction, the custom-code host contract, or IX3 capability gaps.

---

## Webflow Paste Behavior

Pasted XscpData becomes children of Webflow's body wrapper. The current minimal converter maps HTML elements to node types (DivBlock, TextBlock, HtmlEmbed, etc.) and class-based CSS to `styleLess` properties. Custom code embeds (`div.w-embed`) become `HtmlEmbed` nodes that preserve arbitrary HTML/CSS/JS. Image upload/relinking belongs to the minimal converter because it uses the user's Webflow token and target site.

## CSS Ancestry — Why Wrapper Placement Matters

Adding a wrapper div changes the CSS ancestry chain:

- **`overflow: clip` on a parent** — creates a containing block; `position: fixed` children lose viewport reference and get clipped
- **`overflow: hidden` on a parent** — creates a scroll container; breaks `position: sticky` on children
- **`transform`, `filter`, `perspective`, `will-change` on ancestor** — creates new containing block for `position: fixed` descendants
- **`z-index`** — only works within stacking contexts; wrapping can change stacking context boundaries
- **`position: sticky`** — depends on nearest scrollable ancestor being correct

When you move elements inside a wrapper, think about these relationships. Understand the original layout's containment model before changing anything.

## Head Custom Code — Must Be Migrated

The converter strips `<head>` entirely. Any custom code the Webflow author added via Project Settings → Custom Code → Head Code will be **lost** unless you migrate it into the body.

**For each page's `<head>`, identify and migrate:**

- **External CSS `<link>` tags** (e.g., Splide CSS CDN, Lottie CSS, custom font CDNs) → move into their own named embed in the body (e.g., `fb-styles-splide`). **When possible, fetch the CSS content and inline it as `<style>` instead of keeping it as a `<link>`.** Webflow's paste path may not process `<link>` tags inside HTML embeds. If the CSS content is available in the export (cached or bundled), inline it. If only a CDN URL is available and the content can't be fetched, keep the `<link>` as fallback but note this may not render after paste.
- **Custom `<style>` blocks** → read the rules, understand what library or purpose they serve, group them into appropriately named embeds (e.g., Splide overrides → `fb-styles-splide`, Lenis overrides → `fb-styles-lenis`)
- **Custom `<script>` tags** → move into FB Scripts embed (respect dependency order)

**Standard Webflow head elements to IGNORE as custom code** (these are handled by explicit rules, not migrated as arbitrary author code):

- `<meta charset>`, `<meta viewport>`, `<title>`, `<meta name="generator">`
- Open Graph / Twitter Card meta tags
- Baseline CSS links (`normalize.css`, `webflow.css`) — do NOT inline the full files, but also do NOT rely on their HEAD links as evidence. The output HEAD must contain zero local `css/*.css` links; the minimum converter-visible baseline lives in `fb-styles-site` per L-4.
- Favicon, apple-touch-icon links
- The `w-mod-js`/`w-mod-touch` inline script

**Exception:** Under L-1 (Option B, locked 2026-04-17), the HEAD inline `<style>` containing the full inlined site CSS — including its `@font-face` blocks, `:root` variables, class rules, `@keyframes`, and native `@media` blocks — IS the canonical location. It is not "custom head code that must be migrated" — it is skill-authored inline site CSS and stays in HEAD. The original `<link rel="stylesheet" href="css/[sitename].webflow.css">` is REMOVED from HEAD and the referenced CSS file is DELETED from the output ZIP. Single source of truth — no drift between HEAD inline and any disk copy. See `lessons.md` L-1 and `SKILL.md` Input/Output Contracts.

---

## Inlining CSS and JS for the Converter

The current minimal converter extracts CSS from `<style>` blocks inside the HTML. It does **NOT** read external files referenced via `<link>` or `<script src>`. You must inline the site CSS, preserve inline `Webflow.push(...)` animation-data init scripts, and preserve the export's `<script src="js/webflow.js">` reference verbatim in the paste artifact per L-19 (narrowed 2026-04-18 EXP-008: never INLINE webflow.js content; external src passes through).

### Inline the site CSS

Read the site-specific CSS file from `css/` — the one named `[sitename].webflow.[hash].css` or `[sitename].webflow.css` (NOT `normalize.css`, NOT `webflow.css`). Inject its full content as a `<style>` block in the `<head>`.

- `normalize.css` and `webflow.css` are Webflow baselines. Do NOT inline the full files and do NOT keep their local HEAD links as a preview crutch. The converter/paste path does not use those HEAD links as an active styling source, so L-4 requires the minimum baseline floor in `fb-styles-site`; SV-5/L-1.3 require zero local `css/*.css` links in output HEAD.
- **Remove the `<link>` to the site CSS file AND delete the site CSS file from the output ZIP** (L-1 Option B, step 5). The inlined HEAD `<style>` replaces the linked file completely. Keeping both creates two sources of truth and invites drift — the skill forbids this. The HEAD inline `<style>` is what the browser renders for visual verification; no link is needed for that to work.
- **Rewrite relative URLs after inlining.** CSS files in Webflow exports sit in `css/` and reference assets as `../images/...`, `../fonts/...`, etc. Once the CSS content is inlined into `index.html` at the root, those `../` prefixes resolve incorrectly. After inlining, rewrite ALL `url()` values in the inlined CSS: strip the leading `../` from relative paths (e.g., `url('../images/foo.jpg')` → `url('images/foo.jpg')`). Do not touch absolute URLs, data URIs, or fragment references. The source CSS file is deleted after inlining, so no second rewrite pass against the file is needed.
- The converter extracts CSS from body-level `w-embed` `<style>` blocks (`fb-styles-site`, `fb-media-site`, etc.). The HEAD inline `<style>` is preview-only — it serves browser rendering of the pre-treated HTML for visual verification but is not piped through the converter to Webflow paste.

### Webflow runtime output modes; never inline its content

Never inline `js/webflow.js` content. The 071 crash (`TypeError: t is not a function at r.define`) was caused by INLINING the full module registry as an IIFE, which runs at parse time and collides with the publisher's CDN runtime. An external `<script src>` reference does not crash in the local-preview posture (EXP-008 PASS on the inline-IIFE crash mechanism, 2026-04-18 — Maria manual paste + publish verified clean).

**Mode A / local-preview placement (L-15 Addendum, 2026-04-18 EXP-009):** the external `<script src="js/webflow.js">` is NOT inside `fb-scripts` inside `fb-custom-code` — that early placement fails IX2 hydration because the runtime boots before source content parses (audit-082 regression on MNZ). Emit the external reference inside a `fb-runtime.w-embed` host that is a direct child of `fb-page-wrapper`, positioned AFTER all source-content siblings. SV-13-B in `verification-gate.md` enforces the late-placement structurally. See `docs/LESSONS.md` L-15 Addendum for the three-class partition and the `fb-runtime` host shape.

- `local-preview` `index.html`: exactly one `<script src="js/webflow.js">` reference, emitted inside `fb-runtime.w-embed` as a direct child of `fb-page-wrapper` AFTER source-content siblings (L-15 Addendum — external runtime is the one carve-out from L-15 uniform wrapping); zero inlined webflow.js module IIFE (`grep -c 'var e={1361:' index.html` → 0).
- No separate preview artifact is emitted for local-preview mode.
- `webflow-paste` mode is different: suppress `fb-runtime` and every relative `js/webflow.js` reference, preserve `data-w-id`, and neutralize IX-shaped source `style=""` attributes before converter transport when output IX data will be empty. This static-visible contract is enforced by SV-18 / `scripts/paste_contract_probe.py`, which writes or validates `pretreat-manifest.json`. Do not claim animation parity from this mode.
- Inline `Webflow.push(...)` animation-data scripts from the export must still be preserved and wrapped/gated in `fb-scripts` inside `fb-custom-code` (L-16 dep-gate runner where runtime globals are referenced).
- Keep jQuery as an external CDN `<script src>` inside `fb-scripts` inside `fb-custom-code` — it must load from CDN at runtime; stays in the standard L-15 uniform-wrap destination.

Do not reinterpret Webflow readiness guards as authored final styles. Selectors containing `w-mod-js`, `w-mod-ix2`, `w-mod-ix3`, or `:not(.w-mod-ix*)` describe a runtime transition boundary. They can be preserved for `local-preview` when `js/webflow.js` is present and late, but in runtime-free `webflow-paste` they must be converted to static-visible safety or treated as a halt condition.

### What NOT to inline

| File | Why not |
|------|---------|
| `normalize.css` | Full Webflow baseline — too broad to inline; emit only the L-4 baseline floor in `fb-styles-site` and remove the local HEAD link |
| `webflow.css` | Full Webflow baseline — too broad to inline; emit only the L-4 baseline floor in `fb-styles-site` and remove the local HEAD link |
| jQuery CDN | External URL, must load from CDN at runtime |
| Library CDNs (Splide, Lenis, etc.) | Already handled via FB Scripts embed |

---

## What Must Be Extracted Into Embeds

The converter handles class-based CSS rules. Everything else must be routed into a custom code embed. You need to identify and extract:

**Into the FB Styles embed (`<style>` block):**

- `:root { --... }` CSS custom property definitions from the source site CSS — **MUST be placed at the very TOP of the `<style>` content, before any other rules.** Without `:root` variables, all `var()` references resolve to empty and text becomes transparent/invisible. Also check `body {}` and `html {}` for variable definitions — some sites define custom properties there instead of `:root`.

### Webflow Baseline Tag Resets

Webflow's baseline stylesheets (`normalize.css` and `webflow.css`) provide critical geometry and tag-level resets that every Webflow export relies on. The skill correctly treats them as Webflow baselines, not site-specific CSS, but converted local preview and pasted HtmlEmbed CSS do NOT get those resets for free after the source HEAD links are removed or ignored by the converter path. Elements revert to browser defaults unless the skill supplies the minimum baseline surface.

When building the `fb-styles-site` compensation CSS, ALWAYS include this essential baseline floor:

```css
/* Webflow baseline floor — pasted content/local preview doesn't inherit these */
html { height: 100%; }
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; min-height: 100%; }
a { color: inherit; text-decoration: inherit; }
img { max-width: 100%; vertical-align: middle; display: inline-block; }
```

**Why these are necessary:**

- Without `body { margin: 0; }`, browser default `8px` body margin shifts every full-bleed Webflow export. Codex BigBuns and Srta Colombia audits both showed content starting at `x=8/y=8`, nav/menu geometry drifting, and section rhythm changing.
- Without global border-box sizing, Webflow layouts that assume `box-sizing: border-box` gain width from padding/borders. BigBuns nav widths drifted by 16px+ across breakpoints when this reset was absent.
- Without `html` height and `body` min-height, percentage-height chains from Webflow's normalize surface can collapse or compute against the wrong ancestor.
- Without the `a` reset, ALL `<a>` elements render as blue underlined text (browser default). This destroys nav links, footer links, card links, and any styled anchor.
- Without the `img` reset, images can overflow containers and have vertical alignment gaps.

**What NOT to include:**

- Full `normalize.css` / `webflow.css` dumps. They are too broad and can conflict with source site CSS.
- Webflow body typography/color defaults such as `font-family: Arial`, `font-size: 14px`, `line-height: 20px`, or `color: #333` unless a specific fixture proves the site lacks its own body/text rules. The geometric `body` reset above (`margin` / `min-height`) is mandatory; typography defaults are not.
- `h1-h6`, `p`, `ul/ol` resets from `webflow.css` by default — the site-specific CSS almost always overrides these. Including them would duplicate or conflict with the site's own tag selectors.
- Only include resets for tags where the browser default is visually destructive AND the site CSS does not provide its own override.

**Placement in the `fb-styles-site` `<style>` block:** After `:root` CSS variables, before extracted tag selectors from the site CSS. The site's own tag rules (like `body { color: var(--black); }`) should come after and naturally override any baseline values they redefine.

**Detection rule:** Geometry baseline is unconditional: include `html`, global `box-sizing`, and `body` margin/min-height. For non-geometric `a` and `img` resets, check if the site's CSS already defines an equivalent rule. If the site CSS has `a { color: ... }`, don't add the inherited `a` reset; the site's rule is more specific and correct.

### Other extractables to FB Styles embed

- Tag selectors — `h1 { }`, `body { }`, `html { }`, `* { }`, `p { }`, etc.
- Webflow state class combos — `.w--current`, `.w--open`, `.w--tab-active` and rules targeting them
- Pseudo-elements — `::before`, `::after`, `::placeholder`
- `@keyframes` blocks
- Non-breakpoint `@media` queries (see `lessons.md` L-2 for routing into `fb-media-site`)
- `@container`, `@supports`, `@layer` rules
- Body-level CSS — `-webkit-font-smoothing`, `text-rendering`, `scroll-behavior`, etc.

**NEVER extract into embeds:**

- `@font-face` rules — **crashes Webflow Designer** when placed inside a `w-embed` `<style>` block. See `lessons.md` L-1 for the correct placement.

---

## FlowBridge Custom-Code Host Contract

Use a **single** `div.fb-custom-code` as the host for all FlowBridge-owned embeds. Place it at the very top of the wrapper, before any visible content. One container — styles first, then scripts.

Do not rename these to `custom-code`, `fb-styles`, or `fb-scripts` host classes. The converter must preserve these source classes as real Webflow class records, including empty `styleLess` marker classes.

```html
<div class="fb-custom-code" style="display:none">
  <div class="fb-styles-site w-embed">
    <style>/* tag selectors, @keyframes, body CSS, state combos */</style>
  </div>

  <!-- Library-specific CSS (migrated from head) — one embed per library -->
  <div class="fb-styles-splide w-embed">
    <link rel="stylesheet" href="https://cdn.example.com/splide.min.css">
    <style>/* splide overrides from head */</style>
  </div>

  <div class="fb-styles-lenis w-embed">
    <style>/* lenis overrides from head */</style>
  </div>

  <!-- Author's original style embed (if present in the export) is absorbed here -->
  <div class="styles w-embed">
    <style>/* author's body-level / responsive styles */</style>
  </div>

  <div class="fb-scripts w-embed">
    <!-- library CDNs, gated init scripts, author scripts -->
  </div>
</div>
```

**Rules:**

- `div.fb-custom-code` must have `style="display:none"` — it's invisible infrastructure, not page content
- Every embed MUST have the `w-embed` class (converter needs it to create HtmlEmbed nodes)
- Name embeds semantically: `fb-styles-site`, `fb-styles-splide`, `fb-styles-lenis`, `fb-scripts`, etc.
- Don't create empty embeds — only what the site actually needs
- The single host goes near the top of the wrapper before page content
- Any `div.w-embed` from the export that was a body-level sibling (e.g. `div.styles.w-embed`) is absorbed INTO `fb-custom-code` — it must not be a free sibling of `fb-custom-code` in the wrapper
- Inline init scripts inside `fb-scripts` use the dependency-gated runner (see `lessons.md` Script Handling) to handle ordering regardless of DOM position

---

## IX2/IX3 Exceptions — Animations That Need Code Embeds

> **Full reference:** `docs/research/IX3-CAPABILITIES-AND-LIMITS.md`

The general rule is: every interaction Webflow can represent natively should land in the IX2/IX3 Interactions panel, where it remains editable in Designer. Do not generate GSAP/custom code for native-capable interactions.

But IX2/IX3 have capability gaps. These animation types have no native panel equivalent and are legitimate custom-code exceptions:

| Animation Type | Why IX2/IX3 Can't Do It |
|----------------|---------------------|
| **MOUSE_MOVE / cursor tracking** | No native cursor-follow trigger exists in the interactions panels |
| **Number counters (text content animation)** | Webflow interactions animate CSS properties, not `textContent`. No `onUpdate` callback. |
| **GSAP Flip (layout state capture)** | Requires runtime DOM measurement — native interaction values are static |
| **ScrollTrigger pin** | `pin: true` not exposed in the Interactions Visual Builder |
| **Dynamic per-element values** | Native interaction values are static; they can't compute from element index or position |
| **Lottie frame sync** | Native interactions can trigger Lottie playback but can't sync frame progress with arbitrary timing |
| **Infinite marquee (modular wrapping)** | No `modifiers` plugin equivalent. Prefer CSS `@keyframes` instead. |
| **Callbacks (onComplete, onStart, onUpdate)** | IX2/IX3 have no callback mechanism for running arbitrary JavaScript |

### What This Means for Pre-Treatment (reframed 2026-04-19 EXP-019)

**Pipeline boundary.** Pre-treatment is the AI reasoning pass over the raw Webflow export ZIP. The later converter/Webflow stage owns IX2-to-IX3 and IX3-to-IX3 behavior conversion. Pre-treatment preserves source-shipped libraries and retained source inline init bodies as source evidence (L-9, `docs/LESSONS.md`). **The IX2/IX3-impossibility capability table above is research/observational reference for the downstream converter/Webflow stage — it does NOT gate preservation of source-shipped GSAP-family libraries or their source inline init bodies during pre-treatment.**

**Observational scan — useful metadata for the converter, not a pre-treatment strip trigger.**

When the skill reads the export runtime/data surfaces, it may log which IX2/IX3-impossible signatures appear — this is research metadata the downstream converter/Webflow stage can use when deciding how to map source behavior to native panels. The scan is informational; a negative scan result (no IX2/IX3-impossible pattern matched) does NOT authorize removing any source-shipped GSAP-family script. Patterns to scan for:

| Pattern to scan for | IX2/IX3-impossible type |
|---|---|
| `"MOUSE_MOVE"` or `"mousemove"` in IX2 action data | Cursor tracking / mouse follow |
| `onUpdate` callback with `textContent` or `innerHTML` assignment | Number counter |
| `gsap.set(` or `gsap.to(` referencing `e.clientX` / `e.clientY` / `e.pageX` | Mouse follow (author GSAP) |
| `ScrollTrigger` with `pin: true` | ScrollTrigger pin |
| `Flip.getState` / `Flip.from` | GSAP Flip |
| `gsap.utils.toArray` with per-index computed values | Dynamic per-element values |

**Pre-treatment procedure — preservation, not stripping:**

1. **Preserve every source-shipped GSAP-family CDN `<script src>`.** Any `src` matching `gsap`, `greensock`, `ScrollTrigger`, `ScrollSmoother`, `DrawSVG`, `MorphSVG`, `SplitText`, `Flip`, or a future GSAP-family library is preserved inside `fb-scripts.w-embed` in source order per L-15. Do NOT strip based on whether the observational scan found matching IX2/IX3-impossible signatures or not.
2. **Preserve every source-shipped inline init body** associated with GSAP-family libraries (GSAP timelines, SplitText instantiations, ScrollTrigger registrations, Flip animations, etc.). Place it in `fb-scripts.w-embed` in source order after its CDN. If it references runtime globals, wrap it per L-16 with every referenced global in `need[]`; if it immediately targets source DOM selectors, classify them as required or optional and require DOM-parsed plus required selector presence before `fbRun`. Do NOT delete source inline init bodies on the theory that the resulting interaction "could be" re-expressed in Webflow's IX2/IX3 panels.
3. **Record moves in the Mandatory Output Manifest.** When a source library or inline body is relocated, the manifest row L-9 records the original location, new host, source-order index, and dependency reason (which globals the host owns, which retained inline body consumes them). See `SKILL.md §Mandatory Output Manifest — Before You Zip`.
4. **HALT on documented incompatibility; never silently strip.** If a specific source library cannot be preserved safely because of a named, documented concrete pre-treatment/converter incompatibility, the skill writes `HALT-REPORT.md` with the incompatibility evidence and stops. Preservation is the default; removal requires a written justification that another experiment can challenge.
5. **Generate-new ≠ preserve-source-shipped.** SKILL.md Hard Rule #3 continues to ban synthesizing NEW GSAP or custom JavaScript for interactions Webflow can represent in IX2/IX3 panels. L-9's scope is preservation of what the source export already ships; Hard Rule #3's scope is the authoring ban. They are complementary and do not override each other.

IX2/IX3-possible and IX2/IX3-impossible classifications are decisions the converter/Webflow stage makes against the preserved source evidence. Pre-treatment's job is to hand that stage faithful markup plus the observational scan log — not to pre-delete source code that the stage may still need.

### Common Confusion: Sliding Numbers vs Counting Numbers

- **Numbers that SLIDE in/out** (e.g., "01" moves via `y` transform on hover) — this IS native IX3. The text never changes, only its position. Fix is in the converter's IX2→IX3 conversion, not in Code Embeds.
- **Numbers that COUNT** (e.g., "0" counts up to "1,247" frame by frame) — this is NOT IX3. Requires `onUpdate` callback + `textContent` manipulation. Must be Code Embed.

**If the number text changes → Code Embed. If the number element moves → IX3 native.**

---

## Webflow Native Element Markers (Preserve Exactly)

The converter needs these HTML markers to assign correct Webflow node types. The skill must NEVER strip, rename, or restructure elements with these classes.

**Layout:**

- `w-layout-grid` → Grid node. Always paired with user classes (e.g., `w-layout-grid three-col-grid`).

**Tabs:**

- `w-tabs` → TabsWrapper
- `w-tab-menu` → TabsMenu
- `w-tab-link` → TabsLink (often also has `w-inline-block`)
- `w-tab-content` → TabsContent
- `w-tab-pane` → TabsPane

**Slider:**

- `w-slider` → SliderWrapper
- `w-slider-mask` → SliderMask
- `w-slide` → SliderSlide
- `w-slider-arrow-left`, `w-slider-arrow-right` → SliderArrow
- `w-slider-nav` → SliderNav

**Navbar:**

- `w-nav` → NavbarWrapper
- `w-nav-brand` → NavbarBrand
- `w-nav-menu` → NavbarMenu
- `w-nav-link` → NavbarLink
- `w-nav-button` → NavbarButton

**Dropdown:**

- `w-dropdown` → DropdownWrapper
- `w-dropdown-toggle` → DropdownToggle
- `w-dropdown-list` → DropdownList

**Forms:**

- `w-form` → FormWrapper
- `w-input`, `w-select`, `w-checkbox`, `w-radio` → Form field types

**Other:**

- `w-embed` → HtmlEmbed
- `w-inline-block` → Link Block
- `w-container` → BlockContainer
- `w-lightbox` → LightboxWrapper
- `w-background-video` → BackgroundVideoWrapper
- `w-richtext` → Rich Text container
- `w-dyn-list`, `w-dyn-item` → CMS Collection List

**State/modifier classes (preserve, don't treat as structural):**

- `w--current`, `w--tab-active`, `w--open` — component state classes
- `w-mod-js`, `w-mod-ix` — body modifier classes
- `w-round`, `w-num` — slider nav styling

**Grid placement IDs:**

- `w-node-*` pattern in element IDs — Webflow auto-generated grid area placement. Preserve the `id` attribute.

Not all exports will have all of these. MNZ Creative uses: `w-layout-grid`, full Tabs family, full Slider family, `w-embed`, `w-inline-block`. It does NOT use: native Navbar, Dropdown, Forms, CMS, Lightbox, Container.
