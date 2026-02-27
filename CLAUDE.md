# Divine Ingredients — Shopify Theme Project

## What This Is

Custom Shopify theme for [Divine Organic Ingredients](https://divineingredients.com), a USDA/CCOF-certified organic tea, spice, powder, and botanical company. The store at `divine-ingredients.myshopify.com` sells 146 products across 10 categories: Black Tea, Green Tea, Herbal Tea, Oolong Tea, Wellness Tea, Iced Tea, Hemp Tea, Botanicals, Spices, Powders, Accessories, and Gifts.

## Brand Voice

Hip, warm, people-first, facts-driven. Inspired by the owners' natural tone (Blue Ocean Tea background). Key tagline: **"Where Purity Meets Performance."** Descriptions should feel conversational but informative — never corporate or stiff.

## Branch History

All theme work originated on `claude/update-theme-mock-1ql7A` (35+ PRs merged). That branch was merged into the current working branch. Key milestones:

1. Homepage rebuilt from `Divine_Homepage_Mockup_v3.html` (7 custom divine sections)
2. Brand voice rewrite across all site content
3. USDA/CCOF certification logo bar + integration
4. Product data refresh (titles, SEO, comprehensive tags)
5. Product template: schema markup, "How to Use" section, tag display
6. Full product descriptions expanded from truncated Shopify CSV export

## Repo Structure

```
├── assets/                     # CSS + JS (base.css, global.js, divine-mockup-v3.css, etc.)
├── config/
│   ├── settings_schema.json    # Theme setting definitions
│   └── settings_data.json      # Theme setting values
├── layout/
│   ├── theme.liquid            # Main layout (CSS vars, fonts, head)
│   └── password.liquid
├── sections/                   # 87 total (77 standard + 10 custom divine-*)
├── snippets/                   # 88 total (86 standard + 2 custom divine-*)
├── templates/                  # 25 JSON/Liquid templates
├── locales/                    # Translation files
│
├── Divine_Homepage_Mockup_v3.html   # Reference mockup (the design source of truth)
├── THEME_REWRITE_SECTIONS.md        # Detailed spec for each section rewrite
│
├── Products_Consolidated (1).csv    # Shopify CSV export (descriptions truncated)
├── Products_Consolidated.csv        # Earlier product catalog (one row per product)
├── Products_Consolidated_Full.csv   # ← CURRENT: all 146 products, full descriptions
├── Products_Updated.csv             # Full Shopify export (116 columns, variant rows)
├── expand_descriptions.py           # Script that generated Full.csv from (1).csv
└── CLAUDE.md                        # This file
```

## Custom Divine Sections

These are the sections built specifically for this theme:

| Section | Purpose |
|---|---|
| `divine-hero.liquid` | Full-bleed hero banner (Art of Tea / Chado style) |
| `divine-categories.liquid` | Tea category cards with circular images |
| `divine-products.liquid` | Featured products grid with collection links |
| `divine-trust-bar.liquid` | USDA/CCOF certification + trust messaging strip |
| `divine-testimonials.liquid` | Customer testimonial carousel |
| `divine-newsletter.liquid` | Email signup section |
| `divine-brand-story.liquid` | Brand story content block |
| `divine-story-page.liquid` | Full brand story page section |
| `divine-contact-us.liquid` | Contact form + info |
| `divine-collection-filters.liquid` | Collection page tag-based filters |

Custom snippets: `divine-product-tags.liquid` (renders benefit/flavor/dietary tags on product pages), `divine-collection-filters.liquid` (reusable filter component).

## Product Catalog

146 products across these types:

| Type | Count | Caffeine | Steeping |
|---|---|---|---|
| Green Tea | ~20 | Light | 80°C, 2-3 min |
| Black Tea | ~18 | High | 100°C, 3-5 min |
| Herbal Tea | ~12 | Caffeine Free | 100°C, 5-7 min |
| Oolong Tea | ~4 | Medium | 90°C, 3-5 min |
| Wellness Tea | ~5 | Medium | 100°C, 5-7 min |
| Iced Tea | ~6 | Light | Double-strength, pour over ice |
| Hemp Tea | ~5 | Varies | 100°C, 5-7 min |
| Powder | ~35 | Varies | N/A (add to beverages/food) |
| Spices | ~12 | Caffeine Free | N/A |
| Botanicals | ~20 | Caffeine Free | 100°C, 5-6 min |
| Accessories | 1 | — | — |
| Gift | 2 | — | — |

Tags follow a structured convention: `Benefit_*`, `Caffeine_*`, `Category_*`, `Dietary_*`, `Flavor_*`, `Format_*`, `Origin_*`.

## Product Description Format

Every product description follows this structure (see `expand_descriptions.py`):

1. **Intro paragraph** — Unique copy about the product
2. **Product Features** (spices/powders only) — Bullet-style feature highlights
3. **Taste Notes** — Comma-separated flavor descriptors
4. **Ingredients** — Full ingredient list
5. **Pairs well with** (powders only) — Suggested pairings
6. **Steeping Instructions** — "For A Divine Cup" format, temp + time + amount
7. **The Divine Difference** — Standard quality boilerplate: lab-tested, USDA/CCOF certified, no synthetic additives

## Design Tokens

Defined in `layout/theme.liquid` and `assets/divine-mockup-v3.css`:

```
Colors:  #ffffff (bg), #f7f7f7 (alt bg), #1d1d1d (text), #d4c4d9 (accent), #9b76a7 (accent dark)
Fonts:   Josefin Sans (headings), Jost (body)
Radius:  8px (buttons), 12px (cards), 16px (containers)
```

## What's Left / Known Issues

- Homepage mockup v3 sections are built but `THEME_REWRITE_SECTIONS.md` has more detailed specs that may not all be fully implemented yet
- Some product descriptions were reconstructed from truncated CSV — ingredients were inferred from product names/tags and should be verified against actual Shopify product data
- The `Products_Updated.csv` (116-column Shopify export) has full variant data if needed for bulk import work
