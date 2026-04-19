export type ProductType = "template" | "component";
export type ProductStatus = "draft" | "published" | "archived";

export type Product = {
  id: string;
  slug: string;
  type: ProductType;
  title: string;
  tagline?: string;
  summary: string;
  description?: string;
  status: ProductStatus;
  currentVersionId?: string;
  priceCents: number;
  currency: string;
  stripePriceId?: string;
  creatorSlug?: string;
  location?: string;
  category?: string;
  updatedAt?: string;
  tags: string[];
  thumbnail?: string;
  requiredFonts: string[];
  included: string[];
  compatibilityNotes: string[];
  cmsRequired: boolean;
  customCodeRequired: boolean;
  showcase?: ProductShowcase;
};

export type ProductShowcase = {
  stats: Array<{
    value: string;
    label: string;
  }>;
  previewNote: string;
  pitchTitle: string;
  pitch: string[];
  featureGrid: Array<{
    icon: "file" | "database" | "zap" | "waves" | "figma" | "book";
    title: string;
    description: string;
  }>;
  pages: Array<{
    name: string;
    description: string;
  }>;
  sections: Array<{
    number: string;
    name: string;
    description: string;
  }>;
  animations: Array<{
    name: string;
    description: string;
  }>;
  techStack: Array<{
    name: string;
    description: string;
  }>;
  assetRequirements: string[];
  skillLevel: string;
  setupTime: string;
  gallery: string[];
  faq: Array<{
    question: string;
    answer: string;
  }>;
};

export type ProductVersion = {
  id: string;
  productId: string;
  version: string;
  packageId: string;
  packageSchemaVersion: "master-collection-package@1";
  previewUrl?: string;
  packageStorageKey?: string;
  validationStatus: "pending" | "passed" | "failed";
  status: ProductStatus;
};

export type ProductWithVersion = Product & {
  currentVersion?: ProductVersion;
};

