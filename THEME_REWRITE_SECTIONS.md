# Divine Ingredients Theme Rewrite Sections

## Based on: `Divine_Homepage_Mockup_v3.html`

This document defines every section of the Shopify theme that must be rewritten
to match the style, structure, and mobile-first requirements of the HTML mockup v3.

---

## 0. Global Design System Changes

### Files to modify
- `config/settings_data.json` (theme settings values)
- `config/settings_schema.json` (add new setting definitions if needed)
- `layout/theme.liquid` (CSS custom properties in `:root`)
- `assets/base.css` (global resets, typography, base elements)

### 0.1 CSS Custom Properties (Design Tokens)

The mockup defines a strict design token system. The theme's `:root` variables
in `layout/theme.liquid` must be updated or extended to include these:

```css
:root {
  /* Colors — match mockup exactly */
  --color-background: #ffffff;       /* already #ffffff in settings */
  --color-background-alt: #f7f7f7;   /* NEW — used for section-alt backgrounds */
  --color-foreground: #1d1d1d;       /* already #1D1D1D in settings */
  --color-accent: #d4c4d9;           /* exists as scroll_indicator_color */
  --color-accent-dark: #9b76a7;      /* NEW — used for badges, icons, labels */
  --color-text-muted: #666666;       /* NEW — subtitles, meta text, muted copy */
  --color-border: #e8e8e8;           /* already border_color_1 in settings */

  /* Typography */
  --font-heading: 'Josefin Sans', sans-serif;  /* already josefin_sans */
  --font-body: 'Jost', sans-serif;             /* already jost */

  /* Mobile-first spacing scale */
  --spacing-xs: 0.5rem;   /* 8px */
  --spacing-sm: 1rem;     /* 16px */
  --spacing-md: 1.5rem;   /* 24px */
  --spacing-lg: 2rem;     /* 32px */
  --spacing-xl: 3rem;     /* 48px */

  /* Touch-friendly sizing */
  --tap-target: 44px;     /* minimum touch target per WCAG */
  --radius-sm: 8px;       /* buttons, inputs, small cards */
  --radius-md: 12px;      /* product cards, category cards */
  --radius-lg: 16px;      /* large containers */

  /* Transition */
  --transition: all 0.25s ease;
}
```

**Current state:** The theme uses `--spacing-sections-desktop` (60px) and derived
mobile values. The mockup uses a simpler 5-step scale. The existing variables
should remain for backwards compatibility, but the new tokens must be added
alongside them for use in rewritten sections.

**Settings changes (`settings_data.json`):**
- `buttons_radius`: change from `20` to `8` (match `--radius-sm`)
- `global_border_radius`: change from `20` to `12` (match `--radius-md`)
- `global_shadow_opacity`: keep at `0` (mockup uses minimal/no shadows)

### 0.2 Typography Base Styles

**File:** `assets/base.css` (Section 4.1 Base typography)

Current body font-size scales from 1.6rem (mobile) to 1.8rem (desktop).
The mockup uses a flat `16px` base. Changes needed:

| Property            | Current          | Mockup Target       |
|---------------------|------------------|---------------------|
| `body font-size`    | `1.6rem / 1.8rem`| `16px` (1rem)       |
| `body line-height`  | calc-based       | `1.6`               |
| `body letter-spacing`| `0.06rem`       | `0` (remove)        |
| `-webkit-font-smoothing` | not set    | `antialiased`       |
| `overflow-x`        | not set          | `hidden` on body    |

### 0.3 Button Base Styles

**File:** `assets/base.css` (Section 4.3 Buttons)

The mockup defines two button variants. Update the global `.btn` / `.button`
classes:

```
.btn / .button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;          /* --tap-target */
  padding: 14px 24px;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: none;
  border-radius: 8px;        /* --radius-sm */
  cursor: pointer;
  transition: all 0.25s ease;
  width: 100%;               /* full-width on mobile */
}

.btn-primary / .button--primary {
  background: var(--color-foreground);  /* #1d1d1d */
  color: var(--color-background);       /* #ffffff */
}

.btn-secondary / .button--secondary {
  background: transparent;
  color: var(--color-foreground);
  border: 1.5px solid var(--color-foreground);
}

@media (min-width: 768px) {
  .btn / .button {
    width: auto;
    padding: 14px 32px;
  }
}
```

