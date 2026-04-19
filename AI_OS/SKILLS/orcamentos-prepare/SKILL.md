---
name: orcamentos-prepare
description: |
  Use when the user pastes or uploads a PLV/printing quote (RFQ text, PDF, technical drawing, specification sheet, or raw component list) and needs structured extraction into the IMACX intake table format. Also triggers on: "extract this quote", "prepare this for intake", "make a table from this PDF", "what are the components", "extract materials", any paste of component specs in Portuguese (laterais/prateleiras/crowner/cartão/favo/PVC/etc), or quote comparison requests ("what changed between these two").
---

# Orcamentos Prepare — Quote-to-Table Extraction

## Purpose

Extract structured component data from PLV (Publicidade no Local de Venda) quote documents and output tab-separated tables ready to paste into the IMACX intake system's "Importar Tabela" feature.

**Core principle — everything is custom-made.** IMACX produces no standard sizes. Every dimension is client-specific. All formulas in this skill are calculation methods to be applied to whatever dimensions the client provides — never assume or substitute a "standard" value. If a required dimension is missing, ask the client.

---

## Ao receber um paste — ordem de ataque

1. **Mode A?** (specs completas: componente + dimensões + material + impressão) → ir directo a Extraction Rules + Output.
2. **Mode B?** (incompleto ou produto complexo) → classificar → ler `product-rules.md` → perguntar o que falta → extrair.
3. **Sempre** query `materials_unified` em Supabase (project `bnfixjkjrbfalgcqhzof`, tool `mcp__claude_ai_Supabase_2__execute_sql`) antes de escrever a tabela — os 4 campos Material/Caract./Cor/Espessura têm de ser verbatim da DB.
4. **Output** = tabela tab-separated com o header exacto da secção Output Format.
5. **STOP e perguntar** se: dimensão impossível, material sem match, laminação sem acabamento especificado, decisão estrutural em falta.

---

## Reference Files

This skill has two companion reference files in the same directory. Read them as needed during extraction:

- **product-rules.md** — Per-product component rules, decision trees, question templates, and worked examples. Read when a product type has structural decisions to resolve (Mode B) or when you need product-specific formulas (Forra Alarmes planification, Cubo unfolding, Pé de Encosto, etc.).
- **material-reference.md** — Material parsing tables, categories & stacking, espessura matching, outsource rules, brindes, and bought items. Read when resolving material names from RFQ text, checking outsource status, or understanding combo stacking.

---

## Data Sources

All material and model data lives in **Supabase** (project `bnfixjkjrbfalgcqhzof`). Query via Supabase MCP tools — this is the single source of truth, accessible from any machine.

| Table / View               | What it contains                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `materials_unified`        | **Source of truth for all material lookups.** A view exposing both base materials (`source='material'`) and combos (`source='combo'`) with the same 4-field identity (`material`, `carateristica`, `cor`, `espessura`). Always query this view — never query `materials` or `material_combos` separately for material resolution. |
| `materials`                | Base materials table (underlying `materials_unified`). Only query directly for fields not in the view (e.g. `custo_m2`, `tipo`).                                                                                                                                                                                                  |
| `material_synonyms`        | Synonym mappings — used internally by the intake app, not needed for skill output.                                                                                                                                                                                                                                                |
| `material_combos`          | Combo definitions with `nome` and `custo_m2`. Use only to browse available combo names.                                                                                                                                                                                                                                           |
| `material_combo_items`     | Links each combo to its individual material layers with `ordem`. Informational only — never expand layers in output table.                                                                                                                                                                                                        |
| `material_formats`         | Available sheet/roll formats per material.                                                                                                                                                                                                                                                                                        |
| `print_canonical_synonyms` | Print spec normalization (e.g., "single sided 4 colours" → "4/0").                                                                                                                                                                                                                                                                |
| `bought_items`             | Items IMACX buys, not produces (porta-preços, ganchos, abraçadeiras, roll-up mechanisms, metal structures). Flag separately — never extract as a component.                                                                                                                                                                       |
| `client_product_models`    | Known product models per client group with `trigger_keywords` and `base_price`.                                                                                                                                                                                                                                                   |
| `model_components`         | Component breakdown for each known model (material, qty, dimensions, print).                                                                                                                                                                                                                                                      |

