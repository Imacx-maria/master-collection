# Additional Component Patterns

Components beyond the core bento grid that extend the design system.

## Feature Cards

Large rounded cards with overlapping images. Used for showcasing features or content sections.

### Specifications

- **Border radius**: 60px (very rounded)
- **Border**: 1px solid `--green-dark`
- **Padding**: 40px
- **Background**: Typically rose (`#fccddc`) or other accent colors
- **Shadow**: -4px 4px 0px 0px (brutalist offset)
- **Images**: Overlapping, rotated, with varying z-index
- **Typography**: Fredoka 600, uppercase titles

### Structure

```html
<div class="feature-card">
  <div class="feature-card-images">
    <div class="feature-card-image"><img src="..." alt=""></div>
    <div class="feature-card-image"><img src="..." alt=""></div>
    <div class="feature-card-image"><img src="..." alt=""></div>
  </div>
  <div class="feature-card-content">
    <h3 class="feature-card-title">FEATURE NAME</h3>
    <p class="feature-card-subtitle">Description text</p>
  </div>
</div>
```

### CSS Pattern

```css
.feature-card {
    background-color: #fccddc;
    border: 1px solid #03594d;
    border-radius: 60px;
    box-shadow: -4px 4px 0px 0px #03594d;
    padding: 40px;
    overflow: hidden;
}

.feature-card-title {
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    font-size: 32px;
    line-height: 90%;
    text-transform: uppercase;
    color: #03594d;
    text-align: center;
}
```

## Phone Mockup Cards

Device mockups with rotation effects and fan layouts for showcasing screenshots.

### Specifications

- **Border radius**: 20px
- **Border**: 1px solid `--green-dark`
- **Shadow**: Layered shadow effect for premium look
- **Rotation**: Can use `rotate-left` (-5deg) or `rotate-right` (+5deg) classes
- **Fan layout**: Multiple phones in a fan arrangement with varying transforms

### Structure

```html
<div class="phone-fan">
  <div class="phone-card rotate-left">
    <img src="screen1.png" alt="">
  </div>
  <div class="phone-card">
    <img src="screen2.png" alt="">
  </div>
  <div class="phone-card rotate-right">
    <img src="screen3.png" alt="">
  </div>
</div>
```

### CSS Pattern

```css
.phone-card {
    border: 1px solid #03594d;
    border-radius: 20px;
    overflow: hidden;
    box-shadow:
        -0.3px 0.36px 0px 0px rgba(4, 88, 78, 0.06),
        -1.14px 1.37px 0px 0px rgba(4, 88, 78, 0.23),
        -5px 6px 0px 0px rgb(4, 88, 78);
}

.phone-card.rotate-left {
    transform: rotate(-5deg);
}

.phone-card.rotate-right {
    transform: rotate(5deg);
}
```

## Content Cards

Image + text structured cards for displaying content with imagery.

### Specifications

- **Border radius**: 20px
- **Border**: 1px solid `--green-dark`
- **Shadow**: -4px 4px 0px 0px
- **Image aspect ratio**: 16:9
- **Background**: Off-white default, color variants available

### Structure

```html
<div class="content-card">
  <div class="content-card-image">
    <img src="..." alt="">
  </div>
  <div class="content-card-body">
    <span class="content-card-tag">Category</span>
    <h4 class="content-card-title">Card Title</h4>
    <p class="content-card-text">Description text.</p>
  </div>
</div>
```

### CSS Pattern

```css
.content-card {
    background-color: #f9f8f4;
    border: 1px solid #03594d;
    border-radius: 20px;
    box-shadow: -4px 4px 0px 0px #03594d;
    overflow: hidden;
}

.content-card-tag {
    font-family: 'Fredoka', sans-serif;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #03594d;
    background-color: #82eda6;
    padding: 4px 12px;
    border-radius: 100px;
}
```

## Navigation Patterns

### Floating Pill Navigation

Centered navigation bar with pill-shaped buttons and logo in the middle.

### Specifications

