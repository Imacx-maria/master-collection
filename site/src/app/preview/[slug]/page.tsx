import Link from "next/link";
import { notFound } from "next/navigation";
import { ProductPreviewSurface } from "@/components/catalog/product-preview-surface";
import { ThemeToggle } from "@/components/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { getProductBySlug, products } from "@/lib/products";

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export default async function PreviewPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const product = getProductBySlug(slug);

  if (!product) {
    notFound();
  }

  const productHref = product.type === "template" ? `/templates/${product.slug}` : `/components/${product.slug}`;

  return (
    <main className="min-h-svh bg-background">
      <header className="flex items-center gap-3 border-b border-border px-4 py-3">
        <Link className="text-sm font-semibold" href={productHref}>
          Master Collection
        </Link>
        <Badge variant="outline">public preview</Badge>
        <div className="ml-auto">
          <ThemeToggle />
        </div>
      </header>
      <section className="grid min-h-[calc(100svh-57px)] gap-6 p-4 sm:p-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        <ProductPreviewSurface product={product} />
        <aside className="rounded-md border border-border bg-card p-4">
          <p className="font-mono text-[11px] uppercase text-muted-foreground">{product.type}</p>
          <h1 className="mt-2 text-2xl font-semibold">{product.title}</h1>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">{product.summary}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {product.tags.map((tag) => (
              <Badge key={tag}>{tag}</Badge>
            ))}
          </div>
          <Link className="mt-5 inline-flex text-sm font-medium underline underline-offset-4" href={productHref}>
            Back to product
          </Link>
        </aside>
      </section>
    </main>
  );
}
