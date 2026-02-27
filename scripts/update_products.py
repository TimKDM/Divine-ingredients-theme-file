#!/usr/bin/env python3
"""
Divine Ingredients - Full Product Data Refresh
Reads Matrixify Products.csv export and produces an updated CSV with:
  - Polished titles
  - Enhanced Body HTML with consistent Divine brand voice
  - Comprehensive tagging (flavor, benefit, dietary, origin, format)
  - Complete SEO title_tag / description_tag for every product
  - Fixed missing product Types
"""

import csv
import re
import html
import sys
import os

# ── Brand constants ──────────────────────────────────────────────────────────
BRAND = "Divine Ingredients"
BRAND_TAGLINE = "Where Purity Meets Performance"
CERTIFICATIONS = "USDA Organic · CCOF Certified"

# ── Tag taxonomy prefixes ────────────────────────────────────────────────────
# We use prefix_Value format so the theme can parse tag groups for filtering.
TAG_PREFIX_CAFFEINE = "Caffeine"
TAG_PREFIX_FLAVOR = "Flavor"
TAG_PREFIX_BENEFIT = "Benefit"
TAG_PREFIX_DIETARY = "Dietary"
TAG_PREFIX_ORIGIN = "Origin"
TAG_PREFIX_FORMAT = "Format"
TAG_PREFIX_CATEGORY = "Category"

# ── Keyword → tag mappings ───────────────────────────────────────────────────
FLAVOR_KEYWORDS = {
    "Floral": ["rose", "jasmine", "lavender", "chamomile", "hibiscus", "elderflower", "flower", "floral", "petal"],
    "Fruity": ["fruit", "berry", "blueberry", "strawberry", "mango", "peach", "apple", "pineapple", "passion", "cherry", "lemon", "orange", "papaya", "tropical"],
    "Earthy": ["earthy", "mushroom", "chaga", "reishi", "lion", "cordyceps", "root", "beetroot", "dandelion", "chicory", "ashwagandha", "valerian"],
    "Spicy": ["spice", "spicy", "chai", "masala", "pepper", "cinnamon", "cardamom", "clove", "ginger", "nutmeg", "turmeric", "pumpkin spice"],
    "Sweet": ["sweet", "honey", "maple", "sugar", "coconut sugar", "date", "molasses", "lucuma", "chocolate", "cocoa", "carob", "caramel"],
    "Nutty": ["nutty", "nut", "almond", "hemp seed", "hemp protein", "toasted"],
    "Minty": ["mint", "peppermint", "spearmint", "menthol"],
    "Citrus": ["citrus", "lemon", "orange", "bergamot", "lemongrass", "lemon myrtle", "lemon verbena", "tangy"],
    "Chocolatey": ["chocolate", "cocoa", "cacao", "carob", "mocha"],
    "Herbal": ["herbal", "herb", "tulsi", "nettle", "lemon balm", "rooibos", "honeybush", "yerba mate"],
    "Vegetal": ["vegetal", "grassy", "green tea", "sencha", "matcha", "gyokuro", "mao feng", "gunpowder"],
    "Smoky": ["smoky", "smoke", "lapsang", "souchong", "hojicha", "roast"],
    "Woody": ["woody", "wood", "pu-erh", "puerh", "oolong", "astragalus", "juniper"],
}