**Key difference:** Current buttons use `--buttons-radius: 20px` (pill shape).
Mockup uses `8px` (subtle rounding). Current primary button is light gray
(`#F2F2F2` bg, `#1D1D1D` text) — mockup inverts this to dark bg, white text.

---

## 1. Announcement Bar Section

### Files to modify
- `sections/announcements.liquid` (if it exists, otherwise `header.liquid` contains it)
- `assets/base.css` (Section 6.1 Announcement Bar)

### Current state
The announcement bar is likely configured within the header section settings or
as a standalone `announcements.liquid` section.

### Mockup requirements

```
Background:  #1d1d1d (--color-foreground) — dark/inverted
Text color:  #ffffff (--color-background)
Padding:     10px 16px
Text align:  center
Font size:   12px
Link color:  #d4c4d9 (--color-accent)
Link style:  underline, text-underline-offset: 2px
```

### Specific CSS changes needed

```css
.announcement-bar {
  background: var(--color-foreground);
  color: var(--color-background);
  padding: 10px 16px;
  text-align: center;
  font-size: 12px;
  letter-spacing: 0.02em;
}

.announcement-bar a {
  color: var(--color-accent);
  text-decoration: underline;
  text-underline-offset: 2px;
}
```

### Content from mockup
`Free Shipping on $75+ · Shop Wholesale`

---

## 2. Header Section

### Files to modify
- `sections/header.liquid`
- `assets/base.css` (Section 6.2 Header)
- `assets/component-menu-drawer.css`

### Mockup requirements

```
Background:     #ffffff
Padding:        12px 16px
Position:       sticky, top: 0, z-index: 100
Border-bottom:  1px solid #e8e8e8
Layout:         flex, space-between, align-center
```

### Layout structure (mobile)
```
[Hamburger Menu]     [DIVINE INGREDIENTS logo]     [Cart icon + badge]
```

### Specific CSS changes

```css
.header {
  background: var(--color-background);
  padding: 12px 16px;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--color-border);
}

/* Logo */
.logo, .header__heading-link {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--color-foreground);
  text-decoration: none;
}

/* Touch-target icons */
.menu-icon, .header-icon,
header-drawer summary, .header__icon {
  width: 44px;   /* --tap-target */
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Icon SVGs */
.header svg {
  width: 24px;
  height: 24px;
  stroke: var(--color-foreground);
  stroke-width: 1.5;
}

/* Cart count badge */
.cart-count-bubble {
  position: absolute;
  top: 6px;
  right: 6px;
  background: var(--color-accent-dark);  /* #9b76a7 — purple */
  color: #fff;
  font-size: 10px;
  font-weight: 600;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Key changes from current
- Current header padding uses dynamic section settings; mockup uses fixed `12px 16px`
- Cart badge changes from theme accent to `--color-accent-dark` (#9b76a7)
- Logo font-size reduced to `16px` (from dynamic logo width image)
- Simplified to 3-element layout on mobile (hamburger, logo, cart)

---

## 3. Hero / Image Banner Section

### Files to modify
- `sections/image-banner.liquid`
- `assets/section-image-banner.css` (if exists, or inline styles)

### Mockup structure
```
[Full-width hero image — 4:3 aspect ratio on mobile]
[Content BELOW image, centered]
  - Badge: "100% Organic · Ethically Sourced"
  - H1: "Elevate Every Recipe"
  - Subtitle paragraph
  - Two CTA buttons stacked vertically on mobile
```

### Key design differences from current
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Content placement   | Overlaid on image          | **Below** the image          |
| Image aspect ratio  | height setting (sm/md/lg)  | `aspect-ratio: 4/3`         |
| Image gradient      | overlay opacity setting    | gradient fallback only       |
| Hero badge          | not present                | pill badge above headline    |
| Heading size        | extra-large (dynamic)      | `28px` mobile, `36px` desktop|
| Heading weight      | 400 with `<strong>` 600    | same                         |
| Button layout       | horizontal                 | vertical stack on mobile     |
| Content padding     | dynamic                    | `24px 20px 32px`             |

### CSS to implement

```css
.hero {
  position: relative;
}

.hero-image {
  width: 100%;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-content {
  padding: 24px 20px 32px;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  background: var(--color-background-alt);  /* #f7f7f7 */
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-accent-dark);  /* #9b76a7 */
  margin-bottom: 12px;
}