Maria adds and edits materials regularly, so row counts and exact values change. Always query live, never trust cached snapshots.

**How to query:** Use the Supabase MCP `execute_sql` tool with `project_id: "bnfixjkjrbfalgcqhzof"`. The tool name has a session-specific hash prefix — find it via ToolSearch if needed.

**Legacy CSV exports** at `AI_OS/temp/material_*_rows.csv` are stale snapshots — do not use. Always query Supabase.

---

## Workflow: Classify → Decide → Extract → Output

Every RFQ follows this pipeline:

```
INPUT → Classify product type (table below)
      → Do I have enough info?
          YES → Go to Extraction Rules + Output Format
          NO  → Read product-rules.md for that product type → Ask Maria → then extract
```

**Mode A — Full specs given** (component list with dimensions, materials, print specs):
Skip classification. Go straight to extraction rules and output.

**Mode B — Incomplete or complex product** (e.g. "expositor de chão, 4 prateleiras, 130cm"):
Classify → read **product-rules.md** for that product type's decision tree → ask what's missing → extract → output.

**Never guess structural decisions.** If the decision tree says you need to know FAVO vs CARTÃO and the RFQ doesn't say, ask. Better one question now than a wrong quote.

### Product Type Classification

| Signal                                                             | → Product type  |
| ------------------------------------------------------------------ | --------------- |
| Shelves + lateral panels + structure                               | `expositor`     |
| Flat panel on gondola header                                       | `crowner`       |
| Gondola header kit (crowner + 2 laterais)                          | `topo`          |
| Flat panel on feet, floor-standing                                 | `standup`       |
| 3D column/tower without shelves                                    | `totem`         |
| 3D cube or prism, decorative                                       | `cubo`          |
| Printed wrap covering pallet island                                | `forra_ilha`    |
| Rectangular tube wrapping EAS antenna                              | `forra_alarmes` |
| Floor-applied print                                                | `floorgraphic`  |
| Retractable banner                                                 | `roll_up`       |
| Paper poster (A3/A4/monofolha/menu)                                | `cartaz_papel`  |
| Rigid print panel, multi-piece                                     | `placa_rigida`  |
| Window/signage vinyl (Montra/EasyDot)                              | `vinil_montra`  |
| Sticker/self-adhesive                                              | `autocolante`   |
| Banner/flag, hanging                                               | `bandeirola`    |
| Floor banner, large format                                         | `lona`          |
| Counter display, tabletop                                          | `bancada`       |
| Box product explicitly quoted as the item, not transport packaging | `caixa`         |
| Flat print on flexible material                                    | `flexivel`      |
| Can't determine                                                    | → ask Maria     |

**Common misclassifications to watch for:**
| RFQ says | But actually | Why |
|---|---|---|
| "expositor" (flat panel on feet) | `standup` | No shelves → standup |
| "totem" (flat panel) | `standup` | 2D → standup |
| "totem" (cube/prism) | `cubo` | Equal faces → cubo |
| "crowner" (with laterais) | `topo` | Has laterais → topo |
| "cartaz" (rigid multi-piece) | `placa_rigida` | Structure → placa_rigida |
| "cartaz" (vinil) | `vinil_montra` | Montra/EasyDot → vinil_montra |
| "cartaz" (paper poster) | `cartaz_papel` | A3/A4/monofolha → cartaz_papel |

**After classifying:** if the product type has decisions that can't be resolved from the RFQ, read **product-rules.md** for the question templates and formula options, then ask Maria before producing a table.

---

## Input Types

### 1. IMACX Technical Drawings (Desenho Técnico)