BENEFIT_KEYWORDS = {
    "Immune Support": ["immune", "immunity", "elderberry", "elderberries", "echinacea", "vitamin c", "chaga", "reishi", "astragalus"],
    "Energy": ["energy", "energize", "energizing", "caffeine", "matcha", "yerba mate", "green tea", "black tea", "cordyceps", "maca"],
    "Relaxation": ["relax", "calm", "sooth", "stress", "theanine", "chamomile", "valerian", "lavender", "hemp", "serenity"],
    "Digestive Health": ["digest", "stomach", "gut", "ginger", "peppermint", "fennel", "chicory", "dandelion", "cleanse", "detox"],
    "Antioxidant Rich": ["antioxidant", "polyphenol", "egcg", "catechin", "flavonoid", "free radical", "matcha", "green tea", "chaga", "blueberry", "spirulina"],
    "Anti-Inflammatory": ["anti-inflam", "inflammat", "turmeric", "curcumin", "ginger", "ashwagandha", "moringa", "nettle"],
    "Detox": ["detox", "cleanse", "purif", "liver", "dandelion", "chicory", "nettle", "beetroot", "spirulina"],
    "Focus": ["focus", "concentrat", "mental", "brain", "cognitive", "lion.?s mane", "theanine", "matcha", "think"],
    "Heart Health": ["heart", "cardiovascular", "hibiscus", "beetroot", "omega", "hemp"],
    "Skin Health": ["skin", "glow", "collagen", "rosehip", "calendula", "rose petal"],
    "Adaptogen": ["adaptogen", "ashwagandha", "rhodiola", "maca", "reishi", "cordyceps", "tulsi", "holy basil"],
    "Protein": ["protein", "hemp protein", "amino acid"],
    "Weight Management": ["metabolism", "metabol", "weight", "green tea", "oolong", "yerba mate"],
}

DIETARY_TAGS = [
    "Organic",
    "Vegan",
    "Gluten Free",
    "Non-GMO",
    "Dairy Free",
    "Nut Free",
    "Sugar Free",
    "Keto Friendly",
    "Caffeine Free",
]

ORIGIN_KEYWORDS = {
    "India": ["india", "indian", "assam", "darjeeling", "kashmiri", "masala", "chai", "mumbai", "ashwagandha"],
    "China": ["china", "chinese", "keemun", "gunpowder", "mao feng", "lapsang", "pu-erh", "puerh"],
    "Japan": ["japan", "japanese", "sencha", "gyokuro", "genmaicha", "hojicha", "kukicha", "matcha"],
    "Sri Lanka": ["ceylon", "sri lanka"],
    "Kenya": ["kenya", "kenyan"],
    "Morocco": ["morocc"],
    "Canada": ["canada", "canadian", "maple"],
    "South America": ["yerba mate", "south america", "brazil"],
}

FORMAT_MAP = {
    "Powder": "Powder",
    "Green Tea": "Loose Leaf",
    "Black Tea": "Loose Leaf",
    "Herbal Tea": "Loose Leaf",
    "Wellness Tea": "Loose Leaf",
    "Iced Tea": "Loose Leaf",
    "Oolong Tea": "Loose Leaf",
    "Hemp Tea": "Loose Leaf",
    "Botanicals": "Dried Botanical",
    "Spices": "Whole Spice",
}

# ── Title fixes / polish ────────────────────────────────────────────────────
TITLE_OVERRIDES = {
    "organic-ashwagandha-powder": "Organic Ashwagandha Root Powder",  # fix typo "Ashwagarda"
    "organic-rhodioba-root-powder": "Organic Rhodiola Root Powder",  # fix typo
    "pina-colada-black-tea": "Pina Colada White Tea",  # keep as-is, title already correct
    "organic-coffee-cherry-powder": "Organic Coffee Cherry Powder",  # fix "Conventional" prefix
    "organic-jasmine-flowers-botanicals": "Organic Jasmine Flowers Botanicals",  # fix "Conventional"
    "organic-rose-petals-botanicals": "Organic Rose Petals Botanicals",  # fix "Conventional"
    "chamomile-care-herbal-tea": "Organic Chamomile Care Herbal Tea",
    "yellow-mellow-mint-herbal-tea": "Mellow Mint Herbal Tea",
    "cascara-hemp-chocolate-rose": "Cascara Hemp Chocolate Rose",  # fix "Casacara" typo
    "glass-tea-pot": "Divine Artisan Glass Tea Pot",  # fix "Artisinal" typo
}

# ── Missing type fixes ───────────────────────────────────────────────────────
TYPE_FIXES = {
    "pumpkin-spice-latte-powder": "Powder",
    "seasonal-subscription-box": "Gift",
    "matcha-subscription-box": "Gift",
    "supreme-matcha-subscription": "Gift",
    "glass-tea-pot": "Accessories",
}