.hero h1 {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 400;
  line-height: 1.2;
  margin-bottom: 12px;
}

.hero-subtitle {
  font-size: 15px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
  line-height: 1.6;
}

.hero-cta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 768px) {
  .hero-content { padding: 32px 40px 48px; }
  .hero h1 { font-size: 36px; }
  .hero-cta {
    flex-direction: row;
    justify-content: center;
  }
}
```

### Liquid template changes
- Move `show_text_below` to default `true` for this layout
- Add a new block type `badge` to the schema for the "100% Organic" pill
- Ensure heading renders with `<strong>` wrapping for weight variation
- CTA buttons stack vertically via CSS, not Liquid

---

## 4. Trust Bar Section (Multicolumn)

### Files to modify
- `sections/multicolumn.liquid`
- `assets/section-multicolumn.css` or inline styles

### Mockup structure
```
[Horizontally scrollable row of trust items]
  Each item: [SVG icon] [Bold label + description text]
  Items: USDA Organic | Free Ship on $75+ | 4.9★ Reviews | Bulk Pricing
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Layout              | grid columns               | horizontal scroll strip      |
| Scrollbar           | visible                    | hidden (`display: none`)     |
| Scroll behavior     | none                       | `-webkit-overflow-scrolling: touch` |
| Card style          | cards with backgrounds     | no cards, inline items       |
| Images              | raster images              | inline SVG icons             |
| Bottom border       | none                       | `1px solid #e8e8e8`         |
| Padding             | section padding (36px)     | `16px 0`                    |

### CSS to implement

```css
.trust-bar {
  padding: 16px 0;
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.trust-bar::-webkit-scrollbar {
  display: none;
}

.trust-bar-inner {
  display: flex;
  gap: 24px;
  padding: 0 20px;
  min-width: max-content;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.trust-item svg {
  width: 20px;
  height: 20px;
  stroke: var(--color-accent-dark);
  stroke-width: 1.5;
  flex-shrink: 0;
}

.trust-item span {
  font-size: 12px;
  color: var(--color-text-muted);
}

.trust-item strong {
  color: var(--color-foreground);
  font-weight: 600;
}
```

### Liquid changes needed
- Add a new style variant (e.g., `style-three` or `trust-bar`) to the
  multicolumn section schema
- When this style is active, render as a scrollable flex row instead of grid
- Replace image blocks with inline SVG icon support
- Remove card backgrounds and section padding overrides

---

## 5. Category Grid Section (Collection List)

### Files to modify
- `sections/collection-list.liquid`
- `assets/section-featured-collections.css`
- `snippets/card-collection.liquid` (if card template exists)

### Mockup structure
```
Section header:
  Label: "Shop by Category" (small caps, purple)
  Title: "Explore Our Collections"

Grid: 2 columns mobile, 4 columns desktop
Each card:
  [Square image, full bleed]
  [Gradient overlay from bottom]
  [Title + subtitle overlaid at bottom-left]
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Card style          | varies (3 style options)   | image-overlay with gradient  |
| Card aspect ratio   | configurable               | `1:1` (square)              |
| Text placement      | below image (most styles)  | overlaid on image, bottom   |
| Gradient            | none or overlay opacity    | `linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 60%)` |
| Text color on card  | theme foreground           | white (#fff)                |
| Gap                 | grid spacing settings      | `12px` mobile, `20px` desktop |
| Border radius       | card settings              | `12px` (--radius-md)        |
| Section label       | caption style              | `10px`, `0.15em` spacing, uppercase, purple |

### CSS to implement

```css
.section-header {
  text-align: center;
  margin-bottom: 24px;
}

.section-label {
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-accent-dark);
  margin-bottom: 6px;
}

.section-title {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 400;
  color: var(--color-foreground);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.category-card {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
}

.category-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.category-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 60%);
}

.category-card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  z-index: 2;
  color: #fff;
}

.category-card h3 {
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 2px;
}

.category-card p {
  font-size: 11px;
  opacity: 0.85;
}

