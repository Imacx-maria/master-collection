import { PageHeading } from "@/components/page-heading";
import { Badge } from "@/components/ui/badge";
import { orders } from "@/lib/account";
import { formatDate, formatMoney } from "@/lib/format";

export default function BillingPage() {
  return (
    <>
      <PageHeading
        description="Read-only order status for the first MVP. Stripe receipts can be linked after live Checkout is configured."
        eyebrow="Account"
        title="Billing"
      />
      <div className="p-4 sm:p-6">
        <div className="overflow-hidden rounded-md border border-border">
          <table className="w-full min-w-[620px] text-left text-sm">
            <thead className="border-b border-border bg-muted">
              <tr>
                <th className="px-4 py-3 font-medium">Order</th>
                <th className="px-4 py-3 font-medium">Provider</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Amount</th>
                <th className="px-4 py-3 font-medium">Created</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr className="border-b border-border last:border-b-0" key={order.id}>
                  <td className="px-4 py-3 font-mono text-xs">{order.id}</td>
                  <td className="px-4 py-3">{order.provider}</td>
                  <td className="px-4 py-3"><Badge variant="outline">{order.status}</Badge></td>
                  <td className="px-4 py-3">{formatMoney(order.amountCents, order.currency)}</td>
                  <td className="px-4 py-3">{formatDate(order.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
