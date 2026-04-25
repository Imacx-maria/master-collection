
# Basalt E-Commerce

Premium minimal e-commerce system for luxury brands. Clean typography, refined product presentation, and sophisticated interactions. Designed for beauty, skincare, fashion, and lifestyle products where elegance matters.

## Quick Start

**Pages available:**
- `assets/template-home.html` — Homepage with hero, products, categories
- `assets/template-product.html` — Product detail page with accordions
- `assets/template-about.html` — Brand story page

1. Copy relevant template as starting point
2. Replace brand name, content, and images (use Unsplash)
3. Customize colors if needed (default: grayscale)

## Display Typography & Hero Patterns

Basalt lives or dies by its serif drama. The display tokens are non-negotiable in their use:

**`display-xl` (120px, EB Garamond Regular)** — One use only: the brand-defining hero on the home page or about page. Pair with `display-italic` on the first word for the signature editorial accent. Never use for product names or section headers.

**`display-lg` (88px, EB Garamond Regular)** — Section heroes (collection openers, about-us anchors, editorial moments inside product pages). Suitable for page-level headlines that need presence but aren't the brand statement.

**`headline-lg` (56px)** — Product names on detail pages, category headers, sub-section titles. Default headline size.

**Hero patterns by page type:**

- **Home hero** — Split layout (50/50 or 60/40), `display-xl` headline left with italic first word + product photography right. Pair with `5xl` (128px) vertical padding to give the hero airroom worthy of luxury.
- **Collection opener** — Full-bleed image top, then `display-lg` centered or asymmetric below with `4xl` (96px) bottom margin before the product grid.
- **About page hero** — `display-xl` with `display-italic` accent, pair with portrait or product still-life. Use `5xl` top/bottom padding.
- **Product detail** — No display type. `headline-lg` for product name, body Garamond Regular for description, accordions for spec depth.

**Spacing for luxury breathing:**

- Hero sections: `4xl` (96px) or `5xl` (128px) vertical padding
- Section dividers: `4xl` between major sections, `2xl` (48px) inside sections
- Product grid gaps: `xl` (32px) — generous, never tight
- Inside cards: `pad-card` (32px) — never less

## Core Aesthetic

- **Grayscale palette**: #000 / #1e1e1f / #bfbfbf / #e4e4e4 / #f5f5f5 / #fff
- **Typography**: EB Garamond (headlines) + Inter (body/nav)
- **Italic accent**: First word in headlines uses Garamond Italic
- **Floating products**: Products on neutral gray backgrounds with shadows
- **Welcome popup**: Email capture modal on first visit
- **Split product pages**: Image left, details right with accordions

## Design Tokens

```css
:root {
  --color-white: #fff;
  --color-off-white: #f5f5f5;
  --color-light-gray: #e4e4e4;
  --color-mid-gray: #bfbfbf;
  --color-charcoal: #1e1e1f;
  --color-black: #000;
  
  --font-display: "EB Garamond", serif;
  --font-body: "Inter", sans-serif;
  
  --nav-height: 56px;
  --container-max: 1400px;
  --section-gap: 120px;
}
```

## Typography Hierarchy

```css
/* Hero headline - mixed italic/regular */
.hero-headline {
  font-family: var(--font-display);
  font-size: clamp(48px, 8vw, 96px);
  font-weight: 400; /* Always regular weight */
  line-height: 1.1;
}
.hero-headline em {
  font-style: italic; /* First word italic */
}

/* Section headlines */
.section-headline {
  font-family: var(--font-display);
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 400;
}

/* Product name on cards */
.product-name {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Product title on detail page */
.product-title {
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 56px);
  font-weight: 400;
}

/* Body text */
body {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6;
}

/* Nav links */
.nav-link {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 400;
}

/* Section labels (uppercase) */
.section-label {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.15em;
}
```

## Signature Patterns

| Pattern | Description | Usage |
|---------|-------------|-------|
| Italic first word | `<em>Nature's</em> Way to Healthy Skin` | Hero headlines |
| Welcome popup | Dark overlay modal with email input | Homepage on load |
| Floating products | Product on #e4e4e4 bg with drop shadow | Product cards |
| Split product page | 50/50 image left, content right | Product detail |
| Accordion sections | Expandable KEY INGREDIENTS, etc. | Product detail |
| Arrow CTA | `SHOP PRODUCTS ↗` uppercase | All buttons |
| Price format | `$79.00` — name left, price right | Product cards |

## Page Templates

### Homepage (`template-home.html`)
1. Navigation (sticky, white bg)
2. Video/Image Hero with headline
3. Best Sellers (3-col product grid)
4. Category Cards (2-col full-height)
5. About Preview
6. Recent Articles
7. CTA Section
8. Footer