- Header: `HH PRINT: [product name]` or `DESENHO TÉCNICO`
- Each component block: DESCRIÇÃO, MATERIAL, QUANTIDADE, TIPO IMPRESSÃO, MEDIDA (mm)

### 2. HH Global RFQ PDFs

- Fields: Enquiry Number, Enquiry Title, Reply By Date, Quantity/versions, Additional information
- The "Additional information" block is the richest source — parse it carefully
- May have multiple specifications across pages

### 3. IMACX Orçamento PDFs (PHC-generated)

- Header: Orçamento Nº, Data, Nº Cliente
- Free-text Designação field

### 4. Expositor/Display Specifications

Multi-component products: Laterais, Prateleiras, Traseira, Crowner, Base, Batente, Frentes de prateleira, Cruzetas, Enchimentos.

---

## Output Format

ALWAYS output a **tab-separated table** with this EXACT header and column order — this matches the IMACX "Importar Tabela" form. Wrong column order makes the dropdowns come up empty even when the values are correct, and Maria has to fix every row by hand:

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
```

Rules:

- Dimensions ALWAYS in **meters** — convert from mm (÷1000) or cm (÷100). L/A go BEFORE Material.
- **Impressão = number of print colours (CORES field in app).** Always `4/0`, `4/4`, or `0`. Never `0/0`. This is NEVER the colour of the material — it is purely a print specification. This applies to ALL materials without exception. The `cor` field in `materials` table is the physical colour of the material (BRANCO, PRETO, KRAFT, TRANSPARENTE, etc.) — completely separate from Impressão.
- **Material / Caract. / Cor / Espessura must be copied verbatim from `materials_unified`** — never invent, normalize, or guess. The intake form validates all 4 against this view (covers both base materials and combos), and rejects anything that doesn't match.
- **Qty = per-kit** — never multiply by total run
- If the source doc doesn't specify a material → leave the 4 material columns empty so Maria can pick. NEVER write a value that isn't in the database.
- No printing → `0`

### Material resolution — MANDATORY Supabase lookup

Before producing any extraction table you MUST query Supabase (project `bnfixjkjrbfalgcqhzof`) and use the exact `material`, `carateristica`, `cor`, `espessura` values from the matching row in `materials_unified`. This is non-negotiable — Maria's intake app uses a deterministic parser that matches these 4 fields exactly. Querying from memory or legacy CSVs is forbidden.

**The view `materials_unified` exposes two types of rows:**

- `source = 'material'` — base materials (CARTÃO, PVC, VINIL, PP, etc.)
- `source = 'combo'` — combos (e.g. "Cartão 3mm Vinil Laminado Mate"), always with `carateristica = 'COMBO'`, `cor = '-'`, `espessura = '-'`

> Updated 2026-04-15: `materials_unified` now emits combos with the canonical UI shape `COMBO / - / -`. Base material rows are unchanged.

**Combos are first-class materials.** A combo resolves to **one single row** in the output table — never expand into multiple rows (substrate + vinil + laminação separately). The intake app handles cost breakdown internally.

**Lookup order:**

1. **`materials_unified` direct match** — query `WHERE material = '[name]' AND carateristica = '[caract]' AND cor = '[cor]' AND espessura = '[esp]'`. Works for both base materials and combos.
2. **`materials_unified` by material name only** — if caract/cor/esp not specified in RFQ, query `WHERE material = '[name]'` and pick the closest match.
3. **`material_combos` by name** — when RFQ describes a laminated/printed spec (e.g. "Cartão 3mm impressa 4/0, laminação mate"), search `material_combos` for the matching combo name, then confirm it exists in `materials_unified`.
4. **`bought_items`** — items IMACX buys, not produces (porta-preços, ganchos, abraçadeiras, roll-up mechanisms, metal structures, pre-made bolsas if listed). These are NOT components — flag them in a separate note, do not put them in the extraction table.
5. **`client_product_models` + `model_components`** — if the RFQ matches a known client model (check `trigger_keywords`), use the model's component breakdown as the source of truth instead of re-extracting.

**Espessura format varies per row.** PP Branco is stored as `0.5` (no unit). PETG is `0.5MM` (with MM). Vinil is `STANDARD` or `PHT100`. Copy whatever the database has — do not normalize or add/strip units.

**Espessura not found — use closest available + flag.** If the exact espessura doesn't exist in the DB, use the closest available espessura for that material and add a note below the table:

```
⚠️ Adaptação: [Material] [espessura pedida] não existe na DB — usado [espessura usada] (espessura mais próxima disponível). Confirmar com Maria se necessário.
```

Never silently swap without the note. This applies to all attributes (cor, carateristica) — closest match + note, never silent substitution.

**If no match at all for the material itself:** STOP. Tell Maria the exact term that failed, what's closest in the DB, and ask whether to (a) use an existing material, (b) create a new one in `materials`, or (c) treat it as a bought item. One question now beats a broken import later.

(For the full list of Supabase tables and what each contains, see the **Data Sources** section above.)

### One table per ITEM — CRITICAL

**One table = one item to be quoted.** All components of the same item go in the same table, even if they have different dimensions. Separate tables are only used when there are separate items to quote.

- **Forra Ilha ½ palete** (60×60 + 84×60cm) → **one table**, two rows (both panels are components of the same item)
- **Forra Topo Ilha** (64×60 + 84×60cm) → **separate table** (it is a different item), two rows
- **Stand UP + Pé de Encosto** → **one table**, two rows (pé is a component of the stand)
- **Crowner + Pé de Encosto** → **one table**, two rows
- **Expositor with Laterais + Prateleiras + Crowner + Base** → **one table**, one row per component type

The system imports each table as one item with multiple components. The user assigns the item name and enquiry reference per table.

---

## Extraction Rules

### HHGlobal RFQ Field Conflicts

When "Additional information" and the "Dimensions" field (Finished size width/height) give **different values for the same dimension**, always use the **larger value**. No warning needed — just use the larger value silently.

Example: additional info says `143×158cm`, Dimensions says `133×159cm` → use `143×159cm` (143 > 133 for width; 159 > 158 for height — compare per axis independently).

### Dimension Parsing

- `90 x 130 cm` → Largura: 0.900, Altura: 1.300
- `481 x 495 mm` → Largura: 0.481, Altura: 0.495
- `L 1647 x A 850mm` → Largura: 1.647, Altura: 0.850
- `no fto 47 x 50 cm` → Largura: 0.470, Altura: 0.500
- Width (Largura) = first dimension, Height (Altura) = second
- mm ÷ 1000, cm ÷ 100. Never negative.

### Print Parsing

- `impressa/impresso 4/0` → `4/0`
- `0/0`, `sem impressão` → `0`
- `Single sided` + `4 colours` → `4/0`
- `Double sided` → `4/4`
- No info → `0`

### Laminação + Impressão → Usar Combo (UMA linha, não três)

**Regra crítica de produção:** Não é possível laminar sobre impressão directa num substrato rígido. Quando um componente tem **impressão + laminação**, tem de ser representado por um **combo** — uma entrada única em `materials_unified` que já inclui substrato + vinil + laminação.

**Um combo = uma linha na tabela de output.** Nunca expandir em 3 linhas separadas. O intake app resolve o custo internamente.

**Como resolver:**

1. Identificar o acabamento: mate ou brilho? (se não especificado, perguntar antes de extrair)
2. Procurar em `material_combos` o nome do combo correspondente
3. Confirmar em `materials_unified` — combos têm sempre `carateristica = COMBO`, `cor = -`, `espessura = -`
4. A impressão (4/0 etc.) vai na coluna Impressão da linha do combo

**Convenção de nomes dos combos:**

- 2 layers (substrato + vinil, sem laminação): `[Substrato] [esp] + Vinil` → ex: `Cartão 3mm + Vinil`
- 3 layers (substrato + vinil + laminação): `[Substrato] [esp] Vinil Laminado [Brilho/Mate]` → ex: `Cartão 3mm Vinil Laminado Mate`

**Sinais de laminação no RFQ:**
`laminação`, `laminado`, `lam.`, `laminação 1 face`, `laminação 2 faces`, `mate`, `brilho`, `soft touch`, `velvet`

**Exemplo correcto:**
RFQ: `Lateral em Cartão 3mm impressa 4/0, laminação mate 1 face`

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Lateral	2	0.900	1.300	Cartão 3mm Vinil Laminado Mate	COMBO	-	-	4/0
```