@media (min-width: 768px) {
  .category-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
  .section-title { font-size: 28px; }
}
```

### Liquid changes
- Add or select a collection list style that uses the overlay-gradient card pattern
- Section label block should use `--color-accent-dark` for color
- Section title should use `font-weight: 400` (light/regular, not bold)

---

## 6. Best Sellers / Featured Collection Section

### Files to modify
- `sections/featured-collection.liquid`
- `snippets/card-product.liquid`
- `assets/component-card.css`
- `assets/section-featured-collection.css` (if exists)

### Mockup structure
```
Section header:
  Label: "Customer Favorites"
  Title: "Best Sellers"

Horizontal scroll carousel (not grid):
  Each card (200px wide mobile, 240px desktop):
    [Square product image]
    [Optional badge: "Best Seller" or "Sale"]
    [Product title]
    [Product meta: "30g · Premium Japanese"]
    [5 star rating + review count]
    [Price]

Below carousel:
  "View All" secondary button (centered, inline)
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Layout              | grid or slider             | horizontal scroll only       |
| Card width          | column-based               | fixed `200px` / `240px`     |
| Scroll behavior     | slider with arrows         | native scroll-snap           |
| Scrollbar           | visible                    | hidden                       |
| Card shadow         | configurable               | `0 2px 12px rgba(0,0,0,0.06)` |
| Card radius         | `--border-radius` (20px)   | `12px`                      |
| Background          | white                      | `#f7f7f7` (section-alt)     |
| Badge style         | theme badges               | dark bg, 9px uppercase text |
| Sale badge           | theme color scheme         | `#c75050` red               |
| Rating stars        | theme rating component     | inline SVG, `#e5b94e` fill  |
| Product title font  | theme heading              | `13px`, weight 500          |
| Price font size     | theme default              | `14px`, weight 600          |

### CSS to implement

```css
.product-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 0 20px 16px;
  margin: 0 -20px;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
}

.product-scroll::-webkit-scrollbar {
  display: none;
}

.product-card {
  flex: 0 0 200px;
  scroll-snap-align: start;
  background: var(--color-background);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.product-image {
  aspect-ratio: 1;
  position: relative;
  overflow: hidden;
}

.product-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--color-foreground);
  color: #fff;
  padding: 4px 8px;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-radius: 3px;
}

.product-badge.sale {
  background: #c75050;
}

.product-info {
  padding: 14px;
}

.product-title {
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 4px;
  line-height: 1.3;
}

.product-meta {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-bottom: 6px;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-bottom: 6px;
}

.product-rating svg {
  width: 12px;
  height: 12px;
  fill: #e5b94e;
}

.product-rating span {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-left: 4px;
}

.product-price {
  font-weight: 600;
  font-size: 14px;
}

@media (min-width: 768px) {
  .product-scroll {
    padding: 0 40px 16px;
    margin: 0 -40px;
  }
  .product-card { flex: 0 0 240px; }
}
```

### Liquid changes
- Replace grid/slider rendering with native horizontal scroll container
- Remove slider arrow buttons for this section
- Add `scroll-snap-type: x mandatory` and `scroll-snap-align: start`
- Product card snippet should include rating stars (SVG inline)
- Badge rendering: use `product-badge` class with optional `.sale` modifier
- "View All" button: centered below the scroll, `btn-secondary`, inline width

---

## 7. Brand Story Section (Image with Text)

### Files to modify
- `sections/image-with-text.liquid`
- `assets/section-image-with-text.css` (if exists)

### Mockup structure
```
Mobile: stacked (image on top, text below)
Desktop: 2-column grid (image left, text right)

Image: 16:10 aspect ratio mobile, 1:1 desktop, rounded corners
Content:
  H2: "Sourced with Care, Crafted for Quality"
  Paragraph text
  2x2 grid of brand values:
    Each: [SVG icon] [Title + description]
    Values: 100% Organic, Ethically Sourced, Lab Tested, Bulk Pricing
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Image aspect ratio  | adapt/dynamic              | `16:10` mobile, `1:1` desktop|
| Image radius        | `--media-radius`           | `12px` (--radius-md)        |
| Content heading     | dynamic size               | `22px`, weight 400          |
| Body text           | theme default              | `14px`, `#666`, line-height 1.7 |
| Values grid         | not present                | 2x2 grid with icon + text  |
| Icon style          | raster images              | SVG stroke icons, `#9b76a7` |
| Value title         | N/A                        | `12px`, heading font, weight 600 |
| Value description   | N/A                        | `11px`, muted color         |
| Desktop layout      | configurable columns       | `1fr 1fr` with `48px` gap  |

