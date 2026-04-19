export type ProductType = "template" | "component";
export type ProductStatus = "draft" | "published" | "archived";

export type Product = {
  id: string;
  slug: string;
  type: ProductType;
  title: string;
  summary: string;
  description?: string;
  status: ProductStatus;
  currentVersionId?: string;
  priceCents: number;
  currency: string;
  stripePriceId?: string;
  tags: string[];
  thumbnail?: string;
  requiredFonts: string[];
  included: string[];
  compatibilityNotes: string[];
  cmsRequired: boolean;
  customCodeRequired: boolean;
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

function withCurrentVersion(product: Product): ProductWithVersion {
  return {
    ...product,
    currentVersion: productVersions.find((version) => version.id === product.currentVersionId),
  };
}
