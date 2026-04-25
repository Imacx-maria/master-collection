# Mechanical Consultation Reference

Use this reference when a pre-treatment run needs deterministic evidence before the AI skill makes a site-aware decision. This file is a consultation layer, not a mechanical pre-treatment runner.

## Boundary

The skill remains the operator. It reads the site, chooses the output mode, edits the extracted export, and writes the manifest. Mechanical knowledge may provide inventories, classifiers, and checks. It must not make final site-specific decisions by itself.

Do not run `src/pre-treatment/` as the active path. The archived mechanical skill shipped two anti-lessons on MNZ:

- global `.bg-whipe` / reveal-overlay collapse;
- blanket IX2 transform / opacity / zero-size stripping.

Those are banned as transformations. The old code can be read for narrow reference only, especially `@media` classification, baseline CSS floor history, and script/CSS inventory patterns.

## Output Modes

Every run should know which artifact it is producing.

| Mode | Purpose | Runtime | IX inline states | Claim |
|---|---|---|---|---|
| `local-preview` | Browser verification of the pretreated export before converter transport | keep late `fb-runtime.w-embed` with external `js/webflow.js` | preserve by L-8 unless another L-rule narrowly applies | source-runtime preview |
| `webflow-paste` | Static-visible Webflow paste when converter output IX data will be empty | suppress `fb-runtime` and relative `js/webflow.js` | remove IX-shaped source `style=""` attributes before converter xattr serialization, but first transport the equivalent initial visual state into `fb-styles-site` CSS keyed by stable selectors; library visibility fallbacks must target source-present roots/children, not runtime-added state classes | static-visible only |

There is no silent default. Every run must declare exactly one mode before transformation starts. A request such as "fresh ZIP", "current-skill ZIP", or "regenerate the artifact" is ambiguous until the downstream use is stated.

A `local-preview` artifact is not paste-safe input by implication; using it as paste input requires an explicit converter mode that preserves or reconstructs the runtime/IX clearing mechanism. The current minimal converter emits empty IX data, so any run intended for `minimal-converter-4-1.html`, Webflow Designer paste, or published Webflow verification must declare `webflow-paste`. Reserve `local-preview` for explicit preview-only / browser-runtime diagnostics or another explicitly declared runtime-aware downstream lane.

`webflow-paste` artifacts must be static-visible before conversion.

Do not claim animation parity from `webflow-paste` mode. IX2/IX3 reconstruction belongs to a later interaction lane.

For both modes, `fb-styles-site` is the converter-visible source of site CSS. The HEAD inline `<style>` exists for browser preview only and is not transported by the converter. In Mode B, do not route source site class/layout CSS to HEAD only. The same non-font source site class selectors that local-preview carries in `fb-styles-site` must be present in the Mode B `fb-styles-site` embed.

## Safe Mechanical Probes

These probes return facts. The skill decides what to do with the facts. The active probe entry point is `scripts/paste_contract_probe.py`.

| Probe | Reads | Reports | Use |
|---|---|---|---|
| CSS surface classifier | source CSS and embeds | class rules, tag rules, native vs non-native `@media`, `@font-face`, unsupported at-rules | decide HtmlEmbed vs future styleLess promotion |
| Converter-visible site CSS parity | source site CSS + output `fb-styles-site` | source non-baseline site class selector count, output `fb-styles-site` class selector count, missing selector samples | fail Mode B when local preview is styled by HEAD-only CSS that the converter will not transport |
| Webflow baseline/native floor | source DOM + `webflow.css` presence | required baseline resets and native component base rules | ensure `fb-styles-site` carries paste-visible baseline CSS |
| Runtime surface inventory | source/output HTML | `fb-runtime`, `js/webflow.js`, inline module-IIFE signatures | enforce mode-specific runtime contract |
| IX marker inventory | source/output HTML | `data-w-id` count and locations | preserve source interaction evidence |
| IX inline style-attribute inventory | source/output HTML | IX-shaped `style=""` attrs, fully IX-only vs mixed structural+IX | prevent converter `node.data.xattr` from re-emitting frozen states |
| Font URL inventory | CSS/HtmlEmbed surfaces | relative `.woff`, `.woff2`, `.ttf`, `.otf`, `.eot` URLs | warn on paste/publish font risk |
| Script dependency/selector inventory | retained inline scripts | globals, required selectors, optional selectors | support L-16 readiness decisions |
| Static-visible library fallback inventory | `fb-styles-[library]` embeds | root/inner source-present fallback selectors vs runtime-state-only selectors | fail Mode B when visibility depends on classes added by JS hydration |
| Asset reference inventory | HTML attrs and CSS `url(...)` | local refs, source-premise broken refs, skill-introduced broken refs | support L-18 |
| Reserved Webflow class inventory | source CSS/HTML | `w-*`, `w--*`, `_w-*` selector/class surfaces | inform paste-side alias research, not auto-rewrite |

## IX Inline Style-Attribute Probe

