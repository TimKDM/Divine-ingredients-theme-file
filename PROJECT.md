# Divine Ingredients Theme — Project Status

Quick-start brief for resuming work in a new conversation. Last updated end of session 2026-06-19.

---

## What this is

Shopify theme rebuild for **Divine Ingredients** (organic tea + superfood + botanicals brand). Base is the **Flux** premium theme by Mana Themes; we've layered a custom `.d-*` design system on top.

- **Brand**: Forest green + beige palette. Cormorant serif + Jost sans. "Honest ingredients. Nothing more."
- **Repo**: `TimKDM/Divine-ingredients-theme-file`
- **Working branch**: `claude/gracious-sagan-ff3uf5` (current HEAD `e8f4632`). All work happens here; auto-PRs merge it to `main`, and Shopify two-way-syncs `main` back.
- **Store**: Divine Organic Ingredients — `divine-organic-tea.myshopify.com`. Custom domain `divineingredients.com`.
- **GitHub-connected theme**: "Divine-ingredients-theme-file/main" (UNPUBLISHED draft, theme id `149418803375`). The *published* (MAIN) theme is still an old "Updated copy of Flux" — we preview the GitHub draft.

## People

- **Tim** (`tim@kingdigitalmarketers.com`) — engineer running the session.
- **Alisha** — brand owner / decision maker. Final say on copy + product structure.
- **Preet Bhullar** — founder, microbiologist (in the brand story).

## Tech stack & conventions

| Layer | What |
|---|---|
| Custom CSS | `assets/divine-theme-v4.css` — single ~2.6k-line stylesheet, `.d-*` classes. Loads **after** Flux base via `layout/theme.liquid:310`. |
| Custom JS | `assets/divine-theme-v4.js` — small reveal observer. |
| Section files | `sections/divine-*.liquid` — every custom section is `divine-` prefixed. Stock Flux sections (`header.liquid`, `footer.liquid`, `main-product.liquid`) restyled via CSS overlay. |
| Template JSON | `templates/*.json` start with the auto-generated Shopify comment header (`/* IMPORTANT ... */`) — strip the comment before JSON-parsing/validating. |

**Critical rules learned this project:**
1. **PR-only / branch workflow** — never push direct to `main`. Push to `claude/gracious-sagan-ff3uf5`; auto-PR merges it.
2. **Shopify schema validation is strict** — a text setting with `"default": ""` (blank) **fails the whole file's sync** ("default can't be blank"). Keep schema defaults non-blank; blank the *instance* value in the template JSON instead. This silently blocked `divine-product.liquid` from syncing for a while.
3. **Liquid: no filters inside `[ ]` access.** `section.settings['image_' | append: i]` is a syntax error → rejects the file on sync. Assign the key to a variable first. (Broke the powders 3×3.)
4. **`rgba(0,0,0,0)` bg-bug**: Shopify color picker returns `rgba(0,0,0,0)` not blank. Sections consuming `background_color` use the `!= blank and != 'rgba(0,0,0,0)'` pattern.
5. **Em dashes banned** from customer copy (Alisha). Use periods/commas.
6. **Numbers render in Jost everywhere** via a `unicode-range` `@font-face` digit remap on Cormorant/Josefin (top of `divine-theme-v4.css`).
7. **`matrixify/` files are NOT theme files** — the GitHub→theme sync logs them as "ignored" (expected/harmless). They only do anything when **imported in the Matrixify app**.
8. **Shopify MCP writes are blocked** in this environment (every `productUpdate`/`tagsAdd`/theme write returns "requires approval"). So all store data changes go through **Matrixify CSV/XLSX imports** the merchant runs. Reads work (when on the right store).
9. **Matrixify CSV comma bug**: multi-tag cells (`"a, b, c"`) can get split on import → only the first tag lands. **Use the `.xlsx` versions** for anything with multiple tags. `openpyxl` is pip-installable here to generate them.

