# Animation System Reference

Complete animation library for entrance effects, scroll-triggered animations, and interactive micro-animations.

## Animation Variables

```css
:root {
    /* Timing */
    --anim-fast: 150ms;
    --anim-normal: 300ms;
    --anim-slow: 500ms;
    --anim-slower: 800ms;

    /* Easing */
    --ease-out: cubic-bezier(0.33, 1, 0.68, 1);
    --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
    --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
    --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

    /* Distances */
    --slide-distance: 22px;
    --slide-distance-lg: 80px;
}
```

## Entrance Animations

### Fade In

Simple opacity fade-in.

```html
<div class="fade-in">Content</div>
```

```css
.fade-in {
    animation: fadeIn var(--anim-normal) var(--ease-out) forwards;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### Fade In Up

Fades in while sliding up from below.

```html
<div class="fade-in-up">Content</div>
```

```css
.fade-in-up {
    animation: fadeInUp var(--anim-slow) var(--ease-out) forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(var(--slide-distance));
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Fade In Scale

Fades in while scaling from smaller size.

```html
<div class="fade-in-scale">Content</div>
```

```css
.fade-in-scale {
    animation: fadeInScale var(--anim-slow) var(--ease-bounce) forwards;
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}
```

### Pop In

Bouncy pop-in effect with slight overshoot.

```html
<div class="pop-in">Content</div>
```

```css
.pop-in {
    animation: popIn var(--anim-normal) var(--ease-spring) forwards;
}

@keyframes popIn {
    0% {
        opacity: 0;
        transform: scale(0.5);
    }
    70% {
        transform: scale(1.1);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}
```

### Slide In

Horizontal slide-in from left or right.

```html
<div class="slide-in-left">Content</div>
<div class="slide-in-right">Content</div>
```

```css
.slide-in-left {
    animation: slideInLeft var(--anim-slow) var(--ease-out) forwards;
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-60px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
```

## Text Animations

### Letter Reveal

Reveals text letter-by-letter with a stagger effect.

```html
<div class="text-reveal">
  <span class="delay-1">H</span>
  <span class="delay-2">e</span>
  <span class="delay-3">l</span>
  <span class="delay-4">l</span>
  <span class="delay-5">o</span>
</div>
```

```css
.text-reveal span {
    display: inline-block;
    opacity: 0;
    transform: translateY(10px);
    animation: letterReveal var(--anim-normal) var(--ease-out) forwards;
}

.delay-1 { animation-delay: 0.02s; }
.delay-2 { animation-delay: 0.04s; }
.delay-3 { animation-delay: 0.06s; }
/* ... up to delay-15 */
```

### Word Reveal

Reveals text word-by-word for sentences.

```html
<div class="word-reveal">
  <span>Hello</span>
  <span>World</span>
</div>
```

```css
.word-reveal > span {
    display: inline-block;
    opacity: 0;
    transform: translateY(22px);
}

.word-reveal.animate > span {
    animation: wordReveal var(--anim-slow) var(--ease-out) forwards;
}

@keyframes wordReveal {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Scroll-Triggered Animations

### Basic Scroll Animation

Element animates when scrolled into view.

```html
<div data-animate>Content that animates on scroll</div>
```

```css
[data-animate] {
    opacity: 0;
    transform: translateY(var(--slide-distance));
    transition:
        opacity var(--anim-slow) var(--ease-out),
        transform var(--anim-slow) var(--ease-out);
}

[data-animate].in-view {
    opacity: 1;
    transform: translateY(0);
}
```

### Staggered Children

Parent container animates children one after another.

```html
<div data-stagger>
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

```css
[data-stagger] > * {
    opacity: 0;
    transform: translateY(var(--slide-distance));
    transition:
        opacity var(--anim-slow) var(--ease-out),
        transform var(--anim-slow) var(--ease-out);
}

[data-stagger].in-view > *:nth-child(1) {
    transition-delay: 0s;
    opacity: 1;
    transform: translateY(0);
}

[data-stagger].in-view > *:nth-child(2) {
    transition-delay: 0.1s;
    opacity: 1;
    transform: translateY(0);
}

/* ... up to nth-child(6) */
```

### JavaScript for Scroll Animations

Required IntersectionObserver script:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('[data-animate], [data-stagger]').forEach(el => {
        observer.observe(el);
    });
});
```

## Hover Animations

### Lift on Hover

Element lifts up slightly on hover.

```html
<div class="hover-lift">Content</div>
```

```css
.hover-lift {
    transition: transform var(--anim-fast) var(--ease-out);
}

.hover-lift:hover {
    transform: translateY(-4px);
}
```

### Scale on Hover

Element scales up slightly on hover.

```html
<div class="hover-scale">Content</div>
```

```css
.hover-scale {
    transition: transform var(--anim-fast) var(--ease-out);
}

.hover-scale:hover {
    transform: scale(1.05);
}
```

### Wiggle on Hover

Playful wiggle/rotation effect.

```html
<div class="hover-wiggle">Content</div>
```

```css
.hover-wiggle {
    transition: transform var(--anim-fast) var(--ease-out);
}

.hover-wiggle:hover {
    animation: wiggle 0.4s ease;
}

@keyframes wiggle {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-5deg); }
    75% { transform: rotate(5deg); }
}
```

### Bounce on Hover

Bouncing effect on hover.

```html
<div class="hover-bounce">Content</div>
```

```css
.hover-bounce:hover {
    animation: bounce 0.5s var(--ease-spring);
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
```

## Continuous Animations

### Float

Gentle up-and-down floating motion.

```html
<div class="float">Content</div>
```

```css
.float {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
```

### Pulse

Gentle scale pulse.

```html
<div class="pulse">Content</div>
```

```css
.pulse {
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

### Swing

Side-to-side swing motion (useful for decorative elements).

```html
<div class="swing">Content</div>
```

```css
.swing {
    transform-origin: top center;
    animation: swing 2s ease-in-out infinite;
}

@keyframes swing {
    0%, 100% { transform: rotate(-3deg); }
    50% { transform: rotate(3deg); }
}
```

## Reduced Motion Support

Always respect user preferences for reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }

    [data-animate],
    [data-stagger] > * {
        opacity: 1;
        transform: none;
    }
}
```

## Usage Guidelines

1. **Entrance animations**: Use for page load or section reveals
2. **Scroll animations**: Use `data-animate` and `data-stagger` for content that appears on scroll
3. **Hover effects**: Keep subtle and fast (150ms) for responsive feel
4. **Continuous animations**: Use sparingly for decorative elements only
5. **Performance**: Prefer `transform` and `opacity` for smooth animations
6. **Accessibility**: Always include `prefers-reduced-motion` support

