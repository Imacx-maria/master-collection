import { ProductDetail } from "@/components/catalog/product-detail";
import { products } from "@/lib/products";

export function generateStaticParams() {
  return products.filter((product) => product.type === "template").map((product) => ({ slug: product.slug }));
}

export default async function TemplateDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  return <ProductDetail slug={slug} type="template" />;
}