## Fonts
- Body = **Jost**, headings = **Cormorant**. Shopify's `--font-body-family`/`--font-heading-family` (set to Josefin Sans in settings) are **overridden in our `:root`** so all stock sections inherit the brand fonts. Plus targeted `!important` overrides for the mega menu (`.main-navigation*`, `.mega-menu*`) and all form elements.

## Color palette (CSS vars in v4 `:root`)
```
--d-black #111410 · --d-forest #1F3018 · --d-mid #3C4C30
--d-beige #E8E0CC · --d-beige-lt #F2EDE0 · --d-beige-dk #D4CAAE · --d-white #FDFCF8
--d-font-serif: Cormorant · --d-font-sans: Jost
```

## Homepage sections (render order, `templates/index.json`)
`divine_hero` (video+poster) · `divine_ticker` (forest trust bar) · `divine_rituals` (divine-categories, 5 By-Function tiles → now linked to `immunity`/`wind-down`/`gut-reset`/`focus-and-energy`/`detox` collections) · `divine_powders` (divine-powders; supports 2×2 **and 3×3 9-image collage**) · `divine_bestsellers` (divine-products; **hand-picked product blocks** = Mumbai Chai / Taro Powder / Turmeric Spice / Supreme Matcha; prices hidden) · `divine_story` (brand story, Preet) · `divine_discovery` (**The Chai Edit**) · `divine_newsletter` · `divine_certs` (disabled) · `divine_b2b` (wholesale).
Homepage section padding trimmed ~25% for a tighter page.

## Product pages (PDP)
- Templates: **`product.json`** (tea, default) uses `divine_product` + `divine_product_details` (kv_table facts + **numbered_steps "Steeping"**). **`product.powder.json`** uses `divine_product` + `divine_product_details` (kv_table + **numbered_uses "How to Use"**).
- **Facts table** is metafield-driven via snippet **`snippets/divine-product-facts.liquid`** (lookup: individual `custom.*` metafields → `custom.product_facts` → section/template default rows). Rendered in the bottom **2-column** "Additional Information" section (facts left, steeping/how-to-use right) — gap tightened to 48px + centered max-width 1200px.
- Hero (`divine-product.liquid`): image frame is **4:3**, tightened spacing; **8.8oz bulk badge removed** (blanked `bulk_text` in both templates).
- Steeping/How-to-Use steps are **card-styled** (white card + border) on both.

### PDP metafields (custom namespace)
- **Tea/shared**: `tea_type, ingredients, tasting_notes, best_enjoyed, aroma, liquor_colour, certifications, contains_caffeine, origin, allergens, storage`
- **Powder-specific** (wired into the facts snippet): `product_type, active_compounds, fillers, serving`
- One-time: these need definitions in Settings → Custom data → Products. Populated via Matrixify.