export const products: Product[] = [
  {
    id: "prod-jb-studio-ldn",
    slug: "jb-studio-ldn",
    type: "template",
    title: "JB Studio LDN",
    tagline: "A cinematic, motion-first agency and portfolio template. Built for studios that want to stop whispering.",
    summary: "Motion-led agency portfolio template with CMS projects, GSAP interactions, smooth scroll, and a documented setup path.",
    description:
      "A full-bleed, motion-led template for agencies, portfolios, and experience studios that need big type, cinematic project reveals, and a smooth-scroll feel.",
    status: "published",
    currentVersionId: "ver-jb-studio-ldn-1",
    priceCents: 14900,
    currency: "GBP",
    stripePriceId: "price_jb_studio_ldn_placeholder",
    creatorSlug: "joseph-berry",
    location: "London",
    category: "Agency / Portfolio",
    updatedAt: "2026-04-19",
    tags: ["Agency", "Portfolio", "Motion"],
    requiredFonts: ["Inter", "IBM Plex Mono"],
    included: ["Home", "Work", "Studio", "On Demand", "Playground", "Project Detail"],
    compatibilityNotes: ["CMS collections pre-configured", "GSAP interactions documented", "Lenis smooth scroll included"],
    cmsRequired: true,
    customCodeRequired: true,
    showcase: {
      stats: [
        { value: "6", label: "Pages" },
        { value: "14", label: "Sections" },
        { value: "12+", label: "Animations" },
        { value: "100%", label: "Responsive" },
      ],
      previewNote: "Hover to play. Tap to open full-screen. Built with Webflow, GSAP, and Lenis smooth scroll.",
      pitchTitle: "Built for studios that let the work do the talking.",
      pitch: [
        "JB Studio LDN is a full-bleed, motion-led template for agencies, portfolios, and experience studios. No sliders pretending to be carousels. No stock-hero cliches. Just big type, cinematic project reveals, and a smooth-scroll feel that makes your work look expensive because it is.",
        "Designed and built by Joseph Berry, Awwwards Jury, Webflow Professional Partner, and the studio behind JB Studio LDN.",
      ],
      featureGrid: [
        { icon: "file", title: "6 Pages", description: "Home, Work index, Studio, On Demand, Playground, Project Detail (CMS)." },
        { icon: "database", title: "CMS Ready", description: "Projects, Services, and Journal collections pre-configured." },
        { icon: "zap", title: "GSAP Interactions", description: "12+ scroll-triggered animations. Fully customisable." },
        { icon: "waves", title: "Lenis Smooth Scroll", description: "Silk-smooth feel across desktop and touch." },
        { icon: "figma", title: "Figma Source", description: "Full design file, components, and style guide included." },
        { icon: "book", title: "Documentation", description: "Step-by-step setup, swap guide, and custom code notes." },
      ],
      pages: [
        { name: "Home", description: "Animated hero with cycling word morph, showreel, 4 project reveals, studio intro, services wall, what's hot slider." },
        { name: "Work", description: "Full project index with filterable CMS grid and hover-to-play video previews." },
        { name: "Studio", description: "About page with team, services, clients, awards, and manifesto." },
        { name: "On Demand", description: "Productised services page with pricing cards and scope breakdown." },
        { name: "Playground", description: "Experiments, cloneables, and side projects. CMS-driven." },
        { name: "Project Detail (CMS)", description: "Template for every case study: hero video, challenge, approach, outcome, image gallery, next project reveal." },
      ],
      sections: [
        { number: "01", name: "Navigation bar", description: "Minimal top nav with logo, live London time, menu toggle, and Start a Project CTA." },
        { number: "02", name: "Animated hero", description: "Full-screen video background with morphing word cycle for brand, product, experience, and digital." },
        { number: "03", name: "Showreel block", description: "Oversized statement type with click-to-play Vimeo modal." },
        { number: "04", name: "Project reveal x4", description: "Full-bleed video and image blocks with bottom-row metadata." },
        { number: "05", name: "Studio intro", description: "Manifesto section with ambient video background and geometric marks." },
        { number: "06", name: "Services wall", description: "Stacked oversized type list with plus markers and end-of-block CTA." },
        { number: "07", name: "What's Hot slider", description: "3-up Splide.js carousel for news, talks, and upcoming work." },
        { number: "08", name: "Multi-step form modal", description: "5-step intake: Services, Project, Budget, Timeframe, Details." },
        { number: "09", name: "Footer", description: "Big closing CTA, social links, studio mark." },
        { number: "10", name: "Work index grid", description: "CMS-driven project list with hover video previews." },
        { number: "11", name: "Project detail hero", description: "Full-bleed cover with title, year, and services overlay." },
        { number: "12", name: "Case study body", description: "Text and image blocks, full-bleed media, and pull-quote styling." },
        { number: "13", name: "Next project", description: "Animated transition into the following case study." },
        { number: "14", name: "404 and Password page", description: "On-brand error states so nothing feels unfinished." },
      ],
      animations: [
        { name: "Word morph hero", description: "Type cycles through four words with mask reveal and staggered characters." },
        { name: "Full-bleed reveal", description: "Project sections scale in from 80% to 100% with subtle y-axis drift." },
        { name: "Lenis smooth scroll", description: "The whole page moves like butter. Scroll bar optional." },
        { name: "Services wall stagger", description: "Each service line animates in on scroll with a plus marker fade." },
        { name: "Hover video previews", description: "Work grid thumbnails play a silent loop on hover." },
        { name: "Slider transitions", description: "800ms ease on the What's Hot carousel. Drag-enabled." },
        { name: "Modal choreography", description: "5-step form slides and fades between states without losing context." },
        { name: "Page transitions", description: "600ms delay and custom transition mask covers the next page load." },
      ],
      techStack: [
        { name: "Webflow", description: "Core build. Editor-friendly, client-ready." },
        { name: "GSAP", description: "Advanced timelines and ScrollTrigger." },
        { name: "Lenis", description: "Smooth scroll without the JS tax." },
        { name: "Splide.js", description: "Lightweight, touch-enabled slider." },
        { name: "Vimeo", description: "Lazy-loaded video with custom controls." },
        { name: "Moment.js", description: "Powers the live location clock." },
      ],
      assetRequirements: [
        "5-8 project videos, 1920x1080 minimum, MP4 or WebM, 4-10 second loops.",
        "1 showreel video hosted on Vimeo with embed ID.",
        "1 hero background video, muted, autoplay, loop-friendly.",
        "8-12 hero and thumbnail images, 2400px on the long edge, JPEG or WebP.",
        "Logo files, SVG preferred, light and dark variants.",
        "Brand typography with any Typekit or Google font pairing.",
      ],
      skillLevel: "Intermediate",
      setupTime: "2-4 hours",
      gallery: Array.from({ length: 9 }, (_, index) => `Screenshot ${index + 1}`),
      faq: [
        { question: "What Webflow plan do I need?", answer: "A CMS plan is recommended because the project and journal structures are CMS-ready." },
        { question: "Is the Figma file included?", answer: "Yes. The template includes the source design file, components, and style guide." },
        { question: "Can I use this for client work?", answer: "Yes. One purchase can be used for one client or one owned project." },
        { question: "Do I need to know GSAP?", answer: "You do not need to write GSAP from scratch, but basic comfort with custom code embeds helps." },
        { question: "Is it responsive?", answer: "Yes. Desktop, tablet, and mobile breakpoints are included and documented." },
        { question: "Will it work with Webflow Interactions 2.0?", answer: "Yes. GSAP and Webflow interaction notes are included in the setup docs." },
        { question: "How do I get support?", answer: "Use the support email from your account library after purchase." },
        { question: "Can I get a refund?", answer: "Refunds are handled case by case for broken package access or duplicate purchases." },
      ],
    },
  },
  {
    id: "prod-atlas-studio",
    slug: "atlas-studio",
    type: "template",
    title: "Atlas Studio",
    summary: "Editorial studio template with work index, case pages, and compact CMS-ready sections.",
    description:
      "A restrained portfolio system for studios that need crisp project browsing, clean page sections, and a fast install path inside Webflow.",
    status: "published",
    currentVersionId: "ver-atlas-studio-1",
    priceCents: 14900,
    currency: "USD",
    stripePriceId: "price_atlas_studio_placeholder",
    creatorSlug: "joseph-berry",
    location: "London",
    category: "Portfolio",
    updatedAt: "2026-04-19",
    tags: ["Portfolio", "CMS-ready", "Responsive"],
    requiredFonts: ["Inter", "IBM Plex Mono"],
    included: ["Home", "Work index", "Case detail", "Contact", "Utility sections"],
    compatibilityNotes: ["Webflow responsive breakpoints", "CMS collections optional", "No custom code required"],
    cmsRequired: false,
    customCodeRequired: false,
  },
  {
    id: "prod-foundry-commerce",
    slug: "foundry-commerce",
    type: "template",
    title: "Foundry Commerce",
    summary: "Product-forward storefront frame with launch blocks, product grids, and proof sections.",
    description:
      "A neutral ecommerce-style template for small catalogs, digital goods, and service offers that need a compact launch surface.",
    status: "published",
    currentVersionId: "ver-foundry-commerce-1",
    priceCents: 17900,
    currency: "USD",
    creatorSlug: "joseph-berry",
    location: "London",
    category: "Storefront",
    updatedAt: "2026-04-19",
    tags: ["Storefront", "Launch", "Products"],
    requiredFonts: ["Inter"],
    included: ["Catalog home", "Product detail", "Feature rows", "FAQ", "Checkout handoff sections"],
    compatibilityNotes: ["Webflow Ecommerce not required", "Works as marketing storefront", "Images use local assets"],
    cmsRequired: false,
    customCodeRequired: false,
  },
  {
    id: "prod-signal-launch",
    slug: "signal-launch",
    type: "template",
    title: "Signal Launch",
    summary: "Compact launch system for SaaS, apps, and technical product announcements.",
    description:
      "A sharper technical template with dense feature panels, status rows, and documentation-style section rhythm.",
    status: "published",
    currentVersionId: "ver-signal-launch-1",
    priceCents: 12900,
    currency: "USD",
    creatorSlug: "joseph-berry",
    location: "London",
    category: "SaaS",
    updatedAt: "2026-04-19",
    tags: ["SaaS", "Launch", "Technical"],
    requiredFonts: ["Inter", "IBM Plex Mono"],
    included: ["Overview", "Features", "Changelog", "Pricing blocks", "Docs gateway"],
    compatibilityNotes: ["No CMS dependency", "Optional custom script area is documented", "Assets included"],
    cmsRequired: false,
    customCodeRequired: true,
  },
  {
    id: "prod-pricing-grid",
    slug: "pricing-grid",
    type: "component",
    title: "Pricing Grid",
    summary: "Three-tier pricing component with comparison rows, badges, and compact mobile layout.",
    description:
      "A ready-to-install pricing section with stable responsive columns and a small comparison table.",
    status: "published",
    currentVersionId: "ver-pricing-grid-1",
    priceCents: 3900,
    currency: "USD",
    stripePriceId: "price_pricing_grid_placeholder",
    creatorSlug: "joseph-berry",
    location: "London",
    category: "Pricing",
    updatedAt: "2026-04-19",
    tags: ["Pricing", "Section", "Responsive"],
    requiredFonts: ["Inter"],
    included: ["Pricing cards", "Comparison rows", "CTA row", "Mobile stack"],
    compatibilityNotes: ["No CMS dependency", "No custom code required", "Works in any page section"],
    cmsRequired: false,
    customCodeRequired: false,
  },
  {
    id: "prod-proof-rail",
    slug: "proof-rail",
    type: "component",
    title: "Proof Rail",
    summary: "Logo, quote, and metrics rail for evidence-heavy landing pages.",
    description:
      "A compact social-proof component with responsive metric blocks and a controlled quote layout.",
    status: "published",
    currentVersionId: "ver-proof-rail-1",
    priceCents: 2900,
    currency: "USD",
    tags: ["Proof", "Logos", "Metrics"],
    requiredFonts: ["Inter"],
    included: ["Logo rail", "Quote block", "Metric set", "Dark variant"],
    compatibilityNotes: ["Static content first", "CMS can be wired later", "No Webflow token needed"],
    cmsRequired: false,
    customCodeRequired: false,
  },
  {
    id: "prod-cms-feature-list",
    slug: "cms-feature-list",
    type: "component",
    title: "CMS Feature List",
    summary: "CMS-backed feature list with filters, icon slots, and validation notes.",
    description:
      "A component package for teams that need a repeatable feature library while keeping installation inside Webflow.",
    status: "published",
    currentVersionId: "ver-cms-feature-list-1",
    priceCents: 4900,
    currency: "USD",
    tags: ["CMS", "Features", "Filters"],
    requiredFonts: ["Inter", "IBM Plex Mono"],
    included: ["Feature list", "Filter controls", "Empty state", "CMS field notes"],
    compatibilityNotes: ["CMS collection required", "Field names documented", "No custom code required"],
    cmsRequired: true,
    customCodeRequired: false,
  },
];

