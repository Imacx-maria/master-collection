/** @type {import('tailwindcss').Config} */
/* AUTO-GENERATED from motion-directed-spatial-portfolio.design.md on 2026-04-26T14:15:32+00:00. Do not edit. */

export default {
  content: ['./**/*.{html,js,jsx,ts,tsx}'],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        'page-black': '#030303',
        'stage-black': '#070707',
        'charcoal': '#111111',
        'graphite': '#1a1a1a',
        'text-primary': '#f4f4f0',
        'text-secondary': '#c9c7c1',
        'text-muted': '#8a8882',
        'text-ghost': 'rgba(244,244,240,0.45)',
        'hairline': 'rgba(255,255,255,0.12)',
        'hairline-faint': 'rgba(255,255,255,0.06)',
        'accent-acid': '#62ff6a',
        'accent-warm': '#d7c0a2',
        'overlay': 'rgba(0,0,0,0.48)',
      },
      fontFamily: {
        'display': ['Inter Tight, Satoshi, Neue Montreal, Helvetica Neue, Arial, sans-serif', 'serif'],
        'body': ['Cormorant Garamond, Libre Baskerville, Georgia, serif', 'serif'],
        'body-2': ['Inter Tight, Helvetica Neue, Arial, sans-serif', 'serif'],
        'body-3': ['JetBrains Mono, IBM Plex Mono, ui-monospace, monospace', 'monospace'],
      },
      fontSize: {
        'display-xl': ['clamp(72px, 12vw, 168px)', { lineHeight: '0.88', letterSpacing: '-0.055em', fontWeight: '300' }],
        'display-lg': ['clamp(56px, 9vw, 120px)', { lineHeight: '0.9', letterSpacing: '-0.045em', fontWeight: '300' }],
        'headline-md': ['clamp(32px, 5vw, 64px)', { lineHeight: '0.98', letterSpacing: '-0.035em', fontWeight: '400' }],
        'editorial': ['clamp(18px, 1.7vw, 24px)', { lineHeight: '1.15', letterSpacing: '-0.02em', fontWeight: '400' }],
        'body-sm': ['13px', { lineHeight: '1.45', letterSpacing: '-0.01em', fontWeight: '400' }],
        'label': ['12px', { lineHeight: '1', letterSpacing: '-0.02em', fontWeight: '500' }],
        'mono': ['11px', { lineHeight: '1.4', letterSpacing: '-0.01em', fontWeight: '400' }],
      },
      borderRadius: {
        'sharp': '0px',
        'sm': '4px',
        'pill': '9999px',
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
        '3xl': '72px',
        'scene': '100svh',
        'long-scene': '160svh',
      },
      transitionDuration: {
        'fast': '180ms',
        'base': '420ms',
        'scene': '900ms',
        'scrub': 'scroll-linked',
      },
      transitionTimingFunction: {
        'cinematic': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'mask': 'cubic-bezier(0.77, 0, 0.175, 1)',
      },
      container: {
        center: true,
        screens: {
          '2xl': 'none',
        },
      },
    },
  },
};
