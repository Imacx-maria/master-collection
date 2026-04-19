import { PageHeading } from "@/components/page-heading";
import { Badge } from "@/components/ui/badge";

export default function InstallationsPage() {
  return (
    <>
      <PageHeading
        description="Install events will appear after the Webflow app reports code redemption and package installation progress."
        eyebrow="Account"
        title="Installations"
      />
      <div className="p-4 sm:p-6">
        <div className="rounded-md border border-border bg-card p-5">
          <Badge variant="outline">waiting for app events</Badge>
          <h2 className="mt-4 text-lg font-semibold">No install events yet</h2>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            The API boundary exists in this MVP; real rows begin when the Webflow Designer Extension sends install events.
          </p>
        </div>
      </div>
    </>
  );
}