### CSS to implement

```css
.brand-story-image {
  width: 100%;
  aspect-ratio: 16/10;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
}

.brand-story-content h2 {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 400;
  margin-bottom: 16px;
  line-height: 1.3;
}

.brand-story-content p {
  color: var(--color-text-muted);
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.7;
}

.brand-values {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.brand-value {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.brand-value svg {
  width: 20px;
  height: 20px;
  stroke: var(--color-accent-dark);
  stroke-width: 1.5;
  flex-shrink: 0;
  margin-top: 2px;
}

.brand-value h4 {
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 2px;
}

.brand-value p {
  font-size: 11px;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.4;
}

@media (min-width: 768px) {
  .brand-story {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
  }
  .brand-story-image {
    margin-bottom: 0;
    aspect-ratio: 1;
  }
}
```

### Liquid changes
- Add a new block type `brand_values` or `value_icons` to the image-with-text schema
  that renders a 2x2 grid of icon + title + description items
- Each value block needs: SVG icon selector, title (text), description (text)
- Or: create a dedicated `brand-story.liquid` section with its own schema

---

## 8. Testimonials Section

### Files to modify
- `sections/testimonials.liquid`
- `assets/section-testimonials.css` (if exists)

### Mockup structure
```
Section header:
  Label: "What People Say"
  Title: "Customer Reviews"

Horizontal scroll carousel:
  Each card (280px wide):
    [5 gold stars]
    [Italic review text]
    [Author name (bold)]
    [Role/location (muted)]
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Layout              | grid/slider                | horizontal scroll            |
| Card width          | column-based               | fixed `280px`               |
| Card style          | varies by style option     | white bg, `12px` radius, `1px` border |
| Card padding        | theme default              | `20px`                      |
| Star size           | theme rating component     | `14px`, fill `#e5b94e`      |
| Review text         | theme body                 | `13px`, italic, `#1d1d1d`   |
| Author name         | theme default              | heading font, `12px`, weight 600 |
| Role text           | may not exist              | `11px`, `#666`              |
| Background          | configurable               | `#f7f7f7` (section-alt)     |
| Scrollbar           | visible                    | hidden                       |

### CSS to implement

```css
.testimonial-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 0 20px 16px;
  margin: 0 -20px;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
}

.testimonial-scroll::-webkit-scrollbar {
  display: none;
}

.testimonial-card {
  flex: 0 0 280px;
  scroll-snap-align: start;
  background: var(--color-background);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.testimonial-stars {
  display: flex;
  gap: 2px;
  margin-bottom: 12px;
}

.testimonial-stars svg {
  width: 14px;
  height: 14px;
  fill: #e5b94e;
}

.testimonial-text {
  font-size: 13px;
  line-height: 1.6;
  color: var(--color-foreground);
  margin-bottom: 16px;
  font-style: italic;
}

.testimonial-author {
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
}

.testimonial-role {
  font-size: 11px;
  color: var(--color-text-muted);
}

@media (min-width: 768px) {
  .testimonial-scroll {
    padding: 0 40px 16px;
    margin: 0 -40px;
  }
}
```

