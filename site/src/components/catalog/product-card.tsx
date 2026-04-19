import { ArrowUpRight } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { getCreatorBySlug } from "@/lib/creators";
import { formatMoney } from "@/lib/format";
import type { ProductWithVersion } from "@/lib/products";
import { ProductPreviewSurface } from "./product-preview-surface";

export function ProductCard({ product }: { product: ProductWithVersion }) {
  const href = product.type === "template" ? `/templates/${product.slug}` : `/components/${product.slug}`;
  const creator = product.creatorSlug ? getCreatorBySlug(product.creatorSlug) : undefined;

  return (
    <article className="flex min-h-[360px] flex-col rounded-md border border-border bg-card text-card-foreground">
      <ProductPreviewSurface product={product} compact />
      <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="font-mono text-[11px] uppercase text-muted-foreground">
              {product.type}
            </p>
            <h2 className="mt-1 text-base font-semibold">{product.title}</h2>
            {creator ? (
              <Link className="mt-1 block text-xs text-muted-foreground underline-offset-4 hover:underline" href={`/creators/${creator.slug}`}>
                By {creator.name}
              </Link>
            ) : null}
          </div>
          <Badge variant="outline">{formatMoney(product.priceCents, product.currency)}</Badge>
        </div>
        <p className="text-sm leading-6 text-muted-foreground">{product.summary}</p>
        <div className="mt-auto flex flex-wrap gap-2">
          {product.tags.slice(0, 3).map((tag) => (
            <Badge key={tag}>{tag}</Badge>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <LinkButton className="flex-1" href={href} size="sm">
            View
            <ArrowUpRight aria-hidden="true" className="size-3" />
          </LinkButton>
          <LinkButton href={`/preview/${product.slug}`} size="sm" variant="outline">
            Preview
          </LinkButton>
        </div>
      </div>
    </article>
  );
}
