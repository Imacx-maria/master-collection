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
      <div className="p-4 sm:p-6">
        <CatalogSection products={templates} title="Template packages" />
      </div>
    </>
  );
}