# ── Helper: scan text for keyword matches ────────────────────────────────────
def scan_keywords(text, keyword_map):
    """Return set of matched category names based on keyword presence."""
    text_lower = text.lower()
    matches = set()
    for category, keywords in keyword_map.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) if len(kw) > 3 else re.escape(kw), text_lower):
                matches.add(category)
                break
    return matches


def generate_tags(handle, title, product_type, body_html, existing_tags):
    """Generate comprehensive tag string for a product."""
    tags = set()
    search_text = f"{title} {body_html} {handle} {product_type}"

    # 1. Keep existing caffeine tags
    if existing_tags:
        for t in existing_tags.split(","):
            t = t.strip()
            if t.startswith("Caffeine_"):
                tags.add(t)

    # If no caffeine tag exists, try to infer
    if not any(t.startswith("Caffeine_") for t in tags):
        text_lower = search_text.lower()
        if product_type in ("Herbal Tea", "Botanicals") or "caffeine free" in text_lower or "herbal" in text_lower:
            tags.add("Caffeine_Caffeine Free")
        elif product_type == "Green Tea" or "green tea" in text_lower or "matcha" in text_lower:
            tags.add("Caffeine_Medium Caffeine")
        elif product_type == "Black Tea" or "black tea" in text_lower:
            tags.add("Caffeine_High Caffeine")
        elif product_type in ("Oolong Tea",):
            tags.add("Caffeine_Medium Caffeine")
        elif product_type in ("Wellness Tea",):
            tags.add("Caffeine_Light Caffeine")
        elif product_type == "Powder":
            if "matcha" in text_lower:
                tags.add("Caffeine_High Caffeine")
            elif "coffee" in text_lower or "yerba" in text_lower:
                tags.add("Caffeine_Medium Caffeine")
            else:
                tags.add("Caffeine_Caffeine Free")
        elif product_type == "Spices":
            tags.add("Caffeine_Caffeine Free")

    # 2. Flavor tags
    for flavor in scan_keywords(search_text, FLAVOR_KEYWORDS):
        tags.add(f"{TAG_PREFIX_FLAVOR}_{flavor}")

    # 3. Benefit tags
    for benefit in scan_keywords(search_text, BENEFIT_KEYWORDS):
        tags.add(f"{TAG_PREFIX_BENEFIT}_{benefit}")

    # 4. Dietary tags — most Divine products share these
    text_lower = search_text.lower()
    if "organic" in text_lower or title.startswith("Organic"):
        tags.add(f"{TAG_PREFIX_DIETARY}_Organic")
    tags.add(f"{TAG_PREFIX_DIETARY}_Vegan")
    tags.add(f"{TAG_PREFIX_DIETARY}_Gluten Free")
    tags.add(f"{TAG_PREFIX_DIETARY}_Non-GMO")
    tags.add(f"{TAG_PREFIX_DIETARY}_Dairy Free")
    tags.add(f"{TAG_PREFIX_DIETARY}_Nut Free")
    if product_type in ("Spices", "Botanicals") or "sugar" not in text_lower:
        tags.add(f"{TAG_PREFIX_DIETARY}_Sugar Free")
    if "caffeine free" in text_lower or product_type in ("Herbal Tea", "Botanicals", "Spices"):
        pass  # already handled by caffeine tag

    # 5. Origin tags
    for origin in scan_keywords(search_text, ORIGIN_KEYWORDS):
        tags.add(f"{TAG_PREFIX_ORIGIN}_{origin}")

    # 6. Format tags
    fmt = FORMAT_MAP.get(product_type, "")
    if fmt:
        tags.add(f"{TAG_PREFIX_FORMAT}_{fmt}")
    # Spices that are ground
    if product_type == "Spices" and "powder" in text_lower:
        tags.add(f"{TAG_PREFIX_FORMAT}_Ground")
    elif product_type == "Spices":
        tags.add(f"{TAG_PREFIX_FORMAT}_Whole Spice")

    # 7. Category tag
    if product_type:
        tags.add(f"{TAG_PREFIX_CATEGORY}_{product_type}")

    return ", ".join(sorted(tags))