export const productVersions: ProductVersion[] = products.map((product) => ({
  id: product.currentVersionId ?? `${product.id}-version`,
  productId: product.id,
  version: product.slug === "cms-feature-list" ? "0.9.0" : "1.0.0",
  packageId: `pkg-${product.slug}-v1`,
  packageSchemaVersion: "master-collection-package@1",
  previewUrl: `/preview/${product.slug}`,
  packageStorageKey: `fixtures/${product.slug}/master-collection-package.json`,
  validationStatus: product.slug === "cms-feature-list" ? "pending" : "passed",
  status: product.status,
}));

export function getProducts(type?: ProductType): ProductWithVersion[] {
  return products
    .filter((product) => product.status === "published")
    .filter((product) => (type ? product.type === type : true))
    .map(withCurrentVersion);
}

export function getProductBySlug(slug: string) {
  const product = products.find((item) => item.slug === slug && item.status === "published");
  return product ? withCurrentVersion(product) : undefined;
}

export function getProductById(id: string) {
  const product = products.find((item) => item.id === id);
  return product ? withCurrentVersion(product) : undefined;
}

export function getProductVersion(versionId: string) {
  return productVersions.find((version) => version.id === versionId);
}

export function getProductVersionByPackageId(packageId: string) {
  return productVersions.find((version) => version.packageId === packageId);
}

export function getFeaturedProducts() {
  return getProducts().slice(0, 4);
}

export function getProductsByCreator(creatorSlug: string, type?: ProductType) {
  return getProducts(type).filter((product) => product.creatorSlug === creatorSlug);
}

function withCurrentVersion(product: Product): ProductWithVersion {
  return {
    ...product,
    currentVersion: productVersions.find((version) => version.id === product.currentVersionId),
  };
}
