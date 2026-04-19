import { Check, ExternalLink, LockKeyhole, PackageCheck } from "lucide-react";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import { getProductBySlug, type ProductType } from "@/lib/products";
import { ProductPreviewSurface } from "./product-preview-surface";

export function ProductDetail({
  slug,
  type,
}: {
  slug: string;
  type: ProductType;
}) {
  const product = getProductBySlug(slug);

  if (!product || product.type !== type) {
    notFound();
  }

  const checkoutHref = `/sign-in?intent=checkout&product=${product.slug}`;

  return (
    <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_360px]">
      <section className="border-b border-border p-4 sm:p-6 lg:border-b-0 lg:border-r">
        <div className="mb-5 flex flex-wrap items-center gap-2">
          <Badge variant="outline">{product.type}</Badge>
          <Badge variant={product.currentVersion?.validationStatus === "passed" ? "success" : "warning"}>
            validation: {product.currentVersion?.validationStatus ?? "pending"}
          </Badge>
          <Badge>{product.currentVersion?.packageSchemaVersion ?? "package pending"}</Badge>
        </div>
        <ProductPreviewSurface product={product} />
        <div className="mt-6 grid gap-6 xl:grid-cols-2">
          <div>
            <h2 className="text-sm font-semibold">Included</h2>
            <ul className="mt-3 grid gap-2 text-sm text-muted-foreground">
              {product.included.map((item) => (
                <li className="flex gap-2" key={item}>
                  <Check aria-hidden="true" className="mt-1 size-3 text-foreground" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-sm font-semibold">Compatibility</h2>
            <ul className="mt-3 grid gap-2 text-sm text-muted-foreground">
              {product.compatibilityNotes.map((note) => (
                <li className="flex gap-2" key={note}>
                  <PackageCheck aria-hidden="true" className="mt-1 size-3 text-foreground" />
                  <span>{note}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <aside className="p-4 sm:p-6">
        <div className="sticky top-28 flex flex-col gap-5">
          <div>
            <p className="font-mono text-[11px] uppercase text-muted-foreground">
              {product.currentVersion?.version ?? "0.0.0"} · {product.currentVersion?.packageId ?? "package pending"}
            </p>
            <h1 className="mt-2 text-2xl font-semibold">{product.title}</h1>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">{product.description ?? product.summary}</p>
          </div>

          <div className="rounded-md border border-border bg-card p-4">
            <div className="flex items-center justify-between gap-3">
              <span className="text-sm text-muted-foreground">Price</span>
              <strong className="text-xl">{formatMoney(product.priceCents, product.currency)}</strong>
            </div>
            <div className="mt-4 grid gap-2">
              <LinkButton href={checkoutHref}>Sign in to checkout</LinkButton>
              <LinkButton href={`/preview/${product.slug}`} variant="outline">
                Open preview
                <ExternalLink aria-hidden="true" className="size-3" />
              </LinkButton>
            </div>
            <p className="mt-3 flex gap-2 text-xs leading-5 text-muted-foreground">
              <LockKeyhole aria-hidden="true" className="mt-0.5 size-3 shrink-0" />
              Package JSON and private assets unlock from the account library after checkout.
            </p>
          </div>

          <div className="rounded-md border border-border p-4">
            <h2 className="text-sm font-semibold">Install requirements</h2>
            <dl className="mt-3 grid gap-3 text-sm">
              <div className="flex justify-between gap-3">
                <dt className="text-muted-foreground">Fonts</dt>
                <dd className="text-right">{product.requiredFonts.join(", ")}</dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-muted-foreground">CMS</dt>
                <dd>{product.cmsRequired ? "Required" : "Not required"}</dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-muted-foreground">Custom code</dt>
                <dd>{product.customCodeRequired ? "Documented" : "None"}</dd>
              </div>
            </dl>
          </div>
        </div>
      </aside>
    </div>
  );
}
