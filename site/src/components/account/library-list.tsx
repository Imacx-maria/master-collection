import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { ProductPreviewSurface } from "@/components/catalog/product-preview-surface";
import { formatDate } from "@/lib/format";
import type { getLibraryItems } from "@/lib/account";

type LibraryItem = ReturnType<typeof getLibraryItems>[number];

export function LibraryList({ items }: { items: LibraryItem[] }) {
  if (!items.length) {
    return (
      <div className="rounded-md border border-border p-8 text-center">
        <h2 className="text-lg font-semibold">No purchases yet</h2>
        <p className="mt-2 text-sm text-muted-foreground">Purchased templates and components will appear here.</p>
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {items.map((item) => {
        const product = item.product;

        if (!product) {
          return null;
        }

        return (
          <article className="grid gap-4 rounded-md border border-border bg-card p-4 md:grid-cols-[180px_minmax(0,1fr)]" key={item.purchaseId}>
            <ProductPreviewSurface compact product={product} />
            <div className="min-w-0">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="font-mono text-[11px] uppercase text-muted-foreground">{product.type}</p>
                  <Link className="mt-1 block text-lg font-semibold hover:underline" href={`/account/library/${item.purchaseId}`}>
                    {product.title}
                  </Link>
                </div>
                <Badge variant="outline">{item.version?.validationStatus ?? "pending"}</Badge>
              </div>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{product.summary}</p>
              <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                <span>Version {item.version?.version ?? "pending"}</span>
                <span>Purchased {item.order ? formatDate(item.order.createdAt) : "pending"}</span>
                <span>{item.installCode ? "Install code ready" : "Install code pending"}</span>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <LinkButton href={`/account/library/${item.purchaseId}`} size="sm">
                  Open
                </LinkButton>
                <LinkButton href={`/preview/${product.slug}`} size="sm" variant="outline">
                  Preview
                </LinkButton>
              </div>
            </div>
          </article>
        );
      })}
    </div>
  );
}
