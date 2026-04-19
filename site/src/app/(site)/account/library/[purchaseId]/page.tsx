import { notFound } from "next/navigation";
import { InstallCodePanel } from "@/components/account/install-code-panel";
import { ProductPreviewSurface } from "@/components/catalog/product-preview-surface";
import { PageHeading } from "@/components/page-heading";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { getLibraryItem } from "@/lib/account";

export default async function AccountLibraryDetailPage({
  params,
}: {
  params: Promise<{ purchaseId: string }>;
}) {
  const { purchaseId } = await params;
  const item = getLibraryItem(purchaseId);

  if (!item?.product) {
    notFound();
  }

  return (
    <>
      <PageHeading
        actions={
          <>
            <LinkButton href={`/preview/${item.product.slug}`} size="sm" variant="outline">
              Preview
            </LinkButton>
            <LinkButton href="/account/installations" size="sm" variant="outline">
              Install history
            </LinkButton>
          </>
        }
        description="Use this install code inside the Master Collection Webflow app. The website does not ask for Webflow site IDs, page IDs, or API tokens."
        eyebrow="Owned product"
        title={item.product.title}
      />
      <div className="grid gap-6 p-4 sm:p-6 xl:grid-cols-[minmax(0,1fr)_420px]">
        <section className="grid gap-6">
          <ProductPreviewSurface product={item.product} />
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-md border border-border p-4">
              <h2 className="text-sm font-semibold">Package status</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                <Badge variant="outline">version {item.version?.version ?? "pending"}</Badge>
                <Badge>{item.version?.packageSchemaVersion ?? "package pending"}</Badge>
                <Badge variant={item.version?.validationStatus === "passed" ? "success" : "warning"}>
                  {item.version?.validationStatus ?? "pending"}
                </Badge>
              </div>
            </div>
            <div className="rounded-md border border-border p-4">
              <h2 className="text-sm font-semibold">Requirements</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Fonts: {item.product.requiredFonts.join(", ")}. CMS: {item.product.cmsRequired ? "required" : "not required"}.
              </p>
            </div>
          </div>
        </section>
        <aside className="grid content-start gap-4">
          <InstallCodePanel installCode={item.installCode} />
          <div className="rounded-md border border-border p-4 text-sm leading-6 text-muted-foreground">
            Open Webflow, launch the Master Collection app, paste the code, and let the app resolve the package
            and upload assets into the current Webflow site.
          </div>
        </aside>
      </div>
    </>
  );
}