Se o combo não existir na DB → **STOP. Perguntar a Maria** qual o combo a usar ou se deve ser criado.

### Dimension Anomaly — STOP and Ask

When a dimension value appears physically impossible or nonsensical for a POS display item (e.g., A=11330mm on a module that visually looks ~113mm tall, or a width clearly larger than the whole display), **STOP and ask Maria before extracting**. Do not guess, do not proceed. Example:

> ⚠️ A dimensão A=11330mm no Módulo 1 parece um erro (11,33 metros). Confirmas que é 113mm?

Wait for confirmation before producing the table.

### Bought Items and External Items — Always Include in Table

Items that IMACX does not produce (bought items, external procurement) must **still appear as rows in the extraction table**, not just as notes. Add them as a clearly labelled row at the bottom with a flag:

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
...
Focos LED encastrar 4500K	3	—	—	—	—	—	—	0
```

And add a note below:

```
⚠️ [Nome do item] — item externo / compra externa. Não produzido pela IMACX.
```

Before flagging as external, always check `bought_items` table in Supabase — the item may already be catalogued there.

### Orla — Metros Lineares

When a component is described as "orlado" (edge-banded), add an orla row to the same item table. Calculate:

- Perímetro por peça = (L + A) × 2 (for rectangular pieces)
- Total = perímetro × número de peças de favo × 1.30 (add 30% for cuts/waste)
- Assume **BRANCO** unless the DT specifies otherwise
- Leave Material/Caract./Cor/Espessura columns blank (orla is a bought item — bought_items table)
- Impressão = `0`

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Orla Branca 16mm	[metros lineares calculados]	—	—	—	—	—	—	0
```

