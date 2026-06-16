# Divine Ingredients Theme — Project Status

Quick-start brief for resuming work in a new conversation. Last updated end of session 2026-06-16.

---

## What this is

Shopify theme rebuild for **Divine Ingredients** (organic tea + superfood + botanicals brand). Base is the **Flux v2.2.0** premium theme by Mana Themes; we've layered a custom design system on top.

- **Brand**: Forest green + beige palette. Cormorant serif + Jost sans. "Honest ingredients. Nothing more."
- **Repo**: `TimKDM/Divine-ingredients-theme-file`
- **Working branch**: `claude/dazzling-feynman-HfoxL`
- **Two-way sync**: Theme Editor edits auto-commit to `main` (via Shopify GitHub integration); pushes to `main` auto-pull into the live theme within ~30–90s. Auto-PRs (#142 onward) usually self-merge.
- **PR-only workflow** per user — every change goes through a PR, never push directly to `main`.

## People

- **Tim** (`tim@kingdigitalmarketers.com`) — the engineer running this session.
- **Alisha** — the brand owner / decision maker. Final say on copy + product structure.
- **Preet Bhullar** — Divine's founder, microbiologist (mentioned in the brand story).

## Tech stack

| Layer | What |
|---|---|
| Theme base | Flux v2.2.0 (Mana Themes). Latest is 2.6.0 — see "Open: Flux upgrade" below. |
| Custom CSS | `assets/divine-theme-v4.css` — single ~2.5k-line stylesheet using `.d-*` class convention. Loads **after** Flux base CSS via `layout/theme.liquid` line 311. |
| Custom JS | `assets/divine-theme-v4.js` — small reveal observer. |
| Old v3 stylesheet | **Deleted.** All sections migrated to v4 class naming. |
| Section files | `sections/divine-*.liquid` — every custom section is prefixed `divine-`. Stock Flux sections (header.liquid, footer.liquid, contact-form.liquid, main-product.liquid) are mostly untouched and restyled via CSS overlay. |
| Liquid template JSON | `templates/index.json`, `templates/product.json`, `templates/page.*.json`. Each starts with the auto-generated Shopify comment header (`/* * IMPORTANT ... */`) — use a comment-stripping JSON parser for validation. |

## Color palette (CSS variables in v4 root)

```css
--d-black:    #111410
--d-forest:   #1F3018
--d-mid:      #3C4C30
--d-beige:    #E8E0CC
--d-beige-lt: #F2EDE0
--d-beige-dk: #D4CAAE
--d-white:    #FDFCF8
```

Fonts: `--d-font-serif: Cormorant`, `--d-font-sans: Jost`.

## Homepage section inventory (in render order)

| Section ID | File | Notes |
|---|---|---|
| `divine_hero` | divine-hero.liquid | Full-bleed image **+ uploaded video** (faststart re-encode). Side video uploads land in `divineherovideo.mp4`. |
| `divine_ticker` | divine-trust-bar.liquid | Forest green band — USDA/CCOF/Lab Tested etc. |
| `divine_rituals` | divine-categories.liquid | "Your cup, your ritual." 5 By-Function tiles (Immunity / Wind Down / Gut Reset / Focus & Energy / Detox). Text clamp to 2 lines + heavy gradient overlay for contrast. |
| `divine_powders` | divine-powders.liquid | Daily superfoods split. **Now supports 2×2 collage** (image_2/3/4 fields). |
| `divine_bestsellers` | divine-products.liquid | Customer Favorites. **Prices hidden** (`show_price: false`). |
| `divine_story` | divine-brand-story.liquid | Founder story with Preet photo. |
| `divine_discovery` | divine-discovery.liquid | **The Chai Edit**. Content-LEFT, **2×2 collage RIGHT**, side_image (Chai seal/logo) sits inline with the heading. |
| `divine_newsletter` | divine-newsletter.liquid | 20% off signup. |
| `divine_certs` | divine-cert-bar.liquid | Black band with 8 cert logos. |
| `divine_b2b` | divine-wholesale.liquid | Wholesale & trade accounts pills. |

All sections have **explicit `background_color`** values set in `templates/index.json` (not transparent) — see the bg-bug note below.

## Working PRs / branch state

- Branch `claude/dazzling-feynman-HfoxL` is the source of truth. Latest commit at end of session: `372652a`.
- Recent merged PRs: #141 (PDP form + spacing fixes), #143 (homepage polish + v3→v4 migration + hero video), #146 (v3 delete + Matrixify v1), plus a long string of `Update from Shopify for theme` auto-sync commits.
- **Open work since last merge**: tons of small commits accumulated on the branch. Consider opening a PR to roll them into `main` early in the new thread.

## Critical conventions to remember

1. **Always use a PR** — user said "always do a PR push." Never `git push` directly to `main`.
2. **Shopify auto-syncs back to GitHub.** If you edit a file then Shopify also pushes a new commit, you'll hit a merge conflict on push. Standard fix: `git pull --rebase origin claude/dazzling-feynman-HfoxL`, resolve any conflict, re-push.
3. **Background-color setting bug**: Shopify color picker returns `rgba(0,0,0,0)` (not blank) when no color is chosen. Every section that consumes `section.settings.background_color` uses the `!= blank and != 'rgba(0,0,0,0)'` pattern — keep that pattern in mind when adding new sections.
4. **Em dashes are banned** from customer-visible copy per Alisha. Use periods or commas. Mac autocorrect re-inserts them silently; merchant was told to disable "smart dashes" in System Settings.
5. **PNG logo is transparent**, not a white card. Light backgrounds only for the header — dark green header makes the DIVINE letters disappear.

## Matrixify bulk-import files (in `matrixify/`)

| File | Purpose |
|---|---|
| **`divine-bulk-import.xlsx`** | **Recommended.** One file, 3 sheets (Products 76 / Smart Collections 17 / Menus 17). Drop into Matrixify Import. |
| `products-update.csv` | 36 tag-only MERGE rows for existing products |
| `products-descriptions.csv` | 62 products with Body HTML + 4 metafields (tasting_notes, best_enjoyed, origin, tea_type) |
| `products-new.csv` | 8 new draft products (Pumpkin Chai, Tulsi Chai, Herbal Chai, Kashmiri Green Chai, Sweetened Matcha, Ube Matcha, Unflavoured Black Iced Tea, Crimsonberry Tea) |
| `collections.csv` | 17 smart collections (5 By Function, 7 By Type incl. legacy Hemp/Oolong + Boba Boba, 5 category-level) |
| `menus.csv` | Main menu structure |

**Before importing**: Alisha needs to create 11 metafield definitions in Shopify admin (Settings → Custom data → Products). Listed in `matrixify/README.md`.

## PDP metafields (full list)

Custom namespace, populated by Matrixify import:

- `tea_type` (single line)
- `ingredients` (multi line)
- `tasting_notes` (single line)
- `best_enjoyed` (single line)
- `aroma` (single line)
- `liquor_colour` (single line)
- `certifications` (single line)
- `contains_caffeine` (single line)
- `origin` (single line)
- `allergens` (multi line)
- `storage` (single line)

Rendered in `sections/divine-product-details.liquid` kv_table block. Fallback chain: individual metafields → `custom.product_facts` legacy → section block defaults.

## What's done (highlights)

- Full v3 → v4 class migration. v3 CSS file deleted.
- Homepage rebuilt with all 10 sections matching the mockup direction.
- Hero gains local video upload (re-encoded from 4K fragmented MP4 → 1080p H.264 with faststart).
- Header → light cream with dark menu text (logo PNG is transparent).
- All 13 sections fixed for the `rgba(0,0,0,0)` transparent-bg bug.
- All sections have explicit background_color values for editor visibility.
- All em dashes removed (166 across 34 files); CSS comments included.
- Purple/lavender → forest green/beige palette (42 swaps across 10 files).
- Header social icons rebuilt as SVG (Instagram, TikTok, Pinterest, Facebook, YouTube, LinkedIn, X).
- Discovery section now: content-LEFT, 2×2 collage RIGHT, side image inline with heading, 30% smaller padding.
- Powders section: collage option matching Discovery.
- Bestsellers section: prices hidden via `show_price: false`.
- Rituals tiles: balanced via line-clamp + min-height; strong contrast overlay for bright tea-leaf images.
- Contact form: stock Flux restyled via CSS overlay in v4.
- PDP: certs removed from description blocks; metafields integrated.
- Wholesale section: typography matches other sections; caption removed; "organic" dropped from copy.
- Body copy for 62 products integrated from Alisha's Product Descriptions sheet.

## Open / waiting on

| Item | Status |
|---|---|
| **Flux 2.6.0 upgrade** | Need merchant to download the 2.6.0 ZIP from Mana Themes (their license) and provide it. Then three-way merge: 2.2.0 → 2.6.0 → our customizations. See conversation 2026-06-16 for detailed merge plan. |
| **2 of 8 draft products** | Pumpkin Chai BT and Kashmiri Green Chai — drafts created, body copy still needed |
| **Boba Boba** | Type/collection exists, no products tagged yet |
| **Hemp Tea / Oolong Tea collections** | Kept with "planned for removal" note. Delete in future cleanup. |
| **Logo placeholder filename** | `side_image` in templates/index.json points to `logo-divine-ingredients-2026.png`. If merchant uploaded under a different name, fix in Theme Editor or update the JSON. |
| **Matrixify metafield definitions** | Alisha needs to create the 11 `custom.*` definitions in Shopify admin before the bulk import. |

## File structure cheat sheet

```
assets/
  divine-theme-v4.css       <- master stylesheet, .d-* classes
  divine-theme-v4.js        <- reveal observer
  base.css                  <- Flux base (untouched)
config/
  settings_data.json        <- theme settings + color schemes
  settings_schema.json      <- theme settings panel definition
layout/
  theme.liquid              <- main wrapper; loads CSS in order: base → v4
locales/
  en.default.json + de/es/it
matrixify/
  divine-bulk-import.xlsx   <- one-shot upload
  *.csv                     <- individual sheets
  README.md                 <- upload instructions
sections/
  divine-*.liquid           <- all custom sections (15+ files)
  header.liquid             <- stock Flux, restyled via CSS
  footer.liquid             <- stock Flux, restyled via CSS
  contact-form.liquid       <- stock Flux, restyled via CSS
  main-product.liquid       <- stock Flux PDP
  divine-product.liquid     <- our PDP hero
  divine-product-details.liquid  <- our PDP additional info (kv_table)
snippets/
  divine-*.liquid           <- product tags, collection filters
templates/
  index.json                <- homepage composition
  product.json              <- active PDP template (uses divine_product + divine_product_details)
  page.*.json               <- about, wholesale, etc.
PROJECT.md                  <- this file
```

## How to resume

1. New thread, point at this repo + branch `claude/dazzling-feynman-HfoxL`.
2. Skim this file. Most context is here.
3. If diving into PDPs, also skim `sections/divine-product-details.liquid` for the metafield fallback chain.
4. If diving into homepage sections, skim `templates/index.json` first to see current bg colors + image references.
5. Default model behavior: small commits, PR for each, push to feature branch, let Shopify auto-merge OR explicitly merge via GitHub MCP.

## Last actions in previous session (2026-06-16 17:30–18:00 UTC)

1. Replaced Discovery Set with The Chai Edit (commit `fc2e147`)
2. Fixed the `rgba(0,0,0,0)` transparent-bg bug across 13 sections (commit `97165b0`)
3. Reverted header from forest green back to light cream (logo is transparent PNG, dark green letters disappeared on dark bg) (commit `e1e73f8`)
4. Added 2×2 collage layout to Discovery section, flipped to content-LEFT image-RIGHT (commits `409f1ef`, then later flipped again — content-LEFT in `99885df`)
5. Set explicit hex bg colors for every homepage section in templates/index.json (commit `7745c3b`)
6. Integrated 62 product descriptions + 2 new metafields (tasting_notes, best_enjoyed) (commit `f3dcce3`)
7. Added Discovery side_image slot (Chai seal/logo), shrunk section ~30% (commit `c040d8f`)
8. Added matching 2×2 collage option to Powders section (commit `99885df`)
9. Moved Discovery side image inline with heading + built consolidated `divine-bulk-import.xlsx` (commit `372652a`)