### Liquid changes
- Add a `role` or `subtitle` field to testimonial block schema
- Ensure `style-2` renders as horizontal scroll (not grid)
- Remove product reference display from testimonial cards (mockup doesn't show them)
- Stars rendered as inline SVG with gold fill

---

## 9. Email Signup / Newsletter Section

### Files to modify
- `sections/newsletter.liquid`
- `assets/component-newsletter.css`

### Mockup structure
```
Full-width dark section:
  H2: "Get 10% Off Your First Order"
  Subtitle: "Plus exclusive recipes, wellness tips..."
  Email input + Subscribe button (stacked on mobile, inline on desktop)
  Privacy note: "No spam, ever. Unsubscribe anytime."
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Background          | color scheme (configurable)| `#1d1d1d` (dark, forced)    |
| Text color          | color scheme               | `#ffffff`                   |
| Subtitle color      | theme default              | `rgba(255,255,255,0.7)`    |
| Input background    | theme default              | `rgba(255,255,255,0.1)`    |
| Input border        | theme default              | `1px solid rgba(255,255,255,0.2)` |
| Input text color    | theme default              | `#fff`                     |
| Placeholder color   | theme default              | `rgba(255,255,255,0.5)`    |
| Button background   | theme button               | `#d4c4d9` (--color-accent) |
| Button text color   | theme button               | `#1d1d1d` (--color-foreground) |
| Privacy text color  | not present                | `rgba(255,255,255,0.5)`    |
| Padding             | configurable               | `40px 20px`                |
| Form layout mobile  | responsive                 | stacked column, `12px` gap |
| Form layout desktop | responsive                 | inline row, max-width `450px` |

### CSS to implement

```css
.email-signup {
  background: var(--color-foreground);
  color: var(--color-background);
  padding: 40px 20px;
  text-align: center;
}

.email-signup h2 {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 400;
  margin-bottom: 8px;
}

.email-signup p {
  color: rgba(255,255,255,0.7);
  font-size: 14px;
  margin-bottom: 20px;
}

.email-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.email-form input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.1);
  color: #fff;
  font-family: var(--font-body);
  font-size: 15px;
  border-radius: 8px;
}

.email-form input::placeholder {
  color: rgba(255,255,255,0.5);
}

.email-form button {
  width: 100%;
  padding: 14px 24px;
  background: var(--color-accent);
  color: var(--color-foreground);
  border: none;
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: 8px;
  min-height: 44px;
  cursor: pointer;
}

.email-privacy {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  margin-top: 12px;
}

@media (min-width: 768px) {
  .email-form {
    flex-direction: row;
    max-width: 450px;
    margin: 0 auto;
  }
  .email-form input { flex: 1; }
  .email-form button { width: auto; }
}
```

### Liquid changes
- Force dark color scheme (`option-3` or equivalent) for this section
- Add a `privacy_text` setting to the schema for the "No spam" disclaimer
- Submit button should use accent color instead of primary button style

---

## 10. Footer Section

### Files to modify
- `sections/footer.liquid`
- `assets/section-footer.css`

### Mockup structure
```
Background: #f7f7f7

Brand block (centered):
  Logo text: "DIVINE INGREDIENTS"
  Tagline paragraph
  Trust badges: [USDA Organic] [Secure Checkout] (pill badges with icons)

Links grid: 2 columns mobile, 4 columns desktop
  Column: heading + link list

Bottom bar:
  Social icons (Instagram, X/Twitter, YouTube) — centered, 44px touch targets
  Copyright text

Border-top: 1px solid #e8e8e8 above bottom bar
```

### Key design differences
| Aspect              | Current Theme              | Mockup v3                    |
|---------------------|----------------------------|------------------------------|
| Background          | configurable               | `#f7f7f7` (--color-background-alt) |
| Padding             | section settings           | `32px 20px`                 |
| Brand logo          | image/text from settings   | text-only, heading font `18px` |
| Tagline             | brand_description          | `13px`, muted, max-width `280px` |
| Trust badges        | not present in footer      | pill badges with SVG icons  |
| Badge style         | N/A                        | `#fff` bg, `8px` radius, `11px` text |
| Link columns        | configurable (menu blocks) | 2-col mobile, 4-col desktop |
| Column heading      | theme default              | `11px`, `0.1em` spacing, uppercase |
| Link text           | theme default              | `13px`, `#666`, no underline |
| Social icon size    | theme default              | `22px` SVG, `44px` touch target |
| Social icon color   | theme default              | `#666` (--color-text-muted) |
| Copyright           | theme default              | `11px`, muted              |

### CSS to implement

```css
.footer {
  background: var(--color-background-alt);
  padding: 32px 20px;
}

.footer-brand {
  text-align: center;
  margin-bottom: 32px;
}

.footer-brand h3 {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}

.footer-brand p {
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.6;
  max-width: 280px;
  margin: 0 auto 16px;
}

.footer-badges {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.footer-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--color-background);
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
}

.footer-badge svg {
  width: 14px;
  height: 14px;
  stroke: var(--color-accent-dark);
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.footer-column h4 {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.footer-column a {
  font-size: 13px;
  color: var(--color-text-muted);
  text-decoration: none;
}

.footer-column li {
  margin-bottom: 8px;
}

.footer-bottom {
  border-top: 1px solid var(--color-border);
  padding-top: 24px;
  text-align: center;
}

.footer-social {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 16px;
}

.footer-social a {
  color: var(--color-text-muted);
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-social svg {
  width: 22px;
  height: 22px;
}

.footer-copyright {
  font-size: 11px;
  color: var(--color-text-muted);
}

@media (min-width: 768px) {
  .footer-links {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Liquid changes
- Add trust badge blocks to the footer schema (icon + label)
- Ensure brand block renders as centered text, not image
- Social icons should use `fill: currentColor` SVGs at 22px

---

## 11. Section Padding & Spacing Pattern

### Universal section wrapper

Every content section (categories, products, brand story, testimonials) uses
this consistent pattern:

```css
.section {
  padding: 32px 20px;        /* mobile */
}

.section-alt {
  background: #f7f7f7;       /* alternating backgrounds */
}

@media (min-width: 768px) {
  .section {
    padding: 48px 40px;      /* desktop */
  }
}
```

### Alternating background pattern from mockup

| Section              | Background         | Class          |
|----------------------|--------------------|--------------------|
| Announcement Bar     | `#1d1d1d` (dark)   | `.announcement-bar`|
| Header               | `#ffffff`          | `.header`          |
| Hero                 | `#ffffff`          | `.hero`            |
| Trust Bar            | `#ffffff`          | `.trust-bar`       |
| Categories           | `#ffffff`          | `.section`         |
| Best Sellers         | `#f7f7f7`          | `.section.section-alt` |
| Brand Story          | `#ffffff`          | `.section`         |
| Testimonials         | `#f7f7f7`          | `.section.section-alt` |
| Email Signup         | `#1d1d1d` (dark)   | `.email-signup`    |
| Footer               | `#f7f7f7`          | `.footer`          |

This alternation creates visual rhythm without using borders or shadows
between sections.

---

## 12. Desktop Breakpoint Strategy

The mockup uses a **single breakpoint at `768px`** (tablet/desktop).
The current theme uses `990px` as its primary breakpoint.

### Recommendation
Change the primary responsive breakpoint from `990px` to `768px` for all
rewritten sections to match the mockup. This better serves the 72% mobile
traffic since users on tablets (768px+) get the enhanced layout sooner.

Sections using the new breakpoint:
- Hero CTA: stack → row at 768px
- Buttons: full-width → auto-width at 768px
- Category grid: 2-col → 4-col at 768px
- Brand story: stack → 2-col grid at 768px
- Email form: stack → inline at 768px
- Footer links: 2-col → 4-col at 768px

---

## 13. Responsive Scroll Pattern (Shared)

Three sections (Trust Bar, Products, Testimonials) share the same horizontal
scroll UX. This should be extracted into a shared utility:

```css
/* Shared horizontal scroll container */
.scroll-container {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.scroll-container > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}
```

This replaces the current slider/arrow-button pattern with native browser
scroll, which is more performant and touch-friendly on mobile.

---

## Summary: Files to Create or Modify

| File | Action | Section(s) Affected |
|------|--------|---------------------|
| `layout/theme.liquid` | **Modify** | Add new CSS custom properties (0.1) |
| `assets/base.css` | **Modify** | Typography, buttons, section spacing (0.2, 0.3, 11) |
| `assets/divine-mockup-v3.css` | **Create** | New stylesheet with all mockup-specific overrides |
| `sections/header.liquid` | **Modify** | Header + announcement bar (1, 2) |
| `sections/image-banner.liquid` | **Modify** | Hero section (3) |
| `sections/multicolumn.liquid` | **Modify** | Trust bar variant (4) |
| `sections/collection-list.liquid` | **Modify** | Category grid (5) |
| `sections/featured-collection.liquid` | **Modify** | Product carousel (6) |
| `snippets/card-product.liquid` | **Modify** | Product card styling (6) |
| `sections/image-with-text.liquid` | **Modify** | Brand story (7) |
| `sections/testimonials.liquid` | **Modify** | Testimonial carousel (8) |
| `sections/newsletter.liquid` | **Modify** | Email signup (9) |
| `sections/footer.liquid` | **Modify** | Footer (10) |
| `templates/index.json` | **Modify** | Section order and settings (all) |
| `config/settings_data.json` | **Modify** | Global theme settings (0) |