Note below: `⚠️ Orla: [X]m lineares calculados (perímetro × nº peças × 1.30). Cor assumida BRANCO — confirmar se diferente.`

### Quantity Parsing

- `2 Laterais` → 2 | `4 prat.` → 4 | no qty → 1
- Never multiply by total run

### Component Name Standardization

Lateral, Prateleira, Traseira, Crowner, Base, Batente, Frente Prateleira, Cruzeta, Enchimento, Tampo, Rodapé, Costas Externas/Internas, Enchimento Prateleira N, Forra Ilha Frente/Costas, Forra Ilha Lateral, Forra Topo Ilha, Forra Alarmes, Cubo, Paralelepípedo, Pé de Encosto, Stand UP, Easy Dot, Saia Ilha.

### Porta-Preços

Porta-preços are a finished product (produto acabado) — **never include in extraction tables**.

### Caixa vs Caixa de Transporte

When description says "MONTADO EM CAIXA", "FORNECIDO EM CAIXA" or similar, and the box is only transport packaging for another item, flag it as a separate note (NOT as a row in the extraction table):

```
⚠️ Item inclui CAIXA DE TRANSPORTE — flagged separately, not extracted as a component.
```

Do not calculate. Do not ask. Just flag.

Exception: if Maria says the `caixa` is the quoted/printed item itself (not transport packaging), classify as `caixa`, read `product-rules.md`, and output the planified box dimensions in the table.

---

## Quote Comparison

When two documents provided:

1. Extract both
2. Show: components in both (highlight diffs), additions, removals, summary
3. Output NEW quote table ready to paste

