"use client";

import {
  BookOpen,
  Database,
  ExternalLink,
  FileText,
  Palette,
  Play,
  Waves,
  Zap,
} from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import type { Creator } from "@/lib/creators";
import type { ProductShowcase, ProductWithVersion } from "@/lib/products";
import { cn } from "@/lib/utils";
import { ProductPreviewSurface } from "./product-preview-surface";

const iconMap = {
  file: FileText,
  database: Database,
  zap: Zap,
  waves: Waves,
  figma: Palette,
  book: BookOpen,
};

type Viewport = "Desktop" | "Tablet" | "Mobile";

export function TemplateShowcaseDetail({
  product,
  creator,
  relatedProducts,
}: {
  product: ProductWithVersion;
  creator?: Creator;
  relatedProducts: ProductWithVersion[];
}) {
  const [viewport, setViewport] = useState<Viewport>("Desktop");
  const showcase = product.showcase ?? createFallbackShowcase(product);
  const checkoutHref = `/sign-in?intent=checkout&product=${product.slug}`;

  return (
    <article className="bg-background pb-20 text-foreground">
      <StickyTemplateCta
        checkoutHref={checkoutHref}
        previewHref={`/preview/${product.slug}`}
        price={formatMoney(product.priceCents, product.currency)}
        title={product.title}
      />

      <section className="mx-auto grid max-w-[1400px] gap-10 px-6 py-12 sm:px-10 lg:grid-cols-[minmax(0,1fr)_420px] lg:px-14">
        <div className="grid gap-6">
          <nav className="flex flex-wrap gap-2 font-mono text-[11px] uppercase text-muted-foreground" aria-label="Breadcrumb">
            <Link className="hover:text-foreground" href="/templates">
              Templates
            </Link>
            <span>/</span>
            <span>{product.category ?? "Template"}</span>
            <span>/</span>
            <span>{product.title}</span>
          </nav>

          <div className="grid gap-4">
            <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
              <span>{creator ? `By ${creator.name}` : "Independent creator"}</span>
              <span aria-hidden="true">.</span>
              <span>{product.location ?? creator?.location ?? "Remote"}</span>
              <span aria-hidden="true">.</span>
              <span>{product.category ?? "Template"}</span>
              <span aria-hidden="true">.</span>
              <span>{product.updatedAt ?? "Updated 2026"}</span>
            </div>
            <h1 className="max-w-4xl text-5xl font-semibold leading-tight tracking-normal text-foreground md:text-6xl">
              {product.title}
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-muted-foreground">{product.tagline ?? product.summary}</p>
          </div>

          <div className="flex flex-wrap gap-3">
            <LinkButton href={checkoutHref} size="md">
              Buy Template - {formatMoney(product.priceCents, product.currency)}
            </LinkButton>
            <LinkButton href={`/preview/${product.slug}`} size="md" variant="outline">
              Preview Live
              <ExternalLink aria-hidden="true" className="size-3" />
            </LinkButton>
          </div>

          <p className="text-sm text-muted-foreground">
            Includes Webflow project, CMS collections, source design file, interactions, documentation, and support notes.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-2">
          {showcase.stats.map((stat) => (
            <div className="rounded-md border border-border bg-muted/50 p-5 text-center" key={stat.label}>
              <strong className="block text-3xl font-semibold">{stat.value}</strong>
              <span className="mt-1 block text-xs text-muted-foreground">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="border-y border-border bg-muted/40">
        <div className="mx-auto max-w-[1400px] px-6 py-10 sm:px-10 lg:px-14">
          <div className="mb-3 font-mono text-[11px] uppercase tracking-normal text-muted-foreground">Live Preview</div>
          <div className="relative overflow-hidden rounded-md border border-border bg-background">
            <div className="absolute right-3 top-3 z-10 flex rounded-md border border-border bg-background p-1">
              {(["Desktop", "Tablet", "Mobile"] as const).map((item) => (
                <button
                  className={cn(
                    "h-8 rounded-sm px-3 text-xs transition-colors",
                    viewport === item ? "bg-foreground text-background" : "text-muted-foreground hover:bg-muted hover:text-foreground",
                  )}
                  key={item}
                  onClick={() => setViewport(item)}
                  type="button"
                >
                  {item}
                </button>
              ))}
            </div>
            <div
              className={cn(
                "mx-auto p-4 pt-16 transition-all",
                viewport === "Desktop" && "max-w-full",
                viewport === "Tablet" && "max-w-3xl",
                viewport === "Mobile" && "max-w-sm",
              )}
            >
              <ProductPreviewSurface product={product} />
            </div>
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
              <span className="inline-flex size-16 items-center justify-center rounded-full border border-border bg-background shadow-sm">
                <Play aria-hidden="true" className="size-5" />
              </span>
            </div>
          </div>
          <p className="mt-3 text-center text-sm text-muted-foreground">{showcase.previewNote}</p>
        </div>
      </section>

      <ShowcaseSection>
        <div className="max-w-3xl">
          <h2 className="text-3xl font-semibold tracking-normal">{showcase.pitchTitle}</h2>
          <div className="mt-5 grid gap-4 text-base leading-8 text-muted-foreground">
            {showcase.pitch.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
        </div>
      </ShowcaseSection>

      <ShowcaseSection title="What's included">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {showcase.featureGrid.map((feature) => {
            const Icon = iconMap[feature.icon];

            return (
              <div className="rounded-md border border-border bg-background p-5" key={feature.title}>
                <Icon aria-hidden="true" className="size-5" />
                <h3 className="mt-4 text-base font-semibold">{feature.title}</h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </ShowcaseSection>

      <ShowcaseSection title="Pages included">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {showcase.pages.map((page) => (
            <div className="overflow-hidden rounded-md border border-border bg-background" key={page.name}>
              <ImagePlaceholder label={page.name} />
              <div className="p-4">
                <h3 className="text-sm font-semibold">{page.name}</h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{page.description}</p>
                <Link className="mt-3 inline-flex text-sm underline underline-offset-4" href={`/preview/${product.slug}`}>
                  Preview
                </Link>
              </div>
            </div>
          ))}
        </div>
      </ShowcaseSection>

      <ShowcaseSection description="14 sections, each built to earn its place." title="Every section documented">
        <div className="grid gap-x-10 md:grid-cols-2">
          {showcase.sections.map((section) => (
            <div className="grid grid-cols-[80px_1fr] gap-4 border-b border-border py-4" key={section.number}>
              <div className="flex h-14 items-center justify-center rounded-md border border-border bg-muted font-mono text-[11px] text-muted-foreground">
                {section.number}
              </div>
              <div>
                <h3 className="text-sm font-semibold">{section.name}</h3>
                <p className="mt-1 text-sm leading-6 text-muted-foreground">{section.description}</p>
              </div>
            </div>
          ))}
        </div>
      </ShowcaseSection>

      <ShowcaseSection description="Every animation built with GSAP and Webflow Interactions. No duct tape, no jank." title="Motion that earns its keep">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {showcase.animations.map((animation) => (
            <div className="overflow-hidden rounded-md border border-border bg-background" key={animation.name}>
              <div className="relative flex h-36 items-center justify-center bg-muted">
                <span className="inline-flex size-12 items-center justify-center rounded-full border border-border bg-background">
                  <Play aria-hidden="true" className="size-4" />
                </span>
                <Badge className="absolute right-2 top-2" variant="outline">
                  Plays on hover
                </Badge>
              </div>
              <div className="p-4">
                <h3 className="text-sm font-semibold">{animation.name}</h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{animation.description}</p>
              </div>
            </div>
          ))}
        </div>
      </ShowcaseSection>

      <ShowcaseSection tone="muted" title="Under the hood">
        <div className="grid overflow-hidden rounded-md border border-border bg-background md:grid-cols-3 xl:grid-cols-6">
          {showcase.techStack.map((tech) => (
            <div className="border-b border-border p-5 text-center md:border-r xl:border-b-0" key={tech.name}>
              <div className="mx-auto flex size-10 items-center justify-center rounded-md border border-border bg-muted text-xs font-semibold">
                {tech.name.slice(0, 2)}
              </div>
              <h3 className="mt-3 text-sm font-semibold">{tech.name}</h3>
              <p className="mt-2 text-xs leading-5 text-muted-foreground">{tech.description}</p>
            </div>
          ))}
        </div>
      </ShowcaseSection>

      <ShowcaseSection>
        <div className="grid gap-10 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-semibold">What you will need to make it yours.</h2>
            <ul className="mt-5 grid gap-3 text-sm leading-6 text-muted-foreground">
              {showcase.assetRequirements.map((requirement) => (
                <li className="flex gap-3" key={requirement}>
                  <span aria-hidden="true" className="mt-2 size-1.5 rounded-full bg-muted-foreground" />
                  <span>{requirement}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <InfoTile label="Skill level" value={showcase.skillLevel} />
            <InfoTile label="Setup time" value={showcase.setupTime} />
          </div>
        </div>
      </ShowcaseSection>

      <ShowcaseSection description="Desktop, tablet, mobile. Light where it lands, motion where it matters." title="See it in every light">
        <div className="grid gap-3 md:grid-cols-3">
          {showcase.gallery.map((item, index) => (
            <ImagePlaceholder className={index % 3 === 0 ? "min-h-52" : "min-h-40"} key={item} label={item} />
          ))}
        </div>
      </ShowcaseSection>

      {creator ? <DesignerBio creator={creator} /> : null}

      <ShowcaseSection title="Questions, answered">
        <div className="divide-y divide-border rounded-md border border-border bg-background">
          {showcase.faq.map((item) => (
            <details className="group" key={item.question}>
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-4 text-sm font-medium">
                {item.question}
                <span className="text-muted-foreground transition-transform group-open:rotate-45">+</span>
              </summary>
              <p className="px-4 pb-4 text-sm leading-6 text-muted-foreground">{item.answer}</p>
            </details>
          ))}
        </div>
      </ShowcaseSection>

      <ShowcaseSection title={creator ? `More from ${creator.name}` : "Related templates"}>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {relatedProducts.map((related) => (
            <RelatedTemplateCard key={related.id} product={related} />
          ))}
        </div>
      </ShowcaseSection>

      <section className="border-t border-border bg-muted/60">
        <div className="mx-auto max-w-[1400px] px-6 py-16 text-center sm:px-10 lg:px-14">
          <h2 className="text-3xl font-semibold tracking-normal">Ready to ship something that moves?</h2>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-muted-foreground">
            Every template on the marketplace is hand-built by the designer credited. No recycled components, just work you would be proud to put your own name on.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <LinkButton href={checkoutHref}>Buy Template - {formatMoney(product.priceCents, product.currency)}</LinkButton>
            <LinkButton href={`/preview/${product.slug}`} variant="outline">
              Preview Live
            </LinkButton>
          </div>
        </div>
      </section>
    </article>
  );
}

function StickyTemplateCta({
  title,
  price,
  checkoutHref,
  previewHref,
}: {
  title: string;
  price: string;
  checkoutHref: string;
  previewHref: string;
}) {
  return (
    <div className="sticky top-[89px] z-30 border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex max-w-[1400px] items-center gap-4 px-6 py-3 sm:px-10 lg:px-14">
        <div className="min-w-0 flex-1">
          <span className="font-semibold">{title}</span>
          <span className="ml-3 text-sm text-muted-foreground">{price}</span>
        </div>
        <LinkButton href={checkoutHref} size="sm">
          Buy
        </LinkButton>
        <LinkButton className="hidden sm:inline-flex" href={previewHref} size="sm" variant="outline">
          Preview
        </LinkButton>
      </div>
    </div>
  );
}

function ShowcaseSection({
  title,
  description,
  tone = "plain",
  children,
}: {
  title?: string;
  description?: string;
  tone?: "plain" | "muted";
  children: ReactNode;
}) {
  return (
    <section className={cn("border-b border-border", tone === "muted" && "bg-muted/40")}>
      <div className="mx-auto max-w-[1400px] px-6 py-10 sm:px-10 lg:px-14">
        {title ? (
          <div className="mb-6">
            <h2 className="text-2xl font-semibold tracking-normal">{title}</h2>
            {description ? <p className="mt-2 text-sm text-muted-foreground">{description}</p> : null}
          </div>
        ) : null}
        {children}
      </div>
    </section>
  );
}

function ImagePlaceholder({ label, className }: { label: string; className?: string }) {
  return (
    <div
      className={cn(
        "flex min-h-36 items-center justify-center rounded-md border border-border bg-muted text-xs text-muted-foreground",
        className,
      )}
    >
      {label}
    </div>
  );
}

function InfoTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-border bg-background p-5">
      <p className="font-mono text-[11px] uppercase text-muted-foreground">{label}</p>
      <p className="mt-3 text-2xl font-semibold">{value}</p>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">
        Planned for buyers who are comfortable editing Webflow structure, CMS fields, and documented custom code.
      </p>
    </div>
  );
}

function DesignerBio({ creator }: { creator: Creator }) {
  return (
    <ShowcaseSection tone="muted" title="About the designer">
      <div className="rounded-md border border-border bg-background p-5">
        <div className="grid gap-6 sm:grid-cols-[96px_1fr]">
          <div className="flex size-24 items-center justify-center rounded-full border border-border bg-muted text-sm font-semibold">
            {creator.initials}
          </div>
          <div>
            <div className="flex flex-wrap items-baseline gap-2">
              <h3 className="text-xl font-semibold">{creator.name}</h3>
              <span className="text-sm text-muted-foreground">
                {creator.title} . {creator.location}
              </span>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {creator.badges.slice(0, 3).map((badge) => (
                <Badge key={badge} variant="outline">
                  {badge}
                </Badge>
              ))}
            </div>
            <div className="mt-4 grid gap-3 text-sm leading-7 text-muted-foreground">
              {creator.bio.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
            <Link className="mt-4 inline-flex text-sm font-medium underline underline-offset-4" href={`/creators/${creator.slug}`}>
              More by {creator.shortName}
            </Link>
          </div>
        </div>
      </div>
    </ShowcaseSection>
  );
}

function RelatedTemplateCard({ product }: { product: ProductWithVersion }) {
  return (
    <article className="overflow-hidden rounded-md border border-border bg-background">
      <ImagePlaceholder label="Preview" />
      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-sm font-semibold">{product.title}</h3>
          <span className="text-sm font-semibold">{formatMoney(product.priceCents, product.currency)}</span>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {product.tags.slice(0, 2).map((tag) => (
            <Badge key={tag}>{tag}</Badge>
          ))}
        </div>
        <LinkButton className="mt-4 w-full" href={`/templates/${product.slug}`} size="sm" variant="outline">
          View
        </LinkButton>
      </div>
    </article>
  );
}

function createFallbackShowcase(product: ProductWithVersion): ProductShowcase {
  return {
    stats: [
      { value: String(product.included.length), label: "Pages" },
      { value: "8+", label: "Sections" },
      { value: product.customCodeRequired ? "Custom" : "Native", label: "Motion" },
      { value: "100%", label: "Responsive" },
    ],
    previewNote: "Preview the package before checkout, then unlock install codes from your account library.",
    pitchTitle: product.summary,
    pitch: [product.description ?? product.summary],
    featureGrid: [
      { icon: "file", title: "Pages included", description: product.included.join(", ") },
      { icon: "database", title: product.cmsRequired ? "CMS required" : "CMS optional", description: "Setup notes are documented in the package." },
      { icon: "book", title: "Documentation", description: "Install notes, font requirements, and compatibility guidance are included." },
      { icon: "zap", title: "Interactions", description: product.customCodeRequired ? "Custom code is documented." : "No custom code required." },
      { icon: "figma", title: "Source ready", description: "Prepared for preview, checkout, account library, and package access." },
      { icon: "waves", title: "Responsive", description: "Built for Webflow responsive breakpoints." },
    ],
    pages: product.included.map((item) => ({ name: item, description: `${item} page or section included in the package.` })),
    sections: product.included.concat(product.compatibilityNotes).slice(0, 14).map((item, index) => ({
      number: String(index + 1).padStart(2, "0"),
      name: item,
      description: `${item} is documented for installation and buyer handoff.`,
    })),
    animations: Array.from({ length: 8 }, (_, index) => ({
      name: `Interaction ${index + 1}`,
      description: "Animation and responsive behavior documented in the package notes.",
    })),
    techStack: [
      { name: "Webflow", description: "Core build." },
      { name: "CMS", description: product.cmsRequired ? "Required." : "Optional." },
      { name: "Assets", description: "Packaged for install." },
      { name: "Fonts", description: product.requiredFonts.join(", ") },
      { name: "Preview", description: "Public preview route." },
      { name: "Install", description: "Account library code." },
    ],
    assetRequirements: product.compatibilityNotes,
    skillLevel: product.customCodeRequired ? "Intermediate" : "Beginner",
    setupTime: "1-3 hours",
    gallery: Array.from({ length: 9 }, (_, index) => `Screenshot ${index + 1}`),
    faq: [
      { question: "What is included?", answer: product.included.join(", ") },
      { question: "Is it responsive?", answer: "Yes. Webflow responsive breakpoints are part of the package." },
      { question: "Do I need custom code?", answer: product.customCodeRequired ? "Yes, documented custom code is included." : "No custom code is required." },
      { question: "Are fonts included?", answer: product.requiredFonts.join(", ") },
      { question: "Is CMS required?", answer: product.cmsRequired ? "Yes, CMS collections are required." : "No, CMS is optional." },
      { question: "Can I preview it?", answer: "Yes. Use the public preview before checkout." },
      { question: "How do I install it?", answer: "Buy it, open your account library, copy the install code, and paste it into the Webflow app." },
      { question: "Can I use it for client work?", answer: "Yes, for one client or one owned project per purchase." },
    ],
  };
}