## Collection filter (`sections/divine-collection.liquid`)
- Client-side JS filter, paginate `by:250` (whole collection on one page). Parses the **Matrixify tag taxonomy**: `Category_*`, `Type_*`, `Function_*` (prefix stripped + handleized). Falls back to `product.type` for category.
- **Auto-hides** any filter option with 0 matches and any empty group.
- Tea + Powder types share one **"Type"** group (so OR-within-group works). H1 uses the real collection name.
- Real store tags: Category_(Tea/Powder/Spices_Botanicals); Type_(Black/Green/Herbal/Chai/Iced Tea, Matcha, Mushroom/Fruit Powder, Superfood Blend); Function_(Immunity/Wind down/Gut Reset/Focus and Energy/Detox); Caffeine_*; Format_*; Organic.
- **By-Function collections are tea-only** (Alisha's curated lists). Powders must NOT carry `Function_` tags.

## Tagging state (the saga)
- Powders were untagged. Imported `products-powder-tags.xlsx` → added `Category_`/`Type_` (and originally `Function_`, since removed). **Spices** (Ginger/Black Pepper/Cinnamon/Cardamom/Turmeric) = `Category_Spices_Botanicals`, no Type.
- Powder **template** assigned via `products-set-powder-template.csv` (38 non-matcha powders → `template_suffix: powder`). Matcha stays tea per Alisha.
- ⚠️ **OPEN**: `products-powder-remove-function-tags.xlsx` strips `Function_` off 11 powders (Reishi/Chaga/Cordyceps/Lion's Mane/Maca/Rhodiola/Spirulina×2/Moringa/Theanine/Ashwagandha). Merchant imported it but **not yet verified** (connection was on wrong store). The junk `$0` Rhodiola dup (id `8616074084527`) still has its function tag — should be **deleted** in admin.
- `products-organic-tag.xlsx` adds **Organic** to 133 products (excludes the 5 "Conventional" items + teapot/subscriptions/consultation). **Not yet confirmed imported.**

## Done this session (highlights)
Numbers→Jost · footer Help→**Company** · removed 8.8oz badge · contact page now uses simple **`divine-contact`** section · "Discovery Set"→"Chai Edit" swept · collection filter rebuilt (real tags + auto-hide + Type group) · powders 9-image collage · bestsellers hand-picked + 2×2 mobile · PDP facts moved to bottom 2-col + card steps · Preet photo centers in content on mobile · mega-menu + global font sweep to Jost/Cormorant · mobile logo centering, powders 2-col mobile.

## Open / waiting on
| Item | Status |
|---|---|
| **Shopify MCP on wrong store** | Connection is on **`euphree-dealer.myshopify.com`** (a different store). Must switch back to `divine-organic-tea` before any reads/audit. `switch-shop` revokes token → next call prompts re-auth (merchant selects Divine). |
| **Content audit** | NOT done — blocked by wrong-store connection. Sweep active products for missing `descriptionHtml` and missing facts metafields, produce a list. |
| **Verify powder Function_ removal** | Confirm the 11 powders dropped out of By-Function collections after the Matrixify import. |
| **Delete `$0` Rhodiola dup** | id `8616074084527`, no image, $0 — junk duplicate. Merchant deletes in admin. |
| **Footer menus** | `footer-by-function` / `footer-by-category` exist in store + referenced correctly. Should be populated. |
| **Mobile verification** | #6–9 (logo center, powders 2-col, bestsellers 2×2, Preet middle) can't be seen rendered here — verify on device. Header logo centering depends on stock layout. |
| **Possible duplicate products** | Spotted dupes (2× Mellow Mint, Wine Berry Iced Tea, Chamomile, Sweetened Matcha, Conventional Jasmine/Rose, Coffee Cherry). Merchant cleanup. |

## Matrixify files (`matrixify/`) — import in the Matrixify APP, not GitHub
| File | Purpose |
|---|---|
| `divine-bulk-import.xlsx` | Original all-in-one (products/collections/menus). |
| `products-powder-tags.xlsx` / `.csv` | Powder Category_/Type_ tags (Function_ already stripped from source). |
| `products-powder-remove-function-tags.xlsx` | REPLACE tags on 11 powders to drop Function_. **Pending verify.** |
| `products-set-powder-template.csv` | Sets `template_suffix: powder` on 38 powders. |
| `products-organic-tag.xlsx` / `.csv` | Adds `Organic` to 133 products. **Pending import confirm.** |
| `products-update.csv`, `products-descriptions.csv`, `products-new.csv`, `collections.csv`, `menus.csv`, `menus-cleanup.csv` | Earlier tea tagging/descriptions/collections/menus. |

## How to resume
1. New thread → this repo + branch `claude/gracious-sagan-ff3uf5`. Skim this file.
2. **Check the Shopify MCP store first** (`get-shop-info`) — if it's Euphree, get the merchant to switch to Divine before any audit/verify.
3. Small commits, push to the feature branch, let auto-PR + Shopify sync handle deploy. Validate JSON (strip comment header) and Liquid `if/for` balance + no blank schema defaults before pushing.
4. Store data changes = generate Matrixify **.xlsx** (commas-safe) for the merchant to import.
