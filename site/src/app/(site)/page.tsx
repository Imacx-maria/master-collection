import { ArrowRight } from "lucide-react";
import { CatalogSection } from "@/components/catalog/catalog-section";
import { PageHeading } from "@/components/page-heading";
import { LinkButton } from "@/components/ui/button";
import { getProducts } from "@/lib/products";

export default function HomePage() {
  const templates = getProducts("template");
  const components = getProducts("component");

  return (
    <>
      <PageHeading
        actions={
          <>
            <LinkButton href="/templates" size="sm" variant="outline">
              Browse templates
            </LinkButton>
            <LinkButton href="/components" size="sm" variant="outline">
              Browse components
            </LinkButton>
          </>
        }
        description="Browse Webflow templates and components, preview the source, then unlock package access and install codes from your account library."
        eyebrow="Master Collection"
        title="Catalog workspace"
      />
      <div className="grid gap-8 p-4 sm:p-6">
        <section className="grid gap-4 border-b border-border pb-8 lg:grid-cols-[1fr_320px]">
          <div className="grid gap-4 md:grid-cols-3">
            {[
              ["Published items", templates.length + components.length],
              ["Template packages", templates.length],
              ["Component packages", components.length],
            ].map(([label, value]) => (
              <div className="rounded-md border border-border bg-card p-4" key={label}>
                <p className="font-mono text-[11px] uppercase text-muted-foreground">{label}</p>
                <p className="mt-2 text-3xl font-semibold">{value}</p>
              </div>
            ))}
          </div>
          <div className="rounded-md border border-border bg-card p-4">
            <p className="font-mono text-[11px] uppercase text-muted-foreground">Buyer flow</p>
            <ol className="mt-3 grid gap-2 text-sm text-muted-foreground">
              {["Preview product", "Sign in", "Checkout", "Open library", "Copy install code"].map((step) => (
                <li className="flex items-center gap-2" key={step}>
                  <ArrowRight aria-hidden="true" className="size-3 text-foreground" />
                  {step}
                </li>
              ))}
            </ol>
          </div>
        </section>
        <CatalogSection products={templates.slice(0, 3)} title="Templates" />
        <CatalogSection products={components.slice(0, 3)} title="Components" />
      </div>
    </>
  );
}