---

## Context: IMACX Table Import

- Tab-separated format, schema fixo: `Componente | Qty | Largura (m) | Altura (m) | Material | Caract. | Cor | Espessura | Impressão`
- O intake app usa um **parser determinístico** para tabelas neste schema — sem LLM, sem synonym lookup. Os 4 campos Material/Caract./Cor/Espessura são usados directamente para match em `materials_unified`.
- **Os 4 campos têm de ser exactamente os valores da DB** — qualquer diferença de maiúsculas, espaços ou ortografia causa falha silenciosa.
- **System multiplies Qty × total kit quantity** — never pre-multiply
- User sets Enquiry reference and Nome do Item from the document header

---

## Quick Examples

**Princípio:** A skill é um extractor de materiais + dimensões. Não precisa de saber o que é uma shelfstrip, uma lateral, uma saia, um glorifier. Precisa de ler o que está escrito, fazer match do material a `materials_unified` (exacto se bate, senão o mais próximo), e devolver a tabela.

Os modelos (`client_product_models`) só são usados quando o input não tem dimensões explícitas e refere uma estrutura conhecida — ex: "saia de 1 palete" sem dimensões → skill aplica a configuração de 1 palete (perímetro 4.030m, altura 0.750m standard). Para tudo o resto, **respeita o que a Maria escreveu**.

### Exemplo 1 — Shelfstrip (material directo, sem contexto de produto)

**Input:** `SHELFSTRIP PAPEL WHITEBACK 200grs, (1x) 4×48cm a 4/0`

A skill não precisa de saber o que é uma shelfstrip. Só tem de encontrar `PAPEL / WB / BRANCO / 200GR` na DB e usar as dimensões dadas.

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Shelfstrip	1	0.040	0.480	PAPEL	WB	BRANCO	200GR	4/0
```

### Exemplo 2 — Laterais de Topo (componente múltiplo, Qty > 1)

**Input:** `Laterais de topo. CARTÃO 3mm. Conjunto laterais (2x) 50×205cm a 4/0`

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Lateral	2	0.500	2.050	CARTÃO	ESTUCADO/NÃO-ESTUCADO	BRANCO	3MM	4/0
```

### Exemplo 3 — Forra Ilha em Rolo 2P (saia flexível, usar closest + pala)

**Input:** `Forras Ilha em Rolo 2P. PAPEL LAMINADO 150grs + laminação a quente (encapsulação). (1x) 2500×75cm a 4/0`

Saia em rolo → **1 linha**, largura = dimensão dada + pala 0.030m, altura copiada. 150gr não existe na DB — usar o combo mais próximo (`Papel Laminado Brilho 200GR`, que já inclui laminação). Para orçamento o que importa é o m².

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Saia Ilha	1	25.030	0.750	Papel Laminado Brilho	COMBO	-	-	4/0
```

### Exemplo 4 — Saia de Ilha 1P em Cartão (modelo de 1 palete quando dimensão implícita)

**Input:** `Saia de Ilha 1 palete. CARTÃO 3mm. 4/0. Altura 60cm`

Saia em rolo ou saia em cartão com pala → **1 linha**. "1 palete" sem perímetro explícito → skill usa o modelo de 1 palete: perímetro (1.200+0.800)×2 = 4.000m + pala 0.030m = 4.030m. Altura 60cm como dada.

```
Componente	Qty	Largura (m)	Altura (m)	Material	Caract.	Cor	Espessura	Impressão
Saia Ilha	1	4.030	0.600	CARTÃO	ESTUCADO/NÃO-ESTUCADO	BRANCO	3MM	4/0
```

---

## WHEN FULLY AMBIGUOUS

If you cannot classify with confidence:

> Não consigo classificar este pedido com confiança. Parece ser [best guess] mas pode ser [alternative]. Podes confirmar o tipo de produto?

After Maria answers, proceed directly to extraction + output. Don't re-ask.
