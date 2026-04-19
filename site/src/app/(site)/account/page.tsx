import { LibraryList } from "@/components/account/library-list";
import { PageHeading } from "@/components/page-heading";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { getLibraryItems } from "@/lib/account";

export default function AccountPage() {
  const items = getLibraryItems();

  return (
    <>
      <PageHeading
        actions={<LinkButton href="/account/library" size="sm">Open library</LinkButton>}
        description="Local fixture mode shows the intended account shape until Clerk, database, and Stripe credentials are connected."
        eyebrow="Local account fixture"
        title="Account dashboard"
      />
      <div className="grid gap-6 p-4 sm:p-6">
        <section className="grid gap-4 md:grid-cols-3">
          {[
            ["Owned products", items.length],
            ["Ready codes", items.filter((item) => item.installCode?.status === "active").length],
            ["Install events", 0],
          ].map(([label, value]) => (
            <div className="rounded-md border border-border bg-card p-4" key={label}>
              <p className="font-mono text-[11px] uppercase text-muted-foreground">{label}</p>
              <p className="mt-2 text-3xl font-semibold">{value}</p>
            </div>
          ))}
        </section>
        <section>
          <div className="mb-4 flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold">Recent library items</h2>
            <Badge variant="outline">mock data</Badge>
          </div>
          <LibraryList items={items.slice(0, 2)} />
        </section>
      </div>
    </>
  );
}
