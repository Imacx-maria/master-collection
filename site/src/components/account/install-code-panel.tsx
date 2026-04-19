import { Copy, KeyRound } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/format";
import type { InstallCode } from "@/lib/account";

export function InstallCodePanel({ installCode }: { installCode?: InstallCode }) {
  if (!installCode) {
    return (
      <div className="rounded-md border border-border p-4">
        <Badge variant="warning">pending</Badge>
        <h2 className="mt-3 text-sm font-semibold">Install code pending</h2>
        <p className="mt-2 text-sm leading-6 text-muted-foreground">
          Fulfillment will create a hashed install code after payment confirmation.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-md border-2 border-foreground bg-card p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="font-mono text-[11px] uppercase text-muted-foreground">Install code</p>
          <div className="mt-2 flex items-center gap-2 rounded-md border border-border bg-muted px-3 py-2 font-mono text-sm">
            <KeyRound aria-hidden="true" className="size-3" />
            {installCode.mockPlainCode ?? "Hidden in production"}
          </div>
        </div>
        <Button size="sm" type="button" variant="secondary">
          <Copy aria-hidden="true" className="size-3" />
          Copy
        </Button>
      </div>
      <dl className="mt-4 grid gap-2 text-xs text-muted-foreground sm:grid-cols-3">
        <div>
          <dt className="font-mono uppercase">Status</dt>
          <dd className="mt-1 text-foreground">{installCode.status}</dd>
        </div>
        <div>
          <dt className="font-mono uppercase">Uses</dt>
          <dd className="mt-1 text-foreground">
            {installCode.useCount}/{installCode.maxUses}
          </dd>
        </div>
        <div>
          <dt className="font-mono uppercase">Expires</dt>
          <dd className="mt-1 text-foreground">
            {installCode.expiresAt ? formatDate(installCode.expiresAt) : "No expiry"}
          </dd>
        </div>
      </dl>
    </div>
  );
}
