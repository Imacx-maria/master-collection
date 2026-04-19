import { CatalogSection } from "@/components/catalog/catalog-section";
import { PageHeading } from "@/components/page-heading";
import { getProducts } from "@/lib/products";

export default function ComponentsPage() {
  const components = getProducts("component");

  return (
    <>
      <PageHeading
        description="Reusable component packages prepared for the Master Collection Webflow app."
        eyebrow="Catalog"
        title="Components"
      />
      <div className="p-4 sm:p-6">
        <CatalogSection products={components} title="Component packages" />
      </div>
    </>
  );
}
