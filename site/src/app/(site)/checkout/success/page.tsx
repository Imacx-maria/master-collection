import { PageHeading } from "@/components/page-heading";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";

export default function CheckoutSuccessPage() {
  return (
    <>
      <PageHeading
        description="Webhook fulfillment is the source of truth. This page only points buyers toward their account library while access is prepared."
        eyebrow="Checkout"
        title="Checkout success"
      />
      <div className="mx-auto max-w-2xl p-4 sm:p-6">
        <div className="rounded-md border border-border bg-card p-5">
          <Badge variant="outline">fulfillment pending webhook</Badge>
          <h2 className="mt-4 text-xl font-semibold">Preparing library access</h2>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            Stripe redirected back successfully. The webhook grants the entitlement and install code idempotently.
          </p>
          <div className="mt-5">
            <LinkButton href="/account/library">Open library</LinkButton>
          </div>
        </div>
      </div>
    </>
  );
}
