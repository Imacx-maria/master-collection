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
      <div className="mx-auto max-w-[1400px] px-6 py-8 sm:px-10 lg:px-14">
        <LinkButton href="/">Back to catalog</LinkButton>
      </div>
    </>
  );
}