### Product Detail (`template-product.html`)
1. Navigation
2. Split layout:
   - Left: Full-height product image
   - Right: Title, size, description, accordions, buy button
3. Related Products
4. Footer

### About (`template-about.html`)
1. Navigation
2. Hero with brand headline
3. Story sections (alternating image/text)
4. Values/Philosophy
5. Team (optional)
6. CTA
7. Footer

## Welcome Popup Structure

```html
<div class="popup-overlay" id="welcomePopup">
  <div class="popup-modal">
    <button class="popup-close" aria-label="Close">×</button>
    <div class="popup-image">
      <img src="..." alt="">
    </div>
    <div class="popup-content">
      <h3 class="popup-title">WELCOME OFFER</h3>
      <p class="popup-text">Enjoy 15% off from your first order.</p>
      <form class="popup-form">
        <input type="email" placeholder="name@email.com">
        <button type="submit">Signup</button>
      </form>
    </div>
  </div>
</div>
```

## Product Card Structure

```html
<article class="product-card">
  <a href="/product" class="product-image-wrap">
    <img src="product.jpg" alt="Product Name">
  </a>
  <div class="product-info">
    <span class="product-name">CLARO</span>
    <span class="product-price">$79.00</span>
  </div>
</article>
```

## Product Detail Accordion

```html
<div class="accordion">
  <button class="accordion-trigger">
    <span>KEY INGREDIENTS</span>
    <span class="accordion-icon">+</span>
  </button>
  <div class="accordion-content">
    <p>Basalt minerals, Hyaluronic acid, Vitamin E...</p>
  </div>
</div>
```

## Navigation Structure

```html
<nav class="nav">
  <div class="nav-container">
    <div class="nav-left">
      <a href="/shop" class="nav-link">Shop</a>
      <a href="/about" class="nav-link">About</a>
      <a href="/articles" class="nav-link">Articles</a>
      <a href="/contact" class="nav-link">Contact</a>
    </div>
    <a href="/" class="nav-logo">©BASALT</a>
    <div class="nav-right">
      <a href="/account" class="nav-link">Account</a>
      <button class="nav-icon" aria-label="Search">...</button>
      <button class="nav-icon cart-icon" aria-label="Cart">
        <span class="cart-count">0</span>
      </button>
    </div>
  </div>
</nav>
```

## Micro-Interactions

- **Popup**: Appears after 2s delay, closes on X or overlay click
- **Product cards**: Subtle scale (1.02) on hover
- **Accordions**: Smooth expand/collapse with icon rotation
- **Nav**: White background, no transparency changes
- **Buttons**: Background darkens on hover
- **Scroll animations**: Fade-in from below (translateY: 20px → 0)

## Responsive Breakpoints

```css
/* Desktop: ≥1200px */
/* Tablet: 810px - 1199px */
/* Mobile: ≤809px */
```

Key changes:
- Product grid: 3-col → 2-col → 1-col
- Product detail: side-by-side → stacked
- Category cards: side-by-side → stacked

## Critical Rules

1. **EB Garamond Regular only** — never bold, use italic for accent
2. **Inter for all body text** — clean, modern contrast
3. **Floating product images** — gray bg (#e4e4e4), product with shadow
4. **Welcome popup required** — email capture on homepage
5. **Accordions on product page** — KEY INGREDIENTS, SCENT NOTES, APPLICATION
6. **Uppercase labels** — section labels, product names on cards, nav
7. **Arrow icon on CTAs** — diagonal arrow (↗) on all action buttons

## Output Checklist

- [ ] EB Garamond Regular for headlines (italic for first word)
- [ ] Inter for body, nav, labels
- [ ] Welcome popup modal on homepage
- [ ] Product cards with floating product style
- [ ] Product detail page with split layout
- [ ] Accordion sections on product page
- [ ] About page with brand story
- [ ] Uppercase section labels
- [ ] Diagonal arrow on CTAs
- [ ] Responsive at all breakpoints

## Reference Files

- `references/component-patterns.md` — Complete HTML/CSS for all components
- `assets/template-home.html` — Homepage template
- `assets/template-product.html` — Product detail template
- `assets/template-about.html` — About page template

---

## Component Patterns

For complete component code snippets, read the original skill's component-patterns reference.
Source: `/mnt/skills/user/basalt-ecommerce/references/component-patterns.md`

## Templates

HTML starter templates: template-product.html template-home.html template-about.html 
Source: `/mnt/skills/user/basalt-ecommerce/assets/`
