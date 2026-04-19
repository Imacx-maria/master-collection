import { notFound } from "next/navigation";
import { CreatorProfile } from "@/components/creators/creator-profile";
import { creators, getCreatorBySlug } from "@/lib/creators";
import { getProductsByCreator } from "@/lib/products";

export function generateStaticParams() {
  return creators.map((creator) => ({ slug: creator.slug }));
}

export default async function CreatorPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const creator = getCreatorBySlug(slug);

  if (!creator) {
    notFound();
  }

  return <CreatorProfile creator={creator} products={getProductsByCreator(creator.slug, "template")} />;
}
