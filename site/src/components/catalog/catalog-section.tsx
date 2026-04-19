import { ProductCard } from "@/components/catalog/product-card";
import type { ProductWithVersion } from "@/lib/products";

export function CatalogSection({
  title,
  products,
}: {
  title: string;
  products: ProductWithVersion[];
}) {
  return (
    <section className="flex flex-col gap-4">
      <div className="flex items-end justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          <p className="text-sm text-muted-foreground">{products.length} published items</p>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
}
