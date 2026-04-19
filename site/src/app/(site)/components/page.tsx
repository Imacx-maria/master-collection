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
      <div className="mx-auto max-w-[1400px] px-6 py-8 sm:px-10 lg:px-14">
        <CatalogSection products={components} title="Component packages" />
      </div>
    </>
  );
}