- **Position**: Fixed, top: 20px, centered
- **Background**: Off-white with backdrop blur
- **Border**: 1px solid `--green-dark`
- **Border radius**: 100px (pill shape)
- **Shadow**: -3px 3px 0px 0px
- **Layout**: Left nav items | Logo (center) | Right nav items

### Structure

```html
<nav class="navbar">
  <div class="navbar-container">
    <div class="navbar-left">
      <a href="/about" class="nav-link nav-link-rose">ABOUT</a>
    </div>
    <div class="navbar-center">
      <a href="/" class="nav-logo">
        <img src="logo.svg" alt="">
      </a>
    </div>
    <div class="navbar-right">
      <a href="/contact" class="nav-link">CONTACT</a>
    </div>
  </div>
</nav>
```

### CSS Pattern

```css
.navbar {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px 12px;
    background-color: rgba(249, 248, 244, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid #03594d;
    border-radius: 100px;
    box-shadow: -3px 3px 0px 0px #03594d;
}

.nav-link {
    padding: 12px 24px;
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: 1px solid #03594d;
    border-radius: 100px;
    box-shadow: -3px 3px 0px 0px #03594d;
}

.nav-logo {
    width: 48px;
    height: 48px;
    padding: 8px;
    background-color: #82eda6;
    border: 1px solid #03594d;
    border-radius: 100px;
    box-shadow: -3px 3px 0px 0px #03594d;
}
```

### Mobile Bottom Navigation

Bottom-aligned navigation for mobile with hamburger menu.

### Specifications

- **Position**: Fixed, bottom: 20px, centered
- **Hamburger menu**: 3-line icon that animates to X when open
- **Mobile menu overlay**: Full-screen overlay with navigation links

### Structure

```html
<nav class="navbar-mobile">
  <div class="navbar-container">
    <a href="/" class="nav-logo">
      <img src="logo.svg" alt="">
    </a>
    <button class="nav-menu-btn" id="menuBtn">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <a href="/about" class="nav-link">ABOUT</a>
  <a href="/contact" class="nav-link">CONTACT</a>
</div>
```

## Carousel Controls

Arrow buttons for navigating carousels/slideshows.

### Specifications

- **Size**: 48px × 48px (or 52px for larger variants)
- **Border radius**: 100px (circular)
- **Colors**: Yellow for previous, Orange for next (or other accent colors)
- **Shadow**: -4px 4px 0px 0px

### Structure

```html
<div class="carousel-controls">
  <button class="carousel-btn carousel-btn-prev">
    <svg><!-- left arrow --></svg>
  </button>
  <button class="carousel-btn carousel-btn-next">
    <svg><!-- right arrow --></svg>
  </button>
</div>
```

### CSS Pattern

```css
.carousel-btn {
    width: 48px;
    height: 48px;
    border-radius: 100px;
    border: 1px solid #03594d;
    box-shadow: -4px 4px 0px 0px #03594d;
    display: flex;
    align-items: center;
    justify-content: center;
}

.carousel-btn-prev {
    background-color: #ffff94; /* Yellow */
}

.carousel-btn-next {
    background-color: #fdc068; /* Orange */
}
```

## Sticker Cards

Decorative elements with images and labels, often used for categories or features.

### Specifications

- **Layout**: Vertical stack (image above label)
- **Border radius**: 20px or rounded based on image shape
- **Hover effect**: Scale and rotate slightly
- **Image size**: Typically 80px × 80px

### Structure

```html
<div class="sticker-card">
  <img src="icon.svg" alt="" class="sticker-card-image">
  <span class="sticker-card-label">Label Text</span>
</div>
```

### CSS Pattern

```css
.sticker-card {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.sticker-card:hover {
    transform: scale(1.1) rotate(5deg);
}

.sticker-card-image {
    width: 80px;
    height: 80px;
    object-fit: contain;
}

.sticker-card-label {
    font-family: 'Fredoka', sans-serif;
    font-weight: 500;
    font-size: 14px;
    text-transform: uppercase;
    color: #03594d;
}
```

