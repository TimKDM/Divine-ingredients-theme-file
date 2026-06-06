# Matrixify import files

Generated from `Tea & Powder Menu.xlsx`. Two CSVs designed to work together
with the [Matrixify](https://matrixify.app) Shopify app.

## Contents

- **`products.csv`** — 86 products, deduped across the Excel sheets.
  Every product carries rich tags (`Function_*`, `Type_*`, `Category_*`,
  `Format_*`, `Organic`, `Founders_Favourite`) plus a list of smart-collection
  memberships in the `Smart Collections` column.
- **`collections.csv`** — 18 smart collections that auto-populate based on
  the tags above. Add a product to "Immunity" by tagging it `Function_Immunity`;
  no manual collection-membership editing needed.

## Upload order

1. **First, upload `collections.csv`** in Matrixify → Import → Collections.
   This creates the smart-collection skeleton. Without this step, the
   product upload's `Smart Collections` column will try to attach to
   collections that don't exist yet.
2. **Then, upload `products.csv`** in Matrixify → Import → Products.
   The `MERGE` command tells Matrixify to update existing products by
   handle and create the ones that don't exist. `Tags Command: MERGE`
   preserves any tags merchants have already added in admin.

## Tag taxonomy

| Tag prefix | Example | Collection it feeds |
|---|---|---|
| `Function_` | `Function_Immunity` | Immunity |
| `Type_` | `Type_Green Tea` | Green Tea |
| `Category_` | `Category_Tea`, `Category_Powder`, `Category_Spices_Botanicals` | All Teas, All Powders, Spices & Botanicals |
| `Format_` | `Format_Powder`, `Format_Botanical`, `Format_Spice` | (informational; not collection-mapped) |
| `Organic` | — | All Organic |
| `Founders_Favourite` | — | Founders' Favourites |

## Re-generating

The source of truth is the Excel menu. To regenerate after Alisha edits it:

```bash
# Place the updated xlsx in a known path, then re-run the build script
# from the conversation that produced this folder (see git blame).
```

## Known follow-ups

- **Prices**: only the Powders sheet had prices. Tea and botanical
  rows have `Variant Price` empty — merchant fills these in Shopify admin
  or via a follow-up CSV.
- **Variant SKUs**: empty across the board. Add in admin or a follow-up.
- **Body HTML**: empty. Each product needs a description; recommend
  writing in admin to match the brand voice rather than auto-generating.
- **Images**: not included. Matrixify can attach images via an `Image Src`
  column pointing at public URLs; add when image library is ready.
- **Typos in source data**: "Japnese Hojicha", "Rhodioba" URL handle — left
  as-is so the import matches the source spreadsheet. Fix in admin or in
  the source xlsx and re-run.
- **Sheet name mismatches**: Excel uses "Wind down" (lowercase d) for one
  function; the homepage rituals row uses "Wind Down". The CSV mirrors the
  Excel spelling; rename in admin if you want the title-cased version live.