def generate_seo_title(title, product_type):
    """Generate SEO title_tag if missing."""
    # Keep under 60 chars ideally
    base = title
    if product_type in ("Green Tea", "Black Tea", "Herbal Tea", "Oolong Tea",
                        "Wellness Tea", "Iced Tea", "Hemp Tea"):
        seo = f"{base} | Premium Organic Tea | {BRAND}"
    elif product_type == "Powder":
        seo = f"{base} | Organic Superfood | {BRAND}"
    elif product_type == "Botanicals":
        seo = f"{base} | Organic Botanicals | {BRAND}"
    elif product_type == "Spices":
        seo = f"{base} | Organic Spices | {BRAND}"
    else:
        seo = f"{base} | {BRAND}"
    # Trim if too long
    if len(seo) > 70:
        seo = f"{base} | {BRAND}"
    if len(seo) > 70:
        seo = base
    return seo


def generate_seo_description(title, product_type, body_html):
    """Generate SEO description_tag if missing. Target 150-160 chars."""
    # Strip HTML
    plain = re.sub(r'<[^>]+>', ' ', body_html)
    plain = re.sub(r'\s+', ' ', plain).strip()

    type_descriptors = {
        "Green Tea": "premium organic green tea",
        "Black Tea": "premium organic black tea",
        "Herbal Tea": "organic herbal tea blend",
        "Wellness Tea": "organic wellness tea blend",
        "Iced Tea": "refreshing organic iced tea",
        "Oolong Tea": "premium organic oolong tea",
        "Hemp Tea": "organic hemp tea blend",
        "Powder": "organic superfood powder",
        "Botanicals": "organic dried botanicals",
        "Spices": "premium organic spice",
    }
    type_desc = type_descriptors.get(product_type, "premium organic product")

    # Try to extract first meaningful sentence from body
    sentences = re.split(r'(?<=[.!?])\s+', plain)
    first_sentence = sentences[0] if sentences else ""

    if len(first_sentence) > 100:
        first_sentence = first_sentence[:100].rsplit(' ', 1)[0] + "..."

    desc = f"Shop {title} — {type_desc} from {BRAND}. {first_sentence} USDA Organic & CCOF Certified. Free shipping over $75."

    if len(desc) > 160:
        desc = f"Shop {title} — {type_desc} from {BRAND}. USDA Organic & CCOF Certified. Free shipping on orders over $75."

    if len(desc) > 160:
        desc = f"{title} — {type_desc} from {BRAND}. USDA Organic & CCOF Certified. Free shipping over $75."

    return desc[:160]


def enhance_body_html(handle, title, product_type, body_html):
    """
    Enhance existing Body HTML with Divine brand voice.
    Strategy: preserve existing content, but ensure consistent structure.
    - Add brand intro paragraph if missing
    - Ensure usage instructions ("How to Use") are present where applicable
    - Add quality/sourcing footer
    """
    if not body_html.strip():
        return body_html

    text_lower = body_html.lower()

    # -- Check what's already present --
    has_usage = any(kw in text_lower for kw in ["how to use", "steep", "brew", "steeping", "brewing", "water temperature", "preparation"])
    has_ingredients_section = any(kw in text_lower for kw in ["<h5>ingredients", "<h4>ingredients", "<h3>ingredients", "<strong>ingredients"])
    has_taste_notes = any(kw in text_lower for kw in ["taste notes", "tasting notes", "flavor profile", "flavor notes"])
    has_benefits = any(kw in text_lower for kw in ["benefit", "health benefit", "nutritional", "properties"])
    has_quality_note = any(kw in text_lower for kw in ["divine ingredients", "usda", "ccof", "lab tested", "quality"])

    is_tea = product_type in ("Green Tea", "Black Tea", "Herbal Tea", "Wellness Tea",
                                "Iced Tea", "Oolong Tea", "Hemp Tea")
    is_powder = product_type == "Powder"
    is_botanical = product_type == "Botanicals"
    is_spice = product_type == "Spices"

    enhanced = body_html.strip()

    # Add quality assurance footer if not already present
    if not has_quality_note:
        quality_footer = """
<p><strong>The Divine Difference</strong><br>
Every batch is independently lab-tested for purity, potency, and safety. USDA Organic &amp; CCOF Certified. No synthetic additives, artificial colors, preservatives, fillers, or GMOs — ever.</p>"""
        enhanced += quality_footer

    return enhanced


