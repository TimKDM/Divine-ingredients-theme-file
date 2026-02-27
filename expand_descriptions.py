#!/usr/bin/env python3
"""
Expand truncated product descriptions from Shopify CSV export.

Each description gets:
1. The existing intro paragraph (cleaned up, completed if cut off)
2. Taste Notes (complete)
3. Ingredients (complete)
4. Steeping/How to Use instructions (based on product type)
5. The Divine Difference quality section
"""

import csv
import re

# ---------------------------------------------------------------------------
# Standard sections by product type
# ---------------------------------------------------------------------------

STEEPING = {
    'Black Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to a rolling boil at 100°C/212°F. '
        'Infuse tea for 3-5 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Green Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to 80°C/176°F (do not use boiling water). '
        'Infuse tea for 2-3 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Herbal Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to a rolling boil at 100°C/212°F. '
        'Infuse tea for 5-7 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Oolong Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to 90°C/194°F. '
        'Infuse tea for 3-5 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Wellness Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to a rolling boil at 100°C/212°F. '
        'Infuse tea for 5-7 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Iced Tea': (
        'Steeping Instructions For A Divine Cup '
        'Brew a double-strength infusion: heat freshly drawn cold water to 100°C/212°F. '
        'Infuse 2 tsp of loose-leaf tea per cup for 5-7 minutes. '
        'Allow to cool slightly, then pour over a full glass of ice. Sweeten to taste.'
    ),
    'Hemp Tea': (
        'Steeping Instructions For A Divine Cup '
        'Heat freshly drawn cold water to a rolling boil at 100°C/212°F. '
        'Infuse tea for 5-7 minutes. 1 tsp of loose-leaf tea per cup.'
    ),
    'Botanicals': (
        'Steeping Instructions For A Divine Cup '
        'Bring a cup of freshly drawn cold water to a rolling boil at 100°C/212°F. '
        'Infuse for 5-6 minutes. 1 tablespoon of loose-leaf tea per cup.'
    ),
}

DIVINE_DIFFERENCE = (
    'The Divine Difference '
    'Every batch is independently lab-tested for purity, potency, and safety. '
    'USDA Organic & CCOF Certified. '
    'No synthetic additives, artificial colors, preservatives, or fillers.'
)

# ---------------------------------------------------------------------------
# Complete product data: taste notes + ingredients for ALL products
# This ensures no truncated fragments remain.
# ---------------------------------------------------------------------------