This probe is separate from generic IX inventory because audit 147 proved the freeze can survive through raw source `style=""` attributes even when generated `styleLess` is clean. If the HTML still carries IX-shaped inline style attrs, the converter may serialize them as `node.data.xattr[{name:"style"}]` and Webflow will faithfully publish them.

Classify each source-content element with a `style` attribute:

- `ix-only`: declarations are only Webflow IX starts, such as vendor transform quadruple chains, freeze-only `opacity: 0`, or zero width/height start states.
- `mixed`: declarations include both IX starts and structural author styles.
- `structural`: declarations are non-IX, such as `display:none` on `fb-custom-code`.

Mode B requires source-level neutralization plus equivalent transport before conversion:

- copy each required IX initial-state declaration into a converter-visible `fb-styles-site` CSS rule before removing it from the element;
- key that rule by a stable selector, preferably a source-unique `data-flowbridge-ix-state="ixs-N"` marker added to the element when existing classes or `data-w-id` are not unique enough;
- make the transport cascade-dominant against source class defaults. Appending after source CSS is necessary but not sufficient when the source selector has higher specificity; use a selector at least as specific as the source class chain or `!important` on the transported first-frame declarations;
- preserve declaration pairs as pairs. If the source first frame uses `width: 100%` plus `height: 0rem`, transporting only the width is still a first-frame loss;
- remove or rewrite the IX-shaped substring from source-content `style=""` only after the transport exists;
- remove the `style` attribute entirely when no declarations remain;
- keep structural styles, especially `fb-custom-code style="display:none"`;
- preserve every `data-w-id`.

Example output shape for the future script:

```json
{
  "ixInlineStyleAttrs": {
    "sourceStyleAttrs": 143,
    "ixOnly": 137,
    "mixed": 6,
    "structural": 1,
    "requiresModeBNeutralization": true
  }
}
```

## Output Probes

Input probes only identify hazards. Output probes prove the skill satisfied the contract on disk.

For `webflow-paste` mode, the future output gate must verify:

- zero IX-shaped source-content inline `style=""` substrings in the pretreated output;
- required initial-state transport for critical selectors such as menu closed panels, hidden nav links, collapsed image shells, and non-component IX reveal anchors: each must be cascade-safe `converted-to-css/embed` or a documented component-root fallback; `converted-css-cascade-risk` and `stripped-without-equivalent-transport` are FAIL;
- zero `fb-runtime` hosts and zero relative `js/webflow.js` references;
- `data-w-id` output count matches source count unless a manifest row explains a source-premise exception;
- structural hiding such as `fb-custom-code style="display:none"` remains;
- `fb-styles-site` carries the source site class CSS needed by the converter; HEAD-only class/layout CSS is a contract FAIL;
- every detected static-visible library host carries fallback CSS on source-present root and inner selectors; runtime-state-only fallbacks such as `.splide.is-initialized` / `.splide.is-rendered` are contract FAILs;
- relative font URLs are reported as warnings or FAIL rows, not silently accepted;
- `pretreat-manifest.json` exists and agrees with `index.html`.

For `local-preview` mode, the output gate verifies the current L-15A/L-19 posture: one late `fb-runtime` host, one external `js/webflow.js`, no inlined module IIFE, and preserved IX/source evidence.

Run shape:

```bash
python3 AI_OS/SKILLS/webflow-pretreat/scripts/paste_contract_probe.py \
  --source-root <raw export root or zip> \
  --output-root output/{lane}_{source-slug}-file_output \
  --mode <local-preview|webflow-paste> \
  --write-manifest \
  --fail-on-contract
```

`--mode` is mandatory. The probe must not rely on a default or on a stale `pretreat-manifest.json` left by a previous run in another mode.

## Pretreat Manifest Contract

The probe writes a machine-readable `pretreat-manifest.json` beside `index.html`.
In `webflow-paste` mode, contract FAIL rows are fail-closed by default. Use
`--advisory` only for exploratory diagnostics where a non-zero exit would be
counterproductive. `--fail-on-contract` remains accepted and should stay in the
skill runtime command for readability.

Minimum shape:

```json
{
  "schema": "flowbridge.pretreat-manifest.v1",
  "outputMode": "webflow-paste",
  "animationClaim": "static-visible",
  "ixShape": {
    "inventoriedStyleAttrs": 143,
    "neutralizedStyleAttrs": 143,
    "preservedStyleAttrs": 0,
    "preservedReasons": []
  },
  "runtime": {
    "fbRuntimePresent": false,
    "jsWebflowReferences": 0
  },
  "fonts": {
    "relativeFontUrls": [],
    "policy": "reported-only"
  },
  "contractChecks": [],
  "probesRun": []
}
```

Any FAIL in `contractChecks[]` is a pre-zip HALT. WARN rows are allowed only when the policy explicitly says reported-only, currently relative font URLs. A Webflow-paste result without this manifest is not paste-contract-ready.