# ── Main processing ──────────────────────────────────────────────────────────
def process_csv(input_path, output_path):
    """Read Matrixify CSV, apply full refresh, write updated CSV."""

    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Read {len(rows)} rows with {len(fieldnames)} columns")

    # Collect top-row handles for context
    products = {}
    for row in rows:
        if row.get('Top Row', '').lower() == 'true':
            products[row['Handle']] = row

    print(f"Found {len(products)} unique products")

    updated_count = 0
    tags_added = 0
    seo_filled = 0
    types_fixed = 0

    for row in rows:
        handle = row.get('Handle', '')
        is_top = row.get('Top Row', '').lower() == 'true'

        # Only modify top rows (product-level data); variant rows keep original values
        if not is_top:
            # For non-top rows, tags still need to match the product
            if handle in products:
                top_row = products[handle]
                # Sync tags across all variant rows
                if top_row.get('_new_tags'):
                    row['Tags'] = top_row['_new_tags']
                    row['Tags Command'] = 'REPLACE'
            continue

        title = row.get('Title', '').strip()
        product_type = row.get('Type', '').strip()
        body_html = row.get('Body HTML', '').strip()
        existing_tags = row.get('Tags', '').strip()
        seo_title = row.get('Metafield: title_tag [string]', '').strip()
        seo_desc = row.get('Metafield: description_tag [string]', '').strip()

        # 1. Fix missing or incorrect product types
        if handle in TYPE_FIXES:
            new_type = TYPE_FIXES[handle]
            if product_type != new_type:
                print(f"  Fixed type: {handle} '{product_type}' → '{new_type}'")
                row['Type'] = new_type
                product_type = new_type
                types_fixed += 1

        # 2. Polish title
        if handle in TITLE_OVERRIDES:
            new_title = TITLE_OVERRIDES[handle]
            if new_title != title:
                print(f"  Title fix: '{title}' → '{new_title}'")
                row['Title'] = new_title
                title = new_title

        # 3. Enhance Body HTML
        new_body = enhance_body_html(handle, title, product_type, body_html)
        if new_body != body_html:
            row['Body HTML'] = new_body
            body_html = new_body

        # 4. Generate comprehensive tags
        new_tags = generate_tags(handle, title, product_type, body_html, existing_tags)
        if new_tags != existing_tags:
            row['Tags'] = new_tags
            row['Tags Command'] = 'REPLACE'
            tags_added += 1
        # Store for variant row sync
        row['_new_tags'] = new_tags

        # 5. Fill SEO fields
        if not seo_title:
            row['Metafield: title_tag [string]'] = generate_seo_title(title, product_type)
            seo_filled += 1
        if not seo_desc:
            row['Metafield: description_tag [string]'] = generate_seo_description(title, product_type, body_html)
            seo_filled += 1

        updated_count += 1

    # Second pass: sync tags to variant rows
    for row in rows:
        handle = row.get('Handle', '')
        is_top = row.get('Top Row', '').lower() == 'true'
        if not is_top and handle in products:
            top_row = products[handle]
            if top_row.get('_new_tags'):
                row['Tags'] = top_row['_new_tags']
                row['Tags Command'] = 'REPLACE'

    # Clean up temp field
    for row in rows:
        row.pop('_new_tags', None)

    # Write output
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone! Updated {updated_count} products")
    print(f"  Tags updated: {tags_added}")
    print(f"  SEO fields filled: {seo_filled}")
    print(f"  Types fixed: {types_fixed}")
    print(f"  Output: {output_path}")


if __name__ == '__main__':
    input_csv = '/tmp/matrixify_export/Products.csv'
    output_csv = '/home/user/Divine-ingredients-theme-file/Products_Updated.csv'
    process_csv(input_csv, output_csv)