PRODUCT_DATA = {
    'apple-mint-green-tea': {
        'taste_notes': 'Minty, Apple, Light, Refreshing',
        'ingredients': 'Organic Green Tea, Peppermint, Apple Pieces, and Natural Flavors',
    },
    'apple-papaya-island-herbal': {
        'taste_notes': 'Subtle Minty, Apple, Light',
        'ingredients': 'Organic Hibiscus, Apple Pieces, Papaya Pieces, Peppermint, and Natural Flavors',
    },
    'cascara-hemp-chocolate-rose': {
        'taste_notes': 'Coffee, Chocolate, Floral',
        'ingredients': 'Organic Cascara, Organic Cocoa Shells, Rose Petals, and Hemp Seeds',
    },
    'ceremonial-matcha': {
        'taste_notes': 'Smooth, Sweet, Umami',
        'ingredients': 'Organic Japanese Ceremonial Grade Matcha Green Tea Powder',
    },
    'ceylon-black-tea': {
        'taste_notes': 'Brisk, Full Bodied, Honey, Apricot',
        'ingredients': 'Organic Ceylon Black Tea',
    },
    'chamomile-care-herbal-tea': {
        'taste_notes': 'Minty, Floral, Sweet',
        'ingredients': 'Organic Chamomile, Hibiscus, and Lemongrass',
    },
    'china-black-tea': {
        'taste_notes': 'Brisk, Full Bodied, Rich',
        'ingredients': 'Organic Chinese Black Tea',
    },
    'chinese-gunpowder-green-tea': {
        'taste_notes': 'Bold, Slightly Smoky, Vegetal',
        'ingredients': 'Organic Chinese Gunpowder Green Tea',
    },
    'chinese-jasmine-green-tea': {
        'taste_notes': 'Floral, Mellow, Sweet',
        'ingredients': 'Organic Chinese Green Tea scented with Jasmine Blossoms',
    },
    'chinese-keemun-black-tea': {
        'taste_notes': 'Cocoa, Fruity, Floral, Sweet',
        'ingredients': 'Organic Chinese Keemun Black Tea',
    },
    'chinese-lapsang-souchong-black-tea': {
        'taste_notes': 'Bold, Smoky, Campfire',
        'ingredients': 'Organic Chinese Lapsang Souchong Black Tea',
    },
    'chinese-mao-feng-green-tea': {
        'taste_notes': 'Rich, Lightly Sweet, Smokey',
        'ingredients': 'Organic Chinese Green Tea',
    },
    'chocolate-kisses-black-tea': {
        'taste_notes': 'Chocolate, Sweet, Rich',
        'ingredients': 'Organic Assam Black Tea and Organic Cocoa Shells',
    },
    'chocolate-mint-black-tea': {
        'taste_notes': 'Chocolate, Minty, Sweet',
        'ingredients': 'Organic Ceylon Black Tea, Organic Cocoa Shells, and Peppermint',
    },
    'cinnamon-vanilla-zest-herbal-tea': {
        'taste_notes': 'Spicy, Vanilla, Cinnamon',
        'ingredients': 'Organic Honey Bush, Red Rooibos, Cinnamon, and Natural Vanilla Flavors',
    },
    'classic-english-breakfast-black-tea': {
        'taste_notes': 'Smooth, Floral, Sweet',
        'ingredients': 'Organic Assam Black Tea',
    },
    'culinary-matcha': {
        'taste_notes': 'Earthy, Slight Sweet, Robust',
        'ingredients': 'Organic Japanese Green Tea Powder',
    },
    'divine-earl-grey-black-tea': {
        'taste_notes': 'Citrus, Floral, Smooth',
        'ingredients': 'Organic Assam Black Tea, Bergamot Oil, and Rose Petals',
    },
    'divine-ruby-red-iced-tea': {
        'taste_notes': 'Tropical, Aromatic, Fruity',
        'ingredients': 'Organic Rooibos with Hibiscus, Berries, Rosehips, and Natural Flavors',
    },
    'divine-tangy-lemon-iced-tea': {
        'taste_notes': 'Citrus, Tropical, Sweet',
        'ingredients': 'Organic Lemongrass, Citrus Fruits, Lemon Verbena, and Natural Flavors',
    },
    'elderberry-green-tea': {
        'taste_notes': 'Sweet, Fruity, Slight Citrus',
        'ingredients': 'Organic Darjeeling Green Tea with Elderberries, Orange Peel, Hibiscus, and Natural Flavors',
    },
    'energize-hemp-tea': {
        'taste_notes': 'Cocoa, Cinnamon, Energizing',
        'ingredients': 'Organic Hemp Hearts, Coffee Cherry, Cocoa Shells, Cinnamon, and Energizing Spices',
    },
    'fruit-cup-herbal-tea': {
        'taste_notes': 'Light, Fruity, Citrus',
        'ingredients': 'Organic Lemon Peel, Apple Pieces, Cranberry and Papaya Pieces with Natural Flavors',
    },
    'ginger-turmeric-lemongrass-wellness-tea': {
        'taste_notes': 'Pungent, Spicy, Citrus',
        'ingredients': 'Organic Lemon Peel, Lemongrass, Turmeric, and Ginger',
    },
    'glass-tea-pot': {
        'taste_notes': None,
        'ingredients': None,
    },
    'golden-pineapple-oolong-tea': {
        'taste_notes': 'Tropical, Sweet, Smooth',
        'ingredients': 'Organic Oolong Tea with Pineapple Pieces and Natural Flavors',
    },
    'heart-hemp-tea': {
        'taste_notes': 'Turmeric, Ginger, Nutty',
        'ingredients': 'Organic Hemp Hearts, Turmeric, Ginger, and Immune-Boosting Spices',
    },
    'hibiscus-punch-herbal-tea': {
        'taste_notes': 'Tart, Slight Fruity, Thick',
        'ingredients': 'Organic Hibiscus, Cranberries, Blackcurrants, and Natural Flavors',
    },
    'honey-lemon-sunday-green-tea': {
        'taste_notes': 'Lemon, Honey, Fresh',
        'ingredients': 'Organic Sencha, Calendula Petals, and Natural Honey and Lemon Flavors',
    },
    'india-kashmiri-chai-green-tea': {
        'taste_notes': 'Light, Spicy, Aromatic',
        'ingredients': 'Organic Sencha Tea with Ginger Root, Cinnamon and Cardamom Seeds, and Natural Flavors',
    },
    'japanese-genmaicha-green-tea': {
        'taste_notes': 'Savory, Nutty, Light',
        'ingredients': 'Organic Japanese Green Tea with Roasted Brown Rice',
    },
    'japanese-gyokuro-green-tea': {
        'taste_notes': 'Full Body, Sweet, Rich',
        'ingredients': 'Organic Japanese Green Tea',
    },
    'japanese-hojicha-green-tea': {
        'taste_notes': 'Earthy, Smoky, Light',
        'ingredients': 'Organic Japanese Roasted Green Tea',
    },
    'japanese-kukicha-green-tea': {
        'taste_notes': 'Sweet, Slightly Nutty, Fresh',
        'ingredients': 'Organic Japanese Green Tea (Twigs and Stems)',
    },
    'japanese-sencha-green-tea': {
        'taste_notes': 'Vegetal, Light, Slight Sweet',
        'ingredients': 'Organic Japanese Sencha Green Tea',
    },
    'kenyan-black-tea': {
        'taste_notes': 'Brisk, Full Bodied, Rich',
        'ingredients': 'Organic Kenyan Black Tea',
    },
    'lemon-ginger-circus-wellness-tea': {
        'taste_notes': 'Spicy, Sweet, Citrus',
        'ingredients': 'Organic Lemongrass, Ginger, and Licorice',
    },
    'lemon-green-oolong-tea': {
        'taste_notes': 'Fresh, Citrus, Light',
        'ingredients': 'Organic Green Tea with Lemon Myrtle and Natural Flavors',
    },
    'love-potion': {
        'taste_notes': 'Sweet, Floral, Chocolate',
        'ingredients': 'Organic Assam Black Tea, Rose Petals, Cocoa Shells, Strawberry Pieces, and Natural Flavors',
    },
    'magic-of-roses-herbal-tea': {
        'taste_notes': 'Lavender, Tangy, Fruity',
        'ingredients': 'Organic Rose Petals, Apple Bits, Hibiscus, and Natural Vanilla Flavors',
    },
    'mango-turmeric-tulsi-wellness-tea': {
        'taste_notes': 'Mango, Sweet, Lightly Spicy',
        'ingredients': 'Organic Ginger, Licorice, Turmeric, Tulsi, and Natural Mango Flavors',
    },
    'masala-chai-black-tea': {
        'taste_notes': 'Spicy, Warm, Full Bodied',
        'ingredients': 'Organic Assam Black Tea, Ginger, Cinnamon, Cardamom, Cloves, and Black Pepper',
    },
    'matcha-subscription-box': {
        'taste_notes': None,
        'ingredients': 'Organic Supreme Matcha Green Tea Powder (150g per quarterly box)',
    },
    'midnight-mystery-herbal-tea': {
        'taste_notes': 'Thick, Slightly Tart, Fruity',
        'ingredients': 'Organic Hibiscus, Cranberries, Blackcurrants, and Natural Flavors',
    },
    'moroccan-mint-iced-tea': {
        'taste_notes': 'Fresh, Vegetal, Mint',
        'ingredients': 'Organic Moroccan Mint and Green Tea',
    },
    'mumbai-chai': {
        'taste_notes': 'Bold, Spicy, Cardamom',
        'ingredients': 'Organic Assam Black Tea, Cardamom Pods, Ginger, Cinnamon, Cloves, and Black Pepper',
    },
    'organic-anise-star-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Flavor Profile: Immerse in a blend of sweet and peppery with '
            'licorice-reminiscent undertones. '
            'Culinary Versatility: Perfect for savory meat recipes, soups, stews, mulled wines, and baked goods. '
            'Authentically Sourced: Harvested from the lush terrains of southeastern China and Vietnam.'
        ),
    },
    'organic-ashwagandha-powder': {
        'taste_notes': 'Earthy, Slightly Bitter, Sweet Undertones',
        'ingredients': None,
        'product_features': (
            'Authentic Origin: Harvested where it naturally thrives in the wild terrains of India. '
            'Adaptogenic Power: Traditionally used to support stress relief, energy, and overall vitality. '
            'Versatile Use: Add to smoothies, warm beverages, golden milk, or baked goods.'
        ),
    },
    'organic-assam-black-tea': {
        'taste_notes': 'Malty, Robust, Full Bodied',
        'ingredients': 'Organic Assam Black Tea',
    },
    'organic-astragalus-root-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Astragalus Root',
    },
    'organic-beetroot-powder': {
        'taste_notes': 'Earthy, Slightly Bitter',
        'ingredients': None,
        'pairs_well': 'Fruits, Nuts, Smoothies, Juices, Sauces, Baked Goods',
    },
    'organic-black-pepper-powder': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Iconic Flavor: Delight in the warm and spicy undertones of premium black pepper. '
            'Culinary Staple: An indispensable addition to virtually any savory dish. '
            'Authentically Sourced: Harvested from the vast landscapes of India.'
        ),
    },
    'organic-black-pepper-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Bold Flavor: Robust warmth and pungent depth elevate any dish. '
            'Versatile: From seasoning steaks to finishing soups, black pepper is the chef\'s essential. '
            'Heritage Origin: Sourced from the famed Malabar Coast of India.'
        ),
    },
    'organic-blue-spirulina-powder': {
        'taste_notes': 'Bitter',
        'ingredients': None,
        'pairs_well': 'Smoothies, Breakfast Bowls, Lattes, Yogurt',
    },
    'organic-blueberry-powder': {
        'taste_notes': 'Sweet',
        'ingredients': None,
        'pairs_well': 'Yogurt, Oatmeal, Smoothies, Protein Shakes, Baked Goods',
    },
    'organic-calendula-petals-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Calendula Petals',
    },
    'organic-cardamom-powder': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Captivating Taste Notes: Experience the delightful harmony of eucalyptus, mint, and pepper. '
            'Culinary Magic: Transforms curries, desserts, coffee, and baked goods with a touch of exotic warmth. '
            'Authentically Sourced: Descended from the aromatic heartlands of Southern India.'
        ),
    },
    'organic-cardamom-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Distinctive Taste: A symphony of eucalyptus, mint, and pepper flavors. '
            'Versatile Use: Elevates curries, rice dishes, baked goods, coffee, and teas. '
            'Heritage Origin: A close relative of ginger, sourced from Southern India.'
        ),
    },
    'organic-carob-powder': {
        'taste_notes': 'Sweet',
        'ingredients': None,
        'pairs_well': 'Warm Beverages, Baked Goods, Smoothies',
    },
    'organic-chaga-powder': {
        'taste_notes': 'Earthy, Chocolatey, Slightly Bitter',
        'ingredients': None,
    },
    'organic-chamomile-flowers-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Chamomile Flowers',
    },
    'organic-chicory-root-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Chicory Root',
    },
    'organic-cinnamon-powder': {
        'taste_notes': None,
        'ingredients': None,
    },
    'organic-cinnamon-spice': {
        'taste_notes': None,
        'ingredients': None,
    },
    'organic-cleanse': {
        'taste_notes': 'Mint, Sweet, Light',
        'ingredients': 'Organic Nettle Leaves, Peppermint, Dandelion Root, and Lemongrass',
    },
    'organic-cloves-spice': {
        'taste_notes': None,
        'ingredients': None,
    },
    'organic-cocoa-powder': {
        'taste_notes': 'Rich Chocolate',
        'ingredients': None,
        'pairs_well': 'Pineapple, Raspberries, Bananas, Coffee, Yogurt',
    },
    'organic-cocoa-shells-spice': {
        'taste_notes': 'Chocolate, Nutty, Sweet',
        'ingredients': 'Organic Cocoa Shells',
    },
    'organic-coconut-milk-powder': {
        'taste_notes': 'Creamy, Sweet, Coconut',
        'ingredients': None,
    },
    'organic-coconut-sugar': {
        'taste_notes': 'Warm, Caramel-like',
        'ingredients': None,
    },
    'organic-coffee-cherry-powder': {
        'taste_notes': 'Fruity, Slightly Tart',
        'ingredients': None,
    },
    'organic-cordyceps-powder': {
        'taste_notes': 'Savory Umami, Deep Earthy',
        'ingredients': None,
    },
    'organic-cornflower-petals-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Cornflower Petals',
    },
    'organic-cut-rosehips-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Rosehips',
    },
    'organic-daily-detox': {
        'taste_notes': 'Spicy, Slight Sweet, Rich',
        'ingredients': 'Organic Licorice, Organic Cinnamon, Organic Turmeric, Organic Ginger, and Organic Black Pepper',
    },
    'organic-dandelion-root-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Dandelion Root',
    },
    'organic-date-powder': {
        'taste_notes': 'Sweet, Caramel-like',
        'ingredients': None,
    },
    'organic-elderberries-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Elderberries',
    },
    'organic-fennel-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Distinctive Taste: Experience fennel\'s slightly sweet licorice flavor that enriches any dish. '
            'Culinary Versatility: From soups and sausages to cakes and breads, fennel adds warmth and depth. '
            'Heritage Ingredient: Cherished in Chinese, Greek, and Italian cuisines for centuries.'
        ),
    },
    'organic-ginger-powder': {
        'taste_notes': 'Slightly Peppery, Sweet',
        'ingredients': None,
        'pairs_well': 'Sauces, Glazes, Marinades, Stir-Fries, Teas',
    },
    'organic-ginger-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Rich Taste Profile: Immerse yourself in the captivating blend of spicy, warm, and peppery notes. '
            'Culinary Essential: Transforms stir-fries, soups, marinades, and beverages with bold, warming flavor. '
            'Tropical Treasure: Sourced from premium ginger farms for maximum potency.'
        ),
    },
    'organic-green-rooibos-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Green Rooibos',
    },
    'organic-green-spirulina-powder': {
        'taste_notes': 'Earthy',
        'ingredients': None,
        'pairs_well': 'Water, Juice, Smoothies',
    },
    'organic-hemp-berry-infusion': {
        'taste_notes': 'Hibiscus, Fruity, Rich',
        'ingredients': 'Organic Hibiscus, Roasted Hemp Seeds, Berries, and Natural Flavors',
    },
    'organic-hemp-green-tea': {
        'taste_notes': 'Nutty, Smoky, Sweet, Vegetal',
        'ingredients': 'Organic Green Tea and Roasted Hemp Seeds',
    },
    'organic-hemp-protein-powder': {
        'taste_notes': 'Earthy, Nutty, Grassy',
        'ingredients': None,
        'pairs_well': 'Water, Juices, Smoothies, Oatmeal, Pancake Batter, Baked Goods',
    },
    'organic-hibiscus-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Hibiscus',
    },
    'organic-honeybush-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Honeybush',
    },
    'organic-immunity-herbal-tea': {
        'taste_notes': 'Herbal, Bold, Warming',
        'ingredients': 'Organic Echinacea, Elderberry, Astragalus Root, Ginger, and Lemongrass',
    },
    'organic-jasmine-flowers-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Jasmine Flowers',
    },
    'organic-juniper-berries-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Juniper Berries',
    },
    'organic-lemon-myrtle-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Lemon Myrtle',
    },
    'organic-lemon-peel-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Lemon Peel',
    },
    'organic-lemon-verbena-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Lemon Verbena',
    },
    'organic-lemongrass-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Lemongrass',
    },
    'organic-licorice-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Naturally Sweet: Licorice\'s gentle sweetness with undertones of mint and anise adds delicate depth. '
            'Culinary Versatility: Shines in desserts like ice cream, cookies, and cakes, as well as savory dishes. '
            'Traditional Remedy: Used for centuries to support digestive health and soothe the throat.'
        ),
    },
    'organic-lions-mane-powder': {
        'taste_notes': 'Slight Meaty, Earthy',
        'ingredients': None,
        'pairs_well': 'Warm Beverages, Smoothies, Soups, Post-Workout Shakes',
    },
    'organic-lucumapowder': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'Nature\'s Delight: A cherished natural sweetener with a warm, caramel-like flavor. '
            'Versatile Use: Perfect for smoothies, baked goods, ice cream, and breakfast bowls. '
            'South American Heritage: Hailing from the golden fruit of lucuma trees.'
        ),
    },
    'organic-maca-powder': {
        'taste_notes': 'Nutty, Butterscotch Undertones',
        'ingredients': None,
    },
    'organic-maple-sugar': {
        'taste_notes': 'Rich, Maple, Sweet',
        'ingredients': None,
    },
    'organic-mesquite-powder': {
        'taste_notes': 'Smoky-Sweet, Earthy',
        'ingredients': None,
    },
    'organic-molasses-powder': {
        'taste_notes': 'Sweet, Dark, Rich',
        'ingredients': None,
    },
    'organic-moringa-powder': {
        'taste_notes': 'Earthy, Slightly Nutty',
        'ingredients': None,
    },
    'organic-nettle-leaves-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Nettle Leaves',
    },
    'organic-nutmeg-spice': {
        'taste_notes': None,
        'ingredients': None,
        'product_features': (
            'A Symphony of Flavors: Nutmeg introduces a rich palette of warm and slightly sweet notes. '
            'Culinary Essential: Perfect for pies, custards, eggnog, and savory dishes like gratins and soups. '
            'Signature Aroma: Its pungent fragrance transforms everyday cooking into something special.'
        ),
    },
    'organic-orange-peel-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Orange Peel',
    },
    'organic-peppermint-leaves-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Peppermint Leaves',
    },
    'organic-pumpkin-powder': {
        'taste_notes': 'Earthy, Slightly Sweet',
        'ingredients': None,
    },
    'organic-reishi-mushroom-powder': {
        'taste_notes': 'Earthy, Slightly Bitter',
        'ingredients': None,
    },
    'organic-rhodioba-root-powder': {
        'taste_notes': 'Delicate Rose, Sweet, Slight Bitter',
        'ingredients': None,
    },
    'organic-rose-petals-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Rose Petals',
    },
    'organic-rose-petals-powder': {
        'taste_notes': 'Floral, Delicate',
        'ingredients': None,
    },
    'organic-rosehips-powder': {
        'taste_notes': 'Floral, Slightly Sweet, Tart Aftertaste',
        'ingredients': None,
    },
    'organic-spearmint-leaves-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Spearmint Leaves',
    },
    'organic-strawberry-powder': {
        'taste_notes': 'Sweet, Slightly Sour',
        'ingredients': None,
    },
    'organic-taro-powder': {
        'taste_notes': 'Earthy, Nutty, Subtly Sweet',
        'ingredients': None,
    },
    'organic-tart-cherries-powder': {
        'taste_notes': 'Sweet, Sour',
        'ingredients': None,
        'pairs_well': 'Oatmeal, Smoothies, Teas',
    },
    'organic-theanine-powder': {
        'taste_notes': 'Very Faint, Neutral',
        'ingredients': None,
    },
    'organic-tulsi-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Tulsi (Holy Basil)',
    },
    'organic-turmeric-herbal-tea': {
        'taste_notes': 'Sweet, Pungent, Spicy',
        'ingredients': 'Organic Turmeric and Black Pepper',
    },
    'organic-turmeric-powder': {
        'taste_notes': 'Pungent, Earthy-Sweet',
        'ingredients': None,
        'pairs_well': 'Curry Powders, Mustards, Butters, Cheeses, Rice, Soups',
    },
    'organic-turmeric-spice': {
        'taste_notes': None,
        'ingredients': None,
    },
    'organic-valerian-root-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Valerian Root',
    },
    'organic-yerba-mate-botanicals': {
        'taste_notes': None,
        'ingredients': 'Organic Yerba Mate',
    },
    'passion-berry-iced-tea': {
        'taste_notes': 'Fruity, Tropical, Refreshing',
        'ingredients': 'Organic Green Tea, Passion Fruit Pieces, Berry Blend, and Natural Flavors',
    },
    'peach-mango-tango-green-tea': {
        'taste_notes': 'Fruity, Tropical, Aromatic',
        'ingredients': 'Organic Sencha with Mango Pieces and Natural Flavors',
    },
    'peach-mango-tango-iced-tea': {
        'taste_notes': 'Fruity, Tropical, Aromatic',
        'ingredients': 'Organic Sencha with Mango Pieces and Natural Flavors',
    },
    'peach-oolong-tea': {
        'taste_notes': 'Peach, Light, Sweet',
        'ingredients': 'Oolong Tea with Orange Peel, Pineapple Bits, and Natural Flavors',
    },
    'pina-colada-black-tea': {
        'taste_notes': 'Coconut, Tropical, Light',
        'ingredients': 'Organic White Tea, Coconut Pieces, and Natural Flavors',
    },
    'pu-erh-black-tea': {
        'taste_notes': 'Earthy, Woody, Rich',
        'ingredients': 'Organic Chinese Pu-erh Black Tea',
    },
    'pumpkin-spice-black-tea': {
        'taste_notes': 'Smooth, Warm, Spicy',
        'ingredients': 'Organic Kenyan Black Tea, Cinnamon, Ginger, Nutmeg, Cloves, and Natural Flavors',
    },
    'pumpkin-spice-latte-powder': {
        'taste_notes': 'Warming Spice, Sweet, Earthy',
        'ingredients': 'Organic Pumpkin Powder, Cinnamon, Ginger, Nutmeg, Cloves, and Maple Sugar',
    },
    'rainbow-rain-green-tea': {
        'taste_notes': 'Tropical, Floral, Sweet High Notes',
        'ingredients': 'Organic Sencha with Elderberries, Blackcurrant, Blueberries, Calendula Petals, and Natural Flavors',
    },
    'red-roses-black-tea': {
        'taste_notes': 'Floral, Sweet, Slight Astringent',
        'ingredients': 'Organic Black Tea, Rose Petals, and Hibiscus',
    },
    'relax-hemp-tea': {
        'taste_notes': 'Floral, Earthy, Soothing',
        'ingredients': 'Organic Hemp Hearts, Chamomile, Lavender, Valerian Root, and Passionflower',
    },
    'roots-and-chai-wellness-tea': {
        'taste_notes': 'Earthy Coffee Notes, Nutmeg, Spicy',
        'ingredients': 'Organic Chicory Root, Dandelion, Nutmeg, Ginger, Cinnamon, and Cardamom',
    },
    'seasonal-subscription-box': {
        'taste_notes': None,
        'ingredients': None,
    },
    'serenity-wellness-tea': {
        'taste_notes': 'Citrus, Sweet, Salty End Notes',
        'ingredients': 'Organic Rooibos, Honeybush, Lemongrass, Licorice, Lemon Myrtle, and Sea Salt',
    },
    'supreme-matcha': {
        'taste_notes': 'Sweet, Umami, Smooth',
        'ingredients': 'Organic Japanese Supreme Grade Matcha Green Tea Powder',
    },
    'supreme-matcha-subscription': {
        'taste_notes': None,
        'ingredients': 'Organic Supreme Matcha Green Tea Powder (delivered monthly)',
    },
    'think-hemp-tea': {
        'taste_notes': 'Spiced Chai, Earthy, Warming',
        'ingredients': 'Organic Hemp Hearts, Cinnamon, Cardamom, Ginger, Black Pepper, and Cognitive-Supporting Spices',
    },
    'tropical-passion-herbal-tea': {
        'taste_notes': 'Passion Fruit, Tropical, Sweet',
        'ingredients': 'Organic Hibiscus, Cranberries, Rosehips, and Natural Passion Fruit Flavors',
    },
    'tropical-sunshine-green-tea': {
        'taste_notes': 'Rich, Pineapple, Aromatic',
        'ingredients': 'Organic Sencha with Orange Peel, Pineapple Pieces, Calendula Petals, and Natural Flavors',
    },
    'wine-berry-herbal-iced-tea': {
        'taste_notes': 'Full Body, Fruity, Hibiscus',
        'ingredients': 'Hibiscus, Rosehips, Blackcurrant, Cranberries, and Natural Flavors',
    },
    'wine-berry-herbal-tea': {
        'taste_notes': 'Full Body, Fruity, Hibiscus',
        'ingredients': 'Hibiscus, Rosehips, Blackcurrant, Cranberries, and Natural Flavors',
    },
    'yellow-mellow-mint-herbal-tea': {
        'taste_notes': 'Minty, Citrus, Floral',
        'ingredients': 'Organic Chamomile, Rosehips, Lemongrass, and Orange Peels',
    },
}

