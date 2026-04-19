import { CatalogSection } from "@/components/catalog/catalog-section";
import { PageHeading } from "@/components/page-heading";
import { getProducts } from "@/lib/products";

export default function TemplatesPage() {
  const templates = getProducts("template");

  return (
    <>
      <PageHeading
        description="Published template packages with previews, required fonts, and install readiness."
        eyebrow="Catalog"
        title="Templates"
      />
      <div className="mx-auto max-w-[1400px] px-6 py-8 sm:px-10 lg:px-14">
        <CatalogSection products={templates} title="Template packages" />
      </div>
    </>
  );
}
