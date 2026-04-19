import { PageHeading } from "@/components/page-heading";
import { LinkButton } from "@/components/ui/button";

export default function CheckoutCancelPage() {
  return (
    <>
      <PageHeading
        description="No payment was completed. You can return to the catalog and start again."
        eyebrow="Checkout"
        title="Checkout canceled"
      />
      <div className="p-4 sm:p-6">
        <LinkButton href="/">Back to catalog</LinkButton>
      </div>
    </>
  );
}