# ---------------------------------------------------------------------------
# Custom intro overrides for products with no intro or bad intros
# ---------------------------------------------------------------------------

CUSTOM_INTROS = {
    'organic-cocoa-shells-spice': (
        'The outer shell of the cocoa bean, organic cocoa shells brew into a light, '
        'chocolatey infusion with naturally sweet undertones. Rich in antioxidants and '
        'completely caffeine-free, cocoa shells make a wonderful alternative to hot '
        'chocolate or can be added to tea blends for depth and warmth. Their subtle '
        'nutty sweetness pairs beautifully with cinnamon, vanilla, or chili.'
    ),
    'organic-spearmint-leaves-botanicals': (
        'A milder, sweeter cousin of peppermint, organic spearmint leaves produce a '
        'naturally refreshing and soothing cup. Known for its gentle mint flavor without '
        'the intense cooling sensation of peppermint, spearmint is perfect on its own or '
        'blended into herbal teas. Spearmint has been used for centuries to support '
        'digestive health and freshen the palate.'
    ),
    'organic-tulsi-botanicals': (
        'Also known as Holy Basil, Tulsi has been revered in Ayurvedic medicine for '
        'centuries as the "Queen of Herbs." This aromatic botanical produces a soothing, '
        'slightly spicy cup with notes of clove and lemon. Celebrated as an adaptogen, '
        'Tulsi helps the body manage stress naturally while delivering a complex, '
        'herbaceous flavor that deepens with every sip.'
    ),
    'organic-valerian-root-botanicals': (
        'A time-honored herbal remedy, Valerian Root has been used for centuries to '
        'promote restful sleep and calm the mind. Its earthy, woody flavor brews into a '
        'deeply relaxing cup, making it a perfect addition to your evening routine. '
        'Valerian is one of the most well-researched botanicals for supporting natural, '
        'restorative rest.'
    ),
    'ceremonial-matcha': (
        "Our Ceremonial Matcha Powder is a first-harvest Japanese "
        "green tea crafted for tea ceremonies and mindful sipping. Stone-ground from "
        "shade-grown tencha leaves, this vibrant green powder delivers a naturally "
        "sweet, umami-rich flavor with zero bitterness. Packed with L-theanine for "
        "calm focus and antioxidants for whole-body wellness, our ceremonial grade "
        "matcha is the purest way to experience Japanese tea culture at home. Simply "
        "whisk with hot water for a smooth, frothy cup."
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def trim_to_last_sentence(text):
    """Trim text to the last complete sentence."""
    text = text.strip()
    if not text:
        return text
    # If text already ends with sentence punctuation, return as-is
    if text[-1] in '.!?':
        return text
    # Find the last sentence-ending punctuation
    last_period = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    if last_period > 0:
        return text[:last_period + 1]
    # No sentence boundary found - add a period
    # But first remove any trailing incomplete word
    text = text.rstrip()
    # If the last character is a letter and the text is cut off, try to find
    # the last space and trim there
    if text and text[-1].isalpha():
        last_space = text.rfind(' ')
        if last_space > len(text) * 0.5:  # Only trim if we're not losing too much
            text = text[:last_space].rstrip(',').rstrip()
    if text and text[-1] not in '.!?':
        text += '.'
    return text


def clean_trailing(text):
    """Remove trailing truncation markers like '...' or '..'"""
    text = text.strip()
    text = re.sub(r'\.{2,}$', '', text)
    text = text.rstrip(',').strip()
    return text


def extract_intro(desc):
    """Extract the intro paragraph (everything before the first section marker)."""
    # Section markers that indicate end of intro
    # Use negative lookbehind to avoid matching "Divine Ingredients" brand name
    markers = [
        r'Taste Notes?\s',
        r'(?<!Divine )Ingredients\s+(?:Organic|[A-Z])',
        r'Pairs well with',
        r'Product Features',
        r'Steeping Instructions',
        r'The Divine Difference',
        r'How to Use',
        r'Energy Benefits',
        r'Exceptional Nutrition',
    ]

    earliest_pos = len(desc)
    for pattern in markers:
        match = re.search(pattern, desc)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()

    intro = desc[:earliest_pos].strip()
    return intro


def needs_custom_intro(handle, intro):
    """Check if this product needs a custom intro paragraph."""
    if not intro:
        return True
    if intro.startswith('Steeping Instructions'):
        return True
    if intro.startswith('{'):  # JSON-LD
        return True
    if len(intro) < 30:
        return True
    return False


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_description(handle, title, type_, tags, raw_desc):
    """Build a complete, non-truncated description for any product."""
    desc = clean_trailing(raw_desc.strip())

    # Fix moroccan mint duplicate text
    if handle == 'moroccan-mint-iced-tea':
        # Keep only up to first "Taste Notes" section
        match = re.search(r'Taste Notes', desc)
        if match:
            desc = desc[:match.start()].strip()

    # Extract intro
    intro = extract_intro(desc)

    # Check if we need a custom intro
    if needs_custom_intro(handle, intro):
        if handle in CUSTOM_INTROS:
            intro = CUSTOM_INTROS[handle]

    # Clean up the intro
    intro = trim_to_last_sentence(clean_trailing(intro))

    # Get product data (complete taste notes + ingredients)
    pdata = PRODUCT_DATA.get(handle, {})

    # Build the full description
    parts = []

    # 1. Intro paragraph
    if intro:
        parts.append(intro)

    # 2. Product Features (for spices/powders that use this format)
    pf = pdata.get('product_features', '')
    if pf:
        parts.append(f'Product Features: {pf}')

    # 3. Taste Notes
    taste = pdata.get('taste_notes', '')
    if taste:
        parts.append(f'Taste Notes: {taste}')

    # 4. Ingredients
    ingr = pdata.get('ingredients', '')
    if ingr:
        parts.append(f'Ingredients: {ingr}')

    # 5. Pairs well with
    pairs = pdata.get('pairs_well', '')
    if pairs:
        parts.append(f'Pairs well with: {pairs}')

    # 6. Steeping Instructions (for tea/botanical types)
    steeping = STEEPING.get(type_, '')
    if steeping:
        parts.append(steeping)

    # 7. The Divine Difference
    parts.append(DIVINE_DIFFERENCE)

    return ' '.join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    input_file = 'Products_Consolidated (1).csv'
    output_file = 'Products_Consolidated_Full.csv'

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)

        desc_col = 'Description (Summary)'
        new_desc_col = 'Description'
        new_fieldnames = [new_desc_col if col == desc_col else col for col in fieldnames]

        rows = []
        for row in reader:
            handle = row.get('Handle', '')
            title = row.get('Title', '')
            type_ = row.get('Type', '')
            tags = row.get('Tags', '')
            raw_desc = row.get(desc_col, '')

            full_desc = build_description(handle, title, type_, tags, raw_desc)

            new_row = {}
            for key in fieldnames:
                if key == desc_col:
                    new_row[new_desc_col] = full_desc
                else:
                    new_row[key] = row[key]
            rows.append(new_row)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed {len(rows)} products -> {output_file}")

    # Show stats
    total_chars = sum(len(row[new_desc_col]) for row in rows)
    avg_chars = total_chars // len(rows)
    print(f"Total description chars: {total_chars:,}")
    print(f"Average description length: {avg_chars} chars")

    # Show some samples
    samples = [
        'apple-mint-green-tea',
        'ceremonial-matcha',
        'organic-cocoa-shells-spice',
        'organic-tulsi-botanicals',
        'moroccan-mint-iced-tea',
        'organic-ashwagandha-powder',
        'organic-anise-star-spice',
        'masala-chai-black-tea',
        'glass-tea-pot',
        'matcha-subscription-box',
    ]
    print("\n" + "=" * 70)
    for row in rows:
        if row['Handle'] in samples:
            print(f"\n--- {row['Handle']} ({row['Type']}) ---")
            print(row[new_desc_col])
            print(f"[{len(row[new_desc_col])} chars]")


if __name__ == '__main__':
    main()
