import type { Product } from "@/lib/products";
import { cn } from "@/lib/utils";

export function ProductPreviewSurface({
  product,
  compact = false,
}: {
  product: Product;
  compact?: boolean;
}) {
  const cells = product.type === "template" ? 8 : 5;

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-md border border-border bg-muted",
        compact ? "aspect-[4/3]" : "aspect-[16/10]",
      )}
      aria-hidden="true"
    >
      <div className="absolute inset-x-0 top-0 flex h-8 items-center gap-1 border-b border-border bg-background/80 px-3">
        <span className="size-2 rounded-full bg-muted-foreground/30" />
        <span className="size-2 rounded-full bg-muted-foreground/30" />
        <span className="size-2 rounded-full bg-muted-foreground/30" />
        <span className="ml-2 h-2 w-24 rounded-sm bg-muted-foreground/20" />
      </div>
      <div className="grid h-full grid-cols-[1.1fr_0.9fr] gap-3 px-4 pb-4 pt-12">
        <div className="flex flex-col gap-3">
          <span className="h-3 w-28 rounded-sm bg-foreground/80" />
          <span className="h-2 w-40 rounded-sm bg-muted-foreground/30" />
          <span className="h-2 w-32 rounded-sm bg-muted-foreground/20" />
          <div className="mt-auto grid grid-cols-2 gap-2">
            {Array.from({ length: cells }).map((_, index) => (
              <span
                className="h-8 rounded-sm border border-border bg-background/70"
                key={`${product.slug}-preview-cell-${index}`}
              />
            ))}
          </div>
        </div>
        <div className="rounded-md border border-border bg-background/70 p-3">
          <span className="block h-2 w-20 rounded-sm bg-muted-foreground/30" />
          <span className="mt-4 block h-16 rounded-sm bg-muted" />
          <span className="mt-3 block h-2 w-24 rounded-sm bg-muted-foreground/20" />
          <span className="mt-2 block h-2 w-16 rounded-sm bg-muted-foreground/20" />
        </div>
      </div>
    </div>
  );
}
